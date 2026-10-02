@echo off
REM Kalinova - Windows Launch Script
title Kali-Nova Security Control Center

cd /d "%~dp0"

if exist "venv\Scripts\python.exe" (
    echo [Kalinova] Launching using virtual environment...
    start "" "venv\Scripts\python.exe" main.py
) else (
    echo [Kalinova] Virtual environment not found in %~dp0venv.
    echo [Kalinova] Attempting to launch with system Python...
    start "" python main.py
)
