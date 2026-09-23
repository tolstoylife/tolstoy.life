#!/usr/bin/env python3
"""Interactive landing page for docs/research/ — generated from the dossiers.

The project's research lives in ~50 corpus-dive folders under docs/research/,
each with its own index.html. There has been no single front door: a reader
arriving at the research tree had to already know which dive to open. This tool
builds that door — a committed docs/research/index.html that lists every dive,
groups it (single-work / theme / reference), embeds the project's two research
visualizations, and points at the queued backlog.

It mirrors build_evidence_index.py: walk every <slug>/dossier.yaml, read the
`topic` block (title, date, period, scope), classify the dive, and render one
HTML page. Folders without a dossier (older surveys, the evidence index) fall
back to their index.md frontmatter; the two bare reference notes
(pss-volume-mapping, tolstoydigital-tei-reference) are picked up from the
top-level *.md. The page reuses the dark editorial theme of the embedded
visualizations so the whole surface reads as one piece.

Classification (the dossier tells us, no hard-coded dive list):
  - single-work dive  → has a top-level `workRecord:`  (one work documented)
  - theme dive        → has `workRecords:` (multi-work) OR no record at all
                        (the concept dives: tolstoyanism, doukhobors, …)
  - reference & method→ a small named set about the corpus apparatus itself
                        (the four the plan names + the editions reference)

Output (committed; the .gitignore lists the exception):
  docs/research/index.html

It writes nothing else and reads nothing outside docs/research/. Deterministic:
no wall-clock stamp in the page (the "updated" date is the latest dive date), so
rebuilding without a new dive produces a byte-identical file.

Usage:
  build_research_index.py                 # build the page, print SUMMARY
  build_research_index.py --quiet         # suppress per-dive lines
  build_research_index.py --research-dir PATH   # default: docs/research

Auto-runs as part of the docs build: serve.py's build_all() calls build().
Run standalone from anywhere:
  python3 docs/research/lib/build_research_index.py
"""
import argparse
import html
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("build_research_index.py: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

# ── Paths ────────────────────────────────────────────────────────────────────
LIB = Path(__file__).parent.resolve()        # …/docs/research/lib
RESEARCH = LIB.parent                         # …/docs/research
DOCS = RESEARCH.parent                        # …/docs
REPO_ROOT = DOCS.parent                       # repo root
OUT_NAME = "index.html"                       # docs/research/index.html

# Folders that are NOT dives but live in the research tree; never list them.
NON_DIVE_DIRS = {"lib", "visualizations"}

# The "reference & method" bucket — dives about the corpus apparatus itself,
# not a Tolstoy work or theme. The first four are named in the index plan; the
# editions reference joins them (layer: reference). Everything else classifies
# from its dossier (workRecord → single-work; else → theme).
REFERENCE_SLUGS = {
    "evidence-index",
    "jubilee-edition-tei-corpus",
    "tolstoydigital-tei-reference",
    "pss-volume-mapping",
    "biryukov-biography-editions",
    # Visual-resource surveys: catalogues of where Tolstoy appears in art and
    # photographs — reference material, not a work or theme dive.
    "tolstoy-in-art",
    "tolstoy-in-photographs",
}

# A handful of dives carry a workRecord but read as theme dives (the index plan
# names the late-voice dive a theme dive). Override the workRecord → single-work
# rule for these named slugs.
THEME_SLUGS = {
    "late-voice-encryption-compression",
}

# The two promoted visualizations (copied into docs/research/visualizations/).
COVERAGE_VIZ = "visualizations/coverage-map.html"
PROPHET_VIZ = "visualizations/prophet-essays.html"
# The queued-dive backlog plan (rendered to .html by serve.py).
BACKLOG_DOC = "_meta/_prophet-period-nonfiction-dives.html"

GROUP_LABELS = {
    "work": "Single-work dives",
    "theme": "Theme dives",
    "reference": "Reference & method",
}
GROUP_ORDER = ["work", "theme", "reference"]


def collapse_ws(s):
    return " ".join((s or "").split())


def first_sentence(text, limit=200):
    """A one-line scope: the first sentence if short, else a clean truncation."""
    t = collapse_ws(text)
    if not t:
        return ""
    m = re.search(r"\.\s", t)
    if m and m.start() <= limit:
        return t[: m.start() + 1]
    if len(t) <= limit:
        return t
    return t[:limit].rsplit(" ", 1)[0].rstrip(",;—- ") + "…"


def parse_year(slug, date):
    """Composition/sort year: the slug's leading year, else the date's year."""
    m = re.match(r"(\d{4})", slug or "")
    if m:
        return int(m.group(1))
    m = re.match(r"(\d{4})", str(date or ""))
    return int(m.group(1)) if m else 9999


# ── Minimal frontmatter reader (fallback for dossier-less folders) ────────────

def read_frontmatter(path):
    """Return (frontmatter_dict, lede) for a docs .md file."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}, ""
    fm, body = {}, text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            try:
                loaded = yaml.safe_load(text[3:end])
                if isinstance(loaded, dict):
                    fm = loaded
            except yaml.YAMLError:
                fm = {}
            body = text[end + 4:]
    # First real prose paragraph as the lede.
    lede = ""
    for para in re.split(r"\n\s*\n", body):
        p = collapse_ws(para)
        if p and not p.startswith("#") and not p.startswith("!["):
            lede = p
            break
    return fm, lede


# ── Discovery ─────────────────────────────────────────────────────────────────

def classify(slug, data):
    if slug in REFERENCE_SLUGS:
        return "reference"
    if slug in THEME_SLUGS:
        return "theme"
    if isinstance(data, dict) and "workRecord" in data:
        return "work"
    return "theme"


def discover(research_dir):
    """Return a list of dive records discovered from the research tree."""
    dives = []
    seen_dirs = set()

    # Folder dives: prefer dossier.yaml's topic block; fall back to index.md.
    # Dives live nested under works/<genre>/<subcat>/ and themes/<slug>/;
    # _meta/, lib/, visualizations/, evidence-index/ are excluded by construction.
    folder_by_slug = {}
    for pat in ("works/*/*/*/dossier.yaml", "themes/*/dossier.yaml",
                "works/*/*/*/index.md", "themes/*/index.md"):
        for p in research_dir.glob(pat):
            folder_by_slug.setdefault(p.parent.name, p.parent)

    for slug in sorted(folder_by_slug):
        if slug in NON_DIVE_DIRS:
            continue
        folder = folder_by_slug[slug]
        dossier = folder / "dossier.yaml"
        topic, lede = {}, ""
        data = {}
        if dossier.exists():
            try:
                data = yaml.safe_load(dossier.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                data = {}
            topic = data.get("topic") or {}
        if not topic and (folder / "index.md").exists():
            fm, lede = read_frontmatter(folder / "index.md")
            topic = {
                "title": fm.get("title") or slug,
                "date": fm.get("date") or fm.get("lastUpdated"),
                "period": fm.get("period"),
            }
        rel = folder.relative_to(research_dir).as_posix()
        href = f"{rel}/index.html" if (folder / "index.html").exists() \
            or (folder / "index.md").exists() else None
        if href is None:
            continue
        title = collapse_ws(topic.get("title")) or slug
        scope = first_sentence(topic.get("question")) or lede
        dives.append({
            "slug": slug,
            "title": title,
            "scope": scope,
            "date": str(topic.get("date") or ""),
            "period": collapse_ws(topic.get("period")) or "",
            "href": href,
            "group": classify(slug, data),
            "year": parse_year(slug, topic.get("date")),
            "hasDossier": dossier.exists(),
        })
        seen_dirs.add(slug)

    # Bare reference notes at the top level (no folder, no dossier).
    for p in sorted(research_dir.glob("*.md")):
        stem = p.stem
        if stem.startswith("_") or stem in seen_dirs:
            continue
        fm, lede = read_frontmatter(p)
        if not p.with_suffix(".html").exists():
            continue
        dives.append({
            "slug": stem,
            "title": collapse_ws(fm.get("title")) or stem,
            "scope": lede,
            "date": str(fm.get("date") or fm.get("lastUpdated") or ""),
            "period": "",
            "href": f"{stem}.html",
            "group": classify(stem, {}),
            "year": parse_year(stem, fm.get("date") or fm.get("lastUpdated")),
            "hasDossier": False,
        })

    return dives


def sort_dives(dives):
    grouped = {g: [] for g in GROUP_ORDER}
    for d in dives:
        grouped[d["group"]].append(d)
    # Work dives carry a reliable composition-year prefix → chronological.
    # Theme & reference dives mix composition-year and concept slugs, so the
    # year is unreliable → sort by title for a predictable, stable order.
    grouped["work"].sort(key=lambda d: (d["year"], d["title"].lower()))
    grouped["theme"].sort(key=lambda d: d["title"].lower())
    grouped["reference"].sort(key=lambda d: d["title"].lower())
    return grouped


# ── Rendering ──────────────────────────────────────────────────────────────────

def esc(s):
    return html.escape(str(s or ""), quote=True)


CSS = """
:root {
  --bg:#14161a; --panel:#1c1f25; --panel-2:#21252c; --ink:#e8e4da;
  --ink-dim:#9a958a; --ink-faint:#5d594f; --line:#2e323a;
  --green:#54b87f; --amber:#e0a93e; --blue:#6aa3d8; --violet:#a08cc8;
  --accent:#c8b68a;
}
*,*::before,*::after { box-sizing:border-box; }
body {
  margin:0; padding:0; background:var(--bg); color:var(--ink);
  font:16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  -webkit-font-smoothing:antialiased;
}
a { color:var(--accent); text-decoration:none; }
a:hover { text-decoration:underline; }
.wrap { max-width:1180px; margin:0 auto; padding:2.4rem 1.4rem 4rem; }
header.top { border-bottom:1px solid var(--line); padding-bottom:1.4rem; margin-bottom:1.8rem; }
.eyebrow { font-size:.74rem; letter-spacing:.16em; text-transform:uppercase; color:var(--accent); margin:0 0 .5rem; }
h1 { font-size:2rem; font-weight:650; letter-spacing:.01em; margin:0 0 .5rem; }
p.lede { color:var(--ink-dim); max-width:74ch; margin:.2rem 0 0; }
.crumb { font-size:.78rem; color:var(--ink-faint); margin-top:1rem; }
.crumb a { color:var(--ink-dim); }
h2 { font-size:1.2rem; font-weight:600; color:var(--accent); margin:2.8rem 0 .3rem; }
h2 .count { color:var(--ink-faint); font-weight:500; font-size:.9rem; margin-left:.4em; }
p.note { color:var(--ink-faint); font-size:.84rem; max-width:80ch; margin:.2rem 0 1.1rem; }

.stats { display:flex; flex-wrap:wrap; gap:.5rem; margin:1.4rem 0 1.6rem; }
.stat { background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:.5rem .8rem; }
.stat .n { font-size:1.3rem; font-weight:650; font-variant-numeric:tabular-nums; line-height:1; }
.stat .l { font-size:.7rem; color:var(--ink-dim); display:block; margin-top:.25rem; }

.controls { display:flex; flex-wrap:wrap; gap:.8rem; align-items:center; margin:1.2rem 0 .4rem; position:sticky; top:0;
  background:var(--bg); padding:.6rem 0; z-index:5; border-bottom:1px solid var(--line); }
.chips { display:flex; flex-wrap:wrap; gap:.4rem; }
.chip { background:var(--panel); border:1px solid var(--line); color:var(--ink-dim); border-radius:20px;
  padding:.3rem .8rem; font-size:.8rem; cursor:pointer; font-family:inherit; }
.chip:hover { border-color:var(--accent); color:var(--ink); }
.chip[aria-pressed="true"] { background:color-mix(in srgb, var(--accent) 22%, var(--panel)); color:var(--accent); border-color:var(--accent); }
.search { flex:1; min-width:180px; }
.search input { width:100%; background:var(--panel); border:1px solid var(--line); color:var(--ink);
  border-radius:8px; padding:.45rem .7rem; font:inherit; font-size:.85rem; }
.search input::placeholder { color:var(--ink-faint); }

.grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(300px,1fr)); gap:.7rem; margin-top:.3rem; }
.card { display:block; background:var(--panel); border:1px solid var(--line); border-left:3px solid var(--gc);
  border-radius:9px; padding:.8rem .95rem .9rem; transition:transform .08s, border-color .08s; }
.card:hover { transform:translateY(-1px); border-color:var(--gc); text-decoration:none; }
.card .ct { font-weight:600; font-size:1rem; color:var(--ink); line-height:1.35; }
.card .cm { font-size:.72rem; color:var(--ink-faint); margin:.3rem 0 .45rem; display:flex; flex-wrap:wrap; gap:.5em; align-items:center; }
.card .badge { font-size:.62rem; font-weight:650; text-transform:uppercase; letter-spacing:.04em; padding:.1em .5em; border-radius:4px;
  color:var(--gc); background:color-mix(in srgb, var(--gc) 18%, var(--panel)); }
.card .cs { font-size:.83rem; color:var(--ink-dim); line-height:1.45; }
.card[hidden] { display:none; }
.empty { color:var(--ink-faint); font-style:italic; font-size:.85rem; padding:.6rem 0; }

.viz { margin:1rem 0 0; }
.viz-frame { width:100%; border:1px solid var(--line); border-radius:10px; background:#14161a; display:block; }
.viz a.full { font-size:.78rem; }

footer { margin-top:3rem; border-top:1px solid var(--line); padding-top:1rem; color:var(--ink-faint); font-size:.78rem; max-width:88ch; }
footer code { color:var(--ink-dim); }
"""

GROUP_COLOR = {"work": "var(--green)", "theme": "var(--blue)", "reference": "var(--violet)"}
GROUP_BADGE = {"work": "work", "theme": "theme", "reference": "reference"}

# Plain string (not an f-string member) so its JS braces survive templating.
SCRIPT = """
const cards = Array.from(document.querySelectorAll('.card'));
const chips = Array.from(document.querySelectorAll('.chip'));
const q = document.getElementById('q');
let filter = 'all';

function apply() {
  const term = q.value.trim().toLowerCase();
  cards.forEach(c => {
    const okGroup = filter === 'all' || c.dataset.group === filter;
    const okTerm = !term || c.dataset.search.includes(term);
    c.hidden = !(okGroup && okTerm);
  });
  document.querySelectorAll('[data-group-section]').forEach(sec => {
    const any = sec.querySelectorAll('.card:not([hidden])').length;
    sec.style.display = any ? '' : 'none';
  });
}
chips.forEach(ch => ch.addEventListener('click', () => {
  filter = ch.dataset.filter;
  chips.forEach(c => c.setAttribute('aria-pressed', c === ch ? 'true' : 'false'));
  apply();
}));
q.addEventListener('input', apply);

// The visualizations are same-origin, so size each iframe to its own content
// (the grids reflow with width, so a fixed height can't fit every viewport).
const frames = Array.from(document.querySelectorAll('iframe.viz-frame'));
function fitFrames() {
  frames.forEach(f => {
    try {
      const d = f.contentDocument;
      if (d && d.body) f.style.height = (d.documentElement.scrollHeight + 4) + 'px';
    } catch (e) { /* keep the fallback height attribute */ }
  });
}
frames.forEach(f => f.addEventListener('load', fitFrames));
window.addEventListener('load', fitFrames);
window.addEventListener('resize', fitFrames);
"""


def render_card(d):
    meta_bits = []
    if d["date"]:
        meta_bits.append(esc(d["date"]))
    if d["period"]:
        meta_bits.append(esc(d["period"]))
    meta_html = " · ".join(meta_bits)
    badge = f'<span class="badge">{GROUP_BADGE[d["group"]]}</span>'
    scope = f'<div class="cs">{esc(d["scope"])}</div>' if d["scope"] else ""
    search_key = esc((d["title"] + " " + d["scope"] + " " + d["period"]).lower())
    return (
        f'<a class="card" href="{esc(d["href"])}" '
        f'data-group="{d["group"]}" data-search="{search_key}" '
        f'style="--gc:{GROUP_COLOR[d["group"]]}">'
        f'<div class="ct">{esc(d["title"])}</div>'
        f'<div class="cm">{badge}{(" · " + meta_html) if meta_html else ""}</div>'
        f'{scope}</a>'
    )


def render(grouped, meta):
    counts = {g: len(grouped[g]) for g in GROUP_ORDER}
    total = sum(counts.values())

    stats = (
        f'<div class="stat"><span class="n">{total}</span><span class="l">dives & surveys</span></div>'
        f'<div class="stat"><span class="n" style="color:var(--green)">{counts["work"]}</span><span class="l">single-work</span></div>'
        f'<div class="stat"><span class="n" style="color:var(--blue)">{counts["theme"]}</span><span class="l">theme</span></div>'
        f'<div class="stat"><span class="n" style="color:var(--violet)">{counts["reference"]}</span><span class="l">reference</span></div>'
    )

    chips = ['<button class="chip" data-filter="all" aria-pressed="true">All</button>']
    for g in GROUP_ORDER:
        chips.append(
            f'<button class="chip" data-filter="{g}" aria-pressed="false" '
            f'style="--gc:{GROUP_COLOR[g]}">{esc(GROUP_LABELS[g])}</button>'
        )
    chips_html = "".join(chips)

    sections = []
    for g in GROUP_ORDER:
        cards = "".join(render_card(d) for d in grouped[g])
        sections.append(
            f'<section data-group-section="{g}">'
            f'<h2>{esc(GROUP_LABELS[g])}<span class="count">{counts[g]}</span></h2>'
            f'<div class="grid">{cards}</div>'
            f'</section>'
        )
    sections_html = "\n".join(sections)

    updated = meta.get("lastUpdated") or ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Corpus-dive research — tolstoy.life</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <p class="eyebrow">tolstoy.life · research</p>
  <h1>Corpus-dive research</h1>
  <p class="lede">Primary-source dives across the local Tolstoy corpus — the tolstoydigital TEI and the
  90-volume Jubilee Edition. Each dive welds its findings to Tolstoy's own words, the edition's apparatus,
  and the project's prior dives. This page is generated from the dives themselves; it rebuilds on every docs build.</p>
  <p class="crumb"><a href="/INDEX.html">← all notes</a> · {esc(total)} dives · latest {esc(updated)}</p>
</header>

<section class="viz">
  <h2>Where the dives have reached</h2>
  <p class="note">All 90 volumes of the Jubilee Edition, coloured by how far the dives have reached. Hover or focus any volume.
  <a class="full" href="{COVERAGE_VIZ}" target="_blank" rel="noopener">open full ↗</a></p>
  <iframe class="viz-frame" src="{COVERAGE_VIZ}" height="2300" loading="lazy" title="Jubilee Edition corpus-dive coverage map"></iframe>
</section>

<div class="stats">{stats}</div>

<div class="controls">
  <div class="chips">{chips_html}</div>
  <div class="search"><input type="search" id="q" placeholder="Filter dives by title, theme, or period…" aria-label="Filter dives"></div>
</div>

{sections_html}

<section>
  <h2>The queued backlog</h2>
  <p class="note">The next wave: the remaining Prophet-period non-fiction dives, planned but not yet run.
  See the <a href="{BACKLOG_DOC}">backlog plan</a> for the full inventory and run order, and the
  <a href="{COVERAGE_VIZ}" target="_blank" rel="noopener">coverage map</a> for which volumes they draw on.</p>
</section>

<section class="viz">
  <h2>The Prophet period — essays, translations, correspondence</h2>
  <p class="note">Timeline, translation lag, and the correspondence ridgeline behind the Prophet-period work.
  <a class="full" href="{PROPHET_VIZ}" target="_blank" rel="noopener">open full ↗</a></p>
  <iframe class="viz-frame" src="{PROPHET_VIZ}" height="3800" loading="lazy" title="Prophet-period essays, translations and correspondence"></iframe>
</section>

<footer>
  Generated by <code>docs/research/lib/build_research_index.py</code> from each dive's <code>dossier.yaml</code>
  (older surveys fall back to their <code>index.md</code> frontmatter). Do not hand-edit — it regenerates on every
  <code>serve.py</code> build. Visualizations live in <code>docs/research/visualizations/</code>.
  Classification: single-work dives carry a <code>workRecord</code>; theme dives span several works or none;
  reference &amp; method covers the corpus apparatus.
</footer>
</div>

<script>{SCRIPT}</script>
</body>
</html>"""


# ── Main ────────────────────────────────────────────────────────────────────

def build(research_dir=RESEARCH, verbose=True):
    """Discover dives, render docs/research/index.html. Returns the dive count."""
    research_dir = Path(research_dir).resolve()
    dives = discover(research_dir)
    grouped = sort_dives(dives)
    dates = [d["date"] for d in dives if d["date"]]
    meta = {"lastUpdated": max(dates) if dates else ""}

    if verbose:
        for g in GROUP_ORDER:
            for d in grouped[g]:
                src = "dossier" if d["hasDossier"] else "index.md"
                print(f"  {g[:4]:4s} {d['slug']:42s} {d['date'] or '—':10s} ({src})")

    out_path = research_dir / OUT_NAME
    out_path.write_text(render(grouped, meta), encoding="utf-8")
    counts = {g: len(grouped[g]) for g in GROUP_ORDER}
    if verbose:
        print()
        print(f"SUMMARY: {len(dives)} dives — {counts['work']} work / "
              f"{counts['theme']} theme / {counts['reference']} reference · "
              f"latest {meta['lastUpdated'] or '—'}")
        print(f"  ✓ wrote {out_path.relative_to(REPO_ROOT)}")
    return len(dives)


def main():
    ap = argparse.ArgumentParser(
        description="Generate the docs/research/ interactive landing page from the dives.")
    ap.add_argument("--quiet", action="store_true", help="suppress per-dive lines")
    ap.add_argument("--research-dir", default=str(RESEARCH),
                    help="directory holding the dive folders (default: docs/research)")
    args = ap.parse_args()

    research_dir = Path(args.research_dir).resolve()
    if not research_dir.is_dir():
        print(f"build_research_index.py: no such directory: {research_dir}", file=sys.stderr)
        sys.exit(2)
    build(research_dir=research_dir, verbose=not args.quiet)
    sys.exit(0)


if __name__ == "__main__":
    main()
