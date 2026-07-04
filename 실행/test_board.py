#!/usr/bin/env python3
"""Create a local test board and verify default-folder conversion."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "개발" / "src"
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(ROOT_DIR / "실행"))

from auto_convert import format_summary  # noqa: E402
from mark_down import convert_files  # noqa: E402

BOARD_DIR = ROOT_DIR / "테스트보드"
BOARD_INPUT_DIR = BOARD_DIR / "변환할PDF"
BOARD_REPORT = BOARD_DIR / "TEST_BOARD.md"


def main() -> int:
    BOARD_INPUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    source = BOARD_INPUT_DIR / f"sample_{stamp}.txt"
    source.write_text("test board sample\n", encoding="utf-8")

    summary = convert_files([source])
    markdown_dir = BOARD_INPUT_DIR / "변환" / "txt"
    processed_dir = BOARD_INPUT_DIR / "원본완료" / "txt"
    markdown_files = sorted(markdown_dir.glob(f"sample_{stamp}*.md"))
    processed_files = sorted(processed_dir.glob(f"sample_{stamp}*.txt"))

    passed = summary.failed == 0 and len(markdown_files) == 1 and len(processed_files) == 1
    report = [
        "# Test Board",
        "",
        f"- status: {'PASS' if passed else 'FAIL'}",
        f"- input: {source}",
        f"- markdown_dir: {markdown_dir}",
        f"- processed_dir: {processed_dir}",
        f"- markdown_found: {markdown_files[0] if markdown_files else 'NONE'}",
        f"- processed_found: {processed_files[0] if processed_files else 'NONE'}",
        "",
        "## Summary",
        "",
        "```text",
        format_summary(summary),
        "```",
    ]
    BOARD_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"TEST_BOARD={'PASS' if passed else 'FAIL'}")
    print(f"REPORT={BOARD_REPORT}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
