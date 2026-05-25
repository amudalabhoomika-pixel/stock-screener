# Oracle Cloud Always Free Deployment Guide

## 🎯 Overview
Deploy Stock Screener on Oracle Cloud Always Free tier for 24/7 uptime without any cost.

## ✨ What You Get
- **2 Ubuntu VMs** (4GB RAM each)
- **Always Free** - no credits needed
- **24/7 uptime** - perfect for scheduled alerts
- **Free tier forever** (not limited to trial period)

---

## 📋 Step-by-Step Deployment

### **Phase 1: Oracle Cloud Setup (5 minutes)**

#### 1.1 Create Oracle Cloud Account
1. Go to **https://www.oracle.com/cloud/free/**
2. Click **Start for Free**
3. Sign up with email and phone verification
4. No credit card required for Always Free tier
5. Wait for account activation (usually instant)

#### 1.2 Create Ubuntu VM
1. Log in to Oracle Cloud Console
2. Click **Create a VM instance** or navigate to **Compute → Instances**
3. Configure:
   - **Name**: stock-screener
   - **Image**: Ubuntu 22.04 (or latest LTS)
   - **Shape**: Ampere (Always Free eligible)
   - **OCPU**: 1 (free tier default)
   - **RAM**: 6 GB (max for free tier)
4. **Download SSH Key** (save it safely: `id_rsa.key`)
5. Click **Create**

#### 1.3 Configure Network Security
1. Go to **Networking → Virtual Cloud Networks**
2. Find your VCN and edit **Ingress Rules**
3. Add rule:
   - **Source**: 0.0.0.0/0
   - **Protocol**: TCP
   - **Destination Port**: 5000
4. Click **Add Ingress Rule**

---

### **Phase 2: Deploy Application (3 minutes)**

#### 2.1 Connect to VM
```bash
# On your local machine
ssh -i id_rsa.key ubuntu@YOUR_VM_IP

# Example:
# ssh -i id_rsa.key ubuntu@158.101.205.123
```

#### 2.2 Run Deployment Script
```bash
# From VM terminal, clone repo
git clone https://github.com/amudalabhoomika-pixel/stock-screener.git
cd stock-screener

# Make scripts executable
chmod +x deploy.sh restart.sh stop.sh

# Run deployment
bash deploy.sh
```

The script will:
- ✅ Update system packages
- ✅ Install Python & dependencies
- ✅ Clone your repository
- ✅ Create virtual environment
- ✅ Prompt for Telegram credentials
- ✅ Start the application

#### 2.3 Enter Your Credentials
When prompted:
```
Enter TELEGRAM_BOT_TOKEN: your_bot_token_here
Enter TELEGRAM_CHAT_ID: your_chat_id_here
```

---

### **Phase 3: Verify Deployment (1 minute)**

#### 3.1 Check Application Status
```bash
# View logs in real-time
tail -f logs/app.log

# Should see:
# Stock Screener  →  http://localhost:5000
# Alert scheduler started for NYSE at 09:30 America/New_York
```

#### 3.2 Access Web Interface
In your browser, go to:
```
http://YOUR_VM_IP:5000
```

You should see the stock screener dashboard.

#### 3.3 Verify Scheduler
In the logs, you should see:
```
Added job "NYSE Alert (9:30 AM ET)"
Scheduler started
Alert scheduler started for NYSE at 09:30 America/New_York
```

---

## 🔧 Management Commands

### Start Application
```bash
# First time
bash deploy.sh

# Or manually
source venv/bin/activate
python3 app.py
```

### Restart Application
```bash
bash restart.sh
```

### Stop Application
```bash
bash stop.sh
```

### View Logs
```bash
# Real-time logs
tail -f logs/app.log

# Last 50 lines
tail -50 logs/app.log

# Search for errors
grep ERROR logs/app.log
```

### Update Code from GitHub
```bash
git pull origin main
bash restart.sh
```

---

## 🚀 Keep App Running After SSH Logout

The deployment script already handles this with `nohup`, but here are alternatives:

### Option 1: Using systemd (Recommended)
```bash
# Create service file
sudo nano /etc/systemd/system/stock-screener.service
```

Paste this:
```ini
[Unit]
Description=Stock Screener Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/stock-screener
ExecStart=/home/ubuntu/stock-screener/venv/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable stock-screener
sudo systemctl start stock-screener
sudo systemctl status stock-screener
```

### Option 2: Using screen (Simple)
```bash
screen -S screener python3 app.py
# Press Ctrl+A then D to detach

# Later, reconnect:
screen -r screener
```

---

## 📊 Telegram Alerts

Once deployed:
- **NYSE alerts** send every weekday at 9:30 AM ET
- Telegram messages show top 10 stocks with:
  - Rank
  - Ticker
  - Volume spike
  - RSI momentum
  - Composite score

---

## 🆘 Troubleshooting

### App won't start
```bash
# Check if process already running
ps aux | grep python3

# Kill existing process
pkill -f "python3 app.py"

# Check for port conflicts
sudo lsof -i :5000

# Check logs
tail -100 logs/app.log
```

### Telegram alerts not sending
1. Verify `.env` file exists with correct tokens
2. Check logs for errors: `grep ERROR logs/app.log`
3. Test Telegram bot: `curl -X GET https://api.telegram.org/botYOUR_TOKEN/getMe`

### High CPU/Memory usage
```bash
# Monitor resources
top

# See detailed process info
ps aux | grep python3

# Reduce refresh rate in screener.py (BATCH_SLEEP)
```

### App crashes
```bash
# Check logs for errors
tail -100 logs/app.log

# Restart
bash restart.sh
```

---

## 💡 Tips & Best Practices

1. **Backup your configuration**
   ```bash
   cp .env .env.backup
   ```

2. **Monitor logs regularly**
   ```bash
   watch -n 60 'tail -5 logs/app.log'
   ```

3. **Set up alerts for VM health**
   - In Oracle Cloud Console → Monitoring → Alarms

4. **Keep code updated**
   ```bash
   cd stock-screener
   git pull origin main
   bash restart.sh
   ```

5. **Check disk space**
   ```bash
   df -h
   ```

---

## 📈 Scaling Up (Optional)

If you hit API rate limits:
1. Increase VM specs (still free within limits)
2. Reduce ticker count
3. Increase batch sleep time
4. Use multiple VMs for parallel screening

---

## 🔒 Security Notes

- ✅ Keep SSH key safe (don't share)
- ✅ Use strong Telegram bot token
- ✅ Don't commit `.env` to GitHub
- ✅ Enable firewall rules (port 5000 only if needed)
- ✅ Update system regularly: `sudo apt update && sudo apt upgrade`

---

## 📞 Support

For issues:
1. Check logs: `tail -100 logs/app.log`
2. Review this guide's troubleshooting section
3. Check GitHub issues: https://github.com/amudalabhoomika-pixel/stock-screener/issues

---

**Your Stock Screener is now running 24/7 on Oracle Cloud! 🎉**
