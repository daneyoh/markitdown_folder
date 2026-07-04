#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [[ -f "$ROOT_DIR/.venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT_DIR/.venv/bin/activate"
  PYTHON_BIN="python"
  if ! "$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
    printf 'Python 3.10+ is required. Re-run 실행/macOS/setup.sh after installing Python 3.10+.\n' >&2
    exit 1
  fi
else
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
    printf 'Python 3.10+ is required. Run 실행/macOS/setup.sh after installing Python 3.10+.\n' >&2
    exit 1
  }
fi

"$PYTHON_BIN" "$ROOT_DIR/실행/mark_down.py" "$@"
