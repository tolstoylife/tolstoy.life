#!/usr/bin/env python3
"""
docs/ visuals fetcher — tolstoy.life
=====================================
Repopulates the git-ignored `docs/research/*/visuals/` image caches from the
`url:` fields recorded in each dive's `dossier.yaml`. This is the image
analogue of `serve.py --build-only`: serve.py regenerates .html from .md, this
regenerates the third-party portrait/photo cache from the dossier ledger, so a
fresh clone (where `research/*/visuals/` is git-ignored and empty) can render
the figures that `index.md` embeds.

A `visuals[]` entry is fetched when it has both a `url:` and a `localPath:` that
lives under a `visuals/` directory. That selects the downloaded portraits and
skips, by construction: facsimiles we render ourselves (in `extracts/`, no
`url:`), and not-yet-chosen candidates (`localPath: null`). Licence is NOT a
gate — `visuals/` is a local-only, git-ignored cache, so non-PD images may be
cached for research; the publication gate lives at `website/src/`, recorded via
`licence`/`usable` in the dossier.

Usage:
    cd /Volumes/Graugear/Tolstoy
    python3 docs/fetch_visuals.py            # all dives under docs/research/
    python3 docs/fetch_visuals.py crisis     # just one dive (by slug)
    python3 docs/fetch_visuals.py --dry-run  # list targets, no network
    python3 docs/fetch_visuals.py --force    # re-download even if cached
"""

import argparse
import importlib.util
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlsplit

# ── Dependencies ─────────────────────────────────────────────────────────────

def require(package, pip_name=None):
    if importlib.util.find_spec(package) is None:
        name = pip_name or package
        print(f"Installing {name}…")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", name,
                               "--break-system-packages", "-q"])

require("yaml", "pyyaml")
require("requests")
import yaml
import requests

# ── Paths ──────────────────────────────────────────────────────────────────────

DOCS = Path(__file__).parent.resolve()      # …/docs
REPO_ROOT = DOCS.parent                      # repo root; dossier localPaths are repo-relative
RESEARCH = DOCS / "research"

# ⚠ Wikimedia serves 403 to an empty or generic User-Agent; it wants one with contact info.
USER_AGENT = ("tolstoy.life-fetch_visuals/1.0 "
              "(https://tolstoy.life; research image cache) python-requests")

# A Commons "File:" page is HTML, not the image; Special:FilePath/<name> redirects to the full-size file.
COMMONS_FILE_RE = re.compile(
    r"https?://commons\.wikimedia\.org/wiki/File:(.+)$", re.IGNORECASE)
IMG_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".tif", ".tiff", ".svg")

# ── Dossier reading ──────────────────────────────────────────────────────────

def find_dossiers(slug=None):
    """Return the dossier.yaml paths to process (one slug, or all dives)."""
    if slug:
        p = RESEARCH / slug / "dossier.yaml"
        return [p] if p.exists() else []
    return sorted(RESEARCH.glob("*/dossier.yaml"))


def fetch_targets(dossier_path):
    """Visuals entries worth fetching: have a url AND a localPath under visuals/."""
    data = yaml.safe_load(dossier_path.read_text(encoding="utf-8")) or {}
    targets = []
    for entry in (data.get("visuals") or []):
        url = entry.get("url")
        local = entry.get("localPath")
        if not url or not local:
            continue
        if "visuals" not in Path(local).parts:
            continue
        targets.append(entry)
    return targets


def resolve_download_url(url):
    """Map a dossier `url:` to a direct image URL, or None if not fetchable."""
    url = url.split("#")[0]
    m = COMMONS_FILE_RE.match(url)
    if m:
        return f"https://commons.wikimedia.org/wiki/Special:FilePath/{m.group(1)}"
    if urlsplit(url).path.lower().endswith(IMG_EXTENSIONS):
        return url  # already a direct file
    return None     # category page, museum landing page, etc. — not auto-fetchable

# ── Download ─────────────────────────────────────────────────────────────────

def download(url, dest, timeout=30):
    """Stream `url` to `dest` via a `.part` temp file, then atomic-rename."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    resp = requests.get(url, headers={"User-Agent": USER_AGENT},
                        timeout=timeout, allow_redirects=True, stream=True)
    resp.raise_for_status()
    tmp = dest.with_suffix(dest.suffix + ".part")
    try:
        with open(tmp, "wb") as f:
            for chunk in resp.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
        tmp.replace(dest)
    finally:
        if tmp.exists():
            tmp.unlink()


def human(n):
    size = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024

# ── Run ──────────────────────────────────────────────────────────────────────

def run(slug=None, force=False, dry_run=False, pause=0.5):
    dossiers = find_dossiers(slug)
    if not dossiers:
        where = f" for slug '{slug}'" if slug else f" under {RESEARCH.relative_to(REPO_ROOT)}/"
        print(f"No dossier.yaml found{where}.")
        return 1 if slug else 0

    fetched = skipped = failed = unresolved = 0
    for dossier in dossiers:
        targets = fetch_targets(dossier)
        if not targets:
            continue
        print(f"{dossier.relative_to(REPO_ROOT)}  ({len(targets)} visual"
              f"{'s' if len(targets) != 1 else ''})")
        for entry in targets:
            label = entry.get("id") or entry["localPath"]
            dest = REPO_ROOT / entry["localPath"]
            dl_url = resolve_download_url(entry["url"])

            if dl_url is None:
                print(f"  ⚠ {label}: not auto-fetchable ({entry['url']}) — skipped")
                unresolved += 1
                continue

            if dest.exists() and not force:
                print(f"  · {label}: skip (cached)")
                skipped += 1
                continue

            if dry_run:
                print(f"  • {label}: would fetch ← {dl_url}")
                continue

            try:
                download(dl_url, dest)
                print(f"  ✓ {label}: fetched {human(dest.stat().st_size)} "
                      f"→ {entry['localPath']}")
                fetched += 1
                time.sleep(pause)  # be polite to Wikimedia
            except Exception as e:
                print(f"  ✗ {label}: FAIL — {e}")
                failed += 1

    parts = []
    if fetched:    parts.append(f"{fetched} fetched")
    if skipped:    parts.append(f"{skipped} cached")
    if unresolved: parts.append(f"{unresolved} unresolved")
    if failed:     parts.append(f"{failed} failed")
    print("\n" + (", ".join(parts) if parts else "nothing to do") + ".")
    return 1 if failed else 0

# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Repopulate git-ignored research visuals/ caches from dossier.yaml URLs.")
    parser.add_argument("slug", nargs="?",
                        help="restrict to one dive slug (default: all dives)")
    parser.add_argument("--force", action="store_true",
                        help="re-download even if the file is already cached")
    parser.add_argument("--dry-run", action="store_true",
                        help="list what would be fetched, without downloading")
    args = parser.parse_args()
    sys.exit(run(slug=args.slug, force=args.force, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
