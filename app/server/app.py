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
        # Her iki parametre setini de oku
        start_id = request.args.get("startWeekId", type=int)
        end_id   = request.args.get("endWeekId", type=int)
        startL   = request.args.get("startWeekLabel")
        endL     = request.args.get("endWeekLabel")
        limit    = request.args.get("limit", 200, type=int)
        offset   = request.args.get("offset", 0, type=int)

        if not ((start_id and end_id) or (startL and endL)):
            return jsonify({"error": "Provide startWeekId/endWeekId OR startWeekLabel/endWeekLabel"}), 400

        con = get_conn(read_only=True)

        # Tüm haftalara sıra numarası ver
        con.execute("""
            WITH all_weeks AS (
              SELECT DISTINCT week FROM searches ORDER BY week
            ),
            weeks_idx AS (
              SELECT week, ROW_NUMBER() OVER (ORDER BY week) AS week_id
              FROM all_weeks
            )
            SELECT week, week_id FROM weeks_idx
        """)
        weeks_idx = {row[0]: int(row[1]) for row in con.fetchall()}

        # Sınırları belirle
        if start_id and end_id:
            s_id, e_id = min(start_id, end_id), max(start_id, end_id)
        else:
            if startL not in weeks_idx or endL not in weeks_idx:
                con.close()
                return jsonify({"error":"Week labels not found"}), 400
            s_id, e_id = sorted([weeks_idx[startL], weeks_idx[endL]])

        q = f"""
        WITH all_weeks AS (
          SELECT DISTINCT week FROM searches ORDER BY week
        ),
        weeks_idx AS (
          SELECT week, ROW_NUMBER() OVER (ORDER BY week) AS week_id
          FROM all_weeks
        ),
        base AS (
          SELECT s.term, s.rank, w.week_id
          FROM searches s
          JOIN weeks_idx w USING(week)
          WHERE w.week_id BETWEEN ? AND ? AND s.rank IS NOT NULL
        ),
        stepped AS (
          SELECT term, rank,
                 LEAD(rank) OVER (PARTITION BY term ORDER BY week_id) AS next_rank
          FROM base
        )
        SELECT term,
               SUM(CASE WHEN next_rank < rank THEN 1 ELSE 0 END) AS ups
        FROM stepped
        GROUP BY term
        HAVING SUM(CASE WHEN next_rank < rank THEN 1 ELSE 0 END) >= 1
        ORDER BY ups DESC
        LIMIT ? OFFSET ?;
        """
        rows = con.execute(q, [s_id, e_id, limit, offset]).fetchall()
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
