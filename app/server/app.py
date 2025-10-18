# /weeks
con = get_conn()
rows = con.execute("SELECT DISTINCT week FROM main.trends.searches ORDER BY week").fetchall()
con.close()

# /uptrends içinde q'yu çalıştırırken FROM ve WHERE kısımlarındaki tabloyu:
#   FROM main.trends.searches
# olarak yaz.
# Örnek:
q = f"""
WITH base AS (
  SELECT week, term, rank,
         ROW_NUMBER() OVER (PARTITION BY term ORDER BY week) rn
  FROM main.trends.searches
  WHERE week BETWEEN ? AND ?
),
pairs AS (
  SELECT b1.term,
         SUM(CASE WHEN b2.rank < b1.rank THEN 1 ELSE 0 END) AS ups
  FROM base b1
  JOIN base b2 ON b2.term=b1.term AND b2.rn=b1.rn+1
  GROUP BY b1.term
)
SELECT term, ups
FROM pairs
WHERE ups >= 1
ORDER BY ups DESC
LIMIT {limit} OFFSET {offset};
"""

# /series
rows = con.execute("""
  SELECT week, rank
  FROM main.trends.searches
  WHERE term = ?
  ORDER BY week
""", [term]).fetchall()
