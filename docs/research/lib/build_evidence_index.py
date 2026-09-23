#!/usr/bin/env python3
"""Cross-dive evidence index — aggregate every corpus-dive dossier by entity.

Each `docs/research/<slug>/dossier.yaml` welds its findings to primary sources
(TEI id + PSS Tom/pages + byte-faithful quoteRu + extract + facsimile) and lists
the wiki pages those findings feed in its `entities[]` layer. But that connection
lives INSIDE each dive. The same entity recurs across dives (Chertkov in all five,
Biryukov in three) with no aggregate view, so writing a wiki page means reopening
every dossier and re-collating by hand. This tool removes that step.

It walks every dossier, groups entities by a stable key (the slug of
`wikilinkTarget`, == the eventual wiki/works slug), resolves each entity's
`evidenceRefs` to full evidence rows qualified by dive, collates visuals,
re-derives `vaultStatus` live against website/src/, and emits:

  docs/research/evidence-index/evidence-index.yaml   # machine-readable aggregate
  docs/research/evidence-index/index.md              # human view (renders to .html
                                                     #   via serve.py --build-only)

It creates NO wiki pages and touches nothing outside the output dir — pure
aggregation of already-verified research, the reuse bridge for wiki ingestion.

Usage:
  build_evidence_index.py                 # build both artifacts, print SUMMARY
  build_evidence_index.py --check         # lint only; exit 1 on broken links; write nothing
  build_evidence_index.py --quiet         # suppress per-entity lines
  build_evidence_index.py --research-dir PATH   # default: docs/research

Exit codes:
  0  built (or --check found no broken links)
  1  --check found integrity failures (unresolved evidenceRefs / un-keyable entity)
  2  usage / parse error (bad path, unreadable YAML, missing PyYAML)

Run from anywhere:
  python3 docs/research/lib/build_evidence_index.py
"""
import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("build_evidence_index.py: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

# ── Paths ────────────────────────────────────────────────────────────────────
LIB = Path(__file__).parent.resolve()       # …/docs/research/lib
RESEARCH = LIB.parent                        # …/docs/research
DOCS = RESEARCH.parent                       # …/docs
REPO_ROOT = DOCS.parent                      # repo root
WIKI_DIR = REPO_ROOT / "website" / "src" / "wiki"
WORKS_DIR = REPO_ROOT / "website" / "src" / "works"
OUT_DIRNAME = "evidence-index"               # docs/research/evidence-index/

# The twelve wiki article types (website/schema/wiki-schema.md v1.4); anything else, notably `work`, is a Tolstoy work routed to website/src/works/ and flagged.
WIKI_TYPES = {
    "person", "place", "event", "concept", "translator",
    "institution", "adaptation", "criticalWork", "archivalFond",
    "edition", "character", "group",
}

# Mirrors website/src/_config/filters/slugify.js; a live page's frontmatter `id` wins, and disagreements show under lint.slugMismatch.
SLUG_REMOVE_RE = re.compile(r"""[#,&+()$~%.'":*¿?¡!<>{}]""")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
MD_MARK_RE = re.compile(r"[#*_>`~\[\]()|]")


def collapse_ws(s):
    """Collapse all whitespace runs to single spaces; '' for None."""
    return " ".join((s or "").split())


def strip_md_suffix(s):
    """Drop a trailing '.md' from a wikilinkTarget (drift: some dives write it)."""
    s = (s or "").strip()
    return s[:-3].strip() if s.endswith(".md") else s


def slugify_py(s):
    """Best-effort reproduction of the live slugifyString filter."""
    s = SLUG_REMOVE_RE.sub("", (s or ""))
    s = s.lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


# ── Live vault (re-derive vaultStatus, don't trust the dossier) ───────────────

def split_frontmatter(text):
    """Return (frontmatter_dict, body_text). Tolerates the works pages' inline
    `# ELEVENTY`/`# GENERATED` comment lines (YAML comments)."""
    fm, body = {}, text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            block = text[3:end]
            body = text[end + 4:]
            try:
                loaded = yaml.safe_load(block)
                if isinstance(loaded, dict):
                    fm = loaded
            except yaml.YAMLError:
                for line in block.splitlines():
                    if ":" in line and not line.lstrip().startswith("#"):
                        k, _, v = line.partition(":")
                        fm[k.strip()] = v.strip().strip('"')
    return fm, body


def prose_word_count(body):
    """Count prose words in a page body — frontmatter already removed."""
    text = HTML_COMMENT_RE.sub(" ", body or "")
    text = WIKILINK_RE.sub(lambda m: m.group(1).split("|")[-1], text)  # keep link text
    text = MD_MARK_RE.sub(" ", text)
    return len(text.split())


def classify_status(record_status, words):
    """missing handled by caller. stub if thin; else exists."""
    if str(record_status or "").lower() == "draft" and words < 120:
        return "stub"
    if words < 60:
        return "stub"
    return "exists"


def build_live_vault_index():
    """Return {id: {status, vaultPath, wordCount, tree}} and {stemSlug: id}."""
    by_id, by_stem = {}, {}
    for tree, base in (("wiki", WIKI_DIR), ("works", WORKS_DIR)):
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            fm, body = split_frontmatter(text)
            pid = (fm.get("id") or "").strip() or slugify_py(path.stem)
            words = prose_word_count(body)
            status = classify_status(fm.get("recordStatus"), words)
            rel = str(path.relative_to(REPO_ROOT))
            by_id.setdefault(pid, {
                "status": status, "vaultPath": rel,
                "wordCount": words, "tree": tree,
            })
            by_stem.setdefault(slugify_py(path.stem), pid)
    return by_id, by_stem


# ── Dossier loading ───────────────────────────────────────────────────────────

def load_dossiers(research_dir):
    """Return [(slug, rel, data)] for every dive's dossier.yaml, sorted by slug.
    Dives are nested under works/<genre>/<subcat>/ and themes/<slug>/; slug is the
    bare folder name (identity), rel is the research-relative path (for file refs).
    _meta/ reference material is excluded by construction."""
    dossiers = []
    paths = list(research_dir.glob("works/*/*/*/dossier.yaml")) \
          + list(research_dir.glob("themes/*/dossier.yaml"))
    for path in sorted(paths, key=lambda p: p.parent.name):
        slug = path.parent.name
        if slug == OUT_DIRNAME:
            continue
        rel = path.parent.relative_to(research_dir).as_posix()
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        dossiers.append((slug, rel, data))
    return dossiers


def repo_rel(rel, p):
    """Rewrite a dive-relative path (extract/facsimile/localPath) to repo-relative."""
    if not p:
        return None
    return f"docs/research/{rel}/{p}"


# ── Aggregation ───────────────────────────────────────────────────────────────

def aggregate(dossiers, live_by_id, live_by_stem):
    entities = {}   # key -> accumulator
    lint = {
        "unresolvedEvidenceRefs": [],
        "nameConflicts": [],
        "wikiTypeConflicts": [],
        "entitiesWithZeroEvidence": [],
        "missingWikilinkTarget": [],
        "worksRoutedNotWiki": [],
        "vaultStatusDrift": [],
        "slugMismatch": [],
    }
    topic_dates = []
    evidence_total = visual_total = 0

    for slug, rel, data in dossiers:
        d = data.get("topic", {}).get("date")
        if d:
            topic_dates.append(str(d))
        ev_rows = data.get("evidence") or []
        evidence_total += len(ev_rows)
        ev_map = {row.get("id"): row for row in ev_rows if row.get("id")}
        visuals = data.get("visuals") or []
        visual_total += len(visuals)

        # name -> key for THIS dive (used to attach visuals by relatedEntity)
        dive_name_to_key = {}

        for ent in (data.get("entities") or []):
            name = collapse_ws(ent.get("name")) or "(unnamed)"
            raw_target = ent.get("wikilinkTarget")
            display = strip_md_suffix(raw_target) if raw_target else name
            key = slugify_py(display)
            if not raw_target:
                lint["missingWikilinkTarget"].append({"name": name, "dive": slug})
            if not key:
                key = slugify_py(name)
            if not key:
                continue  # un-keyable; counted as integrity failure below
            dive_name_to_key[name] = key

            acc = entities.setdefault(key, {
                "key": key, "displayTitle": display, "names": [],
                "wikiTypes": [], "dives": [], "rolesByDive": {},
                "sources": set(), "ingestionPriorities": [], "dependsOn": set(),
                "dossierVaultStatus": {}, "evidence": [], "visuals": [],
                "_evidence_seen": set(), "_visual_by_ident": {},
            })
            if name not in acc["names"]:
                acc["names"].append(name)
            wtype = ent.get("wikiType")
            if wtype and wtype not in acc["wikiTypes"]:
                acc["wikiTypes"].append(wtype)
            if slug not in acc["dives"]:
                acc["dives"].append(slug)
            role = collapse_ws(ent.get("role"))
            if role:
                acc["rolesByDive"][slug] = role
            for s in (ent.get("sources") or []):
                acc["sources"].add(s)
            ip = ent.get("ingestionPriority")
            if isinstance(ip, int):
                acc["ingestionPriorities"].append(ip)
            for dep in (ent.get("dependsOn") or []):
                acc["dependsOn"].add(slugify_py(strip_md_suffix(str(dep))))
            acc["dossierVaultStatus"][slug] = ent.get("vaultStatus")

            for ref in (ent.get("evidenceRefs") or []):
                row = ev_map.get(ref)
                if row is None:
                    lint["unresolvedEvidenceRefs"].append(
                        {"key": key, "dive": slug, "ref": ref})
                    continue
                dedup = (slug, ref)
                if dedup in acc["_evidence_seen"]:
                    continue
                acc["_evidence_seen"].add(dedup)
                acc["evidence"].append({
                    "dive": slug,
                    "id": ref,
                    "genre": row.get("genre"),
                    "teiId": row.get("teiId"),
                    "pssTom": row.get("pssTom"),
                    "pages": row.get("pages"),
                    "date": str(row.get("date")) if row.get("date") is not None else None,
                    "addressee": collapse_ws(row.get("addressee")) or None,
                    "localPdf": row.get("localPdf"),
                    "extract": repo_rel(rel, row.get("extract")),
                    "facsimile": repo_rel(rel, row.get("facsimile")),
                    "quoteRu": collapse_ws(row.get("quoteRu")) or None,
                    "quoteEn": collapse_ws(row.get("quoteEn")) or None,
                    "significance": collapse_ws(row.get("significance")) or None,
                })

        # Attach visuals by relatedEntity (one name or a list); a visual tied to several entities is filed under each.
        for vis in visuals:
            related = vis.get("relatedEntity")
            names = related if isinstance(related, list) else [related]
            for name in names:
                rel_entity = collapse_ws(name)
                if not rel_entity:
                    continue
                key = dive_name_to_key.get(rel_entity) or slugify_py(rel_entity)
                acc = entities.get(key)
                if acc is None:
                    continue  # visual references an entity with no entity row; skip
                # Dedup across dives by url, then localPath, then id (the same image can be cached under different per-dive paths).
                ident = vis.get("url") or vis.get("localPath") or vis.get("id")
                existing = acc["_visual_by_ident"].get(ident)
                if existing is not None:
                    if slug != existing["dive"] and slug not in existing["alsoInDives"]:
                        existing["alsoInDives"].append(slug)
                    continue
                v = {
                    "dive": slug,
                    "id": vis.get("id"),
                    "type": vis.get("type"),
                    "subject": collapse_ws(vis.get("subject")) or None,
                    "relatedEvidence": vis.get("relatedEvidence"),
                    "licence": vis.get("licence"),
                    "usable": vis.get("usable"),
                    "url": vis.get("url"),
                    "localPath": repo_rel(rel, vis.get("localPath")),
                    "alsoInDives": [],
                }
                acc["_visual_by_ident"][ident] = v
                acc["visuals"].append(v)

    # Finalize each entity: vaultStatus live, reconcile priority, sort, lint.
    finalized = {}
    for key, acc in entities.items():
        live = live_by_id.get(key)
        if live is None and key in live_by_stem and live_by_stem[key] != key:
            # filename matches but its id differs from our key
            lint["slugMismatch"].append(
                {"key": key, "pageId": live_by_stem[key]})
            live = live_by_id.get(live_by_stem[key])
        if live is None:
            vault_status, vault_path, word_count = "missing", None, None
        else:
            vault_status = live["status"]
            vault_path = live["vaultPath"]
            word_count = live["wordCount"]

        # vaultStatus drift: dossier-reported vs live re-derivation
        dossier_vals = {v for v in acc["dossierVaultStatus"].values() if v}
        if dossier_vals and dossier_vals != {vault_status}:
            lint["vaultStatusDrift"].append({
                "key": key,
                "dossierSaid": sorted(dossier_vals),
                "liveIs": vault_status,
            })

        if len(acc["names"]) > 1:
            lint["nameConflicts"].append(
                {"key": key, "names": sorted(acc["names"]), "dives": sorted(acc["dives"])})
        if len(acc["wikiTypes"]) > 1:
            lint["wikiTypeConflicts"].append(
                {"key": key, "wikiTypes": sorted(acc["wikiTypes"]), "dives": sorted(acc["dives"])})
        if not acc["evidence"]:
            lint["entitiesWithZeroEvidence"].append(
                {"key": key, "dives": sorted(acc["dives"])})
        for wt in acc["wikiTypes"]:
            if wt not in WIKI_TYPES:
                lint["worksRoutedNotWiki"].append({"key": key, "wikiType": wt})

        priority = min(acc["ingestionPriorities"]) if acc["ingestionPriorities"] else None
        wiki_type = acc["wikiTypes"][0] if acc["wikiTypes"] else None

        acc["evidence"].sort(key=lambda e: (
            e["dive"], e["pssTom"] if isinstance(e["pssTom"], int) else 0,
            str(e["pages"] or ""), str(e["id"] or "")))
        for v in acc["visuals"]:
            v["alsoInDives"].sort()
        acc["visuals"].sort(key=lambda v: (v["dive"], str(v["id"] or "")))

        finalized[key] = {
            "key": key,
            "displayTitle": acc["displayTitle"],
            "names": acc["names"],
            "wikiType": wiki_type,
            "wikiTypeVariants": sorted(acc["wikiTypes"]),
            "vaultStatus": vault_status,
            "vaultPath": vault_path,
            "wordCount": word_count,
            "dossierVaultStatus": dict(sorted(acc["dossierVaultStatus"].items())),
            "ingestionPriority": priority,
            "dependsOn": sorted(d for d in acc["dependsOn"] if d),
            "dives": sorted(acc["dives"]),
            "sources": sorted(acc["sources"]),
            "rolesByDive": dict(sorted(acc["rolesByDive"].items())),
            "evidenceCount": len(acc["evidence"]),
            "evidence": acc["evidence"],
            "visuals": acc["visuals"],
        }

    # Sort lint lists for deterministic output.
    lint["unresolvedEvidenceRefs"].sort(key=lambda x: (x["dive"], x["key"], str(x["ref"])))
    lint["nameConflicts"].sort(key=lambda x: x["key"])
    lint["wikiTypeConflicts"].sort(key=lambda x: x["key"])
    lint["entitiesWithZeroEvidence"].sort(key=lambda x: x["key"])
    lint["missingWikilinkTarget"].sort(key=lambda x: (x["dive"], x["name"]))
    lint["worksRoutedNotWiki"].sort(key=lambda x: x["key"])
    lint["vaultStatusDrift"].sort(key=lambda x: x["key"])
    lint["slugMismatch"].sort(key=lambda x: x["key"])

    entities_sorted = [finalized[k] for k in sorted(finalized)]
    last_updated = max(topic_dates) if topic_dates else None
    by_status = {"exists": 0, "stub": 0, "missing": 0}
    for e in entities_sorted:
        by_status[e["vaultStatus"]] = by_status.get(e["vaultStatus"], 0) + 1

    meta = {
        "generator": "build_evidence_index.py",
        "builtFrom": [slug for slug, _, _ in dossiers],
        "diveCount": len(dossiers),
        "entityCount": len(entities_sorted),
        "evidenceRowCount": evidence_total,
        "visualCount": visual_total,
        "byVaultStatus": by_status,
        "lastUpdated": last_updated,
    }
    return entities_sorted, lint, meta


# ── Output: evidence-index.yaml ───────────────────────────────────────────────

YAML_HEADER = """\
# Machine-readable cross-dive evidence index.
# GENERATED by docs/research/lib/build_evidence_index.py from docs/research/*/dossier.yaml.
# Do not hand-edit — regenerate: python3 docs/research/lib/build_evidence_index.py
# Entities are keyed by the slug of wikilinkTarget (== the eventual wiki/works slug);
# vaultStatus is re-derived live against website/src/. This is an aggregation of
# already-verified dive research — the reuse bridge for wiki ingestion.
"""


def render_yaml(entities, lint, meta):
    doc = {"meta": meta, "entities": [strip_private(e) for e in entities], "lint": lint}
    body = yaml.safe_dump(
        doc, allow_unicode=True, sort_keys=False,
        default_flow_style=False, width=4096)
    return YAML_HEADER + body


def strip_private(entity):
    """Entities are already public-shaped; defensive copy without scratch keys."""
    return {k: v for k, v in entity.items() if not k.startswith("_")}


# ── Output: index.md (one line per block — serve.py renders with nl2br) ───────

def _attr_line(ev):
    bits = []
    if ev.get("pssTom") is not None:
        pages = f", pp. {ev['pages']}" if ev.get("pages") else ""
        bits.append(f"PSS Tom {ev['pssTom']}{pages}")
    elif ev.get("pages"):
        bits.append(str(ev["pages"]))
    if ev.get("teiId"):
        bits.append(f"TEI {ev['teiId']}")
    bits.append(ev["dive"])
    if ev.get("date"):
        bits.append(str(ev["date"]))
    return " · ".join(bits)


def render_index_md(entities, lint, meta):
    L = []
    L.append("---")
    L.append("layer: reference")
    L.append(f"lastUpdated: {meta.get('lastUpdated') or ''}")
    L.append("tags: [research]")
    L.append("---")
    L.append("")
    L.append("# Cross-dive evidence index")
    L.append("")
    L.append(
        "Generated aggregate of every corpus-dive dossier, keyed by entity. It collates "
        "the verified primary-source citations already gathered across all dives so wiki "
        "ingestion reuses them instead of re-collating by hand. Generated — do not hand-edit; "
        "regenerate with `python3 docs/research/lib/build_evidence_index.py`. "
        "Writing the wiki pages remains a separate, human-in-the-loop step.")
    L.append("")

    # § 1 At a glance
    recurring = [e for e in entities if len(e["dives"]) >= 2]
    bs = meta["byVaultStatus"]
    L.append("## 1. At a glance")
    L.append("")
    L.append(f"- {meta['diveCount']} dives · {meta['entityCount']} distinct entities · "
             f"{meta['evidenceRowCount']} evidence rows · {meta['visualCount']} visuals")
    L.append(f"- By vault status: {bs.get('exists', 0)} exists · "
             f"{bs.get('stub', 0)} stub · {bs.get('missing', 0)} missing")
    L.append(f"- {len(recurring)} entities recur across ≥2 dives")
    L.append("")

    # § 2 Ingestion work-order
    work = [e for e in entities
            if e["vaultStatus"] in ("missing", "stub") and e["evidenceCount"] > 0]
    work.sort(key=lambda e: (
        e["ingestionPriority"] if e["ingestionPriority"] is not None else 99,
        -e["evidenceCount"], e["key"]))
    L.append("## 2. Ingestion work-order")
    L.append("")
    L.append("Entities not yet written (or only stubbed) that already have verified evidence, "
             "ranked by ingestion priority then evidence count. These are ready to write — "
             "the citations are collated in §3.")
    L.append("")
    if work:
        L.append("| Entity | Type | Status | Dives | #Ev | Depends on |")
        L.append("|---|---|---|---|---|---|")
        for e in work:
            dep = ", ".join(e["dependsOn"]) if e["dependsOn"] else "—"
            L.append(f"| {e['displayTitle']} | {e['wikiType'] or '—'} | {e['vaultStatus']} "
                     f"| {', '.join(e['dives'])} | {e['evidenceCount']} | {dep} |")
        L.append("")
    else:
        L.append("_None — every entity with evidence already has a written page._")
        L.append("")
    zero = [e for e in entities if e["evidenceCount"] == 0]
    if zero:
        L.append(f"{len(zero)} entities are named across the dives but carry no evidence rows "
                 f"yet (research gaps, not ready to ingest): "
                 + ", ".join(e["displayTitle"] for e in zero) + ".")
        L.append("")

    # § 3 Collated citations, by entity
    L.append("## 3. Collated citations, by entity")
    L.append("")
    for e in entities:
        if e["evidenceCount"] == 0:
            continue
        L.append(f"### {e['displayTitle']}")
        L.append("")
        meta_bits = [e["wikiType"] or "—", e["vaultStatus"],
                     "dives: " + ", ".join(e["dives"])]
        if len(e["names"]) > 1:
            meta_bits.append("names: " + " / ".join(e["names"]))
        L.append(" · ".join(meta_bits))
        L.append("")
        for dive in e["dives"]:
            role = e["rolesByDive"].get(dive)
            if role:
                L.append(f"_{dive}_: {role}")
        L.append("")
        for ev in e["evidence"]:
            if ev.get("quoteRu"):
                L.append(f"> {ev['quoteRu']}")
                if ev.get("quoteEn"):
                    L.append(f"> {ev['quoteEn']}")
                L.append(f"> — {_attr_line(ev)}")
            else:
                L.append(f"- {_attr_line(ev)} — {ev.get('significance') or ''}".rstrip(" —"))
            L.append("")
        if e["visuals"]:
            usable = [v for v in e["visuals"] if v.get("usable")]
            L.append(f"Visuals: {len(e['visuals'])} ({len(usable)} usable) — "
                     + ", ".join(f"{v['subject']} [{v.get('licence') or '?'}]"
                                 for v in e["visuals"] if v.get("subject")))
            L.append("")

    # § 4 Integrity report
    L.append("## 4. Integrity report")
    L.append("")
    L += _lint_section("Unresolved evidenceRefs", lint["unresolvedEvidenceRefs"],
                       lambda x: f"{x['key']} → {x['ref']} ({x['dive']})")
    L += _lint_section("Name conflicts (same key, multiple spellings)", lint["nameConflicts"],
                       lambda x: f"{x['key']}: {' / '.join(x['names'])} ({', '.join(x['dives'])})")
    L += _lint_section("wikiType conflicts", lint["wikiTypeConflicts"],
                       lambda x: f"{x['key']}: {' / '.join(x['wikiTypes'])}")
    L += _lint_section("Works routed to works/ (not a wiki type)", lint["worksRoutedNotWiki"],
                       lambda x: f"{x['key']} ({x['wikiType']})")
    L += _lint_section("vaultStatus drift (dossier vs live)", lint["vaultStatusDrift"],
                       lambda x: f"{x['key']}: dossier {x['dossierSaid']} → live {x['liveIs']}")
    L += _lint_section("Entities with zero evidence", lint["entitiesWithZeroEvidence"],
                       lambda x: f"{x['key']} ({', '.join(x['dives'])})")
    L += _lint_section("Missing wikilinkTarget", lint["missingWikilinkTarget"],
                       lambda x: f"{x['name']} ({x['dive']})")
    L += _lint_section("Slug ≠ page id", lint["slugMismatch"],
                       lambda x: f"{x['key']} → page id {x['pageId']}")

    # § 5 Method
    L.append("## 5. Method")
    L.append("")
    L.append("Built by `docs/research/lib/build_evidence_index.py`, which walks every "
             "`docs/research/*/dossier.yaml`. Entity key = slug of `wikilinkTarget` "
             "(`.md` stripped), equal to the eventual wiki/works slug. Each entity's "
             "`evidenceRefs` are resolved against its own dive's `evidence[]`; visuals are "
             "attached by `relatedEntity` and deduped across dives. `vaultStatus` is "
             "re-derived live against `website/src/wiki/` and `website/src/works/` "
             "(stub = prose body < 60 words, or a `draft` with < 120). Output is "
             "deterministic. Regenerate: `python3 docs/research/lib/build_evidence_index.py`.")
    L.append("")
    return "\n".join(L) + "\n"


def _lint_section(title, items, fmt):
    out = [f"**{title}** ({len(items)})", ""]
    if items:
        for it in items:
            out.append(f"- {fmt(it)}")
    else:
        out.append("- none")
    out.append("")
    return out


# ── Main ──────────────────────────────────────────────────────────────────────

def integrity_failures(lint):
    """Hard failures for --check: genuinely broken links, not expected drift."""
    return len(lint["unresolvedEvidenceRefs"])


def main():
    ap = argparse.ArgumentParser(
        description="Aggregate corpus-dive dossiers into a cross-dive evidence index.")
    ap.add_argument("--check", action="store_true",
                    help="lint only; write nothing; exit 1 on broken links")
    ap.add_argument("--quiet", action="store_true", help="suppress per-entity lines")
    ap.add_argument("--research-dir", default=str(RESEARCH),
                    help="directory holding <slug>/dossier.yaml dives (default: docs/research)")
    args = ap.parse_args()

    research_dir = Path(args.research_dir).resolve()
    if not research_dir.is_dir():
        print(f"build_evidence_index.py: no such directory: {research_dir}", file=sys.stderr)
        sys.exit(2)

    try:
        dossiers = load_dossiers(research_dir)
    except yaml.YAMLError as exc:
        print(f"build_evidence_index.py: YAML parse error: {exc}", file=sys.stderr)
        sys.exit(2)
    if not dossiers:
        print(f"build_evidence_index.py: no <slug>/dossier.yaml under {research_dir}",
              file=sys.stderr)
        sys.exit(2)

    live_by_id, live_by_stem = build_live_vault_index()
    entities, lint, meta = aggregate(dossiers, live_by_id, live_by_stem)

    if not args.quiet:
        for e in entities:
            mark = {"exists": "✓", "stub": "·", "missing": "•"}.get(e["vaultStatus"], "?")
            print(f"  {mark} {e['key']:38s} {e['vaultStatus']:7s} "
                  f"{e['evidenceCount']:2d} ev  [{', '.join(e['dives'])}]")

    fails = integrity_failures(lint)
    drift = len(lint["vaultStatusDrift"])
    name_conf = len(lint["nameConflicts"])
    print()
    print(f"SUMMARY: {meta['diveCount']} dives, {meta['entityCount']} entities, "
          f"{meta['evidenceRowCount']} evidence rows, {meta['visualCount']} visuals · "
          f"{meta['byVaultStatus']['exists']} exists/{meta['byVaultStatus']['stub']} "
          f"stub/{meta['byVaultStatus']['missing']} missing · "
          f"{fails} unresolved ref(s), {name_conf} name conflict(s), {drift} drift")

    if args.check:
        if fails:
            print(f"build_evidence_index.py: {fails} unresolved evidenceRef(s) — FAIL",
                  file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    out_dir = research_dir / OUT_DIRNAME
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "evidence-index.yaml").write_text(
        render_yaml(entities, lint, meta), encoding="utf-8")
    (out_dir / "index.md").write_text(
        render_index_md(entities, lint, meta), encoding="utf-8")
    print(f"  ✓ wrote {out_dir.relative_to(REPO_ROOT)}/evidence-index.yaml")
    print(f"  ✓ wrote {out_dir.relative_to(REPO_ROOT)}/index.md")
    print("  → render HTML: python3 docs/serve.py --build-only")
    sys.exit(0)


if __name__ == "__main__":
    main()
