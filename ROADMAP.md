# Roadmap — Tolstoy Research Platform

Phase-by-phase implementation plan. The current phase is called out at the top of `AGENTS.md`. This file expands what each phase entails.

---

## Phase 1 — Wiki schema and conventions ✓

Define `wiki-schema.md` with page types (person, place, event, concept, institution, translator, adaptation, criticalWork, archivalFond), frontmatter templates, and the index/log conventions. Establish the sidecar pattern for works metadata.

## Phase 2 — Test run + scripted pipeline (current)

Pick 5–10 well-covered entities (e.g. Sophia Tolstaya, Yasnaya Polyana, Anna Karenina, War and Peace) and run the full wiki cycle: read TEI reference data + biographical sources, create/update wiki pages, populate frontmatter, add wikilinks, update index, log the operation. Validate the format in Obsidian before scaling up.

**Parallel track:** Build the Layer-1 scripted pipeline: `extract-graph.py`, `extract-frontmatter.py`, `generate-briefing.py`. These must be operational before Phase 3.

## Phase 3 — TEI reference data ingestion

Ingest `personList.xml` and `locationList.xml` from the tolstoydigital TEI data — 3,113 persons and 770 locations. Tier by proximity to Tolstoy: inner circle first, then wider associates, then the full dataset.

**Prerequisite:** LightRAG + Ollama (Qwen2.5:7b) operational and indexed (~8,000 files at this point). Set up nightly cron for incremental sync.

## Phase 4 — Biographical source ingestion

Cleaned Birukoff biography first, then Maude, then supplementary sources. Each ingestion enriches existing pages and creates new ones. Run a lint pass after each major source. LightRAG provides semantic querying across the growing vault.

## Phase 5 — Source texts and wikilinks

Convert TEI/XML chapter files to markdown in `text/` subfolders. Build a lookup table from the wiki (all person/place/work pages) and insert wikilinks on first occurrence per chapter. Human review in Obsidian.

At this scale (~26,500 files) all three layers of the scaled architecture are active.

## Phase 6 — Production workflow

Switch from direct writes to a PR model. AI proposes changes on a git branch; maintainer reviews and merges. Add validation tooling: frontmatter schema checks, wikilink resolution, orphan detection.
