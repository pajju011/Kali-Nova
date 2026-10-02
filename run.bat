@echo off
REM Kalinova - Windows Launch Script
title Kali-Nova Security Control Center

set ROOT_DIR=%~dp0
set APP_DIR=%ROOT_DIR%kalinova

if exist "%APP_DIR%\venv\Scripts\python.exe" (
    cd /d "%APP_DIR%"
    echo [Kalinova] Launching using virtual environment...
    start "" "venv\Scripts\python.exe" main.py
) else if exist "%ROOT_DIR%venv\Scripts\python.exe" (
    cd /d "%APP_DIR%"
    echo [Kalinova] Launching using virtual environment...
    start "" "%ROOT_DIR%venv\Scripts\python.exe" main.py
) else (
    cd /d "%APP_DIR%"
    echo [Kalinova] Virtual environment not found. Attempting to launch with system Python...
    start "" python main.py
)
