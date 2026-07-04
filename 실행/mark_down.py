#!/usr/bin/env python3
"""Launcher for the Mark Down folder converter."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "개발" / "src"
sys.path.insert(0, str(SRC_DIR))

from mark_down import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
