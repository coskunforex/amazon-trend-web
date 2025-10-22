# app/server/app.py
from flask import Flask, jsonify, request, send_from_directory, render_template
import logging, os
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

# ---------- Health & UI ----------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def landing():
    # Landing page (templates/landing.html)
    return render_template("landing.html")

@app.get("/app")
def app_ui():
    # Eski UI (templates/index.html)
    return send_from_directory(app.template_folder, "index.html")

# ---------- API: Weeks ----------
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

# ---------- API: Reindex ----------
@app.get("/reindex")
def reindex():
    try:
        mode = (request.args.get("mode") or "append").lower()

        # optional cache clear
        if request.args.get("clear_cache"):
            import shutil
            store = PROJECT_ROOT / "data" / "store"
            shutil.rmtree(store, ignore_errors=True)

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

# app/server/app.py -> /uptrends (HAFİF ve STABİL)
@app.get("/uptrends")
def uptrends():
    try:
        start_id = request.args.get("startWeekId", type=int)
        end_id   = request.args.get("endWeekId", type=int)
        include  = (request.args.get("include") or "").strip().lower()
        exclude  = (request.args.get("exclude") or "").strip().lower()
        limit    = request.args.get("limit", 200, type=int)
        offset   = request.args.get("offset", 0, type=int)
        max_rank = request.args.get("maxRank", 300, type=int)  # daha hafif sorgu

        if not (start_id and end_id):
            return jsonify({"error": "Provide startWeekId and endWeekId"}), 400
        if end_id < start_id:
            start_id, end_id = end_id, start_id

        con = get_conn(read_only=True)

        # REGEX YOK, rank sınırı VAR, >=2 hafta şartı VAR
        base_sql = """
        WITH all_weeks AS (
          SELECT DISTINCT week FROM searches ORDER BY week
        ),
        weeks_idx AS (
          SELECT week, ROW_NUMBER() OVER (ORDER BY week) AS week_id
          FROM all_weeks
        ),
        windowed AS (
          SELECT s.term, s.rank, w.week_id
          FROM searches s
          JOIN weeks_idx w USING(week)
          WHERE w.week_id BETWEEN ? AND ?
            AND s.rank IS NOT NULL
            AND s.rank <= ?
            AND LENGTH(TRIM(s.term)) >= 2
            AND LOWER(s.term) <> UPPER(s.term)  -- harf içeriyor (regex yerine)
        ),
        filtered AS (
          SELECT * FROM windowed
          WHERE 1=1
        """
        params = [start_id, end_id, max_rank]

        if include:
            for w in include.split():
                base_sql += " AND LOWER(term) LIKE ?"
                params.append(f"%{w}%")
        if exclude:
            for w in exclude.split():
                base_sql += " AND LOWER(term) NOT LIKE ?"
                params.append(f"%{w}%")

        base_sql += """
        ),
        atleast2 AS (
          SELECT term
          FROM filtered
          GROUP BY term
          HAVING COUNT(*) >= 2
        ),
        stepped AS (
          SELECT f.term, f.rank,
                 LEAD(f.rank) OVER (PARTITION BY f.term ORDER BY f.week_id) AS next_rank
          FROM filtered f
          JOIN atleast2 a USING(term)
        )
        SELECT term,
               SUM(CASE WHEN next_rank < rank THEN 1 ELSE 0 END) AS ups
        FROM stepped
        GROUP BY term
        HAVING SUM(CASE WHEN next_rank < rank THEN 1 ELSE 0 END) >= 1
        ORDER BY ups DESC
        LIMIT ? OFFSET ?;
        """

        params.extend([limit, offset])

        rows = con.execute(base_sql, params).fetchall()
        con.close()

        # UI mevcut haliyle ups kolonunu kullanıyor. (İleride start/end/total eklenebilir)
        return jsonify([{"term": r[0], "ups": int(r[1])} for r in rows])

    except Exception as e:
        app.logger.exception("uptrends failed")
        return jsonify({"error": "uptrends_failed", "message": str(e)}), 500

# ---------- API: Series ----------
@app.get("/series")
def series():
    try:
        term = (request.args.get("term") or "").strip()
        if not term:
            return jsonify({"error": "term required"}), 400

        con = get_conn(read_only=True)
        rows = con.execute("""
            SELECT week, rank
            FROM searches
            WHERE LOWER(term) = LOWER(?)
            ORDER BY week
        """, [term]).fetchall()
        con.close()

        return jsonify([{"week": r[0], "rank": int(r[1])} for r in rows])
    except Exception as e:
        app.logger.exception("series failed")
        return jsonify({"error": "series_failed", "message": str(e)}), 500

# ---------- API: Diagnostics ----------
@app.get("/diag")
def diag():
    try:
        con = get_conn(read_only=True)
        rows  = con.execute("SELECT COUNT(*) FROM searches").fetchone()[0]
        weeks = con.execute("SELECT COUNT(DISTINCT week) FROM searches").fetchone()[0]
        sample = con.execute("""
            SELECT term FROM searches
            GROUP BY term
            HAVING NOT (
              term LIKE '#%' OR
              REGEXP_MATCHES(term, '^[0-9.eE+\\-]+$') OR
              LENGTH(TRIM(term)) < 2 OR
              NOT REGEXP_MATCHES(term, '[A-Za-z]')
            )
            LIMIT 5
        """).fetchall()
        con.close()
        return jsonify({
            "rows": int(rows),
            "weeks": int(weeks),
            "sample_clean_terms": [r[0] for r in sample]
        })
    except Exception as e:
        app.logger.exception("diag failed")
        return jsonify({"error":"diag_failed","message":str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
