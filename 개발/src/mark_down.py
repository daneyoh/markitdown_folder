#!/usr/bin/env python3
"""One-shot local folder to Markdown converter using MarkItDown."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Protocol, Sequence

SUPPORTED_EXTENSIONS = {
    "pdf",
    "docx",
    "pptx",
    "xlsx",
    "html",
    "txt",
    "csv",
    "json",
    "xml",
}

DEFAULT_OUTPUT_DIR = Path("변환")
DEFAULT_PROCESSED_DIR = Path("원본완료")
DEFAULT_LOG_FILE = Path("logs/conversions.jsonl")
MIN_PYTHON_VERSION = (3, 10)

GENERATED_DIR_NAMES = {
    "변환",
    "원본완료",
    "markdown",
    "processed",
    "logs",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
}


class Converter(Protocol):
    def convert(self, source: Path) -> str:
        """Convert a local file to Markdown text."""


@dataclass(frozen=True)
class ConversionPlan:
    source: Path
    extension: str
    markdown_path: Path
    processed_path: Path


@dataclass
class ConversionResult:
    source: Path
    extension: str
    status: str
    output: Optional[Path] = None
    moved_to: Optional[Path] = None
    error: Optional[str] = None
    reason: Optional[str] = None


@dataclass
class Summary:
    planned: int = 0
    converted: int = 0
    skipped: int = 0
    failed: int = 0
    moved: int = 0
    results: list[ConversionResult] = field(default_factory=list)

    def add(self, result: ConversionResult) -> None:
        self.results.append(result)
        if result.status == "planned":
            self.planned += 1
        elif result.status == "converted":
            self.converted += 1
            if result.moved_to is not None:
                self.moved += 1
        elif result.status == "failed":
            self.failed += 1
        else:
            self.skipped += 1


class MarkItDownConverter:
    """Adapter around MarkItDown so tests can inject a fake converter."""

    def __init__(self) -> None:
        if sys.version_info < MIN_PYTHON_VERSION:
            raise RuntimeError(
                "Python 3.10+ is required for Microsoft MarkItDown. "
                f"Current Python: {sys.version_info.major}.{sys.version_info.minor}"
            )
        try:
            from markitdown import MarkItDown  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "MarkItDown is not installed. Install dependencies with: "
                "python -m pip install -r 개발/requirements.txt"
            ) from exc
        self._client = MarkItDown()

    def convert(self, source: Path) -> str:
        if hasattr(self._client, "convert_local"):
            result = self._client.convert_local(str(source))
        else:
            result = self._client.convert(str(source))
        return extract_markdown_text(result)


def extract_markdown_text(result: object) -> str:
    for attr in ("text_content", "markdown", "text"):
        value = getattr(result, attr, None)
        if isinstance(value, str):
            return value
    if isinstance(result, str):
        return result
    raise TypeError("MarkItDown returned an unsupported result shape")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_extension(path: Path) -> str:
    return path.suffix.lower().lstrip(".")


def is_supported_extension(extension: str) -> bool:
    return extension.lower().lstrip(".") in SUPPORTED_EXTENSIONS


def is_supported_file(path: Path) -> bool:
    return path.is_file() and is_supported_extension(normalize_extension(path))


def should_skip_path(path: Path) -> bool:
    if path.name.startswith("."):
        return True
    return path.is_dir() and path.name.lower() in GENERATED_DIR_NAMES


def scan_root_only(input_dir: Path) -> list[Path]:
    """Return supported root-level files only; v1 intentionally does not recurse."""
    candidates: list[Path] = []
    for child in sorted(input_dir.iterdir(), key=lambda item: item.name.lower()):
        if should_skip_path(child) or child.is_dir():
            continue
        if is_supported_file(child):
            candidates.append(child)
    return candidates


def collision_safe_path(path: Path) -> Path:
    if not path.exists():
        return path

    index = 1
    while True:
        candidate = path.with_name(f"{path.stem}-{index:03d}{path.suffix}")
        if not candidate.exists():
            return candidate
        index += 1


def resolve_under_input(input_dir: Path, path: Path) -> Path:
    expanded = path.expanduser()
    if expanded.is_absolute():
        return expanded
    return input_dir / expanded


def resolve_targets(base_dir: Path, output_dir: Path, processed_dir: Path, log_file: Path) -> tuple[Path, Path, Path]:
    return (
        resolve_under_input(base_dir, output_dir),
        resolve_under_input(base_dir, processed_dir),
        resolve_under_input(base_dir, log_file),
    )


def build_plan(source: Path, markdown_root: Path, processed_root: Path) -> ConversionPlan:
    extension = normalize_extension(source)
    markdown_path = collision_safe_path(markdown_root / extension / f"{source.stem}.md")
    processed_path = collision_safe_path(processed_root / extension / source.name)
    return ConversionPlan(
        source=source,
        extension=extension,
        markdown_path=markdown_path,
        processed_path=processed_path,
    )


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    return value


def write_log(log_file: Path, event: dict[str, Any]) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {"timestamp": utc_now_iso(), **event}
    normalized = {key: json_ready(value) for key, value in payload.items()}
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(normalized, ensure_ascii=False, sort_keys=True) + "\n")


def write_text_no_overwrite(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    created = False
    try:
        with path.open("x", encoding="utf-8") as handle:
            created = True
            handle.write(text)
            if not text.endswith("\n"):
                handle.write("\n")
    except Exception:
        if created:
            try:
                path.unlink()
            except FileNotFoundError:
                pass
        raise


def move_file_no_overwrite(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(destination), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)
    try:
        with source.open("rb") as reader, os.fdopen(fd, "wb") as writer:
            fd = -1
            shutil.copyfileobj(reader, writer)
        shutil.copystat(source, destination)
    except Exception:
        if fd != -1:
            os.close(fd)
        try:
            destination.unlink()
        except FileNotFoundError:
            pass
        raise
    source.unlink()


def plan_dry_run(plan: ConversionPlan) -> ConversionResult:
    return ConversionResult(
        source=plan.source,
        extension=plan.extension,
        status="planned",
        output=plan.markdown_path,
        moved_to=plan.processed_path,
        reason="dry-run",
    )


def convert_plan(plan: ConversionPlan, converter: Converter, log_file: Path) -> ConversionResult:
    markdown_written = False
    try:
        markdown_text = converter.convert(plan.source)
        write_text_no_overwrite(plan.markdown_path, markdown_text)
        markdown_written = True
        move_file_no_overwrite(plan.source, plan.processed_path)
    except Exception as exc:
        if markdown_written:
            try:
                plan.markdown_path.unlink()
            except FileNotFoundError:
                pass
        result = ConversionResult(
            source=plan.source,
            extension=plan.extension,
            status="failed",
            output=plan.markdown_path,
            moved_to=plan.processed_path,
            error=str(exc),
        )
        write_log(
            log_file,
            {
                "status": "failed",
                "source": plan.source,
                "output": plan.markdown_path,
                "moved_to": plan.processed_path,
                "extension": plan.extension,
                "error": str(exc),
                "error_type": type(exc).__name__,
            },
        )
        return result

    result = ConversionResult(
        source=plan.source,
        extension=plan.extension,
        status="converted",
        output=plan.markdown_path,
        moved_to=plan.processed_path,
    )
    write_log(
        log_file,
        {
            "status": "converted",
            "source": plan.source,
            "output": plan.markdown_path,
            "moved_to": plan.processed_path,
            "extension": plan.extension,
        },
    )
    return result


def convert_folder(
    input_dir: Path,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    log_file: Path = DEFAULT_LOG_FILE,
    converter: Optional[Converter] = None,
    dry_run: bool = False,
) -> Summary:
    input_dir = input_dir.expanduser().resolve()
    if not input_dir.exists():
        raise FileNotFoundError(f"Input folder does not exist: {input_dir}")
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input path must be a local folder: {input_dir}")

    markdown_root, processed_root, resolved_log_file = resolve_targets(
        input_dir, output_dir, processed_dir, log_file
    )

    summary = Summary()
    supported_files = set(scan_root_only(input_dir))
    active_converter: Optional[Converter] = converter
    if supported_files and not dry_run and active_converter is None:
        active_converter = MarkItDownConverter()

    for child in sorted(input_dir.iterdir(), key=lambda item: item.name.lower()):
        if should_skip_path(child) or child.is_dir():
            continue
        if child in supported_files:
            plan = build_plan(child, markdown_root, processed_root)
            if dry_run:
                summary.add(plan_dry_run(plan))
            else:
                if active_converter is None:
                    raise RuntimeError("Converter was not initialized")
                summary.add(convert_plan(plan, active_converter, resolved_log_file))
            continue

        result = ConversionResult(
            source=child,
            extension=normalize_extension(child),
            status="skipped",
            reason="unsupported-extension",
        )
        summary.add(result)
        if not dry_run:
            write_log(
                resolved_log_file,
                {
                    "status": "skipped",
                    "source": child,
                    "extension": result.extension,
                    "reason": result.reason,
                },
            )

    return summary


def convert_files(
    files: Sequence[Path],
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    log_file: Path = DEFAULT_LOG_FILE,
    converter: Optional[Converter] = None,
    dry_run: bool = False,
) -> Summary:
    summary = Summary()
    resolved_files: list[Path] = []
    for source in files:
        resolved_source = source.expanduser().resolve()
        if not resolved_source.exists():
            raise FileNotFoundError(f"Selected file does not exist: {resolved_source}")
        if not resolved_source.is_file():
            raise IsADirectoryError(f"Selected path must be a file: {resolved_source}")
        resolved_files.append(resolved_source)

    supported_files = [source for source in resolved_files if is_supported_file(source)]
    active_converter: Optional[Converter] = converter
    if supported_files and not dry_run and active_converter is None:
        active_converter = MarkItDownConverter()

    for source in resolved_files:
        if not is_supported_file(source):
            result = ConversionResult(
                source=source,
                extension=normalize_extension(source),
                status="skipped",
                reason="unsupported-extension",
            )
            summary.add(result)
            if not dry_run:
                _, _, resolved_log_file = resolve_targets(source.parent, output_dir, processed_dir, log_file)
                write_log(
                    resolved_log_file,
                    {
                        "status": "skipped",
                        "source": source,
                        "extension": result.extension,
                        "reason": result.reason,
                    },
                )
            continue

        markdown_root, processed_root, resolved_log_file = resolve_targets(
            source.parent, output_dir, processed_dir, log_file
        )
        plan = build_plan(source, markdown_root, processed_root)
        if dry_run:
            summary.add(plan_dry_run(plan))
            continue
        if active_converter is None:
            raise RuntimeError("Converter was not initialized")
        summary.add(convert_plan(plan, active_converter, resolved_log_file))

    return summary


def print_summary(summary: Summary, dry_run: bool = False) -> None:
    prefix = "DRY RUN - " if dry_run else ""
    print(
        f"{prefix}planned={summary.planned} converted={summary.converted} "
        f"skipped={summary.skipped} failed={summary.failed} moved={summary.moved}"
    )
    for result in summary.results:
        if result.status == "planned":
            print(f"planned: {result.source} -> {result.output}; move -> {result.moved_to}")
        elif result.status == "converted":
            print(f"converted: {result.source} -> {result.output}; moved -> {result.moved_to}")
        elif result.status == "failed":
            print(f"failed: {result.source}: {result.error}", file=sys.stderr)
        else:
            print(f"skipped: {result.source} ({result.reason})")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert supported files in one local folder into Markdown with MarkItDown."
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        default=None,
        help="Local folder to scan once. Required unless --list-supported is used.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Markdown output folder. Relative paths are created under the input folder.",
    )
    parser.add_argument(
        "--processed",
        type=Path,
        default=DEFAULT_PROCESSED_DIR,
        help="Folder for successfully converted originals. Relative paths are under the input folder.",
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=DEFAULT_LOG_FILE,
        help="JSONL conversion log path. Relative paths are under the input folder.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned conversions and moves without writing files or moving originals.",
    )
    parser.add_argument(
        "--list-supported",
        action="store_true",
        help="Print supported extensions and exit.",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_supported:
        print("\n".join(sorted(SUPPORTED_EXTENSIONS)))
        return 0

    if args.input is None:
        parser.print_usage(sys.stderr)
        print("error: --input is required unless --list-supported is used", file=sys.stderr)
        return 2

    try:
        summary = convert_folder(
            input_dir=args.input,
            output_dir=args.output,
            processed_dir=args.processed,
            log_file=args.log,
            dry_run=args.dry_run,
        )
        print_summary(summary, dry_run=args.dry_run)
        return 1 if summary.failed else 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
