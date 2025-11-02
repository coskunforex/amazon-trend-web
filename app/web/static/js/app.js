// DEMO / PRO ayrımı
const MODE = document.body.dataset.mode || 'demo';

function applyDemoLimits() {
  if (MODE !== 'demo') return; // sadece demo'da çalışır

  // include/exclude kapat
  const inc = document.querySelector('#include');
  const exc = document.querySelector('#exclude');
  if (inc) { inc.disabled = true; inc.placeholder = "Available in Pro"; }
  if (exc) { exc.disabled = true; exc.placeholder = "Available in Pro"; }

  // hafta sayısını 8 ile sınırla
  const limitWeeks = () => {
    const startSel = document.querySelector('#start');
    const endSel = document.querySelector('#end');
    const trim = (sel, keepLastN = 8) => {
      if (!sel) return;
      const opts = Array.from(sel.querySelectorAll('option'));
      const toRemove = opts.slice(0, Math.max(0, opts.length - keepLastN));
      toRemove.forEach(o => o.remove());
    };
    trim(startSel, 8);
    trim(endSel, 8);
  };

  setTimeout(limitWeeks, 0);
}

// ---------------- NEW: Preloader helper ----------------
function hidePreloader() {
  const el = document.getElementById('preloader');
  if (el && !el.classList.contains('hidden')) {
    el.classList.add('hidden');
  }
}

// app/web/static/js/app.js

const $ = (sel)=>document.querySelector(sel);

const startSel = $("#start"), endSel = $("#end");
const includeInp = $("#include"), excludeInp = $("#exclude");
const runBtn = $("#run");
const reindexBtn = $("#reindex");                 // may be null
const tbody = $("#tbl tbody"), found = $("#found");
const emptyEl = $("#empty");                      // may be null
const rangePill = $("#range") || $("#rangeBadge");// support both ids
const statusEl = $("#status");                    // may be null

const modal = $("#modal"), closeModalBtn = $("#closeModal"), chartEl = $("#chart");
const toast = $("#toast");                        // may be null

let weeks = [];
let lastFocusedBeforeModal = null;
let currentSort = { key: "total_improvement", dir: "desc" };

/* ---------- helpers ---------- */
function showToast(msg, ms=2600){
  if(!toast) { console.warn(msg); return; }
  toast.textContent = msg;
  toast.classList.remove("hidden");
  setTimeout(()=>toast.classList.add("hidden"), ms);
}

async function fetchJSON(url){
  const res = await fetch(url);
  if(!res.ok){
    const t = await res.text().catch(()=>res.statusText);
    throw new Error(`${res.status} ${res.statusText} - ${t}`);
  }
  return res.json();
}

function setLoading(on){
  if(statusEl){
    statusEl.classList.toggle("hidden", !on);
    statusEl.setAttribute("aria-hidden", on ? "false":"true");
  }
  if(runBtn) runBtn.disabled = on;
  if(reindexBtn) reindexBtn.disabled = on;
}

function persistFilters(){
  const data = {
    start: startSel.value, end: endSel.value,
    include: includeInp.value, exclude: excludeInp.value
  };
  localStorage.setItem("atf.filters", JSON.stringify(data));
}
function restoreFilters(){
  const raw = localStorage.getItem("atf.filters");
  if(!raw) return;
  try{
    const d = JSON.parse(raw);
    if(d.start) startSel.value = String(d.start);
    if(d.end) endSel.value = String(d.end);
    if(d.include!=null) includeInp.value = d.include;
    if(d.exclude!=null) excludeInp.value = d.exclude;
  }catch{}
}

/* ---------- weeks ---------- */
async function loadWeeks(){
  setLoading(true);
  try{
    weeks = await fetchJSON("/weeks");
    startSel.innerHTML = ""; endSel.innerHTML = "";
    for(const w of weeks){
      const o1 = document.createElement("option"); o1.value = w.weekId; o1.textContent = `Week ${w.label}`;
      const o2 = document.createElement("option"); o2.value = w.weekId; o2.textContent = `Week ${w.label}`;
      startSel.appendChild(o1); endSel.appendChild(o2);
    }
    if(weeks.length >= 2){
      startSel.value = weeks[Math.max(0, weeks.length-6)].weekId; // default: last 6 weeks window
      endSel.value = weeks[weeks.length-1].weekId;
    }
    restoreFilters();

    // ---------------- NEW: weeks başarıyla yüklendi -> preloader'ı kapat ----------------
    hidePreloader();

  }catch(err){
    showToast("Failed to load weeks.");
    console.error(err);
    // hata durumunda da kullanıcı kilitlenmesin diye:
    hidePreloader();
  }finally{
    setLoading(false);
  }
}

function parseWeeks(){
  let s = parseInt(startSel.value,10), e = parseInt(endSel.value,10);
  if(!s || !e) throw new Error("Please select start and end week.");
  if(e < s){ const t=s; s=e; e=t; }
  if((e - s + 1) < 2) throw new Error("Range must be at least 2 weeks.");

  const sLabel = weeks.find(w=>w.weekId===s)?.label || s;
  const eLabel = weeks.find(w=>w.weekId===e)?.label || e;
  const total = (e - s + 1);
  return { s, e, sLabel, eLabel, total };
}

/* ---------- query ---------- */
async function runQuery(){
  try{
    setLoading(true);
    const { s, e, sLabel, eLabel, total } = parseWeeks();
    if(rangePill) rangePill.textContent = `${total} weeks • ${sLabel} → ${eLabel}`;

    const norm = str => str.replaceAll(",", " ").trim();
    const params = new URLSearchParams({
      startWeekId: s, endWeekId: e,
      include: norm(includeInp.value),
      exclude: norm(excludeInp.value),
    });

    const rows = await fetchJSON("/uptrends?" + params.toString());
    const sorted = sortRows(rows, currentSort.key, currentSort.dir);
    renderTable(sorted, s, e);
    persistFilters();

    // (opsiyonel) ilk sorgu da bitince kapatmayı garanti altına al
    hidePreloader();

  }catch(err){
    showToast(err.message);
    console.error(err);
    hidePreloader();
  }finally{
    setLoading(false);
  }
}

function sortRows(rows, key, dir){
  const mul = dir === "desc" ? -1 : 1;
  return [...rows].sort((a,b)=>{
    let va = a[key], vb = b[key];
    const na = typeof va === "number", nb = typeof vb === "number";
    if(na && nb) return (va - vb) * mul;
    return String(va).localeCompare(String(vb)) * mul;
  });
}

function renderTable(rows, s, e){
  tbody.innerHTML = "";
  found.textContent = `Found: ${rows.length}`;
  if(emptyEl) emptyEl.classList.toggle("hidden", rows.length>0);

  for(const r of rows){
    const tr = document.createElement("tr");
    tr.tabIndex = 0;
    tr.innerHTML = `
      <td>${r.term}</td>
      <td>${r.start_rank}</td>
      <td>${r.end_rank}</td>
      <td>${r.total_improvement}</td>
      <td>${r.weeks}</td>
    `;
    const open = ()=>showSeries(r.term, s, e);
    tr.addEventListener("click", open);
    tr.addEventListener("keydown", (ev)=>{ if(ev.key==="Enter" || ev.key===" ") { ev.preventDefault(); open(); }});
    tbody.appendChild(tr);
  }
}

/* ---------- series + chart ---------- */
async function showSeries(term, s, e){
  try{
    setLoading(true);
    const params = new URLSearchParams({ term, startWeekId: s, endWeekId: e });
    const data = await fetchJSON("/series?" + params.toString());
    drawMiniChart(term, data);
    openModal();
  }catch(err){
    showToast("Failed to load series.");
    console.error(err);
  }finally{
    setLoading(false);
  }
}

function drawMiniChart(title, data){
  // y axis reversed (smaller rank = better)
  const ranks = data.map(d=>d.rank).filter(v=>Number.isFinite(v));
  const minR = ranks.length ? Math.min(...ranks) : 0;
  const maxR = ranks.length ? Math.max(...ranks) : 1;

  const pad = 24, W = 740, H = 260;
  const y = (v)=> {
    const t = (v - minR) / Math.max(1, (maxR - minR));
    return pad + (H - 2*pad) * t;
  };
  const x = (i)=> pad + (W - 2*pad) * (i/(Math.max(1, data.length-1)));

  const pts = data.map((d,i)=>{
    const rr = Number.isFinite(d.rank) ? d.rank : null;
    return { x:x(i), y: rr!==null? y(rr): null, label:d.weekLabel, rank: rr };
  });

  let path = "";
  for(let i=0;i<pts.length;i++){
    const p = pts[i];
    if(p.y===null) continue;
    path += (path===""? `M ${p.x} ${p.y}` : ` L ${p.x} ${p.y}`);
  }

  const svg = `
  <svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${title} rank chart">
    <g class="axis">
      <line x1="${pad}" y1="${pad}" x2="${pad}" y2="${H-pad}" />
      <line x1="${pad}" y1="${H-pad}" x2="${W-pad}" y2="${H-pad}" />
      <text x="${pad}" y="${pad-6}">${minR}</text>
      <text x="${pad}" y="${H-pad+16}">${data[0]?.weekLabel||""}</text>
      <text x="${W-pad-80}" y="${H-pad+16}">${data[data.length-1]?.weekLabel||""}</text>
      <text x="${pad}" y="${H-pad+30}" fill="#0f172a">${title}</text>
    </g>
    <path class="line" d="${path}"/>
    ${pts.map(p => p.y===null? "" : `<circle class="dot" cx="${p.x}" cy="${p.y}" r="3"><title>${p.label} • rank ${p.rank}</title></circle>`).join("")}
  </svg>`;
  $("#modalTitle").textContent = title;
  chartEl.innerHTML = svg;
}

/* ---------- modal a11y ---------- */
function openModal(){
  lastFocusedBeforeModal = document.activeElement;
  modal.classList.remove("hidden");
  closeModalBtn && closeModalBtn.focus();
  document.addEventListener("keydown", escClose);
  document.addEventListener("focus", trapFocus, true);
}
function closeModal(){
  modal.classList.add("hidden");
  document.removeEventListener("keydown", escClose);
  document.removeEventListener("focus", trapFocus, true);
  if(lastFocusedBeforeModal) lastFocusedBeforeModal.focus();
}
function escClose(e){ if(e.key==="Escape") closeModal(); }
function trapFocus(e){
  if(modal.classList.contains("hidden")) return;
  if(!modal.contains(e.target)){
    e.stopPropagation();
    closeModalBtn && closeModalBtn.focus();
  }
}

/* ---------- events ---------- */
runBtn && runBtn.addEventListener("click", runQuery);

// reindex button is optional; guard it
if (reindexBtn) {
  reindexBtn.addEventListener("click", async ()=>{
    try{
      setLoading(true);
      await fetchJSON("/reindex");
      await loadWeeks();
      showToast("Reindex completed.");
    }catch(err){
      showToast("Reindex failed.");
      console.error(err);
    }finally{
      setLoading(false);
    }
  });
}

closeModalBtn && closeModalBtn.addEventListener("click", closeModal);
modal.addEventListener("click",(e)=>{ if(e.target===modal) closeModal(); });

document.addEventListener("keydown",(e)=>{
  if((e.ctrlKey || e.metaKey) && e.key.toLowerCase()==="enter"){ runQuery(); }
});

/* sortable headers (data-key attrs must exist) */
document.querySelectorAll("#tbl thead th").forEach(th=>{
  th.addEventListener("click", ()=>{
    const key = th.dataset.key;
    if(!key) return;
    currentSort = {
      key,
      dir: (currentSort.key===key && currentSort.dir==="asc") ? "desc" : "asc"
    };
    const rows = Array.from(tbody.querySelectorAll("tr")).map(tr=>{
      const [term, s, e, imp, w] = Array.from(tr.children).map(td=>td.textContent);
      return {
        term,
        start_rank: Number(s), end_rank: Number(e),
        total_improvement: Number(imp), weeks: Number(w)
      };
    });
    const { s, e } = parseWeeks();
    const sorted = sortRows(rows, currentSort.key, currentSort.dir);
    renderTable(sorted, s, e);
  });
});

/* persist filters */
[startSel, endSel, includeInp, excludeInp].forEach(el=>{
  el.addEventListener("change", persistFilters);
  el.addEventListener("input", persistFilters);
});

/* init */
loadWeeks()
  .then(() => { applyDemoLimits(); })
  .then(runQuery)
  .catch(console.error);

// ---------------- NEW: ekstra güvence (tam sayfa yüklendiğinde de kapat) -------------
window.addEventListener('load', hidePreloader);
