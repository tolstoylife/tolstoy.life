#!/usr/bin/env python3
"""Build docs/ and gather what research.tolstoy.life publishes into _site/ at the repository root.

Publishes what git tracks, the HTML generated from tracked .md, the reader audio + timing, and the dive images a dossier records as free; working papers, other images, stale HTML, scripts and tests stay home.

Usage (from the repository root; Johan runs the netlify lines):
    python3 docs/publish.py
    netlify deploy --no-build --dir _site --site tolstoy-research          # draft address, check it first
    netlify deploy --no-build --prod --dir _site --site tolstoy-research   # live
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

import yaml

import serve

DOCS = Path(__file__).parent.resolve()
OUT = DOCS.parent / "_site"
SKIP_SUFFIXES = {".py", ".sh", ".stderr"}
SKIP_PARTS = {"tests", "_audition"}
HEADERS = "/*\n  X-Robots-Tag: noindex\n"  # @until research-listed — keeps the site out of search results
FORM_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Form registration</title><meta name="robots" content="noindex"></head>
<body>
<form name="reader-notes" data-netlify="true" netlify-honeypot="bot-field" hidden>
  <input type="text" name="page">
  <input type="email" name="email">
  <input type="text" name="bot-field">
  <textarea name="text"></textarea>
  <textarea name="jsonld"></textarea>
</form>
</body></html>
"""  # Netlify registers a form by finding it in the uploaded HTML; the reader's Send button posts to it
REDIRECTS = "/  /INDEX.html  200\n"  # the docs front page is INDEX.html, not index.html


def held_back(rel: PurePosixPath) -> bool:
    """Working papers: on GitHub, not on the site — reading annotations, planning docs, verifier output, search logs, session logs."""
    name = rel.name
    return ((name.startswith("annotations.") and rel.parts[0] == "research") or rel.parts[0] == "superpowers"
            or name.startswith("session-log") or "handoff" in name or "_verifier-report" in name
            or (name.startswith("_") and "sweep" in name))  # any _…sweep file is a corpus search log


def publishable(docs: Path = DOCS) -> list[Path]:
    tracked = subprocess.run(["git", "ls-files", "-z"], cwd=docs, capture_output=True, text=True, check=True).stdout
    files = {docs / f for f in tracked.split("\0") if f}
    for md in [f for f in files if f.suffix == ".md"]:
        files.add(md.with_suffix(".html"))
        if md.name == "overview.md":
            files.add(md.parent / "index.html")
    files |= set(docs.glob("reader/**/build/**/*"))  # audio + timing: gitignored, but ours to publish
    files |= {f for f in cleared_images(docs) if f.is_file()}  # dive images a dossier records as free; the rest stay home
    keep = []
    for f in files:
        rel = f.relative_to(docs)
        if (f.is_file() and f.suffix not in SKIP_SUFFIXES and not rel.name.startswith(".")
                and not SKIP_PARTS & set(rel.parts) and not held_back(PurePosixPath(rel.as_posix()))):
            keep.append(rel)
    return sorted(keep)


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
IMG_TAG = re.compile(r'<img\s[^>]*?src="([^"]+)"[^>]*>')
WITHHELD_NOTE = '<span class="img-withheld">Image not shown — rights unclear</span>'


def cleared_images(docs: Path = DOCS) -> set[Path]:
    """Dive images a dossier records as public domain or CC0. Everything else stays home, including images no dossier lists."""
    cleared = set()
    for dossier in docs.glob("research/**/dossier.yaml"):
        try:
            data = yaml.safe_load(dossier.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:  # a malformed dossier withholds its images rather than breaking the build
            print(f"  ! {dossier.relative_to(docs)}: {exc}", file=sys.stderr)
            continue
        for v in data.get("visuals") or []:
            if not isinstance(v, dict) or not v.get("localPath"):
                continue
            licence = str(v.get("licence") or v.get("license") or "").strip().upper()
            free = licence.startswith("PD") or licence == "CC0" or "PUBLIC DOMAIN" in licence
            if free and "RIGHTS-RESERVED" not in licence:  # ⚠ "PD text; museum copy rights-reserved" stays home
                path = re.sub(r"\s*\(.*\)$", "", str(v["localPath"]))  # "visuals/death-met-*.jpg (6 files)" is a wildcard
                cleared |= {f.resolve() for f in dossier.parent.glob(path)} if "*" in path else {(dossier.parent / path).resolve()}
    return cleared


LINKED_ITEM = re.compile(r'<li><a href="([^"#?]+)"[^>]*>[^<]*</a></li>')


def drop_held_links(html: str, page_dir: Path) -> str:
    """In the uploaded copy only: a list item that links to a held-back page (e.g. "Reading annotations") is dropped."""
    def replace(m):
        href = unquote(m.group(1))
        if href.startswith(("http:", "https:", "mailto:")):
            return m.group(0)
        target = DOCS / href.lstrip("/") if href.startswith("/") else (page_dir / href).resolve()
        try:
            rel = PurePosixPath(target.relative_to(DOCS).as_posix())
        except ValueError:
            return m.group(0)
        return "" if held_back(rel.with_suffix(".md")) or held_back(rel) else m.group(0)
    return LINKED_ITEM.sub(replace, html)


def hide_withheld_images(html: str, page_dir: Path, cleared: set[Path]) -> str:
    """In the uploaded copy only: an image that isn't cleared becomes a short note in its place."""
    def replace(m):
        src = m.group(1)
        if src.startswith(("http:", "https:", "data:", "//")):
            return m.group(0)
        target = (page_dir / unquote(src.split("?")[0])).resolve()
        if target.suffix.lower() not in IMAGE_SUFFIXES or target in cleared:
            return m.group(0)
        return WITHHELD_NOTE
    return IMG_TAG.sub(replace, html)


def main():
    subprocess.run([sys.executable, str(DOCS / "serve.py"), "--build-only"], check=True)
    shutil.rmtree(OUT, ignore_errors=True)
    total = 0
    pub = publishable()
    cleared = cleared_images() | {DOCS / rel for rel in pub if rel.suffix.lower() in IMAGE_SUFFIXES}
    for rel in pub:
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if rel.suffix == ".html":
            html = hide_withheld_images((DOCS / rel).read_text(encoding="utf-8"), (DOCS / rel).parent, cleared)
            dest.write_text(drop_held_links(html, (DOCS / rel).parent), encoding="utf-8")
        else:
            shutil.copy2(DOCS / rel, dest)
        total += dest.stat().st_size
    # ⚠ The local front page lists untracked and leftover pages too; the published one lists only what's published.
    live = {DOCS / rel for rel in pub}
    listed = serve.merge_doc_files(serve.collect_md_files(), serve.collect_orphan_html_files())
    kept = {folder: [p for p in files if p.with_suffix(".html") in live] for folder, files in listed.items()}
    (OUT / "INDEX.html").write_text(serve.build_index({f: ps for f, ps in kept.items() if ps}), encoding="utf-8")
    (OUT / "404.html").write_text(serve.md_to_html(DOCS / "404.md"), encoding="utf-8")  # Netlify serves it for any missing address
    (OUT / "__forms.html").write_text(FORM_PAGE, encoding="utf-8")
    (OUT / "_headers").write_text(HEADERS)
    (OUT / "_redirects").write_text(REDIRECTS)
    print(f"{OUT}: {total / 1e6:.0f} MB. Upload with: netlify deploy --no-build --dir _site --site tolstoy-research")


if __name__ == "__main__":
    main()
