#!/bin/bash

# Compound Management System - Disable Auto-Start
# This script disables the automatic startup of the application

echo "🛑 Compound Management System - Disable Auto-Start"
echo "================================================="
echo ""

LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_FILE="com.compound.manager.plist"

# Unload the launch agent
echo "⏹️  Unloading launch agent..."
launchctl unload "$LAUNCH_AGENTS_DIR/$PLIST_FILE" 2>/dev/null

# Remove the plist file
echo "🗑️  Removing launch agent..."
rm -f "$LAUNCH_AGENTS_DIR/$PLIST_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Auto-start disabled successfully"
    echo ""
    echo "The Compound Management System will no longer start automatically."
    echo "You can still start it manually using start.command"
    echo ""
    echo "To re-enable auto-start, run: ./setup-autostart.command"
else
    echo "❌ Failed to disable auto-start"
fi

echo ""
read -p "Press Enter to continue..."