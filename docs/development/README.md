---
title: Development — tolstoy.life
lastUpdated: 2026-05-11
changelog:
  - 2026-05-11 — initial scaffold. Created folder with README and first feature recipe (source-mode-implementation.md).
layer: reference
tags: [development]
---

# Development — tolstoy.life

How the site is built. Implementation guides, conventions, and feature recipes for the frontend and backend of the Eleventy site under `website/`.

This folder complements the others:

- `docs/architecture/` describes *how the system is shaped* — operations, performance, workflows. System-level concerns that span subprojects.
- `docs/design/` describes *what the site looks like* — design tokens, colour research, splash plans. Visual design.
- `docs/editorial/` describes *what the site says and how* — voice, sourcing rules, the source-mode specification.
- `docs/development/` (this folder) describes *how to build it* — Eleventy configuration, markdown pipeline, CSS architecture, JS conventions, and per-feature implementation recipes.

---

## What lives here

**Feature recipes.** One file per feature that has a non-trivial implementation. Each recipe references the editorial or design spec it implements, lists what already exists in the codebase, names the files to add or modify, and flags decisions left for implementation time. Recipes are written so a future session (or a contributor) can implement without re-litigating any settled question.

Current recipes: none in this folder. The first recipe (`source-mode-implementation.md` — per-fact footnotes + toggle, implementing the spec in [`docs/editorial/source-mode.md`](../editorial/source-mode.md)) was ported into the eleventy notes collection during the 2026-05-11 docs → dev-blog migration. New blog-style recipes go to `website/src/posts/notes/`; only structural docs (this README, forthcoming `frontend.md` / `backend.md` conventions) stay here.

**Convention docs (not yet written).** A `frontend.md` and a `backend.md` will land here once enough features have shipped to document real patterns rather than guesses. Until then, the upstream sources are the authoritative reference:

- **Eleventy Excellent** ([lenesaile.com](https://www.lenesaile.com/)) — the starter the site is built on. Lene's choices are deliberate; read before changing.
- **CUBE CSS** ([cube.fyi](https://cube.fyi/)) — the CSS methodology.
- **Every Layout** ([every-layout.dev](https://every-layout.dev/)) — the layout primitives.
- **Lean Web** — the JavaScript principle: HTML and CSS first; JS only when no native primitive does the job.

---

## Working in this part of the project

The Eleventy site lives at `website/`. Useful commands from that directory:

```bash
npm start          # dev server at http://localhost:8080
npm run build      # production build to dist/
npm run colors     # regenerate CSS custom properties from design tokens
npm run test:a11y  # pa11y accessibility tests
```

Before changing CSS, JS, layouts, or markdown plugins, check whether the pattern is already handled by Eleventy Excellent. Lene's setup is intentionally complete — when something looks unusual, it is usually deliberate. Recipes in this folder always name what already exists before describing what to add.

---

## Public docs

Files here are public. The project is openly developed; documenting the build in the open is consistent with the spirit of the project. Internal session planning lives in `_generated/` and `_resources/`, not here.
