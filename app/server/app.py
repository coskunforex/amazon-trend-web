# app/server/app.py
from flask import Flask, jsonify, request
import os, logging
from pathlib import Path
from app.core.db import get_conn, init_full, append_week

# Proje kökü
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Flask uygulaması
app = Flask(
    __name__,
    template_folder=str(PROJECT_ROOT / "app" / "web" / "templates"),
    static_folder=str(PROJECT_ROOT / "app" / "web" / "static"),
)

# Basit log
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

# ----------------------------
# 1) Sağlık kontrolü
# ----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ----------------------------
# 2) Ana sayfa (geçici düz metin)
# ----------------------------
@app.get("/")
def home():
    return "OK - backend is live"

# ----------------------------
# 3) Haftaları listele
# ----------------------------
@app.get("/weeks")
def weeks():
    try:
        con = get_conn()
        rows = con.execute(
            "SELECT DISTINCT week FROM trends.searches ORDER BY week"
        ).fetchall()
        con.close()
        return jsonify([{"weekLabel": r[0]} for r in rows])
    except Exception as e:
        app.logger.exception("weeks failed")
        return jsonify({"error": "weeks_failed", "message": str(e)}), 500

# ----------------------------
# 4) Reindex (full veya append)
#    - full:  /reindex?mode=full
#    - append:/reindex?mode=append&week=YYYY_MM_DD  (CSV: data/raw/YYYY_MM_DD.csv)
# ----------------------------
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

# ----------------------------
# 5) Yükselenler (örnek metrik)
#    Kullanım:
#    /uptrends?startWeekLabel=YYYY_MM_DD&endWeekLabel=YYYY_MM_DD&limit=200&offset=0
# ----------------------------
@app.get("/uptrends")
def uptrends():
    try:
        startL = request.args.get("startWeekLabel")
        endL   = request.args.get("endWeekLabel")
        limit  = request.args.get("limit", 200, type=int)
        offset = request.args.get("offset", 0, type=int)

        if not startL or not endL:
            return jsonify({"error": "startWeekLabel & endWeekLabel required"}), 400

        con = get_conn()
        q = f"""
        WITH base AS (
          SELECT week, term, rank,
                 ROW_NUMBER() OVER (PARTITION BY term ORDER BY week) rn
          FROM trends.searches
          WHERE week BETWEEN ? AND ?
        ),
        pairs AS (
          SELECT b1.term,
                 SUM(CASE WHEN b2.rank < b1.rank THEN 1 ELSE 0 END) AS ups
          FROM base b1
          JOIN base b2 ON b2.term=b1.term AND b2.rn=b1.rn+1
          GROUP BY b1.term
        )
        SELECT term, ups
        FROM pairs
        WHERE ups >= 1
        ORDER BY ups DESC
        LIMIT {limit} OFFSET {offset};
        """
        rows = con.execute(q, [startL, endL]).fetchall()
        con.close()
        return jsonify([{"term": r[0], "ups": int(r[1])} for r in rows])
    except Exception as e:
        app.logger.exception("uptrends failed")
        return jsonify({"error": "uptrends_failed", "message": str(e)}), 500

# ----------------------------
# 6) Bir terimin hafta-rank serisi
#    /series?term=coffee%20mug
# ----------------------------
@app.get("/series")
def series():
    try:
        term = request.args.get("term")
        if not term:
            return jsonify({"error": "term required"}), 400

        con = get_conn()
        rows = con.execute("""
            SELECT week, rank
            FROM trends.searches
            WHERE term = ?
            ORDER BY week
        """, [term]).fetchall()
        con.close()
        return jsonify([{"week": r[0], "rank": int(r[1])} for r in rows])
    except Exception as e:
        app.logger.exception("series failed")
        return jsonify({"error": "series_failed", "message": str(e)}), 500

# ----------------------------
# 7) Lokal çalıştırma
# ----------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
