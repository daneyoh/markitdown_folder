#!/usr/bin/env python3
"""Auto-convert files from the default input folder without GUI dependencies."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "개발" / "src"
sys.path.insert(0, str(SRC_DIR))

from mark_down import Summary, convert_files, scan_root_only  # noqa: E402

DEFAULT_INPUT_DIR = ROOT_DIR / "변환할PDF"
DEFAULT_SKIP_NAMES = {"README.txt"}


def collect_default_files(input_dir: Path = DEFAULT_INPUT_DIR) -> list[Path]:
    if not input_dir.exists():
        input_dir.mkdir(parents=True, exist_ok=True)
    return [path for path in scan_root_only(input_dir) if path.name not in DEFAULT_SKIP_NAMES]


def format_summary(summary: Summary) -> str:
    lines = [
        f"converted={summary.converted} skipped={summary.skipped} failed={summary.failed} moved={summary.moved}"
    ]
    for result in summary.results:
        if result.status == "converted":
            lines.append(f"converted: {result.source.name} -> {result.output}")
        elif result.status == "failed":
            lines.append(f"failed: {result.source.name}: {result.error}")
        elif result.status == "planned":
            lines.append(f"planned: {result.source.name} -> {result.output}")
        else:
            lines.append(f"skipped: {result.source.name} ({result.reason})")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    _ = argv
    files = collect_default_files()
    if not files:
        print(f"변환할 파일 없음: {DEFAULT_INPUT_DIR}")
        print(f"PDF/문서 파일을 여기에 넣고 다시 실행: {DEFAULT_INPUT_DIR}")
        return 0

    summary = convert_files(files)
    print(format_summary(summary))
    print(f"Markdown 저장: {DEFAULT_INPUT_DIR / '변환'}")
    print(f"원본 이동: {DEFAULT_INPUT_DIR / '원본완료'}")
    return 1 if summary.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
