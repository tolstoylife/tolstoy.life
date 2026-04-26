# AGENTS.md — Tolstoy Research Platform

Tool-agnostic instructions for AI assistants working on this project. Mission, architecture, data flow, schema, and operational model.

For Claude Code-specific overlay (OMC orchestration, skills), see `CLAUDE.md`.

---

## Mission

Build the most complete and accurately sourced English-language resource on Leo Tolstoy — his life, writings, manuscripts, and historical context — and make it freely readable online and offline.

---

## Architecture overview

This project uses the **LLM Wiki** pattern: an AI assistant incrementally builds and maintains a persistent wiki — the Obsidian vault — as the single source of truth for all structured metadata and prose content. Raw sources are read, key information extracted, and findings integrated into the vault: updating entity pages, revising article prose, maintaining cross-references, noting where new data contradicts old claims.

### Three-layer model

1. **Raw sources** — two locations, one role:
   - `primary-sources/` (project root, outside the vault) — large binary files: EPUBs, PDFs, TEI/XML archives, high-res images. Organised by **provenance** (`archive-org`, `jubilee-edition`, `standard-ebooks`), not by genre or work type.
   - `website/src/sources/` (inside the vault) — source cards (small `.md` stubs) plus `index.md` and `log.md`. Source cards make sources wikilink-able and visible in Obsidian's graph.

   The assistant reads from both locations but never modifies the binaries in `primary-sources/`.

   **Staging:** `website/src/_staging/` is a holding area for unverified clippings and extracted passages. It lives inside the vault directory (so materials can be wikilinked during review) but is excluded from git and the Eleventy build. Nothing in staging is used to write wiki content until human-verified.

2. **The wiki** (`website/src/wiki/` + `website/src/works/` + `website/src/letters/` + `website/src/images/`) — a structured, interlinked collection of markdown files. Wiki articles cover people, places, events, concepts, translators, institutions, adaptations, critical works, and archival fonds. Work files hold the full bibliography with metadata and prose. Source texts live in `text/` subfolders with wikilinks woven in. Letters have their own section to keep `works/` focused on literary output. Image metadata stubs live in `images/`.

3. **The schema** (`website/schema/wiki-schema.md` + `website/schema/tolstoy-works-schema.md`) — conventions, controlled vocabularies, page templates, and workflow definitions. Evolved collaboratively.

---

## Data flow

```
primary-sources/                                     (binary originals)
website/src/sources/*.md                             (source cards — wikilink-able)
website/src/_staging/                                (unverified clippings; not in git)
  └── Assistant reads source, discusses with human
        └── Assistant writes/updates vault files directly
              ├── website/src/wiki/*.md               (people, places, events, concepts, …)
              ├── website/src/works/**/*.md           (work overviews + text chapters)
              ├── website/src/letters/*.md            (correspondence)
              ├── website/src/images/*.md             (image metadata stubs)
              ├── website/src/sources/*.md            (source card updates)
              ├── website/src/sources/index.md        (catalog of all pages)
              └── website/src/sources/log.md          (operation log)
                    └── committed to git → Netlify build → tolstoy.life
```

**The rules:**

- Binaries in `primary-sources/` are immutable. Read only.
- Each major source gets a **source card** in `website/src/sources/` with metadata, a path to the binary, and ingestion status.
- `_resources/` is a free-form scratchpad for downloaded texts and unverified material not yet promoted to `primary-sources/`. Not tracked in git.
- `projects/` holds active production projects (e.g. epub scanning) with their own version control. Output moves to `primary-sources/` once verified.
- During the **R&D phase** (current), the assistant writes directly to vault files. Human reviews changes in Obsidian and git.
- When the project **goes live**, work shifts to a **PR workflow**: changes are proposed on a git branch and merged after maintainer review.
- **All historical claims must cite a primary source.** No unattributed facts, no literary interpretation.

---

## Wiki operations

Three core operations:

### Ingest

Add a new source. Read it, discuss key findings with the human, then:

1. Create or update relevant wiki pages (people, places, events, concepts, translators, institutions, adaptations, critical works, archival fonds)
2. Create or update relevant work pages (metadata + prose)
3. Add wikilinks connecting new content to existing pages
4. Update `website/src/sources/index.md`
5. Append an entry to `website/src/sources/log.md`

A single source may touch 10–15 wiki pages. Sources are ingested one at a time with human involvement — not batch-processed.

### Query

Ask questions against the wiki. Read the index to find relevant pages, drill in, synthesise. Good answers — comparisons, analyses, connections — should be filed back into the vault as new pages so they compound in the knowledge base.

### Lint

Periodic health checks: contradictions between pages, stale claims newer sources have superseded, orphan pages with no inbound wikilinks, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled from known sources.

---

## Scaled architecture: three-layer processing model

At full scope the vault will contain ~26,500 files (~72 MB, ~115,000 wikilinks) — beyond a single context window. The solution separates intelligence from computation across three layers:

### Layer 1 — Scripted pipeline (nightly cron, zero tokens)

Python scripts handle all mechanical, deterministic work: graph extraction from wikilinks and frontmatter, frontmatter indexing, change detection, dead-link and orphan detection, contradiction flagging, daily briefing generation. They also produce build artefacts the PWA depends on (per-work asset manifests, `relatedWiki` lists, wiki-previews bundle, `works.json` index).

### Layer 2 — LightRAG (nightly cron, zero API tokens)

Local semantic search and knowledge graph querying via Ollama with Qwen2.5:7b. Standard local backends (JSON files for KV + document status, NetworkX for graph, NanoVectorDB for vectors). Scripts in `lightrag/`; generated data in `lightrag/data/` (gitignored). Exposed as a local query API on port 8420 that the assistant can call during wiki operations.

### Layer 3 — AI sessions (on demand, API tokens)

The assistant handles work that requires judgement: source reading, claim extraction, prose writing, contradiction resolution, significance assessment. Produces an **update manifest** (JSON) listing every factual claim and affected pages. Layer 1 scripts verify manifest completeness post-session.

### When each layer activates

- **Phase 2 (current):** Layer 1 only — vault still small enough for direct access.
- **Phase 3 (TEI ingestion, ~8,000 files):** Layer 2 must be operational before bulk ingestion.
- **Phase 5+ (~26,500 files):** All three layers active.

> Cost and capacity details (token budgets, hardware specs, indexing times) live in [docs/architecture/internal-operations.md](./docs/architecture/internal-operations.md). Phase-by-phase plan in [ROADMAP.md](./ROADMAP.md).

---

## Index, log, and changelog

All in `website/src/sources/` (excluded from Eleventy — never generates pages on the live site), except the changelog which is public.

- **`website/src/sources/index.md`** — content-oriented catalog of every page in the wiki (`wiki/` + `works/`). Each entry has a wikilink, a one-line summary, optional metadata. Organised by type. Updated on every ingest. Read first when navigating the vault.

- **`website/src/sources/log.md`** — chronological, append-only record of operations. Each entry: `## [YYYY-MM-DD] operation | Subject`. Operations: `ingest`, `query`, `lint`, `edit`. Captures *why* something happened — narrative context git history alone doesn't carry.

- **`website/src/pages/changelog.md`** — public-facing record at `/changelog/` on tolstoy.life. Date-based versioning (`YYYY-MM-DD`), grouped under **New content**, **Improvements**, **Corrections**. Append an entry whenever changes are pushed to GitHub. Reader-facing only — internal refactoring, schema tweaks, and other invisible-to-visitors changes are skipped.

---

## Shared vocabulary

**LT** — Leo Nikolaevich Tolstoy (1828–1910).

**NS / Gregorian** — New Style dates. The canonical value for all dates in this project.

**OS / Julian** — Old Style dates. Russia used the Julian calendar until 1 February 1918. In the 19th century the Julian calendar ran 12 days behind Gregorian; from 1 March 1900, 13 days behind. All dates that predate the Russian calendar reform must record both NS and OS values.

**Jubilee Edition** — *Полное собрание сочинений* (Complete Collected Works), 90 volumes, 1928–1964. The canonical scholarly edition for all Russian-language texts.

**Yasnaya Polyana** — Tolstoy's primary estate and the location where most of his major works were written, in Tula Oblast, Russia (54.0667°N, 37.5167°E).

**wikilink** — An Obsidian-style `[[double-bracket link]]` connecting articles within the vault. First-class — part of the knowledge graph, not decoration.

**TEXT zone** — The source text of a work, in a separate file within the work's `text/` subfolder. Contains the full text with `[[wikilinks]]` woven in. Marked with `<!-- TEXT — source text, do not modify -->`. Never touched by wiki maintenance operations.

---

## Schema

All work metadata follows `website/schema/tolstoy-works-schema.md` (v6). Wiki article metadata follows `website/schema/wiki-schema.md` (v1.1). These are the single references for field names, types, controlled vocabulary values, and examples.

### Key rules

- YAML fields → **camelCase** (`titleEn`, `dateFirstPublished`, `authoringLocations`).
- `id` is the canonical slug (e.g., `anna-karenina`) — unique across all works, primary key everywhere.
- Dates are ISO 8601 (`YYYY-MM-DD`, `YYYY-MM`, or `YYYY`). Uncertain dates use a companion `*Approximate: true`.
- Every date predating 1918 must have a `...OldStyle` companion field with the Julian (OS) value.
- `language` is ISO 639-1 (`ru`, `fr`).
- Controlled vocabulary: use only values listed in the relevant schema. Don't introduce free-form values without updating the schema first.
- Empty optional fields use `""` (string) or `[]` (array) — never `null` or omitted.
- Prefer Wikidata QIDs as the primary external identifier anchor.

For the full controlled vocabulary tables (genre, completionStatus, draftLabel, condition, authorityType, scope, relationToAuthor, relationshipType, recordStatus, wiki type) and the controlled transcribers list, see the schema files. They are the source of truth — don't duplicate here.

---

## Content and accuracy standards

- All historical claims (dates, locations, archival references) must be sourced. Flag uncertain information with an `approximate` boolean or a `notes` field — never silently guess.
- Russian text in Cyrillic script. Romanisation follows Library of Congress transliteration unless the source uses a different convention.
- Work titles must appear in both `titleEn` (English) and `titleRu` (Cyrillic).
- Primary sources take precedence. In order of authority: Jubilee Edition → Tolstoy's diaries and letters → Birukoff biography → Chertkov correspondence → Maude biography.
- When sources conflict, record **all** values and note the conflict in the relevant `notes` field. Authority order determines the canonical value, but competing claims are always preserved — never silently discarded.

---

## Project structure

Tier-2 platform (per `~/Projects/PROJECT-TEMPLATE.md`): root surface files plus peer-level sub-components.

```
/Volumes/Graugear/Tolstoy/
├── README.md · TODO.md · LOG.md           ← project surface (dashboard reads TODO + LOG)
├── AGENTS.md · CLAUDE.md                  ← AI instructions
├── ROADMAP.md                             ← phase plan
├── MANIFEST.md · LICENSE                  ← public statement, public-domain dedication
├── docs/                                  ← tracked operational docs (architecture/, pwa/, editorial/, design/)
├── _generated/                            ← UNTRACKED: session handoffs, rendered HTML, drafts, decks
├── _resources/ · _design/ · _docs/        ← untracked workspaces
├── lightrag/                              ← Layer 2: semantic search + KG (port 8420)
├── primary-sources/                       ← immutable binary sources, by provenance
├── projects/                              ← active production projects with own version control
├── website/                               ← PWA, e-reader, Obsidian vault (submodule)
├── tools/                                 ← `tl` ebook build toolset (submodule)
└── splash/                                ← pre-launch placeholder site
```

Sub-components (`website/`, `tools/`, `projects/*`) are independent and may have their own AGENTS.md / CLAUDE.md / README.md.

---

## Website (PWA, e-reader, vault)

`website/src/` is the Obsidian vault root and the Eleventy input. Six core sections: **Wiki**, **Works**, **Letters**, **Images**, **My Library** (user-facing offline reading), **E-reader** — plus posts and pages.

**Stack:** Eleventy (11ty) · Obsidian · Vanilla HTML/CSS/JS · Netlify deploys from committed `.md` files (no DB, no build-time network).

**Vault is unified** — `wiki/`, `works/`, `letters/`, `images/`, source texts share one wikilink namespace. **There is no separate wiki article for a work** — the work's own file (`website/src/works/.../Anna Karenina.md`) is canonical for it.

**Filename convention:** human-readable title-case (`Anna Karenina.md`). Required for Obsidian wikilinks. Clean URLs handled by `permalink` derived from the `id` slug. Text landing files use em-dash (`Anna Karenina — Text.md`) to avoid wikilink collision with the overview file.

**Sidecar pattern:** core frontmatter in the `.md` file, deep schema-v6 metadata (manuscripts, transcriptions, bans, fieldSources) in a companion `[id].data.yaml` sidecar consumed via Eleventy data cascade.

**TEXT zone** in source text files is never touched by wiki maintenance.

**Eleventy ignores:** `website/src/sources/` and `website/src/_staging/` excluded via `.eleventyignore`.

**CSS:** CUBE CSS layered on Every Layout, Tailwind as token compiler only (no utility classes in HTML). **JS:** vanilla, ES modules, progressive enhancement, no frameworks.

**PWA architecture details:** see [docs/pwa/](./docs/pwa/) — `local-first-architecture.md`, `wiki-integration.md`, `stage-1-implementation.md`, `tl-pipeline-integration.md` (build artefact contracts: `works.json`, per-work `manifest.json`, hashed `wiki-previews-v<date>-<hash>.json`, deterministic versioning), `yjs-schema-and-sync.md` (Stage-4 CRDT). `docs/pwa/README.md` is the index.

**Chapter URI convention:** every chapter in `website/src/works/.../text/*.md` declares `chapterUri: urn:tolstoy-life:<work>:<book-X-chapter-Y>` in frontmatter. Build fails if missing. URIs are stable across renumbering — annotations follow the URI, not the URL.

**Build:** `cd website && npm run build` (production), `npm start` (dev), `npm run test:a11y` (accessibility).

---

## Tools (ebook toolset)

`tools/` is a fork of the [Standard Ebooks toolset](https://github.com/standardebooks/tools), invoked via `tl` (renamed from `se` to coexist with upstream). Opinionated editorial pipeline producing distributable `.epub` files for the tolstoy.life imprint, sideloading, and the in-browser PWA reader.

For commands, source-directory format, metadata sourcing, branding, and upstream-sync notes, see `tools/README.md` (or run `tl help` / `tl <command> --help`).

**Metadata rule:** `content.opf` values come from canonical YAML in `website/src/works/`. Don't invent or hand-estimate. The `SE_SLUG` placeholder must match the `id` slug.

---

## Contribution model

Primary channel: **GitHub Issues**. Templates cover factual corrections (claim, source, suggested fix), prose suggestions, and missing works/sources.

For git-comfortable contributors:

- **Wiki content PRs** (maintainer validation required): any PR touching wiki article prose or work metadata must cite the specific primary source for every claim.
- **Text wikilink PRs** (open — no factual review): anyone may PR additions or corrections to `[[wikilinks]]` within source text files in `text/` subfolders. Targets must resolve to existing files.

The contribution model relies on GitHub repo configuration outside markdown: `.github/ISSUE_TEMPLATE/`, `CODEOWNERS`, `.github/PULL_REQUEST_TEMPLATE.md`, branch protection on `main`, `.github/workflows/` (schema validation, wikilink resolution, dead-link checks, `relatedWiki` completeness). The PWA's "Improve this article" deep-link assumes these exist.

---

## Roadmap

Phase-by-phase plan: [ROADMAP.md](./ROADMAP.md).

Current: **Phase 2** — wiki schema test run (5–10 well-covered entities) plus Layer-1 scripted pipeline. Layer 2 (LightRAG) operational before Phase 3 begins.

---

## GitHub repositories

The platform spans four repos under the `tolstoylife` org:

- **tolstoy.life** — parent repo (this directory). Tracks root surface files (`README`, `TODO`, `LOG`, `AGENTS`, `CLAUDE`, `ROADMAP`, `MANIFEST`, `LICENSE`), `docs/`, `lightrag/` code, and submodule pointers. Subprojects, binaries, `_generated/`, `_resources/`, `_design/`, and `_docs/` are excluded via `.gitignore` (local-only).
- **website** — PWA, e-reader, vault. Submodule.
- **tools** — `tl` ebook toolset. Submodule.
- **splash** — pre-launch placeholder.
