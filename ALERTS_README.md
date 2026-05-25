# Telegram Alerts Feature

This stock screener now supports automatic Telegram notifications of the top 10 screened stocks at market open time.

## Setup

### Prerequisites
- `.env` file with `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` configured
- Python 3.10+ with dependencies installed (`pip install -r requirements.txt`)

### Configuration

Edit the top of `alerts.py` to choose your market:

```python
# Choose market for alerts: "NSE" or "NYSE"
MARKET = "NSE"  # or "NYSE"
```

## How It Works

- **NSE**: Sends alerts every weekday at **9:15 AM IST** (market open)
- **NYSE**: Sends alerts every weekday at **9:30 AM ET** (market open)

The scheduler automatically handles timezone conversions—you don't need to change your system clock.

## Alert Message Format

Each Telegram message includes:
- Market name (NSE or NYSE)
- Current date and time
- Top 10 stocks with:
  - **Rank**: Position in the screened results
  - **Ticker**: Stock symbol
  - **Vol Spike**: Trading volume ratio (current vs. 20-day average)
  - **RSI**: Relative Strength Index momentum indicator
  - **Score**: Composite screening score

### Sample Alert
```
📊 NSE Stock Alert
2026-05-25 09:15 UTC

Rank │ Ticker │ Vol Spike │ RSI  │ Score
─────┼────────┼───────────┼──────┼───────
1    │ RELIANCE.NS │ 3.2x      │ 66   │ 0.825
2    │ INFY.NS     │ 2.8x      │ 58   │ 0.712
3    │ TCS.NS      │ 2.5x      │ 52   │ 0.645
```

## Running the Screener

```bash
pip install -r requirements.txt
python app.py
```

The scheduler starts automatically when the Flask app starts. It runs in the background and will send alerts at the configured times.

### Graceful Shutdown

When you stop the Flask app (`Ctrl+C`), the scheduler shuts down cleanly.

## How Screening Works

1. Fetches 30+ days of stock data via yfinance
2. Filters by:
   - **P/E Ratio**: < 20 (undervalued)
   - **Volume Spike**: > 2× the 20-day average
   - **Momentum (RSI)**: > 50 (uptrend)
3. Scores each stock based on all three metrics
4. Returns top 10 ranked by composite score

## Troubleshooting

- **No alerts sent?**
  - Check that `.env` contains valid `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`
  - Verify `MARKET` is set to `"NSE"` or `"NYSE"` (case-sensitive)
  - Check the log output for errors when the scheduled time arrives

- **Rate limiting?**
  - The screener throttles API calls to avoid hitting yfinance rate limits
  - If you hit limits, reduce `TOP_N` in `screener.py` or increase batch sleep time

## Files Modified

- `requirements.txt`: Added `python-telegram-bot`, `python-dotenv`, `pytz`, `apscheduler`
- `app.py`: Integrated scheduler startup/shutdown
- `alerts.py`: New module with scheduling and Telegram integration
