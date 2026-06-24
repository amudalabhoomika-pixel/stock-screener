# telegram_notifier.py
# ─────────────────────────────────────────────────────────────────────────────
# US Stock Screener — Telegram Notification Bot
#
# HOW TO USE:
#   1. Make sure your .env file has:
#        TELEGRAM_BOT_TOKEN=your_bot_token_here
#        TELEGRAM_CHAT_ID=your_chat_id_here
#   2. Run:  python3 telegram_notifier.py
#   3. Stop: Ctrl+C
#
# SCHEDULE: fires every weekday at 09:30 AM Eastern (NYSE open)
# ─────────────────────────────────────────────────────────────────────────────

import os
import time
import logging
import requests
import schedule
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from screener import run_screen

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise EnvironmentError(
        "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env file.\n"
        "Create a .env file with:\n"
        "  TELEGRAM_BOT_TOKEN=your_token\n"
        "  TELEGRAM_CHAT_ID=your_chat_id"
    )

MARKET_TZ   = ZoneInfo("America/New_York")
FIRE_TIME   = "09:30"


def send_telegram(message: str) -> bool:
    url     = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        log.info("Telegram message sent.")
        return True
    except requests.RequestException as e:
        log.error(f"Telegram send failed: {e}")
        return False


def format_message(results: list, momentum: list, scanned: int, passed: int) -> str:
    now      = datetime.now(MARKET_TZ)
    date_str = now.strftime("%A, %d %b %Y")
    time_str = now.strftime("%I:%M %p ET")

    lines = [
        f"🇺🇸 <b>US Market Open — Stock Screener Alert</b>",
        f"📅 {date_str}  |  🕐 {time_str}",
        f"🔍 Scanned: {scanned} stocks  |  ✅ Passed filters: {passed}",
        "",
        "<b>━━━ Top 10 Ranked Stocks ━━━</b>",
        "",
    ]

    if not results:
        lines.append("⚠️ No stocks matched all filters today.")
    else:
        for s in results:
            medal = "🥇" if s["rank"] == 1 else "🥈" if s["rank"] == 2 else "🥉" if s["rank"] == 3 else f"#{s['rank']}"
            vol_bar = "█" * min(10, int(s["vol_ratio"]))
            lines.append(
                f"{medal} <b>{s['ticker']}</b>\n"
                f"   💵 Price:     <code>${s['price']:,.2f}</code>\n"
                f"   📊 Vol Spike: <code>{s['vol_ratio']:.2f}×</code> {vol_bar}\n"
                f"   📈 RSI:       <code>{s['rsi']:.1f}</code>\n"
                f"   🎯 Score:     <code>{int(s['score']*100)}%</code>"
            )
            lines.append("")

    if momentum:
        lines.append("<b>━━━ ⚡ Momentum Bursts ━━━</b>")
        lines.append("")
        for m in momentum[:5]:
            arrow = "🚀" if m["day_change_pct"] >= 10 else "⬆️"
            lines.append(
                f"{arrow} <b>{m['ticker']}</b>  "
                f"<code>+{m['day_change_pct']}%</code> today\n"
                f"   Vol: <code>{m['vol_ratio']}×</code>  "
                f"RSI: <code>{m['rsi']:.1f}</code>  "
                f"Score: <code>{int(m['momentum_score']*100)}%</code>"
            )
            lines.append("")

    lines.append("─────────────────────────")
    lines.append("⚙️ Filters: P/E &lt; 25 · Vol &gt; 1.5× avg · RSI &gt; 45")
    lines.append("🤖 US Stock Screener Bot")
    return "\n".join(lines)


def run_and_notify():
    now = datetime.now(MARKET_TZ)
    if now.weekday() >= 5:
        log.info(f"Skipping — {now.strftime('%A')} is a weekend.")
        return

    log.info(f"Market open alert firing at {now.strftime('%H:%M %Z')}")
    send_telegram("🇺🇸 <b>US Screener started</b> — scanning ~700 stocks now...\nResults in ~5–8 minutes.")

    try:
        data = run_screen("US")
        msg  = format_message(
            results  = data["results"],
            momentum = data.get("momentum", []),
            scanned  = data["scanned"],
            passed   = data["passed_filter"],
        )
        send_telegram(msg)
        log.info(f"Alert sent — {len(data['results'])} ranked + {len(data.get('momentum', []))} momentum.")
    except Exception as e:
        log.exception(f"Screener error: {e}")
        send_telegram(f"⚠️ <b>Screener Error</b>\n<code>{str(e)[:200]}</code>")


def schedule_job():
    local_tz      = datetime.now().astimezone().tzinfo
    market_open   = datetime.now(MARKET_TZ).replace(hour=9, minute=30, second=0, microsecond=0)
    local_open    = market_open.astimezone(local_tz)
    local_time_str = local_open.strftime("%H:%M")

    log.info(
        f"Scheduling US market alert:\n"
        f"  Market open : 09:30 ET\n"
        f"  System time : {local_time_str} (your local clock)\n"
        f"  Fires on    : weekdays only"
    )
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
        getattr(schedule.every(), day).at(local_time_str).do(run_and_notify)


if __name__ == "__main__":
    print("=" * 60)
    print("  US Stock Screener — Telegram Notifier")
    print("  Fires at: 09:30 AM ET (weekdays)")
    print("  Universe: ~700 NYSE + NASDAQ stocks")
    print("  Stop    : Ctrl+C")
    print("=" * 60)

    schedule_job()
    log.info("Scheduler running...")

    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        log.info("Stopped.")
        print("\nGoodbye!")
