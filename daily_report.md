# 🚀 Sabit Yol Haritası


# Deployment Yol Haritası (Sabit Omurga)
- Runtime: Python 3.11 (Linux/amd64)
- Paketleme: Docker (multi-stage)
- Veri: DuckDB + Parquet
- Proxy + TLS: Caddy (Let’s Encrypt)
- CI/CD: GitHub Actions → image → SSH deploy
- Konfig: .env / .env.prod
- İzleme: Sentry (errors), UptimeRobot (/health), günlük S3 yedek
- Sunucu: Remote VM (>= 4 vCPU / 8 GB RAM; ideal 8/16 + NVMe)


---

## STATE SUMMARY

- Stage: **Deployment prep**

- Focus: **Dockerfile ve remote VM hazırlığı**

- Next → compose.prod.yml → CI/CD pipeline → health endpoint


---

# DAILY REPORT

**Project root:** `C:\Users\yacos\amazon-trend-web`

## Python & Packages

```
Python 3.13.7

blinker==1.9.0
certifi==2025.10.5
charset-normalizer==3.4.4
click==8.3.0
colorama==0.4.6
contourpy==1.3.3
cycler==0.12.1
duckdb==1.4.0
et_xmlfile==2.0.0
Flask==3.1.2
fonttools==4.60.0
idna==3.11
itsdangerous==2.2.0
Jinja2==3.1.6
kiwisolver==1.4.9
MarkupSafe==3.0.3
matplotlib==3.10.6
numpy==2.3.3
openpyxl==3.1.5
packaging==25.0
pandas==2.3.2
pillow==11.3.0
pip==25.2
pyparsing==3.2.5
python-dateutil==2.9.0.post0
python-dotenv==1.2.1
pytz==2025.2
requests==2.32.5
six==1.17.0
tzdata==2025.2
urllib3==2.5.0
Werkzeug==3.1.3
xlsxwriter==3.2.9

```

## File Tree (filtered)

- **./**
  - ./app/
  - ./config/
  - ./data/
  - ./logolar/
  - ./scripts/
  - ./tools/
  - ./.env
  - ./.env.example
  - ./.gitignore
  - ./Dockerfile
  - ./STATE.json
  - ./daily_report.md
  - ./daily_sync_full_20251106_150701.zip
  - ./daily_sync_full_20251106_211731.zip
  - ./daily_sync_full_20251107_140509.zip
  - ./daily_sync_full_20251107_153129.zip
  - ./daily_sync_full_20251108_163651.zip
  - ./daily_sync_full_20251119_155517.zip
  - ./daily_sync_full_20251122_084502.zip
  - ./daily_sync_full_20251125_094508.zip
  - ./daily_sync_full_20251125_161252.zip
  - ./daily_sync_full_20251126_123719.zip
  - ./daily_sync_full_20251128_083955.zip
  - ./daily_sync_full_20251129_114917.zip
  - ./daily_sync_full_20251129_164521.zip
  - ./daily_sync_full_20251130_092917.zip
  - ./daily_sync_full_20251130_100850.zip
  - ./daily_sync_full_20251201_103919.zip
  - ./mvp-stable.zip
  - ./requirements.txt
  - ./roadmap.md
  - ./structure.txt
- **app/**
  - app/core/
  - app/server/
  - app/web/
  - app/__init__.py
- **app\core/**
  - app\core/__init__.py
  - app\core/auth.py
  - app\core/db.py
  - app\core/payments.py
  - app\core/trend_core.py
- **app\server/**
  - app\server/__init__.py
  - app\server/app.py
  - app\server/emailing.py
  - app\server/ls_webhook.py
- **app\web/**
  - app\web/static/
  - app\web/templates/
- **app\web\static/**
  - app\web\static/css/
  - app\web\static/img/
  - app\web\static/js/
- **app\web\static\css/**
  - app\web\static\css/auth.css
  - app\web\static\css/landing.css
  - app\web\static\css/styles.css
- **app\web\static\img/**
  - app\web\static\img/trust/
  - app\web\static\img/app-screen.png
  - app\web\static\img/case1.png
  - app\web\static\img/case2.png
  - app\web\static\img/favicon.svg
  - app\web\static\img/sample1.png
  - app\web\static\img/sample2.png
  - app\web\static\img/sample3.png
  - app\web\static\img/trend-graph.png
- **app\web\static\img\trust/**
  - app\web\static\img\trust/mastercard.svg
  - app\web\static\img\trust/shield.svg
  - app\web\static\img\trust/ssl-secure.svg
  - app\web\static\img\trust/stripe.svg
  - app\web\static\img\trust/visa.svg
- **app\web\static\js/**
  - app\web\static\js/app.js
- **app\web\templates/**
  - app\web\templates/_nav.html
  - app\web\templates/academy_build_product_ideas.html
  - app\web\templates/academy_ceo_brief.html
  - app\web\templates/academy_fba_seasonality.html
  - app\web\templates/academy_fba_validation.html
  - app\web\templates/academy_how_to_use.html
  - app\web\templates/academy_include_exclude.html
  - app\web\templates/academy_index.html
  - app\web\templates/academy_ppc_cleanup.html
  - app\web\templates/academy_search_momentum.html
  - app\web\templates/academy_shopify_creatives.html
  - app\web\templates/academy_shopify_dropshipping.html
  - app\web\templates/academy_trend_vs_seasonality.html
  - app\web\templates/academy_weekly_routine.html
  - app\web\templates/admin.html
  - app\web\templates/checkout.html
  - app\web\templates/dashboard.html
  - app\web\templates/forgot.html
  - app\web\templates/index.html
  - app\web\templates/landing.html
  - app\web\templates/login.html
  - app\web\templates/privacy.html
  - app\web\templates/refund.html
  - app\web\templates/reset.html
  - app\web\templates/reset_sent.html
  - app\web\templates/signup.html
  - app\web\templates/terms.html
- **config/**
- **data/**
  - data/raw/
  - data/tmp/
  - data/last_snapshot.json
  - data/trends.duckdb
- **data\raw/**
  - data\raw/.keep
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_07_12.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_07_19.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_07_26.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_08_02.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_08_09.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_08_16.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_08_23.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_08_30.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_09_06.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_09_13.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_09_20.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_09_27.csv
- **data\tmp/**
- **logolar/**
  - logolar/MasterCard_Logo.svg.png
  - logolar/UHlogo.png
  - logolar/Visa_Inc._logo.svg.png
  - logolar/images.png
  - logolar/mastercard.svg
  - logolar/shield.svg
  - logolar/ssl-secure.svg
  - logolar/ssl-secured-logo-png_seeklogo-484612.png
  - logolar/stripe.svg
  - logolar/visa.svg
- **scripts/**
  - scripts/convert_to_duckdb.py
  - scripts/daily_report.py
- **tools/**

## data/raw (first 10 files)

```
US_Top_Search_Terms_Simple_Week_2025_07_12.csv
US_Top_Search_Terms_Simple_Week_2025_07_19.csv
US_Top_Search_Terms_Simple_Week_2025_07_26.csv
US_Top_Search_Terms_Simple_Week_2025_08_02.csv
US_Top_Search_Terms_Simple_Week_2025_08_09.csv
US_Top_Search_Terms_Simple_Week_2025_08_16.csv
US_Top_Search_Terms_Simple_Week_2025_08_23.csv
US_Top_Search_Terms_Simple_Week_2025_08_30.csv
US_Top_Search_Terms_Simple_Week_2025_09_06.csv
US_Top_Search_Terms_Simple_Week_2025_09_13.csv
```

## Code Snapshot


### app\__init__.py

```py

```

### app\core\__init__.py

```py

```

### app\core\auth.py

```py
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

```

### app\core\db.py

```py
# app/core/db.py
import duckdb
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data"))
DB_PATH  = DATA_DIR / "trends.duckdb"

def _ensure_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(DB_PATH.as_posix())
    con.execute("""
        CREATE TABLE IF NOT EXISTS searches(
          week TEXT,
          term TEXT,
          rank INTEGER
        )
    """)
    con.close()

def _sniff(path: Path):
    enc = 'utf-8'
    try:
        preview = path.read_text(encoding='utf-8', errors='strict').splitlines()
    except UnicodeDecodeError:
        enc = 'utf-16'
        preview = path.read_text(encoding='utf-16', errors='strict').splitlines()

    header_line_idx = None
    header_line = ''
    for i, line in enumerate(preview[:200]):
        if 'Search Term' in line and 'Search Frequency Rank' in line:
            header_line_idx = i
            header_line = line
            break
    if header_line_idx is None:
        raise RuntimeError(f"Header not found in {path.name}")

    delim = '\t' if '\t' in header_line else ','
    return enc, header_line_idx, delim

import duckdb, os

def get_conn(read_only=False):
    """
    DuckDB bağlantısı (disk tabanlı mod)
    - Bellek limiti: 2 GB
    - Disk (temp) limiti: 10 GB
    - Render diski /app/storage altında çalışır
    """
    data_dir = os.environ.get("DATA_DIR", "/app/storage")
    db_path = os.path.join(data_dir, "trends.duckdb")
    tmp_path = os.path.join(data_dir, "tmp")

    # temp klasörü garantiye al
    os.makedirs(tmp_path, exist_ok=True)

    # bağlantı
    con = duckdb.connect(db_path, read_only=read_only)

    # sistem ayarları
    con.execute(f"SET temp_directory='{tmp_path}';")
    con.execute("SET max_temp_directory_size='10GB';")
    con.execute("SET memory_limit='2GB';")
    con.execute("SET threads=2;")
    con.execute("SET preserve_insertion_order=false;")

    return con

def ensure_subscribers_table():
    """
    Email subscribe için tablo (DuckDB içinde).
    """
    con = get_conn(read_only=False)
    con.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            email TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.close()







def init_full(project_root: Path):
    """data/raw altındaki TÜM CSV'leri baştan yükler."""
    raw = Path(project_root) / "data" / "raw"
    _ensure_db()
    con = get_conn(read_only=False)
    con.execute("DROP TABLE IF EXISTS searches")
    con.execute("CREATE TABLE searches(week TEXT, term TEXT, rank INTEGER)")
    for p in sorted(raw.glob("*.csv")):
        enc, skip, delim = _sniff(p)
        con.execute(f"""
            INSERT INTO searches
            SELECT
              '{p.stem}'::TEXT AS week,
              "Search Term"::TEXT AS term,
              TRY_CAST("Search Frequency Rank" AS INT) AS rank
            FROM read_csv(
              '{p.as_posix()}',
              AUTO_DETECT=TRUE,
              HEADER=TRUE,
              SKIP={skip},
              DELIM='{delim}',
              ENCODING='{enc}',
              QUOTE='"',
              ESCAPE='"',
              NULLSTR='',
              IGNORE_ERRORS=TRUE
            )
            WHERE "Search Term" IS NOT NULL AND TRIM("Search Term") <> '';
        """)
    con.close()

def append_week(week_csv_path: str, week_label: str):
    """Tek haftayı (CSV) ekler."""
    _ensure_db()
    p = Path(week_csv_path)
    enc, skip, delim = _sniff(p)
    con = get_conn(read_only=False)
    con.execute("CREATE TABLE IF NOT EXISTS searches(week TEXT, term TEXT, rank INTEGER)")
    con.execute(f"""
        INSERT INTO searches
        SELECT
          '{week_label}'::TEXT,
          "Search Term"::TEXT,
          TRY_CAST("Search Frequency Rank" AS INT)
        FROM read_csv(
          '{p.as_posix()}',
          AUTO_DETECT=TRUE,
          HEADER=TRUE,
          SKIP={skip},
          DELIM='{delim}',
          ENCODING='{enc}',
          QUOTE='"',
          ESCAPE='"',
          NULLSTR='',
          IGNORE_ERRORS=TRUE
        )
        WHERE "Search Term" IS NOT NULL AND TRIM("Search Term") <> '';
    """)
    con.close()

```

### app\core\payments.py

```py
# app/core/payments.py
import os, requests

# --- DIAGNOSTIC HELPERS ---
import requests, os

BASE_URL = "https://api.lemonsqueezy.com/v1"
API_KEY = os.getenv("LEMON_API_KEY")

def _ls_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "X-Api-Version": "2022-11-16",
    }

def ls_get(path: str):
    """Lemon Squeezy API'den bir path getirir (örnek: stores/123 veya variants/456)."""
    r = requests.get(f"{BASE_URL}/{path.lstrip('/')}", headers=_ls_headers(), timeout=20)
    return r.status_code, r.text
# --- END OF DIAGNOSTIC HELPERS ---


BASE_URL = "https://api.lemonsqueezy.com/v1"

API_KEY   = os.getenv("LEMON_API_KEY")
STORE_ID  = os.getenv("LEMON_STORE_ID")
VARIANT_ID= os.getenv("LEMON_VARIANT_ID")

def create_checkout(email: str) -> str:
    assert API_KEY and STORE_ID and VARIANT_ID, "LEMON_* env vars missing"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "X-Api-Version": "2022-11-16",
    }

    payload = {
        "data": {
            "type": "checkouts",
            "attributes": {
                "checkout_data": {"email": email}
            },
            "relationships": {
                "store":   {"data": {"type": "stores",   "id": str(STORE_ID)}},
                "variant": {"data": {"type": "variants", "id": str(VARIANT_ID)}},
            }
        }
    }

    r = requests.post(f"{BASE_URL}/checkouts", headers=headers, json=payload, timeout=30)
    # Hata durumunda anlamak için metni de gösterelim
    try:
        r.raise_for_status()
    except Exception:
        raise RuntimeError(f"{r.status_code} error: {r.text}")

    d = r.json()
    return d["data"]["attributes"]["url"]

```

### app\core\trend_core.py

```py
"""
trend_core.py — KANONİK ÇEKİRDEK
- data/raw/ altındaki haftalık CSV’leri okur (60+ hafta).
- weekId (1 = en eski, N = en yeni) üretir.
- Strict uptrend ve zaman serisi sorgularını döndürür.
"""

from __future__ import annotations

import os
import re
import csv
import hashlib
import pickle
from pathlib import Path
from datetime import date
from typing import Dict, List, Tuple, Optional

# ---------------------------------------------------------------------
# Dosya adı paterni: US_Top_Search_Terms_Simple_Week_YYYY_MM_DD.csv
# ---------------------------------------------------------------------
DATE_RE = re.compile(
    r"US_Top_Search_Terms_Simple_Week_(\d{4})_(\d{2})_(\d{2})\.csv$",
    re.I
)

# ---------------------------------------------------------------------
# Disk Cache Yardımcıları
# ---------------------------------------------------------------------
def _files_signature(raw_dir: str) -> str:
    """raw_dir altındaki dosya adları + boyut + mtime’dan md5 imzası üretir."""
    names = []
    if not os.path.isdir(raw_dir):
        return "EMPTY"
    for n in sorted(os.listdir(raw_dir)):
        p = os.path.join(raw_dir, n)
        if os.path.isfile(p):
            st = os.stat(p)
            names.append(f"{n}:{st.st_size}:{int(st.st_mtime)}")
    return hashlib.md5("|".join(names).encode()).hexdigest()


def build_index_cached(project_root: str) -> "TrendIndex":
    """
    CSV içerikleri değişmediği sürece index’i pickle’dan yükler.
    Cache deserialize hatasında otomatik yeniden inşa eder.
    """
    raw_dir = os.path.join(project_root, "data", "raw")
    store   = Path(project_root) / "data" / "store"
    store.mkdir(parents=True, exist_ok=True)

    sig = _files_signature(raw_dir)
    cache = store / f"index_{sig}.pkl"

    if cache.exists():
        try:
            return pickle.loads(cache.read_bytes())
        except Exception as e:
            # Bozuk / uyumsuz cache durumunda sıfırdan üret
            print("⚠️ Cache deserialize failed, rebuilding:", e)

    idx = build_index(project_root)
    cache.write_bytes(pickle.dumps(idx, protocol=pickle.HIGHEST_PROTOCOL))
    return idx


# ---------------------------------------------------------------------
# Veri Yapıları
# ---------------------------------------------------------------------
class TrendIndex:
    def __init__(self):
        # weekId sıralı liste: [(weekId, yyyymmdd_date)]
        self.weeks: List[Tuple[int, date]] = []
        # hızlı lookup: weekId -> date
        self.weekid_to_date: Dict[int, date] = {}
        # etiketler (UI): weekId -> "Week {id} (YYYY-MM-DD)"
        self.week_labels: Dict[int, str] = {}
        # term -> { weekId: rank }
        self.term_ranks: Dict[str, Dict[int, int]] = {}


# ---------------------------------------------------------------------
# CSV Okuma
# ---------------------------------------------------------------------
def _list_week_files(raw_dir: str) -> List[Tuple[date, str]]:
    """raw_dir altındaki geçerli haftalık dosyaları [tarih, yol] olarak döndürür."""
    files: List[Tuple[date, str]] = []
    if not os.path.isdir(raw_dir):
        return files
    for name in os.listdir(raw_dir):
        m = DATE_RE.match(name)
        if not m:
            continue
        yyyy, mm, dd = map(int, m.groups())
        files.append((date(yyyy, mm, dd), os.path.join(raw_dir, name)))
    files.sort(key=lambda x: x[0])  # en eski -> en yeni
    return files


def _find_header_index(rows: List[List[str]]) -> Tuple[Optional[int], Optional[int], int]:
    """
    'Search Frequency Rank' ve 'Search Term' başlıklarını bulur.
    Preamble satırları (Reporting Range vs.) atlanır.
    Dönen: (rank_col_index, term_col_index, data_start_row_index)
    """
    for i, row in enumerate(rows):
        norm = [c.strip().lower() for c in row]
        if "search frequency rank" in norm and "search term" in norm:
            return norm.index("search frequency rank"), norm.index("search term"), i + 1
    return None, None, 0


def _read_week_csv(path: str, encoding: str = "utf-8-sig") -> Dict[str, int]:
    """
    Amazon Brand Analytics CSV’lerini esnek şekilde okur.
    - 'Reporting Range' / 'Select week' satırlarını atlar.
    - Fazla virgül veya tırnak hatalarına toleranslıdır.
    """
    with open(path, "r", encoding=encoding, newline="") as f:
        reader = list(csv.reader(f))

    # Başlık tespiti
    rank_idx, term_idx, start = _find_header_index(reader)

    # Fallback: ilk 15 satırda 'rank' ve 'term' geçen ilk iki kolonu kabullen
    if start == 0:
        for i, row in enumerate(reader[:15]):
            cols = [c.strip().lower() for c in row if c and c.strip()]
            if len(cols) >= 2 and "rank" in cols[0] and "term" in cols[1]:
                rank_idx, term_idx, start = 0, 1, i + 1
                break

    out: Dict[str, int] = {}

    for row in reader[start:]:
        if not row or len(row) < 2:
            continue

        try:
            rank_raw = row[rank_idx].strip() if rank_idx is not None and rank_idx < len(row) else ""
            term_raw = row[term_idx].strip() if term_idx is not None and term_idx < len(row) else ""
        except Exception:
            continue

        if not rank_raw or not term_raw:
            continue

        # Rank'ı sayıya çevir
        try:
            rank = int(str(rank_raw).replace(",", "").strip())
        except Exception:
            continue

        term = term_raw.strip().lower()
        if not term or term.startswith("search term"):
            continue

        # Aynı terim tekrar ederse en iyi (en düşük) rank'ı tut
        if term not in out or rank < out[term]:
            out[term] = rank

    return out


# ---------------------------------------------------------------------
# Index İnşası
# ---------------------------------------------------------------------
def build_index(project_root: str) -> TrendIndex:
    """
    project_root: .../amazon-trend-web (proje kökü)
    data/raw içindeki tüm CSV'leri okur, TrendIndex döner.
    """
    raw_dir = os.path.join(project_root, "data", "raw")
    files = _list_week_files(raw_dir)
    if len(files) < 2:
        raise RuntimeError("En az 2 hafta CSV gerekli (data/raw/).")

    idx = TrendIndex()

    # Hafta listesi
    for i, (dt, _) in enumerate(files, start=1):
        idx.weeks.append((i, dt))
        idx.weekid_to_date[i] = dt
        idx.week_labels[i] = f"Week {i} ({dt.isoformat()})"

    # Ranks
    for week_id, (_, path) in zip(range(1, len(files) + 1), files):
        ranks = _read_week_csv(path)
        for term, rank in ranks.items():
            if term not in idx.term_ranks:
                idx.term_ranks[term] = {}
            idx.term_ranks[term][week_id] = rank

    return idx


# ---------------------------------------------------------------------
# Yardımcılar (include/exclude)
# ---------------------------------------------------------------------
def _word_hit(text: str, needle: str) -> bool:
    """needle kelimesi text içinde 'kelime olarak' geçiyor mu? (trump ✔, trumpet ✘)"""
    if not needle:
        return False
    pat = r"\b" + re.escape(needle.strip().lower()) + r"\b"
    return re.search(pat, text.lower()) is not None


def _passes_filters(term: str, include: Optional[str], exclude: Optional[str]) -> bool:
    t = term.lower()

    # EXCLUDE: listedeki herhangi bir kelime/ifadeyi kelime olarak içeriyorsa ELER
    if exclude:
        for part in [p.strip().lower() for p in exclude.split(",") if p.strip()]:
            if _word_hit(t, part):
                return False

    # INCLUDE: listedeki kelime/ifadelerden en az biri kelime olarak geçmeli
    if include:
        inc_parts = [p.strip().lower() for p in include.split(",") if p.strip()]
        if inc_parts and not any(_word_hit(t, p) for p in inc_parts):
            return False

    return True


# ---------------------------------------------------------------------
# Trend Mantığı
# ---------------------------------------------------------------------
def _strict_uptrend_for_range(
    ranks_by_weekid: Dict[int, int],
    start_id: int,
    end_id: int
) -> Optional[Tuple[int, int, int]]:
    """
    Seçilen [start_id..end_id] aralığında:
      - Her hafta mevcut
      - Her adımda prev_rank > curr_rank  (STRICT)
    True ise (start_rank, end_rank, total_improvement) döndürür; aksi halde None.
    """
    last_rank: Optional[int] = None
    start_rank: Optional[int] = None
    for w in range(start_id, end_id + 1):
        if w not in ranks_by_weekid:
            return None
        r = ranks_by_weekid[w]
        if last_rank is None:
            start_rank = r
        else:
            if not (last_rank > r):
                return None
        last_rank = r
    end_rank = last_rank if last_rank is not None else None
    total_impr = (start_rank - end_rank) if (start_rank is not None and end_rank is not None) else 0
    return (start_rank, end_rank, total_impr)  # type: ignore


def query_uptrends(
    idx: TrendIndex,
    start_week_id: int,
    end_week_id: int,
    include: Optional[str] = None,
    exclude: Optional[str] = None,
    limit: int = 2000
) -> List[Dict]:
    if start_week_id > end_week_id:
        start_week_id, end_week_id = end_week_id, start_week_id
    if end_week_id - start_week_id + 1 < 2:
        return []

    results: List[Dict] = []
    for term, weeks_map in idx.term_ranks.items():
        # 🧹 Bozuk / anlamsız terimleri filtrele
        if not term:
            continue
        t = term.strip().lower()

        # Excel/formül hataları (#NAME?, #REF!, vs.)
        if t.startswith("#"):
            continue
        # Tamamen sayısal ya da bilimsel format (9.78E+12, 1.23e-5, 12345, +10, -3.2)
        if re.fullmatch(r"[0-9.eE+\-]+", t):
            continue
        # Çok kısa ya da hiç harf içermeyen şeyleri at
        if len(t) < 2 or not re.search(r"[a-zA-Z]", t):
            continue

        if not _passes_filters(term, include, exclude):
            continue

        check = _strict_uptrend_for_range(weeks_map, start_week_id, end_week_id)
        if check is None:
            continue

        start_rank, end_rank, total_impr = check
        results.append({
            "term": term,
            "start_rank": start_rank,
            "end_rank": end_rank,
            "total_improvement": total_impr,
            "weeks": end_week_id - start_week_id + 1
        })

    # sıralama: önce total_improvement DESC, sonra end_rank ASC
    results.sort(key=lambda r: (-r["total_improvement"], r["end_rank"]))
    return results[:limit]


def query_series(
    idx: TrendIndex,
    term: str,
    start_week_id: int,
    end_week_id: int
) -> List[Dict]:
    if start_week_id > end_week_id:
        start_week_id, end_week_id = end_week_id, start_week_id
    series: List[Dict] = []
    ranks_map = idx.term_ranks.get(term.lower(), {})
    for w in range(start_week_id, end_week_id + 1):
        series.append({
            "weekId": w,
            "weekLabel": idx.week_labels.get(w, f"Week {w}"),
            "rank": ranks_map.get(w)  # None olabilir (UI göstermek için)
        })
    return series

```

### app\server\__init__.py

```py

```

### app\server\app.py

```py
# app/server/app.py
from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import logging, os
from pathlib import Path
from app.core.payments import create_checkout
# --- DIAGNOSTIC ENDPOINT ---
from app.core.payments import ls_get

from app.server.emailing import (
    send_welcome_email,
    send_pro_activated_email,
    send_password_reset_email,
)

from app.core.auth import set_plan
from flask import Response  # en üste importlara ekle

from app.core.db import get_conn, init_full, append_week
from app.core.auth import (
    ensure_users_table,
    create_user,
    verify_user,
    get_user,
    set_plan,
    create_reset_token,
    get_user_by_reset_token,
    set_password_for_email,
)

from app.core.db import get_conn, init_full, append_week, ensure_subscribers_table




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

@app.get("/academy/how-to-use")
def academy_how_to_use():
    return render_template("academy_how_to_use.html")

@app.route("/academy/search-momentum")
def academy_search_momentum():
    return render_template("academy_search_momentum.html")

@app.get("/academy")
def academy_index():
    return render_template("academy_index.html")

@app.get("/academy/ceo-brief")
def academy_ceo_brief():
    return render_template("academy_ceo_brief.html")

@app.get("/academy/weekly-routine")
def academy_weekly_routine():
    return render_template("academy_weekly_routine.html")

@app.get("/academy/shopify-dropshipping")
def academy_shopify_dropshipping():
    return render_template("academy_shopify_dropshipping.html")

@app.get("/academy/trend-vs-seasonality")
def academy_trend_vs_seasonality():
    return render_template("academy_trend_vs_seasonality.html")

@app.get("/academy/build-product-ideas")
def academy_build_product_ideas():
    return render_template("academy_build_product_ideas.html")

@app.get("/academy/shopify-creatives")
def academy_shopify_creatives():
    return render_template("academy_shopify_creatives.html")

@app.get("/academy/amazon-fba-validation")
def academy_amazon_fba_validation():
    return render_template("academy_fba_validation.html")

@app.get("/academy/amazon-fba-seasonality")
def academy_amazon_fba_seasonality():
    return render_template("academy_fba_seasonality.html")

 
@app.get("/academy/ppc-cleanup")
def academy_ppc_cleanup():
    return render_template("academy_ppc_cleanup.html")


@app.get("/academy/include-exclude")
def academy_include_exclude():
    return render_template("academy_include_exclude.html")


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

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()

        user = get_user(email)
        if user:
            token = create_reset_token(email)
            if token:
                try:
                    send_password_reset_email(email, token)
                except Exception as e:
                    app.logger.exception("reset email send failed: %s", e)

        # E-mail gönderildi sayfasına yönlendir
        return redirect(url_for("reset_sent"))

    return render_template("forgot.html")

@app.route("/reset-sent")
def reset_sent():
    return render_template("reset_sent.html")


@app.route("/reset/<token>", methods=["GET", "POST"])
def reset(token):
    user = get_user_by_reset_token(token)
    if not user:
        return render_template(
            "reset.html",
            error="This reset link is invalid or has expired."
        )

    if request.method == "POST":
        pw1 = request.form.get("password") or ""
        pw2 = request.form.get("password2") or ""

        if len(pw1) < 6:
            return render_template(
                "reset.html",
                error="Password must be at least 6 characters."
            )

        if pw1 != pw2:
            return render_template(
                "reset.html",
                error="Passwords do not match."
            )

        set_password_for_email(user["email"], pw1)
        # İstersen burada direkt login de yapıyoruz:
        session["user_email"] = user["email"]
        return redirect(url_for("dashboard"))

    return render_template("reset.html")


@app.route("/subscribe", methods=["POST"])
def subscribe():
    email = (request.form.get("email") or "").strip().lower()
    if not email:
        return "Invalid email", 400

    # tabloyu garantiye al
    ensure_subscribers_table()

    con = get_conn(read_only=False)
    try:
        con.execute(
            "INSERT OR IGNORE INTO subscribers(email) VALUES (?)",
            [email],
        )
        con.commit()
    finally:
        con.close()

    # Şimdilik tekrar landing'e dön
    return redirect(url_for("landing"))
    # landing view fonksiyonunun adı farklıysa onu yaz (ör: "index")



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

        # ✅ MODE sadece session+plan ile belirlenir (URL/cookie ASLA değil)
        email = session.get("user_email")
        mode = "demo"
        if email:
            u = get_user(email)
            if u and u.get("plan") == "pro":
                mode = "pro"

        if not (start_id and end_id):
            return jsonify({"error": "Provide startWeekId and endWeekId"}), 400
        if end_id < start_id:
            start_id, end_id = end_id, start_id

        # ✅ DEMO için 6 hafta clamp (ve pagination bypass kapalı)
        if mode == "demo":
            if (end_id - start_id + 1) > 6:
                end_id = start_id + 5  # 6 hafta
            limit = min(limit, 50)
            offset = 0
        else:
            limit = min(limit, 250)
            offset = max(offset, 0)

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

        # ✅ MODE sadece session+plan ile belirlenir
        email = session.get("user_email")
        mode = "demo"
        if email:
            u = get_user(email)
            if u and u.get("plan") == "pro":
                mode = "pro"

        # ✅ start/end zorunlu olsun (demo full-history çekemesin)
        if not (start_id and end_id):
            return jsonify({"error": "Provide startWeekId and endWeekId"}), 400

        if end_id < start_id:
            start_id, end_id = end_id, start_id

        # ✅ DEMO: max 6 weeks
        if mode == "demo" and (end_id - start_id + 1) > 6:
            return jsonify({
                "error": "upgrade_required",
                "message": "Demo is limited to 6 weeks. Upgrade to Pro."
            }), 403

        con = get_conn(read_only=True)

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

@app.get("/app")
def app_demo():
    email = session.get("user_email")
    if email:
        u = get_user(email)
        if u and u.get("plan") == "pro":
            return redirect(url_for("app_pro"))
    return render_template("index.html", mode="demo")


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



@app.get("/robots.txt")
def robots_txt():
    txt = """User-agent: *
Allow: /
Disallow: /app
Disallow: /pro
Disallow: /dashboard
Disallow: /login
Disallow: /signup
Disallow: /checkout
Disallow: /admin
Disallow: /weeks
Disallow: /uptrends
Disallow: /series
Sitemap: https://www.uptrendhunter.com/sitemap.xml
"""
    return Response(txt, mimetype="text/plain")


@app.get("/sitemap.xml")
def sitemap_xml():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://www.uptrendhunter.com/</loc></url>
  <url><loc>https://www.uptrendhunter.com/terms</loc></url>
  <url><loc>https://www.uptrendhunter.com/privacy</loc></url>
  <url><loc>https://www.uptrendhunter.com/refund</loc></url>
  <url><loc>https://www.uptrendhunter.com/academy</loc></url>
  <url><loc>https://www.uptrendhunter.com/academy/how-to-use</loc></url>
  <url><loc>https://www.uptrendhunter.com/academy/ceo-brief</loc></url>
  <url><loc>https://www.uptrendhunter.com/academy/search-momentum</loc></url>
  <url><loc>https://www.uptrendhunter.com/academy/weekly-routine</loc></url>
  <url><loc>https://www.uptrendhunter.com/academy/trend-vs-seasonality</loc></url>
  <url><loc>https://www.uptrendhunter.com/academy/include-exclude</loc></url>
  <url><loc>https://www.uptrendhunter.com/academy/build-product-ideas</loc></url>
  <url><loc>https://www.uptrendhunter.com/academy/ppc-cleanup</loc></url>
  <url><loc>https://www.uptrendhunter.com/academy/shopify-dropshipping</loc></url>
  <url><loc>https://www.uptrendhunter.com/academy/shopify-creatives</loc></url>
  <url><loc>https://www.uptrendhunter.com/academy/amazon-fba-validation</loc></url>
  <url><loc>https://www.uptrendhunter.com/academy/amazon-fba-seasonality</loc></url>


</urlset>
"""
    return Response(xml, mimetype="application/xml")


# 🟢 En son, sadece bu kalacak:
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)

```

### app\server\emailing.py

```py
# app/server/emailing.py
from dotenv import load_dotenv
load_dotenv()

import os, smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

SENDER_EMAIL = os.getenv("SENDER_EMAIL", "support@uptrendhunter.com")
SENDER_NAME  = os.getenv("SENDER_NAME",  "Uptrend Hunter")
SMTP_HOST    = os.getenv("SMTP_HOST",    "mail.privateemail.com")
SMTP_PORT    = int(os.getenv("SMTP_PORT", "465"))
SMTP_PASS    = os.getenv("SMTP_PASS")
SMTP_USER    = os.getenv("SMTP_USER", SENDER_EMAIL)

def _send_text(to_email: str, subject: str, body: str):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = formataddr((SENDER_NAME, SENDER_EMAIL))
    msg["To"] = to_email

    # Önce SSL 465 dene, olmazsa 587 STARTTLS
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20) as s:
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
    except Exception:
        with smtplib.SMTP(SMTP_HOST, 587, timeout=20) as s:
            s.ehlo(); s.starttls(); s.ehlo()
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)

def send_welcome_email(to_email: str, name: str = ""):
    subject = "Welcome to Uptrend Hunter — Your account is ready 🚀"
    body = f"""Hi there,

Your Uptrend Hunter account has been created successfully.

You can log in and start exploring rising Amazon search trends.
Dashboard: https://www.uptrendhunter.com/app

Plan: Starter (demo limits apply)
• Up to 6 weeks lookback
• Top 50 results per query

Need help? Just reply to this email or write to support@uptrendhunter.com.


— Uptrend Hunter Team
Built by Amazon sellers, for Amazon sellers.
"""
    _send_text(to_email, subject, body)

def send_password_reset_email(to_email: str, token: str):
    reset_url = f"https://www.uptrendhunter.com/reset/{token}"
    subject = "Reset your Uptrend Hunter password"
    body = f"""Hi there,

We received a request to reset the password for your Uptrend Hunter account.

Click the link below to set a new password (this link is valid for 60 minutes):

{reset_url}

If you didn't ask for this, you can safely ignore this email.

— Uptrend Hunter Team
"""
    _send_text(to_email, subject, body)


def send_pro_activated_email(to_email: str, name: str = ""):
    subject = "Uptrend Hunter Pro — Activated ✅"
    body = f"""Hi there,

Your Uptrend Hunter Pro plan is now active. 🎉

What you’ve unlocked:
• Full 18+ week history
• Up to 250 results per query
• Advanced include/exclude filters
• Priority updates & support

Open your dashboard: https://www.uptrendhunter.com/app

If you have any questions, reply to this email or contact support@uptrendhunter.com.
— The Uptrend Hunter Team
Built by Amazon sellers, for Amazon sellers.
"""
    _send_text(to_email, subject, body)

```

### app\server\ls_webhook.py

```py
import os, hmac, hashlib
from flask import Blueprint, request, jsonify
from app.server.emailing import send_pro_activated_email
from app.core.auth import set_plan

ls_bp = Blueprint("ls_bp", __name__)
LS_SECRET = os.getenv("LEMON_WEBHOOK_SECRET", "")

def _verify_signature(raw: bytes, sig: str) -> bool:
    if not LS_SECRET:
        return True  # dev ortamında secret yoksa doğrulama atlanır
    mac = hmac.new(LS_SECRET.encode("utf-8"), msg=raw, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), (sig or "").strip())

@ls_bp.post("/webhooks/lemon")
def lemon_webhook():
    """Lemon Squeezy webhook: PRO plan + mail gönderimi"""
    raw = request.data
    sig = request.headers.get("X-Signature", "")  # Lemon Squeezy'nin HMAC başlığı
    if not _verify_signature(raw, sig):
        return jsonify({"ok": False, "error": "bad_signature"}), 400

    payload = request.get_json(silent=True) or {}
    event = payload.get("meta", {}).get("event_name", "")
    attrs = (payload.get("data", {}) or {}).get("attributes", {}) or {}

    email = (attrs.get("user_email") or attrs.get("email") or "").strip().lower()
    name = (attrs.get("user_name") or "").strip()

    success_events = {"subscription_created", "subscription_payment_success", "order_created"}

    if email and event in success_events:
        # 1) Planı PRO yap
        try:
            set_plan(email, "pro")
        except Exception as e:
            print("set_plan failed:", e)

        # 2) Pro mailini gönder
        try:
            send_pro_activated_email(email, name)
        except Exception as e:
            print("Pro mail send failed:", e)

    return jsonify({"ok": True})

```

### app\web\static\css\auth.css

```css
:root{--bg:#0b1120;--panel:#0f172a;--brand:#0ea5e9;--text:#e5edf5;--muted:#9fb0c6;
font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif}
body{background:var(--bg);color:var(--text);margin:0;display:grid;place-items:center;min-height:100vh}
.auth{background:var(--panel);width:min(520px,92vw);padding:28px;border-radius:14px;border:1px solid #1f2a3d}
h1{margin:0 0 12px;font-size:22px}
label{display:block;font-size:13px;color:var(--muted);margin:14px 0 6px}
input{width:100%;padding:10px 12px;border-radius:10px;border:1px solid #22324a;background:#0b1324;color:var(--text)}
button,.btn{margin-top:16px;width:100%;padding:10px 14px;border-radius:10px;border:1px solid #1476b8;
background:var(--brand);color:#041320;font-weight:700;cursor:pointer;text-align:center;text-decoration:none;display:inline-block}
.btn.ghost{background:transparent;color:var(--brand);border-color:#224a66}
.err{background:#26131a;border:1px solid #5a1321;color:#ffb3c0;padding:10px 12px;border-radius:10px;margin-bottom:8px;font-size:13px}
.muted{color:var(--muted);font-size:13px;text-align:center;margin-top:8px}
.row{display:flex;gap:10px;margin-top:12px}

```

### app\web\static\css\landing.css

```css
/* Amazon Trend Finder AI — Landing Page Styles */
:root {
  --bg: #0b1120;
  --text: #e5edf5;
  --muted: #93a4b8;
  --brand: #0ea5e9;
  --panel: #0f172a;
  --radius: 14px;
  --maxw: 1080px;
  font-family: "Inter", system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
}

body {
  background: var(--bg);
  color: var(--text);
  margin: 0;
}

/* NAVBAR */
.nav {
  position: sticky;
  top: 0;
  background: rgba(11,17,32,0.85);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid #1f2937;
  z-index: 100;
}
.nav-inner {
  max-width: var(--maxw);
  margin: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
}
.logo {
  font-weight: 700;
  font-size: 18px;
}
.logo span { color: var(--brand); }
.menu {
  list-style: none;
  display: flex;
  gap: 22px;
  margin: 0;
  padding: 0;
}
.menu a {
  color: var(--muted);
  text-decoration: none;
  font-size: 14px;
}
.menu a:hover { color: var(--brand); }
.btn {
  background: var(--brand);
  color: #041320;
  padding: 10px 16px;
  border-radius: 10px;
  border: none;
  font-weight: 600;
  text-decoration: none;
  transition: 0.2s;
}
.btn:hover { opacity: 0.9; }
.btn.ghost {
  background: transparent;
  border: 1px solid var(--brand);
  color: var(--brand);
}
.btn.small { font-size: 13px; padding: 8px 12px; }
.btn.full { display: block; text-align: center; margin-top: 10px; }

/* HERO */
.hero {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  max-width: var(--maxw);
  margin: 60px auto;
  padding: 0 20px;
  gap: 40px;
}
.hero-content { flex: 1 1 450px; }
.hero-content h1 {
  font-size: 38px;
  line-height: 1.2;
  margin-bottom: 16px;
}
.hero-content p {
  color: var(--muted);
  font-size: 17px;
  margin-bottom: 24px;
}
.cta-group { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px; }
.badges { display: flex; gap: 10px; flex-wrap: wrap; color: var(--muted); font-size: 13px; }
.hero-image img {
  width: 480px;
  max-width: 100%;
  border-radius: 10px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}

/* FEATURES */
.features {
  max-width: var(--maxw);
  margin: 80px auto;
  padding: 0 20px;
  text-align: center;
}
.features h2 { font-size: 28px; margin-bottom: 30px; }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}
.card {
  background: var(--panel);
  border-radius: var(--radius);
  padding: 24px;
  text-align: left;
  border: 1px solid #1f2a3d;
}
.card h3 { color: var(--brand); margin-top: 0; font-size: 18px; }
.card p { color: var(--muted); font-size: 14px; }

/* HOW IT WORKS */
.how {
  max-width: var(--maxw);
  margin: 100px auto;
  padding: 0 20px;
  text-align: center;
}
.how h2 { font-size: 28px; margin-bottom: 40px; }
.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px,1fr));
  gap: 30px;
}
.step img {
  width: 100%;
  border-radius: var(--radius);
  border: 1px solid #1f2a3d;
  margin-bottom: 12px;
}
.step h3 { color: var(--brand); margin: 0 0 8px; }
.step p { color: var(--muted); font-size: 14px; }

/* PRICING */
.pricing {
  background: #0f172a;
  padding: 80px 20px;
  text-align: center;
}
.pricing h2 { font-size: 28px; margin-bottom: 40px; }
.plans {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 30px;
  max-width: var(--maxw);
  margin: auto;
}
.plan {
  background: var(--panel);
  border-radius: var(--radius);
  border: 1px solid #1f2a3d;
  padding: 30px;
  width: 280px;
}
.plan.highlight {
  border: 1px solid var(--brand);
  box-shadow: 0 0 30px rgba(14,165,233,0.2);
}
.plan h3 { font-size: 20px; margin-top: 0; color: var(--brand); }
.price { font-size: 24px; margin: 10px 0; color: var(--text); }
.plan ul { list-style: none; padding: 0; margin: 0 0 10px; }
.plan ul li { color: var(--muted); font-size: 14px; margin: 6px 0; }

/* FAQ */
.faq {
  max-width: var(--maxw);
  margin: 80px auto;
  padding: 0 20px;
}
.faq h2 { text-align: center; font-size: 28px; margin-bottom: 40px; }
details {
  background: var(--panel);
  border-radius: var(--radius);
  border: 1px solid #1f2a3d;
  padding: 16px 20px;
  margin-bottom: 10px;
}
summary {
  font-weight: 600;
  cursor: pointer;
  color: var(--brand);
}
details p { color: var(--muted); font-size: 14px; margin-top: 10px; }

/* FINAL CTA */
.final-cta {
  text-align: center;
  padding: 100px 20px;
}
.final-cta h2 { font-size: 30px; margin-bottom: 10px; }
.final-cta p { color: var(--muted); margin-bottom: 20px; }

/* FOOTER */
.footer {
  border-top: 1px solid #1f2a3d;
  text-align: center;
  padding: 20px;
  font-size: 13px;
  color: var(--muted);
}
.footer .links {
  margin-top: 6px;
  display: flex;
  justify-content: center;
  gap: 16px;
}
.footer a {
  color: var(--muted);
  text-decoration: none;
}
.footer a:hover { color: var(--brand); }

/* Responsive */
@media(max-width:768px){
  .hero{flex-direction:column;}
  .hero-content{text-align:center;}
  .hero-image img{width:100%;}
  .nav-inner{flex-wrap:wrap;gap:10px;}
  .menu{flex-wrap:wrap;justify-content:center;}
}
/* NAV - eski stile uyumlu, logoyu belirgin yap */
.nav { position: sticky; top: 0; z-index: 10; background: #0b0f1a; border-bottom: 1px solid #1b2333; }
.nav-inner { max-width: 1100px; margin: 0 auto; padding: 12px 16px; display: flex; align-items: center; justify-content: space-between; }
.logo { display: flex; align-items: center; gap: 8px; text-decoration: none; }
.logo .brand { font-weight: 700; color: #eaf0ff; }
.logo .ai { color: #7fb0ff; }
.logo-img { height: 20px; display: block; }

.nav-links { display: flex; align-items: center; gap: 14px; }
.nav-links a { color: #cfd7ff; text-decoration: none; }
.user-info { font-size: 0.9em; opacity: 0.85; }
.btn.small { padding: 6px 10px; border-radius: 6px; }
.btn.small.outline { border: 1px solid #3a455b; }
.payment-note{
  margin-top: 18px;
  text-align: center;
  font-size: .92rem;
  color:#aab2be;
}
.trust-bar {
  padding: 22px 0;
  background: #0a0f1c;
  border-top: 1px solid rgba(255,255,255,0.08);
}

.trust-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
  flex-wrap: wrap;
  opacity: .9;
}

.trust-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.trust-item img {
  height: 22px;
  width: auto;
}

.trust-item span {
  color: #94a3b8;
  font-size: 13px;
  letter-spacing: .3px;
}

.case-studies{
  max-width: 1280px;  /* 980 yerine daha geniş */
  margin: 0 auto;
}

.case-card{
  display:flex;
  gap:32px;                     /* 24 → 32 */
  margin-bottom:80px;           /* 60 → 80 */
  background: rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.08);
  border-radius:20px;           /* 16 → 20 */
  padding:40px;                 /* 24px → 40px */
}

.case-img-wrap{
  width:50%;                    /* 40% → 50% */
}

.case-text{
  width:50%;                    /* 60% → 50% */
  line-height:1.75;             /* daha premium */
  font-size:16px;
}

.case-text h3{
  font-size:22px;               /* 20 → 22 */
}

/* RUN → CANCEL görünümü */
.btn.cancel-mode {
  background: #fbbf24 !important;   /* amber-400 */
  color: #1e293b !important;        /* slate-800 */
  border-color: #f59e0b !important; /* amber-500 */
  box-shadow: 0 0 12px rgba(251,191,36,0.5);
}

.btn.cancel-mode:hover {
  background: #f59e0b !important;   /* amber-500 */
  box-shadow: 0 0 14px rgba(245,158,11,0.6);
}


.email-box {
  margin-top: 20px;
  display: flex;
  gap: 8px;
  justify-content: center;
}

.email-box input {
  padding: 10px 14px;
  border-radius: 6px;
  border: 1px solid rgba(255,255,255,0.2);
  background: rgba(255,255,255,0.05);
  color: white;
  width: 250px;
}

.email-box button {
  padding: 10px 18px;
  border-radius: 6px;
  background: #3b82f6;
  color: white;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

```

### app\web\static\css\styles.css

```css
/* Amazon Trend Finder AI — APP Styles (dark theme, final) */
:root {
  --bg: #0b1120;
  --panel: #0f172a;
  --text: #e5edf5;
  --muted: #93a4b8;
  --stroke: #1e293b;
  --brand: #0ea5e9;
  --radius: 12px;
}

* { box-sizing: border-box; }

html, body {
  height: 100%;
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: "Inter", "Segoe UI", Roboto, sans-serif;
  font-size: 15px;
  line-height: 1.55;
}

/* --- Top 3 blue dots (static horizontal) --- */
.top-dots{
  display:flex;
  gap:6px;
  padding:10px 18px 6px;
}
.top-dots span{
  width:8px; height:8px; border-radius:50%;
  background: linear-gradient(180deg, #38bdf8, #0ea5e9);
  box-shadow: 0 0 10px rgba(56,189,248,.65), 0 0 2px rgba(56,189,248,.6) inset;
}

/* Header */
header{
  padding:12px 18px;
  border-top:1px solid var(--stroke);
  border-bottom:1px solid var(--stroke);
  display:flex; align-items:center; gap:10px;
}
header h1{
  margin:0; font-size:16px; font-weight:700; letter-spacing:.2px;
}

/* Controls (filters) */
.controls{
  display:grid; gap:12px;
  grid-template-columns: repeat(auto-fit, minmax(200px,1fr));
  padding:14px 18px;
}
.controls label{
  display:block; font-size:12px; color:var(--muted); margin-bottom:4px;
}
.controls input,.controls select{
  width:100%; padding:10px; border-radius:10px;
  border:1px solid var(--stroke); background:#0b1220; color:var(--text);
}
.actions{ display:flex; align-items:end; gap:8px; }
.btn{
  padding:10px 14px; border-radius:10px; border:1px solid #134e6f;
  background:var(--brand); color:#041320; font-weight:700; cursor:pointer;
  transition:opacity .2s ease;
}
.btn:disabled{ opacity:.6; cursor:not-allowed; }

/* Summary */
.summary{
  padding:6px 18px; display:flex; gap:10px; align-items:center; color:var(--muted);
}
.pill{
  padding:3px 10px; border-radius:999px; background:#0a192f;
  border:1px solid var(--stroke); color:#c8d7ea; font-size:13px;
}

/* Inline loading (table fetch) — animated, unrelated to top dots */
.loading{ display:inline-flex; align-items:center; gap:7px; }
.loading .dot{
  width:6px; height:6px; border-radius:999px; background:var(--brand);
  animation:b 1s infinite alternate;
}
.loading .dot:nth-child(2){ animation-delay:.2s; }
.loading .dot:nth-child(3){ animation-delay:.4s; }
@keyframes b{ from{transform:translateY(0)} to{transform:translateY(-4px)} }

/* Table */
table{ width:100%; border-collapse:collapse; }
thead th{
  text-align:left; font-weight:700; font-size:13px; color:#c7d2df;
  border-bottom:1px solid var(--stroke); padding:10px 14px; user-select:none; cursor:pointer;
}
tbody td{
  border-bottom:1px solid #0e1a2b; padding:12px 14px; font-size:14px; color:#e2e8f0;
}
tbody tr{ transition:background .12s; }
tbody tr:hover{ background:#0d1728; }

/* Empty state */
#empty{ padding:12px 18px; color:var(--muted); }

/* Modal */
.modal{
  position:fixed; inset:0; background:rgba(3,12,24,.55);
  display:flex; align-items:center; justify-content:center; padding:16px;
}
.modal-card{
  background:#0a1424; border:1px solid var(--stroke); border-radius:16px;
  width:min(820px,96vw); max-height:92vh; display:flex; flex-direction:column;
  box-shadow:0 20px 60px rgba(0,0,0,.45);
}
.modal-header{
  display:flex; align-items:center; justify-content:space-between;
  padding:12px 14px; border-bottom:1px solid var(--stroke);
}
.modal-header h3{ margin:0; font-size:15px; }
.modal-header .btn{ background:#0b1220; color:#e5edf5; border:1px solid var(--stroke); }
.chart{ padding:10px 12px 16px; overflow:auto; }
.hidden{ display:none!important; }

/* Chart SVG */
svg .axis line{ stroke:#2a3b52; stroke-width:1; }
svg .axis text{ fill:#96a8bd; font-size:11px; }
svg .line{ fill:none; stroke:#38bdf8; stroke-width:2; }
svg .dot{ fill:#38bdf8; }

/* Toast */
.toast{
  position:fixed; right:12px; bottom:12px; background:#0b1220; color:#e5edf5;
  padding:10px 12px; border-radius:10px; font-size:13px; border:1px solid var(--stroke);
}

/* --------- TOP DOTS: tek kaynak (A harfine kilitli) --------- */

/* Eski kuralları tamamen etkisiz kıl (özellikle padding/gap kalıntıları) */
.top-dots { all: unset; }
.top-dots span { all: unset; }

/* Başlık kutusu */
.app-header{
  position: relative;
  /* soldaki 18px padding genel layout’unla aynı; üstte 22px alan bırakıyoruz */
  padding: 22px 18px 12px 18px;
}

.app-title{
  position: relative;
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: .2px;
}

/* Noktalar artık H1’in içinde; sol kenarı A ile birebir aynı */
.app-title .top-dots{
  position: absolute;
  top: -6px;   /* yükseklik (gerekirse -13 / -15 deneyebilirsin) */
  left: 0;      /* A harfinin tam başlangıcı */
  display: flex;
  gap: 6px;
  padding: 0;
  margin: 0;
}

.app-title .top-dots > span{
  display: block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: linear-gradient(180deg, #3abef8, #139be3);
  box-shadow: 0 0 4px rgba(56,189,248,.55), 0 0 1px rgba(56,189,248,.40) inset;
  opacity: .95;
}

/* Demo banner */
.upgrade-banner{
  margin: 10px 18px;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px dashed #1e293b;
  background: #0b1220;
  color: #c8d7ea;
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
}
.upgrade-banner .btn.small{
  padding: 8px 10px;
  font-size: 13px;
  background: #0ea5e9;
  color:#041320;
  border-radius: 8px;
  text-decoration: none;
}
/* --- Global Navbar (logo + auth) --- */
.nav {
  background: #0b0e17;
  border-bottom: 1px solid rgba(255,255,255,.06);
}
.nav .nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 18px 8%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.nav .logo,
.nav .nav-links a {
  color: #e8ecf0;
  text-decoration: none;
  font-size: 15px;
}
.nav .logo .ai { color: #6aa8ff; }
.nav .nav-links a { margin-left: 20px; opacity: .95; }
.nav .nav-links a:hover { opacity: .75; }

/* buton */
.btn.small {
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  background: #007aff;
  color: #fff;
  display: inline-block;
}
.btn.small:hover { background:#005fcc; }

/* --- Legal pages spacing under navbar --- */
.page.legal {
  max-width: 860px;
  margin: 32px auto;
  padding: 0 20px;
}
.page.legal h1 {
  margin-top: 12px;
}


/* outline versiyon (Log out) */
.btn.small.outline {
  background: transparent;
  color: #e8ecf0;
  border: 1px solid rgba(255,255,255,.15);
}
.btn.small.outline:hover {
  background: rgba(255,255,255,.06);
}
.navbar {
  display: flex; justify-content: space-between; align-items: center;
  background:#0b0e17; padding:18px 8%;
  border-bottom:1px solid rgba(255,255,255,.05);
}
.navbar a { color:#e8ecf0; text-decoration:none; margin-left:20px; font-size:15px; }
.navbar a:hover { opacity:.75; }
.navbar .btn { padding:6px 14px; border-radius:6px; background:#007aff; color:#fff; font-weight:500; font-size:14px; }
.navbar .btn:hover { background:#005fcc; }
.preloader{
  position:fixed; inset:0;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  background:rgba(2, 6, 23, 0.85); /* koyu blur */
  backdrop-filter:saturate(120%) blur(4px);
  z-index:9999;
}
.preloader .spinner{
  width:28px; height:28px; border-radius:50%;
  border:3px solid rgba(148,163,184,.35);
  border-top-color:#22d3ee;
  animation:spin 0.8s linear infinite;
  margin-bottom:12px;
}
.preloader .preloader-text{
  color:#cbd5e1; font-size:14px; letter-spacing:.3px;
}
@keyframes spin{to{transform:rotate(360deg)}}
.hidden{display:none!important;}
/* ===== Preloader ===== */
.preloader{
  position: fixed; inset: 0;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  background: rgba(2,6,23,0.92); /* koyu overlay */
  backdrop-filter: blur(2px);
  z-index: 9999; /* nav ve her şeyin üstünde */
  transition: opacity .25s ease;
}
.preloader.hidden{ opacity: 0; pointer-events: none; }

.preloader .preloader-text{
  margin-top: 12px; font-size: 14px; color: #9ca3af;
}

/* basit spinner */
.spinner{
  width: 42px; height: 42px; border-radius: 50%;
  border: 3px solid rgba(148,163,184,.25);
  border-top-color: #38bdf8; /* mavi */
  animation: spin 0.9s linear infinite;
}
@keyframes spin{ to{ transform: rotate(360deg); } }

```

### app\web\static\js\app.js

```js
/* ================== PRELOADER (global) ================== */
// index.html'deki inline preloader ile uyumlu kapatma fonksiyonu.
// (app.js yüklenir yüklenmez hazır olsun diye en üstte tanımlı)
window.preloaderHide = window.preloaderHide || function () {
  const el = document.getElementById('preloader');
  if (!el) return;
  el.style.opacity = '0';
  el.style.pointerEvents = 'none';
  setTimeout(() => { try { el.remove(); } catch (_) { el.style.display = 'none'; } }, 260);
};
/* ======================================================== */

// DEMO / PRO ayrımı
const MODE = document.body.dataset.mode || 'demo';
const FILTER_KEY = `atf.filters.${MODE}`;

function applyDemoLimits() {
  if (MODE !== 'demo') return; // sadece demo'da çalışır

  // include/exclude kapat
  const inc = document.querySelector('#include');
  const exc = document.querySelector('#exclude');
  if (inc) { inc.disabled = true; inc.placeholder = "Available in Pro"; }
  if (exc) { exc.disabled = true; exc.placeholder = "Available in Pro"; }

  // hafta sayısını 8 ile sınırla
  const limitWeeks = () => {
    const startSel = document.querySelector('#start');
    const endSel = document.querySelector('#end');
    const trim = (sel, keepLastN = 6) => {
      if (!sel) return;
      const opts = Array.from(sel.querySelectorAll('option'));
      const toRemove = opts.slice(0, Math.max(0, opts.length - keepLastN));
      toRemove.forEach(o => o.remove());
    };
    trim(startSel, 6);
    trim(endSel, 6);
    // trim sonrası seçili değerler uçtuysa son seçeneklere çek
if (startSel && startSel.options.length) {
  startSel.value = startSel.options[0].value;
}
if (endSel && endSel.options.length) {
  endSel.value = endSel.options[endSel.options.length - 1].value;
}

  };

  setTimeout(limitWeeks, 0);
}

// ---------------- Preloader helper (yerel) ----------------
function hidePreloader() {
  // hem yerel fonksiyonu hem de global fallback'i tetikle
  window.preloaderHide && window.preloaderHide();
}

// ----------------------------------------------------------

const $ = (sel)=>document.querySelector(sel);

const startSel = $("#start"), endSel = $("#end");
const includeInp = $("#include"), excludeInp = $("#exclude");
const runBtn = $("#run");
const reindexBtn = $("#reindex");                 // may be null
const tbody = $("#tbl tbody"), found = $("#found");
const emptyEl = $("#empty");                      // may be null
const rangePill = $("#range") || $("#rangeBadge");// support both ids
const statusEl = $("#status");                    // may be null

const modal = $("#modal"), closeModalBtn = $("#closeModal"), chartEl = $("#chart");
const toast = $("#toast");                        // may be null

let weeks = [];
let lastFocusedBeforeModal = null;
let currentSort = { key: "total_improvement", dir: "desc" };
let currentController = null;
let isRunningQuery = false;

/* ---------- helpers ---------- */
function showToast(msg, ms=2600){
  if(!toast) { console.warn(msg); return; }
  toast.textContent = msg;
  toast.classList.remove("hidden");
  setTimeout(()=>toast.classList.add("hidden"), ms);
}

async function fetchJSON(url, signal){
  const res = await fetch(url, { signal });
  if(!res.ok){
    const t = await res.text().catch(()=>res.statusText);
    throw new Error(`${res.status} ${res.statusText} - ${t}`);
  }
  return res.json();
}


function setLoading(on){
  if(statusEl){
    statusEl.classList.toggle("hidden", !on);
    statusEl.setAttribute("aria-hidden", on ? "false":"true");
  }

  // runBtn loading’de disable edilmez → Stop çalışsın
  // sadece diğer actionlar kilitlenir
  if(reindexBtn) reindexBtn.disabled = on;

  // input/selectleri kilitle (Stop basılana kadar)
  if(startSel) startSel.disabled = on;
  if(endSel) endSel.disabled = on;

  // demo’da zaten disabled ama pro’da da kilitle
  if(includeInp) includeInp.disabled = on || (MODE === "demo");
  if(excludeInp) excludeInp.disabled = on || (MODE === "demo");
}


function persistFilters(){
  const data = {
    start: startSel.value,
    end: endSel.value,
    include: includeInp.value,
    exclude: excludeInp.value
  };
  localStorage.setItem(FILTER_KEY, JSON.stringify(data));
}

function restoreFilters(){
  const raw = localStorage.getItem(FILTER_KEY);
  if(!raw) return;

  try{
    const d = JSON.parse(raw);

    if(d.start) startSel.value = String(d.start);
    if(d.end)   endSel.value   = String(d.end);

    // Demo'da include/exclude her zaman boş kalır
    if(MODE === "demo"){
      includeInp.value = "";
      excludeInp.value = "";
      return;
    }

    if(d.include != null) includeInp.value = d.include;
    if(d.exclude != null) excludeInp.value = d.exclude;

  }catch(err){
    console.error("restoreFilters error:", err);
  }
}



/* ---------- weeks ---------- */
async function loadWeeks(){
  setLoading(true);
  try{
    weeks = await fetchJSON("/weeks");
    startSel.innerHTML = ""; endSel.innerHTML = "";
    for(const w of weeks){
      const o1 = document.createElement("option"); o1.value = w.weekId; o1.textContent = `Week ${w.label}`;
      const o2 = document.createElement("option"); o2.value = w.weekId; o2.textContent = `Week ${w.label}`;
      startSel.appendChild(o1); endSel.appendChild(o2);
    }
    if(weeks.length >= 2){
      startSel.value = weeks[Math.max(0, weeks.length-6)].weekId; // default: last 6 weeks window
      endSel.value = weeks[weeks.length-1].weekId;
    }
    restoreFilters();

    // ✅ Haftalar geldi, preloader'ı kapat
    hidePreloader();

  }catch(err){
    showToast("Failed to load weeks.");
    console.error(err);
    // ✅ Hata bile olsa preloader'ı kapat
    hidePreloader();
  }finally{
    setLoading(false);
  }
}

function parseWeeks(){
  let s = parseInt(startSel.value,10), e = parseInt(endSel.value,10);
  if(!s || !e) throw new Error("Please select start and end week.");
  if(e < s){ const t=s; s=e; e=t; }
  if((e - s + 1) < 2) throw new Error("Range must be at least 2 weeks.");

  const sLabel = weeks.find(w=>w.weekId===s)?.label || s;
  const eLabel = weeks.find(w=>w.weekId===e)?.label || e;
  const total = (e - s + 1);
  return { s, e, sLabel, eLabel, total };
}

async function runQuery(){
  // Eğer zaten çalışıyorsa → STOP gibi davran
  if (isRunningQuery && currentController){
    currentController.abort();
    currentController = null;
    isRunningQuery = false;

    if(runBtn){
      runBtn.textContent = "Find uptrends";
      runBtn.classList.remove("danger");
      runBtn.disabled = false;
    }

    setLoading(false);
    return;
  }

  // Yeni sorgu başlatılıyor
  currentController = new AbortController();
  isRunningQuery = true;

  if(runBtn){
    runBtn.textContent = "Cancel Search";
    runBtn.classList.add("danger");
    runBtn.disabled = false; // stop’a basabilsin
  }

 try{
  setLoading(true);
  if (runBtn) runBtn.disabled = false;

    const { s, e, sLabel, eLabel, total } = parseWeeks();
    if(rangePill) rangePill.textContent = `${total} weeks • ${sLabel} → ${eLabel}`;

    const norm = str => str.replaceAll(",", " ").trim();
    const params = new URLSearchParams({
      startWeekId: s, endWeekId: e,
      include: norm(includeInp.value),
      exclude: norm(excludeInp.value),
    });

    const rows = await fetchJSON(
      "/uptrends?" + params.toString(),
      currentController.signal
    );

    const sorted = sortRows(rows, currentSort.key, currentSort.dir);
    renderTable(sorted, s, e);
    persistFilters();

    hidePreloader();

  }catch(err){
    if(err.name !== "AbortError"){
      showToast(err.message || "Query failed.");
      console.error(err);
    }
  }finally{
    setLoading(false);

    isRunningQuery = false;
    currentController = null;

    if(runBtn){
      runBtn.textContent = "Find uptrends";
      runBtn.classList.remove("danger");
      runBtn.disabled = false;
    }
  }
}


function sortRows(rows, key, dir){
  const mul = dir === "desc" ? -1 : 1;
  return [...rows].sort((a,b)=>{
    let va = a[key], vb = b[key];
    const na = typeof va === "number", nb = typeof vb === "number";
    if(na && nb) return (va - vb) * mul;
    return String(va).localeCompare(String(vb)) * mul;
  });
}

function renderTable(rows, s, e){
  tbody.innerHTML = "";
  found.textContent = `Found: ${rows.length}`;
  if(emptyEl) emptyEl.classList.toggle("hidden", rows.length>0);

  for(const r of rows){
    const tr = document.createElement("tr");
    tr.tabIndex = 0;
    tr.innerHTML = `
      <td>${r.term}</td>
      <td>${r.start_rank}</td>
      <td>${r.end_rank}</td>
      <td>${r.total_improvement}</td>
      <td>${r.weeks}</td>
    `;
    const open = ()=>showSeries(r.term, s, e);
    tr.addEventListener("click", open);
    tr.addEventListener("keydown", (ev)=>{ if(ev.key==="Enter" || ev.key===" ") { ev.preventDefault(); open(); }});
    tbody.appendChild(tr);
  }
}

/* ---------- series + chart ---------- */
async function showSeries(term, s, e){
  try{
    setLoading(true);
    const params = new URLSearchParams({ term, startWeekId: s, endWeekId: e });
    const data = await fetchJSON("/series?" + params.toString());
    drawMiniChart(term, data);
    openModal();
  }catch(err){
    showToast("Failed to load series.");
    console.error(err);
  }finally{
    setLoading(false);
  }
}

function drawMiniChart(title, data){
  // y axis reversed (smaller rank = better)
  const ranks = data.map(d=>d.rank).filter(v=>Number.isFinite(v));
  const minR = ranks.length ? Math.min(...ranks) : 0;
  const maxR = ranks.length ? Math.max(...ranks) : 1;

  const pad = 24, W = 740, H = 260;
  const y = (v)=> {
    const t = (v - minR) / Math.max(1, (maxR - minR));
    return pad + (H - 2*pad) * t;
  };
  const x = (i)=> pad + (W - 2*pad) * (i/(Math.max(1, data.length-1)));

  const pts = data.map((d,i)=>{
    const rr = Number.isFinite(d.rank) ? d.rank : null;
    return { x:x(i), y: rr!==null? y(rr): null, label:d.weekLabel, rank: rr };
  });

  let path = "";
  for(let i=0;i<pts.length;i++){
    const p = pts[i];
    if(p.y===null) continue;
    path += (path===""? `M ${p.x} ${p.y}` : ` L ${p.x} ${p.y}`);
  }

 const svg = `
  <svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${title} rank chart"
       style="font-family:Inter, sans-serif; font-size:14px; fill:#e2e8f0;">
    
    <g class="axis" stroke="#334155" stroke-width="1">
      <!-- Y axis -->
      <line x1="${pad}" y1="${pad}" x2="${pad}" y2="${H-pad}" />
      
      <!-- X axis -->
      <line x1="${pad}" y1="${H-pad}" x2="${W-pad}" y2="${H-pad}" />

      <!-- Min rank -->
      <text x="${pad+4}" y="${pad+4}" fill="#e2e8f0" font-size="14" font-weight="600">
        ${minR}
      </text>

      <!-- Start week -->
      <text x="${pad}" y="${H-pad+20}" fill="#cbd5e1" font-size="13">
        ${data[0]?.weekLabel || ""}
      </text>

      <!-- End week -->
      <text x="${W-pad-60}" y="${H-pad+20}" fill="#cbd5e1" font-size="13">
        ${data[data.length-1]?.weekLabel || ""}
      </text>
    </g>

    <!-- Trend line -->
    <path class="line" d="${path}" stroke="#38bdf8" stroke-width="3" fill="none"/>

    <!-- Dots -->
    ${pts.map(p => 
      p.y===null ? "" :
      `<circle cx="${p.x}" cy="${p.y}" r="4" fill="#38bdf8">
         <title>${p.label} • rank ${p.rank}</title>
       </circle>`
    ).join("")}
     <!-- Watermark -->
    <text 
  x="${W - pad - 90}" 
  y="${H - 10}"
  fill="#e2e8f0" opacity="0.45"
  font-size="12" text-anchor="end">
  uptrendhunter.com
</text>

  </svg>`;

  $("#modalTitle").textContent = title;
  chartEl.innerHTML = svg;
}

/* ---------- modal a11y ---------- */
function openModal(){
  lastFocusedBeforeModal = document.activeElement;
  modal.classList.remove("hidden");
  closeModalBtn && closeModalBtn.focus();
  document.addEventListener("keydown", escClose);
  document.addEventListener("focus", trapFocus, true);
}
function closeModal(){
  modal.classList.add("hidden");
  document.removeEventListener("keydown", escClose);
  document.removeEventListener("focus", trapFocus, true);
  if(lastFocusedBeforeModal) lastFocusedBeforeModal.focus();
}
function escClose(e){ if(e.key==="Escape") closeModal(); }
function trapFocus(e){
  if(modal.classList.contains("hidden")) return;
  if(!modal.contains(e.target)){
    e.stopPropagation();
    closeModalBtn && closeModalBtn.focus();
  }
}

/* ---------- events ---------- */
runBtn && runBtn.addEventListener("click", runQuery);

// reindex button is optional; guard it
if (reindexBtn) {
  reindexBtn.addEventListener("click", async ()=>{
    try{
      setLoading(true);
      await fetchJSON("/reindex");
      await loadWeeks();
      showToast("Reindex completed.");
    }catch(err){
      showToast("Reindex failed.");
      console.error(err);
    }finally{
      setLoading(false);
    }
  });
}

closeModalBtn && closeModalBtn.addEventListener("click", closeModal);
modal.addEventListener("click",(e)=>{ if(e.target===modal) closeModal(); });

document.addEventListener("keydown",(e)=>{
  if((e.ctrlKey || e.metaKey) && e.key.toLowerCase()==="enter"){ runQuery(); }
});

/* sortable headers (data-key attrs must exist) */
document.querySelectorAll("#tbl thead th").forEach(th=>{
  th.addEventListener("click", ()=>{
    const key = th.dataset.key;
    if(!key) return;
    currentSort = {
      key,
      dir: (currentSort.key===key && currentSort.dir==="asc") ? "desc" : "asc"
    };
    const rows = Array.from(tbody.querySelectorAll("tr")).map(tr=>{
      const [term, s, e, imp, w] = Array.from(tr.children).map(td=>td.textContent);
      return {
        term,
        start_rank: Number(s), end_rank: Number(e),
        total_improvement: Number(imp), weeks: Number(w)
      };
    });
    const { s, e } = parseWeeks();
    const sorted = sortRows(rows, currentSort.key, currentSort.dir);
    renderTable(sorted, s, e);
  });
});

/* persist filters */
[startSel, endSel, includeInp, excludeInp].forEach(el=>{
  el.addEventListener("change", persistFilters);
  el.addEventListener("input", persistFilters);
});

/* init */
loadWeeks()
  .then(() => { applyDemoLimits(); })
  .then(runQuery)
  .catch(console.error);

// preloader'ı ekstra güvenceyle kapat
document.addEventListener('DOMContentLoaded', ()=> window.preloaderHide && window.preloaderHide());
window.addEventListener('load', ()=> window.preloaderHide && window.preloaderHide());

```

### app\web\templates\_nav.html

```html
<style>
/* --- Embedded navbar styles (works on every page) --- */
.nav{background:#0b0e17;border-bottom:1px solid rgba(255,255,255,.06)}
.nav .nav-inner{max-width:1200px;margin:0 auto;padding:18px 8%;
  display:flex;align-items:center;justify-content:space-between}
.nav .logo,.nav .nav-links a{color:#e8ecf0;text-decoration:none;font-size:15px}
.nav .logo .ai{color:#6aa8ff}
.nav .nav-links a{margin-left:20px;opacity:.95}
.nav .nav-links a:hover{opacity:.75}
.btn.small{padding:6px 14px;border-radius:8px;font-size:14px;font-weight:600;
  background:#007aff;color:#fff;display:inline-block}
.btn.small:hover{background:#005fcc}
.btn.small.outline{background:transparent;color:#e8ecf0;border:1px solid rgba(255,255,255,.15)}
.btn.small.outline:hover{background:rgba(255,255,255,.06)}
</style>


<nav class="nav">
  <div class="nav-inner">
    <a href="{{ url_for('landing') }}" class="logo">
      <span class="brand">Uptrend Hunter <span class="ai">AI</span></span>
    </a>

    <div class="nav-links">
      <a href="/academy">Academy</a>

      {% if current_user %}
        <a href="{{ url_for('dashboard') }}">Dashboard</a>

        {% if current_user.plan == "pro" %}
          <a href="{{ url_for('app_pro') }}">Pro</a>
        {% else %}
          <a href="{{ url_for('checkout') }}">Upgrade</a>
        {% endif %}

        <a href="{{ url_for('logout') }}" class="btn small outline">Log out</a>
      {% else %}
        <a href="{{ url_for('login', next=request.path) }}" class="btn small">Log in</a>
      {% endif %}
    </div>
  </div>
</nav>


```

### app\web\templates\academy_build_product_ideas.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>

  <title>How to Build Product Ideas From Rising Terms</title>
  <link rel="canonical" href="https://www.uptrendhunter.com/academy/build-product-ideas"/>

  <meta name="description" content="A practical guide to turning rising search terms into validated product ideas, niche opportunities, and early launches using marketplace demand signals."/>
  <meta name="robots" content="index,follow"/>

  <!-- Open Graph -->
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="Uptrend Hunter AI"/>
  <meta property="og:url" content="https://www.uptrendhunter.com/academy/build-product-ideas"/>
  <meta property="og:title" content="How to Build Product Ideas From Rising Terms"/>
  <meta property="og:description" content="Learn how to convert rising marketplace search terms into real product opportunities and early launch ideas."/>

  <!-- Twitter -->
  <meta name="twitter:card" content="summary"/>
  <meta name="twitter:title" content="How to Build Product Ideas From Rising Terms"/>
  <meta name="twitter:description" content="Learn how to convert rising marketplace search terms into product ideas."/>

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <style>
    .academy-wrap{max-width:980px;margin:0 auto;padding:40px 8%}
    .academy-wrap h1{font-size:34px;line-height:1.15;margin:10px 0 10px}
    .academy-wrap p{max-width:80ch}
    .kicker{opacity:.9}
    .meta{opacity:.7;font-size:14px;margin:8px 0 22px}
    .card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:18px;margin:18px 0}
    .grid{display:grid;grid-template-columns:1fr;gap:14px}
    @media(min-width:900px){.grid{grid-template-columns:1fr 1fr}}
    ul.check{margin:0;padding-left:18px}
    ul.check li{margin:6px 0}
  </style>
</head>

<body>
  {% include "_nav.html" %}

  <main class="academy-wrap">
    <p class="kicker">Academy • Product Research</p>
    <h1>How to Build Product Ideas From Rising Terms</h1>
    <p class="meta">Updated: 2025-11-30 • Read time: ~7 minutes</p>

    <div class="card">
      <h2>Why rising terms = early product signals</h2>
      <p>
        When a search term improves in rank across multiple weeks, it tells you something is
        gaining attention — demand is forming before supply catches up.
      </p>
      <p>
        Your job is to translate these demand signals into product ideas before the market becomes crowded.
      </p>
    </div>

    <h2>Step 1 — Identify breakout “clusters”</h2>
    <div class="card">
      <p>Don’t evaluate terms one by one at first. Look for clusters:</p>
      <ul class="check">
        <li>multiple rising terms sharing the same core word,</li>
        <li>variations of the same concept (style/material/recipient),</li>
        <li>a family of items trending together.</li>
      </ul>
      <p>
        Clusters = the strongest early signal that a niche is heating up.
      </p>
    </div>

    <h2>Step 2 — Read “intent type” from the term</h2>
    <div class="grid">
      <div class="card">
        <h3>Product intent</h3>
        <ul class="check">
          <li>“penguin crochet doll”</li>
          <li>“wooden name sign”</li>
          <li>“stainless steel mug with lid”</li>
        </ul>
        <p>These indicate direct product ideas.</p>
      </div>

      <div class="card">
        <h3>Problem intent</h3>
        <ul class="check">
          <li>“kitchen clutter solution”</li>
          <li>“pet hair remover tool”</li>
        </ul>
        <p>These hint at gaps you can solve with a product variation.</p>
      </div>
    </div>

    <h2>Step 3 — Use modifiers to shape product direction</h2>
    <div class="card">
      <p>Certain modifiers show what the market wants more specifically:</p>
      <ul class="check">
        <li>material → wooden, steel, acrylic, silicone</li>
        <li>recipient → mom, dad, grandma, teacher</li>
        <li>style → vintage, cute, minimalist</li>
        <li>occasion → birthday, Christmas, wedding</li>
      </ul>
      <p>
        These modifiers help you shape an idea into a real product concept.
      </p>
    </div>

    <h2>Step 4 — Validate with multi-angle checks</h2>
    <div class="grid">
      <div class="card">
        <h3>Demand-side</h3>
        <ul class="check">
          <li>Is the term consistently improving?</li>
          <li>Is it part of a cluster?</li>
          <li>Is there follow-through in the chart?</li>
        </ul>
      </div>
      <div class="card">
        <h3>Supply-side</h3>
        <ul class="check">
          <li>Is the space crowded or immature?</li>
          <li>Are existing listings weak?</li>
          <li>Are there easy angles to differentiate?</li>
        </ul>
      </div>
    </div>

    <h2>Step 5 — Build a quick “Product Angle Sheet”</h2>
    <div class="card">
      <p>Create a sheet with 5 columns:</p>
      <ul class="check">
        <li><strong>Term</strong></li>
        <li><strong>Why it’s rising</strong></li>
        <li><strong>Modifier pattern</strong> (material, recipient, style)</li>
        <li><strong>Gap / improvement opportunity</strong></li>
        <li><strong>PPC testing angle</strong></li>
      </ul>
      <p>
        This turns raw signals into structured ideas you can act on.
      </p>
    </div>

    <h2>Step 6 — Turn the idea into an actual opportunity</h2>
    <div class="card">
      <ul class="check">
        <li>Prototype the niche: which listings dominate?</li>
        <li>List the “weak spots” of top-sellers.</li>
        <li>Use rising modifiers to create a unique angle.</li>
        <li>Run PPC tests on smaller variations before committing.</li>
      </ul>
      <p>
        Rising terms tell you <em>what</em> is forming. Your differentiation tells you <em>how</em> to win it.
      </p>
    </div>

    <div class="card">
      <h2>What to avoid</h2>
      <ul class="check">
        <li>Chasing single-week spikes.</li>
        <li>Assuming one term = one product automatically.</li>
        <li>Ignoring the supply side — demand without execution is useless.</li>
      </ul>
      <p>
        Product opportunities appear when rising demand meets weak supply.
      </p>
    </div>

    <p class="meta">
      Back to: <a href="/academy">Academy</a> · Related:
      <a href="/academy/how-to-use">How to use Uptrend Hunter</a> ·
      <a href="/academy/include-exclude">Include/Exclude filters</a> ·
      <a href="/academy/weekly-routine">Weekly routine</a>
    </p>
  </main>

  <footer class="footer" style="text-align:center; padding:30px 0; border-top:1px solid #1e293b;">
    <p>© 2025 Uptrend Hunter by Erkan Ecom LLC. All rights reserved.</p>
    <div class="links" style="margin-top:10px;">
      <a href="/" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Home</a> |
      <a href="/terms" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Terms</a> |
      <a href="/privacy" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Privacy</a> |
      <a href="/refund" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Refund</a> |
      <a href="mailto:support@uptrendhunter.com" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Contact</a>
    </div>
  </footer>
</body>
</html>

```

### app\web\templates\academy_ceo_brief.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>CEO Brief — Uptrend Hunter AI</title>

  <link rel="canonical" href="https://www.uptrendhunter.com/academy/ceo-brief">
  <meta name="description" content="Executive brief: how Uptrend Hunter changes Amazon PPC + product timing decisions, what KPIs to track, and how to roll it out.">
  <meta name="robots" content="index,follow">

  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Uptrend Hunter AI">
  <meta property="og:url" content="https://www.uptrendhunter.com/academy/ceo-brief">
  <meta property="og:title" content="CEO Brief: PPC + product timing">
  <meta property="og:description" content="What changes, KPIs to track, and rollout plan.">

  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="CEO Brief: PPC + product timing">
  <meta name="twitter:description" content="What changes, KPIs to track, and rollout plan.">

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "CEO Brief: PPC + product timing",
    "about": ["Amazon PPC", "Keyword trends", "Product research"],
    "author": { "@type": "Organization", "name": "Uptrend Hunter AI" },
    "publisher": { "@type": "Organization", "name": "Uptrend Hunter AI" },
    "mainEntityOfPage": "https://www.uptrendhunter.com/academy/ceo-brief"
  }
  </script>
</head>

<body>
  {% include "_nav.html" %}

  <section style="max-width:980px;margin:0 auto;padding:56px 18px;">
    <div style="opacity:.75;font-size:13px;margin-bottom:10px;">
      <a href="/academy" style="color:#9aa0a6;text-decoration:none;">Academy</a> / Executive
    </div>

    <h1 style="margin:0 0 12px 0;">CEO Brief: PPC + product timing</h1>
    <p style="color:#93a4b8;max-width:780px;margin:0 0 22px 0;">
      The goal is simple: spot demand shifts early, then move budgets and launches before competitors react.
    </p>

    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin:18px 0 26px;">
      <div style="border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;">
        <div style="font-weight:700;">What changes</div>
        <ul style="color:#93a4b8;margin:10px 0 0 18px;">
          <li>Faster keyword discovery (new rising terms)</li>
          <li>Less reactive PPC (shift spend earlier)</li>
          <li>Better product timing (launch before peak)</li>
        </ul>
      </div>

      <div style="border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;">
        <div style="font-weight:700;">KPIs to watch</div>
        <ul style="color:#93a4b8;margin:10px 0 0 18px;">
          <li>CTR / CVR on new rising terms</li>
          <li>Acos / Tacos trend for “early” groups</li>
          <li>Share of spend moved to rising terms</li>
        </ul>
      </div>

      <div style="border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;">
        <div style="font-weight:700;">Rollout (7 days)</div>
        <ol style="color:#93a4b8;margin:10px 0 0 18px;">
          <li>Pick 1 category + 1 hero ASIN</li>
          <li>Run weekly scan (same range each week)</li>
          <li>Promote top 10 terms into a test campaign</li>
          <li>Scale winners, kill losers fast</li>
        </ol>
      </div>
    </div>

    <h2 style="margin:26px 0 10px;">How to use it in PPC (simple rule)</h2>
    <p style="color:#93a4b8;max-width:820px;margin:0 0 10px;">
      If a term is consistently improving (rank getting better) across your selected weeks, treat it as
      an “early signal” keyword. Start small (exact + phrase), measure, then scale.
    </p>

    <div style="margin-top:18px;">
      <a href="/academy/how-to-use" class="btn">Read: How to use</a>
      <a href="/app" class="btn" style="margin-left:10px;">Try demo</a>
    </div>
  </section>

  <footer class="footer" style="text-align:center; padding:30px 0; border-top:1px solid #1e293b;">
    <p>© 2025 Uptrend Hunter by Erkan Ecom LLC. All rights reserved.</p>
  </footer>
</body>
</html>

```

### app\web\templates\academy_fba_seasonality.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>

  <title>Amazon FBA: Seasonality vs Real Trend (Avoid Dead Stock)</title>
  <link rel="canonical" href="https://www.uptrendhunter.com/academy/amazon-fba-seasonality"/>

  <meta name="description" content="Amazon FBA guide to separate pure seasonality from real underlying trends using marketplace search momentum. Avoid over-ordering on temporary spikes and dead inventory."/>
  <meta name="robots" content="index,follow"/>

  <!-- Open Graph -->
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="Uptrend Hunter AI"/>
  <meta property="og:url" content="https://www.uptrendhunter.com/academy/amazon-fba-seasonality"/>
  <meta property="og:title" content="Amazon FBA: Seasonality vs Real Trend (Avoid Dead Stock)"/>
  <meta property="og:description" content="Learn how to read marketplace trend data so you don't confuse a seasonal spike with a long-term Amazon FBA opportunity."/>

  <!-- Twitter -->
  <meta name="twitter:card" content="summary"/>
  <meta name="twitter:title" content="Amazon FBA: Seasonality vs Real Trend (Avoid Dead Stock)"/>
  <meta name="twitter:description" content="Learn how to read marketplace trend data so you don't confuse a seasonal spike with a long-term Amazon FBA opportunity."/>

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <style>
    .academy-wrap{max-width:980px;margin:0 auto;padding:40px 8%}
    .academy-wrap h1{font-size:34px;line-height:1.15;margin:10px 0 10px}
    .academy-wrap p{max-width:80ch}
    .kicker{opacity:.9}
    .meta{opacity:.7;font-size:14px;margin:8px 0 22px}
    .card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:18px;margin:18px 0}
    .grid{display:grid;grid-template-columns:1fr;gap:14px}
    @media(min-width:900px){.grid{grid-template-columns:1fr 1fr}}
    ul.check{margin:0;padding-left:18px}
    ul.check li{margin:6px 0}
  </style>
</head>

<body>
  {% include "_nav.html" %}

  <main class="academy-wrap">
    <p class="kicker">Academy • Amazon FBA</p>
    <h1>Amazon FBA: Seasonality vs Real Trend (Avoid Dead Stock)</h1>
    <p class="meta">Updated: 2025-11-30 • Read time: ~9 minutes</p>

    <div class="card">
      <h2>Why seasonality can kill FBA inventory</h2>
      <p>
        A rising search curve looks exciting… until you realize it was just
        a seasonal wave and you’re sitting on 6 months of dead stock.
        Shopify can survive that. FBA can’t.
      </p>
      <p>
        This guide shows you how to use search momentum to separate:
      </p>
      <ul class="check">
        <li><strong>Pure seasonal bumps</strong> (Christmas, Mother’s Day, back-to-school)</li>
        <li><strong>Short “hype” spikes</strong> (social media / viral mentions)</li>
        <li><strong>Real underlying trends</strong> (new habits, lasting demand)</li>
      </ul>
    </div>

    <h2>Step 1 — Look at enough weeks</h2>
    <div class="card">
      <p>
        For FBA, you should rarely make a decision on less than
        <strong>12–18+ weeks</strong> of data:
      </p>
      <ul class="check">
        <li>Short ranges (4–6 weeks) are great for finding ideas,</li>
        <li>Longer ranges are mandatory before spending real inventory money.</li>
      </ul>
      <p>
        If a term only looks strong in a very narrow window and disappears outside it,
        you are probably looking at seasonality or a one-off event.
      </p>
    </div>

    <h2>Step 2 — Recognize classic seasonal shapes</h2>
    <div class="grid">
      <div class="card">
        <h3>Seasonal pattern</h3>
        <ul class="check">
          <li>Sharp climb → sharp peak → sharp drop</li>
          <li>Aligns with obvious calendar events</li>
          <li>Long periods of low activity outside the peak</li>
        </ul>
      </div>
      <div class="card">
        <h3>Trend pattern</h3>
        <ul class="check">
          <li>Stair-step or gradual improvement</li>
          <li>Higher lows over time</li>
          <li>No full collapse after one date</li>
        </ul>
      </div>
    </div>
    <div class="card">
      <p>
        If you zoom out and the curve looks like a narrow mountain around a holiday,
        treat it as seasonal by default.
      </p>
    </div>

    <h2>Step 3 — Check for repeated yearly waves</h2>
    <div class="card">
      <p>
        Some products are <strong>seasonal but predictable</strong> (e.g. ornaments, certain gifts).
        These can still be good FBA plays if:
      </p>
      <ul class="check">
        <li>the wave appears around the same time each year,</li>
        <li>you can time production and shipping correctly,</li>
        <li>you are comfortable with off-season slow sales.</li>
      </ul>
      <p>
        When possible, compare the current year’s wave with previous periods:
        a product that comes back stronger each year is far safer than a one-time spike.
      </p>
    </div>

    <h2>Step 4 — Align search terms with obvious events</h2>
    <div class="card">
      <p>
        Many rising terms literally tell you they are seasonal:
      </p>
      <ul class="check">
        <li>“christmas ornament…”, “xmas tree…”, “halloween costume…”</li>
        <li>“mother’s day gift…”, “father’s day mug…”, “valentines gift…”</li>
        <li>“back to school…”, “easter basket…”</li>
      </ul>
      <p>
        For these, your decision isn’t “trend vs seasonality” — it’s:
      </p>
      <ul class="check">
        <li>Can I execute timing and logistics better than others?</li>
        <li>Will I differentiate enough to win during the peak window?</li>
      </ul>
    </div>

    <h2>Step 5 — Watch out for short hype spikes</h2>
    <div class="card">
      <p>
        Some curves are neither standard seasonal nor long-term trend.
        They’re just hype:
      </p>
      <ul class="check">
        <li>1–3 weeks of explosive improvement,</li>
        <li>no real base before, no support after,</li>
        <li>often linked to a social media moment.</li>
      </ul>
      <p>
        These are extremely dangerous for FBA because production and shipping
        are too slow. By the time your stock arrives, the hype is gone.
      </p>
    </div>

    <h2>Step 6 — Combine search data with listing reality</h2>
    <div class="card">
      <p>
        Before committing to a “trend”, always open the actual search results:
      </p>
      <ul class="check">
        <li>Are top listings clearly seasonal (themes, text, imagery)?</li>
        <li>Do successful listings survive outside the season?</li>
        <li>Are there generic versions that sell all year using different angles?</li>
      </ul>
      <p>
        Sometimes the underlying product is evergreen, but one angle
        (like a holiday gift) is seasonal. You can launch the base product
        and use different positioning the rest of the year.
      </p>
    </div>

    <h2>Step 7 — Decide strategy by product type</h2>
    <div class="grid">
      <div class="card">
        <h3>Pure seasonal products</h3>
        <ul class="check">
          <li>Smaller initial order</li>
          <li>Stronger focus on timing & logistics</li>
          <li>Accept off-season low sales</li>
        </ul>
      </div>
      <div class="card">
        <h3>Evergreen products with seasonal peaks</h3>
        <ul class="check">
          <li>Build listing for evergreen use case</li>
          <li>Layer seasonal keywords & creatives around peaks</li>
          <li>Use seasonality as a booster, not the entire strategy</li>
        </ul>
      </div>
    </div>

    <div class="card">
      <h2>Step 8 — Practical checklist before calling it a “trend”</h2>
      <ul class="check">
        <li>Improvement visible over multiple weeks, not 1–2 only</li>
        <li>No single date explains the entire spike</li>
        <li>Term (or close variations) stay relevant outside one holiday</li>
        <li>Competitor listings show year-round demand, not only seasonal designs</li>
      </ul>
      <p>
        If this checklist fails, treat it as seasonal or hype — and size your
        inventory accordingly.
      </p>
    </div>

    <p class="meta">
      Back to: <a href="/academy">Academy</a> · Related:
      <a href="/academy/amazon-fba-validation">FBA trend validation</a> ·
      <a href="/academy/trend-vs-seasonality">Trend vs seasonality (general)</a>
    </p>
  </main>

  <footer class="footer" style="text-align:center; padding:30px 0; border-top:1px solid #1e293b;">
    <p>© 2025 Uptrend Hunter by Erkan Ecom LLC. All rights reserved.</p>
    <div class="links" style="margin-top:10px;">
      <a href="/" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Home</a> |
      <a href="/terms" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Terms</a> |
      <a href="/privacy" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Privacy</a> |
      <a href="/refund" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Refund</a> |
      <a href="mailto:support@uptrendhunter.com" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Contact</a>
    </div>
  </footer>
</body>
</html>

```

### app\web\templates\academy_fba_validation.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>

  <title>Amazon FBA: Validate Rising Search Terms Before Ordering Inventory</title>
  <link rel="canonical" href="https://www.uptrendhunter.com/academy/amazon-fba-validation"/>

  <meta name="description" content="A complete Amazon FBA framework for validating rising marketplace search terms before ordering inventory. Avoid fake spikes, seasonality traps, and low-margin products."/>
  <meta name="robots" content="index,follow"/>

  <!-- Open Graph -->
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="Uptrend Hunter AI"/>
  <meta property="og:url" content="https://www.uptrendhunter.com/academy/amazon-fba-validation"/>
  <meta property="og:title" content="Amazon FBA: Validate Rising Search Terms Before Ordering Inventory"/>
  <meta property="og:description" content="A risk-proof validation system for Amazon FBA sellers using rising search terms."/>

  <!-- Twitter -->
  <meta name="twitter:card" content="summary"/>
  <meta name="twitter:title" content="Amazon FBA: Validate Rising Search Terms Before Ordering Inventory"/>
  <meta name="twitter:description" content="A risk-proof validation system for Amazon FBA sellers using rising search terms."/>

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <style>
    .academy-wrap{max-width:980px;margin:0 auto;padding:40px 8%}
    .academy-wrap h1{font-size:34px;line-height:1.15;margin:10px 0 10px}
    .academy-wrap p{max-width:80ch}
    .kicker{opacity:.9}
    .meta{opacity:.7;font-size:14px;margin:8px 0 22px}
    .card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:18px;margin:18px 0}
    .grid{display:grid;grid-template-columns:1fr;gap:14px}
    @media(min-width:900px){.grid{grid-template-columns:1fr 1fr}}
    ul.check{margin:0;padding-left:18px}
    ul.check li{margin:6px 0}
  </style>

</head>

<body>
  {% include "_nav.html" %}

  <main class="academy-wrap">
    <p class="kicker">Academy • Amazon FBA</p>
    <h1>Amazon FBA: Validate Rising Search Terms Before Ordering Inventory</h1>
    <p class="meta">Updated: 2025-11-30 • Read time: ~10 minutes</p>

    <div class="card">
      <h2>Why FBA sellers must validate trends differently</h2>
      <p>
        Shopify dropshippers can test a product today and kill it tomorrow—no real risk.
        Amazon FBA is the opposite: you invest thousands into inventory, shipping, and prep.
        That’s why rising search terms must be validated through a
        <strong>risk-proof layer</strong> before placing an order.
      </p>
      <p>
        This guide shows you how to take a rising search term and decide:
      </p>
      <ul class="check">
        <li>Is this a real opportunity?</li>
        <li>Is it just a seasonal bump?</li>
        <li>Are competitors too strong?</li>
        <li>Is margin achievable?</li>
        <li>Can I differentiate enough to survive?</li>
      </ul>
    </div>

    <h2>Step 1 — Confirm the trend is real (not a fake spike)</h2>
    <div class="card">
      <p>
        Rising terms can be misleading. For FBA you must confirm:
      </p>
      <ul class="check">
        <li><strong>Consistent multi-week improvement</strong> (not 1 week jump)</li>
        <li><strong>Healthy end rank</strong> (below ~150k is where money starts)</li>
        <li><strong>Not extremely seasonal</strong> unless planned</li>
      </ul>
      <p>
        A term that went <em>900k → 120k</em> over 6–10 weeks is a real signal.  
        A term that went <em>900k → 200k</em> in 1 week is a fake spike.
      </p>
    </div>

    <h2>Step 2 — Check competitive pressure on Amazon</h2>
    <div class="grid">
      <div class="card">
        <h3>Good signs</h3>
        <ul class="check">
          <li>Top sellers have weak images</li>
          <li>Poor bullets / weak SEO</li>
          <li>Review counts under 300 in top 10 listings</li>
          <li>Inconsistent branding (easy to out-brand)</li>
        </ul>
      </div>
      <div class="card">
        <h3>Bad signs</h3>
        <ul class="check">
          <li>All top 10 listings are saturated & branded</li>
          <li>Thousands of reviews</li>
          <li>All same supplier / same product (commodity trap)</li>
          <li>Low margins even at high volume</li>
        </ul>
      </div>
    </div>

    <h2>Step 3 — Price × COGS × Margin reality check</h2>
    <div class="card">
      <p>
        A rising term does not equal a profitable product.  
        You must confirm:
      </p>
      <ul class="check">
        <li>Target Amazon price (top 20 ASINs)</li>
        <li>Your landed cost (manufacturer → prep → FBA fees)</li>
        <li>Expected PPC cost (based on CPC in category)</li>
      </ul>

      <p>
        If margin after PPC is below <strong>20–25%</strong>, it’s not worth launching.
      </p>
    </div>

    <h2>Step 4 — Identify differentiation opportunities</h2>
    <div class="card">
      <p>
        For FBA, differentiation is mandatory. Look for:
      </p>
      <ul class="check">
        <li>Bundling ideas (most competitors sell standalone)</li>
        <li>Material upgrade (bamboo → steel, plastic → silicone)</li>
        <li>Feature variation (size, color, form)</li>
        <li>USP supported by rising terms (e.g., “gift”, “funny”, “aesthetic”)</li>
      </ul>
      <p>
        A rising term often contains the clue for differentiation — for example:
      </p>
      <ul class="check">
        <li><em>“aesthetic desk organizer”</em> → design-focused version</li>
        <li><em>“grandma gift”</em> → emotional packaging + message card</li>
      </ul>
    </div>

    <h2>Step 5 — Validate demand via related terms (clusters)</h2>
    <div class="card">
      <p>
        For Amazon FBA, you want **clusters**, not isolated winners.
        Check if related terms also show improvement:
      </p>
      <ul class="check">
        <li>variations (size / material)</li>
        <li>recipient versions (mom / dad / grandma)</li>
        <li>style variations (cute / minimalist / funny)</li>
      </ul>
      <p>
        If multiple related terms are rising → much stronger signal.
      </p>
    </div>

    <h2>Step 6 — Avoid the 3 deadly traps</h2>
    <div class="card">
      <ul class="check">
        <li><strong>Seasonality trap:</strong> looks like a trend but it's just holiday/season spike.</li>
        <li><strong>Commodity trap:</strong> everyone sells the same item from same factory.</li>
        <li><strong>Margin trap:</strong> PPC eats all profit even with demand.</li>
      </ul>
      <p>
        Your job is not just finding rising terms — it's avoiding these traps.
      </p>
    </div>

    <h2>Step 7 — Final validation checklist before ordering</h2>
    <div class="card">
      <ul class="check">
        <li>Trend consistent across multiple weeks</li>
        <li>End rank strong enough (ideally below 150k)</li>
        <li>Competition beatable (weak listings)</li>
        <li>COGS & margin solid even after PPC</li>
        <li>Clear differentiation angle exists</li>
        <li>Cluster support from related terms</li>
      </ul>
      <p>
        If all checks are green → safe to start sampling and ordering inventory.
      </p>
    </div>

    <p class="meta">
      Back to: <a href="/academy">Academy</a> · Related:
      <a href="/academy/shopify-dropshipping">Shopify dropshipping</a> ·
      <a href="/academy/build-product-ideas">Build product ideas</a>
    </p>
  </main>

  <footer class="footer" style="text-align:center; padding:30px 0; border-top:1px solid #1e293b;">
    <p>© 2025 Uptrend Hunter by Erkan Ecom LLC. All rights reserved.</p>
    <div class="links" style="margin-top:10px;">
      <a href="/" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Home</a> |
      <a href="/terms" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Terms</a> |
      <a href="/privacy" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Privacy</a> |
      <a href="/refund" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Refund</a> |
      <a href="mailto:support@uptrendhunter.com" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Contact</a>
    </div>
  </footer>

</body>
</html>

```

### app\web\templates\academy_how_to_use.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>

  <title>How to Use Uptrend Hunter AI (5-minute walkthrough)</title>
  <link rel="canonical" href="https://www.uptrendhunter.com/academy/how-to-use"/>

  <meta name="description" content="A practical 5-minute guide to using Uptrend Hunter AI: pick weeks, use include/exclude filters, interpret results, and turn rising terms into PPC + product actions."/>
  <meta name="robots" content="index,follow"/>

  <!-- Open Graph -->
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="Uptrend Hunter AI"/>
  <meta property="og:url" content="https://www.uptrendhunter.com/academy/how-to-use"/>
  <meta property="og:title" content="How to Use Uptrend Hunter AI (5-minute walkthrough)"/>
  <meta property="og:description" content="Pick weeks, filter terms, read improvements, and turn rising queries into PPC + product decisions."/>

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary"/>
  <meta name="twitter:title" content="How to Use Uptrend Hunter AI (5-minute walkthrough)"/>
  <meta name="twitter:description" content="Pick weeks, filter terms, read improvements, and turn rising queries into PPC + product decisions."/>

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <!-- JSON-LD: Article -->
  <script type="application/ld+json">
  {
    "@context":"https://schema.org",
    "@type":"Article",
    "headline":"How to Use Uptrend Hunter AI (5-minute walkthrough)",
    "description":"A practical 5-minute guide to using Uptrend Hunter AI: pick weeks, use include/exclude filters, interpret results, and turn rising terms into PPC + product actions.",
    "author":{"@type":"Organization","name":"Uptrend Hunter AI"},
    "publisher":{"@type":"Organization","name":"Uptrend Hunter AI"},
    "mainEntityOfPage":{"@type":"WebPage","@id":"https://www.uptrendhunter.com/academy/how-to-use"},
    "datePublished":"2025-11-29",
    "dateModified":"2025-11-29"
  }
  </script>

  <style>
    /* minimalist readable article styles (no new css file needed) */
    .academy-wrap{max-width:980px;margin:0 auto;padding:40px 8%}
    .academy-wrap h1{font-size:34px;line-height:1.15;margin:10px 0 10px}
    .academy-wrap p{max-width:80ch}
    .kicker{opacity:.9}
    .meta{opacity:.7;font-size:14px;margin:8px 0 22px}
    .card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:18px;margin:18px 0}
    .grid{display:grid;grid-template-columns:1fr;gap:14px}
    @media(min-width:900px){.grid{grid-template-columns:1fr 1fr}}
    code, pre{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.10);border-radius:12px}
    pre{padding:14px;overflow:auto}
    .btnrow{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 10px}
    .btnlite{display:inline-block;padding:10px 14px;border-radius:10px;border:1px solid rgba(255,255,255,.18);text-decoration:none}
    .btnsolid{display:inline-block;padding:10px 14px;border-radius:10px;background:#007aff;color:#fff;text-decoration:none;font-weight:700}
    .btnsolid:hover{opacity:.92}
    .btnlite:hover{background:rgba(255,255,255,.06)}
    .check{margin:0;padding-left:18px}
    .check li{margin:6px 0}
    .note{opacity:.85}
  </style>
</head>

<body>
  {% include "_nav.html" %}

  <main class="academy-wrap">
    <p class="kicker">Academy • Getting Started</p>
    <h1>How to Use Uptrend Hunter AI (5-minute walkthrough)</h1>
    <p class="meta">Updated: 2025-11-29 • Read time: ~5 minutes</p>

    <div class="btnrow">
      <a class="btnsolid" href="/app">Open Demo</a>
      <a class="btnlite" href="/checkout">Upgrade to Pro</a>
      <a class="btnlite" href="/dashboard">Dashboard</a>
    </div>

    <div class="card">
      <h2>What this tool actually does</h2>
      <p>
        Uptrend Hunter AI surfaces <strong>search terms improving in rank</strong> over a selected week range.
        Lower rank number = higher search popularity. So if a term goes from <em>500,000 → 80,000</em>,
        that’s a strong improvement.
      </p>
    </div>

    <h2>Step 1 — Pick the right week range</h2>
    <div class="grid">
      <div class="card">
        <h3>For fast-moving trends</h3>
        <ul class="check">
          <li>Use a shorter range (e.g., 4–8 weeks)</li>
          <li>Goal: catch early breakout terms</li>
        </ul>
      </div>
      <div class="card">
        <h3>For stable products / evergreen niches</h3>
        <ul class="check">
          <li>Use a longer range (e.g., 12–18+ weeks)</li>
          <li>Goal: confirm consistent momentum</li>
        </ul>
      </div>
    </div>

    <p class="note">
      Demo is limited (6 weeks + fewer rows). Pro gives full weeks and stronger filtering.
    </p>

    <h2>Step 2 — Use Include / Exclude like a sniper</h2>
    <div class="card">
      <h3>Include keywords (space-separated)</h3>
      <p>Use includes to lock into a niche. Examples:</p>
      <pre><code>cat toothbrush
teacher gift
stainless steel mug</code></pre>

      <h3>Exclude keywords</h3>
      <p>Use excludes to remove noise / irrelevant clusters:</p>
      <pre><code>iphone case charger
free printable
tutorial pattern</code></pre>
    </div>

    <h2>Step 3 — Click “Find uptrends” and interpret the table</h2>
    <div class="card">
      <p>Key columns:</p>
      <ul class="check">
        <li><strong>Start rank</strong> vs <strong>End rank</strong>: shows movement over time</li>
        <li><strong>Total improvement</strong>: (start − end). Bigger = stronger momentum</li>
        <li><strong>Weeks</strong>: how many data points exist in that range</li>
      </ul>

      <p><strong>Rule of thumb:</strong> prioritize terms that improve a lot AND end at a meaningful rank (not still 1,200,000).</p>
    </div>

    <h2>Step 4 — Open the chart (modal) and check shape</h2>
    <div class="card">
      <p>What you want:</p>
      <ul class="check">
        <li>downward trend in rank (rank numbers getting smaller)</li>
        <li>not just a single-week spike (fake hype)</li>
      </ul>
      <p>What you avoid:</p>
      <ul class="check">
        <li>one huge jump then flat / reversal</li>
        <li>noisy zig-zag with no direction</li>
      </ul>
    </div>

    <h2>Step 5 — Turn it into PPC + product actions</h2>
    <div class="grid">
      <div class="card">
        <h3>PPC actions (quick wins)</h3>
        <ul class="check">
          <li>Add term to phrase/exact campaigns</li>
          <li>Increase bids on rising terms (controlled)</li>
          <li>Lower bids / pause falling terms</li>
        </ul>
      </div>
      <div class="card">
        <h3>Product actions (bigger wins)</h3>
        <ul class="check">
          <li>Validate demand (category + competition + reviews)</li>
          <li>Check seasonality (is it holiday-only?)</li>
          <li>Build listing keywords early</li>
        </ul>
      </div>
    </div>

    <div class="card">
      <h2>Next: the weekly routine (20 minutes)</h2>
      <p>
        If you want this to produce money, do it weekly.
        I’ll write the “20-minute weekly PPC routine” article next and link it here.
      </p>
    </div>

    <p class="meta">
      Back to: <a href="/academy">Academy</a>
    </p>
  </main>
</body>
</html>

```

### app\web\templates\academy_include_exclude.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>

  <title>Include / Exclude Filters Playbook</title>
  <link rel="canonical" href="https://www.uptrendhunter.com/academy/include-exclude"/>

  <meta name="description" content="A practical playbook for using include and exclude filters to clean up marketplace search data and lock into profitable niches."/>
  <meta name="robots" content="index,follow"/>

  <!-- Open Graph -->
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="Uptrend Hunter AI"/>
  <meta property="og:url" content="https://www.uptrendhunter.com/academy/include-exclude"/>
  <meta property="og:title" content="Include / Exclude Filters Playbook"/>
  <meta property="og:description" content="Learn how to use include and exclude filters to focus on the right marketplace search terms and remove noise."/>

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary"/>
  <meta name="twitter:title" content="Include / Exclude Filters Playbook"/>
  <meta name="twitter:description" content="Learn how to use include and exclude filters to focus on the right marketplace search terms and remove noise."/>

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <style>
    .academy-wrap{max-width:980px;margin:0 auto;padding:40px 8%}
    .academy-wrap h1{font-size:34px;line-height:1.15;margin:10px 0 10px}
    .academy-wrap p{max-width:80ch}
    .kicker{opacity:.9}
    .meta{opacity:.7;font-size:14px;margin:8px 0 22px}
    .card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:18px;margin:18px 0}
    .grid{display:grid;grid-template-columns:1fr;gap:14px}
    @media(min-width:900px){.grid{grid-template-columns:1fr 1fr}}
    ul.check{margin:0;padding-left:18px}
    ul.check li{margin:6px 0}
    pre{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:12px;overflow:auto;font-size:13px}
    code{font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,"Liberation Mono","Courier New",monospace}
  </style>
</head>

<body>
  {% include "_nav.html" %}

  <main class="academy-wrap">
    <p class="kicker">Academy • Playbook</p>
    <h1>Include / Exclude Filters Playbook</h1>
    <p class="meta">Updated: 2025-11-30 • Read time: ~6 minutes</p>

    <div class="card">
      <h2>Why filters matter so much</h2>
      <p>
        The raw table can show thousands of marketplace search terms. If you don’t filter,
        you waste time scrolling and chasing noise.
      </p>
      <p>
        <strong>Include</strong> and <strong>Exclude</strong> filters are how you:
      </p>
      <ul class="check">
        <li>lock into a niche or product family,</li>
        <li>remove terms you would never bid on or build around,</li>
        <li>see the real opportunities without getting blinded by junk.</li>
      </ul>
    </div>

    <h2>How the filters work (simple mental model)</h2>
    <div class="card">
      <ul class="check">
        <li><strong>Include</strong> = “only show terms that contain these words”.</li>
        <li><strong>Exclude</strong> = “hide any term that contains these words”.</li>
        <li>Both accept <strong>space-separated words or short phrases</strong>.</li>
      </ul>
      <p>
        You don’t need to overfit. Start broad, then gradually tighten.
      </p>
    </div>

    <h2>Step 1 — Define your core niche with Include</h2>
    <div class="card">
      <p>
        Use Include to describe the type of products you actually care about.
      </p>
      <p>Examples:</p>
      <pre><code>cat toothbrush
wooden ornament
stainless steel mug
teacher gift
</code></pre>
      <ul class="check">
        <li>Use 1–3 words that describe the niche, not a full sentence.</li>
        <li>Think like a shopper: how would they phrase this?</li>
        <li>If you sell multiple product lines, run them one-by-one.</li>
      </ul>
    </div>

    <h2>Step 2 — Clean the junk with Exclude</h2>
    <div class="card">
      <p>
        Exclude is where you get rid of terms that are technically “related”
        but useless for you.
      </p>
      <p>Common patterns to exclude in marketplace search data:</p>
      <ul class="check">
        <li>tutorial / pattern / diy / how to / free / printable</li>
        <li>phone models you don’t sell for (iphone, samsung, etc.)</li>
        <li>sizes or materials you never stock</li>
        <li>“for kids” if you only sell adult, or the reverse</li>
      </ul>
      <p>Example exclude patterns:</p>
      <pre><code>free printable pattern diy
tutorial pdf
iphone case
</code></pre>
    </div>

    <h2>Step 3 — Combine filters into “recipes”</h2>
    <div class="grid">
      <div class="card">
        <h3>Gift-focused recipe</h3>
        <p><strong>Include:</strong></p>
        <pre><code>gift for mom grandma gift</code></pre>
        <p><strong>Exclude:</strong></p>
        <pre><code>card printable svg pattern</code></pre>
        <ul class="check">
          <li>Focus on physical items, not digital downloads.</li>
          <li>Cleaner view of real product demand.</li>
        </ul>
      </div>

      <div class="card">
        <h3>Accessories-only recipe</h3>
        <p><strong>Include:</strong></p>
        <pre><code>case cover holder stand</code></pre>
        <p><strong>Exclude:</strong></p>
        <pre><code>tutorial how to repair</code></pre>
        <ul class="check">
          <li>Lock into accessory-type terms.</li>
          <li>Drop repair / info-only queries.</li>
        </ul>
      </div>
    </div>

    <h2>Step 4 — Avoid these common mistakes</h2>
    <div class="card">
      <ul class="check">
        <li>
          <strong>Over-filtering with Include.</strong>
          If you add too many words, you can kill good long-tail terms.
          Start simple, then tighten if needed.
        </li>
        <li>
          <strong>Forgetting that filters are AND-based.</strong>
          If you write <code>cat dog</code> in Include, you’re asking for terms that contain
          <em>both</em>, not one or the other.
        </li>
        <li>
          <strong>Not refreshing recipes over time.</strong>
          As you learn your niche, update your Include/Exclude recipes to reflect reality.
        </li>
      </ul>
    </div>

    <h2>Step 5 — Work from broad to narrow</h2>
    <div class="card">
      <p>A good pattern for each session:</p>
      <ul class="check">
        <li>Run a broad Include + minimal Exclude to see the landscape.</li>
        <li>Note clusters that look interesting.</li>
        <li>Then create a tighter Include recipe for each cluster.</li>
      </ul>
      <p>
        This way you don’t miss opportunities, but you still end with a focused,
        high-quality shortlist.
      </p>
    </div>

    <h2>Step 6 — Save your best filter sets</h2>
    <div class="card">
      <p>
        Keep a simple doc or sheet where you store the Include/Exclude combos that
        “worked” for you:
      </p>
      <ul class="check">
        <li>Write the date, filter values, and what you found.</li>
        <li>Re-use these recipes in future weeks for faster scanning.</li>
        <li>Over time, this becomes your personal playbook for reading marketplace demand.</li>
      </ul>
    </div>

    <p class="meta">
      Back to: <a href="/academy">Academy</a> · Related:
      <a href="/academy/how-to-use">How to use Uptrend Hunter</a> ·
      <a href="/academy/weekly-routine">20-minute weekly routine</a>
    </p>
  </main>

  <footer class="footer" style="text-align:center; padding:30px 0; border-top:1px solid #1e293b;">
    <p>© 2025 Uptrend Hunter by Erkan Ecom LLC. All rights reserved.</p>
    <div class="links" style="margin-top:10px;">
      <a href="/" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Home</a> |
      <a href="/terms" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Terms</a> |
      <a href="/privacy" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Privacy</a> |
      <a href="/refund" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Refund</a> |
      <a href="mailto:support@uptrendhunter.com" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Contact</a>
    </div>
  </footer>
</body>
</html>

```

### app\web\templates\academy_index.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Academy — Uptrend Hunter AI</title>

  <link rel="canonical" href="https://www.uptrendhunter.com/academy">
  <meta name="description" content="Guides and playbooks to find rising marketplace search trends and turn them into faster product + PPC decisions.">
  <meta name="robots" content="index,follow">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Uptrend Hunter AI">
  <meta property="og:url" content="https://www.uptrendhunter.com/academy">
  <meta property="og:title" content="Uptrend Hunter Academy">
  <meta property="og:description" content="Guides and playbooks for marketplace trend + PPC decisions.">

  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="Uptrend Hunter Academy">
  <meta name="twitter:description" content="Guides and playbooks for marketplace trend + PPC decisions.">

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">
</head>

<body>
  {% include "_nav.html" %}

  <section style="max-width:980px;margin:0 auto;padding:56px 18px;">
    <h1 style="margin:0 0 10px 0;">Academy</h1>
    <p style="color:#93a4b8;max-width:720px;margin:0 0 24px 0;">
      Short, practical docs. No fluff. Use these to turn rising marketplace search terms into product + PPC moves.
    </p>

    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;">

      <!-- How to use -->
      <a href="/academy/how-to-use" style="display:block;border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;text-decoration:none;">
        <div style="opacity:.75;font-size:12px;">Getting Started</div>
        <div style="font-weight:700;margin-top:6px;color:#e5e7eb;">How to use Uptrend Hunter</div>
        <div style="color:#93a4b8;margin-top:6px;font-size:14px;">Step-by-step: ranges, filters, and interpreting results.</div>
      </a>

      <!-- Trend vs seasonality -->
      <a href="/academy/trend-vs-seasonality" style="display:block;border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;text-decoration:none;">
        <div style="opacity:.75;font-size:12px;">Concepts</div>
        <div style="font-weight:700;margin-top:6px;color:#e5e7eb;">Trend vs seasonality</div>
        <div style="color:#93a4b8;margin-top:6px;font-size:14px;">
          How to separate real upward trends from short seasonal spikes in search data.
        </div>
      </a>

      <!-- Build Product Ideas -->
      <a href="/academy/build-product-ideas" style="display:block;border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;text-decoration:none;">
        <div style="opacity:.75;font-size:12px;">Product Research</div>
        <div style="font-weight:700;margin-top:6px;color:#e5e7eb;">Build product ideas from rising terms</div>
        <div style="color:#93a4b8;margin-top:6px;font-size:14px;">
          Turn rising search signals into real product opportunities and early launch ideas.
        </div>
      </a>

      <!-- Shopify dropshipping -->
      <a href="/academy/shopify-dropshipping" style="display:block;border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;text-decoration:none;">
        <div style="opacity:.75;font-size:12px;">Shopify Dropshipping</div>
        <div style="font-weight:700;margin-top:6px;color:#e5e7eb;">
          Find Shopify dropshipping products from rising terms
        </div>
        <div style="color:#93a4b8;margin-top:6px;font-size:14px;">
          Use rising marketplace search signals to pick products you can launch and test with ads today.
        </div>
      </a>

           <!-- Shopify ad hooks & creatives -->
      <a href="/academy/shopify-creatives" style="display:block;border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;text-decoration:none;">
        <div style="opacity:.75;font-size:12px;">Shopify Dropshipping</div>
        <div style="font-weight:700;margin-top:6px;color:#e5e7eb;">
          Ad hooks & creatives from rising terms
        </div>
        <div style="color:#93a4b8;margin-top:6px;font-size:14px;">
          Turn marketplace search intent into scroll-stopping hooks and UGC-style creatives for your Shopify store.
        </div>
      </a>
 
      <!-- Amazon FBA: trend validation -->
      <a href="/academy/amazon-fba-validation" style="display:block;border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;text-decoration:none;">
        <div style="opacity:.75;font-size:12px;">Amazon FBA</div>
        <div style="font-weight:700;margin-top:6px;color:#e5e7eb;">
          Validate rising terms before ordering inventory
        </div>
        <div style="color:#93a4b8;margin-top:6px;font-size:14px;">
          Risk-proof validation system for FBA sellers using multi-week trend signals.
        </div>
      </a>

            <!-- Amazon FBA: seasonality vs real trend -->
      <a href="/academy/amazon-fba-seasonality" style="display:block;border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;text-decoration:none;">
        <div style="opacity:.75;font-size:12px;">Amazon FBA</div>
        <div style="font-weight:700;margin-top:6px;color:#e5e7eb;">
          Seasonality vs real trend (avoid dead stock)
        </div>
        <div style="color:#93a4b8;margin-top:6px;font-size:14px;">
          Learn how to read seasonal waves vs lasting trends so you don’t over-order on temporary spikes.
        </div>
      </a>

      

            <!-- PPC clean-up checklist -->
      <a href="/academy/ppc-cleanup" style="display:block;border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;text-decoration:none;">
        <div style="opacity:.75;font-size:12px;">PPC</div>
        <div style="font-weight:700;margin-top:6px;color:#e5e7eb;">PPC keyword clean-up checklist</div>
        <div style="color:#93a4b8;margin-top:6px;font-size:14px;">
          10-minute weekly routine to cut dead keywords, protect budget, and double down on real demand.
        </div>
      </a>


       <!-- Include / Exclude -->
      <a href="/academy/include-exclude" style="display:block;border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;text-decoration:none;">
        <div style="opacity:.75;font-size:12px;">Playbook</div>
        <div style="font-weight:700;margin-top:6px;color:#e5e7eb;">Include / Exclude filters</div>
        <div style="color:#93a4b8;margin-top:6px;font-size:14px;">
          Concrete recipes for using filters to clean up marketplace data and lock into niches.
        </div>
      </a>

      <!-- Weekly routine -->
      <a href="/academy/weekly-routine" style="display:block;border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;text-decoration:none;">
        <div style="opacity:.75;font-size:12px;">Playbook</div>
        <div style="font-weight:700;margin-top:6px;color:#e5e7eb;">20-minute weekly routine</div>
        <div style="color:#93a4b8;margin-top:6px;font-size:14px;">
          A simple weekly process to review trends and update PPC + product moves.
        </div>
      </a>
      
      <!-- Search Momentum -->
      <a href="/academy/search-momentum" style="display:block;border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;text-decoration:none;">
        <div style="opacity:.75;font-size:12px;">Concepts</div>
        <div style="font-weight:700;margin-top:6px;color:#e5e7eb;">What is search momentum?</div>
        <div style="color:#93a4b8;margin-top:6px;font-size:14px;">
          Learn how to read demand direction, not just static volume — and why that matters for timing.
        </div>
      </a>

      <!-- CEO brief -->
      <a href="/academy/ceo-brief" style="display:block;border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:16px;text-decoration:none;">
        <div style="opacity:.75;font-size:12px;">Executive</div>
        <div style="font-weight:700;margin-top:6px;color:#e5e7eb;">CEO Brief: trend data + PPC</div>
        <div style="color:#93a4b8;margin-top:6px;font-size:14px;">What changes when you use marketplace search data across product + ads.</div>
      </a>

    </div>
  </section>

  <footer class="footer" style="text-align:center; padding:30px 0; border-top:1px solid #1e293b;">
    <p>© 2025 Uptrend Hunter by Erkan Ecom LLC. All rights reserved.</p>
    <div class="links" style="margin-top:10px;">
      <a href="/" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Home</a> |
      <a href="/terms" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Terms</a> |
      <a href="/privacy" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Privacy</a> |
      <a href="/refund" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Refund</a> |
      <a href="mailto:support@uptrendhunter.com" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Contact</a>
    </div>
  </footer>
</body>
</html>

```

### app\web\templates\academy_ppc_cleanup.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>

  <title>PPC Keyword Clean-Up Checklist (10-minute routine)</title>
  <link rel="canonical" href="https://www.uptrendhunter.com/academy/ppc-cleanup"/>

  <meta name="description" content="A 10-minute weekly checklist to clean up PPC keywords using marketplace trend data: cut dead terms, protect budget, and double down on real demand."/>
  <meta name="robots" content="index,follow"/>

  <!-- Open Graph -->
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="Uptrend Hunter AI"/>
  <meta property="og:url" content="https://www.uptrendhunter.com/academy/ppc-cleanup"/>
  <meta property="og:title" content="PPC Keyword Clean-Up Checklist (10-minute routine)"/>
  <meta property="og:description" content="Use this 10-minute checklist to clean up PPC keywords using marketplace trend data and protect your ad budget."/>

  <!-- Twitter -->
  <meta name="twitter:card" content="summary"/>
  <meta name="twitter:title" content="PPC Keyword Clean-Up Checklist (10-minute routine)"/>
  <meta name="twitter:description" content="Use this 10-minute checklist to clean up PPC keywords using marketplace trend data and protect your ad budget."/>

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <style>
    .academy-wrap{max-width:980px;margin:0 auto;padding:40px 8%}
    .academy-wrap h1{font-size:34px;line-height:1.15;margin:10px 0 10px}
    .academy-wrap p{max-width:80ch}
    .kicker{opacity:.9}
    .meta{opacity:.7;font-size:14px;margin:8px 0 22px}
    .card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:18px;margin:18px 0}
    .grid{display:grid;grid-template-columns:1fr;gap:14px}
    @media(min-width:900px){.grid{grid-template-columns:1fr 1fr}}
    ul.check{margin:0;padding-left:18px}
    ul.check li{margin:6px 0}
  </style>
</head>

<body>
  {% include "_nav.html" %}

  <main class="academy-wrap">
    <p class="kicker">Academy • PPC</p>
    <h1>PPC Keyword Clean-Up Checklist (10-minute routine)</h1>
    <p class="meta">Updated: 2025-11-30 • Read time: ~7 minutes</p>

    <div class="card">
      <h2>Why you need a clean-up routine</h2>
      <p>
        Most ad accounts slowly fill up with dead or weak keywords that still burn money.
        A simple weekly clean-up protects budget and pushes more spend into terms where
        demand is actually rising.
      </p>
      <p>
        This checklist is a <strong>10-minute routine</strong> to run once per week using
        your performance data + marketplace trend signals.
      </p>
    </div>

    <h2>Step 1 — Pull your “watch list” of keywords</h2>
    <div class="card">
      <p>Before opening any tool, decide which keywords are worth reviewing:</p>
      <ul class="check">
        <li>keywords with spend but weak results,</li>
        <li>keywords you suspect are seasonal or fading,</li>
        <li>keywords where you’re unsure whether to keep pushing or cut.</li>
      </ul>
      <p>
        You don’t need the full account. A focused list of 20–50 keywords is enough
        for a weekly pass.
      </p>
    </div>

    <h2>Step 2 — Check trend direction for each keyword</h2>
    <div class="card">
      <p>
        For each keyword on your watch list, use your trend data to check whether
        the underlying search term is:
      </p>
      <ul class="check">
        <li><strong>Rising</strong> (rank improving across weeks),</li>
        <li><strong>Flat</strong> (no real change),</li>
        <li><strong>Falling</strong> (rank getting worse).</li>
      </ul>
      <p>
        The chart shape + total improvement tell you if the market itself is helping
        or fighting your ads.
      </p>
    </div>

    <h2>Step 3 — Apply the simple decision grid</h2>
    <div class="grid">
      <div class="card">
        <h3>Rising demand + decent performance</h3>
        <ul class="check">
          <li>Keep the keyword.</li>
          <li>Consider <strong>gradual bid increases</strong>.</li>
          <li>Test it in more focused ad groups if it’s currently buried.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Falling demand + weak performance</h3>
        <ul class="check">
          <li>Lower bids aggressively or pause.</li>
          <li>Cut it from “broad” campaigns first.</li>
          <li>Don’t let yesterday’s winners drain today’s budget.</li>
        </ul>
      </div>
    </div>

    <div class="grid">
      <div class="card">
        <h3>Rising demand + weak performance</h3>
        <ul class="check">
          <li>Keep the keyword, but treat it as a <strong>fix candidate</strong>.</li>
          <li>Check listing relevance (titles, bullets, images).</li>
          <li>Check match type and search term quality feeding into it.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Flat demand + decent performance</h3>
        <ul class="check">
          <li>Maintain or slowly trim bids.</li>
          <li>Only scale if the margin is very healthy.</li>
          <li>Prefer to push truly rising terms instead.</li>
        </ul>
      </div>
    </div>

    <h2>Step 4 — Clean obvious waste first</h2>
    <div class="card">
      <p>Go after the “easy wins” in every session:</p>
      <ul class="check">
        <li>keywords with clear falling trend and bad results,</li>
        <li>keywords tied to past seasonal waves that are now over,</li>
        <li>keywords with near-zero conversions over a reasonable spend threshold.</li>
      </ul>
      <p>
        Aggressively tightening these frees budget for your rising signals.
      </p>
    </div>

    <h2>Step 5 — Consolidate winning themes</h2>
    <div class="card">
      <p>
        Your rising keywords will often share themes: same recipient, style, or use case.
        Treat these as PPC “clusters”:
      </p>
      <ul class="check">
        <li>Group related keywords into tighter ad groups.</li>
        <li>Align ad copy and creative to that specific angle.</li>
        <li>Use trend strength as a guide for where to concentrate spend.</li>
      </ul>
    </div>

    <h2>Step 6 — Lock the routine into your week</h2>
    <div class="card">
      <p>
        The clean-up works because it’s <strong>repeated</strong>, not because it’s complex.
        Each week:
      </p>
      <ul class="check">
        <li>Pick your watch list (5–10 minutes from your ad platform).</li>
        <li>Check trend direction and apply the decision grid (10 minutes).</li>
        <li>Write down 2–3 changes you made and why.</li>
      </ul>
      <p>
        After a few weeks, you’ll see more budget flowing into keywords that
        the market actually cares about.
      </p>
    </div>

    <p class="meta">
      Back to: <a href="/academy">Academy</a> · Related:
      <a href="/academy/weekly-routine">20-minute weekly routine</a> ·
      <a href="/academy/build-product-ideas">Build product ideas from rising terms</a>
    </p>
  </main>

  <footer class="footer" style="text-align:center; padding:30px 0; border-top:1px solid #1e293b;">
    <p>© 2025 Uptrend Hunter by Erkan Ecom LLC. All rights reserved.</p>
    <div class="links" style="margin-top:10px;">
      <a href="/" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Home</a> |
      <a href="/terms" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Terms</a> |
      <a href="/privacy" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Privacy</a> |
      <a href="/refund" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Refund</a> |
      <a href="mailto:support@uptrendhunter.com" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Contact</a>
    </div>
  </footer>
</body>
</html>

```

### app\web\templates\academy_search_momentum.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>

  <title>What Is Search Momentum? (Marketplace search data)</title>
  <link rel="canonical" href="https://www.uptrendhunter.com/academy/search-momentum"/>

  <meta name="description" content="A clear explanation of search momentum in marketplace search data: what it means, why it matters, and how to use it for product and PPC decisions."/>
  <meta name="robots" content="index,follow"/>

  <!-- Open Graph -->
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="Uptrend Hunter AI"/>
  <meta property="og:url" content="https://www.uptrendhunter.com/academy/search-momentum"/>
  <meta property="og:title" content="What Is Search Momentum? (Marketplace search data)"/>
  <meta property="og:description" content="Understand search momentum in marketplace search data and how to use it for timing product and PPC moves."/>

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary"/>
  <meta name="twitter:title" content="What Is Search Momentum? (Marketplace search data)"/>
  <meta name="twitter:description" content="Understand search momentum in marketplace search data and how to use it for timing product and PPC moves."/>

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <style>
    .academy-wrap{max-width:980px;margin:0 auto;padding:40px 8%}
    .academy-wrap h1{font-size:34px;line-height:1.15;margin:10px 0 10px}
    .academy-wrap p{max-width:80ch}
    .kicker{opacity:.9}
    .meta{opacity:.7;font-size:14px;margin:8px 0 22px}
    .card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:18px;margin:18px 0}
    .grid{display:grid;grid-template-columns:1fr;gap:14px}
    @media(min-width:900px){.grid{grid-template-columns:1fr 1fr}}
    ul.check{margin:0;padding-left:18px}
    ul.check li{margin:6px 0}
  </style>
</head>

<body>
  {% include "_nav.html" %}

  <main class="academy-wrap">
    <p class="kicker">Academy • Concepts</p>
    <h1>What Is Search Momentum?</h1>
    <p class="meta">Updated: 2025-11-30 • Read time: ~4 minutes</p>

    <div class="card">
      <h2>Quick definition</h2>
      <p>
        <strong>Search momentum</strong> describes how quickly a search term is rising or falling in marketplace demand
        across time. It’s not just about how big the search volume is today – it’s about
        <strong>direction</strong> and <strong>speed</strong>.
      </p>
      <ul class="check">
        <li><strong>Positive momentum:</strong> demand is climbing week over week.</li>
        <li><strong>Flat momentum:</strong> demand is stable, no real movement.</li>
        <li><strong>Negative momentum:</strong> demand is clearly slowing down.</li>
      </ul>
    </div>

    <h2>Why marketplace sellers should care</h2>
    <div class="card">
      <p>
        Most people focus only on “big” terms by volume. The problem: big terms are often
        <strong>mature or saturated</strong>. Momentum adds timing to the picture.
      </p>
      <ul class="check">
        <li><strong>High volume + flat momentum</strong> → usually late and crowded.</li>
        <li><strong>Moderate volume + strong rising momentum</strong> → early-stage opportunity.</li>
      </ul>
      <p>
        That’s why momentum is so valuable: it helps you see the <strong>early part of the curve</strong>,
        not just the top.
      </p>
    </div>

    <h2>How Uptrend Hunter thinks about momentum</h2>
    <div class="card">
      <p>
        Uptrend Hunter analyzes multiple weeks of marketplace search data and looks at:
      </p>
      <ul class="check">
        <li>Week-over-week direction (is rank improving, flat, or slipping?)</li>
        <li>How big the improvement is over the full range</li>
        <li>Whether the move is consistent or just a one-week spike</li>
        <li>Acceleration or slowdown over time</li>
        <li>Seasonal patterns and recurring waves</li>
      </ul>
      <p>
        When those signals line up in a sustained uptrend, the term behaves like a
        <strong>strong momentum candidate</strong>. When they are mixed or weak, the momentum is low.
      </p>
    </div>

    <h2>How to use search momentum in practice</h2>
    <div class="grid">
      <div class="card">
        <h3>Product decisions</h3>
        <ul class="check">
          <li>Use rising momentum to validate new product ideas.</li>
          <li>Avoid ideas where momentum is flat or clearly negative.</li>
          <li>Check if the trend is seasonal or building into something longer-term.</li>
        </ul>
      </div>
      <div class="card">
        <h3>PPC decisions</h3>
        <ul class="check">
          <li>Increase bids on terms that show strong, consistent momentum.</li>
          <li>Reduce spend on terms that are clearly losing demand.</li>
          <li>Build ad groups around rising clusters instead of static “big” terms.</li>
        </ul>
      </div>
    </div>

    <div class="card">
      <h2>Reading momentum alongside rank</h2>
      <p>
        A term that improves from rank <strong>500,000 → 80,000</strong> over your selected range
        is more interesting than a term stuck around <strong>120,000 → 110,000</strong>.
      </p>
      <ul class="check">
        <li>Look for <strong>big total improvement</strong> (start rank − end rank).</li>
        <li>Check that the <strong>end rank</strong> lands in a meaningful zone (not still extremely deep).</li>
        <li>Open the chart to confirm it’s a trend, not just a noisy spike.</li>
      </ul>
      <p>
        Momentum + chart shape together tell you whether this is a real wave or just random noise.
      </p>
    </div>

    <div class="card">
      <h2>Connecting this with the rest of the tool</h2>
      <p>
        In practice, you’ll combine momentum with filters and charts:
      </p>
      <ul class="check">
        <li>Use <strong>Include</strong> to lock into a product family or niche.</li>
        <li>Use <strong>Exclude</strong> to remove irrelevant clusters.</li>
        <li>Use <strong>total improvement</strong> and <strong>end rank</strong> to shortlist candidates.</li>
        <li>Use the <strong>chart</strong> to decide if the move is clean enough to act on.</li>
      </ul>
      <p>
        Once you see momentum as “direction + speed of demand”, the whole table becomes easier to read.
      </p>
    </div>

    <p class="meta">
      Back to: <a href="/academy">Academy</a> · Next: <a href="/academy/how-to-use">How to use Uptrend Hunter</a>
    </p>
  </main>

  <footer class="footer" style="text-align:center; padding:30px 0; border-top:1px solid #1e293b;">
    <p>© 2025 Uptrend Hunter by Erkan Ecom LLC. All rights reserved.</p>
    <div class="links" style="margin-top:10px;">
      <a href="/" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Home</a> |
      <a href="/terms" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Terms</a> |
      <a href="/privacy" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Privacy</a> |
      <a href="/refund" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Refund</a> |
      <a href="mailto:support@uptrendhunter.com" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Contact</a>
    </div>
  </footer>
</body>
</html>

```

### app\web\templates\academy_shopify_creatives.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>

  <title>Ad Hooks & Creatives From Rising Terms (Shopify Dropshipping)</title>
  <link rel="canonical" href="https://www.uptrendhunter.com/academy/shopify-creatives"/>

  <meta name="description" content="A practical guide for Shopify dropshippers: turn rising search terms into ad hooks, angles, and UGC-style creatives that actually convert."/>
  <meta name="robots" content="index,follow"/>

  <!-- Open Graph -->
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="Uptrend Hunter AI"/>
  <meta property="og:url" content="https://www.uptrendhunter.com/academy/shopify-creatives"/>
  <meta property="og:title" content="Ad Hooks & Creatives From Rising Terms (Shopify Dropshipping)"/>
  <meta property="og:description" content="Learn how to transform rising marketplace search terms into strong ad hooks and UGC creatives for your Shopify dropshipping store."/>

  <!-- Twitter -->
  <meta name="twitter:card" content="summary"/>
  <meta name="twitter:title" content="Ad Hooks & Creatives From Rising Terms (Shopify Dropshipping)"/>
  <meta name="twitter:description" content="Learn how to transform rising marketplace search terms into strong ad hooks and UGC creatives for your Shopify dropshipping store."/>

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <style>
    .academy-wrap{max-width:980px;margin:0 auto;padding:40px 8%}
    .academy-wrap h1{font-size:34px;line-height:1.15;margin:10px 0 10px}
    .academy-wrap p{max-width:80ch}
    .kicker{opacity:.9}
    .meta{opacity:.7;font-size:14px;margin:8px 0 22px}
    .card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:18px;margin:18px 0}
    .grid{display:grid;grid-template-columns:1fr;gap:14px}
    @media(min-width:900px){.grid{grid-template-columns:1fr 1fr}}
    ul.check{margin:0;padding-left:18px}
    ul.check li{margin:6px 0}
    code{font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,"Liberation Mono","Courier New",monospace}
  </style>
</head>

<body>
  {% include "_nav.html" %}

  <main class="academy-wrap">
    <p class="kicker">Academy • Shopify Dropshipping</p>
    <h1>Ad Hooks & Creatives From Rising Terms (Shopify Dropshipping)</h1>
    <p class="meta">Updated: 2025-11-30 • Read time: ~8 minutes</p>

    <div class="card">
      <h2>Why creatives should start from search intent</h2>
      <p>
        Most dropshippers start with a random TikTok trend and try to force a product into it.
        A better way: let <strong>search intent</strong> tell you what problems people already
        care about, then build ads directly on top of that.
      </p>
      <p>
        Rising search terms show what people <em>type</em> when they are actively looking for
        something. Your job is to turn that into:
      </p>
      <ul class="check">
        <li>a clear hook in the first 1–3 seconds,</li>
        <li>a simple promise,</li>
        <li>a visual that proves the promise.</li>
      </ul>
    </div>

    <h2>Step 1 — Break the term into “hook pieces”</h2>
    <div class="card">
      <p>Take a rising term and split it into 3 parts:</p>
      <ul class="check">
        <li><strong>Who</strong> it’s for (recipient / audience),</li>
        <li><strong>What</strong> the item is (core product idea),</li>
        <li><strong>Why</strong> they want it (problem / desire / emotion).</li>
      </ul>
      <p>Example: <em>“car seat gap filler organizer”</em></p>
      <ul class="check">
        <li>Who → drivers, people who hate messy cars</li>
        <li>What → organizer that fills the gap</li>
        <li>Why → stops stuff falling, keeps car clean</li>
      </ul>
      <p>
        These 3 pieces will become your first line of text, voiceover, or on-screen caption.
      </p>
    </div>

    <h2>Step 2 — Turn the term into 3–5 raw hooks</h2>
    <div class="card">
      <p>Use the search term itself as seed and write hooks like:</p>
      <ul class="check">
        <li>“Tired of stuff falling between your car seats?”</li>
        <li>“This simple organizer fixes the most annoying car problem.”</li>
        <li>“If your car looks like this, you need this.”</li>
      </ul>
      <p>
        Keep hooks:
      </p>
      <ul class="check">
        <li><strong>conversational</strong> (like a friend, not a brand),</li>
        <li><strong>problem-first</strong> (start with pain, not product name),</li>
        <li><strong>short</strong> (you have 1–3 seconds max).</li>
      </ul>
    </div>

    <h2>Step 3 — Use modifiers to create angles</h2>
    <div class="grid">
      <div class="card">
        <h3>Recipient-driven angle</h3>
        <p>If the term has a recipient (mom, dad, grandma, teacher):</p>
        <ul class="check">
          <li>“Gift your grandma something she’ll actually use every day.”</li>
          <li>“Teachers secretly love this kind of gift.”</li>
        </ul>
      </div>
      <div class="card">
        <h3>Use-case-driven angle</h3>
        <p>If the term includes a context (car, office, kitchen):</p>
        <ul class="check">
          <li>“Every kitchen needs this 5-second fix.”</li>
          <li>“Your office desk will never look the same.”</li>
        </ul>
      </div>
    </div>

    <h2>Step 4 — Map term → creative structure</h2>
    <div class="card">
      <p>For each promising term, you can outline a basic UGC creative like this:</p>
      <ul class="check">
        <li><strong>0–3s:</strong> Hook based on pain or desire from the term.</li>
        <li><strong>3–8s:</strong> Show the product solving that exact situation.</li>
        <li><strong>8–15s:</strong> Quick proof (before/after, reactions, small demo).</li>
        <li><strong>End:</strong> Simple CTA (“Shop now”, “Get yours today”).</li>
      </ul>
      <p>
        Write this as a one-line script next to each rising term you care about.
      </p>
    </div>

    <h2>Step 5 — Build a “hook bank” from your top terms</h2>
    <div class="card">
      <p>Create a simple doc or sheet with columns like:</p>
      <ul class="check">
        <li><strong>Rising term</strong></li>
        <li><strong>Problem</strong> (1 short sentence)</li>
        <li><strong>Primary hook</strong></li>
        <li><strong>Alternative hooks (2–3)</strong></li>
        <li><strong>Visual idea</strong> (what we show in first 3 seconds)</li>
      </ul>
      <p>
        This becomes your personal hook bank. Whenever you find a new rising term,
        you immediately add 2–3 hook ideas instead of just bookmarking the product.
      </p>
    </div>

    <h2>Step 6 — Test hooks, not just products</h2>
    <div class="card">
      <p>
        For Shopify dropshipping, winning or losing often comes down to the angle,
        not the exact SKU. Use your rising terms to test:
      </p>
      <ul class="check">
        <li>different recipients (for mom vs for grandma),</li>
        <li>different pain points (messy vs time-saving vs aesthetic),</li>
        <li>different proof styles (before/after vs reaction vs POV).</li>
      </ul>
      <p>
        When a rising term works with one hook but not another, you learn which psychological
        angle actually moves that niche.
      </p>
    </div>

    <h2>Step 7 — Tie your creatives back into search demand</h2>
    <div class="card">
      <p>
        Once you see a hook + creative working, loop back to your trend data:
      </p>
      <ul class="check">
        <li>Is the core search term still improving or stable?</li>
        <li>Are related terms also rising (cluster effect)?</li>
        <li>Can you create more creatives for those related terms with the same angle?</li>
      </ul>
      <p>
        This is where creative testing stops being random and starts flowing directly
        from marketplace demand.
      </p>
    </div>

    <p class="meta">
      Back to: <a href="/academy">Academy</a> · Related:
      <a href="/academy/shopify-dropshipping">Shopify dropshipping from rising terms</a> ·
      <a href="/academy/build-product-ideas">Build product ideas from rising terms</a>
    </p>
  </main>

  <footer class="footer" style="text-align:center; padding:30px 0; border-top:1px solid #1e293b;">
    <p>© 2025 Uptrend Hunter by Erkan Ecom LLC. All rights reserved.</p>
    <div class="links" style="margin-top:10px;">
      <a href="/" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Home</a> |
      <a href="/terms" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Terms</a> |
      <a href="/privacy" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Privacy</a> |
      <a href="/refund" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Refund</a> |
      <a href="mailto:support@uptrendhunter.com" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Contact</a>
    </div>
  </footer>
</body>
</html>

```

### app\web\templates\academy_shopify_dropshipping.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>

  <title>Shopify Dropshipping: Using Rising Search Terms to Find Products You Can Launch Today</title>
  <link rel="canonical" href="https://www.uptrendhunter.com/academy/shopify-dropshipping"/>

  <meta name="description" content="A practical guide for Shopify dropshippers: use rising marketplace search terms to pick products you can test quickly with ads and landing pages."/>
  <meta name="robots" content="index,follow"/>

  <!-- Open Graph -->
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="Uptrend Hunter AI"/>
  <meta property="og:url" content="https://www.uptrendhunter.com/academy/shopify-dropshipping"/>
  <meta property="og:title" content="Shopify Dropshipping: Using Rising Search Terms to Find Products You Can Launch Today"/>
  <meta property="og:description" content="Learn how Shopify dropshippers can use rising search terms to quickly find and test new product ideas."/>

  <!-- Twitter -->
  <meta name="twitter:card" content="summary"/>
  <meta name="twitter:title" content="Shopify Dropshipping: Using Rising Search Terms to Find Products You Can Launch Today"/>
  <meta name="twitter:description" content="Learn how Shopify dropshippers can use rising search terms to quickly find and test new product ideas."/>

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <style>
    .academy-wrap{max-width:980px;margin:0 auto;padding:40px 8%}
    .academy-wrap h1{font-size:34px;line-height:1.15;margin:10px 0 10px}
    .academy-wrap p{max-width:80ch}
    .kicker{opacity:.9}
    .meta{opacity:.7;font-size:14px;margin:8px 0 22px}
    .card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:18px;margin:18px 0}
    .grid{display:grid;grid-template-columns:1fr;gap:14px}
    @media(min-width:900px){.grid{grid-template-columns:1fr 1fr}}
    ul.check{margin:0;padding-left:18px}
    ul.check li{margin:6px 0}
  </style>
</head>

<body>
  {% include "_nav.html" %}

  <main class="academy-wrap">
    <p class="kicker">Academy • Shopify Dropshipping</p>
    <h1>Shopify Dropshipping: Using Rising Search Terms to Find Products You Can Launch Today</h1>
    <p class="meta">Updated: 2025-11-30 • Read time: ~8 minutes</p>

    <div class="card">
      <h2>Why dropshippers should care about rising search terms</h2>
      <p>
        As a Shopify dropshipper, you don’t need factories, molds, or big inventory decisions.
        Your edge is <strong>speed</strong>: you can launch and test products as soon as you see demand forming.
      </p>
      <p>
        Rising search terms in marketplace data tell you where shoppers are moving <em>right now</em>.
        If you can connect that with a supplier and a clean landing page, you can test the idea days or weeks
        before slower sellers even notice it.
      </p>
    </div>

    <h2>Step 1 — Pick a niche and pull rising terms</h2>
    <div class="card">
      <p>Start with a clear niche you actually want to sell in. Examples:</p>
      <ul class="check">
        <li>pet accessories,</li>
        <li>home organization,</li>
        <li>giftable items (grandma, mom, teacher),</li>
        <li>fitness / recovery,</li>
        <li>kitchen tools.</li>
      </ul>
      <p>
        Use includes to lock into that niche (e.g. <em>“pet hair remover”</em>, <em>“desk organizer”</em>,
        <em>“grandma gift”</em>) and run a search for rising terms over the last few weeks.
      </p>
      <p>
        Your goal at this stage is not perfection — just a shortlist of 10–20 terms that clearly
        improved in rank.
      </p>
    </div>

    <h2>Step 2 — Look for “ad-friendly” products</h2>
    <div class="grid">
      <div class="card">
        <h3>Good for paid ads</h3>
        <ul class="check">
          <li>visually clear benefit (before/after is obvious),</li>
          <li>problem-solving or emotionally driven,</li>
          <li>easy to explain in 5–10 seconds of video,</li>
          <li>not purely generic commodity (difficult for ads).</li>
        </ul>
      </div>
      <div class="card">
        <h3>Hard for paid ads</h3>
        <ul class="check">
          <li>super generic items (plain spoons, basic towels),</li>
          <li>items with tiny price and no margin,</li>
          <li>high complexity, needs long education.</li>
        </ul>
      </div>
    </div>
    <p class="card">
      When you look at each rising term, ask: <strong>“Can I show this in a short UGC-style video and make someone feel ‘I need this’?”</strong>
      If yes, it’s a strong dropshipping candidate.
    </p>

    <h2>Step 3 — Use modifiers to build angles</h2>
    <div class="card">
      <p>
        Rising terms often contain modifiers that tell you which angle is working:
      </p>
      <ul class="check">
        <li><strong>Recipient:</strong> mom, dad, kids, grandma, teacher</li>
        <li><strong>Use case:</strong> car, kitchen, office, travel</li>
        <li><strong>Style:</strong> cute, minimalist, aesthetic, funny</li>
        <li><strong>Format:</strong> set, bundle, kit, starter pack</li>
      </ul>
      <p>
        For dropshipping, you are not just choosing a product — you are choosing a <strong>marketing angle</strong>.
        If you see multiple rising terms that share the same angle, that’s your hook for creatives and landing page copy.
      </p>
    </div>

    <h2>Step 4 — Cross-check with suppliers fast</h2>
    <div class="card">
      <p>
        Once you have 3–5 promising terms, move quickly to your suppliers (AliExpress, agent, or another source):
      </p>
      <ul class="check">
        <li>Search for the core idea (not the full long-tail phrase).</li>
        <li>Check if there’s a product that clearly matches the shopper intent.</li>
        <li>Filter for stable suppliers, reviews, and shipping times that won’t kill you.</li>
      </ul>
      <p>
        Your benchmark: you should be able to go from <em>“rising term” → “product link”</em> in under 10–15 minutes for each idea.
      </p>
    </div>

    <h2>Step 5 — Build a lightweight validation funnel</h2>
    <div class="card">
      <p>For each shortlisted product, you don’t need a full brand yet. Build a simple funnel:</p>
      <ul class="check">
        <li>one clean product page focused on the main benefit,</li>
        <li>1–3 creatives (UGC-style if possible),</li>
        <li>basic ad set targeting your core audience.</li>
      </ul>
      <p>
        The goal is to see <strong>signal</strong>: clicks, add-to-carts, first sales — not to fully optimize the account on day one.
      </p>
    </div>

    <h2>Step 6 — Combine performance data with trend data</h2>
    <div class="card">
      <p>
        After a few days of traffic, you’ll have two layers of information:
      </p>
      <ul class="check">
        <li><strong>Marketplace trend:</strong> is the search term still improving or at least holding?</li>
        <li><strong>Your ads:</strong> are people clicking and buying when you show this product?</li>
      </ul>
      <p>
        A strong dropshipping opportunity is usually:
      </p>
      <ul class="check">
        <li>built on a rising or stable term, <em>and</em></li>
        <li>showing early positive signs in your ad metrics.</li>
      </ul>
    </div>

    <h2>Step 7 — Decide: scale, iterate, or kill</h2>
    <div class="card">
      <ul class="check">
        <li>
          <strong>Scale:</strong> good metrics + rising/stable term.
          Increase budget slowly, test more creatives, and refine targeting.
        </li>
        <li>
          <strong>Iterate:</strong> mixed metrics + rising term.
          Keep the idea but try new angles (different recipient, bundle, or creative).
        </li>
        <li>
          <strong>Kill:</strong> bad metrics + flat/falling term.
          Don’t stay emotionally attached; move to the next rising signal.
        </li>
      </ul>
      <p>
        Dropshipping rewards speed and volume of tests — as long as your tests are based on real demand signals, not random guessing.
      </p>
    </div>

    <p class="meta">
      Back to: <a href="/academy">Academy</a> · Related:
      <a href="/academy/build-product-ideas">Build product ideas from rising terms</a> ·
      <a href="/academy/ppc-cleanup">PPC clean-up checklist</a>
    </p>
  </main>

  <footer class="footer" style="text-align:center; padding:30px 0; border-top:1px solid #1e293b;">
    <p>© 2025 Uptrend Hunter by Erkan Ecom LLC. All rights reserved.</p>
    <div class="links" style="margin-top:10px;">
      <a href="/" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Home</a> |
      <a href="/terms" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Terms</a> |
      <a href="/privacy" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Privacy</a> |
      <a href="/refund" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Refund</a> |
      <a href="mailto:support@uptrendhunter.com" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Contact</a>
    </div>
  </footer>
</body>
</html>

```

### app\web\templates\academy_trend_vs_seasonality.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>

  <title>Trend vs Seasonality — Don’t Get Tricked by Spikes</title>
  <link rel="canonical" href="https://www.uptrendhunter.com/academy/trend-vs-seasonality"/>

  <meta name="description" content="How to tell the difference between real upward trends and short seasonal spikes in marketplace search data, and why it matters for product and PPC decisions."/>
  <meta name="robots" content="index,follow"/>

  <!-- Open Graph -->
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="Uptrend Hunter AI"/>
  <meta property="og:url" content="https://www.uptrendhunter.com/academy/trend-vs-seasonality"/>
  <meta property="og:title" content="Trend vs Seasonality — Don’t Get Tricked by Spikes"/>
  <meta property="og:description" content="Learn how to separate real upward trends from short seasonal spikes in marketplace search data."/>


  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary"/>
  <meta name="twitter:title" content="Trend vs Seasonality — Don’t Get Tricked by Spikes"/>
  <meta name="twitter:description" content="Learn how to separate real upward trends from short seasonal spikes in marketplace search data."/>

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <style>
    .academy-wrap{max-width:980px;margin:0 auto;padding:40px 8%}
    .academy-wrap h1{font-size:34px;line-height:1.15;margin:10px 0 10px}
    .academy-wrap p{max-width:80ch}
    .kicker{opacity:.9}
    .meta{opacity:.7;font-size:14px;margin:8px 0 22px}
    .card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:18px;margin:18px 0}
    .grid{display:grid;grid-template-columns:1fr;gap:14px}
    @media(min-width:900px){.grid{grid-template-columns:1fr 1fr}}
    ul.check{margin:0;padding-left:18px}
    ul.check li{margin:6px 0}
  </style>
</head>

<body>
  {% include "_nav.html" %}

  <main class="academy-wrap">
    <p class="kicker">Academy • Concepts</p>
    <h1>Trend vs Seasonality — Don’t Get Tricked by Spikes</h1>
    <p class="meta">Updated: 2025-11-30 • Read time: ~5 minutes</p>

    <div class="card">
      <h2>Why this matters</h2>
      <p>
        Marketplace search data is full of “beautiful” spikes that can fool you into bad decisions.
        Some spikes are part of a real long-term trend. Others are just <strong>seasonal noise</strong>.
      </p>
      <p>
        If you confuse the two, you either:
      </p>
      <ul class="check">
        <li>launch a product too late into a seasonal wave, or</li>
        <li>ignore a real trend that is quietly compounding.</li>
      </ul>
    </div>

    <h2>What we mean by “trend”</h2>
    <div class="card">
      <p>
        A <strong>trend</strong> is a sustained move in one direction across time.
        In search data, that usually means:
      </p>
      <ul class="check">
        <li>rank is improving (numbers going down) across many weeks, not just one;</li>
        <li>there is a clear slope in the chart, even if there is noise;</li>
        <li>the pattern doesn’t instantly reset to the old baseline.</li>
      </ul>
      <p>
        Trends often come from real changes in behaviour: new use cases, new styles,
        new gifting patterns, new problems to solve.
      </p>
    </div>

    <h2>What we mean by “seasonality”</h2>
    <div class="card">
      <p>
        <strong>Seasonality</strong> is a pattern that repeats in a predictable window:
        holidays, back-to-school, wedding season, tax time, etc.
      </p>
      <ul class="check">
        <li>Searches jump up, then fall back to the old baseline.</li>
        <li>The spike usually lines up with a known calendar event.</li>
        <li>Next year, the pattern often repeats in a similar week range.</li>
      </ul>
      <p>
        Seasonality is not “bad” — you just need to treat it differently in product and PPC decisions.
      </p>
    </div>

    <h2>How to tell them apart in charts</h2>
    <div class="grid">
      <div class="card">
        <h3>Signs of a real trend</h3>
        <ul class="check">
          <li>Multiple consecutive improvements in rank, with only small pullbacks.</li>
          <li>Higher lows: even when it dips, it doesn’t fully reset.</li>
          <li>No hard “cut” right after a fixed calendar date.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Signs of pure seasonality</h3>
        <ul class="check">
          <li>One tall spike, then a fast return to the old level.</li>
          <li>Movement tightly clustered around known dates (e.g. end-of-year).</li>
          <li>Very little build-up before the peak and no follow-through after.</li>
        </ul>
      </div>
    </div>

    <h2>How Uptrend Hunter fits into this</h2>
    <div class="card">
      <p>
        Uptrend Hunter surfaces terms with improving rank over a chosen week range.
        How you read that depends on <strong>where you are in the calendar</strong>.
      </p>
      <ul class="check">
        <li>During heavy seasonal periods, expect more sharp spikes.</li>
        <li>Outside those periods, strong moves are more likely to be real structural shifts.</li>
        <li>For ambiguous cases, compare different week ranges (short vs long).</li>
      </ul>
      <p>
        The tool shows you the movement; it’s your job to decide if it’s a wave or a one-off splash.
      </p>
    </div>

    <h2>Practical rules for product decisions</h2>
    <div class="card">
      <ul class="check">
        <li>
          Don’t launch a new product purely because of a <strong>single seasonal spike</strong>,
          especially if you are already mid-season.
        </li>
        <li>
          For seasonal ideas, plan ahead: use this year’s pattern to plan next year’s inventory and
          positioning, not a last-minute scramble.
        </li>
        <li>
          For non-seasonal categories, give more weight to trends that stay strong
          across both “busy” and “quiet” months.
        </li>
      </ul>
    </div>

    <h2>Practical rules for PPC decisions</h2>
    <div class="grid">
      <div class="card">
        <h3>During seasonal waves</h3>
        <ul class="check">
          <li>Be willing to scale rising seasonal terms — but with an exit date in mind.</li>
          <li>Track performance weekly; expect the wave to break quickly after the event.</li>
          <li>Don’t treat seasonal performance as your new permanent baseline.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Outside seasonal windows</h3>
        <ul class="check">
          <li>Give more budget to terms with clean, sustained momentum.</li>
          <li>Use trend strength to decide where to consolidate campaigns.</li>
          <li>Cut or down-bid terms that clearly rolled over after their peak.</li>
        </ul>
      </div>
    </div>

    <div class="card">
      <h2>Simple checklist for each rising term</h2>
      <ul class="check">
        <li>Is this move tied to a clear calendar event?</li>
        <li>If I zoom out, does the chart show a new level or does it snap back?</li>
        <li>Would this opportunity still make sense outside the peak weeks?</li>
      </ul>
      <p>
        If the answer is “only makes sense for a short calendar window”, treat it as a seasonal play.
        If the answer is “yes, this persists”, you are likely looking at a real trend.
      </p>
    </div>

    <p class="meta">
      Back to: <a href="/academy">Academy</a> · Related:
      <a href="/academy/search-momentum">What is search momentum?</a> ·
      <a href="/academy/weekly-routine">20-minute weekly routine</a>
    </p>
  </main>

  <footer class="footer" style="text-align:center; padding:30px 0; border-top:1px solid #1e293b;">
    <p>© 2025 Uptrend Hunter by Erkan Ecom LLC. All rights reserved.</p>
    <div class="links" style="margin-top:10px;">
      <a href="/" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Home</a> |
      <a href="/terms" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Terms</a> |
      <a href="/privacy" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Privacy</a> |
      <a href="/refund" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Refund</a> |
      <a href="mailto:support@uptrendhunter.com" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Contact</a>
    </div>
  </footer>
</body>
</html>

```

### app\web\templates\academy_weekly_routine.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>

  <title>20-Minute Weekly Trend & PPC Routine</title>
  <link rel="canonical" href="https://www.uptrendhunter.com/academy/weekly-routine"/>

  <meta name="description" content="A simple 20-minute weekly routine to review marketplace search trends, shortlist rising terms, and turn them into PPC and product actions."/>
  <meta name="robots" content="index,follow"/>

  <!-- Open Graph -->
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="Uptrend Hunter AI"/>
  <meta property="og:url" content="https://www.uptrendhunter.com/academy/weekly-routine"/>
  <meta property="og:title" content="20-Minute Weekly Trend & PPC Routine"/>
  <meta property="og:description" content="Use this 20-minute routine to turn marketplace trend data into cleaner PPC and product decisions every week."/>

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary"/>
  <meta name="twitter:title" content="20-Minute Weekly Trend & PPC Routine"/>
  <meta name="twitter:description" content="Use this 20-minute routine to turn marketplace trend data into cleaner PPC and product decisions every week."/>

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <style>
    .academy-wrap{max-width:980px;margin:0 auto;padding:40px 8%}
    .academy-wrap h1{font-size:34px;line-height:1.15;margin:10px 0 10px}
    .academy-wrap p{max-width:80ch}
    .kicker{opacity:.9}
    .meta{opacity:.7;font-size:14px;margin:8px 0 22px}
    .card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:18px;margin:18px 0}
    .grid{display:grid;grid-template-columns:1fr;gap:14px}
    @media(min-width:900px){.grid{grid-template-columns:1fr 1fr}}
    ul.check{margin:0;padding-left:18px}
    ul.check li{margin:6px 0}
  </style>
</head>

<body>
  {% include "_nav.html" %}

  <main class="academy-wrap">
    <p class="kicker">Academy • Playbook</p>
    <h1>20-Minute Weekly Trend & PPC Routine</h1>
    <p class="meta">Updated: 2025-11-30 • Read time: ~5 minutes</p>

    <div class="card">
      <h2>Why this routine exists</h2>
      <p>
        Trend data only pays off if you touch it regularly. This is a simple
        <strong>once-per-week, 20-minute routine</strong> to turn marketplace search data
        into cleaner PPC and product decisions.
      </p>
      <p>
        You don’t need to overthink it. Same steps, every week.
      </p>
    </div>

    <h2>Step 1 — Pick your week range (1–2 minutes)</h2>
    <div class="card">
      <ul class="check">
        <li><strong>For fast moves:</strong> use a shorter window (4–8 weeks).</li>
        <li><strong>For stable / evergreen:</strong> use 12–18+ weeks.</li>
      </ul>
      <p>
        Keep this consistent for a few weeks so your eyes learn how the numbers behave.
      </p>
    </div>

    <h2>Step 2 — Lock into a niche with filters (3–4 minutes)</h2>
    <div class="card">
      <p>Use <strong>Include</strong> and <strong>Exclude</strong> like a sniper:</p>
      <ul class="check">
        <li>Include = the niche or product family you care about.</li>
        <li>Exclude = accessories, patterns, tutorial queries, irrelevant devices, etc.</li>
      </ul>
      <p>
        Goal here is simple: make the table show <strong>only the kind of terms you’d actually bid on
        or build around</strong>.
      </p>
    </div>

    <h2>Step 3 — Sort and shortlist (5–6 minutes)</h2>
    <div class="card">
      <p>After you click <strong>Find uptrends</strong>, focus on:</p>
      <ul class="check">
        <li><strong>Total improvement:</strong> bigger improvement = stronger momentum.</li>
        <li><strong>End rank:</strong> the term should end in a realistic zone, not buried extremely deep.</li>
        <li><strong>Weeks:</strong> more weeks = more reliable signal.</li>
      </ul>
      <p>
        Each week, pick a small shortlist, for example:
      </p>
      <ul class="check">
        <li>3–5 terms for PPC testing.</li>
        <li>2–3 terms that look like product or bundle opportunities.</li>
      </ul>
    </div>

    <h2>Step 4 — Open charts and check shape (3–4 minutes)</h2>
    <div class="card">
      <p>
        Click into the chart for your shortlisted terms and sanity-check the pattern.
      </p>
      <ul class="check">
        <li>You want rank numbers <strong>consistently going down</strong> over time (better rank).</li>
        <li>You want to avoid one-week spikes followed by a fast reversal.</li>
        <li>Small zig-zags are normal; the overall direction is what matters.</li>
      </ul>
      <p>
        If the chart looks like random noise, drop it from the shortlist.
      </p>
    </div>

    <h2>Step 5 — Turn it into PPC actions (5 minutes)</h2>
    <div class="grid">
      <div class="card">
        <h3>Add & adjust</h3>
        <ul class="check">
          <li>Add the strongest rising terms into phrase/exact ad groups.</li>
          <li>Give them a controlled but meaningful starting bid.</li>
          <li>Monitor them over the next 1–2 weeks, not 1–2 days.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Clean up</h3>
        <ul class="check">
          <li>Lower bids on terms that clearly lost momentum.</li>
          <li>Pause or negative-match terms that are burning spend with no signal.</li>
          <li>Focus budget where demand is actually moving up.</li>
        </ul>
      </div>
    </div>

    <h2>Step 6 — Capture product ideas (1–2 minutes)</h2>
    <div class="card">
      <p>
        Create a simple “idea list” where you store the most interesting rising terms
        that look like product or bundle candidates.
      </p>
      <ul class="check">
        <li>Write the term, a quick note, and date.</li>
        <li>Each month, review this list and run a deeper validation pass.</li>
      </ul>
      <p>
        The goal is not to launch something every week — it’s to keep
        <strong>a backlog of validated ideas</strong> based on real demand.
      </p>
    </div>

    <div class="card">
      <h2>What this looks like in real time</h2>
      <ul class="check">
        <li>2 minutes: choose range + filters.</li>
        <li>6–8 minutes: scan table, shortlist, open charts.</li>
        <li>8–10 minutes: adjust PPC and update your idea list.</li>
      </ul>
      <p>
        Done weekly, this builds a compounding edge: you always know which terms
        are moving up, which are fading, and where to direct money and time.
      </p>
    </div>

    <p class="meta">
      Back to: <a href="/academy">Academy</a> · Related: 
      <a href="/academy/search-momentum">What is search momentum?</a> ·
      <a href="/academy/how-to-use">How to use Uptrend Hunter</a>
    </p>
  </main>

  <footer class="footer" style="text-align:center; padding:30px 0; border-top:1px solid #1e293b;">
    <p>© 2025 Uptrend Hunter by Erkan Ecom LLC. All rights reserved.</p>
    <div class="links" style="margin-top:10px;">
      <a href="/" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Home</a> |
      <a href="/terms" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Terms</a> |
      <a href="/privacy" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Privacy</a> |
      <a href="/refund" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Refund</a> |
      <a href="mailto:support@uptrendhunter.com" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Contact</a>
    </div>
  </footer>
</body>
</html>

```

### app\web\templates\admin.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Admin — Uptrend Hunter</title>

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="stylesheet" href="/static/css/styles.css?v=app-final-7">
  <style>
    .admin-wrap{max-width:1100px;margin:96px auto 64px;padding:0 16px;}
    .kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px;}
    .kpi{background:#0b1220;border:1px solid #1f2937;border-radius:12px;padding:12px;}
    .kpi .label{font-size:12px;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;}
    .kpi .value{font-size:20px;font-weight:700;margin-top:4px;}
    .grid{display:grid;grid-template-columns:1.2fr .8fr;gap:12px;}
    .card{background:#0b1220;border:1px solid #1f2937;border-radius:12px;padding:0;overflow:hidden;}
    table{width:100%;border-collapse:collapse;}
    th,td{padding:10px 12px;border-bottom:1px solid #111827;font-size:14px;}
    th{background:#0f172a;text-align:left;color:#cbd5e1;font-weight:600;}
    tr:hover td{background:#0f172a;}
    .pill{padding:2px 8px;border-radius:999px;font-size:12px;border:1px solid #1f2937;}
    .pill.pro{color:#bbf7d0;background:rgba(21,128,61,0.25);border-color:rgba(74,222,128,0.6);}
    .pill.demo{color:#e2e8f0;background:#0f172a;}
    .pill.paid{color:#38bdf8;background:#0f172a;}
    @media(max-width:900px){
      .kpis{grid-template-columns:repeat(2,1fr);}
      .grid{grid-template-columns:1fr;}
    }
  </style>
</head>
<body>
  {% include "_nav.html" %}

  <main class="admin-wrap">
    <h1 style="margin:0 0 10px;font-size:22px;">Admin Dashboard</h1>

    <section class="kpis">
      <div class="kpi">
        <div class="label">Total users</div>
        <div class="value">{{ stats.total_users }}</div>
      </div>
      <div class="kpi">
        <div class="label">Pro users</div>
        <div class="value">{{ stats.pro_users }}</div>
      </div>
      <div class="kpi">
        <div class="label">Demo users</div>
        <div class="value">{{ stats.demo_users }}</div>
      </div>
      <div class="kpi">
        <div class="label">Paid total</div>
        <div class="value">{{ stats.paid_total }}</div>
      </div>
    </section>

    <section class="grid">
      <!-- USERS -->
      <div class="card">
        <div style="padding:10px 12px;font-weight:700;">Latest Signups</div>
        <table>
          <thead>
            <tr>
              <th>Email</th>
              <th>Plan</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {% for u in users %}
              <tr>
                <td>{{ u[0] }}</td>
                <td>
                  {% if u[1] == "pro" %}
                    <span class="pill pro">PRO</span>
                  {% else %}
                    <span class="pill demo">{{ (u[1] or "demo")|upper }}</span>
                  {% endif %}
                </td>
                <td>{{ u[2] }}</td>
              </tr>
            {% endfor %}
            {% if users|length == 0 %}
              <tr><td colspan="3" class="muted">No users found.</td></tr>
            {% endif %}
          </tbody>
        </table>
      </div>

      <!-- PAYMENTS -->
      <div class="card">
        <div style="padding:10px 12px;font-weight:700;">Latest Payments</div>
        <table>
          <thead>
            <tr>
              <th>Email</th>
              <th>Status</th>
              <th>Amount</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {% for p in payments %}
              <tr>
                <td>{{ p[0] }}</td>
                <td><span class="pill paid">{{ p[1] }}</span></td>
                <td>{{ p[2] }} {{ p[3] }}</td>
                <td>{{ p[4] }}</td>
              </tr>
            {% endfor %}
            {% if payments|length == 0 %}
              <tr><td colspan="4" class="muted">No payments table / no payments yet.</td></tr>
            {% endif %}
          </tbody>
        </table>
      </div>
    </section>
  </main>
</body>
</html>

```

### app\web\templates\checkout.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Checkout — Uptrend Hunter</title>
  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9C7CGEWT0X"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-9C7CGEWT0X');
  </script>
</head>

<body>
  {% include "_nav.html" %}

  <!-- nav'dan boşluk: yapışmasın -->
  <main class="container" style="max-width:720px;margin:96px auto 56px;">
    <section class="card" style="padding:28px 28px; text-align:center;">

      <h1 style="margin:0 0 6px;">{{ plan_name }}</h1>

      <!-- Normal fiyat bloğu (BF yok) -->
      <div style="margin:0 0 16px;">
        <div style="font-size:28px; font-weight:800; line-height:1.1;">
          $29.99
          <span style="font-size:16px; opacity:.7; margin-left:6px; font-weight:500;">
            / month
          </span>
        </div>
        <div class="muted" style="margin-top:4px; font-size:13px;">
          Recurring subscription. Cancel anytime from your billing portal.
        </div>
      </div>

      {% if user %}
        <p class="muted" style="margin:0 0 16px;">Signed in as <strong>{{ user.email }}</strong></p>
      {% else %}
        <p class="muted" style="margin:0 20px 18px;">
          To upgrade, please create an account or log in.
        </p>
        <div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap; margin-bottom:18px;">
          <a class="btn" href="{{ url_for('signup', next='/checkout') }}">Create account</a>
          <a class="btn outline" href="{{ url_for('login',  next='/checkout') }}">Log in</a>
        </div>
      {% endif %}

      <ul style="text-align:left; max-width:520px; margin:0 auto 16px; line-height:1.55;">
        {% for b in benefits %}<li>{{ b }}</li>{% endfor %}
      </ul>

      <!-- trust badges -->
      <div style="display:flex; gap:14px; justify-content:center; flex-wrap:wrap; margin:14px 0 24px;">

        <div style="
          display:flex; align-items:center; gap:6px;
          padding:7px 12px;
          background:rgba(255,255,255,0.04);
          border:1px solid rgba(255,255,255,0.10);
          border-radius:12px;
          font-size:13px;
          backdrop-filter:blur(6px);
        ">
          <span style="font-size:14px;">🔒</span>
          <span style="opacity:.9;">Secure checkout</span>
        </div>

        <div style="
          display:flex; align-items:center; gap:6px;
          padding:7px 12px;
          background:rgba(255,255,255,0.04);
          border:1px solid rgba(255,255,255,0.10);
          border-radius:12px;
          font-size:13px;
          backdrop-filter:blur(6px);
        ">
          <span style="font-size:14px;">↺</span>
          <span style="opacity:.9;">Cancel anytime</span>
        </div>

        <div style="
          display:flex; align-items:center; gap:6px;
          padding:7px 12px;
          background:rgba(255,255,255,0.04);
          border:1px solid rgba(255,255,255,0.10);
          border-radius:12px;
          font-size:13px;
          backdrop-filter:blur(6px);
        ">
          <span style="font-size:14px;">💸</span>
          <span style="opacity:.9;">30-day refund</span>
        </div>

      </div>

      <style>
        .checkout-pro-btn {
          background: linear-gradient(90deg, #0ea5e9, #38bdf8);
          padding: 14px 28px;
          color: #fff;
          font-size: 17px;
          font-weight: 600;
          border: none;
          border-radius: 10px;
          cursor: pointer;
          width: 100%;
          max-width: 320px;
          box-shadow: 0 0 14px rgba(14,165,233,0.35);
          transition: all 0.25s ease;
        }

        .checkout-pro-btn:hover {
          transform: translateY(-2px) scale(1.02);
          box-shadow: 0 0 22px rgba(14,165,233,0.6);
          background: linear-gradient(90deg, #38bdf8, #0ea5e9);
        }
      </style>

      <form method="post" action="/checkout/start" style="margin-top:16px;">
        <button class="checkout-pro-btn" type="submit">Proceed to secure payment</button>
      </form>

      {% if error %}
        <p style="color:#ff8383; margin-top:14px;">{{ error }}</p>
      {% endif %}

      <p class="muted" style="margin-top:10px;">You’ll be redirected to a secure Lemon Squeezy checkout.</p>

      <!-- MINI SOCIAL PROOF -->
      <div style="max-width:520px; margin:8px auto 14px; text-align:left;">
        <p style="margin:0 0 8px; font-weight:700;">Amazon sellers say…</p>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
          <blockquote style="margin:0; padding:10px 12px; background:rgba(255,255,255,.04); border-radius:12px; font-size:14px;">
            “Caught two winners early. Way faster than spreadsheets.”
            <div style="margin-top:6px; font-size:12px; opacity:.7;">— Alex, Amazon Seller</div>
          </blockquote>
          <blockquote style="margin:0; padding:10px 12px; background:rgba(255,255,255,.04); border-radius:12px; font-size:14px;">
            “I check trend momentum in minutes. Clean and simple.”
            <div style="margin-top:6px; font-size:12px; opacity:.7;">— Priya, FBA Operator</div>
          </blockquote>
        </div>
      </div>

      <!-- MINI FAQ -->
      <div style="max-width:520px; margin:10px auto 6px; text-align:left;">
        <p style="margin:0 0 8px; font-weight:700;">Quick FAQ</p>

        <details style="background:rgba(255,255,255,.03); padding:8px 10px; border-radius:10px; margin:6px 0;">
          <summary style="cursor:pointer; font-weight:600;">Is the data up to date?</summary>
          <p style="margin:6px 0 0; font-size:14px; opacity:.9;">
            Yes. The system analyzes recent weekly search-term data.
            We process <strong>marketplace-level search results</strong>, normalize ranking changes,
            and calculate momentum based on the latest uploaded reports.
          </p>
        </details>

        <details style="background:rgba(255,255,255,.03); padding:8px 10px; border-radius:10px; margin:6px 0;">
          <summary style="cursor:pointer; font-weight:600;">Can I cancel anytime?</summary>
          <p style="margin:6px 0 0; font-size:14px; opacity:.9;">Yes. Cancel in 1 click from your billing portal.</p>
        </details>

        <details style="background:rgba(255,255,255,.03); padding:8px 10px; border-radius:10px; margin:6px 0;">
          <summary style="cursor:pointer; font-weight:600;">Refund policy?</summary>
          <p style="margin:6px 0 0; font-size:14px; opacity:.9;">Full refund within 30 days if you're not happy.</p>
        </details>
      </div>

      {% if user %}
        {# extra user-only copy eklemek istersen buraya koyarsın #}
      {% endif %}

    </section>
  </main>
</body>
</html>

```

### app\web\templates\dashboard.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Dashboard — Uptrend Hunter</title>

  <!-- Mevcut stiller -->
  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="stylesheet" href="/static/css/styles.css?v=app-final-7">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">
  
  <style>
    /* Dashboard layout */
    .dash-page {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      background: radial-gradient(circle at top, #0f172a 0, #020617 45%, #020617 100%);
      color: #e5e7eb;
    }
    .dash-inner {
      flex: 1;
      max-width: 960px;
      margin: 0 auto;
      padding: 96px 16px 40px;
      display: flex;
      align-items: flex-start;
      justify-content: center;
    }
    .dash-card {
      width: 100%;
      max-width: 640px;
      background: radial-gradient(circle at top left, rgba(56,189,248,0.10), rgba(15,23,42,0.95));
      border-radius: 16px;
      padding: 28px 28px 24px;
      box-shadow: 0 18px 45px rgba(15,23,42,0.9);
      border: 1px solid rgba(148,163,184,0.25);
    }

    .dash-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }
    .dash-title {
      font-size: 1rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: #9ca3af;
    }
    .plan-pill {
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      border: 1px solid rgba(148,163,184,0.5);
    }
    .plan-pill.demo {
      color: #e5e7eb;
      background: rgba(15,23,42,0.8);
    }
    .plan-pill.pro {
      color: #bbf7d0;
      border-color: rgba(74,222,128,0.7);
      background: rgba(21,128,61,0.25);
    }

    .account-meta {
      font-size: 0.9rem;
      color: #cbd5f5;
      margin-bottom: 18px;
    }
    .account-meta div {
      margin-bottom: 2px;
    }

    .plan-box {
      background: rgba(15,23,42,0.9);
      border-radius: 14px;
      padding: 18px 18px 16px;
      border: 1px solid rgba(148,163,184,0.6);
      margin-bottom: 20px;
    }
    .plan-name {
      font-size: 1rem;
      font-weight: 600;
      color: #e5e7eb;
      margin-bottom: 4px;
    }
    .plan-sub {
      font-size: 0.85rem;
      color: #9ca3af;
      margin-bottom: 10px;
    }
    .plan-price {
      font-size: 0.95rem;
      color: #e5e7eb;
      margin-bottom: 10px;
    }
    .plan-benefits {
      list-style: none;
      padding: 0;
      margin: 0;
      font-size: 0.85rem;
      color: #d1d5db;
    }
    .plan-benefits li {
      display: flex;
      align-items: flex-start;
      gap: 6px;
      margin-bottom: 4px;
    }
    .plan-benefits li span {
      font-size: 1.1rem;
      line-height: 1.2;
      color: #22c55e;
    }

    .dash-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 12px;
    }
    .btn-primary-dash,
    .btn-secondary-dash {
      border-radius: 999px;
      padding: 9px 18px;
      font-size: 0.9rem;
      font-weight: 500;
      border: 1px solid transparent;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      white-space: nowrap;
    }
    .btn-primary-dash {
      background: linear-gradient(135deg, #0ea5e9, #22d3ee);
      color: #0b1220;
      box-shadow: 0 10px 25px rgba(56,189,248,0.45);
    }
    .btn-primary-dash:hover {
      filter: brightness(1.04);
    }
    .btn-secondary-dash {
      background: rgba(15,23,42,0.8);
      color: #e5e7eb;
      border-color: rgba(148,163,184,0.7);
    }
    .btn-secondary-dash:hover {
      background: rgba(15,23,42,0.95);
    }

    .dash-footnote {
      font-size: 0.75rem;
      color: #9ca3af;
    }

    .dash-help {
      margin-top: 14px;
      font-size: 0.8rem;
      color: #94a3b8;
    }
    .dash-help a {
      color: #38bdf8;
      text-decoration: none;
    }
    .dash-help a:hover {
      text-decoration: underline;
    }

    @media (max-width: 640px) {
      .dash-inner {
        padding-top: 80px;
      }
      .dash-card {
        padding: 20px 16px 18px;
      }
      .dash-actions {
        flex-direction: column;
        align-items: stretch;
      }
      .btn-primary-dash,
      .btn-secondary-dash {
        width: 100%;
        justify-content: center;
      }
    }
  </style>
  <!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9C7CGEWT0X"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-9C7CGEWT0X');
</script>
</head>

<body class="dash-page" data-mode="demo">

  {% include "_nav.html" %}

  <main class="dash-inner">
    <section class="dash-card">
      <header class="dash-card-header">
        <div class="dash-title">Account</div>
        {% if user and user.plan == "pro" %}
          <div class="plan-pill pro">PRO • Active</div>
        {% else %}
          <div class="plan-pill demo">DEMO</div>
        {% endif %}
      </header>

      <div class="account-meta">
        <div><strong>Email:</strong> {{ user.email if user else "—" }}</div>
        <div><strong>Plan:</strong> {{ user.plan|upper if user and user.plan else "DEMO" }}</div>
      </div>

      {% if user and user.plan == "pro" %}
        {# --------- PRO BLOĞU --------- #}
        <div class="plan-box">
          <div class="plan-name">You’re on Uptrend Hunter Pro</div>
          <div class="plan-sub">Full access is active. Happy hunting! 🚀</div>

          <ul class="plan-benefits">
            <li><span>•</span><div>Data window: 18+ weeks of search data</div></li>
            <li><span>•</span><div>Results per query: up to 250 terms</div></li>
            <li><span>•</span><div>Filters: include &amp; exclude keywords for precise hunting</div></li>
            <li><span>•</span><div>Priority updates &amp; support</div></li>
          </ul>
        </div>

       <div class="dash-actions">
  <a href="/pro" class="btn">Open Pro app</a>
  <a href="/app" class="btn ghost">Open Demo (sandbox)</a>

  {% if LEMON_PORTAL_URL %}
    <a
      href="{{ LEMON_PORTAL_URL }}"
      class="btn ghost"
      target="_blank"
      rel="noopener"
      style="margin-top:10px;"
    >
      Manage account &amp; billing
    </a>
    <p class="dash-note">
      Update card, view invoices, cancel anytime.
    </p>
  {% endif %}
</div>


        <div class="dash-help">
          Need help or have feedback? Reach out at
          <a href="mailto:support@uptrendhunter.com">support@uptrendhunter.com</a>.
        </div>

      {% else %}
        {# --------- DEMO BLOĞU --------- #}
        <div class="plan-box">
          <div class="plan-name">Uptrend Hunter Pro — {{ price_text }}</div>
          <div class="plan-sub">For serious Amazon sellers who want to catch uptrends early.</div>

          <ul class="plan-benefits">
            <li><span>✓</span><div>Full access to 18+ weeks of historical search data</div></li>
            <li><span>✓</span><div>Smart include / exclude keyword filters</div></li>
            <li><span>✓</span><div>Up to 250 results per query</div></li>
            <li><span>✓</span><div>Priority updates &amp; support</div></li>
          </ul>
        </div>

        <div class="dash-actions">
          <a href="/checkout" class="btn-primary-dash">
            Upgrade to Pro
          </a>
          <a href="/app" class="btn-secondary-dash">
            Open Demo App
          </a>
        </div>

        <div class="dash-footnote">
          Cancel anytime. Secure payment handled by Lemon Squeezy.
        </div>

        <div class="dash-help">
          Questions before upgrading? Contact
          <a href="mailto:support@uptrendhunter.com">support@uptrendhunter.com</a>.
        </div>
      {% endif %}
    </section>
  </main>
</body>
</html>

```

### app\web\templates\forgot.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Forgot password — Uptrend Hunter</title>
  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="stylesheet" href="/static/css/styles.css?v=app-final-7">
</head>
<body>
  {% include "_nav.html" %}

  <main style="
    min-height: calc(100vh - 64px);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
  ">
    <section style="
      width: 100%;
      max-width: 420px;
      padding: 32px 28px;
      border-radius: 18px;
      background: rgba(15,23,42,0.92);
      box-shadow: 0 24px 60px rgba(0,0,0,0.65);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(148,163,184,0.3);
      color: #e5e7eb;
    ">
      <h1 style="font-size: 26px; margin: 0 0 8px; font-weight: 600;">
        Reset your password
      </h1>
      <p style="margin: 0 0 20px; font-size: 14px; color:#cbd5f5;">
        Enter your email and we’ll send you a reset link.
      </p>

      {% if msg %}
        <div style="
          margin-bottom: 16px;
          padding: 10px 12px;
          border-radius: 8px;
          font-size: 13px;
          background: rgba(22,163,74,0.12);
          border: 1px solid rgba(22,163,74,0.5);
          color: #bbf7d0;
        ">
          {{ msg }}
        </div>
      {% endif %}

      <form method="post" style="display:flex;flex-direction:column;gap:12px;">
        <input
          type="email"
          name="email"
          placeholder="Your email"
          required
          style="
            padding: 10px 12px;
            border-radius: 10px;
            border: 1px solid rgba(148,163,184,0.6);
            background: rgba(15,23,42,0.9);
            color:#e5e7eb;
            font-size: 14px;
            outline: none;
          "
        />

        <button type="submit" style="
          margin-top: 4px;
          padding: 10px 14px;
          border-radius: 999px;
          border: none;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
        " class="btn-primary">
          Send reset link
        </button>
      </form>

      <p style="margin-top: 16px; font-size: 13px; color:#9ca3af;">
        Remembered your password?
        <a href="{{ url_for('login') }}" style="color:#93c5fd; text-decoration:none;">
          Go back to login
        </a>
      </p>
    </section>
  </main>
</body>
</html>

```

### app\web\templates\index.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Amazon Trend Finder AI — App</title>

  <!-- Ortak stiller -->
  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="stylesheet" href="/static/css/styles.css?v=app-final-7">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

<meta name="robots" content="noindex,nofollow">


  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9C7CGEWT0X"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-9C7CGEWT0X');
  </script>
</head>

<body data-mode="{{ mode or 'demo' }}">

  <!-- ===== PRELOADER (sadece kendi içinde animasyon, grafiklere sızmaz) ===== -->
  <div id="preloader" style="
    position:fixed; inset:0;
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    background:rgba(2,6,23,.94); backdrop-filter:blur(3px);
    z-index:10000; transition:opacity .6s ease; opacity:1;
  ">
    <div style="display:flex; gap:10px;">
      <div class="pre-dot"></div>
      <div class="pre-dot"></div>
      <div class="pre-dot"></div>
    </div>
    <p id="preloaderText" style="margin-top:14px; font-size:15px; color:#9ca3af;">
      {{ 'Loading Pro…' if (mode=='pro') else 'Loading Demo…' }}
    </p>
  </div>

  <style>
    #preloader .pre-dot{
      width:14px; height:14px; border-radius:50%;
      background-color:#38bdf8;
      animation: pre_pulse 1.2s ease-in-out infinite;
    }
    #preloader .pre-dot:nth-child(1){ animation-delay:0s; }
    #preloader .pre-dot:nth-child(2){ animation-delay:0.2s; }
    #preloader .pre-dot:nth-child(3){ animation-delay:0.4s; }

    @keyframes pre_pulse{
      0%,80%,100%{ transform:scale(0.6); opacity:0.5; }
      40%{ transform:scale(1); opacity:1; }
    }
  </style>

  <script>
    // preloader gizleme
    (function(){
      let done=false;
      window.preloaderHide=function(){
        if(done) return; done=true;
        const el=document.getElementById('preloader');
        if(!el) return;
        setTimeout(()=>{
          el.style.opacity='0';
          el.style.pointerEvents='none';
          setTimeout(()=>{ try{el.remove();}catch(e){el.style.display='none';} },600);
        },2500);
      };
      window.addEventListener('load', window.preloaderHide);
      setTimeout(()=>{ if(document.getElementById('preloader')) window.preloaderHide(); },6000);
    })();
  </script>
  <!-- ===== /PRELOADER ===== -->

  {% include "_nav.html" %}

  {% if mode == 'demo' %}
    <div class="upgrade-banner" role="status">
      You’re using the free demo. Last 6 weeks and 50 results only, advanced filters disabled.
      <a href="{{ url_for('checkout') }}" class="btn small">Upgrade to Pro</a>
    </div>
  {% endif %}

  <!-- Filtreler -->
  <section class="controls" aria-labelledby="filtersTitle">
    <h2 id="filtersTitle" class="hidden">Filters</h2>

    <div>
      <label for="start">Start week</label>
      <select id="start" name="start"></select>
    </div>

    <div>
      <label for="end">End week</label>
      <select id="end" name="end"></select>
    </div>

    <div>
      <label>Include keywords (space-separated)</label>
      <input id="include" placeholder="trump costume dog" ... >
    </div>

    <div>
      <label>Exclude keywords (space-separated)</label>
      <input id="exclude" placeholder="iphone case charger" ... >
    </div>

    <div class="actions">
      <button id="run" class="btn" aria-label="Find uptrends">Find uptrends</button>
    </div>
  </section>

  <!-- Özet -->
  <section class="summary" aria-live="polite">
    <span id="found" class="pill">Found: 0</span>
    <span id="range" class="pill"></span>

    <span id="status" class="loading hidden" aria-hidden="true">
      <span class="dot"></span><span class="dot"></span><span class="dot"></span> Loading…
    </span>
  </section>

  <!-- Sonuç Tablosu -->
  <section aria-labelledby="resultsTitle">
    <h2 id="resultsTitle" class="hidden">Results</h2>
    <table id="tbl">
      <thead>
        <tr>
          <th data-key="term">Term</th>
          <th data-key="start_rank">Start rank</th>
          <th data-key="end_rank">End rank</th>
          <th data-key="total_improvement">Total improvement</th>
          <th data-key="weeks">Weeks</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
    <div id="empty" class="hidden">No results. Try relaxing your filters.</div>
  </section>

  <!-- Modal (grafik) -->
  <div id="modal" class="modal hidden" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
    <div class="modal-card">
      <div class="modal-header">
        <h3 id="modalTitle">Trend</h3>
        <button id="closeModal" class="btn" aria-label="Close">✕</button>
      </div>
      <div id="chart" class="chart"></div>
    </div>
  </div>

  <!-- Toast -->
  <div id="toast" class="toast hidden" role="status" aria-live="polite"></div>

  <!-- App JS -->
  <script src="/static/js/app.js" defer></script>
</body>
</html>

```

### app\web\templates\landing.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Uptrend Hunter AI — Find rising Amazon search trends</title>

  <!-- SEO -->
  <link rel="canonical" href="https://www.uptrendhunter.com/">
  <meta name="description" content="Uptrend Hunter AI helps Amazon sellers spot rising search terms early — so you can launch faster and optimize PPC before competitors react.">
  <meta name="robots" content="index,follow">

  <!-- Open Graph (WhatsApp/LinkedIn/etc) -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Uptrend Hunter AI">
  <meta property="og:url" content="https://www.uptrendhunter.com/">
  <meta property="og:title" content="Uptrend Hunter AI — Spot rising Amazon search trends early">
  <meta property="og:description" content="Find rising search terms early and make faster product + PPC decisions.">

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="Uptrend Hunter AI — Spot rising Amazon search trends early">
  <meta name="twitter:description" content="Find rising search terms early and make faster product + PPC decisions.">

  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9C7CGEWT0X"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-9C7CGEWT0X');
  </script>

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Uptrend Hunter AI",
    "applicationCategory": "BusinessApplication",
    "operatingSystem": "Web",
    "url": "https://www.uptrendhunter.com/",
    "description": "Uptrend Hunter AI helps Amazon sellers spot rising search terms early so they can make faster product and PPC decisions.",
    "offers": {
      "@type": "Offer",
      "price": "29.99",
      "priceCurrency": "USD",
      "url": "https://www.uptrendhunter.com/checkout"
    }
  }
  </script>
</head>

<body>

  {% include "_nav.html" %}

  <!-- Hero -->
  <section class="hero">
    <div class="hero-content">
      <h1>Spot rising Amazon search trends — weeks before others notice.</h1>
      <p>
        AI-powered trend detector for Amazon sellers. Analyze <strong>18+ weeks</strong>
        of marketplace search momentum and reveal <strong>early uptrends</strong> in seconds —
        no setup, no spreadsheets.
      </p>

      <div class="cta-group">
        {% if current_user and current_user.plan == "pro" %}
          <a href="/pro" class="btn">Open Pro app</a>
          <a
            href="{{ LEMON_PORTAL_URL or '/dashboard' }}"
            class="btn ghost"
            target="_blank"
            rel="noopener"
          >
            Account &amp; billing
          </a>
        {% else %}
          <a href="/app" class="btn">Try Free Demo</a>
          <a href="/checkout" class="btn ghost">Upgrade to Pro</a>
        {% endif %}
      </div>

      <p class="hero-sub" style="margin-top:18px;">
        Powered by marketplace-level search term data and long-range keyword momentum analysis.
      </p>
    </div>

    <div class="hero-image">
      <img src="/static/img/app-screen.png" alt="Uptrend Hunter — Amazon trend dashboard" loading="lazy">
    </div>
  </section>

  <!-- Features -->
  <section id="features" class="features">
    <h2>Why Amazon sellers choose Uptrend Hunter</h2>
    <div class="grid">
      <div class="card">
        <h3>Early Trend Detection</h3>
        <p>Find terms with meaningful <strong>search rank improvement</strong> across your chosen weeks — quickly separate signal from noise.</p>
      </div>
      <div class="card">
        <h3>Smart Filters</h3>
        <p>Include or exclude keywords (e.g., “iphone”, exclude “case”) to focus on the segments that matter.</p>
      </div>
      <div class="card">
        <h3>18+ Weeks History</h3>
        <p>Look back more than a year to validate <strong>seasonality</strong> and <strong>sustained momentum</strong>, not just a single snapshot.</p>
      </div>
      <div class="card">
        <h3>Lightweight & Fast</h3>
        <p>Server-side optimized queries. No installs, no accounts required to test.</p>
      </div>
    </div>
  </section>

  <!-- Case Studies -->
  <section style="padding: 80px 0; background: #0C1220;">
    <div class="container" style="max-width: 1250px; margin: auto; padding: 0 24px;">

      <h2 style="font-size: 34px; font-weight: 700; margin-bottom: 50px;">
        Case Studies — <span style="color:#82C8F8;">Real sellers using trend momentum</span>
      </h2>

      <!-- CASE STUDY 1 -->
      <div style="
        display: flex;
        gap: 40px;
        margin-bottom: 90px;
        flex-wrap: wrap;
        align-items: flex-start;
      ">
        <div style="flex: 1 1 520px; text-align: center;">
          <img src="/static/img/case2.png"
               alt="Case Study 1"
               style="width: 100%; border-radius: 14px; cursor: zoom-in;"
               onclick="openZoom('/static/img/case2.png')">
          <p style="margin-top: 8px; opacity: 0.75;">Click to zoom</p>
        </div>

        <div style="flex: 1 1 520px;">
          <h3 style="font-size: 26px; margin-bottom: 10px;">Case Study #1 — Seasonal product timing</h3>

          <p style="opacity: 0.9; line-height: 1.55;">
            “Seasonal products were always a guessing game for me. I used to rely on last year’s patterns and gut feeling.
            Once I started tracking weekly search momentum, everything became clearer.”
          </p>

          <p style="opacity: 0.9; line-height: 1.55; margin-top: 12px;">
            “I noticed <strong>‘burgundy Christmas ornaments’</strong> climbing steadily weeks before the main peak.
            That signal helped me prioritize the right style early, list ahead of the crowd, and be fully stocked when demand exploded.”
          </p>

          <p style="margin-top:16px; font-weight:600;">
            — A.K. <span style="opacity:0.7;">(real user, seasonal & home category seller)</span>
          </p>
        </div>
      </div>

      <!-- CASE STUDY 2 -->
      <div style="
        display: flex;
        gap: 40px;
        flex-wrap: wrap;
        align-items: flex-start;
      ">
        <div style="flex: 1 1 520px; text-align: center;">
          <img src="/static/img/case1.png"
               alt="Case Study 2"
               style="width: 100%; border-radius: 14px; cursor: zoom-in;"
               onclick="openZoom('/static/img/case1.png')">
          <p style="margin-top: 8px; opacity: 0.75;">Click to zoom</p>
        </div>

        <div style="flex: 1 1 520px;">
          <h3 style="font-size: 26px; margin-bottom: 10px;">Case Study #2 — Smarter ad decisions</h3>

          <p style="opacity: 0.9; line-height: 1.55;">
            “My biggest problem with ads was wasting budget on the wrong keyword variations.
            It was hard to know which terms were actually gaining demand week by week.”
          </p>

          <p style="opacity: 0.9; line-height: 1.55; margin-top: 12px;">
            “By following the momentum table, I saw which <strong>‘trump mug’</strong> variations were rising fastest.
            I shifted spend toward the high-momentum terms and reduced budget on flat ones.
            That cut waste and boosted sales right when demand was accelerating.”
          </p>

          <p style="margin-top:16px; font-weight:600;">
            — M.Y. <span style="opacity:0.7;">(real user, gifts & mugs category seller)</span>
          </p>
        </div>
      </div>

    </div>
  </section>

  <!-- Modal for zoom -->
  <div id="zoomModal" style="
    display:none; position:fixed; inset:0; background:rgba(0,0,0,.7);
    backdrop-filter: blur(4px); z-index:9999; align-items:center; justify-content:center;">
    <img id="zoomImg" src="" style="max-width:90%; max-height:90%; border-radius:14px;">
  </div>

  <script>
    function openZoom(src) {
      document.getElementById('zoomImg').src = src;
      document.getElementById('zoomModal').style.display = 'flex';
    }
    document.getElementById('zoomModal').onclick = () =>
      document.getElementById('zoomModal').style.display = 'none';
  </script>

  <!-- Use Cases -->
  <section id="usecases" class="features" style="margin-top:60px;">
    <h2>What you can do with it</h2>
    <div class="grid">
      <div class="card">
        <h3>🎁 Seasonal wins</h3>
        <p>Catch gift trends before they peak; plan inventory and creatives.</p>
      </div>
      <div class="card">
        <h3>🔎 Idea validation</h3>
        <p>Confirm sustained momentum, not one-week spikes shows trends.</p>
      </div>
      <div class="card">
        <h3>💸 Smarter PPC</h3>
        <p>Allocate your Ads budget to queries that are gaining rank on keywords.</p>
      </div>
    </div>
  </section>

  <!-- Why it works: chart -->
  <div style="display:flex;justify-content:center;align-items:center;flex-direction:column;">
    <img src="/static/img/trend-graph.png"
         alt="Example of Uptrend Hunter chart showing keyword momentum"
         style="max-width:800px; width:100%; border-radius:12px; box-shadow:0 0 20px rgba(0,0,0,0.2);"
         loading="lazy">
    <p style="color:#9ca3af; font-size:14px; margin-top:12px;">
      Real app view — keyword momentum over 12 weeks. Only consistent upward trends are flagged.
    </p>
  </div>

  <!-- How it works -->
  <section id="how" class="how">
    <h2>How It Works</h2>
    <div class="steps">
      <div class="step">
        <img src="/static/img/sample1.png" alt="Pick weeks">
        <h3>1. Pick weeks</h3>
        <p>Pick start & end weeks (e.g., last 10–12) to measure momentum.</p>
      </div>
      <div class="step">
        <img src="/static/img/sample2.png" alt="Add filters">
        <h3>2. Add filters</h3>
        <p>Use Include/Exclude to focus on keyword families that matter.</p>
      </div>
      <div class="step">
        <img src="/static/img/sample3.png" alt="See uptrends">
        <h3>3. See uptrends</h3>
        <p>Sort by <strong>Total Improvement</strong> and open a term to view its weekly trajectory.</p>
      </div>
    </div>
  </section>

  <!-- Pricing -->
  <section id="pricing" class="pricing">
    <h2>Simple pricing</h2>
    <div class="plans">

      <div class="plan">
        <h3>Starter</h3>
        <p class="price">Free</p>
        <ul>
          <li>Up to 50 results per query</li>
          <li>6 week lookback</li>
          <li>Basic filters</li>
        </ul>
        <a href="/app" class="btn full" aria-label="Start free demo">Start Demo</a>
      </div>

      <div class="plan highlight">
        <h3>Pro</h3>
        <p class="price">
          $29.99 <span style="font-size:14px; opacity:0.7;">/ month</span>
        </p>
        <ul>
          <li>Full 18+ week history</li>
          <li>Advanced Include/Exclude</li>
          <li>Up to 250 results per query</li>
          <li>Priority updates & support</li>
        </ul>

        {% if current_user and current_user.plan == "pro" %}
          <a href="/pro" class="btn full" aria-label="Open Pro app">Open Pro</a>
          <p style="margin-top:8px; font-size:14px; color:#9ea8b7;">
            You already have Pro — thank you for supporting Uptrend Hunter.
          </p>
        {% else %}
          <a href="/checkout" class="btn full" aria-label="Upgrade to Pro">Start Pro</a>
          <p style="margin-top:8px; font-size:14px; color:#9ea8b7;">
            🔒Secure checkout · 30-day refund
          </p>
        {% endif %}
      </div>

    </div>
  </section>

  <!-- FAQ -->
  <section id="faq" class="faq">
    <h2>FAQ</h2>

    <details>
      <summary>How Uptrend Hunter works?</summary>
      <p>Uptrend Hunter analyzes weekly marketplace search behavior and builds a historical dataset.</p>
    </details>

    <details>
      <summary>How many weeks of data are included?</summary>
      <p>18+ weeks and growing, updated regularly.</p>
    </details>

    <details>
      <summary>Where does Uptrend Hunter’s data come from?</summary>
      <p>
        Uptrend Hunter uses an internally maintained marketplace search-term dataset
        built from tracking weekly search behavior over time. We store repeated
        queries, monitor ranking changes, and compute a momentum score to highlight
        genuine rising trends instead of random spikes. Everything is based on publicly
        observable marketplace search patterns.
      </p>
    </details>

    <details>
      <summary>Which browsers are supported?</summary>
      <p>Latest versions of Chrome, Edge, Safari, and Firefox.</p>
    </details>

    <details>
      <summary>Is there a refund policy?</summary>
      <p>Yes — cancel Pro anytime within 30 days for a full refund.</p>
    </details>

    <details>
      <summary>How fast does it process results?</summary>
      <p>Starter: up to 50 results per query. Pro: higher limits and faster queries.</p>
    </details>
  </section>

    <!-- Final CTA -->
  <section class="final-cta">
    <h2>Find your next winning product today</h2>
    <p>No signup required. Get started in seconds.</p>
    <a href="/app" class="btn">Try Free Demo</a>
  </section>

  <!-- Newsletter / weekly report -->
  <section class="newsletter" style="padding:60px 20px 40px; text-align:center;">
    <div class="container" style="max-width:720px; margin:0 auto;">
      <h2 style="font-size:26px; margin-bottom:10px;">
        Get Weekly Amazon Trend Reports — Free
      </h2>
      <p style="color:#9ca3af; font-size:15px; margin-bottom:22px;">
        Once a week we send a short, data-packed email with rising search terms,
        seasonal breakouts and early product ideas you can actually use.
      </p>

      <form class="email-box"
            method="POST"
            action="/subscribe"
            style="display:flex; gap:10px; justify-content:center; flex-wrap:wrap;">
        <input
          type="email"
          name="email"
          placeholder="Your email…"
          required
          style="padding:12px 14px; border-radius:8px; border:1px solid #1f2933;
                 background:#020617; color:#e5e7eb; min-width:240px; flex:1 1 260px;"
        >
        <button
          type="submit"
          class="btn"
          style="padding:12px 20px; border-radius:8px; font-weight:600;"
        >
          Get Weekly Report
        </button>
      </form>

      <p style="margin-top:10px; font-size:13px; color:#6b7280;">
        No spam. One actionable email per week. Unsubscribe anytime.
      </p>
    </div>
  </section>


  <!-- Built by sellers block -->
  <section class="builtby" style="text-align:center; padding:80px 20px;">
    <h2>Made by Amazon sellers, for Amazon sellers</h2>
    <p style="max-width:720px; margin:10px auto; color:#93a4b8; font-size:15px;">
      Uptrend Hunter is built by real FBA operators. Our mission: give every seller the same data edge big players use.
    </p>
    <div style="margin-top:18px;">
      <a href="/app" class="btn">Open live demo</a>
    </div>
  </section>

  <!-- Footer -->
  <footer class="footer" style="text-align:center; padding:30px 0; border-top:1px solid #1e293b;">
    <p>© 2025 Uptrend Hunter by Erkan Ecom LLC. All rights reserved.</p>
    <div class="links" style="margin-top:10px;">
      <a href="/terms" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Terms &amp; Conditions</a> |
      <a href="/privacy" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Privacy Policy</a> |
      <a href="/refund" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Refund Policy</a> |
      <a href="mailto:support@uptrendhunter.com" style="color:#9aa0a6; text-decoration:none; margin:0 10px;">Contact</a>
    </div>
    <div class="payment-note">🔒 Secure payments — by Lemon Squeezy</div>
  </footer>

  <!-- Trust bar -->
  <section class="trust-bar">
    <div class="trust-inner">
      <div class="trust-item">
        <img src="/static/img/trust/ssl-secure.svg" alt="SSL Secure">
        <span>SSL Secured</span>
      </div>
      <div class="trust-item">
        <img src="/static/img/trust/visa.svg" alt="Visa">
        <span>Visa</span>
      </div>
      <div class="trust-item">
        <img src="/static/img/trust/mastercard.svg" alt="Mastercard">
        <span>Mastercard</span>
      </div>
      <div class="trust-item">
        <img src="/static/img/trust/stripe.svg" alt="Stripe">
        <span>Stripe</span>
      </div>
      <div class="trust-item">
        <img src="/static/img/trust/shield.svg" alt="Data Protection">
        <span>Data Protection</span>
      </div>
    </div>
  </section>

  <!-- Lightbox -->
  <div id="lightbox" style="
    position:fixed; inset:0; background:rgba(0,0,0,0.85);
    display:none; align-items:center; justify-content:center;
    z-index:9999; padding:24px;">
    <img id="lightbox-img" src=""
         style="max-width:95%; max-height:95%; border-radius:14px; border:1px solid rgba(255,255,255,0.15);">
  </div>

  <script>
    function openLightbox(src){
      const lb = document.getElementById('lightbox');
      const img = document.getElementById('lightbox-img');
      img.src = src;
      lb.style.display = 'flex';
    }
    document.getElementById('lightbox').addEventListener('click', function(){
      this.style.display = 'none';
    });
  </script>

</body>
</html>

```

### app\web\templates\login.html

```html
<!doctype html><html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Log in — Amazon Trend Finder AI</title>
<link rel="stylesheet" href="/static/css/landing.css?v=1">

<link rel="stylesheet" href="/static/css/auth.css?v=1">
<link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9C7CGEWT0X"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-9C7CGEWT0X');
</script>
</head>

<body>
  <!-- <body> açıldıktan hemen sonra -->
<div class="top-right">
  <a href="{{ url_for('landing') }}">← Back to Home</a>
</div>
<style>
  .top-right { position:absolute; top:18px; right:18px; }
  .top-right a { padding:8px 12px; border-radius:8px; background:#0b5; color:#fff; text-decoration:none; font-weight:600; }
  .top-right a:hover { opacity:.9; }
</style>


<div class="auth">
  <h1>Welcome back</h1>

  {% if error %}
    <div class="err">{{ error }}</div>
  {% endif %}

  <form method="post">
    <label>Email</label>
    <input name="email" type="email" required autocomplete="email" />

    <label>Password</label>
    <input name="password" type="password" required />

    <button type="submit" class="btn-primary">Log in</button>

    <p class="auth-extra">
      <a href="{{ url_for('forgot') }}">Forgot your password?</a>
    </p>
  </form>

  <p class="muted">
    New here? <a href="/signup">Create an account</a>
  </p>
</div>

</body></html>

```

### app\web\templates\privacy.html

```html
<!doctype html><html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Privacy Policy — Uptrend Hunter AI</title>
<link rel="stylesheet" href="/static/css/landing.css?v=2">
<link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

</head><body>
  {% include "_nav.html" %}

<main class="page legal">
  <h1>Privacy Policy</h1>
  <p><em>Last updated: October 2025</em></p>

  <p>This Privacy Policy explains how Uptrend Hunter (“we,” “our,” “us”) collects, uses, and protects your information.</p>

  <h2>Information We Collect</h2>
  <ul>
    <li>Account data (name, email) you provide when signing up.</li>
    <li>Usage data (logs, device info) to maintain and improve the Service.</li>
    <li>Payment data collected and processed by our Payment Partners to complete transactions.</li>
  </ul>

  <h2>How We Use Information</h2>
  <ul>
    <li>To provide and maintain the Service.</li>
    <li>To communicate updates, billing, and support.</li>
    <li>To prevent abuse, secure accounts, and comply with legal obligations.</li>
  </ul>

  <h2>Data Sharing</h2>
  <p>We do not sell your personal data. We share only the minimum necessary information with service providers (e.g., hosting, analytics, Payment Partners) to operate the Service and fulfill purchases, subject to appropriate safeguards.</p>

  <h2>Data Protection</h2>
  <p>We apply reasonable technical and organizational measures to protect your data and comply with applicable data protection laws (e.g., GDPR where applicable).</p>

  <h2>Cookies</h2>
  <p>We use essential cookies to maintain sessions and improve functionality. You can disable cookies in your browser settings; some features may not function correctly.</p>

  <h2>Your Rights</h2>
  <p>Where applicable, you may request access, correction, deletion, or portability of your personal data. Contact us to exercise these rights.</p>

  <h2>Contact</h2>
  <p>Privacy questions? Email <a href="mailto:support@uptrendhunter.com">support@uptrendhunter.com</a>.</p>

  <p style="margin-top:20px"><a class="btn small" href="/">← Back to Home</a></p>
</main>
</body></html>

```

### app\web\templates\refund.html

```html
<!doctype html><html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Refund Policy (30-Day Money Back) — Uptrend Hunter AI</title>
<link rel="stylesheet" href="/static/css/landing.css?v=2">
<link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

</head><body>
  {% include "_nav.html" %}

<main class="page legal">
  <h1>Refund Policy (30-Day Money Back Guarantee)</h1>
  <p><em>Last updated: October 2025</em></p>

  <p>All purchases are processed securely by our authorized Payment Partners and/or an authorized reseller acting as Merchant of Record.</p>

  <h2>Refund Window</h2>
  <p>We offer a <strong>30-day refund window</strong> for new purchases. If you experience a technical issue that prevents normal use of the Service, contact us within 30 days of purchase.</p>

  <h2>How to Request a Refund</h2>
  <p>Email your request to <a href="mailto:support@uptrendhunter.com">support@uptrendhunter.com</a> (or <a href="mailto:support@uptrendhunter.com">support@uptrendhunter.com</a>) with your order reference and reason for the refund.</p>

  <h2>Exclusions</h2>
  <ul>
    <li>Refunds are not granted for repeated violations of our Terms or misuse of the Service.</li>
    <li>Where a Payment Partner or reseller’s policy imposes specific rules (e.g., tax handling, chargeback windows), those rules may apply.</li>
  </ul>

  <p style="margin-top:20px"><a class="btn small" href="/">← Back to Home</a></p>
</main>
</body></html>

```

### app\web\templates\reset.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Set new password — Uptrend Hunter</title>
  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="stylesheet" href="/static/css/styles.css?v=app-final-7">
</head>
<body>
  {% include "_nav.html" %}

  <main class="auth-main" style="max-width:480px;margin:40px auto;padding:24px;">
    <h1>Set a new password</h1>

    {% if error %}
      <div class="alert-error">{{ error }}</div>
    {% endif %}

    <form method="post" style="display:flex;flex-direction:column;gap:12px;margin-top:16px;">
      <input
        type="password"
        name="password"
        placeholder="New password"
        required
      />
      <input
        type="password"
        name="password2"
        placeholder="Repeat new password"
        required
      />
      <button type="submit">Update password</button>
    </form>
  </main>
</body>
</html>

```

### app\web\templates\reset_sent.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Email sent — Uptrend Hunter</title>
  <link rel="stylesheet" href="/static/css/landing.css?v=1">
  <link rel="stylesheet" href="/static/css/styles.css?v=app-final-7">
</head>
<body>
  {% include "_nav.html" %}

  <main style="
    min-height: calc(100vh - 64px);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
  ">
    <section style="
      width: 100%;
      max-width: 420px;
      padding: 32px 28px;
      border-radius: 18px;
      background: rgba(15,23,42,0.92);
      box-shadow: 0 24px 60px rgba(0,0,0,0.65);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(148,163,184,0.3);
      color: #e5e7eb;
      text-align: center;
    ">
      <h1 style="font-size: 26px; margin-bottom: 12px; font-weight: 600;">
        Check your email 📩
      </h1>

      <p style="font-size: 15px; color:#cbd5f5; line-height:1.6;">
        If your email address is registered, we’ve sent you a link<br>
        to reset your password.
      </p>

      <p style="margin-top: 20px; font-size: 13px; color:#9ca3af;">
        Didn’t receive anything?  
        <br>Check your spam folder or
        <a href="{{ url_for('forgot') }}" style="color:#93c5fd;">try again</a>.
      </p>

      <a href="{{ url_for('login') }}" style="
        display:inline-block;
        margin-top: 20px;
        padding: 10px 16px;
        border-radius: 999px;
        background:#3b82f6;
        color:white;
        text-decoration:none;
        font-size:14px;
      ">
        Return to login
      </a>
    </section>
  </main>
</body>
</html>

```

### app\web\templates\signup.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Create account — Uptrend Hunter AI</title>
  <link rel="stylesheet" href="/static/css/auth.css?v=2">
  <link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

  <style>
    /* sağ üst back link */
    .top-right { position: absolute; top: 18px; right: 18px; }
    .top-right a { padding: 8px 12px; border-radius: 8px; background:#0b5; color:#fff; text-decoration:none; font-weight:600; }
    .top-right a:hover { opacity:.9; }
  </style>
  <!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9C7CGEWT0X"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-9C7CGEWT0X');
</script>
</head>
<body class="auth-page">

  <!-- NAVBAR YOK; sadece back-to-home -->
  <div class="top-right">
    <a href="{{ url_for('landing') }}">← Back to Home</a>
  </div>

  <div class="auth">
    <h1>Create your account</h1>

    {% if error %}
      <div class="error">{{ error }}</div>
    {% endif %}

    <form method="post" id="signupForm" novalidate>
      <label>Email</label>
      <input type="email" name="email" required autocomplete="email"/>

      <label>Password</label>
      <input type="password" name="password" required minlength="6" autocomplete="new-password"/>

      <label>Confirm password</label>
      <input type="password" name="password2" required minlength="6" autocomplete="new-password"/>

      <button class="btn" type="submit">Create account</button>
    </form>

    <p class="muted">Already have an account? <a href="{{ url_for('login') }}">Log in</a></p>
  </div>

  <script>
    // Basit frontend doğrulama
    document.getElementById('signupForm').addEventListener('submit', function (e) {
      const p1 = this.password.value.trim();
      const p2 = this.password2.value.trim();
      if (p1.length < 6) {
        alert('Password must be at least 6 characters.');
        e.preventDefault(); return;
      }
      if (p1 !== p2) {
        alert('Passwords do not match.');
        e.preventDefault();
      }
    });
  </script>
</body>
</html>

```

### app\web\templates\terms.html

```html
<!doctype html><html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Terms & Conditions — Uptrend Hunter AI</title>
<link rel="stylesheet" href="/static/css/landing.css?v=2">
<link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">

</head><body>
  {% include "_nav.html" %}

<main class="page legal">
  <h1>Terms & Conditions</h1>
  <p><em>Last updated: October 2025</em></p>

  <p>These Terms of Service (“Terms”) govern your access to and use of Uptrend Hunter (the “Service”). “Company,” “we,” “us,” or “our” refers to Erkan Ecom LLC. By accessing or using the Service, you agree to be bound by these Terms.</p>

  <h2>Use of Service</h2>
  <p>You may use the Service only for lawful purposes and in accordance with these Terms. You are responsible for maintaining the confidentiality of your account.</p>

  <h2>Subscriptions & Payments</h2>
  <p>Paid plans are billed in advance. We use trusted third-party payment processors and/or an authorized reseller acting as Merchant of Record (“Payment Partners”) to process transactions securely. By purchasing, you authorize our Payment Partners to charge your selected payment method. Prices may change with prior notice.</p>

  <h2>Cancellation & Termination</h2>
  <p>You can cancel your subscription anytime from your account/dashboard. Access remains active until the end of the current billing cycle. We may suspend or terminate access for violations of these Terms or misuse of the Service.</p>

  <h2>Refunds</h2>
  <p>Refunds are handled under our <a href="/refund">Refund Policy</a>.</p>

  <h2>Modifications</h2>
  <p>We may update these Terms from time to time. Continued use of the Service after changes become effective constitutes acceptance of the revised Terms.</p>

  <h2>Contact</h2>
  <p>Questions about these Terms? Email <a href="mailto:support@uptrendhunter.com">support@uptrendhunter.com</a>.</p>

  <p style="margin-top:20px"><a class="btn small" href="/">← Back to Home</a></p>
</main>
</body></html>

```

### scripts\convert_to_duckdb.py

```py
# scripts/convert_to_duckdb.py
import duckdb, pathlib, os

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_DIR = pathlib.Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data"))
RAW = PROJECT_ROOT / "data" / "raw"
DB  = DATA_DIR / "trends.duckdb"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def sniff_file(path: pathlib.Path):
    """
    - encoding: 'utf-8' veya 'utf-16'
    - header_line_idx: 'Search Term' başlığının olduğu satır (0-based)
    - delim: '\\t' (tab) veya ',' (virgül)
    """
    # 1) encoding
    encoding = 'utf-8'
    try:
        preview = path.read_text(encoding='utf-8', errors='strict').splitlines()
    except UnicodeDecodeError:
        encoding = 'utf-16'
        preview = path.read_text(encoding='utf-16', errors='strict').splitlines()

    # 2) başlık satırı
    header_line_idx = None
    header_line = ''
    for i, line in enumerate(preview[:200]):
        if 'Search Term' in line and 'Search Frequency Rank' in line:
            header_line_idx = i
            header_line = line
            break
    if header_line_idx is None:
        raise RuntimeError(f"Header not found in {path.name} (no 'Search Term' line)")

    # 3) delimiter
    delim = '\t' if '\t' in header_line else ','

    return encoding, header_line_idx, delim

# DuckDB tablo (şemasız, tek tablo)
con = duckdb.connect(str(DB))
con.execute("""
CREATE TABLE IF NOT EXISTS searches(
  week TEXT,
  term TEXT,
  rank INTEGER
)
""")

files = sorted(RAW.glob("*.csv"))
for p in files:
    enc, skip, delim = sniff_file(p)
    print(f">> importing {p.name} (enc={enc}, skip={skip}, delim={'TAB' if delim=='\\t' else 'COMMA'})")
    # ÖNEMLİ: AUTO_DETECT=TRUE + HEADER=TRUE + SKIP (preamble’ı at)
    con.execute(f"""
        INSERT INTO searches
        SELECT
          '{p.stem}'::TEXT AS week,
          "Search Term"::TEXT AS term,
          TRY_CAST("Search Frequency Rank" AS INT) AS rank
        FROM read_csv(
          '{p.as_posix()}',
          AUTO_DETECT=TRUE,
          HEADER=TRUE,
          SKIP={skip},
          DELIM='{delim}',
          ENCODING='{enc}',
          QUOTE='"',
          ESCAPE='"',
          NULLSTR='',
          IGNORE_ERRORS=TRUE
        )
        WHERE "Search Term" IS NOT NULL AND TRIM("Search Term") <> '';
    """)

con.close()
print("✅ OK ->", DB.as_posix(), "files imported:", len(files))

```

### scripts\daily_report.py

```py
# scripts/daily_report.py  (MARKDOWN RAPOR)

import os, sys, subprocess
from pathlib import Path

# --- Yol haritası entegrasyonu (sabit) ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROADMAP = PROJECT_ROOT / "ROADMAP.md"

def _read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception as e:
        return f"*Dosya okunamadı: {e}*"
# --- /Yol haritası entegrasyonu ---

OUT_MD = PROJECT_ROOT / "daily_report.md"

INCLUDE_EXT = {".py", ".js", ".html", ".css"}
EXCLUDE_DIRS = {".venv", "__pycache__", "logs", ".git", "node_modules"}  # data hariç

def list_tree(root: Path) -> str:
    lines = []
    for dp, dn, fn in os.walk(root):
        p = Path(dp)
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        rel = "." if p == root else str(p.relative_to(root))
        lines.append(f"- **{rel}/**")
        for d in sorted([d for d in dn if d not in EXCLUDE_DIRS]):
            lines.append(f"  - {rel}/{d}/")
        for f in sorted(fn):
            lines.append(f"  - {rel}/{f}")
    return "\n".join(lines)

def collect_files(root: Path):
    files = []
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in INCLUDE_EXT:
            files.append(p)
    files.sort()
    return files

def py_info() -> str:
    v = subprocess.run([sys.executable, "-V"], capture_output=True, text=True).stdout.strip()
    pk = subprocess.run([sys.executable, "-m", "pip", "list", "--format=freeze"], capture_output=True, text=True).stdout
    return v + "\n\n" + pk

def main():
    md = []

    # --- ROADMAP en üste iliştir ---
    if ROADMAP.exists():
        md.append("# 🚀 Sabit Yol Haritası\n\n")
        md.append(_read_text(ROADMAP))
        md.append("\n---\n")
    # --- /ROADMAP ---

    # --- MINI STATE ---
    STATE = PROJECT_ROOT / "STATE.json"
    if STATE.exists():
        import json
        state = json.loads(STATE.read_text(encoding="utf-8"))
        md.append("## STATE SUMMARY\n")
        md.append(f"- Stage: **{state.get('project_stage','?')}**\n")
        md.append(f"- Focus: **{state.get('current_focus','?')}**\n")
        if "next_steps" in state:
            md.append("- Next → " + " → ".join(state["next_steps"]) + "\n")
        md.append("\n---\n")
    # --- /MINI STATE ---

    # --- Günlük rapor gövdesi ---
    md.append(f"# DAILY REPORT\n\n**Project root:** `{PROJECT_ROOT}`\n")

    md.append("## Python & Packages\n")
    md.append("```\n" + py_info() + "\n```")

    md.append("\n## File Tree (filtered)\n")
    md.append(list_tree(PROJECT_ROOT))

    # data/raw hızlı görünüm (varsa ilk 10 dosya)
    data_raw = PROJECT_ROOT / "data" / "raw"
    if data_raw.exists():
        md.append("\n## data/raw (first 10 files)\n")
        names = sorted([p.name for p in data_raw.glob("*.csv")])[:10]
        md.append("```\n" + "\n".join(names) + ("\n" if names else "") + "```")

    md.append("\n## Code Snapshot\n")
    for f in collect_files(PROJECT_ROOT):
        rel = f.relative_to(PROJECT_ROOT)
        lang = f.suffix.lower().lstrip(".")
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            content = f"<<read_error: {e}>>"
        md.append(f"\n### {rel}\n")
        md.append(f"```{lang}\n{content}\n```")
    # --- /Gövde ---

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"OK -> {OUT_MD}")

if __name__ == "__main__":
    main()

# Kaydettiğimiz raporun son snapshot'unu referans olarak sakla
from datetime import datetime
import json
snapshot = {
    "timestamp": datetime.now().isoformat(),
    "files": [str(p) for p in Path(PROJECT_ROOT).rglob("*.py")]
}
with open("data/last_snapshot.json", "w") as f:
    json.dump(snapshot, f, indent=2)
print("Snapshot saved -> data/last_snapshot.json")

# --- AUTO SYNC SNAPSHOT FOR CHATGPT (FULL) ---
import zipfile
from datetime import datetime

snapshot_files = [
    # Core backend
    "app/server/app.py",
    "app/core/trend_core.py",
    "app/core/db.py",
    "requirements.txt",
    "Dockerfile",
    "render.yaml",
    ".env",
    # Frontend
    "app/web/templates/index.html",
    "app/web/static/js/app.js",
    "app/web/static/css/style.css",
    # Scripts & State
    "scripts/daily_report.py",
    "STATE.json",
    "daily_report.md",
    "structure.txt"
]

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
zip_path = f"daily_sync_full_{timestamp}.zip"

with zipfile.ZipFile(zip_path, "w") as z:
    for f in snapshot_files:
        if os.path.exists(f):
            z.write(f)
print(f"📦 Full snapshot created: {zip_path}")
# --- /AUTO SYNC ---

```