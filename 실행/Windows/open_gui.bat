@echo off
setlocal

set "ROOT_DIR=%~dp0..\.."
if exist "%ROOT_DIR%\.venv\Scripts\python.exe" (
  "%ROOT_DIR%\.venv\Scripts\python.exe" "%ROOT_DIR%\실행\auto_convert.py"
  pause
  exit /b 0
)

py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 (
  echo Python 3.10+ is required. Run .\실행\Windows\setup.ps1 first.
  pause
  exit /b 1
)

py -3 "%ROOT_DIR%\실행\auto_convert.py"
pause
