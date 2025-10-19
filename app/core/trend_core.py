"""
trend_core.py — KANONİK ÇEKİRDEK
- data/raw/ altındaki tüm haftalık CSV'leri okur (60+ hafta).
- weekId (1=en eski, N=en yeni) üretir.
- Strict uptrend sorgularını ve seri verisini döndürür.
"""

# --- ADD: disk cache ---
import hashlib, pickle
from pathlib import Path

def _files_signature(raw_dir:str)->str:
    names=[]
    for n in sorted(os.listdir(raw_dir)):
        p=os.path.join(raw_dir,n)
        if os.path.isfile(p):
            st=os.stat(p)
            names.append(f"{n}:{st.st_size}:{int(st.st_mtime)}")
    return hashlib.md5("|".join(names).encode()).hexdigest()

def build_index_cached(project_root:str)->'TrendIndex':
    raw_dir = os.path.join(project_root, "data", "raw")
    store   = Path(project_root)/"data"/"store"
    store.mkdir(parents=True, exist_ok=True)
    sig = _files_signature(raw_dir)
    cache = store/f"index_{sig}.pkl"
    if cache.exists():
        return pickle.loads(cache.read_bytes())
    idx = build_index(project_root)  # mevcut fonksiyonunu kullanıyoruz
    cache.write_bytes(pickle.dumps(idx, protocol=pickle.HIGHEST_PROTOCOL))
    return idx
# --- /ADD ---


import os, re, csv
from datetime import date
from typing import Dict, List, Tuple, Optional

# Beklenen dosya adı: US_Top_Search_Terms_Simple_Week_YYYY_MM_DD.csv
DATE_RE = re.compile(r"US_Top_Search_Terms_Simple_Week_(\d{4})_(\d{2})_(\d{2})\.csv$", re.I)

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

def _list_week_files(raw_dir: str) -> List[Tuple[date, str]]:
    files = []
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
    """
    for i, row in enumerate(rows):
        norm = [c.strip().lower() for c in row]
        if "search frequency rank" in norm and "search term" in norm:
            return norm.index("search frequency rank"), norm.index("search term"), i + 1
    return None, None, 0

def _read_week_csv(path: str, encoding="utf-8-sig") -> Dict[str, int]:
    """
    Amazon Brand Analytics CSV'lerini esnek şekilde okur.
    - 'Reporting Range' veya 'Select week' satırlarını atlar.
    - Fazla virgül veya tırnak hatalarına toleranslıdır.
    """
    import csv

    with open(path, "r", encoding=encoding, newline="") as f:
        reader = list(csv.reader(f))

    # Başlığı bul
    rank_idx, term_idx, start = _find_header_index(reader)

    # Eğer bulunamazsa: fallback
    if start == 0:
        for i, row in enumerate(reader[:15]):  # ilk 15 satırı tara
            cols = [c.strip().lower() for c in row if c.strip()]
            if len(cols) >= 2 and "rank" in cols[0] and "term" in cols[1]:
                rank_idx, term_idx, start = 0, 1, i + 1
                break

    out: Dict[str, int] = {}

    for row in reader[start:]:
        if not row or len(row) < 2:
            continue

        # Sütunları esnek al
        try:
            rank_raw = row[rank_idx].strip() if rank_idx < len(row) else ""
            term_raw = row[term_idx].strip() if term_idx < len(row) else ""
        except Exception:
            continue

        # Geçersiz satırları atla
        if not rank_raw or not term_raw:
            continue

        # Sayısal rank temizle
        try:
            rank = int(str(rank_raw).replace(",", "").strip())
        except:
            continue

        term = term_raw.lower()
        if not term or term.startswith("search term"):
            continue

        # Aynı terim varsa en iyi (en düşük) rank'ı al
        if term not in out or rank < out[term]:
            out[term] = rank

    return out


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
    for i, (dt, _) in enumerate(files, start=1):
        idx.weeks.append((i, dt))
        idx.weekid_to_date[i] = dt
        idx.week_labels[i] = f"Week {i} ({dt.isoformat()})"

    for week_id, (_, path) in zip(range(1, len(files)+1), files):
        ranks = _read_week_csv(path)
        for term, rank in ranks.items():
            if term not in idx.term_ranks:
                idx.term_ranks[term] = {}
            idx.term_ranks[term][week_id] = rank

    return idx

import re

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


def _strict_uptrend_for_range(ranks_by_weekid: Dict[int, int], start_id: int, end_id: int) -> Optional[Tuple[int,int,int]]:
    """
    Seçilen [start_id..end_id] aralığında:
      - Her hafta mevcut
      - Her adımda prev_rank > curr_rank  (strict)
    True ise (start_rank, end_rank, total_improvement) döndürür; aksi halde None.
    """
    last_rank = None
    start_rank = None
    for w in range(start_id, end_id+1):
        if w not in ranks_by_weekid:
            return None
        r = ranks_by_weekid[w]
        if last_rank is None:
            start_rank = r
        else:
            if not (last_rank > r):
                return None
        last_rank = r
    end_rank = last_rank
    total_impr = start_rank - end_rank  # pozitif = iyileşme
    return (start_rank, end_rank, total_impr)

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

    results = []
    for term, weeks_map in idx.term_ranks.items():
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

def query_series(idx: TrendIndex, term: str, start_week_id: int, end_week_id: int) -> List[Dict]:
    if start_week_id > end_week_id:
        start_week_id, end_week_id = end_week_id, start_week_id
    series = []
    ranks_map = idx.term_ranks.get(term.lower(), {})
    for w in range(start_week_id, end_week_id+1):
        series.append({
            "weekId": w,
            "weekLabel": idx.week_labels.get(w, f"Week {w}"),
            "rank": ranks_map.get(w)  # None olabilir (UI göstermek için)
        })
    return series
