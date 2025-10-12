# 🚀 Sabit Yol Haritası


# Deployment Yol Haritası (Sabit Omurga)
- Runtime: Python 3.11 (Linux/amd64)
- Paketleme: Docker (multi-stage)
- Veri: DuckDB + Parquet
- Proxy + TLS: Caddy (Let’s Encrypt)
- CI/CD: GitHub Actions → image → SSH deploy
- Konfig: .env / .env.prod
- İzleme: Sentry (errors), UptimeRobot (/health), günlük S3 yedek
- Sunucu: Remote VM (>= 4 vCPU / 8 GB RAM; ideal 8/16 + NVMe)


---

## STATE SUMMARY

- Stage: **Deployment prep**

- Focus: **Dockerfile ve remote VM hazırlığı**

- Next → compose.prod.yml → CI/CD pipeline → health endpoint


---

# DAILY REPORT

**Project root:** `C:\Users\yacos\amazon-trend-web`

## Python & Packages

```
Python 3.13.7

blinker==1.9.0
click==8.3.0
colorama==0.4.6
contourpy==1.3.3
cycler==0.12.1
duckdb==1.4.0
et_xmlfile==2.0.0
Flask==3.1.2
fonttools==4.60.0
itsdangerous==2.2.0
Jinja2==3.1.6
kiwisolver==1.4.9
MarkupSafe==3.0.3
matplotlib==3.10.6
numpy==2.3.3
openpyxl==3.1.5
packaging==25.0
pandas==2.3.2
pillow==11.3.0
pip==25.2
pyparsing==3.2.5
python-dateutil==2.9.0.post0
pytz==2025.2
six==1.17.0
tzdata==2025.2
Werkzeug==3.1.3
xlsxwriter==3.2.9

```

## File Tree (filtered)

- **./**
  - ./app/
  - ./config/
  - ./data/
  - ./scripts/
  - ./tools/
  - ./.env
  - ./.env.example
  - ./STATE.json
  - ./daily_report.md
  - ./roadmap.md
- **app/**
  - app/core/
  - app/server/
  - app/web/
  - app/__init__.py
- **app\core/**
  - app\core/__init__.py
  - app\core/trend_core.py
- **app\server/**
  - app\server/__init__.py
  - app\server/app.py
- **app\web/**
  - app\web/static/
  - app\web/templates/
- **app\web\static/**
  - app\web\static/css/
  - app\web\static/js/
- **app\web\static\css/**
  - app\web\static\css/styles.css
- **app\web\static\js/**
  - app\web\static\js/app.js
- **app\web\templates/**
  - app\web\templates/index.html
- **config/**
- **data/**
  - data/raw/
  - data/store/
- **data\raw/**
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_07_12.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_07_19.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_07_26.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_08_02.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_08_09.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_08_16.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_08_23.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_08_30.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_09_06.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_09_13.csv
  - data\raw/US_Top_Search_Terms_Simple_Week_2025_09_20.csv
- **data\store/**
  - data\store/index_4556008e7eabdf36c29ad24b7a4a3631.pkl
- **scripts/**
  - scripts/daily_report.py
- **tools/**

## data/raw (first 10 files)

```
US_Top_Search_Terms_Simple_Week_2025_07_12.csv
US_Top_Search_Terms_Simple_Week_2025_07_19.csv
US_Top_Search_Terms_Simple_Week_2025_07_26.csv
US_Top_Search_Terms_Simple_Week_2025_08_02.csv
US_Top_Search_Terms_Simple_Week_2025_08_09.csv
US_Top_Search_Terms_Simple_Week_2025_08_16.csv
US_Top_Search_Terms_Simple_Week_2025_08_23.csv
US_Top_Search_Terms_Simple_Week_2025_08_30.csv
US_Top_Search_Terms_Simple_Week_2025_09_06.csv
US_Top_Search_Terms_Simple_Week_2025_09_13.csv
```

## Code Snapshot


### app\__init__.py

```py

```

### app\core\__init__.py

```py

```

### app\core\trend_core.py

```py
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
    with open(path, "r", encoding=encoding, newline="") as f:
        reader = list(csv.reader(f))
    rank_idx, term_idx, start = _find_header_index(reader)
    out: Dict[str, int] = {}
    for row in reader[start:]:
        if not row:
            continue
        if (
            rank_idx is None or term_idx is None
            or rank_idx >= len(row) or term_idx >= len(row)
        ):
            # esnek fallback: ilk iki dolu sütun
            cols = [c for c in row if c and c.strip()]
            if len(cols) < 2:
                continue
            rank_raw, term_raw = cols[0], cols[1]
        else:
            rank_raw, term_raw = row[rank_idx], row[term_idx]

        term = (term_raw or "").strip().lower()
        if not term:
            continue
        try:
            rank = int(str(rank_raw).strip().replace(",", ""))
        except:
            continue
        if rank < 1:
            continue
        # aynı terim tekrarlanırsa en iyi (en küçük) rank'ı tut
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

```

### app\server\__init__.py

```py

```

### app\server\app.py

```py
from flask import Flask, jsonify, request, render_template
import os
from app.core.trend_core import build_index_cached, query_uptrends, query_series


# Proje kökü: bu dosyanın 3 üstü (amazon-trend-web/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, "app", "web", "templates"),
    static_folder=os.path.join(PROJECT_ROOT, "app", "web", "static"),
)

# Uygulama açılışında index'i yükle
# Eski:
# INDEX = build_index(PROJECT_ROOT)

# Yeni:
INDEX = build_index_cached(PROJECT_ROOT)


@app.route("/")
def home():
    return render_template("index.html")

@app.get("/weeks")
def weeks():
    items = []
    for weekId, dt in INDEX.weeks:
        items.append({
            "weekId": weekId,
            "label": INDEX.week_labels[weekId],
            "date": dt.isoformat()
        })
    return jsonify(items)

@app.get("/uptrends")
def uptrends():
    try:
        startId = int(request.args.get("startWeekId"))
        endId = int(request.args.get("endWeekId"))
    except:
        return jsonify({"error":"startWeekId & endWeekId required"}), 400

    include = request.args.get("include") or ""
    exclude = request.args.get("exclude") or ""

    rows = query_uptrends(INDEX, startId, endId, include=include, exclude=exclude, limit=5000)
    return jsonify(rows)

@app.get("/series")
def series():
    term = request.args.get("term")
    if not term:
        return jsonify({"error":"term required"}), 400
    try:
        startId = int(request.args.get("startWeekId"))
        endId = int(request.args.get("endWeekId"))
    except:
        return jsonify({"error":"startWeekId & endWeekId required"}), 400

    rows = query_series(INDEX, term, startId, endId)
    return jsonify(rows)

@app.get("/reindex")
def reindex():
    global INDEX
    INDEX = build_index(PROJECT_ROOT)
    return jsonify({"status":"ok", "weeks": len(INDEX.weeks)})

if __name__ == "__main__":
    # Geliştirme için:
    app.run(host="127.0.0.1", port=8000, debug=True)

```

### app\web\static\css\styles.css

```css
:root{--bg:#0b0d10;--fg:#e9eef3;--muted:#9fb0c0;--card:#131821;--border:#233042}
*{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.4 system-ui,Segoe UI,Arial}
header{padding:16px 20px;border-bottom:1px solid var(--border)}
h1{margin:0;font-size:18px}
.controls{display:flex;gap:12px;flex-wrap:wrap;padding:12px 20px;border-bottom:1px solid var(--border)}
.controls label{display:block;font-size:12px;color:var(--muted);margin-bottom:4px}
.controls input,.controls select{padding:8px 10px;background:var(--card);border:1px solid var(--border);color:var(--fg);border-radius:8px;min-width:180px}
button{padding:10px 14px;background:#3558ff;color:#fff;border:0;border-radius:8px;cursor:pointer}
button:hover{filter:brightness(1.05)}
#tbl{width:100%;border-collapse:collapse;margin:12px 20px}
#tbl th,#tbl td{border-bottom:1px solid var(--border);padding:10px}
#tbl tbody tr{cursor:pointer}
#tbl tbody tr:hover{background:#141c27}
.summary{padding:6px 20px;color:var(--muted)}
.modal{position:fixed;inset:0;background:rgba(0,0,0,.6);display:flex;align-items:center;justify-content:center}
.hidden{display:none}
.modal-card{background:var(--card);border:1px solid var(--border);border-radius:12px;min-width:320px;max-width:720px;width:90%}
.modal-header{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-bottom:1px solid var(--border)}
.chart{padding:10px 14px}
svg{width:100%;height:260px;background:transparent}
.axis text{fill:var(--muted);font-size:12px}
.axis line,.axis path{stroke:var(--border)}
.line{fill:none;stroke:#5cc8ff;stroke-width:2}
.dot{fill:#5cc8ff}

```

### app\web\static\js\app.js

```js
const $ = (sel)=>document.querySelector(sel);
const startSel = $("#start"), endSel = $("#end");
const includeInp = $("#include"), excludeInp = $("#exclude");
const runBtn = $("#run"), reindexBtn = $("#reindex");
const tbody = $("#tbl tbody"), found = $("#found");
const modal = $("#modal"), closeModalBtn = $("#closeModal"), chartEl = $("#chart");
let weeks = [];

async function loadWeeks(){
  const res = await fetch("/weeks");
  weeks = await res.json();
  startSel.innerHTML = ""; endSel.innerHTML = "";
  for(const w of weeks){
    const o1 = document.createElement("option"); o1.value = w.weekId; o1.textContent = w.label;
    const o2 = document.createElement("option"); o2.value = w.weekId; o2.textContent = w.label;
    startSel.appendChild(o1); endSel.appendChild(o2);
  }
  if(weeks.length >= 2){
    startSel.value = weeks[Math.max(0, weeks.length-6)].weekId; // varsayılan: son 6 haftanın başı
    endSel.value = weeks[weeks.length-1].weekId;
  }
}

async function runQuery(){
  let s = parseInt(startSel.value,10), e = parseInt(endSel.value,10);
  if(!s || !e) return;
  if(e < s){ const t=s; s=e; e=t; }
  if((e - s + 1) < 2){ alert("Aralık en az 2 hafta olmalı."); return; }

  const params = new URLSearchParams({
    startWeekId: s, endWeekId: e,
    include: includeInp.value.trim(),
    exclude: excludeInp.value.trim(),
  });
  const res = await fetch("/uptrends?" + params.toString());
  const rows = await res.json();
  renderTable(rows, s, e);
}

function renderTable(rows, s, e){
  tbody.innerHTML = "";
  found.textContent = `Found: ${rows.length}`;
  for(const r of rows){
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${r.term}</td>
      <td>${r.start_rank}</td>
      <td>${r.end_rank}</td>
      <td>${r.total_improvement}</td>
      <td>${r.weeks}</td>
    `;
    tr.addEventListener("click", ()=>showSeries(r.term, s, e));
    tbody.appendChild(tr);
  }
}

async function showSeries(term, s, e){
  const params = new URLSearchParams({ term, startWeekId: s, endWeekId: e });
  const res = await fetch("/series?" + params.toString());
  const data = await res.json();
  drawMiniChart(term, data);
  modal.classList.remove("hidden");
}

function drawMiniChart(title, data){
  // y ekseni ters: min rank (en iyi) üstte
  const ranks = data.map(d=>d.rank).filter(v=>typeof v==="number");
  const minR = Math.min(...ranks), maxR = Math.max(...ranks);
  const pad = 24, W = 680, H = 240;
  const y = (v)=> { // ters eksen
    const t = (v - minR) / Math.max(1, (maxR - minR));
    return pad + (H - 2*pad) * t;
  };
  const x = (i)=> pad + (W - 2*pad) * (i/(Math.max(1, data.length-1)));

  const pts = data.map((d,i)=>{
    const rr = (typeof d.rank==="number") ? d.rank : null;
    return { x:x(i), y: rr!==null? y(rr): null, label:d.weekLabel, rank: rr };
  });

  let path = "";
  for(let i=0;i<pts.length;i++){
    const p = pts[i];
    if(p.y===null) continue;
    path += (path===""? `M ${p.x} ${p.y}` : ` L ${p.x} ${p.y}`);
  }

  const svg = `
  <svg viewBox="0 0 ${W} ${H}">
    <g class="axis">
      <line x1="${pad}" y1="${pad}" x2="${pad}" y2="${H-pad}" />
      <line x1="${pad}" y1="${H-pad}" x2="${W-pad}" y2="${H-pad}" />
      <text x="${pad}" y="${pad-6}">${minR}</text>
      <text x="${pad}" y="${H-pad+16}">${data[0]?.weekLabel||""}</text>
      <text x="${W-pad-80}" y="${H-pad+16}">${data[data.length-1]?.weekLabel||""}</text>
      <text x="${pad}" y="${H-pad+30}" fill="#9fb0c0">${title}</text>
    </g>
    <path class="line" d="${path}"/>
    ${pts.map(p => p.y===null? "" : `<circle class="dot" cx="${p.x}" cy="${p.y}" r="3"><title>${p.label} • rank ${p.rank}</title></circle>`).join("")}
  </svg>`;
  $("#modalTitle").textContent = title;
  chartEl.innerHTML = svg;
}

$("#run").addEventListener("click", runQuery);
$("#reindex").addEventListener("click", async ()=>{
  await fetch("/reindex");
  await loadWeeks();
});
$("#closeModal").addEventListener("click", ()=>modal.classList.add("hidden"));
modal.addEventListener("click",(e)=>{ if(e.target===modal) modal.classList.add("hidden"); });

loadWeeks().then(runQuery);

```

### app\web\templates\index.html

```html
<!doctype html>
<html lang="tr">
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Amazon Trend Finder</title>
<link rel="stylesheet" href="/static/css/styles.css">
<body>
<header>
  <h1>Amazon Trend Finder</h1>
</header>

<section class="controls">
  <div>
    <label>Start week</label>
    <select id="start"></select>
  </div>
  <div>
    <label>End week</label>
    <select id="end"></select>
  </div>
  <div>
    <label>Include</label>
    <input id="include" placeholder="iphone, croc..." />
  </div>
  <div>
    <label>Exclude</label>
    <input id="exclude" placeholder="case, charger..." />
  </div>
  <button id="run">Find uptrends</button>
  <button id="reindex" title="Yeni hafta eklediysen">Reindex</button>
</section>

<section class="summary">
  <span id="found">Found: 0</span>
</section>

<section>
  <table id="tbl">
    <thead>
      <tr>
        <th>Term</th>
        <th>Start rank</th>
        <th>End rank</th>
        <th>Total improvement</th>
        <th>Weeks</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>
</section>

<!-- Modal -->
<div id="modal" class="modal hidden" role="dialog" aria-modal="true">
  <div class="modal-card">
    <div class="modal-header">
      <h3 id="modalTitle">Trend</h3>
      <button id="closeModal">✕</button>
    </div>
    <div id="chart" class="chart"></div>
  </div>
</div>

<script src="/static/js/app.js"></script>
</body>
</html>

```

### scripts\daily_report.py

```py
# scripts/daily_report.py  (MARKDOWN RAPOR)

import os, sys, subprocess
from pathlib import Path

# --- Yol haritası entegrasyonu (sabit) ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROADMAP = PROJECT_ROOT / "ROADMAP.md"

def _read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception as e:
        return f"*Dosya okunamadı: {e}*"
# --- /Yol haritası entegrasyonu ---

OUT_MD = PROJECT_ROOT / "daily_report.md"

INCLUDE_EXT = {".py", ".js", ".html", ".css"}
EXCLUDE_DIRS = {".venv", "__pycache__", "logs", ".git", "node_modules"}  # data hariç

def list_tree(root: Path) -> str:
    lines = []
    for dp, dn, fn in os.walk(root):
        p = Path(dp)
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        rel = "." if p == root else str(p.relative_to(root))
        lines.append(f"- **{rel}/**")
        for d in sorted([d for d in dn if d not in EXCLUDE_DIRS]):
            lines.append(f"  - {rel}/{d}/")
        for f in sorted(fn):
            lines.append(f"  - {rel}/{f}")
    return "\n".join(lines)

def collect_files(root: Path):
    files = []
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in INCLUDE_EXT:
            files.append(p)
    files.sort()
    return files

def py_info() -> str:
    v = subprocess.run([sys.executable, "-V"], capture_output=True, text=True).stdout.strip()
    pk = subprocess.run([sys.executable, "-m", "pip", "list", "--format=freeze"], capture_output=True, text=True).stdout
    return v + "\n\n" + pk

def main():
    md = []

    # --- ROADMAP en üste iliştir ---
    if ROADMAP.exists():
        md.append("# 🚀 Sabit Yol Haritası\n\n")
        md.append(_read_text(ROADMAP))
        md.append("\n---\n")
    # --- /ROADMAP ---

    # --- MINI STATE ---
    STATE = PROJECT_ROOT / "STATE.json"
    if STATE.exists():
        import json
        state = json.loads(STATE.read_text(encoding="utf-8"))
        md.append("## STATE SUMMARY\n")
        md.append(f"- Stage: **{state.get('project_stage','?')}**\n")
        md.append(f"- Focus: **{state.get('current_focus','?')}**\n")
        if "next_steps" in state:
            md.append("- Next → " + " → ".join(state["next_steps"]) + "\n")
        md.append("\n---\n")
    # --- /MINI STATE ---

    # --- Günlük rapor gövdesi ---
    md.append(f"# DAILY REPORT\n\n**Project root:** `{PROJECT_ROOT}`\n")

    md.append("## Python & Packages\n")
    md.append("```\n" + py_info() + "\n```")

    md.append("\n## File Tree (filtered)\n")
    md.append(list_tree(PROJECT_ROOT))

    # data/raw hızlı görünüm (varsa ilk 10 dosya)
    data_raw = PROJECT_ROOT / "data" / "raw"
    if data_raw.exists():
        md.append("\n## data/raw (first 10 files)\n")
        names = sorted([p.name for p in data_raw.glob("*.csv")])[:10]
        md.append("```\n" + "\n".join(names) + ("\n" if names else "") + "```")

    md.append("\n## Code Snapshot\n")
    for f in collect_files(PROJECT_ROOT):
        rel = f.relative_to(PROJECT_ROOT)
        lang = f.suffix.lower().lstrip(".")
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            content = f"<<read_error: {e}>>"
        md.append(f"\n### {rel}\n")
        md.append(f"```{lang}\n{content}\n```")
    # --- /Gövde ---

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"OK -> {OUT_MD}")

if __name__ == "__main__":
    main()

```