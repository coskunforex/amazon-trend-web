import duckdb
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "trends.duckdb"

def get_conn(read_only=True):
    return duckdb.connect(DB_PATH.as_posix(), read_only=read_only)

def init_full(project_root):
    """data/raw içindeki tüm CSV’leri DuckDB'ye baştan yüklemek istersen (canlıda)."""
    import pathlib
    root = Path(project_root)
    raw  = root / "data" / "raw"
    con  = duckdb.connect(DB_PATH.as_posix())
    con.execute("DROP TABLE IF EXISTS searches;")
    con.execute("CREATE TABLE searches(week TEXT, term TEXT, rank INTEGER);")
    for p in sorted(raw.glob("*.csv")):
        con.execute(f"""
          INSERT INTO searches
          SELECT '{p.stem}'::TEXT, "Search Term"::TEXT,
                 TRY_CAST(REPLACE("Search Frequency Rank", ',', '') AS INT)
          FROM read_csv_auto('{p.as_posix()}', header=true, sample_size=-1, ignore_errors=true);
        """)
    con.close()

def append_week(week_csv_path: str, week_label: str):
    """Yeni bir CSV haftasını DuckDB'ye ekle (haftalık rutin)."""
    con = duckdb.connect(DB_PATH.as_posix())
    con.execute("""
      CREATE TABLE IF NOT EXISTS searches(week TEXT, term TEXT, rank INTEGER);
    """)
    con.execute(f"""
      INSERT INTO searches
      SELECT '{week_label}'::TEXT, "Search Term"::TEXT,
             TRY_CAST(REPLACE("Search Frequency Rank", ',', '') AS INT)
      FROM read_csv_auto('{week_csv_path}', header=true, sample_size=-1, ignore_errors=true);
    """)
    con.close()
