#!/bin/bash

# Compound Management System Startup Script

echo "🧪 Starting Compound Management System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "❌ Dependencies not installed. Please run ./setup.sh first."
    exit 1
fi

# Start the application
echo "🚀 Launching application..."
echo "📱 Application will be available at: http://localhost:8081"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

python run.py