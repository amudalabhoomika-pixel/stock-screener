# alerts.py — Telegram notification scheduler for stock screener

import os
import logging
from datetime import datetime, time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import requests
from dotenv import load_dotenv
from screener import run_screen

load_dotenv()

log = logging.getLogger(__name__)

# ── Configuration ──────────────────────────────────────────────────────────────
# Choose market for alerts: "NSE" or "NYSE"
MARKET = "NYSE"

# Telegram credentials from .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ─────────────────────────────────────────────────────────────────────────────


def send_telegram_message(message: str) -> bool:
    """
    Send a message via Telegram bot.
    Returns True if successful, False otherwise.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        log.error("Telegram credentials not found in .env file")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            log.info(f"Telegram message sent successfully for {MARKET}")
            return True
        else:
            log.error(f"Telegram API error: {response.status_code} — {response.text}")
            return False
    except Exception as e:
        log.error(f"Failed to send Telegram message: {e}")
        return False


def format_alert_message(results: dict) -> str:
    """
    Format screening results into a Telegram message.
    """
    market = results.get("market", "UNKNOWN")
    timestamp = results.get("timestamp", "")
    stocks = results.get("results", [])

    # Parse ISO timestamp to readable format
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        formatted_time = dt.strftime("%Y-%m-%d %H:%M UTC")
    except:
        formatted_time = timestamp

    # Build message header
    msg = f"<b>📊 {market} Stock Alert</b>\n"
    msg += f"<i>{formatted_time}</i>\n"
    msg += "─" * 50 + "\n\n"

    if not stocks:
        msg += "<i>No stocks matched the screening criteria.</i>"
        return msg

    # Format each stock
    msg += "<code>"
    msg += "Rank │ Ticker │ Vol Spike │ RSI  │ Score\n"
    msg += "─────┼────────┼───────────┼──────┼───────\n"

    for stock in stocks[:10]:
        rank = str(stock.get("rank", "?")).ljust(4)
        ticker = stock.get("ticker", "?").ljust(6)
        vol_ratio = f"{stock.get('vol_ratio', 0):.1f}x".ljust(9)
        rsi = f"{stock.get('rsi', 0):.0f}".ljust(4)
        score = f"{stock.get('score', 0):.3f}".ljust(7)

        msg += f"{rank} │ {ticker} │ {vol_ratio} │ {rsi} │ {score}\n"

    msg += "</code>"
    return msg


def send_daily_alert():
    """
    Fetch latest screening results and send Telegram alert.
    Called by the scheduler at market open time.
    """
    log.info(f"Running alert task for {MARKET}")
    try:
        results = run_screen(MARKET)
        message = format_alert_message(results)
        send_telegram_message(message)
    except Exception as e:
        log.error(f"Alert task failed: {e}")


def start_scheduler():
    """
    Start the background scheduler with timezone-aware cron jobs.
    """
    scheduler = BackgroundScheduler()

    # Determine timezone and cron schedule based on MARKET
    if MARKET == "NSE":
        # NSE opens at 9:15 AM IST, every weekday
        timezone_str = "Asia/Kolkata"
        hour = 9
        minute = 15
        job_name = "NSE Alert (9:15 AM IST)"
    elif MARKET == "NYSE":
        # NYSE opens at 9:30 AM ET, every weekday
        timezone_str = "America/New_York"
        hour = 9
        minute = 30
        job_name = "NYSE Alert (9:30 AM ET)"
    else:
        log.error(f"Unknown market: {MARKET}")
        return None

    # Schedule job: Monday-Friday (Mon=0, Sun=6), specific hour:minute
    trigger = CronTrigger(
        day_of_week="mon-fri",
        hour=hour,
        minute=minute,
        timezone=pytz.timezone(timezone_str),
    )

    scheduler.add_job(
        send_daily_alert,
        trigger=trigger,
        id="stock_alert_job",
        name=job_name,
        replace_existing=True,
    )

    scheduler.start()
    log.info(
        f"Alert scheduler started for {MARKET} at {hour:02d}:{minute:02d} {timezone_str}"
    )
    return scheduler


def stop_scheduler(scheduler):
    """Stop the background scheduler gracefully."""
    if scheduler and scheduler.running:
        scheduler.shutdown(wait=True)
        log.info("Alert scheduler stopped")
