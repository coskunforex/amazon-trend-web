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
click==8.3.0
colorama==0.4.6
contourpy==1.3.3
cycler==0.12.1
duckdb==1.4.0
et_xmlfile==2.0.0
Flask==3.1.2
fonttools==4.60.0
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
pytz==2025.2
six==1.17.0
tzdata==2025.2
Werkzeug==3.1.3
xlsxwriter==3.2.9

```

## File Tree (filtered)

- **./**
  - ./app/
  - ./config/
  - ./data/
  - ./scripts/
  - ./tools/
  - ./.env
  - ./.env.example
  - ./.gitignore
  - ./Dockerfile
  - ./STATE.json
  - ./daily_report.md
  - ./daily_sync_full_20251019_113201.zip
  - ./daily_sync_full_20251019_122246.zip
  - ./daily_sync_full_20251020_142938.zip
  - ./daily_sync_full_20251022_151429.zip
  - ./daily_sync_full_20251022_202324.zip
  - ./daily_sync_full_20251023_135206.zip
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
  - app\core/db.py
  - app\core/trend_core.py
- **app\server/**
  - app\server/__init__.py
  - app\server/app.py
- **app\web/**
  - app\web/static/
  - app\web/templates/
- **app\web\static/**
  - app\web\static/css/
  - app\web\static/img/
  - app\web\static/js/
- **app\web\static\css/**
  - app\web\static\css/landing.css
  - app\web\static\css/styles.css
- **app\web\static\img/**
  - app\web\static\img/app-screen.png
  - app\web\static\img/sample1.png.png
  - app\web\static\img/sample2.png
- **app\web\static\js/**
  - app\web\static\js/app.js
- **app\web\templates/**
  - app\web\templates/index.html
  - app\web\templates/landing.html
- **config/**
- **data/**
  - data/raw/
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

        # include/exclude: boşluk ile
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

```

### app\web\static\css\landing.css

```css
body {
  margin: 0;
  font-family: "Inter", sans-serif;
  background-color: #0f172a;
  color: #e2e8f0;
}

.container {
  width: 90%;
  max-width: 1100px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  padding: 80px 20px;
  background: linear-gradient(180deg, #0f172a, #1e293b);
}

.hero h1 {
  font-size: 2.8rem;
  font-weight: 700;
  color: #f1f5f9;
}

.hero .ai {
  color: #38bdf8;
}

.subtitle {
  margin-top: 12px;
  font-size: 1.2rem;
  color: #94a3b8;
}

.cta {
  display: inline-block;
  margin-top: 24px;
  background: #38bdf8;
  color: #0f172a;
  padding: 14px 28px;
  border-radius: 10px;
  font-weight: 600;
  text-decoration: none;
  transition: 0.2s;
}
.cta:hover {
  background: #0ea5e9;
  color: white;
}

.how {
  padding: 80px 0;
}

.how h2,
.samples h2 {
  font-size: 2rem;
  color: #f1f5f9;
  margin-bottom: 30px;
  text-align: center;
}

.how-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: center;
}

.how-grid ol {
  font-size: 1.1rem;
  line-height: 1.8;
}

.how-grid img {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.samples {
  background: #1e293b;
  padding: 80px 0;
}

.sample-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

.card {
  background: #0f172a;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  transition: 0.2s;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}
.card:hover {
  transform: scale(1.03);
}
.card img {
  width: 100%;
  border-radius: 8px;
  margin-bottom: 10px;
}

footer {
  text-align: center;
  padding: 40px;
  color: #64748b;
  font-size: 0.9rem;
  border-top: 1px solid #1e293b;
}

```

### app\web\static\css\styles.css

```css
:root{
  --bg:#0f1720;
  --panel:#121a24;
  --text:#e6edf3;
  --muted:#9fb0c3;
  --brand:#1976ff;
  --brand-ghost:#243346;
  --stroke:#1f2a37;
  --radius:14px;
}

*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; background:var(--bg); color:var(--text);
  font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,Inter,Arial,sans-serif;
}

/* NAVIGATION */
.nav{
  max-width:1200px; margin:0 auto; padding:18px 20px;
  display:flex; align-items:center; justify-content:space-between;
}
.nav__brand{font-weight:700; letter-spacing:.2px}
.nav__links a{color:var(--muted); margin-left:18px; text-decoration:none}
.nav__links a:hover{color:var(--text)}

/* HERO */
.hero{
  max-width:1200px; margin:0 auto; padding:48px 20px 24px;
  display:grid; grid-template-columns:1.2fr 1fr; gap:40px; align-items:center;
}
.hero__text h1{font-size:40px; line-height:1.2; margin:0 0 10px}
.hero__text p{color:var(--muted); margin:0 0 16px}
.hero__cta{display:flex; gap:12px; margin:16px 0 10px}
.btn{
  display:inline-block; padding:10px 16px; border-radius:999px; text-decoration:none;
  border:1px solid transparent; font-weight:600;
}
.btn--primary{background:var(--brand); color:#fff}
.btn--primary:hover{filter:brightness(1.06)}
.btn--ghost{background:var(--brand-ghost); color:#cfe0ff; border-color:#2b3a4e}
.btn--ghost:hover{filter:brightness(1.06)}
.hero__bullets{margin:14px 0 0; padding-left:18px; color:var(--muted)}
.hero__bullets li{margin:6px 0}
.hero__media img{
  width:100%; height:auto; border-radius:var(--radius);
  display:block; box-shadow:0 6px 30px rgba(0,0,0,.35);
  border:1px solid var(--stroke);
}

/* VALUE SECTION */
.value{max-width:1200px; margin:20px auto 0; padding:0 20px}
.value h2{margin:14px 0 18px}
.value__grid{
  display:grid; gap:16px; grid-template-columns:repeat(3,1fr);
}
.card{
  background:var(--panel); border:1px solid var(--stroke); border-radius:var(--radius);
  padding:18px;
}
.card h3{margin:6px 0 8px}
.card p{margin:0; color:var(--muted)}

/* SCREENSHOTS */
.screens{max-width:1200px; margin:26px auto 60px; padding:0 20px}
.screens h2{margin:10px 0 12px}
.screens__grid{
  display:grid; gap:16px; grid-template-columns:repeat(3,1fr);
}
figure{margin:0}
figure img{
  width:100%; height:auto; display:block; border-radius:12px;
  border:1px solid var(--stroke); background:#0b1219;
}
figcaption{color:var(--muted); font-size:13px; margin-top:6px}

/* FOOTER */
.footer{
  border-top:1px solid var(--stroke); color:var(--muted);
  max-width:1200px; margin:20px auto 30px; padding:16px 20px;
}

/* RESPONSIVE */
@media (max-width: 1024px){
  .hero{grid-template-columns:1fr; gap:26px}
  .hero__text h1{font-size:34px}
  .value__grid, .screens__grid{grid-template-columns:1fr 1fr}
}
@media (max-width: 640px){
  .value__grid, .screens__grid{grid-template-columns:1fr}
  .hero__text h1{font-size:28px}
}

```

### app\web\static\js\app.js

```js
// app/web/static/js/app.js

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

/* ---------- helpers ---------- */
function showToast(msg, ms=2600){
  if(!toast) { console.warn(msg); return; }
  toast.textContent = msg;
  toast.classList.remove("hidden");
  setTimeout(()=>toast.classList.add("hidden"), ms);
}

async function fetchJSON(url){
  const res = await fetch(url);
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
  if(runBtn) runBtn.disabled = on;
  if(reindexBtn) reindexBtn.disabled = on;
}

function persistFilters(){
  const data = {
    start: startSel.value, end: endSel.value,
    include: includeInp.value, exclude: excludeInp.value
  };
  localStorage.setItem("atf.filters", JSON.stringify(data));
}
function restoreFilters(){
  const raw = localStorage.getItem("atf.filters");
  if(!raw) return;
  try{
    const d = JSON.parse(raw);
    if(d.start) startSel.value = String(d.start);
    if(d.end) endSel.value = String(d.end);
    if(d.include!=null) includeInp.value = d.include;
    if(d.exclude!=null) excludeInp.value = d.exclude;
  }catch{}
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
  }catch(err){
    showToast("Failed to load weeks.");
    console.error(err);
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

/* ---------- query ---------- */
async function runQuery(){
  try{
    setLoading(true);
    const { s, e, sLabel, eLabel, total } = parseWeeks();
    if(rangePill) rangePill.textContent = `${total} weeks • ${sLabel} → ${eLabel}`;

    const norm = str => str.replaceAll(",", " ").trim();
    const params = new URLSearchParams({
      startWeekId: s, endWeekId: e,
      include: norm(includeInp.value),
      exclude: norm(excludeInp.value),
    });

    const rows = await fetchJSON("/uptrends?" + params.toString());
    const sorted = sortRows(rows, currentSort.key, currentSort.dir);
    renderTable(sorted, s, e);
    persistFilters();
  }catch(err){
    showToast(err.message);
    console.error(err);
  }finally{
    setLoading(false);
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
  <svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${title} rank chart">
    <g class="axis">
      <line x1="${pad}" y1="${pad}" x2="${pad}" y2="${H-pad}" />
      <line x1="${pad}" y1="${H-pad}" x2="${W-pad}" y2="${H-pad}" />
      <text x="${pad}" y="${pad-6}">${minR}</text>
      <text x="${pad}" y="${H-pad+16}">${data[0]?.weekLabel||""}</text>
      <text x="${W-pad-80}" y="${H-pad+16}">${data[data.length-1]?.weekLabel||""}</text>
      <text x="${pad}" y="${H-pad+30}" fill="#0f172a">${title}</text>
    </g>
    <path class="line" d="${path}"/>
    ${pts.map(p => p.y===null? "" : `<circle class="dot" cx="${p.x}" cy="${p.y}" r="3"><title>${p.label} • rank ${p.rank}</title></circle>`).join("")}
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
loadWeeks().then(runQuery).catch(console.error);

```

### app\web\templates\index.html

```html
<<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Amazon Trend Finder AI</title>
  <link rel="stylesheet" href="/static/css/styles.css">
  <style>
    /* light UX tweaks */
    :root { --pad: 12px; }
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif; }
    header { padding: var(--pad) 16px; display:flex; align-items:center; gap:12px; }
    header h1 { margin: 0; font-size: 20px; }
    .controls { display:grid; gap:12px; grid-template-columns: repeat(auto-fit, minmax(180px,1fr)); padding: 12px 16px; }
    .controls label { display:block; font-size: 12px; color:#566; margin-bottom:4px; }
    .controls input, .controls select { width:100%; padding:8px; border:1px solid #ccd6e0; border-radius:8px; }
    .controls .actions { display:flex; align-items:end; gap:8px; }
    .summary { padding: 6px 16px; font-size: 13px; color:#234; display:flex; gap:12px; align-items:center; }
    .summary .pill { padding:2px 8px; border-radius:999px; background:#eef3f8; border:1px solid #d9e4ee; }
    table { width:100%; border-collapse:collapse; }
    thead th { text-align:left; font-weight:600; font-size:13px; color:#355; border-bottom:1px solid #e5ecf2; padding:10px 12px; user-select:none; cursor:pointer; }
    tbody td { border-bottom:1px solid #f1f4f7; padding:10px 12px; font-size:14px; }
    tbody tr { transition: background .15s; }
    tbody tr:hover { background:#fafcff; }
    .hidden { display:none !important; }
    .modal { position:fixed; inset:0; background:rgba(9,25,50,.35); display:flex; align-items:center; justify-content:center; padding:16px; }
    .modal-card { background:#fff; border-radius:14px; width:min(820px, 96vw); max-height:92vh; display:flex; flex-direction:column; box-shadow:0 10px 30px rgba(0,0,0,.15); }
    .modal-header { display:flex; align-items:center; justify-content:space-between; padding:12px 16px; border-bottom:1px solid #eef2f7; }
    .modal-header h3 { margin:0; font-size:16px; color:#111; }
    .chart { padding:10px 12px 16px; overflow:auto; }
    .btn { padding:9px 12px; border-radius:10px; border:1px solid #cdd9e5; background:#fff; cursor:pointer; }
    .btn.primary { background:#0b74ff; color:#fff; border-color:#0b74ff; }
    .btn:disabled { opacity:.6; cursor:not-allowed; }
    .toast { position:fixed; right:12px; bottom:12px; background:#0b1220; color:#fff; padding:10px 12px; border-radius:10px; font-size:13px; box-shadow:0 8px 24px rgba(0,0,0,.25); }
    .sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); border:0; }
    .loading { display:inline-flex; align-items:center; gap:8px; }
    .loading .dot { width:6px; height:6px; border-radius:50%; background:#0b74ff; animation: b 1s infinite alternate; }
    .loading .dot:nth-child(2){ animation-delay:.2s } .loading .dot:nth-child(3){ animation-delay:.4s }
    @keyframes b { from{ transform:translateY(0)} to{ transform:translateY(-4px)} }
    svg .axis line { stroke:#c8d4e0; stroke-width:1; }
    svg .axis text { fill:#5a6b7c; font-size:11px; }
    svg .line { fill:none; stroke:#0b74ff; stroke-width:2; }
    svg .dot { fill:#0b74ff; }
    /* modal close button better contrast */
    .modal-header button { color:#111; background:#fff; border:1px solid #cbd5e1; border-radius:8px; padding:4px 8px; }
    .modal-header button:hover { background:#f1f5f9; }
  </style>
</head>
<body>
<header>
  <!-- Logo: dots üstte, A hizasından başlar -->
<div class="logo-container">
  <div class="ai-dots" aria-hidden="true">
    <span>.</span><span>.</span><span>.</span>
  </div>
  <h1 class="app-title">Amazon Trend Finder AI</h1>
</div>



</header>

<section class="controls" aria-labelledby="filtersTitle">
  <h2 id="filtersTitle" class="sr-only">Filters</h2>

  <div>
    <label for="start">Start week</label>
    <select id="start" name="start"></select>
  </div>

  <div>
    <label for="end">End week</label>
    <select id="end" name="end"></select>
  </div>

  <div>
    <label for="include">Include (comma-separated)</label>
    <input id="include" name="include" placeholder="iphone, crocs…" autocomplete="off"/>
  </div>

  <div>
    <label for="exclude">Exclude (comma-separated)</label>
    <input id="exclude" name="exclude" placeholder="case, charger…" autocomplete="off"/>
  </div>

  <div class="actions">
    <button id="run" class="btn primary" aria-label="Find uptrends">Find uptrends</button>
    <!-- removed: reindex button -->
  </div>
</section>

<section class="summary" aria-live="polite">
  <span id="found" class="pill">Found: 0</span>
  <span id="range" class="pill"></span>
  <span id="status" class="loading hidden" aria-hidden="true">
    <span class="dot"></span><span class="dot"></span><span class="dot"></span> Loading…
  </span>
</section>

<section aria-labelledby="resultsTitle">
  <h2 id="resultsTitle" class="sr-only">Results</h2>
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
  <div id="empty" class="hidden" style="padding:12px 16px; color:#566;">
    No results. Try relaxing your filters.
  </div>
</section>

<!-- Modal -->
<div id="modal" class="modal hidden" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
  <div class="modal-card">
    <div class="modal-header">
      <h3 id="modalTitle">Trend</h3>
      <button id="closeModal" class="btn" aria-label="Close">✕</button>
    </div>
    <div id="chart" class="chart"></div>
  </div>
</div>

<div id="toast" class="toast hidden" role="status" aria-live="polite"></div>

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
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Amazon Trend Finder AI</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body class="landing">

  <!-- NAV -->
  <header class="nav">
    <div class="nav__brand">Amazon Trend Finder AI</div>
    <nav class="nav__links">
      <a href="/app">Open App</a>
      <a href="/diag" target="_blank">Diagnostics</a>
    </nav>
  </header>

  <!-- HERO -->
  <section class="hero">
    <div class="hero__text">
      <h1>Turn weekly Amazon search data into actionable trends.</h1>
      <p>Pick a date range, add quick include/exclude keywords, and instantly see which queries are steadily climbing.</p>
      <div class="hero__cta">
        <a class="btn btn--primary" href="/app">Launch App</a>
        <a class="btn btn--ghost" href="#screens">See Screens</a>
      </div>

      <ul class="hero__bullets">
        <li>Strict, week-over-week uptrends</li>
        <li>Fast filtering (include/exclude)</li>
        <li>Lightweight charts with exact ranks</li>
      </ul>
    </div>

    <div class="hero__media">
      <img src="{{ url_for('static', filename='img/app-screen.png') }}"
           alt="App overview" loading="lazy">
    </div>
  </section>

  <!-- WHY SECTION -->
  <section class="value">
    <h2>Why Amazon Trend Finder AI?</h2>
    <div class="value__grid">
      <div class="card">
        <h3>Real weekly signals</h3>
        <p>Based on raw Brand Analytics CSVs—no guessing, just rank deltas across chosen weeks.</p>
      </div>
      <div class="card">
        <h3>Clear improvement scores</h3>
        <p>Sort by total improvement to surface the most meaningful gains first.</p>
      </div>
      <div class="card">
        <h3>Simple, robust UI</h3>
        <p>Pick weeks, filter terms, click any row to see its time-series chart—done.</p>
      </div>
    </div>
  </section>

  <!-- SCREENSHOTS -->
  <section id="screens" class="screens">
    <h2>Screenshots</h2>
    <div class="screens__grid">
      <figure>
        <img src="{{ url_for('static', filename='img/app-screen.png') }}"
             alt="Results table" loading="lazy">
        <figcaption>Rank deltas table</figcaption>
      </figure>
      <figure>
        <img src="{{ url_for('static', filename='img/sample1.png') }}"
             alt="Trend chart" loading="lazy">
        <figcaption>Trend chart modal</figcaption>
      </figure>
      <figure>
        <img src="{{ url_for('static', filename='img/sample2.png') }}"
             alt="Filters & weeks" loading="lazy">
        <figcaption>Filters & week picker</figcaption>
      </figure>
    </div>
  </section>

  <footer class="footer">
    <span>© 2025 Amazon Trend Finder AI</span>
  </footer>

</body>
</html>

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