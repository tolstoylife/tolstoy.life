---
title: "Tolstoy e-reader PWA: document index"
description: "Reading order and purpose of the PWA architecture documents. Start here."
date: 2026-04-20
status: draft
tags: [index, tolstoy-life, pwa]
---

# Tolstoy e-reader PWA: document index

Five design documents and three `/ultraplan` briefs, meant to be read together. Each design document stands alone but they're designed to form a coherent whole.

## Reading order — design documents

1. **`local-first-architecture.md`** — The overall argument. What PWAs can do, why local-first fits this project, the four data layers (works, wiki articles, app shell, user annotations), Workbox adoption, and the staged roadmap (Stages 1–5). Start here. The other documents are the detailed specifications of individual sections of this one.

2. **`wiki-integration.md`** — How the wiki layer integrates with the works layer. Defines the `relatedWiki` per-work declaration, the shared deduplicated wiki cache, the bundled wiki-previews file for offline modal previews, and the GitHub deep-link contribution surface. Read this before or alongside the Stage 1 implementation document.

3. **`stage-1-implementation.md`** — A concrete implementation plan for the first real local-first step: letting users download individual works (and their referenced wiki articles) for offline reading, all served by a Workbox-based service worker. Scoped to be shippable on its own, with no dependencies on stages that haven't been built. This is the document most directly feedable into `/ultraplan`.

4. **`tl-pipeline-integration.md`** — What the Layer-1 scripted pipeline (CLAUDE.md, scaled architecture) must produce to make Stage 1 possible: deterministic content-addressed versioning (`v<YYYY-MM-DD>-<hash6>`), per-work asset manifests with `relatedWiki`, the wiki-previews bundle, the works.json index, and the explicit `chapterUri` frontmatter convention. A prerequisite for Stage 1.

5. **`yjs-schema-and-sync.md`** — The CRDT data model and sync relay design for Stage 4 and later. Specifies the Y.Doc shape, the per-annotation schema, the Cloudflare Worker + Durable Object relay (y-durableobjects pattern), the fragment-URL QR pairing flow with BIP-39 fallback, encryption-at-rest, the device list and revocation mechanism, and key rotation. Not needed for Stage 1, but referenced from it for the overall arc.

## Companion audit

- **`../architecture/architecture-review.html`** (2026-04-23) — A standalone, second-pass audit of the five design documents above. Ten parts covering: plain-English sync-model explainer, storage topology (what lives in Cache API vs IndexedDB), install UX across platforms (with CSS-only device mockups), sync-visibility UX (what the indicator should look like, accessibility-first), volume/bandwidth risk analysis, CRDT/QR sync problems, a critical build-pipeline cascade bug, hosting strategy (Netlify vs Cloudflare Pages vs R2 vs Bunny/Hetzner), build-minute economics, and a ranked priority-fix list. Open in a browser for the formatted reading experience. Session handoff with action items lives at `handoff-2026-04-23.md`.

## Planning briefs (for `/ultraplan`)

The three briefs are derivative of the design documents — they re-state the design in a form suitable for `/ultraplan` and explicitly call out which decisions are resolved versus which are open questions for the planning session. They live in `_generated/PWA/briefs/` as staging artefacts:

- `ultraplan-brief-01-sync.md` — Stage 4: Yjs schema and sync relay.
- `ultraplan-brief-02-stage-1.md` — Stage 1: offline works (with wiki integration).
- `ultraplan-brief-03-tl-integration.md` — Pipeline contract Stage 1 depends on.

Recommended implementation order: brief 3 → brief 2 → brief 1.

## Using these for `/ultraplan`

When running `/ultraplan` to plan Stage 1 implementation, feed it the relevant design documents as context, and use the brief as the planning prompt:

- `local-first-architecture.md` (for the overall design, especially §§1–3 and §§5.6–5.8)
- `wiki-integration.md` (for the wiki integration the Stage 1 plan depends on)
- `stage-1-implementation.md` (the actual plan, with the resolved Workbox routing and shared wiki cache design)
- `tl-pipeline-integration.md` (the pipeline prerequisite — the deterministic version scheme, asset manifests, `relatedWiki`, wiki-previews bundle)

`yjs-schema-and-sync.md` can be left out of the Stage 1 plan; it's relevant only when Stage 4 comes around. Including it would widen the planning scope unnecessarily.

An updated prompt for `/ultraplan` might look like:

```
/ultraplan Implement Stage 1 of the Tolstoy e-reader local-first PWA
as specified in ./stage-1-implementation.md, with the
wiki integration in ./wiki-integration.md and the
build-pipeline contract in ./tl-pipeline-integration.md.
The architectural context is in ./local-first-architecture.md.

Focus on:

1. The four Layer-1 generators
   (generate-wiki-previews.py, generate-related-wiki.py,
   generate-asset-manifests.py, generate-works-index.py) and the
   shared canonical-JSON serialiser they use.
2. The Workbox-based service worker — routing rules, the
   downloaded-work matcher, the shared wiki cache strategy. Bundle
   budget 30 KB gzipped.
3. The download coordinator with wiki deduplication, progress
   reporting, and cancellation.
4. The wikilink modal preview component using the bundled previews
   and falling through to the shared wiki cache.
5. The settings storage panel including the shared wiki cache line
   and the advanced "Download the entire wiki" toggle.

Propose alternatives for the open questions in section 14 of
stage-1-implementation.md and section 13 of
tl-pipeline-integration.md. Include risk analysis for the
iOS Safari storage eviction case.
```

The specific call-outs in the prompt (open questions, the iOS case) matter. Without them, `/ultraplan` might assume those are settled; with them, it knows to treat them as design decisions to work through.

## Document status

All five design documents are drafts. They've been written to be internally consistent — a change in one would ripple to the others and should be made deliberately. Before committing to a plan via `/ultraplan`, a full read-through to catch drift is worthwhile.

The three briefs are kept in sync with the design documents; if a design document changes, the corresponding brief should be re-checked.

## Values alignment check

A concluding principle: every decision in these documents should pass the check, "does this honour the reader?"

- Offline availability honours the reader's device and connection.
- Local-first storage honours the reader's ownership.
- Standards-based annotations honour the reader's freedom to move their data.
- No accounts required honours the reader's privacy.
- The sync relay as a dumb pipe honours the reader's data sovereignty.
- Deliberate download choices honour the reader's device as a resource.
- The wiki travelling with the work it annotates honours the reader's offline experience as a complete one.
- The works themselves as public domain honour the reader's right to read freely.

If a design decision doesn't pass this check, it's the wrong decision, and the architecture should be revised. The goal isn't to build a great e-reader in general. It's to build one that a reader of Tolstoy would recognise as made in the right spirit.
