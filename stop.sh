#!/bin/bash

# Stock Screener - Stop Script
# Usage: bash stop.sh

echo "Stopping Stock Screener..."
pkill -f "python3 app.py" && echo "✅ Stopped successfully" || echo "⚠️  No process found"
