# Kalinova - Windows PowerShell Launch Script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AppDir = Join-Path $ScriptDir "kalinova"
$VenvPython = Join-Path $AppDir "venv\Scripts\python.exe"

Set-Location $AppDir

if (Test-Path $VenvPython) {
    Write-Host "[Kalinova] Launching using virtual environment..." -ForegroundColor Cyan
    Start-Process -FilePath $VenvPython -ArgumentList "main.py" -WorkingDirectory $AppDir
} else {
    Write-Host "[Kalinova] Virtual environment not found. Attempting to launch with system Python..." -ForegroundColor Yellow
    Start-Process -FilePath "python" -ArgumentList "main.py" -WorkingDirectory $AppDir
}
