#!/bin/bash

# Stock Screener - Restart Script
# Usage: bash restart.sh

set -e

echo "Stopping Stock Screener..."
pkill -f "python3 app.py" || echo "No process found"
sleep 2

echo "Starting Stock Screener..."
cd "$(dirname "$0")"
source venv/bin/activate

mkdir -p logs
nohup python3 app.py > logs/app.log 2>&1 &

echo "✅ Stock Screener restarted!"
echo "📋 View logs: tail -f logs/app.log"
