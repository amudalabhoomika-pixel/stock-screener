# 🚀 PythonAnywhere Quick Start Guide

## What You Get
- ✅ **Free Python hosting** - no credit card needed
- ✅ **Always running** - 24/7 uptime
- ✅ **Easy setup** - GUI-based configuration
- ✅ **Built-in domain** - yourusername.pythonanywhere.com

---

## Step 1: Create Free Account (2 minutes)

1. Go to: **https://www.pythonanywhere.com/registration/register/free/**
2. Sign up with email
3. Verify email
4. **Done!** You have a free account

---

## Step 2: Set Up Web App (5 minutes)

### 2.1 Create Web App
1. Log in to Dashboard
2. Click **Web** → **Add a new web app**
3. Choose **Python 3.10**
4. Skip framework (we'll use Flask directly)

### 2.2 Clone Your Repository
1. Click **Consoles** → **Bash**
2. Run these commands:
```bash
cd /home/YOUR_USERNAME
git clone https://github.com/amudalabhoomika-pixel/stock-screener.git
cd stock-screener
pip install -r requirements.txt
```

### 2.3 Configure Web App
1. Go to **Web** → Click your web app
2. Under **Code section**, set:
   - **Source code**: `/home/YOUR_USERNAME/stock-screener`
   - **Working directory**: `/home/YOUR_USERNAME/stock-screener`

3. Under **WSGI configuration file**, click and edit:
   - Replace content with this:

```python
import sys
import os

path = '/home/YOUR_USERNAME/stock-screener'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

from app import app as application
```

4. Click **Save**

---

## Step 3: Add Environment Variables (2 minutes)

1. In **Web** tab, scroll to **Environment variables**
2. Click **Add a new variable**
3. Add two variables:

**Variable 1:**
- Name: `TELEGRAM_BOT_TOKEN`
- Value: `your_bot_token_here`

**Variable 2:**
- Name: `TELEGRAM_CHAT_ID`
- Value: `your_chat_id_here`

4. Click **Save**

---

## Step 4: Reload & Test (1 minute)

1. Go to **Web** tab
2. Click the green **Reload** button at the top
3. Wait 10 seconds
4. Your app is now live at: `https://YOUR_USERNAME.pythonanywhere.com`

---

## Step 5: Test Everything

### Access Dashboard
```
https://YOUR_USERNAME.pythonanywhere.com
```
You should see the stock screener dashboard!

### Check Logs
1. Go to **Web** tab
2. Click **Latest log files** → **Web Server log**
3. Should see Flask starting without errors

### Test Telegram Alert
1. Go to **Bash console**
2. Run:
```bash
cd /home/YOUR_USERNAME/stock-screener
source /home/YOUR_USERNAME/.virtualenvs/stock-screener/bin/activate
python3 -c "from alerts import send_daily_alert; send_daily_alert()"
```
You should receive a Telegram message!

---

## Scheduled Tasks (Background Alerts)

The scheduler runs **inside** the Flask app, but to ensure it runs even when not accessed:

### Option 1: Always-On (Recommended for Free Users)
PythonAnywhere free tier puts apps to sleep if unused. To keep alerts working:

1. **Enable always-on** (upgrades to Hacker plan - $5/month)
   - Guarantees your app runs 24/7

### Option 2: Free Alternative (No Cost)
Set up a **PythonAnywhere Scheduled Task**:

1. Click **Tasks** in dashboard
2. Click **Create a new scheduled task**
3. Set time: **9:30 AM UTC** (equals 9:30 AM ET with daylight time)
4. Command:
```bash
/home/YOUR_USERNAME/.virtualenvs/stock-screener/bin/python3 -c "
import sys
sys.path.insert(0, '/home/YOUR_USERNAME/stock-screener')
from alerts import send_daily_alert
send_daily_alert()
"
```
5. Click **Create**

This ensures alerts send even if app is sleeping!

---

## Management

### Restart App
```
Web tab → Click green Reload button
```

### View Logs
```
Web tab → Latest log files → Web server log
```

### Update Code
```bash
# In Bash console
cd /home/YOUR_USERNAME/stock-screener
git pull origin main
# Then reload in Web tab
```

### Check Status
```
Web tab → Status shows if running
```

---

## Troubleshooting

### App Not Loading
1. Check **Web server log** for errors
2. Verify Python version is 3.10+
3. Ensure all requirements installed: `pip list`

### Telegram Alerts Not Sending
1. Test: Run `from alerts import send_daily_alert; send_daily_alert()` in Bash
2. Check environment variables are set
3. View error logs: **Web tab → Latest log files**

### App Too Slow
- Reduce number of tickers in `screener.py`
- Increase batch sleep time
- Consider upgrading to Hacker plan for faster response

---

## Pricing

| Plan | Cost | Alerts | Dashboard |
|------|------|--------|-----------|
| **Beginner** | Free | Yes (scheduled task) | Yes |
| **Hacker** | $5/month | Yes (24/7) | Yes |

For 24/7 guaranteed alerts, upgrade to Hacker ($5/month).

---

## Your Domain

Free account gets: `https://YOUR_USERNAME.pythonanywhere.com`

To use custom domain: Upgrade to Hacker plan

---

## Next Steps

1. ✅ Sign up at pythonanywhere.com
2. ✅ Create web app
3. ✅ Clone repository
4. ✅ Configure WSGI
5. ✅ Add environment variables
6. ✅ Click Reload
7. ✅ Access dashboard
8. ✅ Set up scheduled task for alerts

---

## Questions?

Check PythonAnywhere docs: https://www.pythonanywhere.com/help/

Or check our DEPLOYMENT.md for more info!

---

**Your app is now online! 🎉**
