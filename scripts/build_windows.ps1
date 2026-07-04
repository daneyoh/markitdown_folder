$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

$Activate = Join-Path $RootDir ".venv\Scripts\Activate.ps1"
if (Test-Path $Activate) {
    . $Activate
}

python -m PyInstaller --onedir --name mark-down --icon assets\icons\mark-down.ico --paths src bin\mark_down.py
Write-Host "Built Windows onedir package at $RootDir\dist\mark-down"
