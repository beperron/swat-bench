#!/usr/bin/env python3
"""Generate interactive SWAT-Bench results HTML (standalone)."""

import json
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RESULTS_DIR = os.path.join(BASE, "results", "qwen")
TASKS_DIR = os.path.join(BASE, "tasks")
OUTPUT = os.path.join(BASE, "results", "SWAT-Bench_Results.html")

MODELS = [
    ("Qwen3.5-9B Q4", "qwen3.5-9b-q4", "9.7B", "9.7B", "Dense", "Q4_K_M", 6.6),
    ("Qwen3.5-9B Q8", "qwen3.5-9b-q8", "9.7B", "9.7B", "Dense", "Q8_0", 10.0),
    ("Qwen3.5-27B", "qwen3.5-27b-q4", "27.8B", "27.8B", "Dense", "Q4_K_M", 17.0),
    ("Qwen3-Coder-30B", "qwen3-coder-30b-q4", "30.5B", "3.3B", "MoE 128/8", "Q4_K_M", 18.0),
    ("Qwen3.5-35B-A3B", "qwen3.5-35b-q4", "36.0B", "3.0B", "MoE 256/8+1", "Q4_K_M", 23.0),
    ("Qwen3-Coder-Next", "qwen3-coder-next-q4", "79.7B", "3.0B", "Hybrid MoE 512/10+1", "Q4_K_M", 51.0),
    ("Qwen3.5-122B-A10B", "qwen3.5-122b-q4", "125.1B", "10.0B", "MoE 256/8+1", "Q4_K_M", 81.0),
]

DOMAIN_ORDER = [
    "Data Cleaning & Validation",
    "Data Preparation & Transformation",
    "Descriptive Statistics & Measurement",
    "Inferential Statistics",
    "Applied Social Work Analytics",
    "Text & Natural Language Processing",
]


def find_run_dir(prefix):
    for name in sorted(os.listdir(RESULTS_DIR)):
        if name.startswith(prefix + "_") and os.path.isdir(os.path.join(RESULTS_DIR, name)):
            if "seed" in name and "seed" not in prefix:
                continue
            return name
    return None


def load_data():
    # Task metadata
    task_meta = {}
    for task_dir in sorted(os.listdir(TASKS_DIR)):
        checks_path = os.path.join(TASKS_DIR, task_dir, "expected", "checks.json")
        if not os.path.isfile(checks_path):
            continue
        with open(checks_path) as f:
            data = json.load(f)
        task_meta[task_dir] = {
            "test_id": data.get("test_id", task_dir),
            "task_name": data.get("task_name", task_dir),
            "domain": data.get("domain", "Unknown"),
            "difficulty": data.get("difficulty", "Unknown"),
            "total_points": data.get("total_points", 0),
            "num_checks": len(data.get("checks", [])),
        }

    # Order tasks by domain
    ordered = []
    for domain in DOMAIN_ORDER:
        dt = [(tid, m) for tid, m in task_meta.items() if m["domain"] == domain]
        dt.sort(key=lambda x: x[0])
        ordered.extend(dt)
    task_ids = [t[0] for t in ordered]

    all_models = []
    for display, prefix, total_p, active_p, arch, quant, size_gb in MODELS:
        run_dir = find_run_dir(prefix)
        if not run_dir:
            continue

        # Parse run log for totals
        log_path = os.path.join(RESULTS_DIR, f"{prefix}_run.log")
        run_time = 0
        run_tokens = 0
        run_tools = 0
        if os.path.isfile(log_path):
            with open(log_path) as f:
                for line in f:
                    if "TOTAL" in line and "/" in line and "s " in line:
                        parts = line.split()
                        for i, p in enumerate(parts):
                            if p.endswith("s") and "/" not in p and "." in p:
                                try:
                                    run_time = float(p[:-1])
                                except ValueError:
                                    pass
                            if p.replace(",", "").isdigit() and i > 2:
                                val = int(p.replace(",", ""))
                                if val > 100000:
                                    run_tokens = val
                                    break

        tasks = []
        for tid in task_ids:
            tm = task_meta[tid]
            score_path = os.path.join(RESULTS_DIR, run_dir, tid, "auto_score.json")
            meta_path = os.path.join(RESULTS_DIR, run_dir, tid, "run_meta.json")

            entry = {
                "id": tm["test_id"],
                "name": tm["task_name"],
                "domain": tm["domain"],
                "diff": tm["difficulty"],
                "max": tm["total_points"],
                "earned": 0,
                "pct": 0,
                "cp": 0,
                "ct": tm["num_checks"],
                "time": 0,
                "tokens": 0,
                "tools": 0,
                "checks": [],
            }

            if os.path.isfile(score_path):
                with open(score_path) as f:
                    sd = json.load(f)
                earned = sum(c.get("score", 0) for c in sd.get("checks", []))
                passed = sum(1 for c in sd.get("checks", []) if c.get("passed", False))
                entry["earned"] = earned
                entry["pct"] = round(earned / tm["total_points"], 4) if tm["total_points"] > 0 else 0
                entry["cp"] = passed
                entry["checks"] = [
                    {"l": c.get("label", ""), "p": c.get("passed", False),
                     "s": c.get("score", 0), "m": c.get("points", 0),
                     "d": c.get("detail", "")}
                    for c in sd.get("checks", [])
                ]

            if os.path.isfile(meta_path):
                with open(meta_path) as f:
                    md = json.load(f)
                entry["time"] = round(md.get("duration_seconds", 0), 1)
                tok = md.get("tokens", {})
                entry["tokens"] = tok.get("total", 0) if isinstance(tok, dict) else 0
                tools = md.get("tools", {})
                entry["tools"] = tools.get("total_calls", 0) if isinstance(tools, dict) else 0

            tasks.append(entry)

        te = sum(t["earned"] for t in tasks)
        tp = sum(t["max"] for t in tasks)

        all_models.append({
            "name": display,
            "prefix": prefix,
            "tp": total_p,
            "ap": active_p,
            "arch": arch,
            "q": quant,
            "gb": size_gb,
            "earned": te,
            "possible": tp,
            "pct": round(te / tp * 100, 1) if tp > 0 else 0,
            "time": run_time,
            "tokens": run_tokens,
            "tools": run_tools,
            "tasks": tasks,
        })

    return {"models": all_models, "domains": DOMAIN_ORDER}


def build_html(data):
    json_str = json.dumps(data, separators=(",", ":"))

    # Use placeholder replacement instead of f-string to avoid {{}} escaping issues in JS
    template = _HTML_TEMPLATE.replace("__DATA_PLACEHOLDER__", json_str)
    return template


_HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SWAT-Bench Results</title>
<style>
:root {
  --bg: #0f1117; --surface: #1a1d27; --surface2: #242836; --border: #2e3345;
  --text: #e4e6ed; --text-dim: #8b90a0; --accent: #6c8cff; --accent2: #4ecdc4;
  --green: #22c55e; --yellow: #eab308; --orange: #f97316; --red: #ef4444;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; background:var(--bg); color:var(--text); min-height:100vh; }

/* Header: title left, stats right, single row */
.header { display:flex; align-items:center; justify-content:space-between; padding:20px 32px; border-bottom:1px solid var(--border); background:linear-gradient(180deg,#151821,var(--bg)); flex-wrap:wrap; gap:12px; }
.header-left h1 { font-size:22px; font-weight:700; letter-spacing:-0.5px; }
.header-left h1 span { color:var(--accent); }
.header-left .sub { color:var(--text-dim); font-size:12px; margin-top:2px; }
.header-stats { display:flex; gap:18px; flex-wrap:wrap; }
.stat { display:flex; align-items:baseline; gap:4px; }
.stat .v { font-size:16px; font-weight:700; color:var(--accent2); }
.stat .l { font-size:10px; color:var(--text-dim); text-transform:uppercase; letter-spacing:.4px; }

/* Tabs */
.tabs { display:flex; border-bottom:1px solid var(--border); background:var(--surface); }
.tab { padding:9px 20px; cursor:pointer; font-size:13px; font-weight:500; color:var(--text-dim); border-bottom:2px solid transparent; transition:all .15s; }
.tab:hover { color:var(--text); }
.tab.active { color:var(--accent); border-bottom-color:var(--accent); }
.panel { display:none; padding:16px 32px 40px; }
.panel.active { display:block; }

/* Toolbar: filters left, legend right, single row */
.toolbar { display:flex; align-items:center; justify-content:space-between; padding:10px 0; flex-wrap:wrap; gap:8px; }
.toolbar-left { display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
.toolbar-left label { font-size:10px; color:var(--text-dim); text-transform:uppercase; letter-spacing:.5px; font-weight:600; }
.toolbar-right { display:flex; align-items:center; gap:6px; }
.legend-group { display:flex; align-items:center; gap:6px; }
.legend-group-label { font-size:9px; color:var(--text-dim); text-transform:uppercase; letter-spacing:.6px; font-weight:600; white-space:nowrap; }
.btn-group { display:flex; border-radius:6px; overflow:hidden; border:1px solid var(--border); }
.btn-group button { padding:4px 11px; background:var(--surface); color:var(--text-dim); border:none; cursor:pointer; font-size:11px; font-weight:500; transition:all .15s; }
.btn-group button:not(:last-child) { border-right:1px solid var(--border); }
.btn-group button.active { background:var(--accent); color:white !important; }
.btn-group button:hover:not(.active) { background:var(--surface2); color:var(--text); }

/* Heatmap layout: heatmap left, scorecards right */
.hm-layout { display:flex; gap:20px; align-items:flex-start; }
@media(max-width:1400px) { .hm-layout { flex-direction:column; } }

/* Scorecards sidebar */
.scorecards { flex-shrink:0; width:220px; display:flex; flex-direction:column; gap:8px; }
@media(max-width:1400px) { .scorecards { flex-direction:row; flex-wrap:wrap; width:100%; } .scorecard { flex:1; min-width:180px; } }
.scorecard { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:12px 14px; }
.sc-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
.sc-name { font-size:11px; font-weight:700; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:130px; }
.sc-pct { font-size:16px; font-weight:800; }
.sc-bar { width:100%; height:4px; background:var(--surface2); border-radius:2px; margin-bottom:8px; overflow:hidden; }
.sc-bar-fill { height:100%; border-radius:2px; }
.sc-stats { display:grid; grid-template-columns:1fr 1fr; gap:4px 8px; }
.sc-stat { display:flex; flex-direction:column; }
.sc-stat .sc-v { font-size:11px; font-weight:600; }
.sc-stat .sc-l { font-size:8px; color:var(--text-dim); text-transform:uppercase; letter-spacing:.4px; }

/* Heatmap (tasks=rows, models=cols) */
.hm-wrap { overflow-x:auto; overflow-y:visible; flex:1; min-width:0; }
.hm-table { border-collapse:separate; border-spacing:2px; }
.hm-table th { padding:6px 4px; font-size:10px; font-weight:600; color:var(--text-dim); text-transform:uppercase; letter-spacing:.3px; white-space:nowrap; }
.hm-table th.model-col { min-width:54px; width:54px; writing-mode:vertical-lr; text-orientation:mixed; transform:rotate(180deg); padding:8px 2px; height:140px; text-align:left; font-size:11px; }
.hm-table td.task-label { padding:4px 10px 4px 4px; font-size:11px; white-space:nowrap; text-align:right; font-weight:500; }
.hm-table td.domain-row { padding:6px 10px; font-size:11px; font-weight:700; color:var(--accent); text-transform:uppercase; letter-spacing:.5px; background:var(--surface); border-radius:4px; }
.hm-cell { width:54px; min-width:54px; height:30px; border-radius:3px; text-align:center; vertical-align:middle; font-size:9.5px; font-weight:600; cursor:pointer; transition:all .12s; position:relative; }
.hm-cell:hover { transform:scale(1.2); z-index:10; box-shadow:0 4px 16px rgba(0,0,0,.6); }
.pts-col { text-align:center; font-size:10px; color:var(--text-dim); padding:4px 6px; }
.diff-F { color:#60a5fa; } .diff-I { color:#a78bfa; } .diff-A { color:#f472b6; }

/* Tooltip */
.tooltip { display:none; position:fixed; z-index:1000; background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:14px; min-width:300px; max-width:380px; box-shadow:0 12px 40px rgba(0,0,0,.6); pointer-events:none; }
.tooltip.visible { display:block; }
.tt-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; padding-bottom:6px; border-bottom:1px solid var(--border); }
.tt-task { font-size:13px; font-weight:700; }
.tt-score { font-size:16px; font-weight:800; }
.tt-meta { font-size:10px; color:var(--text-dim); margin-bottom:8px; }
.check-row { display:flex; align-items:center; gap:6px; padding:2px 0; font-size:10px; }
.ck-icon { width:14px; height:14px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:9px; flex-shrink:0; }
.ck-icon.pass { background:rgba(34,197,94,.2); color:var(--green); }
.ck-icon.fail { background:rgba(239,68,68,.2); color:var(--red); }
.ck-label { flex:1; color:var(--text-dim); }
.ck-pts { font-weight:600; min-width:36px; text-align:right; }

/* Scatter */
.scatter-grid { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-top:16px; }
@media(max-width:1100px) { .scatter-grid { grid-template-columns:1fr; } }
.scatter-card { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:20px; }
.scatter-card h3 { font-size:14px; font-weight:600; margin-bottom:12px; }
.scatter-card canvas { width:100% !important; height:300px !important; }

/* Summary table */
.summary-table { width:100%; border-collapse:collapse; font-size:12px; margin-top:16px; }
.summary-table th { text-align:left; padding:8px 10px; background:var(--surface); color:var(--text-dim); font-size:10px; text-transform:uppercase; letter-spacing:.5px; font-weight:600; border-bottom:2px solid var(--border); }
.summary-table th.r,.summary-table td.r { text-align:right; }
.summary-table td { padding:8px 10px; border-bottom:1px solid var(--border); }
.summary-table tr:hover td { background:rgba(108,140,255,.04); }
.pct-bar { width:70px; height:5px; background:var(--surface2); border-radius:3px; overflow:hidden; display:inline-block; vertical-align:middle; margin-left:6px; }
.pct-fill { height:100%; border-radius:3px; }

/* Legend (inline, inside toolbar-right) */
.legend-item { display:flex; align-items:center; gap:4px; font-size:10px; color:var(--text-dim); }
.legend-swatch { width:10px; height:10px; border-radius:2px; flex-shrink:0; }
.legend-sep { width:1px; height:20px; background:var(--border); margin:0 8px; }
.color-bar { width:72px; height:8px; border-radius:2px; background:linear-gradient(90deg,#dc2626,#f97316,#eab308,#84cc16,#22c55e,#059669); }
.color-bar-label { font-size:9px; color:var(--text-dim); }
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <h1><span>SWAT-Bench</span> Preliminary Results</h1>
    <div class="sub">Single-run benchmark &mdash; March 2026</div>
  </div>
  <div class="header-stats" id="statsBar"></div>
</div>
<div class="tabs">
  <div class="tab active" data-panel="heatmapPanel">Heatmap</div>
  <div class="tab" data-panel="scatterPanel">Comparisons</div>
  <div class="tab" data-panel="tablePanel">Summary Table</div>
</div>
<div class="panel active" id="heatmapPanel">
  <div class="toolbar" id="hmToolbar"></div>
  <div class="hm-layout">
    <div class="hm-wrap" id="hmWrap"></div>
    <div class="scorecards" id="scorecards"></div>
  </div>
</div>
<div class="panel" id="scatterPanel">
  <div class="scatter-grid" id="scatterGrid"></div>
</div>
<div class="panel" id="tablePanel">
  <div id="summaryTable"></div>
</div>
<div class="tooltip" id="tooltip"></div>

<script>
const D = __DATA_PLACEHOLDER__;

const DS = {"Data Cleaning & Validation":"D1: Cleaning","Data Preparation & Transformation":"D2: Preparation","Descriptive Statistics & Measurement":"D3: Descriptive","Inferential Statistics":"D4: Inferential","Applied Social Work Analytics":"D5: Applied","Text & Natural Language Processing":"D6: NLP"};
const DC = {"Data Cleaning & Validation":"#6c8cff","Data Preparation & Transformation":"#4ecdc4","Descriptive Statistics & Measurement":"#a78bfa","Inferential Statistics":"#f472b6","Applied Social Work Analytics":"#fb923c","Text & Natural Language Processing":"#34d399"};
const MC = ["#6c8cff","#4ecdc4","#a78bfa","#f472b6","#fb923c","#34d399","#f87171"];

let hMode="fraction", hDiff="all";

function sColor(p) { return p>=.95?"#059669":p>=.85?"#22c55e":p>=.7?"#84cc16":p>=.5?"#eab308":p>=.25?"#f97316":"#dc2626"; }
function tColor(p) { return (p>=.85||p<.25)?"#fff":"#1a1d27"; }
function timeColor(s) { return s>600?"#dc2626":s>300?"#f97316":s>120?"#eab308":"#22c55e"; }
function tokColor(t) { return t>500000?"#dc2626":t>200000?"#f97316":t>100000?"#eab308":"#22c55e"; }
function fmtTime(s) { if(!s)return"\u2014"; const m=Math.floor(s/60),sec=Math.round(s%60); return m>0?m+"m "+sec+"s":sec+"s"; }
function fmtTok(n) { if(!n)return"\u2014"; return n>=1e6?(n/1e6).toFixed(1)+"M":n>=1e3?Math.round(n/1e3)+"K":n; }
function badgeStyle(p) { return p>=98?"background:rgba(5,150,105,.2);color:#22c55e":p>=95?"background:rgba(34,197,94,.2);color:#22c55e":p>=90?"background:rgba(132,204,22,.2);color:#84cc16":"background:rgba(234,179,8,.2);color:#eab308"; }

// Stats bar (compact, in header)
(function() {
  const b=D.models.reduce((a,b)=>a.pct>b.pct?a:b);
  const tp=D.models[0].tasks.reduce((s,t)=>s+t.max,0);
  document.getElementById("statsBar").innerHTML=`
    <div class="stat"><span class="v">${D.models.length}</span><span class="l">Models</span></div>
    <div class="stat"><span class="v">${D.models[0].tasks.length}</span><span class="l">Tasks</span></div>
    <div class="stat"><span class="v">${tp}</span><span class="l">Points</span></div>
    <div class="stat"><span class="v">${b.pct}%</span><span class="l">Best</span></div>`;
})();

// Scorecards
(function() {
  const el=document.getElementById("scorecards");
  let h="";
  // Sort by score descending for ranking
  const ranked=D.models.slice().sort((a,b)=>b.pct-a.pct);
  for(let i=0;i<ranked.length;i++) {
    const m=ranked[i];
    const sc=sColor(m.pct/100);
    const perfect=m.tasks.filter(t=>t.pct>=1).length;
    const tp=m.tasks.reduce((s,t)=>s+t.max,0);
    h+=`<div class="scorecard">
      <div class="sc-header">
        <span class="sc-name" title="${m.name}">${m.name}</span>
        <span class="sc-pct" style="color:${sc}">${m.pct}%</span>
      </div>
      <div class="sc-bar"><div class="sc-bar-fill" style="width:${m.pct}%;background:${sc}"></div></div>
      <div class="sc-stats">
        <div class="sc-stat"><span class="sc-v">${m.earned}/${tp}</span><span class="sc-l">Score</span></div>
        <div class="sc-stat"><span class="sc-v">${perfect}/${m.tasks.length}</span><span class="sc-l">Perfect</span></div>
        <div class="sc-stat"><span class="sc-v">${fmtTime(m.time)}</span><span class="sc-l">Time</span></div>
        <div class="sc-stat"><span class="sc-v">${fmtTok(m.tokens)}</span><span class="sc-l">Tokens</span></div>
      </div>
    </div>`;
  }
  el.innerHTML=h;
})();

// Tabs
document.querySelectorAll(".tab").forEach(t=>t.addEventListener("click",()=>{
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"));
  document.querySelectorAll(".panel").forEach(x=>x.classList.remove("active"));
  t.classList.add("active");
  document.getElementById(t.dataset.panel).classList.add("active");
  if(t.dataset.panel==="scatterPanel") renderScatter();
}));

// Unified toolbar: filters left, legend right
document.getElementById("hmToolbar").innerHTML=`
  <div class="toolbar-left">
    <label>Display</label>
    <div class="btn-group" id="dispMode">
      <button class="active" data-m="fraction">Score</button>
      <button data-m="pct">%</button>
      <button data-m="passfail">Pass/Fail</button>
      <button data-m="time">Time</button>
      <button data-m="tokens">Tokens</button>
    </div>
    <label>Difficulty</label>
    <div class="btn-group" id="diffFilt">
      <button class="active" data-d="all">All</button>
      <button data-d="Foundational" style="color:#60a5fa">Foundational</button>
      <button data-d="Intermediate" style="color:#a78bfa">Intermediate</button>
      <button data-d="Advanced" style="color:#f472b6">Advanced</button>
    </div>
  </div>
  <div class="toolbar-right" id="colorLegend"></div>`;
function updateLegend() {
  const el=document.getElementById("colorLegend");
  if(hMode==="time") {
    el.innerHTML=`<div class="legend-group"><span class="legend-group-label">Time</span>
      <div class="legend-item"><div class="legend-swatch" style="background:#22c55e"></div>&lt; 2m</div>
      <div class="legend-item"><div class="legend-swatch" style="background:#eab308"></div>2\u20135m</div>
      <div class="legend-item"><div class="legend-swatch" style="background:#f97316"></div>5\u201310m</div>
      <div class="legend-item"><div class="legend-swatch" style="background:#dc2626"></div>&gt; 10m</div></div>`;
  } else if(hMode==="tokens") {
    el.innerHTML=`<div class="legend-group"><span class="legend-group-label">Tokens</span>
      <div class="legend-item"><div class="legend-swatch" style="background:#22c55e"></div>&lt; 100K</div>
      <div class="legend-item"><div class="legend-swatch" style="background:#eab308"></div>100\u2013200K</div>
      <div class="legend-item"><div class="legend-swatch" style="background:#f97316"></div>200\u2013500K</div>
      <div class="legend-item"><div class="legend-swatch" style="background:#dc2626"></div>&gt; 500K</div></div>`;
  } else {
    el.innerHTML=`<div class="legend-group"><span class="legend-group-label">Score</span>
      <span class="color-bar-label">0%</span><div class="color-bar"></div><span class="color-bar-label">100%</span></div>`;
  }
}
updateLegend();
document.getElementById("dispMode").addEventListener("click",e=>{if(e.target.tagName!=="BUTTON")return;document.querySelectorAll("#dispMode button").forEach(b=>b.classList.remove("active"));e.target.classList.add("active");hMode=e.target.dataset.m;updateLegend();renderHM();});
document.getElementById("diffFilt").addEventListener("click",e=>{if(e.target.tagName!=="BUTTON")return;document.querySelectorAll("#diffFilt button").forEach(b=>b.classList.remove("active"));e.target.classList.add("active");hDiff=e.target.dataset.d;renderHM();});

function renderHM() {
  const models=D.models;
  const tasks=models[0].tasks.filter(t=>hDiff==="all"||t.diff===hDiff);
  const nM=models.length, nT=tasks.length;

  // Build task index map for filtered tasks
  const taskIdx = tasks.map(t=>models[0].tasks.indexOf(t));

  let h='<table class="hm-table"><thead><tr><th style="min-width:180px"></th><th class="pts-col">Pts</th>';
  for(const m of models) h+=`<th class="model-col">${m.name}</th>`;
  h+='</tr></thead><tbody>';

  let lastDom="";
  for(let ti=0;ti<nT;ti++) {
    const t0=tasks[ti];
    const origIdx=taskIdx[ti];
    // Domain separator row
    if(t0.domain!==lastDom) {
      lastDom=t0.domain;
      const short=DS[t0.domain]||t0.domain;
      const domColor=DC[t0.domain]||"#555";
      h+=`<tr><td class="domain-row" colspan="${nM+2}" style="border-left:3px solid ${domColor}">${short}</td></tr>`;
    }
    const dc=t0.diff==="Foundational"?"diff-F":t0.diff==="Intermediate"?"diff-I":"diff-A";
    h+=`<tr><td class="task-label"><span class="${dc}">${t0.id}</span> ${t0.name}</td>`;
    h+=`<td class="pts-col">${t0.max}</td>`;

    for(let mi=0;mi<nM;mi++) {
      const t=models[mi].tasks[origIdx];
      let bg,fg,txt;
      if(hMode==="time") {
        bg=timeColor(t.time); fg=tColor(t.time>300?0:1);
        txt=t.time>0?(t.time>=60?Math.round(t.time/60)+"m":Math.round(t.time)+"s"):"\u2014";
      } else if(hMode==="tokens") {
        bg=tokColor(t.tokens); fg=tColor(t.tokens>200000?0:1);
        txt=t.tokens>0?fmtTok(t.tokens):"\u2014";
      } else if(hMode==="pct") {
        bg=sColor(t.pct); fg=tColor(t.pct);
        txt=Math.round(t.pct*100)+"%";
      } else if(hMode==="passfail") {
        bg=sColor(t.pct); fg=tColor(t.pct);
        txt=t.pct>=1?"\u2713":t.pct>0?"\u25CB":"\u2717";
      } else {
        bg=sColor(t.pct); fg=tColor(t.pct);
        const e=t.earned===Math.floor(t.earned)?t.earned:t.earned.toFixed(1);
        txt=e+"/"+t.max;
      }
      h+=`<td class="hm-cell" style="background:${bg};color:${fg}" onmouseenter="showTT(event,${mi},${origIdx})" onmouseleave="hideTT()">${txt}</td>`;
    }
    h+='</tr>';
  }
  h+='</tbody></table>';
  document.getElementById("hmWrap").innerHTML=h;

}

function showTT(ev,mi,ti) {
  const m=D.models[mi], t=m.tasks[ti];
  const sc=sColor(t.pct);
  let ch="";
  for(const c of t.checks) {
    const ic=c.p?'<div class="ck-icon pass">\u2713</div>':'<div class="ck-icon fail">\u2717</div>';
    ch+=`<div class="check-row">${ic}<span class="ck-label">${c.l}</span><span class="ck-pts">${c.s}/${c.m}</span></div>`;
  }
  const tt=document.getElementById("tooltip");
  tt.innerHTML=`
    <div class="tt-header"><div class="tt-task">${t.id}: ${t.name}</div><div class="tt-score" style="color:${sc}">${t.earned}/${t.max}</div></div>
    <div class="tt-meta"><strong>${m.name}</strong> &middot; ${t.domain}<br>
    Difficulty: <span style="color:${t.diff==='Foundational'?'#60a5fa':t.diff==='Intermediate'?'#a78bfa':'#f472b6'}">${t.diff}</span>
    &middot; Time: ${fmtTime(t.time)} &middot; Tokens: ${fmtTok(t.tokens)} &middot; Tools: ${t.tools}</div>
    ${ch}`;
  tt.classList.add("visible");
  const r=tt.getBoundingClientRect();
  let x=ev.clientX+14, y=ev.clientY-16;
  if(x+r.width>window.innerWidth-16) x=ev.clientX-r.width-14;
  if(y+r.height>window.innerHeight-16) y=window.innerHeight-r.height-16;
  if(y<8) y=8;
  tt.style.left=x+"px"; tt.style.top=y+"px";
}
function hideTT() { document.getElementById("tooltip").classList.remove("visible"); }

// === Scatter Plots (pure canvas, no dependencies) ===
function renderScatter() {
  const grid=document.getElementById("scatterGrid");
  if(grid.children.length>0) return; // already rendered

  const plots=[
    { title:"Score (%) vs Total Parameters", xKey:"tp_num", yKey:"pct", xLabel:"Total Parameters (B)", yLabel:"Score (%)", xFmt:v=>v+"B", yFmt:v=>v+"%" },
    { title:"Score (%) vs Active Parameters", xKey:"ap_num", yKey:"pct", xLabel:"Active Parameters (B)", yLabel:"Score (%)", xFmt:v=>v+"B", yFmt:v=>v+"%" },
    { title:"Score (%) vs Time to Complete", xKey:"time", yKey:"pct", xLabel:"Wall Time (minutes)", yLabel:"Score (%)", xFmt:v=>Math.round(v)+"m", yFmt:v=>v+"%" },
    { title:"Score (%) vs Total Tokens", xKey:"tokens_m", yKey:"pct", xLabel:"Tokens (millions)", yLabel:"Score (%)", xFmt:v=>v.toFixed(1)+"M", yFmt:v=>v+"%" },
    { title:"Score (%) vs Model Size (GB)", xKey:"gb", yKey:"pct", xLabel:"GGUF Size (GB)", yLabel:"Score (%)", xFmt:v=>v+"GB", yFmt:v=>v+"%" },
    { title:"Time (min) vs Total Tokens", xKey:"tokens_m", yKey:"time_m", xLabel:"Tokens (millions)", yLabel:"Time (minutes)", xFmt:v=>v.toFixed(1)+"M", yFmt:v=>Math.round(v)+"m" },
  ];

  const pts=D.models.map((m,i)=>({
    name:m.name,
    pct:m.pct,
    tp_num:parseFloat(m.tp),
    ap_num:parseFloat(m.ap),
    time:m.time,
    time_m:m.time/60,
    tokens_m:m.tokens/1e6,
    gb:m.gb,
    color:MC[i],
    idx:i
  }));

  for(const plot of plots) {
    const card=document.createElement("div");
    card.className="scatter-card";
    card.innerHTML=`<h3>${plot.title}</h3><canvas></canvas>`;
    grid.appendChild(card);
    const canvas=card.querySelector("canvas");
    const ctx=canvas.getContext("2d");

    // Hi-DPI
    const dpr=window.devicePixelRatio||1;
    const rect=canvas.getBoundingClientRect();
    canvas.width=rect.width*dpr;
    canvas.height=300*dpr;
    canvas.style.width=rect.width+"px";
    canvas.style.height="300px";
    ctx.scale(dpr,dpr);

    const W=rect.width, H=300;
    const pad={t:20,r:20,b:44,l:56};
    const pw=W-pad.l-pad.r, ph=H-pad.t-pad.b;

    const xs=pts.map(p=>p[plot.xKey]).filter(v=>v>0);
    const ys=pts.map(p=>p[plot.yKey]).filter(v=>v>0);
    let xMin=Math.min(...xs)*0.9, xMax=Math.max(...xs)*1.1;
    let yMin=Math.min(...ys)*0.95, yMax=Math.max(...ys)*1.03;
    if(plot.yKey==="pct") { yMin=Math.max(85,yMin); yMax=Math.min(100.5,yMax); }

    const sx=v=>(v-xMin)/(xMax-xMin)*pw+pad.l;
    const sy=v=>H-pad.b-(v-yMin)/(yMax-yMin)*ph;

    // Grid
    ctx.strokeStyle="#2e3345"; ctx.lineWidth=0.5;
    for(let i=0;i<=4;i++) {
      const y=pad.t+ph*i/4;
      ctx.beginPath(); ctx.moveTo(pad.l,y); ctx.lineTo(W-pad.r,y); ctx.stroke();
      const val=yMax-(yMax-yMin)*i/4;
      ctx.fillStyle="#8b90a0"; ctx.font="10px Inter,sans-serif"; ctx.textAlign="right";
      ctx.fillText(plot.yFmt(val),pad.l-6,y+3);
    }
    for(let i=0;i<=4;i++) {
      const x=pad.l+pw*i/4;
      ctx.beginPath(); ctx.moveTo(x,pad.t); ctx.lineTo(x,H-pad.b); ctx.stroke();
      const val=xMin+(xMax-xMin)*i/4;
      ctx.fillStyle="#8b90a0"; ctx.font="10px Inter,sans-serif"; ctx.textAlign="center";
      ctx.fillText(plot.xFmt(val),x,H-pad.b+14);
    }

    // Axis labels
    ctx.fillStyle="#8b90a0"; ctx.font="11px Inter,sans-serif";
    ctx.textAlign="center";
    ctx.fillText(plot.xLabel,pad.l+pw/2,H-4);
    ctx.save(); ctx.translate(12,pad.t+ph/2); ctx.rotate(-Math.PI/2);
    ctx.fillText(plot.yLabel,0,0); ctx.restore();

    // Points
    for(const p of pts) {
      const xv=p[plot.xKey], yv=p[plot.yKey];
      if(!xv||!yv) continue;
      const cx=sx(xv), cy=sy(yv);
      // Glow
      ctx.beginPath(); ctx.arc(cx,cy,10,0,Math.PI*2);
      ctx.fillStyle=p.color+"22"; ctx.fill();
      // Dot
      ctx.beginPath(); ctx.arc(cx,cy,5,0,Math.PI*2);
      ctx.fillStyle=p.color; ctx.fill();
      ctx.strokeStyle="#0f1117"; ctx.lineWidth=1.5; ctx.stroke();
      // Label
      ctx.fillStyle="#e4e6ed"; ctx.font="bold 9px Inter,sans-serif"; ctx.textAlign="center";
      ctx.fillText(p.name,cx,cy-10);
    }
  }
}

// Summary table
(function() {
  let h='<table class="summary-table"><tr><th>Model</th><th>Arch</th><th>Total</th><th>Active</th><th>Quant</th><th class="r">Size</th><th class="r">Score</th><th>%</th><th class="r">Time</th><th class="r">Tokens</th></tr>';
  for(const m of D.models) {
    const bc=sColor(m.pct/100);
    const bw=Math.round(m.pct*.8);
    h+=`<tr><td><strong>${m.name}</strong></td><td>${m.arch}</td><td>${m.tp}</td><td>${m.ap}</td><td>${m.q}</td><td class="r">${m.gb}GB</td><td class="r"><strong>${m.earned}/${m.possible}</strong></td><td>${m.pct}%<div class="pct-bar"><div class="pct-fill" style="width:${bw}%;background:${bc}"></div></div></td><td class="r">${fmtTime(m.time)}</td><td class="r">${fmtTok(m.tokens)}</td></tr>`;
  }
  h+='</table>';
  document.getElementById("summaryTable").innerHTML=h;
})();

renderHM();
</script>
</body>
</html>'''


def main():
    data = load_data()
    html = build_html(data)
    with open(OUTPUT, "w") as f:
        f.write(html)
    print(f"Saved: {OUTPUT} ({os.path.getsize(OUTPUT) / 1024:.0f} KB)")
    print(f"Models: {len(data['models'])}, Tasks: {len(data['models'][0]['tasks'])}")


if __name__ == "__main__":
    main()
