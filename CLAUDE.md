# CLAUDE.md — tolstoy.life

A progressive web app (PWA) and e-reader about the life and works of Leo Tolstoy (LT).

The app has these main functions:

1. A **wiki** using Obsidian markdown with wikilinks covering all information relating to LT — people, events, places, context.
2. A **works** section as a complete bibliography of LT. Each work has its own folder and is a git repo that anyone can fork and suggest changes to. An overview markdown file lists all facts about the work and available editions. At least one English translation of each work should be added; each edition is converted to Obsidian markdown file(s). For novels and long-form text, a separate markdown file per chapter is preferred.
3. **My library** — users can add editions to a personal library that the PWA caches on-device for offline reading.
4. An **e-reader** view. Clicking an edition adds it to the library in the background and opens a focus-mode reading view. The reader supports toggling wikilinks, footnotes, and other preferences. A Table of Contents lets users navigate chapters.

In addition to these core sections, the site has **posts** (blog/news) and **pages** (about, legal, etc.).

---

## Project overview

**Domain:** tolstoy.life
**Stack:** Eleventy (11ty) · Obsidian · Supabase (PostgreSQL) · Vanilla HTML/CSS/JS
**Purpose:** PWA e-reader and encyclopedic wiki covering Tolstoy's biography, works, manuscripts, transcriptions, and related scholarly identifiers.

---

## Data architecture

**Supabase is the single source of truth for all structured metadata.** A `generate-md.js` script (run via `npm run db:pull`) fetches rows from Supabase and writes YAML frontmatter into `.md` files in `src/`. Prose content is authored separately in Obsidian and preserved across regeneration cycles.

### .md file zones

Every generated file has two zones:

```md
---
# GENERATED — do not edit above this line
id: anna-karenina
titleEn: Anna Karenina
# ...all schema fields...
---

<!-- PROSE — edit freely in Obsidian -->

Prose body with [[wikilinks]] here.
```

The generation script replaces only the frontmatter block. The prose body is never touched.

**Rule:** Never hand-edit YAML frontmatter in `src/wiki/` or `src/works/` files. Edit metadata in Supabase, then run `npm run db:pull`.

### Obsidian vault

`src/` is the Obsidian vault. Obsidian opens the `src/` directory directly. Wikilinks, backlinks, and graph view work against the generated `.md` files in `src/wiki/` and `src/works/`.

---

## Commands

```bash
# Development
npm start                # Eleventy dev server

# Build
npm run build            # Clean + production build

# Database → markdown sync
npm run db:pull          # Fetch from Supabase, regenerate .md frontmatter
npm run db:pull:dry      # Preview what would change without writing files
```

---

## Project architecture

```
tolstoy.life/
├── src/                          # Obsidian vault root + Eleventy input
│   ├── .obsidian/                # Obsidian config (do not edit manually)
│   ├── _config/                  # Eleventy config modules
│   │   ├── collections.js
│   │   ├── filters/
│   │   ├── plugins/
│   │   └── events/               # Build-time tasks (CSS, JS bundling, OG images)
│   ├── _data/                    # Global Eleventy data files
│   ├── _includes/                # Nunjucks layouts and partials
│   ├── _layouts/                 # Page layout templates
│   ├── assets/
│   │   ├── css/
│   │   │   └── global/
│   │   │       ├── base/         # Resets and element defaults
│   │   │       ├── compositions/ # Every Layout primitives
│   │   │       ├── blocks/       # CUBE CSS blocks (scoped components)
│   │   │       ├── utilities/    # Single-purpose helpers
│   │   │       └── global.css    # Custom properties + layer imports
│   │   └── scripts/              # Vanilla JS modules
│   ├── common/                   # System files: feeds, sitemap, robots, PWA manifest
│   ├── pages/                    # Static pages (about, legal, accessibility, etc.)
│   ├── posts/                    # Blog / news posts
│   ├── wiki/                     # Wiki articles (people, events, places)
│   │   └── Leo Tolstoy.md        # Generated frontmatter + Obsidian prose
│   └── works/                    # Work overview pages (generated frontmatter + prose)
│       └── Anna Karenina.md
├── works/                        # Rich YAML schema source files (input to db:pull)
│   └── the-kingdom-of-god-is-within-you.yaml
├── scripts/                      # Build scripts (planned: generate-md.js)
├── eleventy.config.js            # Eleventy config entry point
├── tolstoy-works-schema.md       # Canonical schema reference (v5)
├── sources.yaml                  # Controlled sources library
└── CLAUDE.md
```

---

## Build pipeline

`db:pull` and `npm run build` are intentionally separate and must stay that way.

**Why:** `npm run build` must work purely from the committed `.md` files in git — no network calls, no Supabase dependency. This keeps Netlify builds fast, deterministic, and independent of the database.

**Local development workflow:**
```bash
# 1. Edit metadata in Supabase dashboard
# 2. Regenerate .md frontmatter locally
npm run db:pull

# 3. Commit the updated .md files
git add src/works/ src/wiki/
git commit -m "chore: sync metadata from Supabase"

# 4. Deploy — Netlify builds from the committed .md files, no DB needed
npm run build
```

**Do not** add `db:pull` to the Netlify build command. If you ever need Netlify to pull from Supabase on deploy, add it explicitly in `netlify.toml` as a separate decision — do not bake it into `npm run build`.

---

## Contribution model

The project uses a two-phase architecture:

**Phase 1 — DB-driven (current):** Supabase is authoritative for structured metadata. `db:pull` generates `.md` frontmatter. Prose is authored in Obsidian. Contributors edit metadata in Supabase; prose via git.

**Phase 2 — File-driven (future, when the project goes public):** The `.md` files in git become authoritative for everything — frontmatter and prose. Supabase is no longer needed for the build. Anyone can fork the repo and open a pull request to fix a date, add a source, correct a title, or improve the prose.

The transition is deliberate and simple: stop running `db:pull` and start treating the `.md` files as the canonical source. The two-zone file structure (`GENERATED` / `PROSE`) is already in place for this.

A future `db:push` script (`.md` files → Supabase) can be added to enable bidirectional sync during Phase 1 if direct edits to `.md` frontmatter are needed before the cutover.

---

## Data schema conventions

All work metadata follows the schema defined in `tolstoy-works-schema.md`.

**Naming convention:**

- YAML frontmatter → **camelCase** (e.g., `titleEn`, `dateFirstPublished`)
- Supabase/PostgreSQL columns → **snake_case** (e.g., `title_en`, `date_first_published`)

**Key rules:**

- `id` is the canonical slug (e.g., `anna-karenina`) — unique across all works.
- Dates are ISO 8601 strings (`YYYY-MM-DD`). Uncertain dates use a companion `*Approximate: true` boolean.
- `language` is ISO 639-1 (e.g., `ru`, `fr`).
- Controlled vocabulary fields (`genre`, `completionStatus`, `firstPublishedVenueType`) must use only values listed in the schema — never introduce free-form values without updating the schema first.
- `transcriberId` must reference the controlled transcriber list in the schema. Use `other` and populate `transcriberName` for unlisted transcribers.
- Empty optional fields use `""` (string) or `[]` (array) — never `null` or omitted.
- Prefer Wikidata QIDs as the primary external identifier anchor.

---

## CSS methodology

CSS is written using **CUBE CSS** layered on **Every Layout** primitives with **lean web** principles.

Layer order:

1. **Base** — resets, element defaults
2. **Compositions** — Every Layout primitives (Stack, Center, Cluster, Sidebar, Grid, etc.)
3. **Blocks** — scoped component styles (e.g., `.work-card`, `.timeline-entry`, `.reader-view`)
4. **Utilities** — single-purpose helpers (e.g., `.sr-only`, `.text-center`)

Rules:

- Use CSS custom properties for all design tokens. Never hardcode values.
- Reach for an Every Layout primitive before writing custom layout CSS.
- Prefer the CSS class approach (`.stack`) over web components (`<stack-l>`) unless progressive enhancement is needed.
- No CSS frameworks (Tailwind, Bootstrap, etc.).
- Media queries are a last resort — use intrinsic layout first.

---

## JavaScript conventions

- **Vanilla JS only** — no frameworks, no build-step JS transforms unless strictly necessary.
- Prefer platform APIs: `fetch`, `IntersectionObserver`, `ResizeObserver`, `dialog`, `details/summary`.
- Use `<script type="module">` for all JS.
- Keep scripts small and purpose-specific — no large monolithic bundles.
- Progressive enhancement: the page must be useful without JS.
- PWA features (service worker, caching, install prompt) live in `src/common/serviceworker.njk` and related files.

---

## Supabase / database

- Database is PostgreSQL hosted on Supabase.
- All table and column names are **snake_case**.
- Array fields (e.g., `gutenberg`, `oclc`) are stored as PostgreSQL arrays or JSONB — confirm column type before writing queries.
- Row-level security (RLS) is assumed to be enabled; do not disable it.
- When writing SQL, prefer CTEs over subqueries for readability.

---

## Content and accuracy

- All historical claims (dates, locations, archival references) must be sourced. Flag uncertain information with an `approximate` boolean or a `notes` field — never silently guess.
- Russian text in Cyrillic script. Romanisation follows Library of Congress transliteration unless the source uses a different convention.
- Work titles must appear in both `titleEn` (English) and `titleRu` (Cyrillic).

---

## Sensible defaults

- When creating new content files, use the blank template in `tolstoy-works-schema.md` as the starting point.
- When in doubt about a schema field, check `tolstoy-works-schema.md` before inventing structure.
- Prefer static generation over dynamic rendering — Eleventy pages should be pre-rendered wherever possible.
- Images in WebP/AVIF with `width`/`height` attributes and `loading="lazy"`.
- All interactive elements must be keyboard-accessible.
