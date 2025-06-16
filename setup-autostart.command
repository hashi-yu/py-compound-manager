#!/bin/bash

# Compound Management System - Auto-Start Setup
# This script sets up the application to start automatically at login

cd "$(dirname "$0")"

echo "🔧 Compound Management System - Auto-Start Setup"
echo "==============================================="
echo ""

# Create logs directory
mkdir -p logs

# Copy plist to LaunchAgents
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_FILE="com.compound.manager.plist"

echo "📋 Installing launch agent..."

# Ensure LaunchAgents directory exists
mkdir -p "$LAUNCH_AGENTS_DIR"

# Copy the plist file
cp "$PLIST_FILE" "$LAUNCH_AGENTS_DIR/"

if [ $? -eq 0 ]; then
    echo "✅ Launch agent installed successfully"
else
    echo "❌ Failed to install launch agent"
    exit 1
fi

# Load the launch agent
echo "🚀 Loading launch agent..."
launchctl load "$LAUNCH_AGENTS_DIR/$PLIST_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Launch agent loaded successfully"
    echo ""
    echo "🎉 Setup complete!"
    echo ""
    echo "The Compound Management System will now:"
    echo "• Start automatically when you log in"
    echo "• Be available at: http://localhost:8081"
    echo "• Run in the background"
    echo ""
    echo "💡 You can bookmark http://localhost:8081 in your browser!"
    echo ""
    echo "To disable auto-start, run: ./disable-autostart.command"
else
    echo "❌ Failed to load launch agent"
    echo "Please check the log files in the logs/ directory"
    exit 1
fi

read -p "Press Enter to continue..."