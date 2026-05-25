# app.py — Flask backend for Stock Screener

import threading
import time
import logging
from flask import Flask, jsonify, render_template, request
from screener import run_screen
from alerts import start_scheduler, stop_scheduler

log = logging.getLogger(__name__)

app = Flask(__name__)

# ── Alert scheduler ───────────────────────────────────────────────────────────
_scheduler = None

# ── In-memory scan state (one scan at a time) ─────────────────────────────────
_scan_lock   = threading.Lock()
_scan_state  = {
    "running":   False,
    "progress":  0,
    "market":    None,
    "result":    None,   # last completed result
    "error":     None,
}
# Cache: avoid re-scanning within 55 seconds of the last scan for the same market
_cache       = {}   # market -> {result, completed_at}
CACHE_TTL    = 55   # seconds
# ─────────────────────────────────────────────────────────────────────────────


def _set_progress(pct: int):
    _scan_state["progress"] = pct


def _run_scan_thread(market: str):
    with _scan_lock:
        _scan_state["running"]  = True
        _scan_state["progress"] = 0
        _scan_state["error"]    = None
        _scan_state["market"]   = market

    try:
        result = run_screen(market, progress_cb=_set_progress)
        with _scan_lock:
            _scan_state["result"]  = result
            _scan_state["running"] = False
            _scan_state["progress"] = 100
            _cache[market] = {"result": result, "completed_at": time.time()}
    except Exception as e:
        log.exception(f"Scan failed for {market}: {e}")
        with _scan_lock:
            _scan_state["running"] = False
            _scan_state["error"]   = str(e)
            _scan_state["progress"] = 0


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/scan")
def api_scan():
    market = request.args.get("market", "NSE").upper()
    force = request.args.get("force", "false").lower() == "true"
    
    if market not in ("NSE", "NYSE"):
        return jsonify({"error": "market must be NSE or NYSE"}), 400

    # Return cached result if fresh and not forced
    if not force:
        cached = _cache.get(market)
        if cached and (time.time() - cached["completed_at"]) < CACHE_TTL:
            log.info(f"Returning cached result for {market}")
            return jsonify({"cached": True, **cached["result"]})

    # If already scanning the same market, return status
    with _scan_lock:
        if _scan_state["running"] and _scan_state["market"] == market:
            return jsonify({
                "scanning": True,
                "progress": _scan_state["progress"],
                "market":   market,
            }), 202

        if _scan_state["running"]:
            return jsonify({"error": "A scan is already in progress for another market. Please wait."}), 429

    # Kick off background scan
    t = threading.Thread(target=_run_scan_thread, args=(market,), daemon=True)
    t.start()

    return jsonify({
        "scanning": True,
        "progress": 0,
        "market":   market,
    }), 202


@app.route("/api/status")
def api_status():
    with _scan_lock:
        state = dict(_scan_state)

    if state["error"]:
        return jsonify({"status": "error", "error": state["error"]}), 500

    if state["running"]:
        return jsonify({
            "status":   "scanning",
            "progress": state["progress"],
            "market":   state["market"],
        })

    if state["result"]:
        return jsonify({
            "status":   "ready",
            "progress": 100,
            **state["result"],
        })

    return jsonify({"status": "idle"})


if __name__ == "__main__":
    print("=" * 60)
    print("  Stock Screener  →  http://localhost:5000")
    print("=" * 60)

    # Start alert scheduler
    try:
        _scheduler = start_scheduler()
    except Exception as e:
        log.error(f"Failed to start alert scheduler: {e}")

    try:
        app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
    finally:
        # Graceful shutdown
        if _scheduler:
            stop_scheduler(_scheduler)
