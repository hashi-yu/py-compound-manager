#!/bin/bash

# Compound Management System - One-Click Launcher
# This script will automatically set up and launch the application

cd "$(dirname "$0")"

echo "🧪 Compound Management System Launcher"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo ""
    echo "Please install Python 3.8 or higher from:"
    echo "https://www.python.org/downloads/"
    echo ""
    echo "Make sure to check 'Add Python to PATH' during installation."
    read -p "Press Enter to exit..."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version detected, but Python $required_version or higher is required."
    echo ""
    echo "Please update Python from: https://www.python.org/downloads/"
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment (first time setup)..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment."
        echo "Please make sure Python 3 is properly installed."
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check and install dependencies
echo "📚 Checking dependencies..."
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Installing dependencies (this may take a few minutes)..."
    pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies."
        echo "Please check your internet connection and try again."
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo "✅ Dependencies installed successfully"
else
    echo "✅ Dependencies already installed"
fi

# Initialize database if it doesn't exist
if [ ! -f "instance/compounds.db" ]; then
    echo "🗄️  Initializing database..."
    mkdir -p instance
    mkdir -p app/uploads/structures
    mkdir -p app/uploads/data
    
    python3 -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('✅ Database initialized successfully')
" 2>/dev/null
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to initialize database."
        read -p "Press Enter to exit..."
        exit 1
    fi
else
    echo "✅ Database already exists"
fi

# Start the application
echo ""
echo "🚀 Starting Compound Management System..."
echo "📱 Application will open in your browser shortly..."
echo "🌐 Manual access: http://localhost:8081"
echo "⏹️  Press Ctrl+C in this window to stop the server"
echo ""

# Open browser after a short delay
sleep 3 && open http://localhost:8081 &

# Start Flask application
python run.py

# Cleanup message
echo ""
echo "👋 Compound Management System stopped."
echo "To restart, simply double-click start.command again."
read -p "Press Enter to close..."