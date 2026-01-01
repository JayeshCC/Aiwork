@echo off
echo ==========================================
echo      AIWork Setup Script (Windows)
echo ==========================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist .venv (
    echo [*] Creating virtual environment...
    python -m venv .venv
) else (
    echo [*] Virtual environment already exists.
)

:: Activate and install dependencies
echo [*] Activating virtual environment...
call .venv\Scripts\activate

echo [*] Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo ==========================================
echo      Setup Complete! 
echo ==========================================
echo.
echo To start, run:
echo    .venv\Scripts\activate
echo    python examples/quickstart.py
echo.
pause
