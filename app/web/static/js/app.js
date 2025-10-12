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
