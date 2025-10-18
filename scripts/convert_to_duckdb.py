# app/core/db.py
import duckdb
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "trends.duckdb"

def get_conn(read_only=True):
    return duckdb.connect(DB_PATH.as_posix(), read_only=read_only)

def init_full(project_root):
    """data/raw içindeki TÜM CSV'leri DuckDB'ye baştan yükler."""
    root = Path(project_root)
    raw  = root / "data" / "raw"
    con  = duckdb.connect(DB_PATH.as_posix())
    con.execute("CREATE SCHEMA IF NOT EXISTS trends")
    con.execute("DROP TABLE IF EXISTS trends.searches")
    con.execute("CREATE TABLE trends.searches(week TEXT, term TEXT, rank INTEGER)")
    for p in sorted(raw.glob("*.csv")):
        # !!! DİKKAT: header=false + column0/1 + preamble filtreleri
        con.execute(f"""
            INSERT INTO trends.searches
            SELECT
              '{p.stem}'::TEXT AS week,
              column0::TEXT    AS term,
              TRY_CAST(column1 AS INT) AS rank
            FROM read_csv_auto('{p.as_posix()}', header=false)
            WHERE column0 IS NOT NULL
              AND column0 <> ''
              AND column0 <> 'Search Term'                 -- gerçek header satırını at
              AND column0 NOT LIKE 'Reporting Range=%'     -- preamble 1
              AND column0 NOT LIKE 'US_Top_Search_Terms_%' -- preamble 2
        """)
    con.close()

def append_week(week_csv_path: str, week_label: str):
    """Tek bir haftalık CSV'yi ekler (haftalık rutin)."""
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
