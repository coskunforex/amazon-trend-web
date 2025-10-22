# app/server/app.py
import re
from flask import Flask, jsonify, request, send_from_directory
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
    # templates klasöründeki index.html'i döndür
    return send_from_directory(app.template_folder, "index.html")


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

        # optional cache clear
        if request.args.get("clear_cache"):
            import shutil
            store = PROJECT_ROOT / "data" / "store"
            shutil.rmtree(store, ignore_errors=True)

        if mode == "full":
            init_full(PROJECT_ROOT)
            return jsonify({"status": "ok", "mode": "full"})

        # append mode
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
        start_id = request.args.get("startWeekId", type=int)
        end_id   = request.args.get("endWeekId", type=int)
        include  = (request.args.get("include") or "").strip().lower()
        exclude  = (request.args.get("exclude") or "").strip().lower()
        limit    = request.args.get("limit", 200, type=int)
        offset   = request.args.get("offset", 0, type=int)

        if not (start_id and end_id):
            return jsonify({"error": "Provide startWeekId and endWeekId"}), 400
        if end_id < start_id:
            start_id, end_id = end_id, start_id

        # virgül+boşluk normalize
        def split_terms(s: str):
            return [t.strip() for t in s.replace(",", " ").split() if t.strip()]

        inc_terms = split_terms(include)
        exc_terms = split_terms(exclude)

        con = get_conn(read_only=True)
        base_sql = """
        WITH all_weeks AS (
          SELECT DISTINCT week FROM searches ORDER BY week
        ),
        weeks_idx AS (
          SELECT week, ROW_NUMBER() OVER (ORDER BY week) AS week_id
          FROM all_weeks
        ),
        clean AS (
          SELECT s.term, s.rank, w.week_id
          FROM searches s
          JOIN weeks_idx w USING(week)
          WHERE w.week_id BETWEEN ? AND ?
            AND s.rank IS NOT NULL
            AND NOT (
              s.term LIKE '#%%'
              OR REGEXP_MATCHES(s.term, '^[0-9.eE+\\-]+$')
              OR LENGTH(TRIM(s.term)) < 2
              OR NOT REGEXP_MATCHES(s.term, '[A-Za-z]')
            )
        )
        """
        params = [start_id, end_id]
        extra = ""

        # include: tam kelime / kelime sınırı (ör. 'trump' eşleşsin, 'trumpet' eşleşmesin)
        for w in inc_terms:
            # kelimenin başında/sonunda harf-rakam olmayan sınır: (^|[^a-z0-9]) … ([^a-z0-9]|$)
            pat = rf'(^|[^a-z0-9]){re.escape(w)}([^a-z0-9]|$)'
            extra += " AND REGEXP_MATCHES(LOWER(s.term), ?)"
            params.append(pat)

        # exclude: mevcut davranışı koruyoruz (istersen regex'e de geçiririz)
        for w in exc_terms:
            extra += " AND LOWER(s.term) NOT LIKE ?"
            params.append(f"%{w}%")

        q = f"""
        {base_sql}
        , filtered AS (
          SELECT * FROM clean s WHERE 1=1 {extra}
        )
        , agg AS (
          SELECT
            term,
            MIN(CASE WHEN week_id = ? THEN rank END) AS start_rank,
            MIN(CASE WHEN week_id = ? THEN rank END) AS end_rank,
            COUNT(DISTINCT week_id) AS weeks
          FROM filtered
          GROUP BY term
        )
        SELECT
          term,
          CAST(start_rank AS INTEGER) AS start_rank,
          CAST(end_rank   AS INTEGER) AS end_rank,
          CAST(start_rank - end_rank AS INTEGER) AS total_improvement,
          weeks
        FROM agg
        WHERE start_rank IS NOT NULL AND end_rank IS NOT NULL
          AND (start_rank - end_rank) > 0
        ORDER BY total_improvement DESC
        LIMIT ? OFFSET ?;
        """
        params.extend([start_id, end_id, limit, offset])
        rows = con.execute(q, params).fetchall()
        con.close()

        return jsonify([
          {
            "term": r[0],
            "start_rank": int(r[1]),
            "end_rank": int(r[2]),
            "total_improvement": int(r[3]),
            "weeks": int(r[4]),
          }
          for r in rows
        ])

    except Exception as e:
        app.logger.exception("uptrends failed")
        return jsonify({"error": "uptrends_failed", "message": str(e)}), 500


@app.get("/series")
def series():
    try:
        term = (request.args.get("term") or "").strip()
        if not term:
            return jsonify({"error": "term required"}), 400

        start_id = request.args.get("startWeekId", type=int)
        end_id   = request.args.get("endWeekId", type=int)
        if start_id and end_id and end_id < start_id:
            start_id, end_id = end_id, start_id

        con = get_conn(read_only=True)

        base_sql = """
        WITH all_weeks AS (
          SELECT DISTINCT week FROM searches ORDER BY week
        ),
        weeks_idx AS (
          SELECT week, ROW_NUMBER() OVER (ORDER BY week) AS week_id
          FROM all_weeks
        )
        SELECT s.week, s.rank
        FROM searches s
        JOIN weeks_idx w USING(week)
        WHERE LOWER(s.term) = LOWER(?)
        """
        params = [term]

        # sadece iki id de geldiyse aralığı uygula
        if start_id and end_id:
            base_sql += " AND w.week_id BETWEEN ? AND ?"
            params += [start_id, end_id]

        base_sql += " ORDER BY s.week"

        rows = con.execute(base_sql, params).fetchall()
        con.close()

        # weekLabel dahil döndürelim (UI her ikisini de destekliyor)
        return jsonify([{"week": r[0], "weekLabel": r[0], "rank": int(r[1])} for r in rows])

    except Exception as e:
        app.logger.exception("series failed")
        return jsonify({"error": "series_failed", "message": str(e)}), 500


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
              term LIKE '#%'
              OR REGEXP_MATCHES(term, '^[0-9.eE+\\-]+$')
              OR LENGTH(TRIM(term)) < 2
              OR NOT REGEXP_MATCHES(term, '[A-Za-z]')
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

# en üstte var zaten:
from flask import Flask, jsonify, request, send_from_directory, render_template
from pathlib import Path
# ...

PROJECT_ROOT = Path(__file__).resolve().parents[2]

app = Flask(
    __name__,
    template_folder=str(PROJECT_ROOT / "app" / "web" / "templates"),
    static_folder=str(PROJECT_ROOT / "app" / "web" / "static"),
)

# --- YENİ / GÜNCEL ROUTES ---

@app.get("/")
def landing():
    # templates/landing.html dosyasını göster
    return render_template("landing.html")

@app.get("/app")
def app_ui():
    # eskiden "/" dönen UI: templates/index.html
    return send_from_directory(app.template_folder, "index.html")
