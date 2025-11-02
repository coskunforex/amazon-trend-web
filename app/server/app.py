# app/server/app.py
from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import logging, os
from pathlib import Path
from app.core.payments import create_checkout

from app.core.db import get_conn, init_full, append_week
from app.core.auth import (
    ensure_users_table, create_user, verify_user, get_user, set_plan
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

app = Flask(
    __name__,
    template_folder=str(PROJECT_ROOT / "app" / "web" / "templates"),
    static_folder=str(PROJECT_ROOT / "app" / "web" / "static"),
)

# ---------- Secrets / Logs / DB bootstrap ----------
app.secret_key = os.environ.get("SECRET_KEY", "dev-change-me")

logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

# users tablosu hazır olsun
ensure_users_table()

# ---------- Health & Landing ----------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def landing():
    return render_template("landing.html")

@app.get("/terms")
def terms():
    return render_template("terms.html")

@app.get("/privacy")
def privacy():
    return render_template("privacy.html")

@app.get("/refund")
def refund():
    return render_template("refund.html")


# ---------- APP (demo/pro) ----------
@app.get("/app")
def app_demo():
    # Demo: include/exclude kapalı, 8 hafta UI limiti (JS tarafında uygulanıyor)
    return render_template("index.html", mode="demo")

@app.get("/pro")
def app_pro():
    # Pro: login + plan kontrolü
    email = session.get("user_email")
    if not email:
        return redirect(url_for("login", next="/pro"))
    u = get_user(email)
    if not u or u.get("plan") != "pro":
        return redirect(url_for("dashboard"))
    return render_template("index.html", mode="pro")

# ---------- AUTH ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        ok = create_user(email, password, plan="demo")
        if ok:
            session["user_email"] = email
            nxt = request.args.get("next") or url_for("dashboard")
            return redirect(nxt)
        return render_template("signup.html", error="Email already exists or invalid.")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        if verify_user(email, password):
            session["user_email"] = email
            nxt = request.args.get("next") or url_for("dashboard")
            return redirect(nxt)
        return render_template("login.html", error="Invalid credentials.")
    return render_template("login.html")

@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))

@app.get("/dashboard")
def dashboard():
    email = session.get("user_email")
    user = get_user(email) if email else None
    return render_template("dashboard.html", user=user)

# ---------- TEMP ADMIN (payment gelene kadar) ----------
@app.post("/admin/setpro")
def admin_setpro():
    admin_key_env = os.environ.get("ADMIN_KEY")
    key = request.form.get("key") or request.args.get("key")
    email = (request.form.get("email") or request.args.get("email") or "").strip().lower()
    if not admin_key_env or key != admin_key_env:
        return jsonify({"error": "forbidden"}), 403
    if not email:
        return jsonify({"error": "email required"}), 400
    set_plan(email, "pro")
    return jsonify({"status": "ok", "email": email, "plan": "pro"})

# ---------- API: Weeks ----------
@app.get("/weeks")
def weeks():
    try:
        con = get_conn(read_only=True)
        rows = con.execute("""
            SELECT DISTINCT week
            FROM searches
            ORDER BY week
        """).fetchall()
        con.close()
        return jsonify([r[0] for r in rows])
    except Exception as e:
        app.logger.error("weeks failed: %s", e)
        # Boş DB durumunda boş liste dön, frontend kırılmasın:
        return jsonify([])


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

# ---------- API: Uptrends ----------
@app.get("/uptrends")
def uptrends():
    try:
        start_id = request.args.get("startWeekId", type=int)
        end_id   = request.args.get("endWeekId", type=int)
        include  = (request.args.get("include") or "").strip().lower()
        exclude  = (request.args.get("exclude") or "").strip().lower()
        limit    = request.args.get("limit", 200, type=int)
        offset   = request.args.get("offset", 0, type=int)
        # YÜKSEK DEFAULT: büyük farklar gözüksün
        max_rank = request.args.get("maxRank", 1_500_000, type=int)

        if not (start_id and end_id):
            return jsonify({"error": "Provide startWeekId and endWeekId"}), 400
        if end_id < start_id:
            start_id, end_id = end_id, start_id

        con = get_conn(read_only=True)
        try:
            tmp_root = os.environ.get("DATA_DIR", "/app/storage")
            os.makedirs(os.path.join(tmp_root, "tmp"), exist_ok=True)
            con.execute(f"SET temp_directory='{os.path.join(tmp_root, 'tmp')}';")
            con.execute("SET max_temp_directory_size='10GB';")
            con.execute("SET memory_limit='2GB';")
            con.execute("SET threads=2;")
            con.execute("SET preserve_insertion_order=false;")
        except Exception:
            pass

        sql = """
        WITH all_weeks AS (
          SELECT DISTINCT week FROM searches ORDER BY week
        ),
        weeks_idx AS (
          SELECT week, ROW_NUMBER() OVER (ORDER BY week) AS week_id
          FROM all_weeks
        ),
        filtered AS (
          SELECT s.term, s.rank, w.week_id
          FROM searches s
          JOIN weeks_idx w USING(week)
          WHERE w.week_id BETWEEN ? AND ?
            AND s.rank IS NOT NULL
            AND s.rank <= ?
            AND LENGTH(TRIM(s.term)) >= 2
            AND LOWER(s.term) <> UPPER(s.term)
        ),
        filt2 AS (
          SELECT * FROM filtered WHERE 1=1
        """
        params = [start_id, end_id, max_rank]

        def _parts_space(s: str):
            return [p.strip().lower() for p in s.split() if p.strip()]

        if include:
            for w in _parts_space(include):
                sql += " AND LOWER(term) LIKE ?"
                params.append(f"%{w}%")
        if exclude:
            for w in _parts_space(exclude):
                sql += " AND LOWER(term) NOT LIKE ?"
                params.append(f"%{w}%")

        sql += """
        ),
        term_bounds AS (
          SELECT term,
                 MIN(week_id) AS min_w,
                 MAX(week_id) AS max_w,
                 COUNT(*)     AS cnt
          FROM filt2
          GROUP BY term
          HAVING COUNT(*) >= 2
        ),
        start_end AS (
          SELECT f.term,
                 MAX(CASE WHEN f.week_id = tb.min_w THEN f.rank END) AS start_rank,
                 MAX(CASE WHEN f.week_id = tb.max_w THEN f.rank END) AS end_rank,
                 tb.cnt AS weeks
          FROM filt2 f
          JOIN term_bounds tb USING(term)
          GROUP BY f.term, tb.cnt
        )
        SELECT se.term,
               se.start_rank::BIGINT,
               se.end_rank::BIGINT,
               (se.start_rank - se.end_rank)::BIGINT AS total_improvement,
               se.weeks::BIGINT
        FROM start_end se
        WHERE se.start_rank IS NOT NULL
          AND se.end_rank   IS NOT NULL
          AND se.start_rank > se.end_rank
        ORDER BY total_improvement DESC, se.end_rank ASC
        LIMIT ? OFFSET ?;
        """

        params.extend([limit, offset])

        rows = con.execute(sql, params).fetchall()
        con.close()

        return jsonify([
            {
                "term": r[0],
                "start_rank": int(r[1]) if r[1] is not None else None,
                "end_rank":   int(r[2]) if r[2] is not None else None,
                "total_improvement": int(r[3]) if r[3] is not None else None,
                "weeks": int(r[4]) if r[4] is not None else None,
            } for r in rows
        ])

    except Exception as e:
        app.logger.exception("uptrends failed")
        return jsonify({"error": "uptrends_failed", "message": str(e)}), 500

# ---------- API: Series (range-aware) ----------
@app.get("/series")
def series():
    try:
        term = (request.args.get("term") or "").strip()
        if not term:
            return jsonify({"error": "term required"}), 400

        start_id = request.args.get("startWeekId", type=int)
        end_id   = request.args.get("endWeekId", type=int)

        con = get_conn(read_only=True)

        if start_id and end_id:
            if end_id < start_id:
                start_id, end_id = end_id, start_id
            rows = con.execute("""
                WITH all_weeks AS (
                  SELECT DISTINCT week FROM searches ORDER BY week
                ),
                weeks_idx AS (
                  SELECT week, ROW_NUMBER() OVER (ORDER BY week) AS week_id
                  FROM all_weeks
                )
                SELECT w.week, s.rank
                FROM searches s
                JOIN weeks_idx w USING(week)
                WHERE LOWER(s.term) = LOWER(?)
                  AND w.week_id BETWEEN ? AND ?
                ORDER BY w.week
            """, [term, start_id, end_id]).fetchall()
        else:
            rows = con.execute("""
                SELECT week, rank
                FROM searches
                WHERE LOWER(term) = LOWER(?)
                ORDER BY week
            """, [term]).fetchall()

        con.close()

        return jsonify([{"week": r[0], "weekLabel": r[0], "rank": int(r[1])} for r in rows])
    except Exception as e:
        app.logger.exception("series failed")
        return jsonify({"error": "series_failed", "message": str(e)}), 500

# ---------- CHECKOUT (placeholder) ----------
@app.get("/checkout")
def checkout():
    email = session.get("user_email")
    user = get_user(email) if email else None
    return render_template("checkout.html", user=user)

# Geçici: ödeme simülasyonu (sadece login kullanıcı)
@app.post("/checkout/simulate")
def checkout_simulate():
    email = session.get("user_email")
    if not email:
        return redirect(url_for("login", next="/checkout"))
    # burada normalde Stripe/Paddle webhook set_plan('pro') yapar
    set_plan(email, "pro")
    return redirect(url_for("dashboard"))

@app.post("/checkout/start")
def checkout_start():
    email = session.get("user_email")
    if not email:
        return redirect(url_for("login", next="/checkout"))
    try:
        url = create_checkout(email)
        return redirect(url)
    except Exception as e:
        app.logger.exception("checkout_start failed")
        return render_template("checkout.html", user=get_user(email), error=str(e)), 500


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

# --- Lemon Squeezy Webhook (ödeme -> PRO) ---
import hmac, hashlib

LEMON_SECRET = os.getenv("LEMON_WEBHOOK_SECRET", "")

@app.post("/webhooks/lemon")
def lemon_webhook():
    raw = request.get_data()
    sig = request.headers.get("X-Signature", "")

    if not LEMON_SECRET:
        return "secret-missing", 500

    mac = hmac.new(LEMON_SECRET.encode(), raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(mac, sig or ""):
        return "invalid-signature", 400

    payload = request.get_json(silent=True) or {}
    event = (payload.get("meta") or {}).get("event_name", "")
    attrs = (payload.get("data") or {}).get("attributes") or {}
    email = (attrs.get("user_email") or attrs.get("email") or "").strip().lower()

    if email and event in ("order_created", "subscription_created", "subscription_payment_success"):
        set_plan(email, "pro")

    return "ok", 200
# --- /Webhook ---


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)

# --- DIAGNOSTIC ENDPOINT ---
from app.core.payments import ls_get
import os
from flask import jsonify

@app.get("/diag/lemon")
def diag_lemon():
    """Lemon Squeezy store ve variant ID'lerini test eder."""
    store_id = os.getenv("LEMON_STORE_ID", "").strip()
    variant_id = os.getenv("LEMON_VARIANT_ID", "").strip()

    results = {"store_id": store_id, "variant_id": variant_id}

    sc1, st1 = ls_get(f"stores/{store_id}")
    results["GET /stores/{id}"] = {"status": sc1, "body": st1[:400]}

    sc2, st2 = ls_get(f"variants/{variant_id}")
    results["GET /variants/{id}"] = {"status": sc2, "body": st2[:400]}

    return jsonify(results)
# --- END OF DIAGNOSTIC ENDPOINT ---
