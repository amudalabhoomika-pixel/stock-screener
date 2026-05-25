# Telegram Alerts — Quick Start Guide

## 1-Minute Setup

### Change Market
Edit **line 19** of `alerts.py`:
```python
MARKET = "NSE"   # ← Change this to "NYSE" for US stocks
```

### Run the App
```bash
pip install -r requirements.txt
python app.py
```

That's it! ✅

## When Alerts Send

- **NSE**: Every weekday at **9:15 AM IST** (market open)
- **NYSE**: Every weekday at **9:30 AM ET** (market open)

The system automatically handles timezone conversion—no clock changes needed!

## What You'll Get

A Telegram message with the top 10 screened stocks:

```
📊 NSE Stock Alert
2026-05-25 09:15 UTC

Rank │ Ticker │ Vol Spike │ RSI  │ Score
─────┼────────┼───────────┼──────┼───────
1    │ RELIANCE.NS │ 3.2x      │ 66   │ 0.825
2    │ INFY.NS     │ 2.8x      │ 58   │ 0.712
3    │ TCS.NS      │ 2.5x      │ 52   │ 0.645
```

Each metric:
- **Rank**: Position in results (1-10)
- **Ticker**: Stock symbol (with .NS for NSE)
- **Vol Spike**: How much volume exceeds 20-day average (e.g., 3.2x = 320%)
- **RSI**: Momentum indicator (0-100, >50 = uptrend)
- **Score**: Composite ranking score (0-1, higher is better)

## Credentials

Your `.env` file needs:
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

These are already configured in your project! ✓

## Stop the App

Press **Ctrl+C** to stop. The scheduler shuts down gracefully.

---

**See `ALERTS_README.md` for detailed documentation.**
