$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

py -3 -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
$Requirements = Join-Path "개발" "requirements.txt"
$Launcher = Join-Path "실행" "mark_down.py"
python -m pip install -r $Requirements
python $Launcher --list-supported

Write-Host ""
Write-Host "Setup complete. Try:"
Write-Host "  .\실행\run_windows.bat --input C:\path\to\folder --dry-run"
