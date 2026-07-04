@echo off
setlocal

set "ROOT_DIR=%~dp0.."
if exist "%ROOT_DIR%\.venv\Scripts\activate.bat" call "%ROOT_DIR%\.venv\Scripts\activate.bat"

python "%ROOT_DIR%\mark_down.py" %*
