from app.core.db import get_conn
from werkzeug.security import generate_password_hash, check_password_hash
import secrets, time

def ensure_users_table():
    con = get_conn()
    # Yeni kurulum için şema
    con.execute("""
        CREATE TABLE IF NOT EXISTS users(
          email TEXT PRIMARY KEY,
          password_hash TEXT NOT NULL,
          plan TEXT NOT NULL DEFAULT 'demo',
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          reset_token TEXT,
          reset_expires BIGINT
        )
    """)
    # Eski tabloda reset kolonları yoksa ekle (migration)
    try:
        con.execute("ALTER TABLE users ADD COLUMN reset_token TEXT")
    except Exception:
        pass
    try:
        con.execute("ALTER TABLE users ADD COLUMN reset_expires BIGINT")
    except Exception:
        pass
    con.close()


def create_user(email: str, password: str, plan: str='demo') -> bool:
    email = (email or '').strip().lower()
    if not email or not password:
        return False
    ph = generate_password_hash(password)
    con = get_conn()
    try:
        con.execute("INSERT INTO users(email, password_hash, plan) VALUES (?, ?, ?)", [email, ph, plan])
        return True
    except Exception:
        return False
    finally:
        con.close()

def get_user(email: str):
    if not email: return None
    con = get_conn(read_only=True)
    row = con.execute("SELECT email, password_hash, plan FROM users WHERE email = ?", [email.strip().lower()]).fetchone()
    con.close()
    if not row: return None
    return {"email": row[0], "password_hash": row[1], "plan": row[2]}

def verify_user(email: str, password: str) -> bool:
    u = get_user(email)
    return bool(u and check_password_hash(u["password_hash"], password))

def set_plan(email: str, plan: str):
    con = get_conn()
    con.execute("UPDATE users SET plan=? WHERE email=?", [plan, (email or '').strip().lower()])
    con.close()
def create_reset_token(email: str) -> str | None:
    """
    Verilen email için random token üretir ve DB'ye yazar.
    60 dakika geçerli.
    """
    email = (email or "").strip().lower()
    if not email:
        return None

    token = secrets.token_urlsafe(32)
    expires = int(time.time()) + 60 * 60  # 60 dakika

    con = get_conn()
    con.execute(
        "UPDATE users SET reset_token = ?, reset_expires = ? WHERE email = ?",
        [token, expires, email],
    )
    con.close()
    return token


def get_user_by_reset_token(token: str):
    """
    Token geçerli ve süresi dolmamışsa ilgili email'i döner.
    Aksi halde None.
    """
    if not token:
        return None

    con = get_conn(read_only=True)
    row = con.execute(
        "SELECT email, reset_expires FROM users WHERE reset_token = ?",
        [token],
    ).fetchone()
    con.close()

    if not row:
        return None

    email, expires = row[0], row[1]
    if not expires or expires < int(time.time()):
        return None

    return {"email": email}


def set_password_for_email(email: str, new_password: str) -> bool:
    """
    Şifreyi günceller ve reset token'ı sıfırlar.
    """
    email = (email or "").strip().lower()
    if not email or not new_password:
        return False

    ph = generate_password_hash(new_password)
    con = get_conn()
    con.execute(
        """
        UPDATE users
        SET password_hash = ?, reset_token = NULL, reset_expires = NULL
        WHERE email = ?
        """,
        [ph, email],
    )
    con.close()
    return True
