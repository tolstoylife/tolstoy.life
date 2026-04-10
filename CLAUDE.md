# CLAUDE.md — Tolstoy Research Project

This folder contains the projects that together form a scholarly publishing platform about the life and works of Leo Tolstoy (LT).

```
/Volumes/Graugear/Tolstoy/
├── CLAUDE.md              ← this file — shared context for all projects
├── MANIFEST.md            ← public project statement
├── website/               ← front-end PWA, e-reader, and Obsidian vault (tolstoy.life)
├── splash/                ← temporary splash site (pre-launch placeholder)
├── corpus/                ← archived data pipeline (LightRAG, now retired)
├── primary-sources/       ← immutable primary source files (EPUBs, TEI/XML, images)
├── _generated/            ← internal outputs from Claude (tasks, analyses, notes)
└── tools/                 ← utilities and helper scripts
```

Each sub-project has its own `CLAUDE.md` covering project-specific conventions. This file covers what is shared: mission, vocabulary, data flow, the canonical schema, and the wiki maintenance model.

---

## Mission

To build the most complete and accurately sourced English-language resource on Leo Tolstoy — his life, writings, manuscripts, and historical context — and to make it freely readable online and offline.

---

## Architecture — the LLM Wiki model

This project follows the **LLM Wiki** pattern: instead of using RAG or a graph database, Claude incrementally builds and maintains a persistent wiki — the Obsidian vault — as the single source of truth for all structured metadata and prose content. Raw sources are read by Claude, key information is extracted, and findings are integrated into the existing vault: updating entity pages, revising article prose, maintaining cross-references, noting where new data contradicts old claims.

The three layers:

1. **Raw sources** — two locations, one role:
   - `primary-sources/` (project root, outside the vault) — large binary files: EPUBs, PDFs, TEI/XML archives, high-res images. Too large or non-renderable for Obsidian.
   - `src/sources/` (inside the vault) — source cards (small `.md` stubs), plus `index.md` and `log.md`. Source cards make sources wikilink-able and visible in Obsidian's graph. Also contains the canonical index of all wiki pages and the chronological operation log.
   - `src/_staging/` — staging area for unverified clippings, notes, and extracted passages. Not committed to git, not compiled by Eleventy.

   Claude reads from both locations but never modifies the binaries in `primary-sources/`. Source cards are maintained by Claude.
2. **The wiki** (the Obsidian vault: `src/wiki/` + `src/works/`) — a structured, interlinked collection of markdown files maintained by Claude. Wiki articles cover people, places, events, and concepts. Work files hold the full bibliography with metadata and prose. Source texts live in `text/` subfolders with wikilinks woven in.
3. **The schema** (this file + `website/schema/wiki-schema.md` + `website/schema/tolstoy-works-schema.md`) — conventions, controlled vocabularies, page templates, and workflow definitions. Evolved collaboratively between Johan and Claude.

### What was retired

The previous architecture used **LightRAG** (a local knowledge graph on Ollama) and **Supabase** (a hosted database) as intermediate layers between raw sources and the vault. These have been retired in favour of the direct LLM Wiki model:

- **LightRAG / corpus pipeline** — the `corpus/` project is archived. The graph database, ingestion scripts, and local Ollama dependency are no longer used. Raw source files that lived in `corpus/data/` should be moved to `primary-sources/` or `src/_staging/`.
- **Supabase** — the hosted database that stored works metadata is no longer the source of truth. YAML frontmatter in the vault files is now canonical.
- **generate-md.js** — the sync script that fetched from Supabase and wrote frontmatter is retired. Claude writes frontmatter directly.

The `corpus/` directory is preserved as an archive for reference but is not part of the active workflow. See `corpus/CLAUDE.md` for details.

---

## Data flow

```
primary-sources/                (binary originals — EPUBs, PDFs, TEI/XML, images)
src/sources/*.md                (source cards — metadata stubs, wikilink-able)
src/_staging/                   (staging — clippings, notes, extracted passages; not in git)
  └── Claude reads source, discusses with Johan
        └── Claude writes/updates vault files directly
              ├── src/wiki/*.md                (people, places, events, concepts)
              ├── src/works/**/*.md            (work overviews + text chapters)
              ├── src/sources/*.md             (source card updates — ingestion status)
              ├── src/sources/index.md         (catalog of all pages)
              └── src/sources/log.md           (chronological record of operations)
                    └── committed to git → Netlify build → tolstoy.life
```

**The rules:**
- Binary source files in `primary-sources/` are immutable. Claude reads from them but never modifies them.
- Each major source gets a **source card** in `src/sources/` — a small `.md` stub with metadata, a path to the binary, and ingestion status. Source cards are wikilink-able, so sources appear in Obsidian's graph alongside the wiki articles they feed.
- `src/_staging/` is the staging area for unverified source material — clipped articles, notes, PDFs. It lives inside the Obsidian vault so materials can be wikilinked and cross-referenced, but nothing in `src/_staging/` is used to write wiki content until it has been human-verified.
- During the **R&D phase** (current), Claude writes directly to vault files. Johan reviews changes in Obsidian and git.
- When the project **goes live**, Claude shifts to a **PR workflow**: changes are proposed on a git branch and merged after maintainer review.
- All historical claims must cite a primary source. No unattributed facts, no literary interpretation.

---

## Wiki operations

Following the LLM Wiki pattern, there are three core operations:

### Ingest

Add a new source to the project. Claude reads the source, discusses key findings with Johan, then:
1. Creates or updates relevant wiki pages (people, places, events, concepts)
2. Creates or updates relevant work pages (metadata + prose)
3. Adds wikilinks connecting the new content to existing pages
4. Updates `src/sources/index.md`
5. Appends an entry to `src/sources/log.md`

A single source may touch 10–15 wiki pages. Sources are ingested one at a time with Johan involved — not batch-processed.

### Query

Ask questions against the wiki. Claude reads the index to find relevant pages, drills into them, and synthesises an answer. Good answers — comparisons, analyses, connections — should be filed back into the wiki as new pages so they compound in the knowledge base.

### Lint

Periodic health checks. Claude reviews the wiki for:
- Contradictions between pages
- Stale claims that newer sources have superseded
- Orphan pages with no inbound wikilinks
- Important concepts mentioned but lacking their own page
- Missing cross-references
- Data gaps that could be filled from known sources

---

## Index and log

Both files live in `src/sources/` — which is excluded from Eleventy — so they never generate pages on the live site.

**`src/sources/index.md`** — content-oriented catalog of every page in the wiki (both `src/wiki/` and `src/works/`). Each entry has a wikilink, a one-line summary, and optionally metadata. Organised by type (people, places, events, concepts, works). Updated on every ingest. Claude reads this first when navigating the vault.

**`src/sources/log.md`** — chronological, append-only record of operations. Each entry starts with a consistent prefix: `## [YYYY-MM-DD] operation | Subject`. Operations: `ingest`, `query`, `lint`, `edit`. The log gives narrative context that git history alone doesn't capture — *why* something was ingested, what was found, what questions remain.

---

## Shared vocabulary

**LT** — Leo Nikolaevich Tolstoy (1828–1910).

**NS / Gregorian** — New Style dates. The Gregorian calendar, used as the canonical value for all dates in this project.

**OS / Julian** — Old Style dates. Russia used the Julian calendar until 1 February 1918. In the 19th century the Julian calendar ran 12 days behind Gregorian; from 1 March 1900, 13 days behind. All dates that predate the Russian calendar reform must record both NS and OS values.

**Jubilee Edition** — *Полное собрание сочинений* (Complete Collected Works), 90 volumes, 1928–1964. The canonical scholarly edition for all Russian-language texts.

**Yasnaya Polyana** — Tolstoy's primary estate and the location where most of his major works were written, in Tula Oblast, Russia (54.0667°N, 37.5167°E).

**wikilink** — An Obsidian-style `[[double-bracket link]]` connecting articles within the vault. Used throughout `src/wiki/`, `src/works/` prose, and the source texts themselves. Wikilinks are first-class — they are part of the knowledge graph, not decoration.

**TEXT zone** — The source text of a work, in a separate file within the work's `text/` subfolder. Contains the full text with `[[wikilinks]]` woven in. Marked with `<!-- TEXT — source text, do not modify -->`. Never touched by wiki maintenance operations.

---

## Canonical schema reference

All work metadata follows the schema defined in `website/schema/tolstoy-works-schema.md` (v5). Wiki article metadata follows `website/schema/wiki-schema.md`. These are the single references for field names, types, controlled vocabulary values, and examples.

### Naming convention

- YAML fields → **camelCase** (e.g., `titleEn`, `dateFirstPublished`, `authoringLocations`)

### Key rules

- `id` is the canonical slug (e.g., `anna-karenina`) — unique across all works and used as the primary key everywhere.
- Dates are ISO 8601 strings (`YYYY-MM-DD`, `YYYY-MM`, or `YYYY`). Uncertain dates use a companion `*Approximate: true` boolean field.
- Every date field that predates 1918 must have a `...OldStyle` companion field recording the Julian (OS) value as found in Russian sources.
- `language` is ISO 639-1 (e.g., `ru`, `fr`).
- Controlled vocabulary fields must use only values listed in the relevant schema. Never introduce free-form values without updating the schema first.
- Empty optional fields use `""` (string) or `[]` (array) — never `null` or omitted.
- Prefer Wikidata QIDs as the primary external identifier anchor.

### Controlled vocabulary quick reference

**genre:** `novel` · `novella` · `short_story` · `parable` · `play` · `essay` · `philosophical` · `religious` · `diary` · `letter` · `poem` · `fragment`

**completionStatus:** `complete` · `incomplete` · `fragmentary`

**firstPublishedVenueType / firstPublishedInRussiaVenueType:** `journal` · `newspaper` · `book` · `samizdat`

**draftLabel:** `first-draft` · `intermediate-draft` · `final-draft` · `fair-copy` · `printers-copy`

**condition:** `good` · `fair` · `poor` · `damaged` · `lost`

**authorityType (bans):** `imperial-state` · `holy-synod` · `foreign-government` · `periodical-editor` · `other`

**scope (bans):** `complete-ban` · `passages-cut` · `serialization-refused` · `confiscation` · `pre-publication-rejected`

**relationToAuthor (transcriptions):** `wife` · `daughter` · `son` · `secretary` · `physician` · `friend` · `self` · `other`

**relationshipType (relatedWorks):** `cycle` · `sequel` · `prequel` · `revision` · `source` · `companion` · `adaptation`

**recordStatus:** `draft` · `reviewed` · `verified`

### Controlled transcribers

| `transcriberId` | Name |
|---|---|
| `sophia-tolstaya` | Sophia Andreevna Tolstaya |
| `tatyana-tolstaya` | Tatyana Lvovna Tolstaya |
| `maria-tolstaya` | Maria Lvovna Tolstaya |
| `nikolai-gusev` | Nikolai Nikolaevich Gusev |
| `leo-tolstoy` | Leo Nikolaevich Tolstoy (autograph) |
| `other` | Other — specify in `transcriberName` |

---

## Content and accuracy standards

- All historical claims (dates, locations, archival references) must be sourced. Flag uncertain information with an `approximate` boolean or a `notes` field — never silently guess.
- Russian text in Cyrillic script. Romanisation follows Library of Congress transliteration unless the source uses a different convention.
- Work titles must appear in both `titleEn` (English) and `titleRu` (Cyrillic).
- Primary sources take precedence. In order of authority: Jubilee Edition → Tolstoy's diaries and letters → Birukoff biography → Chertkov correspondence → Maude biography.
- When sources conflict, record both values and note the conflict in the relevant `notes` field. Never silently prefer one source over another.

---

## Contribution model

The primary contribution channel for general readers is **GitHub Issues**. Issue templates should cover three cases: factual corrections (claim, source, suggested fix), prose suggestions, and missing works or sources.

For contributors comfortable with git, pull requests remain welcome:

**Wiki content PRs** (maintainer validation required before merge): any PR touching wiki article prose or work metadata must cite the specific primary source for every claim. A maintainer reviews the diff against that source before merging.

**Text wikilink PRs** (open — no factual review required): anyone may fork and PR additions or corrections to `[[wikilinks]]` within source text files in `text/` subfolders. Wikilink targets must resolve to existing files in the vault.

---

## Vault and file structure

The Obsidian vault (`src/`) is unified — `wiki/` articles, `works/` overview pages, and source texts all live in the same graph and share the same wikilink namespace.

**There is no separate wiki article for a work.** The work's own file (`src/works/fiction/novels/anna-karenina/Anna Karenina.md`) is the canonical article for that work. Wiki articles in `src/wiki/` cover people, places, events, and concepts — not works.

**Work folder structure:**
```
src/works/fiction/novels/anna-karenina/
├── Anna Karenina.md          ← overview article (frontmatter + prose)
├── anna-karenina.data.yaml   ← sidecar: deep scholarly metadata (manuscripts, transcriptions, bans, fieldSources)
└── text/
    ├── Anna Karenina — Text.md  ← text landing / table of contents
    ├── Part 1, Chapter 1.md
    ├── Part 1, Chapter 2.md
    ├── ...
    └── assets/
        └── repin-portrait-1887.jpg
```

**Sidecar convention:** Each work's `.md` file contains core frontmatter (identity, dates, genre, locations, identifiers, themes). The full schema v5 metadata — manuscripts, transcriptions, bans, fieldSources — lives in a companion `[id].data.yaml` file in the same folder. This keeps the markdown readable in Obsidian while preserving the complete scholarly record. Eleventy consumes the sidecar via data cascade.

**Filename convention:** Files use human-readable title-case names (e.g. `Anna Karenina.md`, not `index.md` or `anna-karenina.md`). This is required for Obsidian wikilinks to resolve correctly. Clean URLs on the live site are handled by the `permalink` field in `works.11tydata.json`, derived from the `id` slug — not from the filename.

---

## E-reader design notes

Works are rendered from Markdown in the e-reader, preserving Obsidian-style `[[wikilinks]]`. The UI renders these as interactive links with a toggleable mode: readers can turn wikilinks on or off, and when on, tapping or hovering a wikilink opens a modal preview sourced from the corresponding `src/wiki/` article or work file — similar to Wikipedia's link previews. Wiki summary content should be bundled at build time (not fetched on demand) to support offline PWA use.

---

## Implementation plan

### Phase 1 — Wiki schema and conventions (current)

Define `wiki-schema.md` with page types (person, place, event, concept), frontmatter templates, and the index/log conventions. Update all CLAUDE.md files. Establish the sidecar pattern for works metadata.

### Phase 2 — Test run

Pick 5–10 well-covered entities (e.g. Sophia Tolstaya, Yasnaya Polyana, Anna Karenina, War and Peace) and run the full wiki cycle: read TEI reference data + biographical sources, create/update wiki pages, populate frontmatter, add wikilinks, update index, log the operation. Validate the format in Obsidian before scaling up.

### Phase 3 — TEI reference data ingestion

Ingest `personList.xml` and `locationList.xml` from the tolstoydigital TEI data — 3,113 persons and 770 locations. Create wiki pages tiered by proximity to Tolstoy: inner circle first, then wider associates, then the full dataset.

### Phase 4 — Biographical source ingestion

Ingest the cleaned Birukoff biography, then Maude, then supplementary sources. Each ingestion enriches existing pages and creates new ones. After each major source, run a lint pass.

### Phase 5 — Source texts and wikilinks

Convert TEI/XML chapter files to markdown in `text/` subfolders. Build a lookup table from the wiki (all person/place/work pages) and insert wikilinks on first occurrence per chapter. Human review in Obsidian.

### Phase 6 — Production workflow

Switch from direct writes to a PR model. Claude proposes changes on a git branch; Johan reviews and merges. Add validation tooling (frontmatter schema checks, wikilink resolution, orphan detection).
