# CLAUDE.md — tolstoy.life

A web app and progressive web app(PWA) about the life and works of Leo Tolstoy(LT). The app should have two main functions: present a wiki using Obsidian and Obsidian markup with wikilinks with all info relating to LT (people, events, family etc). The project also aims to be a complete bibliography of all works written by LT with at least one edition to read of every work.

---

## Project overview

**Domain:** tolstoy.life
**Stack:** Eleventy (11ty) - Obsidian · Supabase (PostgreSQL) · Vanilla HTML/CSS/JS
**Purpose:** Encyclopedic reference as a wiki covering Tolstoy's biography, works, manuscripts, transcriptions, and related identifiers.

---

## Commands
```bash
# Development
npm start          # or: npx @11ty/eleventy --serve

# Build
npm run build      # or: npx @11ty/eleventy

# Preview production build
npm run preview
```

---

## Project architecture
```
tolstoy.life/
├── src/
│   ├── _data/           # Global Eleventy data files (JS, JSON, or YAML)
│   ├── _includes/       # Reusable Nunjucks/Liquid layouts and partials
│   ├── assets/
│   │   ├── css/
│   │   │   └── global/
│   │   │       ├── compositions/   # Every Layout primitives
│   │   │       ├── blocks/         # CUBE CSS blocks (scoped components)
│   │   │       ├── utilities/      # Single-purpose utility classes
│   │   │       └── global.css      # Global styles and custom properties
│   │   ├── js/                     # Vanilla JS modules
│   │   └── images/
│   ├── works/           # Content for individual works (YAML/Markdown)
│   └── index.njk        # Homepage
├── .eleventy.js         # Eleventy config
├── tolstoy-works-schema.md   # Canonical schema reference
└── CLAUDE.md
```

> The folder structure above is the intended target; adjust if the actual layout differs.


---

## Data schema conventions

All work metadata follows the schema defined in `tolstoy-works-schema.md`.

**Naming convention:**
- YAML frontmatter → **camelCase** (e.g., `titleEn`, `dateFirstPublished`)
- Supabase/PostgreSQL columns → **snake_case** (e.g., `title_en`, `date_first_published`)

**Key rules:**
- `id` is the canonical slug (e.g., `anna-karenina`) and must be unique across all works.
- Dates are ISO 8601 strings (`YYYY-MM-DD`). If the exact date is uncertain, set the companion `*Approximate: true` boolean.
- `language` is ISO 639-1 (e.g., `ru`, `fr`).
- Controlled vocabulary fields (`genre`, `completionStatus`, `firstPublishedVenueType`) must use only the values listed in the schema — never introduce free-form values without updating the schema.
- `transcriberId` must reference the controlled transcriber list in the schema. Use `other` and populate `transcriberName` when the transcriber is unlisted.
- Empty optional fields should use `""` (string) or `[]` (array) rather than `null` or being omitted entirely.
- When adding identifiers, prefer Wikidata QIDs as the primary external anchor.

---

## CSS methodology

CSS is written using **CUBE CSS** layered on **Every Layout** primitives with **lean web** principles.

### Layer order
1. **Global** — custom properties, resets, base element styles
2. **Compositions** — layout primitives from Every Layout (Stack, Center, Cluster, Sidebar, Grid, etc.)
3. **Blocks** — scoped component styles (e.g., `.work-card`, `.timeline-entry`)
4. **Utilities** — single-purpose helpers (e.g., `.sr-only`, `.text-center`)

### Rules
- Use CSS custom properties for all design tokens (colour, spacing, type scale). Never hardcode values.
- Reach for an Every Layout primitive before writing any custom layout CSS.
- Prefer the CSS class approach (`.stack`) over web components (`<stack-l>`) unless progressive enhancement of the layout is needed.
- No CSS frameworks (Tailwind, Bootstrap, etc.).
- Media queries are a last resort — use intrinsic layout (Every Layout) first.

---

## JavaScript conventions

- **Vanilla JS only** — no frameworks, no build-step JS transforms unless strictly necessary.
- Prefer platform APIs: `fetch`, `IntersectionObserver`, `ResizeObserver`, `dialog`, `details/summary`.
- Use `<script type="module">` for all JS.
- Keep scripts small and purpose-specific; avoid large monolithic bundles.
- Progressive enhancement: the page must be useful without JS.

---

## Supabase / database

- Database is PostgreSQL hosted on Supabase.
- All table and column names are **snake_case**.
- Array fields (e.g., `gutenberg`, `oclc`) are stored as PostgreSQL arrays or JSONB — confirm actual column type before writing queries.
- Row-level security (RLS) is assumed to be enabled; do not disable it.
- When writing SQL, use `snake_case` and prefer CTEs over subqueries for readability.

---

## Content and accuracy

- All historical claims (dates, locations, archival references) must be sourced. Flag uncertain information with an `approximate` boolean or a `notes` field — never silently guess.
- Russian text should be in Cyrillic script. Romanisation follows the Library of Congress transliteration system unless the source uses a different convention.
- Work titles must appear in both `titleEn` (English) and `titleRu` (Cyrillic).

---

## Sensible defaults

- When creating new content files, use the blank template at the bottom of `tolstoy-works-schema.md` as the starting point.
- When in doubt about a schema field, check `tolstoy-works-schema.md` before inventing structure.
- Prefer static generation over dynamic rendering — Eleventy pages should be pre-rendered wherever possible.
- Images should be served in modern formats (WebP, AVIF) with appropriate `width`/`height` attributes and `loading="lazy"`.
- All interactive elements must be keyboard-accessible.
