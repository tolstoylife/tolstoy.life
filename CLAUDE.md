# CLAUDE.md — Tolstoy Research Platform

This document defines the mission, architecture, data flow, schema, and operational model for the scholarly publishing platform at tolstoy.life.

---

## Mission

To build the most complete and accurately sourced English-language resource on Leo Tolstoy — his life, writings, manuscripts, and historical context — and to make it freely readable online and offline.

---

## Architecture overview

This project uses the **LLM Wiki** pattern: Claude incrementally builds and maintains a persistent wiki — the Obsidian vault — as the single source of truth for all structured metadata and prose content. Raw sources are read by Claude, key information is extracted, and findings are integrated into the vault: updating entity pages, revising article prose, maintaining cross-references, noting where new data contradicts old claims.

### Three-layer model

1. **Raw sources** — two locations, one role:
   - `primary-sources/` (project root, outside the vault) — large binary files: EPUBs, PDFs, TEI/XML archives, high-res images. Too large or non-renderable for Obsidian.
   - `website/src/sources/` (inside the vault) — source cards (small `.md` stubs), plus `index.md` and `log.md`. Source cards make sources wikilink-able and visible in Obsidian's graph. Also contains the canonical index of all wiki pages and the chronological operation log.
   
   Claude reads from both locations but never modifies the binaries in `primary-sources/`. Source cards are maintained by Claude.
   
   **Staging:** `website/src/_staging/` is a holding area for unverified clippings, notes, and extracted passages. It lives inside the Obsidian vault directory (so materials can be wikilinked during review) but is excluded from git and from the Eleventy build via `.gitignore`. Nothing in staging is used to write wiki content until it has been human-verified.

2. **The wiki** (the Obsidian vault: `website/src/wiki/` + `website/src/works/`) — a structured, interlinked collection of markdown files maintained by Claude. Wiki articles cover people, places, events, and concepts. Work files hold the full bibliography with metadata and prose. Source texts live in `text/` subfolders with wikilinks woven in.

3. **The schema** (sections below + `website/schema/wiki-schema.md` + `website/schema/tolstoy-works-schema.md`) — conventions, controlled vocabularies, page templates, and workflow definitions. Evolved collaboratively between Johan and Claude.

---

## Data flow

```
primary-sources/                                     (binary originals)
website/src/sources/*.md                             (source cards — wikilink-able)
website/src/_staging/                                (unverified clippings; not in git)
  └── Claude reads source, discusses with Johan
        └── Claude writes/updates vault files directly
              ├── website/src/wiki/*.md               (people, places, events, concepts)
              ├── website/src/works/**/*.md           (work overviews + text chapters)
              ├── website/src/sources/*.md            (source card updates)
              ├── website/src/sources/index.md        (catalog of all pages)
              └── website/src/sources/log.md          (operation log)
                    └── committed to git → Netlify build → tolstoy.life
```

**The rules:**

- Binary source files in `primary-sources/` are immutable. Claude reads from them but never modifies them. The folder is organised by **provenance** (where the material came from: `archive-org`, `jubilee-edition`, `standard-ebooks`, etc.) — never by genre or work type.
- Each major source gets a **source card** in `website/src/sources/` — a small `.md` stub with metadata, a path to the binary, and ingestion status. Source cards are wikilink-able.
- `_resources/` is a free-form scratchpad for downloaded texts, research clippings, and unverified material that has not yet been promoted to `primary-sources/`. It is not tracked in git.
- `projects/` holds active production projects (e.g. epub scanning/production) that need their own version control. A project moves its finished output into `primary-sources/` once complete and verified.
- `website/src/_staging/` is for unverified material. Nothing in staging is used to write wiki content until it has been human-verified.
- During the **R&D phase** (current), Claude writes directly to vault files. Johan reviews changes in Obsidian and git.
- When the project **goes live**, Claude shifts to a **PR workflow**: changes are proposed on a git branch and merged after maintainer review.
- **All historical claims must cite a primary source.** No unattributed facts, no literary interpretation.

---

## Wiki operations

Following the LLM Wiki pattern, there are three core operations:

### Ingest

Add a new source to the project. Claude reads the source, discusses key findings with Johan, then:

1. Creates or updates relevant wiki pages (people, places, events, concepts)
2. Creates or updates relevant work pages (metadata + prose)
3. Adds wikilinks connecting the new content to existing pages
4. Updates `website/src/sources/index.md`
5. Appends an entry to `website/src/sources/log.md`

A single source may touch 10–15 wiki pages. Sources are ingested one at a time with Johan involved — not batch-processed.

### Query

Ask questions against the wiki. Claude reads the index to find relevant pages, drills into them, and synthesises an answer. Good answers — comparisons, analyses, connections — should be filed back into the vault as new pages so they compound in the knowledge base.

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

Both files live in `website/src/sources/` — which is excluded from Eleventy — so they never generate pages on the live site.

**`website/src/sources/index.md`** — content-oriented catalog of every page in the wiki (both `website/src/wiki/` and `website/src/works/`). Each entry has a wikilink, a one-line summary, and optionally metadata. Organised by type (people, places, events, concepts, works). Updated on every ingest. Claude reads this first when navigating the vault.

**`website/src/sources/log.md`** — chronological, append-only record of operations. Each entry starts with a consistent prefix: `## [YYYY-MM-DD] operation | Subject`. Operations: `ingest`, `query`, `lint`, `edit`. The log gives narrative context that git history alone doesn't capture — *why* something was ingested, what was found, what questions remain.

---

## Changelog

**`website/src/pages/changelog.md`** — public-facing record of all notable changes, rendered at `/changelog/` on tolstoy.life. Uses date-based versioning (`YYYY-MM-DD`), not semver. Entries are grouped by date under three categories: **New content**, **Improvements**, and **Corrections**.

**When to update:** Claude appends an entry to the changelog whenever Johan pushes changes to GitHub. The entry should summarise what changed from a reader's perspective — new wiki articles, new works, site improvements, factual corrections. Internal refactoring, schema tweaks, and other changes invisible to visitors do not need entries.

**Format:**

```md
## YYYY-MM-DD

### New content
- Wiki article: Sophia Tolstaya — biography sourced from Birukoff and Maude

### Improvements
- E-reader now shows chapter table of contents in side menu

### Corrections
- Fixed first publication date for Anna Karenina (1878 → 1877)
```

Omit any category that has no entries for a given date. Most recent date goes at the top, below the introductory paragraph.

---

## Shared vocabulary

**LT** — Leo Nikolaevich Tolstoy (1828–1910).

**NS / Gregorian** — New Style dates. The Gregorian calendar, used as the canonical value for all dates in this project.

**OS / Julian** — Old Style dates. Russia used the Julian calendar until 1 February 1918. In the 19th century the Julian calendar ran 12 days behind Gregorian; from 1 March 1900, 13 days behind. All dates that predate the Russian calendar reform must record both NS and OS values.

**Jubilee Edition** — *Полное собрание сочинений* (Complete Collected Works), 90 volumes, 1928–1964. The canonical scholarly edition for all Russian-language texts.

**Yasnaya Polyana** — Tolstoy's primary estate and the location where most of his major works were written, in Tula Oblast, Russia (54.0667°N, 37.5167°E).

**wikilink** — An Obsidian-style `[[double-bracket link]]` connecting articles within the vault. Used throughout `website/src/wiki/`, `website/src/works/` prose, and the source texts themselves. Wikilinks are first-class — they are part of the knowledge graph, not decoration.

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
- When sources conflict, record **all** values and note the conflict in the relevant `notes` field. The authority order above determines which value is used as canonical, but the competing claims must always be preserved — never silently discard a source's value.

---

## Project structure

```
/Volumes/Graugear/Tolstoy/
├── CLAUDE.md                    ← this file
├── MANIFEST.md                  ← public project statement
├── README.md                    ← GitHub repo overview
├── LICENSE                      ← Soli Deo Gloria public-domain dedication
├── .git/                        ← version control (GitHub: tolstoylife/tolstoy.life)
├── .gitignore                   ← excludes subfolders, binaries, _generated
├── .gitmodules                  ← tracks tools/ as a git submodule
├── _generated/                  ← internal outputs from Claude (tasks, analyses, notes)
├── _resources/                  ← untracked workspace: scratchpad, downloaded texts, research clippings
├── _design/                     ← presentation assets, infographics (untracked)
├── _docs/                       ← project docs, research notes, source guides (untracked)
├── primary-sources/             ← immutable source files, organised by provenance (not genre)
├── projects/                    ← active production projects with own version control
│   ├── bethink-yourselves/      ← epub scanning + production project (Swedish + English)
│   ├── birukoff-biography/      ← re-OCR and epub production of 1906 Heinemann edition
│   └── korrektur/               ← OCR/proofreading workspace
├── website/                     ← PWA, e-reader, vault (GitHub: tolstoylife/website)
│   ├── src/                     ← Obsidian vault root + Eleventy input
│   │   ├── .obsidian/           ← Obsidian config
│   │   ├── _config/             ← Eleventy config modules
│   │   ├── _data/               ← global Eleventy data
│   │   ├── _includes/           ← layouts and partials
│   │   ├── _layouts/            ← page templates
│   │   ├── assets/              ← CSS, JS
│   │   │   ├── css/global/      ← CUBE CSS + Every Layout
│   │   │   └── scripts/         ← vanilla JS modules
│   │   ├── common/              ← feeds, sitemap, PWA manifest
│   │   ├── pages/               ← static pages (about, legal, accessibility)
│   │   ├── posts/               ← blog / news posts
│   │   ├── sources/             ← source cards + index + log
│   │   ├── _staging/            ← unverified clippings (not in git)
│   │   ├── wiki/                ← wiki articles (people, places, events, concepts)
│   │   └── works/               ← work folders: [Title].md + sidecar + text/
│   ├── schema/                  ← schema and convention docs
│   │   ├── tolstoy-works-schema.md
│   │   └── wiki-schema.md
│   ├── eleventy.config.js
│   └── CLAUDE.md                ← (deprecated; use parent CLAUDE.md)
├── splash/                      ← temporary splash site (pre-launch)
├── tools/                       ← ebook build toolset (GitHub: tolstoylife/tools)
│   ├── se/                      ← Standard Ebooks fork
│   ├── setup.py                 ← installs as `tl` command
│   └── CLAUDE.md                ← (deprecated; use parent CLAUDE.md)
└── __backup/                    ← archived material (retired corpus/, prior CLAUDE.md, etc.)
```

---

## Website: PWA, e-reader, and vault

The `website/` folder contains the public-facing progressive web app (PWA), the e-reader interface, and the Obsidian vault that serves as the single source of truth for all content.

### What it does

Four core sections:

1. **Wiki** — Obsidian markdown articles with wikilinks covering people, events, places, and concepts. Note: wiki articles cover entities — *not* works. There is no separate wiki article for *Anna Karenina*; the work's own overview file is the canonical article for it.
2. **Works** — complete bibliography. Each work has an overview page (frontmatter + prose) inside a named folder, with an optional sidecar `.data.yaml` for deep scholarly metadata. Long-form works also have a `text/` subfolder containing one file per chapter.
3. **My Library** — users add editions to a personal library cached on-device for offline reading (`IndexedDB`, no backend).
4. **E-reader** — focus-mode reading view with togglable wikilinks, footnotes, and a chapter Table of Contents.

Plus **posts** (blog/news) and **pages** (about, legal, accessibility).

### Stack

**Eleventy (11ty) · Obsidian · Vanilla HTML/CSS/JS**  
**Domain:** tolstoy.life  
**Deployed on:** Netlify (builds from committed `.md` files — no database, no network calls at build time)

### Vault and file structure

The Obsidian vault (`website/src/`) is unified — `wiki/` articles, `works/` overview pages, and source texts all live in the same graph and share the same wikilink namespace.

**There is no separate wiki article for a work.** The work's own file (`website/src/works/fiction/novels/anna-karenina/Anna Karenina.md`) is the canonical article for that work. Wiki articles in `website/src/wiki/` cover people, places, events, and concepts — not works.

**Work folder structure:**

```
website/src/works/fiction/novels/anna-karenina/
├── Anna Karenina.md             ← overview article (frontmatter + prose)
├── anna-karenina.data.yaml      ← sidecar: deep scholarly metadata
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

The text landing file for a work is named `[Title] — Text.md` (em-dash, not hyphen) to avoid wikilink collision with the overview file. Chapter files use title-case part and chapter names: `Part 1, Chapter 1.md`.

### .md file structure

Work overview files (`website/src/works/.../Anna Karenina.md`) have frontmatter and prose:

```md
---
id: anna-karenina
recordStatus: draft
titleEn: Anna Karenina
titleRu: Анна Каренина
genre: novel
language: ru
completionStatus: complete
# ...core schema fields...
---

Factual prose about composition, publication history, reception, etc.
All claims cite a verified primary source. [[wikilinks]] to people, places, events.
```

The `---` delimiters separate frontmatter from prose. No zone markers needed — the boundary is the closing `---`.

Source text files (`website/src/works/.../text/Part 1, Chapter 1.md`) have a TEXT zone:

```md
---
title: Part 1, Chapter 1
work: anna-karenina
part: 1
chapter: 1
---

<!-- TEXT — source text, do not modify -->

The full text of the chapter with [[wikilinks]] woven in.
```

Wiki article files (`website/src/wiki/Sophia Tolstaya.md`) follow the templates in `website/schema/wiki-schema.md`.

**Rules:**

- Frontmatter is authored by Claude based on primary sources. During R&D, Claude writes directly. In production, changes come via PR.
- The TEXT zone in source text files is never touched by wiki maintenance operations.
- All prose must cite primary sources. No unattributed claims, no literary interpretation.

### Eleventy ignores

`website/src/sources/` and `website/src/_staging/` are excluded from Eleventy via `.eleventyignore` — the index, log, source cards, and staging materials must never generate pages. If adding other vault-only folders in future, add them to `.eleventyignore` as well.

### Obsidian vault

`website/src/` is the Obsidian vault. Open `website/src/` directly in Obsidian. Wikilinks, backlinks, and graph view work against all `.md` files in `wiki/`, `works/`, and `sources/`.

### Build pipeline

`npm run build` works purely from committed `.md` files — no scripts, no external dependencies, no network calls.

**Commands** (run from `website/`):

```bash
npm start            # Eleventy dev server (alias for dev:11ty)
npm run build        # Clean + production build
npm run test:a11y    # Pa11y accessibility checks against a test build
```

**Local development workflow:**

```bash
# 1. Claude session: ingest sources, update vault files
# 2. Review changes in Obsidian (graph view, backlinks, content)
# 3. cd website/
# 4. git add src/wiki/ src/works/ src/sources/
# 5. git commit
# 6. npm run build / push to deploy
```

### E-reader design notes

Works are rendered from Markdown in the e-reader, preserving Obsidian-style `[[wikilinks]]`. The UI renders these as interactive links with a toggleable mode: readers can turn wikilinks on or off, and when on, tapping or hovering a wikilink opens a modal preview sourced from the corresponding `website/src/wiki/` article or work file — similar to Wikipedia's link previews. Wiki summary content should be bundled at build time (not fetched on demand) to support offline PWA use.

### CSS methodology

CSS is written using **CUBE CSS** layered on **Every Layout** primitives with **lean web** principles.

**Tailwind is used as a design token compiler only** — not as a utility-class framework. `tailwind.config.js` defines the design system (colour palette, type scale, spacing). The Tailwind build step compiles these tokens into CSS custom properties. **Tailwind utility classes must not appear in HTML templates.**

Layer order:

1. **Base** — resets, element defaults
2. **Compositions** — Every Layout primitives (Stack, Center, Cluster, Sidebar, Grid, etc.)
3. **Blocks** — scoped component styles (`.work-card`, `.timeline-entry`, `.reader-view`)
4. **Utilities** — single-purpose helpers (`.sr-only`, `.text-center`)

Rules:

- Use CSS custom properties for all design tokens. Never hardcode values.
- Reach for an Every Layout primitive before writing custom layout CSS.
- Prefer the CSS class approach (`.stack`) over web components (`<stack-l>`) unless progressive enhancement is needed.
- Media queries are a last resort — use intrinsic layout first.

### JavaScript conventions

- **Vanilla JS only** — no frameworks, no build-step JS transforms unless strictly necessary.
- Prefer platform APIs: `fetch`, `IntersectionObserver`, `ResizeObserver`, `dialog`, `details/summary`.
- Use `<script type="module">` for all JS.
- Keep scripts small and purpose-specific — no large monolithic bundles.
- Progressive enhancement: the page must be useful without JS.
- PWA features (service worker, caching, install prompt) live in `website/src/common/serviceworker.njk` and related files.

### Sensible defaults

- When creating new content files, use the templates in `website/schema/wiki-schema.md` or `website/schema/tolstoy-works-schema.md` as the starting point.
- When in doubt about a schema field, check the relevant schema before inventing structure.
- Prefer static generation over dynamic rendering — Eleventy pages should be pre-rendered wherever possible.
- Images in WebP/AVIF with `width`/`height` attributes and `loading="lazy"`.
- All interactive elements must be keyboard-accessible.

### Git remotes

- `origin` → `https://github.com/tolstoylife/website.git`
- `upstream` → `https://github.com/madrilene/eleventy-excellent.git` (Eleventy Excellent theme — pull updates from here)

---

## Tools: ebook build toolset

The `tools/` folder contains the tolstoy.life ebook toolset — a Python command-line toolkit adapted from the Standard Ebooks toolset.

### What it is

This is a fork of the [Standard Ebooks toolset](https://github.com/standardebooks/tools), adapted for tolstoy.life. It is a Python command-line toolkit (invoked via the `tl` command) that handles the full lifecycle of producing a production-quality EPUB ebook from a marked-up source directory.

The CLI is called `tl` (not `se`) so it can coexist with an upstream Standard Ebooks installation. Under the hood, the Python package is still `se/` — only the console entry point differs.

It is **not** a general-purpose ebook converter. It is an opinionated editorial pipeline that enforces consistent typography, accessibility, metadata, and structural standards across every ebook produced under the tolstoy.life imprint.

### What it produces

Finished `.epub` files suitable for:

- Distribution via tolstoy.life
- Sideloading onto e-readers (Kindle, Kobo, Apple Books, etc.)
- In-browser reading via the tolstoy.life PWA e-reader

### The source directory format

Every ebook lives in a source directory with a fixed structure:

```
my-ebook/
├── images/
│   ├── cover.jpg         ← cover artwork
│   ├── cover.svg         ← cover SVG (generated)
│   └── titlepage.svg     ← titlepage SVG (generated)
└── src/
    └── epub/
        ├── content.opf   ← EPUB metadata (publisher, title, author, etc.)
        ├── css/
        ├── images/
        └── text/
            ├── colophon.xhtml
            ├── imprint.xhtml
            ├── uncopyright.xhtml
            └── *.xhtml   ← chapter files
```

This structure is created by `tl create-draft` and then populated with the source text.

### Key commands

| Command | What it does |
|---|---|
| `tl create-draft` | Scaffold a new ebook source directory from templates |
| `tl build` | Compile a source directory into a distributable `.epub` |
| `tl build-images` | Generate cover and titlepage SVGs from templates |
| `tl lint` | Check the source directory for style and structural errors |
| `tl typogrify` | Apply typography rules (smart quotes, em-dashes, etc.) |
| `tl semanticate` | Auto-add EPUB semantic markup to XHTML files |
| `tl build-toc` | Generate the table of contents |
| `tl build-manifest` | Generate the OPF manifest |
| `tl recompose-epub` | Collapse an EPUB into a single HTML file (for the PWA reader) |
| `tl prepare-release` | Final pre-release checks and metadata updates |
| `tl import-text` | Import a local .txt, .md, .html, or .epub into chapter files |
| `tl ia-import` | Download from Internet Archive, scaffold, and import in one step |
| `tl export-wiki` | Export ebook text + metadata as wiki-ready Obsidian Markdown |

Run `tl help` for the full list, or `tl <command> --help` for per-command options.

### Metadata sourcing

Ebook metadata (title, author, dates, genre, source transcription) originates in the vault and flows through production via the `content.opf` file. When producing an ebook, populate `content.opf` metadata from the canonical YAML in `website/src/works/` — do not invent or hand-estimate metadata values. Cross-reference against the works schema (`website/schema/tolstoy-works-schema.md`).

### Cover artwork

Cover images should be sourced from public domain artworks. Preferred sources are paintings and portraits already catalogued in the vault or available in `_resources/`.

### Ebook URL slugs

The `SE_SLUG` placeholder in the colophon and OPF templates must match the `id` field from the canonical works schema (e.g., `anna-karenina`, `war-and-peace`). These slugs are the primary keys shared across all projects.

### Branding and copy

This fork replaces Standard Ebooks branding with tolstoy.life throughout. Key things to know:

- **Publisher name:** `tolstoy.life` (lowercase, with dot)
- **Publisher URL:** `https://tolstoy.life/`
- **CLI command:** `tl` (not `se` — avoids collision with upstream Standard Ebooks)
- **Logo:** `se/data/templates/logo.svg` — a simple text wordmark (placeholder; update when final brand assets are ready)
- **SE vocabulary namespace** (`se: https://standardebooks.org/vocab/1.0`) is retained intentionally — it is a technical EPUB standard, not visible branding

### Installation

Requires Python >= 3.10.12.

```shell
# Install with pipx (recommended)
pipx install .

# Or for development
python3 -m venv venv
source venv/bin/activate
pip install -e . --break-system-packages
```

After installation, verify with `tl --version`. If you also have the upstream Standard Ebooks toolset installed, both `se` and `tl` will be available side by side.

### Upstream sync

This repository tracks upstream changes from `standardebooks/tools`. When pulling upstream updates:

1. Review any changes to files in `se/data/templates/` — these are the primary rebranded files and upstream changes may overwrite tolstoy.life copy
2. The files most likely to conflict are: `colophon.xhtml`, `imprint.xhtml`, `uncopyright.xhtml`, `logo.svg`, `cover.svg`, `titlepage.svg`, `content.opf`, `setup.py`
3. Lint rules and Python logic in `se_epub_lint.py` and `se_epub_build.py` can generally be taken from upstream without conflict
4. The `setup.py` entry point (`tl`) must be preserved — upstream uses `se`

---

## Contribution model

The primary contribution channel for general readers is **GitHub Issues**. Issue templates should cover three cases: factual corrections (claim, source, suggested fix), prose suggestions, and missing works or sources.

For contributors comfortable with git, pull requests remain welcome:

**Wiki content PRs** (maintainer validation required before merge): any PR touching wiki article prose or work metadata must cite the specific primary source for every claim. A maintainer reviews the diff against that source before merging.

**Text wikilink PRs** (open — no factual review required): anyone may fork and PR additions or corrections to `[[wikilinks]]` within source text files in `text/` subfolders. Wikilink targets must resolve to existing files in the vault.

---

## Implementation plan

### Phase 1 — Wiki schema and conventions

Define `wiki-schema.md` with page types (person, place, event, concept), frontmatter templates, and the index/log conventions. Establish the sidecar pattern for works metadata.

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

---

## GitHub repositories

The Tolstoy Research Platform spans four repositories under the `tolstoylife` organization:

- **tolstoy.life** (`https://github.com/tolstoylife/tolstoy.life`) — parent repo (this one). Tracks root-level files, metadata, and _generated/ outputs. Excludes subprojects and binaries via .gitignore.
- **website** (`https://github.com/tolstoylife/website`) — the PWA, e-reader, and vault. Registered as a git submodule in the parent repo.
- **tools** (`https://github.com/tolstoylife/tools`) — the ebook build toolset. Registered as a git submodule in the parent repo.
- **splash** (`https://github.com/tolstoylife/splash`) — temporary splash site (pre-launch placeholder).

The parent repo tracks subprojects as submodules so they remain independent while maintaining loose coupling at the organizational level.
