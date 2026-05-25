# Stock Screener — CLAUDE.md

## Project Overview
A real-time stock screener supporting Indian NSE (Nifty 500) and US NYSE markets.
Filters stocks by P/E < 20, Volume spike > 2× 20-day average, and RSI > 50.
Ranks results using a composite score across all three metrics.

## Stack
- **Backend**: Python 3.10+, Flask, yfinance, pandas, numpy
- **Frontend**: Vanilla HTML/CSS/JS (served by Flask)
- **Port**: 5000

## Project Structure
```
stock-screener/
├── CLAUDE.md               # This file
├── app.py                  # Flask app — API routes + static serving
├── screener.py             # Core screening logic (fetch, filter, score)
├── tickers.py              # Nifty 500 and NYSE ticker lists
├── requirements.txt        # Python dependencies
└── templates/
    └── index.html          # Dark-theme dashboard UI
```

## Running the App
```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

## API Endpoints
- `GET /api/scan?market=NSE`  — Run screener for NSE Nifty 500
- `GET /api/scan?market=NYSE` — Run screener for NYSE
- `GET /api/status`           — Returns current scan status / progress

## Screening Logic
1. Fetch historical data (30 days OHLCV) and info for each ticker via yfinance
2. Filter: P/E < 20, Volume > 2× 20-day avg, RSI(14) > 50
3. Score each stock:
   - Volume score: vol_ratio / 5 (capped at 1.0)
   - RSI score: (RSI - 50) / 50
   - PE score: (20 - PE) / 20
   - Composite = (vol_score + rsi_score + pe_score) / 3
4. Return top 10 sorted by composite score descending

## Rate Limiting Strategy
- yfinance has no official rate limit but will throttle at ~2000 req/hour
- Ticker data is fetched in batches of 20 with a 1-second sleep between batches
- Results are cached in memory for 55 seconds (just under the 60s UI refresh)
- `yf.download()` with group_by='ticker' is used for bulk price/volume fetching
- Info (P/E) is fetched per-ticker with individual calls, throttled

## Filters (Configurable via screener.py constants)
- PE_MAX = 20
- VOLUME_SPIKE_FACTOR = 2.0
- RSI_MIN = 50
- RSI_PERIOD = 14
- TOP_N = 10

## Notes
- NSE tickers use `.NS` suffix (e.g., `RELIANCE.NS`)
- NYSE tickers use no suffix
- Nifty 500 list is bundled as a static list in tickers.py (as of 2024)
- Pre-market / post-market hours: yfinance returns last available close; UI shows a market status badge
