#!/usr/bin/env python3
"""
docs/ document server — tolstoy.life
======================================
Converts all .md files in docs/ to HTML on startup (and on request),
then serves them with live navigation via INDEX.html.

Usage:
    cd /Volumes/Graugear/Tolstoy/docs
    python3 serve.py            # serves on http://localhost:7866
    python3 serve.py --port 8001
    python3 serve.py --build-only   # convert md→html without starting server
"""

import argparse
import http.server
import importlib.util
import os
import re
import socketserver
import sys
from datetime import datetime
from pathlib import Path

# ── Dependencies ───────────────────────────────────────────────────────────────

def require(package, pip_name=None):
    if importlib.util.find_spec(package) is None:
        name = pip_name or package
        print(f"Installing {name}…")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", name,
                               "--break-system-packages", "-q"])

require("markdown")
import markdown
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension

# ── Paths ──────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.resolve()

SKIP_DIRS  = {".git", ".claude", ".omc", "__pycache__", "node_modules"}
SKIP_FILES = {"serve.py"}
PASSTHROUGH_EXTENSIONS = {".html", ".pdf", ".pptx", ".mp3", ".jpg", ".png",
                           ".svg", ".yaml", ".yml", ".skill", ".json"}

# Paths (relative to docs/) lifted to the top of INDEX as a featured card.
# Featured entries are removed from their normal section grid to avoid duplication.
FEATURED = ("architecture/architecture-review.html",)

# ── Design tokens ──────────────────────────────────────────────────────────────

CSS = """
:root {
  --ink: #1e1a17;
  --ink-soft: #4a4038;
  --paper: #faf7f2;
  --rule: #d9d1c5;
  --accent: #6b4423;
  --accent-soft: #8c6a4a;
  --measure: 38rem;
  --measure-wide: 52rem;
}

*, *::before, *::after { box-sizing: border-box; }

html { font-size: 150%; -webkit-text-size-adjust: 100%; }

body {
  margin: 0; padding: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: "Iowan Old Style", "Palatino Linotype", Palatino,
               "URW Palladio L", P052, Charter, Georgia, "Times New Roman", serif;
  font-size: 1.05rem;
  line-height: 1.65;
  font-feature-settings: "kern", "liga", "onum";
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
}

/* ── Layout ── */
.site-header {
  max-width: var(--measure-wide);
  margin: 0 auto;
  padding: 1.4rem 1.5rem 1rem;
  display: flex;
  align-items: baseline;
  gap: 1.2rem;
  border-bottom: 1px solid var(--rule);
}
.site-header a.home {
  font-size: 0.78rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent-soft);
  text-decoration: none;
  font-style: italic;
  white-space: nowrap;
}
.site-header a.home:hover { color: var(--accent); }
.breadcrumb {
  font-size: 0.82rem;
  color: var(--ink-soft);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.breadcrumb a { color: var(--ink-soft); text-decoration: none; }
.breadcrumb a:hover { color: var(--accent); text-decoration: underline; }
.breadcrumb span { color: var(--rule); margin: 0 0.3em; }

header.doc-header {
  max-width: var(--measure);
  margin: 0 auto;
  padding: 3rem 1.5rem 2rem;
  border-bottom: 1px solid var(--rule);
}
header.doc-header .eyebrow {
  font-size: 0.78rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent-soft);
  font-style: italic;
  margin: 0 0 0.8rem;
}
header.doc-header h1 {
  font-size: 2.2rem;
  line-height: 1.15;
  margin: 0 0 0.5rem;
  font-weight: 600;
  letter-spacing: -0.012em;
}
header.doc-header .meta {
  font-size: 0.85rem;
  color: var(--ink-soft);
  margin: 0;
  font-variant-numeric: oldstyle-nums;
}

main {
  max-width: var(--measure);
  margin: 0 auto;
  padding: 2.5rem 1.5rem 6rem;
}

/* ── Typography ── */
h1 { font-size: 2.2rem; line-height: 1.15; margin: 0 0 1rem; font-weight: 600; letter-spacing: -0.012em; }
h2 { font-size: 1.6rem; line-height: 1.25; margin: 3rem 0 0.4rem; font-weight: 600; letter-spacing: -0.005em; }
h3 { font-size: 1.18rem; line-height: 1.3; margin: 2.4rem 0 0.6rem; font-weight: 600; }
h4 { font-size: 1rem; font-weight: 600; margin: 1.6rem 0 0.4rem; }
p { margin: 0 0 1.1rem; hyphens: auto; -webkit-hyphens: auto; }
ol, ul { padding-left: 1.4rem; margin: 0 0 1.3rem; }
li { margin-bottom: 0.55rem; }
li > ol, li > ul { margin-top: 0.4rem; margin-bottom: 0.2rem; }
strong { font-weight: 600; }
em { font-style: italic; }
a { color: var(--accent); text-decoration: underline;
    text-decoration-thickness: 1px; text-underline-offset: 2px; }
a:hover { color: var(--ink); }
blockquote {
  margin: 1.4rem 0; padding: 0 0 0 1.2rem;
  border-left: 2px solid var(--accent-soft);
  color: var(--ink-soft); font-style: italic;
}
hr { border: 0; border-top: 1px solid var(--rule); margin: 3rem 0; }

code, kbd, samp {
  font-family: "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
  font-size: 0.88em;
  background: rgba(107,68,35,0.07);
  padding: 0.08em 0.34em;
  border-radius: 2px;
}
pre {
  background: rgba(107,68,35,0.05);
  border: 1px solid var(--rule);
  border-radius: 3px;
  padding: 1rem 1.2rem;
  overflow-x: auto;
  margin: 0 0 1.4rem;
  font-size: 0.88rem;
  line-height: 1.5;
}
pre code { background: none; padding: 0; font-size: inherit; }

table {
  width: 100%; border-collapse: collapse;
  margin: 1.4rem 0 1.8rem; font-size: 0.94rem;
}
th, td {
  text-align: left; padding: 0.6rem 0.8rem 0.6rem 0;
  border-bottom: 1px solid var(--rule); vertical-align: top;
}
th {
  font-weight: 600; font-size: 0.82rem;
  letter-spacing: 0.06em; text-transform: uppercase;
  color: var(--accent-soft); font-style: italic;
  border-bottom: 1px solid var(--accent-soft);
}

/* ── Index page ── */
.featured-section {
  max-width: var(--measure-wide);
  margin: 1rem auto 2.5rem;
  padding: 0 1.5rem;
}
.featured-card {
  display: block;
  padding: 1.7rem 1.9rem;
  background: rgba(107, 68, 35, 0.06);
  border: 1px solid var(--accent-soft);
  border-radius: 4px;
  text-decoration: none;
  color: var(--ink);
  transition: border-color 0.15s, background 0.15s;
}
.featured-card:hover {
  border-color: var(--accent);
  background: rgba(107, 68, 35, 0.10);
  color: var(--ink);
}
.featured-card .eyebrow {
  font-size: 0.78rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent-soft);
  font-style: italic;
  margin: 0 0 0.7rem;
}
.featured-card .card-title {
  font-size: 1.42rem;
  font-weight: 600;
  margin: 0 0 0.4rem;
  line-height: 1.25;
  letter-spacing: -0.005em;
}
.featured-card .card-meta {
  font-size: 0.82rem;
  color: var(--ink-soft);
  font-style: italic;
  margin: 0 0 0.85rem;
}
.featured-card .card-lede {
  font-size: 0.97rem;
  color: var(--ink);
  line-height: 1.55;
  margin: 0;
}

.index-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
  gap: 0.8rem;
  margin: 0 0 2.5rem;
}
.index-card {
  display: block;
  padding: 1rem 1.1rem;
  background: rgba(107,68,35,0.04);
  border: 1px solid var(--rule);
  border-radius: 3px;
  text-decoration: none;
  color: var(--ink);
  transition: border-color 0.15s, background 0.15s;
}
.index-card:hover {
  border-color: var(--accent-soft);
  background: rgba(107,68,35,0.07);
  color: var(--ink);
}
.index-card .card-title {
  font-size: 0.97rem;
  font-weight: 600;
  margin: 0 0 0.25rem;
  line-height: 1.3;
}
.index-card .card-meta {
  font-size: 0.78rem;
  color: var(--ink-soft);
  font-style: italic;
}
.index-card .card-lede {
  font-size: 0.85rem;
  color: var(--ink-soft);
  margin: 0.35rem 0 0;
  line-height: 1.45;
}

.section-label {
  font-size: 0.78rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent-soft);
  font-style: italic;
  margin: 2.5rem 0 0.8rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--rule);
}

footer {
  max-width: var(--measure);
  margin: 0 auto;
  padding: 3rem 1.5rem 4rem;
  border-top: 1px solid var(--rule);
  font-size: 0.88rem;
  color: var(--ink-soft);
  font-style: italic;
  text-align: center;
}

/* ── Annotations ── */
mark.annotation {
  background: rgba(107, 68, 35, 0.13);
  border-bottom: 1.5px solid var(--accent-soft);
  cursor: pointer;
  border-radius: 1px;
  padding: 0 1px;
}
mark.annotation:hover { background: rgba(107, 68, 35, 0.22); }

#ann-popover {
  position: fixed;
  z-index: 1000;
  background: var(--paper);
  border: 1px solid var(--accent-soft);
  border-radius: 4px;
  box-shadow: 0 4px 18px rgba(30,26,23,0.13);
  padding: 0.9rem 1rem;
  width: 22rem;
  display: none;
  font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
}
#ann-popover .ann-quote {
  font-size: 0.82rem;
  color: var(--ink-soft);
  font-style: italic;
  margin: 0 0 0.6rem;
  border-left: 2px solid var(--accent-soft);
  padding-left: 0.6rem;
  line-height: 1.4;
  max-height: 3.5rem;
  overflow: hidden;
}
#ann-popover textarea {
  width: 100%;
  font-family: inherit;
  font-size: 0.9rem;
  line-height: 1.5;
  border: 1px solid var(--rule);
  border-radius: 2px;
  padding: 0.5rem 0.6rem;
  background: #fff;
  color: var(--ink);
  resize: vertical;
  min-height: 4rem;
  outline: none;
}
#ann-popover textarea:focus { border-color: var(--accent-soft); }
#ann-popover .ann-actions {
  display: flex; gap: 0.5rem; margin-top: 0.6rem; justify-content: flex-end;
}
#ann-popover button {
  font-family: inherit; font-size: 0.82rem; padding: 0.3rem 0.75rem;
  border-radius: 2px; cursor: pointer; border: 1px solid var(--rule);
  background: var(--paper); color: var(--ink-soft);
}
#ann-popover button.primary {
  background: var(--accent); border-color: var(--accent); color: #fff; font-weight: 600;
}
#ann-popover button.primary:hover { background: var(--ink); border-color: var(--ink); }
#ann-popover button:not(.primary):hover { border-color: var(--accent-soft); color: var(--ink); }

#ann-tooltip {
  position: fixed; z-index: 999;
  background: var(--ink); color: var(--paper);
  font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  font-size: 0.85rem; line-height: 1.5;
  padding: 0.6rem 0.85rem; border-radius: 3px;
  max-width: 22rem; box-shadow: 0 3px 12px rgba(30,26,23,0.18);
  pointer-events: none; display: none; white-space: pre-wrap;
}

#ann-bar {
  position: fixed; bottom: 1.2rem; right: 1.4rem;
  display: none; gap: 0.5rem; z-index: 998;
}
#ann-bar button {
  font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  font-size: 0.82rem; padding: 0.4rem 0.9rem; border-radius: 2px;
  cursor: pointer; border: 1px solid var(--accent-soft);
  background: var(--paper); color: var(--ink-soft);
  box-shadow: 0 2px 8px rgba(30,26,23,0.1);
}
#ann-bar button:hover { border-color: var(--accent); color: var(--ink); }
#ann-bar button.danger { border-color: #c0392b55; color: #c0392b; }
#ann-bar button.danger:hover { background: #c0392b; color: #fff; border-color: #c0392b; }
"""

# ── Markdown → HTML ────────────────────────────────────────────────────────────

MD = markdown.Markdown(extensions=[
    TableExtension(),
    FencedCodeExtension(),
    "nl2br",
    "sane_lists",
    "attr_list",
])

def md_to_html(md_path: Path) -> str:
    """Convert a markdown file to a full HTML page."""
    text = md_path.read_text(encoding="utf-8")

    # Strip YAML frontmatter
    frontmatter = {}
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            fm_block = text[3:end].strip()
            for line in fm_block.splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    frontmatter[k.strip()] = v.strip().strip('"')
            text = text[end+3:].strip()

    # Extract title from first # heading if not in frontmatter
    title = frontmatter.get("title", "")
    if not title:
        m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = m.group(1).strip() if m else md_path.stem.replace("-", " ").title()
        if m:
            text = text[:m.start()] + text[m.end():]

    # Extract lede
    lede = frontmatter.get("description", "")
    if not lede:
        stripped = text.strip()
        para_match = re.search(r"^(?!>)([A-Za-z].{20,})", stripped, re.MULTILINE)
        if para_match:
            lede = para_match.group(1)[:160].strip()

    # Convert markdown
    MD.reset()
    body_html = MD.convert(text)

    # Relative path for breadcrumb
    rel = md_path.relative_to(ROOT)
    parts = rel.parts
    folder = parts[-2] if len(parts) > 1 else ""

    mtime = datetime.fromtimestamp(md_path.stat().st_mtime).strftime("%-d %B %Y")

    breadcrumb = ""
    if folder and folder != ".":
        breadcrumb = f"""
        <span class="breadcrumb">
          <a href="/INDEX.html">Index</a>
          <span>›</span>
          {folder}
        </span>"""

    doc_key = "docs/" + str(rel.with_suffix(""))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — tolstoy.life docs</title>
<style>{CSS}</style>
</head>
<body>
<div class="site-header">
  <a class="home" href="/INDEX.html">tolstoy.life / docs</a>
  {breadcrumb}
</div>
<header class="doc-header">
  <p class="eyebrow">{folder or "docs"}</p>
  <h1>{title}</h1>
  <p class="meta">Last modified {mtime} · <a href="/{rel.with_suffix('.md')}">view source</a></p>
</header>
<main>
{body_html}
</main>
<footer>tolstoy.life · public documentation</footer>

<!-- Annotation UI -->
<div id="ann-popover">
  <div class="ann-quote" id="ann-quote"></div>
  <textarea id="ann-text" placeholder="Your comment…" autocomplete="off"></textarea>
  <div class="ann-actions">
    <button id="ann-cancel">Cancel</button>
    <button class="primary" id="ann-save">Save</button>
  </div>
</div>
<div id="ann-tooltip"></div>
<div id="ann-bar">
  <button id="ann-export">Copy annotations</button>
  <button class="danger" id="ann-clear">Clear all</button>
</div>

<script>
(function() {{
  const DOC_KEY = {repr(doc_key)};
  const STORE_KEY = 'tolstoy_annotations';

  // ── Storage ──────────────────────────────────────────────────────────────
  function loadAll() {{
    try {{ return JSON.parse(localStorage.getItem(STORE_KEY) || '{{}}'); }}
    catch {{ return {{}}; }}
  }}
  function saveAll(data) {{
    localStorage.setItem(STORE_KEY, JSON.stringify(data));
  }}
  function loadDoc() {{
    return loadAll()[DOC_KEY] || [];
  }}
  function saveDoc(anns) {{
    const all = loadAll();
    if (anns.length === 0) delete all[DOC_KEY];
    else all[DOC_KEY] = anns;
    saveAll(all);
  }}

  // ── Fuzzy text anchor ────────────────────────────────────────────────────
  function getContext(range) {{
    const selected = range.toString();
    const container = range.commonAncestorContainer;
    const full = (container.textContent || container.innerText || '');
    const start = full.indexOf(selected);
    if (start === -1) return null;
    return {{
      text: selected,
      before: full.slice(Math.max(0, start - 30), start),
      after: full.slice(start + selected.length, start + selected.length + 30)
    }};
  }}

  // ── Rendering ────────────────────────────────────────────────────────────
  function findAndWrap(ann, index) {{
    const main = document.querySelector('main');
    if (!main) return;
    const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {{
      const idx = node.textContent.indexOf(ann.anchor.text);
      if (idx === -1) continue;
      const before10 = ann.anchor.before.slice(-10);
      const after10 = ann.anchor.after.slice(0, 10);
      const nodeText = node.textContent;
      const contextOk = (!before10 || nodeText.slice(Math.max(0,idx-10), idx).includes(before10.slice(-4)))
                     || (!after10  || nodeText.slice(idx + ann.anchor.text.length, idx + ann.anchor.text.length + 10).includes(after10.slice(0,4)));
      if (!contextOk && ann.anchor.before && ann.anchor.after) continue;

      const before = node.textContent.slice(0, idx);
      const after = node.textContent.slice(idx + ann.anchor.text.length);
      const mark = document.createElement('mark');
      mark.className = 'annotation';
      mark.dataset.index = index;
      mark.textContent = ann.anchor.text;
      const afterNode = document.createTextNode(after);
      node.textContent = before;
      node.parentNode.insertBefore(mark, node.nextSibling);
      node.parentNode.insertBefore(afterNode, mark.nextSibling);
      attachTooltip(mark, ann, index);
      break;
    }}
  }}

  function renderAll() {{
    document.querySelectorAll('mark.annotation').forEach(m => {{
      m.replaceWith(document.createTextNode(m.textContent));
    }});
    const anns = loadDoc();
    anns.forEach((ann, i) => findAndWrap(ann, i));
    updateBar();
  }}

  // ── Tooltip ──────────────────────────────────────────────────────────────
  const tooltip = document.getElementById('ann-tooltip');

  function attachTooltip(mark, ann, index) {{
    mark.addEventListener('mouseenter', e => {{
      tooltip.textContent = ann.comment;
      tooltip.style.display = 'block';
      positionTooltip(e);
    }});
    mark.addEventListener('mousemove', positionTooltip);
    mark.addEventListener('mouseleave', () => {{ tooltip.style.display = 'none'; }});
    mark.addEventListener('click', e => {{
      e.stopPropagation();
      showDeleteConfirm(index, mark);
    }});
  }}

  function positionTooltip(e) {{
    const pad = 12;
    let x = e.clientX + pad;
    let y = e.clientY - tooltip.offsetHeight - pad;
    if (x + tooltip.offsetWidth > window.innerWidth - pad) x = e.clientX - tooltip.offsetWidth - pad;
    if (y < pad) y = e.clientY + pad;
    tooltip.style.left = x + 'px';
    tooltip.style.top = y + 'px';
  }}

  // ── Delete confirm ────────────────────────────────────────────────────────
  function showDeleteConfirm(index, mark) {{
    const anns = loadDoc();
    const comment = anns[index] ? anns[index].comment : '';
    if (confirm('Delete this annotation?\\n\\n"' + comment + '"')) {{
      anns.splice(index, 1);
      saveDoc(anns);
      renderAll();
    }}
  }}

  // ── Popover ───────────────────────────────────────────────────────────────
  const popover = document.getElementById('ann-popover');
  const annText = document.getElementById('ann-text');
  const annQuote = document.getElementById('ann-quote');
  let pendingAnchor = null;
  let pendingRange = null;

  document.getElementById('ann-save').addEventListener('click', () => {{
    const comment = annText.value.trim();
    if (!comment || !pendingAnchor) {{ hidePopover(); return; }}
    const anns = loadDoc();
    anns.push({{ anchor: pendingAnchor, comment, created: new Date().toISOString() }});
    saveDoc(anns);
    hidePopover();
    renderAll();
  }});

  document.getElementById('ann-cancel').addEventListener('click', hidePopover);

  annText.addEventListener('keydown', e => {{
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) document.getElementById('ann-save').click();
    if (e.key === 'Escape') hidePopover();
  }});

  function hidePopover() {{
    popover.style.display = 'none';
    annText.value = '';
    pendingAnchor = null;
    if (pendingRange) {{ window.getSelection().removeAllRanges(); pendingRange = null; }}
  }}

  function showPopover(x, y, anchor, range) {{
    pendingAnchor = anchor;
    pendingRange = range;
    annQuote.textContent = '"' + anchor.text.slice(0, 120) + (anchor.text.length > 120 ? '…' : '') + '"';
    popover.style.display = 'block';
    let px = x, py = y + 12;
    if (px + popover.offsetWidth > window.innerWidth - 16) px = window.innerWidth - popover.offsetWidth - 16;
    if (py + popover.offsetHeight > window.innerHeight - 16) py = y - popover.offsetHeight - 12;
    popover.style.left = px + 'px';
    popover.style.top = py + 'px';
    setTimeout(() => annText.focus(), 50);
  }}

  // ── Selection listener ────────────────────────────────────────────────────
  document.addEventListener('mouseup', e => {{
    if (popover.contains(e.target)) return;
    const sel = window.getSelection();
    if (!sel || sel.isCollapsed) return;
    const text = sel.toString().trim();
    if (text.length < 3) return;
    const main = document.querySelector('main');
    if (!main) return;
    const range = sel.getRangeAt(0);
    if (!main.contains(range.commonAncestorContainer)) return;
    const anchor = getContext(range);
    if (!anchor) return;
    showPopover(e.clientX, e.clientY, anchor, range);
  }});

  document.addEventListener('mousedown', e => {{
    if (!popover.contains(e.target)) hidePopover();
  }});

  // ── Export / clear bar ────────────────────────────────────────────────────
  const bar = document.getElementById('ann-bar');

  function updateBar() {{
    const anns = loadDoc();
    bar.style.display = anns.length > 0 ? 'flex' : 'none';
  }}

  document.getElementById('ann-export').addEventListener('click', () => {{
    const anns = loadDoc();
    if (!anns.length) return;
    const lines = ['# Annotations — ' + DOC_KEY, ''];
    anns.forEach((a, i) => {{
      lines.push('## ' + (i+1) + '. ' + a.created.slice(0,10));
      lines.push('> ' + a.anchor.text);
      lines.push('');
      lines.push(a.comment);
      lines.push('');
    }});
    navigator.clipboard.writeText(lines.join('\\n')).then(() => {{
      const btn = document.getElementById('ann-export');
      const orig = btn.textContent;
      btn.textContent = 'Copied!';
      setTimeout(() => {{ btn.textContent = orig; }}, 1800);
    }});
  }});

  document.getElementById('ann-clear').addEventListener('click', () => {{
    if (confirm('Delete all annotations on this page?')) {{
      saveDoc([]);
      renderAll();
    }}
  }});

  // ── Init ──────────────────────────────────────────────────────────────────
  renderAll();
}})();
</script>
</body>
</html>"""


# ── Index builder ──────────────────────────────────────────────────────────────

FOLDER_META = {
    "architecture": ("Architecture", "System design, scalability, and operational context"),
    "editorial":    ("Editorial",    "Project principles, voice, and style"),
    "design":       ("Design",       "Visual identity, period colours, and typographic system"),
    "pwa":          ("PWA",          "E-reader, local-first architecture, and tl pipeline"),
    "_root":        ("Root",         "Top-level documents"),
}
FOLDER_ORDER = ["architecture", "editorial", "design", "pwa", "_root"]


def _extract_lede_md(md_path: Path) -> str:
    try:
        text = md_path.read_text(encoding="utf-8")
        if text.startswith("---"):
            end = text.find("---", 3)
            if end != -1:
                text = text[end+3:]
        for line in text.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith(">") \
               and not line.startswith("---") and len(line) > 30:
                return line[:140] + ("…" if len(line) > 140 else "")
    except Exception:
        pass
    return ""


def _extract_title_md(md_path: Path) -> str:
    try:
        text = md_path.read_text(encoding="utf-8")
        if text.startswith("---"):
            end = text.find("---", 3)
            if end != -1:
                fm = text[3:end]
                for line in fm.splitlines():
                    if line.startswith("title:"):
                        return line.partition(":")[2].strip().strip('"')
                text = text[end+3:]
        m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return md_path.stem.replace("-", " ").title()


# Hand-authored HTML docs (no .md sibling) carry their own title/description.
# Strip the site suffix so the index card title isn't repetitive.
_HTML_TITLE_SUFFIXES = (" — tolstoy.life docs", " — tolstoy.life")


def _extract_title_html(html_path: Path) -> str:
    try:
        text = html_path.read_text(encoding="utf-8")
        m = re.search(r"<title>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
        if m:
            title = re.sub(r"\s+", " ", m.group(1)).strip()
            for suffix in _HTML_TITLE_SUFFIXES:
                if title.endswith(suffix):
                    title = title[:-len(suffix)].strip()
            return title
    except Exception:
        pass
    return html_path.stem.replace("-", " ").title()


def _extract_lede_html(html_path: Path) -> str:
    try:
        text = html_path.read_text(encoding="utf-8")
        m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']',
                      text, re.IGNORECASE)
        if m:
            return m.group(1).strip()[:160]
        m = re.search(r'<p[^>]*class=["\']lede["\'][^>]*>(.*?)</p>',
                      text, re.IGNORECASE | re.DOTALL)
        if m:
            lede = re.sub(r"<[^>]+>", "", m.group(1))
            lede = re.sub(r"\s+", " ", lede).strip()
            return lede[:140] + ("…" if len(lede) > 140 else "")
    except Exception:
        pass
    return ""


def extract_title(path: Path) -> str:
    return _extract_title_html(path) if path.suffix == ".html" else _extract_title_md(path)


def extract_lede(path: Path) -> str:
    return _extract_lede_html(path) if path.suffix == ".html" else _extract_lede_md(path)


def build_index(docs: dict) -> str:
    featured_paths = [ROOT / rel for rel in FEATURED]
    featured_set = {p.resolve() for p in featured_paths if p.exists()}

    featured_html = ""
    for path in featured_paths:
        if not path.exists():
            continue
        title = extract_title(path)
        lede = extract_lede(path)
        mtime = datetime.fromtimestamp(path.stat().st_mtime).strftime("%-d %b %Y")
        rel = path.relative_to(ROOT)
        folder = rel.parts[0] if len(rel.parts) > 1 else "_root"
        href = "/" + str(rel.with_suffix(".html"))
        featured_html += f"""
    <div class="featured-section">
      <a class="featured-card" href="{href}">
        <p class="eyebrow">Featured</p>
        <div class="card-title">{title}</div>
        <div class="card-meta">{folder} · {mtime}</div>
        {"<p class='card-lede'>" + lede + "</p>" if lede else ""}
      </a>
    </div>"""

    sections_html = ""
    for folder in FOLDER_ORDER:
        files = [f for f in docs.get(folder, []) if f.resolve() not in featured_set]
        if not files:
            continue
        label, desc = FOLDER_META.get(folder, (folder.title(), ""))
        cards = ""
        for path in sorted(files, key=lambda p: p.stat().st_mtime, reverse=True):
            title = extract_title(path)
            lede = extract_lede(path)
            mtime = datetime.fromtimestamp(path.stat().st_mtime).strftime("%-d %b %Y")
            rel = path.relative_to(ROOT)
            href = "/" + str(rel.with_suffix(".html"))
            cards += f"""
      <a class="index-card" href="{href}">
        <div class="card-title">{title}</div>
        <div class="card-meta">{folder} · {mtime}</div>
        {"<div class='card-lede'>" + lede + "</div>" if lede else ""}
      </a>"""

        sections_html += f"""
    <p class="section-label">{label} — {desc}</p>
    <div class="index-grid">{cards}
    </div>"""

    now = datetime.now().strftime("%-d %B %Y, %H:%M")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>docs — tolstoy.life</title>
<style>{CSS}</style>
</head>
<body>
<div class="site-header">
  <a class="home" href="/INDEX.html">tolstoy.life / docs</a>
</div>
<header class="doc-header">
  <p class="eyebrow">tolstoy.life</p>
  <h1>Documentation</h1>
  <p class="meta">Generated {now}</p>
</header>
{featured_html}
<main>
  <p style="color:var(--ink-soft);font-style:italic;margin-bottom:2rem">
    Architecture, editorial principles, and technical specifications.
    Tracked in git. Start a local server with <code>python3 serve.py</code>
    from <code>docs/</code>.
  </p>
  {sections_html}
</main>
<footer>tolstoy.life · public documentation</footer>
</body>
</html>"""


# ── Build pipeline ─────────────────────────────────────────────────────────────

def collect_md_files() -> dict:
    docs = {}
    for path in ROOT.rglob("*.md"):
        parts = path.relative_to(ROOT).parts
        if any(p in SKIP_DIRS for p in parts):
            continue
        if path.name in SKIP_FILES:
            continue
        if len(parts) == 1:
            folder = "_root"
        else:
            folder = parts[0]
        docs.setdefault(folder, []).append(path)
    return docs


def collect_orphan_html_files() -> dict:
    """Hand-authored HTML docs (no .md sibling) live alongside generated HTML."""
    docs = {}
    for path in ROOT.rglob("*.html"):
        parts = path.relative_to(ROOT).parts
        if any(p in SKIP_DIRS for p in parts):
            continue
        if path.name == "INDEX.html":
            continue
        if path.with_suffix(".md").exists():
            continue
        if len(parts) == 1:
            folder = "_root"
        else:
            folder = parts[0]
        docs.setdefault(folder, []).append(path)
    return docs


def merge_doc_files(*sources: dict) -> dict:
    merged = {}
    for src in sources:
        for folder, files in src.items():
            merged.setdefault(folder, []).extend(files)
    return merged


def build_all(verbose=True):
    md_docs = collect_md_files()
    html_docs = collect_orphan_html_files()
    count = 0
    for folder, files in md_docs.items():
        for md_path in files:
            html_path = md_path.with_suffix(".html")
            html = md_to_html(md_path)
            html_path.write_text(html, encoding="utf-8")
            if verbose:
                print(f"  ✓ {md_path.relative_to(ROOT)}")
            count += 1

    index_html = build_index(merge_doc_files(md_docs, html_docs))
    (ROOT / "INDEX.html").write_text(index_html, encoding="utf-8")
    if verbose:
        print(f"  ✓ INDEX.html")
        orphans = sum(len(v) for v in html_docs.values())
        suffix = f" + {orphans} hand-authored HTML" if orphans else ""
        print(f"\n{count} documents converted{suffix}.")
    return count


# ── HTTP server ────────────────────────────────────────────────────────────────

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path = self.path.split("?")[0].lstrip("/")
        if path == "" or path == "INDEX.html":
            build_all(verbose=False)
        else:
            md_equiv = ROOT / Path(path).with_suffix(".md")
            if md_equiv.exists():
                html = md_to_html(md_equiv)
                html_path = md_equiv.with_suffix(".html")
                html_path.write_text(html, encoding="utf-8")
        super().do_GET()

    def log_message(self, fmt, *args):
        if args and str(args[1]) not in ("200", "304"):
            super().log_message(fmt, *args)


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="docs/ document server — tolstoy.life")
    parser.add_argument("--port", type=int, default=7866,
                        help="Port to serve on (default: 7866)")
    parser.add_argument("--build-only", action="store_true",
                        help="Convert md→html and exit without starting server")
    args = parser.parse_args()

    print("Building documents…")
    build_all()

    if args.build_only:
        return

    with socketserver.TCPServer(("", args.port), Handler) as httpd:
        httpd.allow_reuse_address = True
        url = f"http://localhost:{args.port}/INDEX.html"
        print(f"\nServing at {url}")
        print("Documents rebuild on each page load. Ctrl-C to stop.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
