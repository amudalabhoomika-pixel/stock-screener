# app.py — Flask backend for Stock Screener (US-only)

import threading
import time
import logging
from flask import Flask, jsonify, render_template, request
from screener import run_screen

log = logging.getLogger(__name__)

app = Flask(__name__)

# ── In-memory scan state ──────────────────────────────────────────────────────
_scan_lock  = threading.Lock()
_scan_state = {
    "running":  False,
    "progress": 0,
    "result":   None,
    "error":    None,
}
_cache    = {"result": None, "completed_at": 0}
CACHE_TTL = 55   # seconds — set to 0 to disable during testing
# ─────────────────────────────────────────────────────────────────────────────


def _set_progress(pct: int):
    _scan_state["progress"] = pct


def _run_scan_thread():
    with _scan_lock:
        _scan_state["running"]  = True
        _scan_state["progress"] = 0
        _scan_state["error"]    = None

    try:
        result = run_screen("US", progress_cb=_set_progress)
        with _scan_lock:
            _scan_state["result"]   = result
            _scan_state["running"]  = False
            _scan_state["progress"] = 100
            _cache["result"]        = result
            _cache["completed_at"]  = time.time()
    except Exception as e:
        log.exception(f"Scan failed: {e}")
        with _scan_lock:
            _scan_state["running"]  = False
            _scan_state["error"]    = str(e)
            _scan_state["progress"] = 0


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/scan")
def api_scan():
    force = request.args.get("force", "false").lower() == "true"

    # Return cached result if fresh
    age = time.time() - _cache["completed_at"]
    if not force and _cache["result"] and age < CACHE_TTL:
        log.info(f"Returning cached result (age: {age:.0f}s)")
        return jsonify({"cached": True, "cache_age_seconds": int(age), **_cache["result"]})

    # If scan already running, return progress
    with _scan_lock:
        if _scan_state["running"]:
            return jsonify({
                "scanning": True,
                "progress": _scan_state["progress"],
                "market":   "US",
            }), 202

    # Kick off background scan
    t = threading.Thread(target=_run_scan_thread, daemon=True)
    t.start()

    return jsonify({"scanning": True, "progress": 0, "market": "US"}), 202


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
            "market":   "US",
        })

    if state["result"]:
        return jsonify({"status": "ready", "progress": 100, **state["result"]})

    return jsonify({"status": "idle"})


if __name__ == "__main__":
    print("=" * 60)
    print("  US Stock Screener  →  http://localhost:5000")
    print("  Universe: ~700 stocks (S&P500 + Nasdaq + Russell mid-caps)")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
