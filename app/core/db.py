# app/core/db.py
import duckdb
import os
from pathlib import Path

DATA_DIR = Path(os.getenv("DATA_DIR", Path(__file__).resolve().parents[2] / "data"))
DB_PATH  = DATA_DIR / "trends.duckdb"

def _ensure_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        con = duckdb.connect(DB_PATH.as_posix())
        con.execute("CREATE SCHEMA IF NOT EXISTS trends")
        con.execute("CREATE TABLE IF NOT EXISTS trends.searches(week TEXT, term TEXT, rank INTEGER)")
        con.close()

def get_conn(read_only=True):
    # DB yoksa oluştur (read_only olsa bile)
    _ensure_db()
    return duckdb.connect(DB_PATH.as_posix(), read_only=read_only)

def init_full(project_root):
    """data/raw altındaki TÜM CSV'leri DuckDB'ye baştan yükler."""
    from pathlib import Path
    raw = Path(project_root) / "data" / "raw"
    _ensure_db()
    con  = duckdb.connect(DB_PATH.as_posix())
    con.execute("CREATE SCHEMA IF NOT EXISTS trends")
    con.execute("DROP TABLE IF EXISTS trends.searches")
    con.execute("CREATE TABLE trends.searches(week TEXT, term TEXT, rank INTEGER)")
    for p in sorted(raw.glob("*.csv")):
        con.execute(f"""
            INSERT INTO trends.searches
            SELECT
              '{p.stem}'::TEXT AS week,
              column0::TEXT    AS term,
              TRY_CAST(column1 AS INT) AS rank
            FROM read_csv_auto('{p.as_posix()}', header=false)
            WHERE column0 IS NOT NULL
              AND column0 <> ''
              AND column0 <> 'Search Term'
              AND column0 NOT LIKE 'Reporting Range=%'
              AND column0 NOT LIKE 'US_Top_Search_Terms_%'
        """)
    con.close()

def append_week(week_csv_path: str, week_label: str):
    """Tek haftalık CSV ekle (haftalık rutin)."""
    _ensure_db()
    con = duckdb.connect(DB_PATH.as_posix())
    con.execute("CREATE TABLE IF NOT EXISTS trends.searches(week TEXT, term TEXT, rank INTEGER)")
    con.execute(f"""
        INSERT INTO trends.searches
        SELECT
          '{week_label}'::TEXT,
          column0::TEXT,
          TRY_CAST(column1 AS INT)
        FROM read_csv_auto('{week_csv_path}', header=false)
        WHERE column0 IS NOT NULL
          AND column0 <> ''
          AND column0 <> 'Search Term'
          AND column0 NOT LIKE 'Reporting Range=%'
          AND column0 NOT LIKE 'US_Top_Search_Terms_%'
    """)
    con.close()
