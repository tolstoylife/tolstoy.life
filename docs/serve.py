#!/usr/bin/env python3
"""
docs/ document server — tolstoy.life
======================================
Converts all .md files in docs/ to HTML on startup (and on request),
then serves them with live navigation via INDEX.html.

Every page gets the universal reading shell (top bar, TOC drawer, Tools
overlay, themes, annotations). Reader-edition bundles — a `<work>.<version>.md`
beside `build/segments.<version>.json` — additionally render from segments
with sentence spans, a version switch, editorial layers, and (where
`build/timing.<version>.json` + audio exist) read-along.
Static shell assets live in reader/assets/{shell.css,shell.js,annotations.js,readalong.js}.

Usage:
    cd /Volumes/Graugear/Tolstoy/docs
    python3 serve.py            # serves on http://localhost:7866
    python3 serve.py --port 8001
    python3 serve.py --build-only   # convert md→html without starting server
"""

import argparse
import http.server
import importlib.util
import json
import os
import re
import socketserver
import sys
from datetime import datetime
from html import escape as esc
from pathlib import Path
from urllib.parse import quote, unquote

# ── Dependencies ───────────────────────────────────────────────────────────────

def require(package, pip_name=None):
    if importlib.util.find_spec(package) is None:
        name = pip_name or package
        print(f"Installing {name}…")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", name,
                               "--break-system-packages", "-q"])

require("markdown")
require("pymdownx", "pymdown-extensions")
import markdown
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension

# ── Paths ──────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.resolve()

SKIP_DIRS  = {".git", ".claude", ".omc", ".pytest_cache", "__pycache__", "node_modules"}
SKIP_FILES = {"serve.py", "404.md"}  # 404.md is built by publish.py, not listed
PASSTHROUGH_EXTENSIONS = {".html", ".pdf", ".pptx", ".mp3", ".jpg", ".png",
                           ".svg", ".yaml", ".yml", ".skill", ".json"}

# Hand-authored HTML doesn't carry YAML frontmatter, so layer/date for
# orphan HTML files is declared explicitly here. .md files use their own
# frontmatter — see Phase 1 of the docs→dev-blog migration.
HTML_META = {
    "architecture/architecture-review.html":  {"layer": "blog", "date": "2026-05-09"},
    "design/period-colours-preview.html":     {"layer": "blog", "date": "2026-04-26"},
}

# ── Page chrome (the reading shell) ────────────────────────────────────────────
# Styling lives in reader/assets/shell.css; behaviour in shell.js /
# annotations.js / readalong.js. These constants are plain strings (not
# f-strings) so their braces need no doubling.

# Applies saved theme/type settings before first paint (no flash).
HEAD_SNIPPET = """
(function(){try{var s=JSON.parse(localStorage.getItem('tolstoy_reader_settings')||'{}');
var h=document.documentElement;h.dataset.theme=s.theme||'paper';
h.style.setProperty('--font-scale',s.fontScale||1);
if(s.measure)h.style.setProperty('--measure',s.measure+'ch');
var L=s.layers||{};['wikilinks','cuts','footnotes'].forEach(function(k){
h.dataset['l'+k[0].toUpperCase()+k.slice(1)]=L[k]?'on':'off';});}catch(e){}})();
""".strip()

# Inline icon symbols — copied from the UI drafts (Tabler-outline style):
# _generated/design/session-reader-ui-drafts-2026-07-03/reader-ui-drafts.html
ICONS = """
<svg style="display:none" aria-hidden="true">
  <symbol id="i-list" viewBox="0 0 24 24"><line x1="4" y1="6" x2="20" y2="6"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="18" x2="20" y2="18"/></symbol>
  <symbol id="i-note" viewBox="0 0 24 24"><rect x="5" y="4" width="14" height="16" rx="2"/><line x1="8.5" y1="9" x2="15.5" y2="9"/><line x1="8.5" y1="13" x2="15.5" y2="13"/></symbol>
  <symbol id="i-tools" viewBox="0 0 24 24"><line x1="4" y1="8" x2="20" y2="8"/><circle cx="14" cy="8" r="2.6"/><line x1="4" y1="16" x2="20" y2="16"/><circle cx="9" cy="16" r="2.6"/></symbol>
  <symbol id="i-focus" viewBox="0 0 24 24"><path d="M4 8 V4 H8"/><path d="M16 4 H20 V8"/><path d="M20 16 V20 H16"/><path d="M8 20 H4 V16"/></symbol>
  <symbol id="i-min" viewBox="0 0 24 24"><path d="M4 8 H8 V4"/><path d="M20 8 H16 V4"/><path d="M4 16 H8 V20"/><path d="M20 16 H16 V20"/></symbol>
  <symbol id="i-play" viewBox="0 0 24 24"><path d="M7 5v14l12-7z"/></symbol>
  <symbol id="i-pause" viewBox="0 0 24 24"><line x1="9" y1="5" x2="9" y2="19"/><line x1="15" y1="5" x2="15" y2="19"/></symbol>
</svg>
"""

TOC_DRAWER = """
<nav id="toc-drawer" aria-label="Contents">
  <button class="panel-close" title="Close">✕</button>
  <h2>Contents</h2>
  <ol></ol>
</nav>
"""

NOTES_PANEL = """
<aside id="notes-panel" role="dialog" aria-label="Notes">
  <button class="panel-close" title="Close">✕</button>
  <h2>Notes</h2>
  <ul id="notes-list"></ul>
  <div class="notes-actions">
    <button id="notes-copytext">Copy as text</button>
    <button id="notes-export">Copy JSON-LD</button>
    <button id="notes-import">Import…</button>
    <button id="notes-send">Send to the project</button>
    <button id="notes-clear" class="danger">Clear all</button>
  </div>
  <div id="notes-send-row" hidden>
    <input type="email" id="notes-email" placeholder="Your email, if you'd like a reply" autocomplete="email">
    <p class="notes-send-note">Sends the notes on this page and its address. Nothing else is collected, and the email is optional.</p>
    <div class="notes-actions"><button id="notes-send-go">Send</button></div>
  </div>
</aside>
"""

TOOLS_DISPLAY = """
  <h3>Display</h3>
  <div class="tool-row"><span>Text size</span>
    <span class="stepper"><button id="font-smaller" title="Smaller" aria-label="Smaller text">−</button><span class="aa">Aa</span><button id="font-larger" title="Larger" aria-label="Larger text">+</button></span></div>
  <div class="tool-slider">
    <div class="tool-row"><span>Line length</span><output id="measure-out">56 ch</output></div>
    <input type="range" class="track" id="measure-range" min="48" max="82" step="1" value="56" aria-label="Line length">
  </div>
  <div class="tool-row"><span>Theme</span>
    <span class="dots">
      <button class="dot paper" data-theme-pick="paper" title="Paper" aria-label="Paper theme"></button>
      <button class="dot sepia" data-theme-pick="sepia" title="Sepia" aria-label="Sepia theme"></button>
      <button class="dot dark" data-theme-pick="dark" title="Dark" aria-label="Dark theme"></button>
    </span></div>
"""

TOOLS_LAYERS = """
  <h3>Layers</h3>
  <label class="tool-row">Wikilinks <input type="checkbox" class="sw" data-layer="wikilinks"></label>
  <label class="tool-row">Editorial cuts <input type="checkbox" class="sw" data-layer="cuts"></label>
  <label class="tool-row">Footnotes <input type="checkbox" class="sw" data-layer="footnotes"></label>
"""

ANNOTATION_UI = """
<div id="ann-popover">
  <div class="ann-quote" id="ann-quote"></div>
  <textarea id="ann-text" placeholder="Your comment…" autocomplete="off"></textarea>
  <label class="ann-fix"><input type="checkbox" id="ann-fix"> 🔧 Needs a text fix</label>
  <div class="ann-actions">
    <button id="ann-cancel">Cancel</button>
    <button class="primary" id="ann-save">Save</button>
  </div>
</div>
<div id="ann-tooltip"></div>
"""

TRANSPORT = """
<div id="transport">
  <button id="rl-play" title="Play / pause" aria-label="Play or pause"><svg class="ic"><use id="rl-play-icon" href="#i-play"/></svg></button>
  <span class="rl-section" id="rl-sec">–/–</span>
  <input type="range" class="track" id="rl-seek" min="0" max="100" step="0.1" value="0" title="Seek" aria-label="Seek">
  <span class="rl-time" id="rl-time">0:00 / 0:00</span>
  <button id="rl-speed" title="Playback speed">1×</button>
  <a href="/reader/index.html" title="Back to the library">⌂</a>
</div>
"""


def page_shell(*, title, eyebrow, heading, meta_line, body_html, config,
               kind="doc", home_html="", lib_html="", crumb_html="",
               hub_title="", hub_html="", tools_extra="",
               readalong=False, lang="en"):
    """Wrap rendered content in the universal reading shell."""
    tools = f"""
<aside id="tools-overlay" role="dialog" aria-label="Reading tools">
  <button class="panel-close" title="Close">✕</button>
{TOOLS_DISPLAY}
{tools_extra}
</aside>"""
    transport = TRANSPORT if readalong else ""
    readalong_js = '\n<script src="/reader/assets/readalong.js"></script>' if readalong else ""
    audio_attr = ' data-audio="true"' if readalong else ""
    ident = (f'<nav class="tb-crumb">{crumb_html}</nav>' if crumb_html
             else f'<span class="tb-title">{title}</span>')
    div = '<span class="tb-div">|</span>'
    _fixed = [x for x in (home_html, lib_html) if x]
    left_nav = (div.join(_fixed) + div if _fixed else "") + (
        '<button id="tb-contents" title="Contents" aria-label="Contents">'
        '<svg class="ic"><use href="#i-list"/></svg></button>') + ident
    if hub_html:
        drawer = f"""<nav id="toc-drawer" aria-label="Contents">
  <button class="panel-close" title="Close">✕</button>
  <h2 class="work">{hub_title}</h2>
  <ul class="hub">
{hub_html}
  </ul>
  <h3 class="onpage">On this page</h3>
  <ol></ol>
</nav>"""
    else:
        drawer = TOC_DRAWER
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — tolstoy.life research</title>
<script>{HEAD_SNIPPET}</script>
<link rel="stylesheet" href="/reader/assets/shell.css">
</head>
<body data-kind="{kind}"{audio_attr}>
{ICONS}
<div id="progress"><div class="fill"></div></div>
<header id="topbar">
  <div class="tb-group">
    {left_nav}
  </div>
  <div class="tb-group">
    <button id="tb-notes" title="Notes" aria-label="Notes"><svg class="ic"><use href="#i-note"/></svg></button>
    <button id="tb-zen" title="Focus — fullscreen reading" aria-label="Focus"><svg class="ic"><use id="zen-icon" href="#i-focus"/></svg></button>
    <button id="tb-tools" class="gear" title="Tools" aria-label="Tools"><svg class="ic"><use href="#i-tools"/></svg></button>
  </div>
</header>
{drawer}
{tools}
{NOTES_PANEL}
<header class="doc-header">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{heading}</h1>
  <p class="meta">{meta_line}</p>
</header>
<main>
{body_html}
</main>
<footer>tolstoy.life · public documentation</footer>
{ANNOTATION_UI}
{transport}
<script>window.READER = {json.dumps(config)};</script>
<script src="/reader/assets/shell.js"></script>
<script src="/reader/assets/annotations.js"></script>{readalong_js}
</body>
</html>"""


# ── Markdown → HTML ────────────────────────────────────────────────────────────

from markdown.extensions.wikilinks import WikiLinkExtension

def wiki_url(label: str, base: str, end: str) -> str:
    """`[[Henry George]]` → `/research/wiki/Henry%20George.html`.

    The extension's default builder substitutes underscores for spaces, but the
    filename here IS the title (the Obsidian convention that keeps wikilinks
    working in the vault), so the space is preserved and percent-encoded instead.
    """
    return f"{base}{quote(label)}{end}"

MD = markdown.Markdown(extensions=[
    TableExtension(),
    FencedCodeExtension(),
    # ponytail: no nl2br — a single newline in wrapped source is a soft wrap, not a
    # <br> (Markdown spec). Intended breaks still work via two trailing spaces.
    "sane_lists",
    "attr_list",
    "footnotes",            # the work's own authorial/translator notes ([^n])
    "pymdownx.critic",      # editorial marks: {--cut--} {++add++} {~~a~>b~~} {>>note<<} {==hi==}
    WikiLinkExtension(base_url="/research/wiki/", end_url=".html",
                      html_class="wikilink", build_url=wiki_url),
])

# serve.py lives in docs/, so the repo root isn't on sys.path by default — add it
# so the shared reader/ helpers import (web + EPUB share the same ID rule).
_REPO_ROOT = str(Path(__file__).resolve().parent.parent)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)
from reader.paragraph_ids import add_paragraph_ids
from reader import ids as reader_ids

_WIKILINK_A_RE = re.compile(r'<a class="wikilink" href="/research/wiki/([^"]+)\.html"')

def mark_missing_wikilinks(html: str) -> str:
    """Flag `[[links]]` whose page isn't written yet, so a dead end is visible.

    Most entities legitimately have no page — the vault is a universe, not a
    queue — so these stay clickable and keep their layer-toggle behaviour; they
    just stop looking like a promise the preview can keep.
    """
    def repl(mo):
        name = unquote(mo.group(1))
        if (ROOT / "research" / "wiki" / f"{name}.md").exists():
            return mo.group(0)
        return mo.group(0).replace(
            'class="wikilink"', 'class="wikilink wikilink-missing" title="No page yet"')
    return _WIKILINK_A_RE.sub(repl, html)

PSS_ABBR = '<abbr title="Полное собрание сочинений — the 90-volume Jubilee edition of the complete works">PSS</abbr>'

def abbr_pss(html: str) -> str:
    """A bare PSS in running text gets its <abbr>; one already in <abbr>, <code> or <pre>, or inside a tag, is left alone."""
    out, inside = [], 0
    for part in re.split(r"(<[^>]+>)", html):
        if part.startswith("<"):
            m = re.match(r"<(/?)(abbr|code|pre)\b", part)
            if m:
                inside += -1 if m.group(1) else 1
        elif not inside:
            part = re.sub(r"\bPSS\b", PSS_ABBR, part)
        out.append(part)
    return "".join(out)

def render_body(text: str) -> str:
    """Convert a Markdown string (CriticMarkup, footnotes, [[wikilinks]]) to an HTML fragment."""
    MD.reset()
    return add_paragraph_ids(abbr_pss(mark_missing_wikilinks(MD.convert(text))))


# ── Dive cross-link resolution (post-2026-07 folder move) ───────────────────────
# The move relocated every dive from flat  research/<slug>/  into
# research/{works/<genre>/<subcat>,themes,_meta}/<slug>/  (and renamed a few
# slugs). Existing dives still link each other with the old flat  ../<slug>/… ,
# which now misses on both ends. Rewrite those `../…` links at render time to the
# real location — move-map.tsv gives old-path → new-path, and current folder names
# cover dives written since. Links that don't resolve (website/ draft-note
# pointers, not-yet-created siblings) are left untouched.
_DIVE_ALIAS = None

def _dive_alias() -> dict:
    """old-slug / current-folder-name / moved-file-path → new root-relative path."""
    global _DIVE_ALIAS
    if _DIVE_ALIAS is None:
        research = ROOT / "research"
        alias = {}
        for idx in (list(research.glob("works/**/index.md"))
                    + list(research.glob("themes/*/index.md"))
                    + list(research.glob("_meta/*/index.md"))):
            alias[idx.parent.name] = idx.parent.relative_to(ROOT).as_posix()
        mm = research / "_meta" / "move-map.tsv"
        if mm.exists():
            for line in mm.read_text(encoding="utf-8").splitlines():
                if "\t" not in line:
                    continue
                old, new = (x.strip() for x in line.split("\t", 1))
                if old and new:
                    alias.setdefault(old, "research/" + new)   # current names win
        _DIVE_ALIAS = alias
    return _DIVE_ALIAS

_DIVE_HREF_RE = re.compile(r'(href=")(\.\./[^"#]*)(#[^"]*)?(")')

def resolve_dive_links(html: str) -> str:
    """Rewrite flat-era `../<slug>/…` dive links to their real post-move URL."""
    alias = _dive_alias()
    research = ROOT / "research"
    def repl(mo):
        pre, raw, frag, post = mo.group(1), mo.group(2), mo.group(3) or "", mo.group(4)
        rest = re.sub(r"^(\.\./)+", "", raw)
        if rest in alias:                             # a moved file/dir, matched whole
            return f"{pre}/{alias[rest]}{frag}{post}"
        seg0 = rest.split("/", 1)[0]
        if seg0 in alias:                             # a dive dir + trailing /index.html
            return f"{pre}/{alias[seg0]}{rest[len(seg0):]}{frag}{post}"
        if (research / rest).exists():                # never moved (lib/, shared docs)
            return f"{pre}/research/{rest}{frag}{post}"
        return mo.group(0)                            # dangling → leave as authored
    return _DIVE_HREF_RE.sub(repl, html)


# ── Work reader (reader-edition bundles) ───────────────────────────────────────

def work_version_of(md_path: Path):
    """`the-great-sin.en-1905.md` + sibling `build/segments.en-1905.json`
    → ("the-great-sin", "en-1905"); anything else → None."""
    stem = md_path.stem
    if "." not in stem:
        return None
    work, _, version = stem.rpartition(".")
    if (md_path.parent / "build" / f"segments.{version}.json").exists():
        return (work, version)
    return None


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _version_label(version: str) -> str:
    if version.startswith("en-machine"):
        return "MT"
    if version.startswith("en"):
        return "EN"
    if version.startswith("ru"):
        return "RU"
    return version.upper()


def _version_order(version: str):
    return (0 if version.startswith("ru")
            else 2 if version.startswith("en-machine") else 1, version)


def _read_order(version: str):
    """Which edition the overview's Read button opens first: published EN,
    then RU, then machine translation."""
    return (0 if version.startswith("en") and not version.startswith("en-machine")
            else 1 if version.startswith("ru") else 2, version)


def bundle_editions(bundle: Path):
    """Reader editions in a bundle dir, best-read-first: [(work, version), …]."""
    found = [wv for p in sorted(bundle.glob("*.md")) for wv in [work_version_of(p)] if wv]
    return sorted(found, key=lambda wv: _read_order(wv[1]))


# ── Per-work navigation: the Docs | Library | ☰ Work crumb + the Contents hub ────
# The Contents drawer lists every page of a work (its editions + apparatus pages +
# the research dive/annotations), auto-built from the bundle folder and its dive
# folder so it stays in sync as pages come and go.

_PAGE_LABELS = {
    "restored-text.md": "Restored text",
    "translation-diagnostic.md": "Fidelity report",
    "alignment-notes.md": "Alignment notes",
    "index.md": "The corpus dive",
    "annotations.md": "Reading annotations",
}
_HUB_APPARATUS = ["restored-text.md", "translation-diagnostic.md", "alignment-notes.md"]


def _edition_year(bundle: Path, version: str) -> str:
    """4-digit year for an edition whose version tag isn't itself a year
    (e.g. en-wiener → 1904, read from meta.<version>.json's date)."""
    meta_path = bundle / f"meta.{version}.json"
    if meta_path.exists():
        m = re.search(r"\d{4}", str(_load_json(meta_path).get("date", "")))
        if m:
            return m.group()
    return ""


def _edition_label(version: str, readalong: bool = False, verbose: bool = False,
                   year: str = "") -> str:
    # verbose = the spelled-out drawer/body form; terse (default) = the crumb form.
    if version.startswith("en-machine"):
        base = "English (machine translation)" if verbose else "English (machine)"
    elif version.startswith("en"):
        suffix = version.split("-", 1)[1] if "-" in version else ""
        if suffix[:4].isdigit():
            base = f"English, {suffix}"
        elif year:
            # named-translator edition (e.g. en-wiener): year from meta.json,
            # translator spelled out in the drawer/body form only.
            name = suffix.replace("-", " ").title()
            base = f"English, {year} ({name})" if verbose and name else f"English, {year}"
        else:
            base = "English"
    elif version.startswith("ru"):
        base = "Русский (Russian version)" if verbose else "Русский"
    else:
        base = version.upper()
    return base + (" · read-along" if readalong else "")


def _page_label(md_path: Path, work: str) -> str:
    """Short label for a work's page — shared by the crumb tail and the hub."""
    if md_path.name == "overview.md":
        return "Overview"
    wv = work_version_of(md_path)
    if wv:
        return _edition_label(wv[1], year=_edition_year(md_path.parent, wv[1]))
    return (_PAGE_LABELS.get(md_path.name) or _extract_title_md(md_path)
            or md_path.stem.replace("-", " ").title())


_WORK_INDEX = None

def _work_index():
    """One row per reader bundle: (bundle_dir, work_slug, work_title, dive_dir|None).

    ponytail: memoized for the process — a bundle or page added while serve.py is
    running appears on restart (same contract as _DIVE_ALIAS).
    """
    global _WORK_INDEX
    if _WORK_INDEX is None:
        rows = []
        for ov in sorted(ROOT.glob("reader/**/overview.md")):
            bundle = ov.parent
            eds = bundle_editions(bundle)
            work = eds[0][0] if eds else bundle.name
            title = _extract_title_md(ov) or work.replace("-", " ").title()
            dive = next(ROOT.glob(f"research/works/**/*-{work}/index.md"), None)
            rows.append((bundle, work, title, dive.parent if dive else None))
        _WORK_INDEX = rows
    return _WORK_INDEX


def work_context(md_path: Path):
    """The work a page belongs to — whether it lives in the reader bundle or in
    the research dive folder — or None for a plain doc page."""
    parent = md_path.parent
    for bundle, work, title, dive_dir in _work_index():
        if parent == bundle or parent == dive_dir:
            return (bundle, work, title, dive_dir)
    return None


def work_hub_html(bundle: Path, work: str, dive_dir, current_url: str) -> str:
    """The per-work page list for the Contents drawer, in reading order."""
    def u(p: Path) -> str:
        return "/" + p.relative_to(ROOT).with_suffix(".html").as_posix()
    items = []  # (href, label)
    ov = bundle / "overview.md"
    if ov.exists():
        items.append((u(ov), "Overview"))
    for w, v in bundle_editions(bundle):
        ra = (bundle / "build" / f"timing.{v}.json").exists() and v.startswith("en")
        items.append((u(bundle / f"{w}.{v}.md"),
                      _edition_label(v, ra, verbose=True, year=_edition_year(bundle, v))))
    for name in _HUB_APPARATUS:
        if (bundle / name).exists():
            items.append((u(bundle / name), _PAGE_LABELS[name]))
    if dive_dir:
        for name in ("index.md", "annotations.md"):
            if (dive_dir / name).exists():
                items.append((u(dive_dir / name), _PAGE_LABELS[name]))
    lis = []
    for href, label in items:
        cur = ' class="current" aria-current="page"' if href == current_url else ""
        lis.append(f'    <li><a href="{href}"{cur}>{esc(label)}</a></li>')
    return "\n".join(lis)


def nav_for(md_path: Path) -> dict:
    """Top-bar identity + Contents hub for a page: Docs | Library | ☰ Work ›
    Subpage, with the drawer listing every page of the work. Plain docs get
    just the Docs link."""
    nav = {"home_html": '<a class="tb-home" href="/INDEX.html">Research</a>',
           "lib_html": "", "crumb_html": "", "hub_title": "", "hub_html": ""}
    ctx = work_context(md_path)
    if not ctx:
        return nav
    bundle, work, title, dive_dir = ctx
    current_url = "/" + md_path.relative_to(ROOT).with_suffix(".html").as_posix()
    nav["lib_html"] = '<a class="tb-lib" href="/reader/index.html">Library</a>'
    nav["hub_title"] = esc(title)
    nav["hub_html"] = work_hub_html(bundle, work, dive_dir, current_url)
    ov_url = "/" + (bundle / "overview.md").relative_to(ROOT).with_suffix(".html").as_posix()
    crumb = f'<a class="here" href="{ov_url}">{esc(title)}</a>'
    if md_path.name != "overview.md":
        crumb += f'<span class="sep">›</span><span class="sub">{esc(_page_label(md_path, work))}</span>'
    nav["crumb_html"] = crumb
    return nav


def _render_sentence_web(text: str) -> str:
    """Sentence display text → HTML: [^label] markers become noterefs, the rest
    is escaped. The web twin of build_xhtml._render_sentence (same ids, no
    epub: attributes)."""
    out = []
    for part in re.split(r"(\[\^\w+\])", text):
        m = re.fullmatch(r"\[\^(\w+)\]", part)
        if m:
            label = m.group(1)
            nid = reader_ids.note_id(int(label)) if label.isdigit() else f"note-{label}"
            out.append(f'<a class="noteref" href="#{nid}"><sup>{esc(label)}</sup></a>')
        else:
            out.append(esc(part))
    return "".join(out)


def work_page_html(md_path: Path, work: str, version: str) -> str:
    """Render a reader-edition page from its segments.json — each sentence a
    <span class="sentence" id=…> inside <p id=…>, exactly the coordinates
    timing.json and the EPUB use."""
    bundle = md_path.parent
    seg = _load_json(bundle / "build" / f"segments.{version}.json")

    meta_path = bundle / f"meta.{version}.json"
    meta = _load_json(meta_path) if meta_path.exists() else {}

    # Body: sections → paragraphs → sentence spans (+ end-of-text notes)
    parts = []
    for sec in seg["sections"]:
        parts.append(f'<h2 id="{sec["id"]}">{esc(sec["heading"])}</h2>')
        for p in sec["paragraphs"]:
            spans = " ".join(
                f'<span class="sentence" id="{s["id"]}">{_render_sentence_web(s["display"])}</span>'
                for s in p["sentences"])
            parts.append(f'<p id="{p["id"]}">{spans}</p>')
    notes = seg.get("notes") or []
    if notes:
        asides = "\n".join(f'<aside id="{n["id"]}"><p>{n["html"]}</p></aside>' for n in notes)
        parts.append(f'<section class="work-notes">{asides}</section>')
    body_html = "\n".join(parts)

    # Version switch: sibling editions that exist as both segments + md
    versions = sorted(
        (p.name[len("segments."):-len(".json")] for p in (bundle / "build").glob("segments.*.json")),
        key=_version_order)
    links = []
    for v in versions:
        if not (bundle / f"{work}.{v}.md").exists():
            continue
        cur = " current" if v == version else ""
        links.append(f'<a class="version-link{cur}" data-v="{v}" '
                     f'href="{work}.{v}.html">{_version_label(v)}</a>')
    version_html = ""
    if len(links) > 1:
        version_html = f'\n  <h3>Version</h3>\n  <div class="seg">{"".join(links)}</div>'

    # Top bar + Contents hub: Docs | Library | ☰ Work › <edition>
    title = meta.get("title") or work.replace("-", " ").title()
    nav = nav_for(md_path)
    author = meta.get("author", "")
    date = meta.get("date", "")
    eyebrow = " · ".join(x for x in [author, date, "reader edition"] if x)
    meta_bits = []
    if meta.get("translator"):
        meta_bits.append(f"Translated by {esc(meta['translator'])}")
    if meta.get("source"):
        meta_bits.append(esc(meta["source"]))
    rel = md_path.relative_to(ROOT)
    meta_bits.append(f'<a href="/{rel}">view source</a>')

    doc_key = "docs/" + str(rel.with_suffix(""))
    config = {"docKey": doc_key, "kind": "work", "work": work, "version": version}
    timing = bundle / "build" / f"timing.{version}.json"
    readalong = timing.exists() and version.startswith("en")
    if readalong:
        config["readalong"] = {"timing": f"build/timing.{version}.json"}

    return page_shell(
        title=esc(title),
        eyebrow=esc(eyebrow),
        heading=esc(title),
        meta_line=" · ".join(meta_bits),
        body_html=body_html,
        config=config,
        kind="work",
        home_html=nav["home_html"],
        lib_html=nav["lib_html"],
        crumb_html=nav["crumb_html"],
        hub_title=nav["hub_title"],
        hub_html=nav["hub_html"],
        tools_extra=TOOLS_LAYERS + version_html,
        readalong=readalong,
        lang="ru" if version.startswith("ru") else "en",
    )


def md_to_html(md_path: Path) -> str:
    """Convert a markdown file to a full HTML page (or a work-reader page
    when the file is a reader-edition version with built segments)."""
    wv = work_version_of(md_path)
    if wv:
        return work_page_html(md_path, *wv)

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

    # Title: prefer frontmatter, else the first body "# " heading.
    title = frontmatter.get("title", "")
    if not title:
        m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = m.group(1).strip() if m else md_path.stem.replace("-", " ").title()
        if m:
            text = text[:m.start()] + text[m.end():]
    else:
        # The body conventionally still opens with an H1 repeating the title.
        # serve.py renders the title itself in the doc-header below, so a
        # leading body H1 that duplicates it would render twice. Strip the
        # duplicate — but only when it matches the title, so a genuinely
        # different leading heading is left alone.
        m = re.match(r"#\s+(.+?)\s*(?:\n|$)", text)
        if m and m.group(1).strip() == title.strip():
            text = text[m.end():].lstrip("\n")

    # Convert markdown
    body_html = render_body(text)
    # Dives authored `../<slug>/…` against the old flat layout; fix those links.
    if (ROOT / "research") in md_path.parents:
        body_html = resolve_dive_links(body_html)

    # Relative path for breadcrumb
    rel = md_path.relative_to(ROOT)
    parts = rel.parts
    folder = parts[-2] if len(parts) > 1 else ""

    mtime = datetime.fromtimestamp(md_path.stat().st_mtime).strftime("%-d %B %Y")

    doc_key = "docs/" + str(rel.with_suffix(""))

    # Top bar + Contents hub. Docs | Library | ☰ Work › Subpage for any page
    # that belongs to a work (bundle page OR its research dive/annotations);
    # a plain doc keeps just the Docs link.
    nav = nav_for(md_path)
    eyebrow = folder or "docs"
    if nav["hub_html"] and (ROOT / "reader") in md_path.parents:
        eyebrow = "reader edition · overview" if md_path.name == "overview.md" else "reader edition"

    return page_shell(
        title=esc(title),
        eyebrow=esc(eyebrow),
        heading=esc(title),
        meta_line=f"Last modified {mtime} · <a href=\"/{rel.with_suffix('.md')}\">view source</a>",
        body_html=body_html,
        config={"docKey": doc_key, "kind": "doc"},
        kind="doc",
        home_html=nav["home_html"],
        lib_html=nav["lib_html"],
        crumb_html=nav["crumb_html"],
        hub_title=nav["hub_title"],
        hub_html=nav["hub_html"],
    )


# ── Index builder ──────────────────────────────────────────────────────────────

FOLDER_META = {
    "architecture":  ("Architecture",  "System design, scalability, and operational context"),
    "editorial":     ("Editorial",     "Project principles, voice, and style"),
    "design":        ("Design",        "Visual identity, period colours, and typographic system"),
    "pwa":           ("PWA",           "E-reader, local-first architecture, and tl pipeline"),
    "research":      ("Research",      "Primary-source surveys and reference material"),
    "development":   ("Development",   "Implementation guides and feature recipes"),
    "_root":         ("Root",          "Top-level documents"),
}
FOLDER_ORDER = ["architecture", "editorial", "design", "pwa", "research", "development", "_root"]


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
_HTML_TITLE_SUFFIXES = (" — tolstoy.life research", " — tolstoy.life docs", " — tolstoy.life")


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


def _parse_frontmatter_md(path: Path) -> dict:
    """Parse YAML-ish frontmatter, return a flat str→str dict.

    Only handles scalar `key: value` lines. Multi-line values (lists,
    blocks) are skipped — sufficient for layer/date/lastUpdated lookup.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([a-zA-Z][a-zA-Z0-9_-]*):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"')
    return fm


def extract_meta(path: Path) -> dict:
    """Return {title, lede, layer, date} for any docs file.

    Files without an explicit layer default to `reference` — safer during
    migration than defaulting to `blog`.
    """
    if path.suffix == ".html":
        rel = str(path.relative_to(ROOT))
        ext = HTML_META.get(rel, {})
        return {
            "title": _extract_title_html(path),
            "lede": _extract_lede_html(path),
            "layer": ext.get("layer", "reference"),
            "date": ext.get("date", ""),
        }
    wv = work_version_of(path) if path.suffix == ".md" else None
    if wv:
        work, version = wv
        meta_path = path.parent / f"meta.{version}.json"
        meta = _load_json(meta_path) if meta_path.exists() else {}
        title = meta.get("title") or work.replace("-", " ").title()
        return {
            "title": f"{title} ({_version_label(version)} reader edition)",
            "lede": "",
            "layer": "reference",
            "date": "",
        }
    fm = _parse_frontmatter_md(path)
    return {
        "title": _extract_title_md(path),
        "lede": _extract_lede_md(path),
        "layer": fm.get("layer", "reference"),
        "date": fm.get("date") or fm.get("lastUpdated") or "",
    }


def build_index(docs: dict) -> str:
    """Build INDEX.html as a chronological blog feed + reference appendix.

    Phase 2 of the docs→dev-blog migration: entries with `layer: blog`
    (md frontmatter or HTML_META) are sorted by `date:` and grouped by
    year. Reference entries follow as a pending-port appendix.
    """
    entries = []
    for folder, files in docs.items():
        for path in files:
            meta = extract_meta(path)
            rel = path.relative_to(ROOT)
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            entries.append({
                "title": meta["title"],
                "lede": meta["lede"],
                "layer": meta["layer"],
                "date": meta["date"],
                "folder": "" if folder == "_root" else folder,
                "href": "/" + str(rel.with_suffix(".html")),
                "mtime": mtime,
            })

    def fmt_date(s: str, fallback: datetime) -> str:
        try:
            return datetime.strptime(s, "%Y-%m-%d").strftime("%-d %b %Y")
        except (ValueError, TypeError):
            return fallback.strftime("%-d %b %Y")

    def sort_key(e):
        return e["date"] or e["mtime"].strftime("%Y-%m-%d")

    blog = sorted(
        [e for e in entries if e["layer"] == "blog"],
        key=sort_key, reverse=True,
    )
    reference = sorted(
        [e for e in entries if e["layer"] == "reference"],
        key=lambda e: e["title"].lower(),
    )

    by_year: dict[str, list] = {}
    for e in blog:
        by_year.setdefault(sort_key(e)[:4], []).append(e)

    def folder_label(f: str) -> str:
        if not f:
            return "General"
        return {"pwa": "PWA"}.get(f, f.replace("-", " ").title())

    blog_html = ""
    for year in sorted(by_year.keys(), reverse=True):
        posts = ""
        for e in by_year[year]:
            date_str = fmt_date(e["date"], e["mtime"])
            folder_chip = (
                f"<span class='post-folder'>{e['folder']}</span>"
                if e["folder"] else ""
            )
            lede_html = (
                f"<p class='post-lede'>{e['lede']}</p>" if e["lede"] else ""
            )
            posts += f"""
        <li class="post-entry">
          <a href="{e['href']}">
            <div class="post-row">
              <time>{date_str}</time>
              <span class="post-title">{e['title']}</span>
              {folder_chip}
            </div>
            {lede_html}
          </a>
        </li>"""
        blog_html += f"""
    <h3 class="year-label">{year}</h3>
    <ul class="post-list">{posts}
    </ul>"""

    # ── Embedded centerpiece: the corpus-in-time timeline (chart 1 of the
    # prophet-essays visualizations, shown via its #embed-timeline mode) ──
    viz = ROOT / "research" / "visualizations" / "prophet-essays.html"
    viz_html = ""
    if viz.exists():
        viz_html = """
  <section class="viz">
    <iframe class="viz-frame" src="/research/visualizations/prophet-essays.html#embed-timeline"
      height="940" loading="lazy" title="The Prophet-period corpus in time"></iframe>
    <p class="viz-caption">From the prophet-essays visualizations —
      <a href="/research/visualizations/prophet-essays.html">see all four →</a></p>
  </section>"""
    else:
        print("  ! prophet-essays.html missing — index built without the chart",
              file=sys.stderr)

    # ── Section-nav cards: one per major area, counts from the docs dict ──
    folder_counts: dict[str, int] = {}
    for e in entries:
        folder_counts[e["folder"]] = folder_counts.get(e["folder"], 0) + 1
    nav_cards = f"""
      <a class="nav-card" href="/research/index.html">
        <div class="nc-title">Research</div>
        <div class="nc-meta">{folder_counts.get('research', 0)} docs · corpus-dive landing page</div>
      </a>
      <a class="nav-card" href="/reader/index.html">
        <div class="nc-title">Library</div>
        <div class="nc-meta">{folder_counts.get('reader', 0)} docs · reader editions &amp; works tracker</div>
      </a>"""
    for f in sorted(folder_counts):
        if f in ("research", "reader"):
            continue
        anchor = f or "general"
        nav_cards += f"""
      <a class="nav-card" href="#ref-{anchor}">
        <div class="nc-title">{folder_label(f)}</div>
        <div class="nc-meta">{folder_counts[f]} doc{'s' if folder_counts[f] != 1 else ''}</div>
      </a>"""

    # ── Reference docs grouped by top-level folder ──
    by_folder: dict[str, list] = {}
    for e in reference:
        by_folder.setdefault(e["folder"], []).append(e)
    ref_html = ""
    for f in sorted(by_folder):
        cards = ""
        for e in by_folder[f]:
            last = fmt_date(e["date"], e["mtime"])
            lede_html = (
                f"<div class='card-lede'>{e['lede']}</div>" if e["lede"] else ""
            )
            cards += f"""
      <a class="index-card" href="{e['href']}">
        <div class="card-title">{e['title']}</div>
        <div class="card-meta">updated {last}</div>
        {lede_html}
      </a>"""
        ref_html += f"""
    <h2 id="ref-{f or 'general'}">{folder_label(f)}<span class="count">{len(by_folder[f])}</span></h2>
    <div class="index-grid">{cards}
    </div>"""

    now = datetime.now().strftime("%-d %B %Y, %H:%M")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research — tolstoy.life</title>
<style>
:root {{
  --bg:#14161a; --panel:#1c1f25; --panel-2:#21252c; --ink:#e8e4da;
  --ink-dim:#9a958a; --ink-faint:#5d594f; --line:#2e323a;
  --green:#54b87f; --amber:#e0a93e; --blue:#6aa3d8; --violet:#a08cc8;
  --accent:#c8b68a;
}}
*,*::before,*::after {{ box-sizing:border-box; }}
body {{
  margin:0; padding:0; background:var(--bg); color:var(--ink);
  font:16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  -webkit-font-smoothing:antialiased;
}}
a {{ color:var(--accent); text-decoration:none; }}
a:hover {{ text-decoration:underline; }}
.topbar {{ position:sticky; top:0; z-index:300;
  display:flex; align-items:center; justify-content:space-between; gap:1rem;
  padding:9px 16px; border-bottom:1px solid var(--line);
  background:color-mix(in srgb, var(--bg) 86%, transparent);
  backdrop-filter:blur(10px); -webkit-backdrop-filter:blur(10px); }}
.topbar .tb-group {{ display:flex; align-items:center; gap:10px; min-width:0; }}
.topbar a {{ font-size:12px; color:var(--ink-dim); }} .topbar a:hover {{ color:var(--ink); text-decoration:none; }}
.topbar .tb-brand {{ font-size:13px; color:var(--accent); }}
.topbar .sep {{ font-size:12px; color:var(--ink-faint); }}
.topbar .tb-here {{ font-size:13px; font-weight:600; color:var(--ink); }}
.wrap {{ max-width:1180px; margin:0 auto; padding:2.4rem 1.4rem 4rem; }}
header.top {{ border-bottom:1px solid var(--line); padding-bottom:1.4rem; margin-bottom:1.8rem; }}
.eyebrow {{ font-size:.74rem; letter-spacing:.16em; text-transform:uppercase; color:var(--accent); margin:0 0 .5rem; }}
h1 {{ font-size:2rem; font-weight:650; letter-spacing:.01em; margin:0 0 .5rem; }}
p.lede {{ color:var(--ink-dim); max-width:74ch; margin:.2rem 0 .7rem; }}
p.meta {{ font-size:.78rem; color:var(--ink-faint); margin-top:1rem; }}
h2 {{ font-size:1.2rem; font-weight:600; color:var(--accent); margin:2.8rem 0 .3rem; }}
h2 .count {{ color:var(--ink-faint); font-weight:500; font-size:.9rem; margin-left:.4em; }}
.viz {{ margin:1.6rem 0 0; }}
.viz-frame {{ width:100%; border:1px solid var(--line); border-radius:10px; background:var(--bg); display:block; }}
.viz-caption {{ font-size:.78rem; color:var(--ink-faint); margin:.5rem 0 0; }}
.nav-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(210px,1fr)); gap:.7rem; margin-top:.6rem; }}
.nav-card {{ display:block; background:var(--panel); border:1px solid var(--line); border-radius:9px;
  padding:.75rem .95rem .85rem; transition:transform .08s, border-color .08s; }}
.nav-card:hover {{ transform:translateY(-1px); border-color:var(--accent); text-decoration:none; }}
.nc-title {{ font-weight:600; color:var(--ink); }}
.nc-meta {{ font-size:.74rem; color:var(--ink-faint); margin-top:.25rem; }}
.year-label {{ font-size:.95rem; font-weight:600; color:var(--ink-dim); margin:1.6rem 0 .3rem; }}
.post-list {{ list-style:none; margin:0; padding:0; }}
.post-entry a {{ display:block; padding:.5rem .6rem; border-radius:8px; color:inherit; }}
.post-entry a:hover {{ background:var(--panel); text-decoration:none; }}
.post-row {{ display:flex; flex-wrap:wrap; gap:.7em; align-items:baseline; }}
.post-row time {{ font-size:.78rem; color:var(--ink-faint); font-variant-numeric:tabular-nums; min-width:7.5em; }}
.post-title {{ font-weight:600; color:var(--ink); }}
.post-folder {{ font-size:.68rem; color:var(--ink-faint); text-transform:uppercase; letter-spacing:.05em; }}
.post-lede {{ font-size:.83rem; color:var(--ink-dim); margin:.15rem 0 0 8.6em; max-width:74ch; }}
.index-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(300px,1fr)); gap:.7rem; margin-top:.5rem; }}
.index-card {{ display:block; background:var(--panel); border:1px solid var(--line); border-radius:9px;
  padding:.8rem .95rem .9rem; transition:transform .08s, border-color .08s; }}
.index-card:hover {{ transform:translateY(-1px); border-color:var(--accent); text-decoration:none; }}
.card-title {{ font-weight:600; color:var(--ink); line-height:1.35; }}
.card-meta {{ font-size:.72rem; color:var(--ink-faint); margin:.3rem 0 .45rem; }}
.card-lede {{ font-size:.83rem; color:var(--ink-dim); line-height:1.45; }}
footer {{ margin-top:3rem; border-top:1px solid var(--line); padding-top:1rem; color:var(--ink-faint); font-size:.78rem; }}
</style>
</head>
<body>
<header class="topbar">
  <div class="tb-group">
    <a class="tb-brand" href="https://tolstoy.life/">tolstoy.life</a>
    <span class="sep">›</span>
    <span class="tb-here">Research</span>
  </div>
  <div class="tb-group tb-links">
    <a href="/reader/index.html">Library</a>
    <a href="/research/index.html">Corpus dives</a>
  </div>
</header>
<div class="wrap">
<header class="top">
  <p class="eyebrow">tolstoy.life · research</p>
  <h1>Research</h1>
  <p class="lede">Open research on the last thirty years of Leo Tolstoy's life — from <em>A Confession</em> (1879–82) to his death in 1910, the stretch this project calls the Prophet period. It is the part of his work that is least read and least translated: the religious and social writing he turned to after the novels, and whose copyright he renounced so that it would belong to everyone.</p>
  <p class="lede">The reading, the source work and the writing are done by Claude Code, an AI, under the supervision of Johan Edlund. The sources are the 90-volume Jubilee Edition, the tolstoydigital TEI corpus, and Tolstoy's own diaries and letters; every claim is tied to one by name, and what hasn't been checked says so.</p>
  <p class="lede">This page indexes everything: reader's editions with read-along audio, research dives through the corpus, and the build log. Nothing here is behind a login — the pages, the working notes and the code that builds them are all in <a href="https://github.com/tolstoylife/tolstoy.life">tolstoylife/tolstoy.life</a>. Corrections, sources and questions are welcome as issues there, and anyone who wants to work on it is welcome to join.</p>
  <p class="meta">Generated {now}</p>
</header>
<section class="reading">
  <h2>Read and listen</h2>
  <div class="nav-grid">
    <a class="nav-card" href="/reader/non-fiction/personal-papers/confession/">
      <div class="nc-title">A Confession</div>
      <div class="nc-meta">1879–82 · the Russian, Wiener's 1904 English, a first machine draft · read-along audio</div>
    </a>
    <a class="nav-card" href="/reader/non-fiction/essays-and-criticism/the-great-sin/">
      <div class="nc-title">The Great Sin</div>
      <div class="nc-meta">1905 · the Russian, the 1905 English (<em>A Great Iniquity</em>), a first machine draft · read-along audio</div>
    </a>
    <a class="nav-card" href="/reader/index.html">
      <div class="nc-title">The whole library</div>
      <div class="nc-meta">every work, with what exists for each</div>
    </a>
  </div>
</section>
{viz_html}
<section>
  <h2>Browse</h2>
  <div class="nav-grid">{nav_cards}
  </div>
</section>
{ref_html}
<section>
  <h2>Notes</h2>
  {blog_html}
</section>
<footer>tolstoy.life · public build log · generated by <code>docs/serve.py</code><br>Extracts from the <a href="https://tolstoydigital.org/">tolstoydigital</a> TEI corpus are shared under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>. Tolstoy's own words are in the public domain, and everything else here is dedicated to it (<a href="https://github.com/tolstoylife/tolstoy.life/blob/main/LICENSE">licence</a>).</footer>
</div>
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
        # Generated-and-committed pages (not hand-authored orphans): the research
        # landing page and its promoted visualizations are built by
        # build_research_index.py, not part of the chronological notes feed.
        rel = path.relative_to(ROOT).as_posix()
        if rel == "research/index.html" or rel.startswith("research/visualizations/"):
            continue
        if path.with_suffix(".md").exists():
            continue
        # A bundle's index.html is the generated twin of its overview.md
        if path.name == "index.html" and (path.parent / "overview.md").exists():
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


def build_research_index_page(verbose=True):
    """Regenerate docs/research/index.html from the dives (decoupled, best-effort).

    Mirrors build_evidence_index.py but is wired into the build so the research
    landing page is correct by construction — it never needs a hand rebuild as
    new dives ship. Loaded by path so serve.py stays import-free; a failure
    (missing PyYAML, a malformed dossier) warns and skips rather than breaking
    the whole docs build.
    """
    import importlib.util
    gen = ROOT / "research" / "lib" / "build_research_index.py"
    if not gen.exists():
        return
    try:
        spec = importlib.util.spec_from_file_location("build_research_index", gen)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.build(verbose=False)
        if verbose:
            print("  ✓ research/index.html")
    except Exception as exc:  # noqa: BLE001 — never let it break the docs build
        print(f"  ! research/index.html skipped: {exc}")


def build_works_tracker_page(verbose=True):
    """Regenerate docs/reader/index.html (the works tracker) from the dives, the
    works records, and the hand-kept status file. Same best-effort contract as the
    research index: loaded by path, a failure warns and skips rather than breaking
    the whole docs build."""
    import importlib.util
    gen = ROOT / "reader" / "lib" / "build_works_tracker.py"
    if not gen.exists():
        return
    try:
        spec = importlib.util.spec_from_file_location("build_works_tracker", gen)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.build(verbose=False)
        if verbose:
            print("  ✓ reader/index.html")
    except Exception as exc:  # noqa: BLE001 — never let it break the docs build
        print(f"  ! reader/index.html skipped: {exc}")


def build_all(verbose=True):
    md_docs = collect_md_files()
    html_docs = collect_orphan_html_files()
    count = 0
    for folder, files in md_docs.items():
        for md_path in files:
            html_path = md_path.with_suffix(".html")
            html = md_to_html(md_path)
            html_path.write_text(html, encoding="utf-8")
            if md_path.name == "overview.md":
                # the bundle's front page: the bare folder URL serves it too
                (md_path.parent / "index.html").write_text(html, encoding="utf-8")
            if verbose:
                print(f"  ✓ {md_path.relative_to(ROOT)}")
            count += 1

    index_html = build_index(merge_doc_files(md_docs, html_docs))
    (ROOT / "INDEX.html").write_text(index_html, encoding="utf-8")
    if verbose:
        print(f"  ✓ INDEX.html")
    build_research_index_page(verbose=verbose)
    build_works_tracker_page(verbose=verbose)
    if verbose:
        orphans = sum(len(v) for v in html_docs.values())
        suffix = f" + {orphans} hand-authored HTML" if orphans else ""
        print(f"\n{count} documents converted{suffix}.")
    return count


# ── HTTP server ────────────────────────────────────────────────────────────────

class Handler(http.server.SimpleHTTPRequestHandler):
    # Default .txt to text/plain with no charset, which browsers then guess as
    # Latin-1 / cp1252 and render UTF-8 prose (Cyrillic, French diacritics) as
    # mojibake. Force UTF-8 for text/* responses.
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".txt": "text/plain; charset=utf-8",
        ".md": "text/plain; charset=utf-8",
        ".py": "text/plain; charset=utf-8",
        ".m4a": "audio/mp4",
        ".jsonld": "application/ld+json",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        # Dev server: always revalidate, so shell.css/js edits show on reload.
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_GET(self):
        path = self.path.split("?")[0].lstrip("/")
        if path == "" or path == "INDEX.html":
            build_all(verbose=False)
        elif (ROOT / path).is_dir() and (ROOT / path / "overview.md").exists():
            html = md_to_html(ROOT / path / "overview.md")
            (ROOT / path / "index.html").write_text(html, encoding="utf-8")
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
