#!/bin/bash

# Compound Management System Setup Script
# This script sets up the application for first-time use

echo "🧪 Setting up Compound Management System..."
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    echo "   Download from: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version is installed, but Python $required_version or higher is required."
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create instance directory if it doesn't exist
mkdir -p instance

# Initialize database
echo "🗄️  Initializing database..."
python3 -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('✅ Database initialized successfully')
"

# Create uploads directories
echo "📁 Creating upload directories..."
mkdir -p app/uploads/structures
mkdir -p app/uploads/data

# Copy environment example if .env doesn't exist
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Environment file created from example"
    else
        echo "⚠️  No .env file found. Using default configuration."
    fi
fi

echo ""
echo "🎉 Setup completed successfully!"
echo "=========================================="
echo ""
echo "To start the application:"
echo "  1. Run: source venv/bin/activate"
echo "  2. Run: python run.py"
echo "  3. Open: http://localhost:8081"
echo ""
echo "Or simply run: ./start.sh"
echo ""

# Make start script executable
chmod +x start.sh 2>/dev/null || true

echo "Happy researching! 🧬"