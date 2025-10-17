# app/server/app.py
from flask import Flask, jsonify, request
import os, gc
from pathlib import Path

# Repo kökü
PROJECT_ROOT = Path(__file__).resolve().parents[2]

app = Flask(
    __name__,
    template_folder=str(PROJECT_ROOT / "app" / "web" / "templates"),
    static_folder=str(PROJECT_ROOT / "app" / "web" / "static"),
)

# Boot'ta AĞIR İŞ YOK
INDEX = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def home():
    return "OK - backend is live"

@app.get("/weeks")
def weeks():
    global INDEX
    if INDEX is None:
        return jsonify([])
    items = [{"weekId": w, "label": INDEX.week_labels[w], "date": dt.isoformat()}
             for (w, dt) in INDEX.weeks]
    return jsonify(items)

@app.get("/uptrends")
def uptrends():
    global INDEX
    if INDEX is None:
        return jsonify([])
    try:
        startId = int(request.args.get("startWeekId"))
        endId   = int(request.args.get("endWeekId"))
    except:
        return jsonify({"error":"startWeekId & endWeekId required"}), 400
    include = request.args.get("include") or ""
    exclude = request.args.get("exclude") or ""
    from app.core import trend_core as core   # LAZY IMPORT
    rows = core.query_uptrends(INDEX, startId, endId, include=include, exclude=exclude, limit=5000)
    return jsonify(rows)

@app.get("/series")
def series():
    global INDEX
    if INDEX is None:
        return jsonify([])
    term = request.args.get("term")
    if not term:
        return jsonify({"error":"term required"}), 400
    try:
        startId = int(request.args.get("startWeekId"))
        endId   = int(request.args.get("endWeekId"))
    except:
        return jsonify({"error":"startWeekId & endWeekId required"}), 400
    from app.core import trend_core as core   # LAZY IMPORT
    rows = core.query_series(INDEX, term, startId, endId)
    return jsonify(rows)

@app.get("/reindex")
def reindex():
    global INDEX
    from app.core import trend_core as core   # LAZY IMPORT
    INDEX = core.build_index_cached(PROJECT_ROOT)
    gc.collect()
    return jsonify({"status":"ok","weeks": len(INDEX.weeks)})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
