@echo off
title Compound Management System

echo.
echo 🧪 Starting Compound Management System...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup_windows.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if dependencies are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ❌ Dependencies not installed. Please run setup_windows.bat first.
    pause
    exit /b 1
)

REM Start the application
echo 🚀 Launching application...
echo 📱 Application will be available at: http://localhost:8081
echo ⏹️  Press Ctrl+C to stop the server
echo.

python run.py

pause