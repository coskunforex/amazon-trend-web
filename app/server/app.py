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

# app/server/app.py içindeki uptrends fonksiyonunu TAMAMIYLA bununla değiştir
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
        # 1) Tüm haftaları sırala, numerik week_id ver
        # 2) İstenen aralığı numerik olarak daralt
        # 3) LEAD() ile ardışık haftalarda rank iyileşmesini say
        q = f"""
        WITH all_weeks AS (
          SELECT DISTINCT week FROM searches ORDER BY week
        ),
        weeks_idx AS (
          SELECT week,
                 ROW_NUMBER() OVER (ORDER BY week) AS week_id
          FROM all_weeks
        ),
        bounds AS (
          SELECT
            (SELECT week_id FROM weeks_idx WHERE week = ?) AS start_id,
            (SELECT week_id FROM weeks_idx WHERE week = ?) AS end_id
        ),
        base AS (
          SELECT s.term,
                 s.rank,
                 w.week_id
          FROM searches s
          JOIN weeks_idx w USING(week)
          JOIN bounds b
            ON w.week_id BETWEEN b.start_id AND b.end_id
          WHERE s.rank IS NOT NULL
        ),
        stepped AS (
          SELECT
            term,
            rank,
            LEAD(rank) OVER (PARTITION BY term ORDER BY week_id) AS next_rank
          FROM base
        )
        SELECT
          term,
          SUM(CASE WHEN next_rank < rank THEN 1 ELSE 0 END) AS ups
        FROM stepped
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
