from app.core.db import get_conn
from werkzeug.security import generate_password_hash, check_password_hash

def ensure_users_table():
    con = get_conn()
    con.execute("""
        CREATE TABLE IF NOT EXISTS users(
          email TEXT PRIMARY KEY,
          password_hash TEXT NOT NULL,
          plan TEXT NOT NULL DEFAULT 'demo',
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
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
