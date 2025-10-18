# app/server/app.py
from flask import Flask, jsonify, request
import os, logging
from pathlib import Path
from app.core.db import get_conn, init_full, append_week

PROJECT_ROOT = Path(__file__).resolve().parents[2]

app = Flask(
    __name__,
    template_folder=str(PROJECT_ROOT / "app" / "web" / "templates"),
    static_folder=str(PROJECT_ROOT / "app" / "web" / "static"),
)

logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def home():
    return "OK - backend is live"

@app.get("/weeks")
def weeks():
    try:
        con = get_conn(read_only=True)
        rows = con.execute("""
            SELECT
              ROW_NUMBER() OVER (ORDER BY week) AS weekId,
              week AS label
            FROM (SELECT DISTINCT week FROM searches ORDER BY week)
        """).fetchall()
        con.close()
        return jsonify([{"weekId": int(r[0]), "label": r[1]} for r in rows])
    except Exception as e:
        app.logger.exception("weeks failed")
        return jsonify({"error": "weeks_failed", "message": str(e)}), 500

@app.get("/reindex")
def reindex():
    try:
        mode = (request.args.get("mode") or "append").lower()
        if mode == "full":
            init_full(PROJECT_ROOT)
            return jsonify({"status": "ok", "mode": "full"})
        week = request.args.get("week")
        if not week:
            return jsonify({"error": "week required for append"}), 400
        csv_path = PROJECT_ROOT / "data" / "raw" / f"{week}.csv"
        if not csv_path.exists():
            return jsonify({"error": f"csv not found: {csv_path.name}"}), 404
        append_week(csv_path.as_posix(), week)
        return jsonify({"status": "ok", "mode": "append", "week": week})
    except Exception as e:
        app.logger.exception("reindex failed")
        return jsonify({"error": "reindex_failed", "message": str(e)}), 500

@app.get("/uptrends")
def uptrends():
    try:
        startL = request.args.get("startWeekLabel")
        endL   = request.args.get("endWeekLabel")
        limit  = request.args.get("limit", 200, type=int)
        offset = request.args.get("offset", 0, type=int)
        if not startL or not endL:
            return jsonify({"error": "startWeekLabel & endWeekLabel required"}), 400

        con = get_conn(read_only=True)
        # 🔄 LEAD() kullanımı: self-join yok → az RAM
        q = f"""
        WITH base AS (
          SELECT
            term,
            rank,
            LEAD(rank) OVER (PARTITION BY term ORDER BY week) AS next_rank
          FROM searches
          WHERE week BETWEEN ? AND ?
        )
        SELECT
          term,
          SUM(CASE WHEN next_rank < rank THEN 1 ELSE 0 END) AS ups
        FROM base
        GROUP BY term
        HAVING SUM(CASE WHEN next_rank < rank THEN 1 ELSE 0 END) >= 1
        ORDER BY ups DESC
        LIMIT {limit} OFFSET {offset};
        """
        rows = con.execute(q, [startL, endL]).fetchall()
        con.close()
        return jsonify([{"term": r[0], "ups": int(r[1])} for r in rows])
    except Exception as e:
        app.logger.exception("uptrends failed")
        return jsonify({"error": "uptrends_failed", "message": str(e)}), 500

@app.get("/series")
def series():
    try:
        term = request.args.get("term")
        if not term:
            return jsonify({"error": "term required"}), 400
        con = get_conn(read_only=True)
        rows = con.execute("""
            SELECT week, rank
            FROM searches
            WHERE term = ?
            ORDER BY week
        """, [term]).fetchall()
        con.close()
        return jsonify([{"week": r[0], "rank": int(r[1])} for r in rows])
    except Exception as e:
        app.logger.exception("series failed")
        return jsonify({"error": "series_failed", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
