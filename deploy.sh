#!/bin/bash

# Stock Screener - Oracle Cloud Always Free Deployment Script
# Usage: bash deploy.sh

set -e

echo "=========================================="
echo "Stock Screener - Deployment Setup"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Step 1: Update system
echo -e "${BLUE}[1/7] Updating system packages...${NC}"
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git curl

# Step 2: Clone repository
echo -e "${BLUE}[2/7] Cloning repository...${NC}"
if [ -d "stock-screener" ]; then
    echo "Repository already exists, pulling latest changes..."
    cd stock-screener
    git pull origin main
else
    git clone https://github.com/amudalabhoomika-pixel/stock-screener.git
    cd stock-screener
fi

# Step 3: Create virtual environment
echo -e "${BLUE}[3/7] Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Step 4: Install dependencies
echo -e "${BLUE}[4/7] Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Step 5: Create .env file if it doesn't exist
echo -e "${BLUE}[5/7] Setting up .env configuration...${NC}"
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    read -p "Enter TELEGRAM_BOT_TOKEN: " TOKEN
    read -p "Enter TELEGRAM_CHAT_ID: " CHAT_ID
    
    cat > .env << EOF
TELEGRAM_BOT_TOKEN=$TOKEN
TELEGRAM_CHAT_ID=$CHAT_ID
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Step 6: Stop existing process if running
echo -e "${BLUE}[6/7] Checking for existing processes...${NC}"
pkill -f "python3 app.py" || true
sleep 2

# Step 7: Start the application
echo -e "${BLUE}[7/7] Starting Stock Screener...${NC}"
nohup python3 app.py > logs/app.log 2>&1 &

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo "📊 Stock Screener is now running!"
echo ""
echo "📍 Access your app at:"
echo "   http://YOUR_VM_IP:5000"
echo ""
echo "📋 To view logs:"
echo "   tail -f logs/app.log"
echo ""
echo "⏹️  To stop the app:"
echo "   pkill -f 'python3 app.py'"
echo ""
echo "🔄 To restart the app:"
echo "   bash restart.sh"
echo ""
echo "=========================================="
