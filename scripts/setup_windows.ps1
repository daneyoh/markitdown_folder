$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

py -3.10 -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python bin\mark_down.py --list-supported

Write-Host ""
Write-Host "Setup complete. Try:"
Write-Host "  .\scripts\run_windows.bat --input C:\path\to\folder --dry-run"
