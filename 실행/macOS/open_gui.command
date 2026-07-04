#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [[ -f "$ROOT_DIR/.venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT_DIR/.venv/bin/activate"
  python "$ROOT_DIR/실행/auto_convert.py"
  read -r -p "완료. Enter를 누르면 닫힙니다." _ || true
  exit 0
fi

for candidate in python3.12 python3.11 python3.10 python3; do
  if command -v "$candidate" >/dev/null 2>&1 &&
    "$candidate" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
    "$candidate" "$ROOT_DIR/실행/auto_convert.py"
    read -r -p "완료. Enter를 누르면 닫힙니다." _ || true
    exit 0
  fi
done

osascript -e 'display dialog "Python 3.10+가 필요합니다. 실행/macOS/setup.command를 먼저 실행하세요." buttons {"확인"} default button "확인"'
