#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$ROOT_DIR"

find_python() {
  for candidate in python3.12 python3.11 python3.10 python3; do
    if command -v "$candidate" >/dev/null 2>&1 &&
      "$candidate" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

PYTHON_BIN="$(find_python)" || {
  printf 'Python 3.10+ is required. Install Python 3.10 or newer first.\n' >&2
  exit 1
}

"$PYTHON_BIN" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r 개발/requirements.txt
python 실행/mark_down.py --list-supported
mkdir -p 변환할PDF

printf '\nSetup complete. Try:\n'
printf '  기본 작업 폴더: %s/변환할PDF\n' "$ROOT_DIR"
printf '  실행/macOS/open_gui.command\n'
