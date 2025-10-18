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
