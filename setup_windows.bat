@echo off
title Compound Management System Setup

echo.
echo 🧪 Setting up Compound Management System...
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo    Please install Python 3.8 or higher from: https://www.python.org/downloads/
    echo    Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo ✅ Python detected

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Create instance directory if it doesn't exist
if not exist "instance" mkdir instance

REM Initialize database
echo 🗄️  Initializing database...
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ Database initialized successfully')"

REM Create uploads directories
echo 📁 Creating upload directories...
if not exist "app\uploads\structures" mkdir app\uploads\structures
if not exist "app\uploads\data" mkdir app\uploads\data

REM Copy environment example if .env doesn't exist
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env
        echo ✅ Environment file created from example
    ) else (
        echo ⚠️  No .env file found. Using default configuration.
    )
)

echo.
echo 🎉 Setup completed successfully!
echo ==========================================
echo.
echo To start the application:
echo   1. Run: start_windows.bat
echo   2. Open: http://localhost:8081
echo.
echo Happy researching! 🧬
echo.
pause