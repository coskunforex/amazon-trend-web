from flask import Flask, jsonify, request, render_template
import os
from app.core.trend_core import build_index_cached, query_uptrends, query_series


# Proje kökü: bu dosyanın 3 üstü (amazon-trend-web/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, "app", "web", "templates"),
    static_folder=os.path.join(PROJECT_ROOT, "app", "web", "static"),
)

# Uygulama açılışında index'i yükle
# Eski:
# INDEX = build_index(PROJECT_ROOT)

# Yeni:
INDEX = build_index_cached(PROJECT_ROOT)


@app.route("/")
def home():
    return render_template("index.html")

@app.get("/weeks")
def weeks():
    items = []
    for weekId, dt in INDEX.weeks:
        items.append({
            "weekId": weekId,
            "label": INDEX.week_labels[weekId],
            "date": dt.isoformat()
        })
    return jsonify(items)

@app.get("/uptrends")
def uptrends():
    try:
        startId = int(request.args.get("startWeekId"))
        endId = int(request.args.get("endWeekId"))
    except:
        return jsonify({"error":"startWeekId & endWeekId required"}), 400

    include = request.args.get("include") or ""
    exclude = request.args.get("exclude") or ""

    rows = query_uptrends(INDEX, startId, endId, include=include, exclude=exclude, limit=5000)
    return jsonify(rows)

@app.get("/series")
def series():
    term = request.args.get("term")
    if not term:
        return jsonify({"error":"term required"}), 400
    try:
        startId = int(request.args.get("startWeekId"))
        endId = int(request.args.get("endWeekId"))
    except:
        return jsonify({"error":"startWeekId & endWeekId required"}), 400

    rows = query_series(INDEX, term, startId, endId)
    return jsonify(rows)

@app.get("/reindex")
def reindex():
    global INDEX
    INDEX = build_index(PROJECT_ROOT)
    return jsonify({"status":"ok", "weeks": len(INDEX.weeks)})


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    # Geliştirme için:
    app.run(host="127.0.0.1", port=8000, debug=True)
