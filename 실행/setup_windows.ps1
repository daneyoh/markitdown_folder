$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

$VersionCheck = "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
py -3 -c $VersionCheck
if ($LASTEXITCODE -ne 0) {
    throw "Python 3.10+ is required. Install Python 3.10 or newer first."
}

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
