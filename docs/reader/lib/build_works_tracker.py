#!/usr/bin/env python3
"""The prophet-period works tracker — a sortable table that is the run-list and
the progress board for the interactive reader editions.

One row per work, assembled from three honest sources and nothing invented:
  - the corpus dives (docs/research/*/dossier.yaml) — title, PSS location, dates,
    period, whether a works/ record exists yet (the gap);
  - the works records (website/src/works/**/<Title>.md frontmatter) — genre, dates,
    and any translation sidecar (.data.yaml, schema §8) once it exists;
  - a small hand-kept status file (docs/reader/status.yaml) for the human-judgment
    loop stages the machine can't see (read · re-dived · ingested).

What the machine CAN see it derives: a work is 'dived' if it has a dossier, and
'built' if its bundle's build/ folder exists. Everything else comes from status.yaml.

The translation columns stay blank until the per-work .data.yaml sidecars are
written (none exist yet) — they are scaffolding for the canonical-translation flag.

Output (tracked; the .gitignore only excludes each bundle's build/):
  docs/reader/index.html

Deterministic: no wall-clock in the page (the 'updated' date is the latest dive
date), so rebuilding without a new dive produces a byte-identical file. Auto-runs
from serve.py's build_all(); also runnable standalone:
  python3 docs/reader/lib/build_works_tracker.py
"""
import argparse
import html
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("build_works_tracker.py: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

# ── Paths ────────────────────────────────────────────────────────────────────
LIB = Path(__file__).parent.resolve()        # …/docs/reader/lib
READER = LIB.parent                           # …/docs/reader
DOCS = READER.parent                          # …/docs
REPO_ROOT = DOCS.parent                       # repo root
RESEARCH = DOCS / "research"
WORKS = REPO_ROOT / "website" / "src" / "works"
STATUS_FILE = READER / "status.yaml"
OUT_NAME = "index.html"                        # docs/reader/index.html


def dive_dossiers():
    """Every dive's dossier.yaml — now nested under works/ and themes/
    (work-dives at works/<genre>/<subcat>/<dive>/, theme-dives at themes/<dive>/;
    _meta/ reference material is excluded by construction)."""
    yield from sorted(RESEARCH.glob("works/*/*/*/dossier.yaml"))
    yield from sorted(RESEARCH.glob("themes/*/dossier.yaml"))

# The loop the editions move through, in order. The first two are derived from
# artifacts on disk; the rest are human-judgment stages set in status.yaml.
LOOP_STAGES = ["dived", "built", "read", "re-dived", "ingested"]
DERIVABLE = {"dived", "built"}


def collapse_ws(s):
    return " ".join((s or "").split())


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def load_yaml(path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}


# ── Reading the heterogeneous dossiers ────────────────────────────────────────

def pluck_field(fields, name):
    """workRecord(.fields) is a list of {field, value, …}; return the named value."""
    if not isinstance(fields, list):
        return None
    for f in fields:
        if isinstance(f, dict) and f.get("field") == name:
            return f.get("value")
    return None


def work_rows_from_dossier(slug, data, dive_href):
    """Yield one row-seed per work a dossier documents. A dossier is one of:
      - single-work: a top-level `work:` block (+ optional `workRecord:`),
      - multi-work:  a `workRecords:` list,
      - neither:     a concept/theme dive — no works, yield nothing."""
    topic = data.get("topic") or {}
    base_period = collapse_ws(topic.get("period"))
    dive_date = str(topic.get("date") or "")

    def seed(work_id, title, record_path, record_exists, pss, dates, genre):
        return {
            "slug": slug, "workId": work_id or "", "title": collapse_ws(title) or work_id or slug,
            "recordPath": record_path or "", "recordExists": bool(record_exists),
            "pss": pss or "", "dates": dates or "", "genre": genre or "",
            "period": base_period, "diveDate": dive_date,
            "diveHref": dive_href,
        }

    work = data.get("work")
    wr = data.get("workRecord")
    wrs = data.get("workRecords")

    if isinstance(work, dict):  # single-work dive: the richest, most uniform source
        pss = _fmt_pss(work.get("pssTom"), work.get("pssPages"))
        dates = _fmt_dates(work.get("compositionStart"), work.get("compositionRoughComplete"))
        genre = None
        if isinstance(wr, dict):
            genre = pluck_field(wr.get("fields"), "genre")
        yield seed(work.get("recordPath", "").rsplit("/", 2)[-2] if work.get("recordPath") else slug,
                   topic.get("title"), work.get("recordPath"),
                   work.get("recordExists"), pss, dates, genre)
        return

    if isinstance(wr, dict):  # a workRecord without a `work:` block
        fields = wr.get("fields")
        yield seed(wr.get("workId"), pluck_field(fields, "titleEn") or topic.get("title"),
                   wr.get("recordPath"), wr.get("action") == "fill",
                   _pss_from_fields(fields), _dates_from_fields(fields),
                   pluck_field(fields, "genre"))
        return

    if isinstance(wrs, list):  # multi-work theme dive: one row per record
        for rec in wrs:
            if not isinstance(rec, dict):
                continue
            fields = rec.get("fields")
            yield seed(rec.get("workId"),
                       pluck_field(fields, "titleEn") or rec.get("workId"),
                       rec.get("recordPath"), rec.get("action") == "fill",
                       _pss_from_fields(fields), _dates_from_fields(fields),
                       pluck_field(fields, "genre"))
        return
    # else: concept/theme/reference dive — no works to list.


def _fmt_pss(tom, pages):
    if not tom:
        return ""
    return f"{tom}: {pages}" if pages else str(tom)


def _fmt_dates(start, rough):
    start, rough = (str(start or "")).strip(), (str(rough or "")).strip()
    if start and rough and rough != start:
        return f"{start} – {rough}"
    return start or rough


def _pss_from_fields(fields):
    ident = pluck_field(fields, "identifiers") or {}
    jub = ident.get("jubileeEdition") if isinstance(ident, dict) else None
    if isinstance(jub, dict) and jub.get("volumes"):
        return f"{jub['volumes']}"
    return ""


def _dates_from_fields(fields):
    return _fmt_dates(pluck_field(fields, "dateWritingStarted"),
                      pluck_field(fields, "dateWritingCompleted"))


# ── Reading the works records (frontmatter) ───────────────────────────────────

def read_frontmatter(path):
    """Return the YAML frontmatter dict of a works .md record."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    return load_yaml_str(text[3:end])


def load_yaml_str(s):
    try:
        d = yaml.safe_load(s)
        return d if isinstance(d, dict) else {}
    except yaml.YAMLError:
        return {}


def all_work_records():
    """workId → {title, genre, category, dates, sidecar?} for every works/ record."""
    out = {}
    if not WORKS.is_dir():
        return out
    for md in WORKS.glob("*/*/*/*.md"):
        if md.stem in ("README", "INDEX") or md.stem.startswith("_"):
            continue
        fm = read_frontmatter(md)
        wid = fm.get("id") or md.parent.name
        sidecar = md.with_suffix(".data.yaml")
        out[wid] = {
            "title": fm.get("titleEn") or fm.get("title") or wid,
            "genre": fm.get("genre") or "",
            "dates": _fmt_dates(fm.get("dateWritingStarted"), fm.get("dateWritingCompleted")),
            "translations": _translations_from_sidecar(sidecar) if sidecar.exists() else ("", ""),
            "recordPath": str(md.relative_to(REPO_ROOT)),
        }
    return out


def _translations_from_sidecar(path):
    """(available, canonical) from translationEditions[] (schema §8). The canonical
    one carries readerDefault: true (the reader-default flag). Empty until sidecars exist."""
    data = load_yaml(path)
    eds = data.get("translationEditions") or []
    if not isinstance(eds, list):
        return "", ""
    en = [e for e in eds if isinstance(e, dict) and (e.get("language") or "").startswith("en")]
    names = [collapse_ws(e.get("translatorName")) or e.get("translatorId") or "" for e in en]
    names = [n for n in names if n]
    canonical = next((collapse_ws(e.get("translatorName")) or e.get("translatorId") or ""
                      for e in en if e.get("readerDefault")), "")
    return ", ".join(names), canonical


# ── Loop status ───────────────────────────────────────────────────────────────

def bundle_dir(record_path):
    """…/works/<cat>/<subcat>/<wid>/… → the work's reader bundle dir, or None."""
    if not record_path:
        return None
    parts = Path(record_path).parts
    if "works" not in parts:
        return None
    i = parts.index("works")
    try:
        cat, subcat, wid = parts[i + 1], parts[i + 2], parts[i + 3]
    except IndexError:
        return None
    return DOCS / "reader" / cat / subcat / wid


def bundle_built(record_path):
    """A work is 'built' if its bundle's build/ folder exists with a segments file."""
    bdir = bundle_dir(record_path)
    if not bdir:
        return False
    build = bdir / "build"
    return build.is_dir() and any(build.glob("segments*.json"))


def overview_href(record_path):
    """Bundle overview page (relative to docs/reader/index.html), or ''."""
    bdir = bundle_dir(record_path)
    if bdir and (bdir / "overview.md").exists():
        return f"{bdir.relative_to(READER).as_posix()}/"
    return ""


def furthest_stage(derived, declared):
    """The furthest-reached stage: the further of what we derived and what status.yaml declares."""
    candidates = [s for s in (derived, declared) if s in LOOP_STAGES]
    if not candidates:
        return ""
    return max(candidates, key=LOOP_STAGES.index)


# ── Assembly ──────────────────────────────────────────────────────────────────

def assemble():
    records = all_work_records()
    status = load_yaml(STATUS_FILE)
    rows, seen = [], set()

    # 1) Every work a dossier documents.
    for dossier in dive_dossiers():
        slug = dossier.parent.name
        data = load_yaml(dossier)
        dive_href = f"/research/{dossier.parent.relative_to(RESEARCH).as_posix()}/index.html"
        for seed in work_rows_from_dossier(slug, data, dive_href):
            rows.append(_finish_row(seed, records, status, dived=True))
            seen.add(seed["workId"])

    # 2) Works that have a record but no dossier referencing them (recorded, not dived).
    for wid, rec in sorted(records.items()):
        if wid in seen:
            continue
        seed = {"slug": "", "workId": wid, "title": rec["title"], "recordPath": rec["recordPath"],
                "recordExists": True, "pss": "", "dates": rec["dates"], "genre": rec["genre"],
                "period": "", "diveDate": "", "diveHref": ""}
        rows.append(_finish_row(seed, records, status, dived=False))

    rows.sort(key=lambda r: (r["sortYear"], r["title"].lower()))
    return rows


def _finish_row(seed, records, status, dived):
    rec = records.get(seed["workId"], {})
    record_exists = seed["recordExists"] or seed["workId"] in records
    avail, canonical = rec.get("translations", ("", ""))
    built = bundle_built(seed["recordPath"])
    derived = "built" if built else ("dived" if dived else "")
    st = status.get(seed["workId"]) if isinstance(status, dict) else None
    declared = (st or {}).get("stage", "") if isinstance(st, dict) else ""
    ready = bool((st or {}).get("ready")) if isinstance(st, dict) else False
    return {
        "workId": seed["workId"],
        "title": seed["title"],
        "type": (seed["genre"] or rec.get("genre") or "").replace("_", " "),
        "dates": seed["dates"] or rec.get("dates", ""),
        "period": _short_period(seed["period"]),
        "pss": seed["pss"],
        "translations": avail,
        "canonical": canonical,
        "stage": furthest_stage(derived, declared),
        "recordExists": record_exists,
        "ready": ready,
        "diveHref": seed["diveHref"],
        "overviewHref": overview_href(seed["recordPath"]),
        "sortYear": _year(seed["slug"], seed["dates"] or rec.get("dates", "")),
    }


def _short_period(period):
    if not period:
        return ""
    if "Prophet" in period:
        return "Prophet"
    return collapse_ws(period).split(";")[0][:24]


def _year(slug, dates):
    m = re.match(r"(\d{4})", slug or "")
    if m:
        return int(m.group(1))
    m = re.search(r"(\d{4})", str(dates or ""))
    return int(m.group(1)) if m else 9999


# ── Rendering ──────────────────────────────────────────────────────────────────

CSS = """
:root {
  --bg:#14161a; --panel:#1c1f25; --ink:#e8e4da; --ink-dim:#9a958a; --ink-faint:#5d594f;
  --line:#2e323a; --green:#54b87f; --amber:#e0a93e; --blue:#6aa3d8; --accent:#c8b68a;
}
*,*::before,*::after { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink);
  font:15px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; -webkit-font-smoothing:antialiased; }
a { color:var(--accent); text-decoration:none; } a:hover { text-decoration:underline; }
/* Top bar — the reader shell's bar in the Library's dark palette (sans, modern) */
.topbar { position:sticky; top:0; z-index:300;
  display:flex; align-items:center; justify-content:space-between; gap:1rem;
  padding:9px 16px; border-bottom:1px solid var(--line);
  background:color-mix(in srgb, var(--bg) 86%, transparent);
  backdrop-filter:blur(10px); -webkit-backdrop-filter:blur(10px); }
.topbar .tb-group { display:flex; align-items:center; gap:10px; min-width:0; }
.topbar a { font-size:12px; color:var(--ink-dim); } .topbar a:hover { color:var(--ink); text-decoration:none; }
.topbar .tb-brand { font-size:13px; color:var(--accent); }
.topbar .sep { font-size:12px; color:var(--ink-faint); }
.topbar .tb-here { font-size:13px; font-weight:600; color:var(--ink); }
.wrap { max-width:1280px; margin:0 auto; padding:2.2rem 1.3rem 4rem; }
header.top { border-bottom:1px solid var(--line); padding-bottom:1.2rem; margin-bottom:1.4rem; }
.eyebrow { font-size:.72rem; letter-spacing:.16em; text-transform:uppercase; color:var(--accent); margin:0 0 .4rem; }
h1 { font-size:1.8rem; font-weight:650; margin:0 0 .4rem; }
p.lede { color:var(--ink-dim); max-width:80ch; margin:.2rem 0 0; }
.crumb { font-size:.78rem; color:var(--ink-faint); margin-top:.9rem; }
.crumb a { color:var(--ink-dim); }
.stats { display:flex; flex-wrap:wrap; gap:.5rem; margin:1.1rem 0 1.2rem; }
.stat { background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:.45rem .75rem; }
.stat .n { font-size:1.25rem; font-weight:650; font-variant-numeric:tabular-nums; line-height:1; }
.stat .l { font-size:.68rem; color:var(--ink-dim); display:block; margin-top:.25rem; }
.controls { display:flex; flex-wrap:wrap; gap:.7rem; align-items:center; margin:.6rem 0 1rem; }
.search { flex:1; min-width:200px; }
.search input { width:100%; background:var(--panel); border:1px solid var(--line); color:var(--ink);
  border-radius:8px; padding:.45rem .7rem; font:inherit; font-size:.85rem; }
.search input::placeholder { color:var(--ink-faint); }
button.csv { background:var(--panel); border:1px solid var(--line); color:var(--ink-dim);
  border-radius:8px; padding:.45rem .8rem; font:inherit; font-size:.8rem; cursor:pointer; }
button.csv:hover { border-color:var(--accent); color:var(--ink); }
table { width:100%; border-collapse:collapse; font-size:.84rem; }
th, td { text-align:left; padding:.5rem .6rem; border-bottom:1px solid var(--line); vertical-align:top; }
th { position:sticky; top:40px; background:var(--bg); color:var(--accent); font-weight:600; cursor:pointer;
  white-space:nowrap; user-select:none; font-size:.74rem; letter-spacing:.03em; text-transform:uppercase; }
th:hover { color:var(--ink); }
th[aria-sort="ascending"]::after { content:" ▲"; font-size:.7em; }
th[aria-sort="descending"]::after { content:" ▼"; font-size:.7em; }
tbody tr:hover { background:var(--panel); }
td.title { font-weight:600; color:var(--ink); min-width:15rem; }
td.muted, .muted { color:var(--ink-faint); }
.pill { display:inline-block; font-size:.66rem; font-weight:650; text-transform:uppercase; letter-spacing:.03em;
  padding:.1em .5em; border-radius:4px; white-space:nowrap; }
.pill.stage { color:var(--blue); background:color-mix(in srgb, var(--blue) 16%, var(--panel)); }
.pill.built { color:var(--green); background:color-mix(in srgb, var(--green) 16%, var(--panel)); }
.pill.gap { color:var(--amber); background:color-mix(in srgb, var(--amber) 16%, var(--panel)); }
.pill.ready { color:var(--green); background:color-mix(in srgb, var(--green) 18%, var(--panel)); }
tr[hidden] { display:none; }
footer { margin-top:2.4rem; border-top:1px solid var(--line); padding-top:1rem; color:var(--ink-faint);
  font-size:.78rem; max-width:90ch; } footer code { color:var(--ink-dim); }
"""

SCRIPT = """
const q = document.getElementById('q');
const table = document.getElementById('tracker');
const tbody = table.tBodies[0];
const rows = Array.from(tbody.rows);

q.addEventListener('input', () => {
  const term = q.value.trim().toLowerCase();
  rows.forEach(r => { r.hidden = term && !r.dataset.search.includes(term); });
});

let sortCol = -1, sortDir = 1;
Array.from(table.tHead.rows[0].cells).forEach((th, i) => {
  th.addEventListener('click', () => {
    sortDir = (sortCol === i) ? -sortDir : 1;
    sortCol = i;
    Array.from(table.tHead.rows[0].cells).forEach(c => c.removeAttribute('aria-sort'));
    th.setAttribute('aria-sort', sortDir === 1 ? 'ascending' : 'descending');
    const num = th.dataset.num === '1';
    rows.sort((a, b) => {
      let x = a.cells[i].dataset.sort ?? a.cells[i].textContent.trim();
      let y = b.cells[i].dataset.sort ?? b.cells[i].textContent.trim();
      if (num) { x = parseFloat(x) || 0; y = parseFloat(y) || 0; return (x - y) * sortDir; }
      return x.localeCompare(y) * sortDir;
    });
    rows.forEach(r => tbody.appendChild(r));
  });
});

document.getElementById('csv').addEventListener('click', () => {
  const head = Array.from(table.tHead.rows[0].cells).map(c => c.textContent.trim());
  const lines = [head.join(',')];
  rows.filter(r => !r.hidden).forEach(r => {
    lines.push(Array.from(r.cells).map(c => {
      const v = (c.dataset.sort ?? c.textContent).trim().replace(/"/g, '""');
      return /[",\\n]/.test(v) ? '"' + v + '"' : v;
    }).join(','));
  });
  const blob = new Blob([lines.join('\\n')], {type:'text/csv'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = 'prophet-works.csv'; a.click();
});
"""

COLUMNS = [
    ("Title", "title", False),
    ("Type", "type", False),
    ("Written", "dates", False),
    ("Period", "period", False),
    ("PSS", "pss", False),
    ("English translation(s)", "translations", False),
    ("Canonical", "canonical", False),
    ("In the loop", "stage", False),
    ("Record", "record", False),
    ("Ready", "ready", False),
]


def render_cell(row, key):
    if key == "title":
        inner = esc(row["title"])
        # overview page (the work's own front page) beats the dive; the
        # overview links onward to the dive itself
        href = row.get("overviewHref") or row["diveHref"]
        if href:
            inner = f'<a href="{esc(href)}">{inner}</a>'
        return f'<td class="title" data-sort="{esc(row["title"].lower())}">{inner}</td>'
    if key == "stage":
        s = row["stage"]
        if not s:
            return '<td class="muted" data-sort="0">—</td>'
        cls = "built" if s in ("built", "read", "re-dived", "ingested") else "stage"
        rank = LOOP_STAGES.index(s) + 1
        return f'<td data-sort="{rank}"><span class="pill {cls}">{esc(s)}</span></td>'
    if key == "record":
        if row["recordExists"]:
            return '<td data-sort="1"><span class="pill built">yes</span></td>'
        return '<td data-sort="0"><span class="pill gap">none yet</span></td>'
    if key == "ready":
        if row["ready"]:
            return '<td data-sort="1"><span class="pill ready">ready</span></td>'
        return '<td class="muted" data-sort="0">—</td>'
    val = row.get(key, "")
    cls = "" if val else "muted"
    return f'<td class="{cls}">{esc(val) if val else "—"}</td>'


def render(rows, meta):
    n = len(rows)
    built = sum(1 for r in rows if r["stage"] in ("built", "read", "re-dived", "ingested"))
    dived = sum(1 for r in rows if r["stage"])
    gaps = sum(1 for r in rows if not r["recordExists"])

    head = "".join(
        f'<th data-num="{1 if num else 0}">{esc(label)}</th>' for label, _, num in COLUMNS)
    body = []
    for r in rows:
        search = esc(" ".join([r["title"], r["type"], r["period"], r["pss"],
                               r["translations"], r["stage"]]).lower())
        cells = "".join(render_cell(r, key) for _, key, _ in COLUMNS)
        body.append(f'<tr data-search="{search}">{cells}</tr>')
    body_html = "\n".join(body)

    stats = (
        f'<div class="stat"><span class="n">{n}</span><span class="l">works tracked</span></div>'
        f'<div class="stat"><span class="n" style="color:var(--blue)">{dived}</span><span class="l">in the loop</span></div>'
        f'<div class="stat"><span class="n" style="color:var(--green)">{built}</span><span class="l">built or further</span></div>'
        f'<div class="stat"><span class="n" style="color:var(--amber)">{gaps}</span><span class="l">no record yet</span></div>'
    )
    updated = meta.get("lastUpdated") or ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Reader-editions works tracker — tolstoy.life</title>
<style>{CSS}</style>
</head>
<body>
<header class="topbar">
  <div class="tb-group">
    <a class="tb-brand" href="/INDEX.html">tolstoy.life</a>
    <span class="sep">›</span>
    <span class="tb-here">Library</span>
  </div>
  <div class="tb-group tb-links">
    <a href="/INDEX.html">Docs</a>
    <a href="/research/index.html">Research index</a>
  </div>
</header>
<div class="wrap">
<header class="top">
  <p class="eyebrow">tolstoy.life · reader editions</p>
  <h1>Works tracker</h1>
  <p class="lede">Every work the dives have surfaced — the run-list for the reader editions and the progress
  board for where each sits in the loop (dived → built → read → re-dived → ingested). The reader editions
  focus on the prophet period; the Period column marks which works belong to it, and the table sorts by date.
  Click a column to sort; type to filter. Generated from the dives, the works records, and the hand-kept
  status file; it rebuilds on every docs build.</p>
  <p class="crumb">{esc(n)} works · latest dive {esc(updated)}</p>
</header>

<div class="stats">{stats}</div>

<div class="controls">
  <div class="search"><input type="search" id="q" placeholder="Filter by title, type, period, PSS…" aria-label="Filter works"></div>
  <button class="csv" id="csv">Download CSV</button>
</div>

<table id="tracker">
<thead><tr>{head}</tr></thead>
<tbody>
{body_html}
</tbody>
</table>

<footer>
  Generated by <code>docs/reader/lib/build_works_tracker.py</code> from each dive's <code>dossier.yaml</code>,
  the works records under <code>website/src/works/</code>, and <code>docs/reader/status.yaml</code> (the hand-kept
  loop status). <strong>Dived</strong> and <strong>built</strong> are read from disk; the later stages are set by
  hand in the status file. The translation columns stay blank until each work's <code>.data.yaml</code> sidecar
  (works schema §8) is written. Do not hand-edit this page — it regenerates on every <code>serve.py</code> build.
</footer>
</div>
<script>{SCRIPT}</script>
</body>
</html>"""


def build(verbose=True):
    rows = assemble()
    # The page's "updated" is the latest dive date, not a wall-clock stamp.
    dive_dates = []
    for dossier in dive_dossiers():
        topic = (load_yaml(dossier).get("topic") or {})
        if topic.get("date"):
            dive_dates.append(str(topic["date"]))
    meta = {"lastUpdated": max(dive_dates) if dive_dates else ""}

    out_path = READER / OUT_NAME
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render(rows, meta), encoding="utf-8")
    if verbose:
        gaps = sum(1 for r in rows if not r["recordExists"])
        built = sum(1 for r in rows if r["stage"] in ("built", "read", "re-dived", "ingested"))
        print(f"SUMMARY: {len(rows)} works — {built} built+ · {gaps} without a record · "
              f"latest dive {meta['lastUpdated'] or '—'}")
        print(f"  ✓ wrote {out_path.relative_to(REPO_ROOT)}")
    return len(rows)


def main():
    ap = argparse.ArgumentParser(description="Generate the reader-editions works tracker.")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    build(verbose=not args.quiet)
    sys.exit(0)


if __name__ == "__main__":
    main()
