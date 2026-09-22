#!/usr/bin/env python3
"""Build docs/ and gather what research.tolstoy.life publishes into _site/ at the repository root.

Publishes what git tracks, the HTML generated from tracked .md, and the reader audio + timing; dive images, stale HTML, scripts and tests stay home.

Usage (from the repository root; Johan runs the netlify lines):
    python3 docs/publish.py
    netlify deploy --no-build --dir _site --site tolstoy-research          # draft address, check it first
    netlify deploy --no-build --prod --dir _site --site tolstoy-research   # live
"""
import shutil
import subprocess
import sys
from pathlib import Path

DOCS = Path(__file__).parent.resolve()
OUT = DOCS.parent / "_site"
SKIP_SUFFIXES = {".py", ".sh", ".stderr"}
SKIP_PARTS = {"tests", "_audition"}
HEADERS = "/*\n  X-Robots-Tag: noindex\n"  # @until research-listed — keeps the site out of search results
REDIRECTS = "/  /INDEX.html  200\n"  # the docs front page is INDEX.html, not index.html


def publishable(docs: Path = DOCS) -> list[Path]:
    tracked = subprocess.run(["git", "ls-files", "-z"], cwd=docs, capture_output=True, text=True, check=True).stdout
    files = {docs / f for f in tracked.split("\0") if f}
    for md in [f for f in files if f.suffix == ".md"]:
        files.add(md.with_suffix(".html"))
        if md.name == "overview.md":
            files.add(md.parent / "index.html")
    files |= set(docs.glob("reader/**/build/**/*"))  # audio + timing: gitignored, but ours to publish
    keep = []
    for f in files:
        rel = f.relative_to(docs)
        if f.is_file() and f.suffix not in SKIP_SUFFIXES and not rel.name.startswith(".") and not SKIP_PARTS & set(rel.parts):
            keep.append(rel)
    return sorted(keep)


def main():
    subprocess.run([sys.executable, str(DOCS / "serve.py"), "--build-only"], check=True)
    shutil.rmtree(OUT, ignore_errors=True)
    total = 0
    for rel in publishable():
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(DOCS / rel, dest)
        total += dest.stat().st_size
    (OUT / "_headers").write_text(HEADERS)
    (OUT / "_redirects").write_text(REDIRECTS)
    print(f"{OUT}: {total / 1e6:.0f} MB. Upload with: netlify deploy --no-build --dir _site --site tolstoy-research")


if __name__ == "__main__":
    main()
