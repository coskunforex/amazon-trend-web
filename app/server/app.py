@app.get("/uptrends")
def uptrends():
    """
    Param:
      startWeekLabel, endWeekLabel (zorunlu)
      include, exclude (opsiyonel, virgül ile)
      limit, offset
    """
    try:
        startL = request.args.get("startWeekLabel")
        endL   = request.args.get("endWeekLabel")
        if not startL or not endL:
            return jsonify({"error":"startWeekLabel & endWeekLabel required"}), 400
        include = (request.args.get("include") or "").strip()
        exclude = (request.args.get("exclude") or "").strip()
        limit   = request.args.get("limit", 200, type=int)
        offset  = request.args.get("offset", 0, type=int)

        con = get_conn(read_only=True)

        # include/exclude filtre cümleleri
        inc_clause = ""
        if include:
            inc_parts = [p.strip().lower() for p in include.split(",") if p.strip()]
            if inc_parts:
                ors = " OR ".join([f"regexp_matches(term, '\\\\b{p}\\\\b')" for p in inc_parts])
                inc_clause = f"AND ({ors})"
        exc_clause = ""
        if exclude:
            exc_parts = [p.strip().lower() for p in exclude.split(",") if p.strip()]
            if exc_parts:
                ors = " OR ".join([f"regexp_matches(term, '\\\\b{p}\\\\b')" for p in exc_parts])
                exc_clause = f"AND NOT ({ors})"

        # SIKI FİLTRE: en az bir harf içersin, #NAME? olmasın, saf sayısal/scientific formatı olmasın
        #   - regexp_matches(term, '[A-Za-z]')  -> en az bir harf
        #   - NOT regexp_matches(term, '^[0-9eE.+-]+$') -> tamamı sayı/işaret/E/e/. + - ise ele
        #   - UPPER(TRIM(term)) <> '#NAME?' -> excel hatası ele
        q = f"""
        PRAGMA threads=1;
        WITH all_weeks AS (
          SELECT DISTINCT week FROM searches ORDER BY week
        ),
        widx AS (
          SELECT week, ROW_NUMBER() OVER (ORDER BY week) AS week_id FROM all_weeks
        ),
        bounds AS (
          SELECT
            (SELECT week_id FROM widx WHERE week = ?) AS s,
            (SELECT week_id FROM widx WHERE week = ?) AS e
        ),
        base AS (
          SELECT s.term, s.rank, w.week_id
          FROM searches s
          JOIN widx w USING(week)
          JOIN bounds b ON w.week_id BETWEEN b.s AND b.e
          WHERE s.rank IS NOT NULL
            AND s.term IS NOT NULL
            AND TRIM(s.term) <> ''
            AND UPPER(TRIM(s.term)) <> '#NAME?'
            AND regexp_matches(s.term, '[A-Za-z]')
            AND NOT regexp_matches(s.term, '^[0-9eE.+-]+$')
            {inc_clause}
            {exc_clause}
        ),
        stepped AS (
          SELECT term, rank,
                 LEAD(rank) OVER (PARTITION BY term ORDER BY week_id) AS next_rank
          FROM base
        )
        SELECT term,
               SUM(CASE WHEN next_rank < rank THEN 1 ELSE 0 END) AS ups
        FROM stepped
        GROUP BY term
        HAVING SUM(CASE WHEN next_rank < rank THEN 1 ELSE 0 END) >= 1
        ORDER BY ups DESC
        LIMIT {limit} OFFSET {offset};
        """
        rows = con.execute(q, [startL, endL]).fetchall()
        con.close()
        return jsonify([{"term": r[0], "ups": int(r[1])} for r in rows])
    except Exception as e:
        app.logger.exception("uptrends failed")
        return jsonify({"error":"uptrends_failed","message":str(e)}), 500
