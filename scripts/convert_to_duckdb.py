# scripts/convert_to_duckdb.py
import duckdb, pathlib, os

DATA_DIR = pathlib.Path(os.getenv("DATA_DIR", "data"))
RAW = pathlib.Path("data/raw")
DB  = DATA_DIR / "trends.duckdb"
DATA_DIR.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(str(DB))
con.execute("CREATE SCHEMA IF NOT EXISTS trends")
con.execute("""
CREATE TABLE IF NOT EXISTS trends.searches(
  week TEXT,
  term TEXT,
  rank INTEGER
)
""")

files = sorted(RAW.glob("*.csv"))
for p in files:
  print(">> importing", p.name)
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
print("OK ->", DB.as_posix(), "files:", len(files))
