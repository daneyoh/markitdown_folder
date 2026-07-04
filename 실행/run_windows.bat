@echo off
setlocal

set "ROOT_DIR=%~dp0.."
if exist "%ROOT_DIR%\.venv\Scripts\activate.bat" (
  call "%ROOT_DIR%\.venv\Scripts\activate.bat"
  python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
  if errorlevel 1 (
    echo Python 3.10+ is required. Re-run setup after installing Python 3.10 or newer.
    exit /b 1
  )
  python "%~dp0mark_down.py" %*
  exit /b %errorlevel%
)

py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 (
  echo Python 3.10+ is required. Run .\실행\setup_windows.ps1 after installing Python 3.10 or newer.
  exit /b 1
)

py -3 "%~dp0mark_down.py" %*
