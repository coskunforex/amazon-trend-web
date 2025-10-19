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
