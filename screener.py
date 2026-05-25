# screener.py — Core stock screening logic

import time
import logging
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timezone
from tickers import get_tickers

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ── Configurable constants ────────────────────────────────────────────────────
PE_MAX            = 20.0
VOLUME_SPIKE_MIN  = 2.0   # must be > 2× 20-day avg volume
RSI_MIN           = 50.0
RSI_PERIOD        = 14
TOP_N             = 10
BATCH_SIZE        = 20    # tickers per yfinance bulk download
BATCH_SLEEP       = 1.2   # seconds between batches (rate-limit safety)
HISTORY_DAYS      = "45d" # enough for 20-day vol avg + 14-day RSI warmup
# ─────────────────────────────────────────────────────────────────────────────


def compute_rsi(close: pd.Series, period: int = RSI_PERIOD) -> float:
    """Compute RSI for the most recent bar."""
    delta = close.diff().dropna()
    if len(delta) < period:
        return float("nan")
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean().iloc[-1]
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean().iloc[-1]
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)


def composite_score(pe: float, vol_ratio: float, rsi: float) -> float:
    """
    Normalised composite score in [0, 1].
    Higher is better.
      - PE score:      lower PE → higher score  (capped at PE_MAX)
      - Vol score:     higher ratio → higher score (capped at 5×)
      - RSI score:     higher RSI (>50) → higher score (capped at 100)
    """
    pe_score  = max(0.0, (PE_MAX - pe) / PE_MAX)
    vol_score = min(1.0, (vol_ratio - VOLUME_SPIKE_MIN) / (5.0 - VOLUME_SPIKE_MIN))
    rsi_score = max(0.0, (rsi - RSI_MIN) / (100.0 - RSI_MIN))
    return round((pe_score + vol_score + rsi_score) / 3, 4)


def fetch_bulk_history(tickers: list[str], progress_cb=None) -> dict:
    """
    Download OHLCV history for all tickers in batches.
    Returns dict: ticker -> DataFrame (Date index, OHLCV columns)
    """
    result = {}
    total_batches = (len(tickers) + BATCH_SIZE - 1) // BATCH_SIZE

    for i in range(0, len(tickers), BATCH_SIZE):
        batch = tickers[i: i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        log.info(f"Downloading batch {batch_num}/{total_batches}: {batch}")

        try:
            raw = yf.download(
                tickers=batch,
                period=HISTORY_DAYS,
                interval="1d",
                group_by="ticker",
                auto_adjust=True,
                progress=False,
                threads=True,
            )
        except Exception as e:
            log.warning(f"Batch {batch_num} download failed: {e}")
            if i + BATCH_SIZE < len(tickers):
                time.sleep(BATCH_SLEEP)
            continue

        if isinstance(raw.columns, pd.MultiIndex):
            for ticker in batch:
                try:
                    df = raw[ticker].dropna()
                    if not df.empty:
                        result[ticker] = df
                except KeyError:
                    pass
        else:
            # Single ticker returned flat
            if len(batch) == 1 and not raw.empty:
                result[batch[0]] = raw.dropna()

        if progress_cb:
            progress_cb(min(100, int((i + BATCH_SIZE) / len(tickers) * 60)))

        if i + BATCH_SIZE < len(tickers):
            time.sleep(BATCH_SLEEP)

    return result


def fetch_pe_ratios(tickers: list[str], progress_cb=None) -> dict:
    """
    Fetch trailing P/E ratios one ticker at a time (yfinance .info).
    Returns dict: ticker -> pe_ratio (float or None)
    """
    pe_map = {}
    total = len(tickers)

    for idx, ticker in enumerate(tickers):
        try:
            info = yf.Ticker(ticker).fast_info
            pe = getattr(info, "pe_ratio", None)
            # fast_info may not have pe_ratio; fall back to info dict
            if pe is None or (isinstance(pe, float) and np.isnan(pe)):
                full = yf.Ticker(ticker).info
                pe = full.get("trailingPE") or full.get("forwardPE")
            pe_map[ticker] = float(pe) if pe else None
        except Exception as e:
            log.debug(f"PE fetch failed for {ticker}: {e}")
            pe_map[ticker] = None

        if progress_cb and idx % 10 == 0:
            progress_cb(60 + int(idx / total * 35))

        # Light throttle every 20 tickers
        if (idx + 1) % 20 == 0:
            time.sleep(BATCH_SLEEP)

    return pe_map


def run_screen(market: str, progress_cb=None) -> dict:
    """
    Full screening pipeline.
    Returns {
        'results': [...top N dicts...],
        'scanned': int,
        'passed_filter': int,
        'market': str,
        'timestamp': str,
    }
    """
    tickers = get_tickers(market)
    log.info(f"Starting screen for {market} — {len(tickers)} tickers")

    if progress_cb:
        progress_cb(2)

    # Step 1: Bulk download OHLCV history
    history = fetch_bulk_history(tickers, progress_cb)
    log.info(f"Got history for {len(history)} tickers")

    if progress_cb:
        progress_cb(60)

    # Step 2: Pre-filter by volume spike (cheap — no extra API call needed)
    volume_candidates = []
    for ticker, df in history.items():
        if len(df) < 22:
            continue
        avg_vol = df["Volume"].iloc[-21:-1].mean()
        latest_vol = df["Volume"].iloc[-1]
        if avg_vol > 0 and (latest_vol / avg_vol) >= VOLUME_SPIKE_MIN:
            volume_candidates.append(ticker)

    log.info(f"{len(volume_candidates)} tickers passed volume filter")

    if progress_cb:
        progress_cb(63)

    # Step 3: Fetch P/E for volume-filtered candidates only (reduces API calls)
    pe_map = fetch_pe_ratios(volume_candidates, progress_cb)

    if progress_cb:
        progress_cb(95)

    # Step 4: Apply all filters + compute composite scores
    qualified = []
    for ticker in volume_candidates:
        pe = pe_map.get(ticker)
        if pe is None or pe <= 0 or pe >= PE_MAX:
            continue

        df = history[ticker]
        avg_vol = df["Volume"].iloc[-21:-1].mean()
        latest_vol = df["Volume"].iloc[-1]
        vol_ratio = round(latest_vol / avg_vol, 2) if avg_vol > 0 else 0

        rsi = compute_rsi(df["Close"])
        if np.isnan(rsi) or rsi < RSI_MIN:
            continue

        current_price = round(float(df["Close"].iloc[-1]), 2)
        score = composite_score(pe, vol_ratio, rsi)

        qualified.append({
            "ticker":      ticker,
            "price":       current_price,
            "pe":          round(pe, 2),
            "vol_ratio":   vol_ratio,
            "rsi":         rsi,
            "score":       score,
        })

    qualified.sort(key=lambda x: x["score"], reverse=True)
    top = qualified[:TOP_N]

    # Add rank
    for i, item in enumerate(top):
        item["rank"] = i + 1

    log.info(f"Screen complete — {len(qualified)} passed all filters, returning top {len(top)}")

    if progress_cb:
        progress_cb(100)

    return {
        "results":       top,
        "scanned":       len(history),
        "passed_filter": len(qualified),
        "market":        market.upper(),
        "timestamp":     datetime.now(timezone.utc).isoformat(),
    }
