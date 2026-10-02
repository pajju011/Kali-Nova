@echo off
REM Kalinova - Windows Launch Script
title Kali-Nova Security Control Center

set ROOT_DIR=%~dp0
set APP_DIR=%ROOT_DIR%kalinova

cd /d "%APP_DIR%"

if exist "venv\Scripts\python.exe" (
    echo [Kalinova] Launching using virtual environment...
    start "" "venv\Scripts\python.exe" main.py
) else (
    echo [Kalinova] Virtual environment not found in %APP_DIR%\venv.
    echo [Kalinova] Attempting to launch with system Python...
    start "" python main.py
)
