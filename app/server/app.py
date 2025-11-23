# app/server/app.py
from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import logging, os
from pathlib import Path
from app.core.payments import create_checkout
# --- DIAGNOSTIC ENDPOINT ---
from app.core.payments import ls_get

from app.server.emailing import send_welcome_email, send_pro_activated_email
from app.core.auth import set_plan


from app.core.db import get_conn, init_full, append_week
from app.core.auth import (
    ensure_users_table, create_user, verify_user, get_user, set_plan
)

# ---- Pricing / Plan text (used by dashboard & checkout) ----
PRICE_TEXT = os.environ.get("PRICE_TEXT", "$29.99/month")
PLAN_NAME  = os.environ.get("PLAN_NAME", "Uptrend Hunter Pro")
PLAN_BENEFITS = [
    "Full access to 18+ weeks of data",
    "Smart include/exclude filters",
    "250 results per query",
    "Priority updates & support",
]



PROJECT_ROOT = Path(__file__).resolve().parents[2]

app = Flask(
    __name__,
    template_folder=str(PROJECT_ROOT / "app" / "web" / "templates"),
    static_folder=str(PROJECT_ROOT / "app" / "web" / "static"),
)
from app.server.ls_webhook import ls_bp
app.register_blueprint(ls_bp)


# Tüm şablonlarda current_user kullanabilelim
@app.context_processor
def inject_current_user():
    email = session.get("user_email")
    u = get_user(email) if email else None
    lemon_portal = os.environ.get("LEMON_PORTAL_URL", "").strip()
    return {
        "current_user": u,
        "LEMON_PORTAL_URL": lemon_portal,
    }


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
        password2 = request.form.get("password2") or ""

        # Basit doğrulamalar
        if len(password) < 6:
            return render_template("signup.html", error="Password must be at least 6 characters.")
        if password != password2:
            return render_template("signup.html", error="Passwords do not match.")

        ok = create_user(email, password, plan="demo")
        if ok:
            try:
                send_welcome_email(email, "")
                app.logger.info("WELCOME_MAIL_SENT to=%s", email)
            except Exception as e:
                app.logger.exception("WELCOME_MAIL_FAILED to=%s err=%s", email, e)

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
    return render_template(
        "dashboard.html",
        user=user,
        plan_name=PLAN_NAME,
        price_text=PRICE_TEXT,
        benefits=PLAN_BENEFITS,
    )


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


# ====== ADMIN DASHBOARD (senin göreceğin panel) ======
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "").strip()

def require_admin(req):
    if not ADMIN_TOKEN:
        return False
    t = (req.args.get("token") or req.headers.get("X-Admin-Token") or "").strip()
    return t == ADMIN_TOKEN

@app.get("/admin")
def admin_dashboard():
    if not require_admin(request):
        return "Not authorized", 401

    con = get_conn(read_only=True)

    users = []
    try:
        users = con.execute("""
            SELECT email, plan, created_at
            FROM users
            ORDER BY created_at DESC
            LIMIT 500
        """).fetchall()
    except Exception:
        app.logger.exception("ADMIN users query failed")

    payments = []
    try:
        payments = con.execute("""
            SELECT email, status, amount, currency, created_at
            FROM payments
            ORDER BY created_at DESC
            LIMIT 200
        """).fetchall()
    except Exception:
        payments = []

    stats = {"total_users": 0, "pro_users": 0, "demo_users": 0, "paid_total": 0}

    try:
        stats["total_users"] = con.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        stats["pro_users"]   = con.execute("SELECT COUNT(*) FROM users WHERE plan='pro'").fetchone()[0]
        stats["demo_users"]  = con.execute("SELECT COUNT(*) FROM users WHERE plan!='pro'").fetchone()[0]
    except Exception:
        pass

    try:
        stats["paid_total"] = con.execute("""
            SELECT COALESCE(SUM(amount),0)
            FROM payments
            WHERE status='paid'
        """).fetchone()[0]
    except Exception:
        stats["paid_total"] = 0

    con.close()

    return render_template(
        "admin.html",
        users=users,
        payments=payments,
        stats=stats,
    )
# ==============================================



@app.get("/weeks")
def weeks():
    try:
        con = get_conn(read_only=True)
        rows = con.execute("""
            WITH all_weeks AS (
              SELECT DISTINCT week FROM searches ORDER BY week
            )
            SELECT
              ROW_NUMBER() OVER (ORDER BY week)   AS week_id,
              week                                 AS label
            FROM all_weeks
        """).fetchall()
        con.close()
        return jsonify([{"weekId": int(r[0]), "label": r[1]} for r in rows])
    except Exception as e:
        app.logger.error("weeks failed: %s", e)
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
        import re

        start_id = request.args.get("startWeekId", type=int)
        end_id   = request.args.get("endWeekId", type=int)
        include  = (request.args.get("include") or "").strip().lower()
        exclude  = (request.args.get("exclude") or "").strip().lower()
        limit    = request.args.get("limit", 250, type=int)
        offset   = request.args.get("offset", 0, type=int)
        max_rank = request.args.get("maxRank", 1_500_000, type=int)

        # ✅ MODE tespiti (URL ?mode=pro|demo, cookie fallback, default demo)
        mode = (request.args.get("mode") or request.cookies.get("mode") or "demo").lower()
        mode = "pro" if mode == "pro" else "demo"

        # ✅ Login olmuş PRO kullanıcıyı session'dan tespit et ve mode'u zorla PRO yap
        email = session.get("user_email")
        if email:
            u = get_user(email)
            if u and u.get("plan") == "pro":
                mode = "pro"

        if not (start_id and end_id):
            return jsonify({"error": "Provide startWeekId and endWeekId"}), 400
        if end_id < start_id:
            start_id, end_id = end_id, start_id

        # ✅ DEMO için 6 hafta clamp
        if mode == "demo":
            if (end_id - start_id + 1) > 6:
                end_id = start_id + 5  # 6 hafta

        # ✅ Sonuç limiti: demo=50, pro=250 (gelen limit parametresini üstten sınırla)
        if mode == "demo":
            limit = min(limit, 50)
        else:
            limit = min(limit, 250)

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

        # include/exclude stringlerini parçala
        def _parts_space(s: str):
            parts = re.split(r"[,\s]+", s or "")
            return [p.strip().lower() for p in parts if p.strip()]

        # ✅ INCLUDE: kelime bazlı eşleşme (trumpet sorunu çözülüyor)
        if include:
            for w in _parts_space(include):
                pattern = rf"(^|[^a-z]){re.escape(w)}([^a-z]|$)"
                sql += " AND REGEXP_MATCHES(LOWER(term), ?)"
                params.append(pattern)

        # ✅ EXCLUDE: aynı mantıkla hariç tut
        if exclude:
            for w in _parts_space(exclude):
                pattern = rf"(^|[^a-z]){re.escape(w)}([^a-z]|$)"
                sql += " AND NOT REGEXP_MATCHES(LOWER(term), ?)"
                params.append(pattern)

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

@app.get("/series")
def series():
    """Seçilen terim için haftalık rank serisini döner (grafik)."""
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
                  AND w.week_id BETWEEN ?
                                  AND ?
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

        return jsonify([
            {"week": r[0], "weekLabel": r[0], "rank": int(r[1])}
            for r in rows
        ])

    except Exception as e:
        app.logger.exception("series failed")
        return jsonify({"error": "series_failed", "message": str(e)}), 500


# ---------- CHECKOUT (placeholder) ----------
@app.get("/checkout")
def checkout():
    email = session.get("user_email")
    user = get_user(email) if email else None

    # Pro kullanıcı zaten ödeme yapmışsa checkout yerine dashboard'a gönder
    if user and user.get("plan") == "pro":
        return redirect(url_for("dashboard"))

    return render_template(
        "checkout.html",
        user=user,
        plan_name=PLAN_NAME,
        price_text=PRICE_TEXT,
        benefits=PLAN_BENEFITS,
    )




# Geçici: ödeme simülasyonu (sadece login kullanıcı)
@app.post("/checkout/simulate")
def checkout_simulate():
    email = session.get("user_email")
    if not email:
        return redirect(url_for("login", next="/checkout"))
    # burada normalde Stripe/Paddle webhook set_plan('pro') yapar
    set_plan(email, "pro")
    try:
        send_pro_activated_email(email, "")
    except Exception as e:
        app.logger.exception("PRO_MAIL_FAILED to=%s err=%s", email, e)

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



# --- DIAGNOSTIC ENDPOINT ---
from app.core.payments import ls_get

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


# --- DIAG: test welcome mail endpoint ---
@app.post("/diag/test_mail")
def diag_test_mail():
    to = (request.args.get("to") or "").strip()
    name = request.args.get("name") or "Diag"
    if not to:
        return jsonify({"ok": False, "error": "missing_to_param"}), 400
    try:
        app.logger.info("DIAG: sending welcome to=%s", to)
        send_welcome_email(to, name)
        return jsonify({"ok": True})
    except Exception as e:
        app.logger.exception("diag mail failed")
        return jsonify({"ok": False, "error": str(e)}), 500


# 🟢 En son, sadece bu kalacak:
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
