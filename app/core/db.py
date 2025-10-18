# app/core/db.py
import duckdb
import os
from pathlib import Path

# Disk kullanırsan DATA_DIR'i env'den alır; yoksa repo/data kullanır
DATA_DIR = Path(os.getenv("DATA_DIR", Path(__file__).resolve().parents[2] / "data"))
DB_PATH  = DATA_DIR / "trends.duckdb"

def get_conn(read_only=True):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(DB_PATH.as_posix(), read_only=read_only)

def init_full(project_root):
    """data/raw altındaki TÜM CSV'leri DuckDB'ye baştan yükler."""
    raw = Path(project_root) / "data" / "raw"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
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
    """Tek bir haftalık CSV'yi ekler (haftalık rutin)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(DB_PATH.as_posix())
    con.execute("""
      CREATE TABLE IF NOT EXISTS trends.searches(
        week TEXT, term TEXT, rank INTEGER
      )
    """)
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
