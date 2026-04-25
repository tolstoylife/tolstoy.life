---
title: "Ultraplan brief: tl pipeline integration with PWA versioning"
description: "A detailed prompt to feed to /ultraplan for aligning the tl ebook build pipeline with the PWA's content-addressed versioning scheme."
date: 2026-04-20
status: draft
tags: [ultraplan, pwa, tl, ebook-pipeline, versioning, tolstoy-life]
---

# Ultraplan brief: tl pipeline integration with PWA versioning

This is the prompt to feed to `/ultraplan` for integrating the existing `tl` ebook build pipeline with the PWA's content-addressed versioning scheme. This is the glue that lets Stages 1–4 function correctly when works evolve over time.

## Context for this brief

The tolstoy.life project uses a modified Standard Ebooks toolset (the `tl` CLI, documented in the `ebook-creator` skill) to produce publication-quality EPUB ebooks from source XHTML. Separately, the project's website is a static Eleventy build that consumes the same source vault. The PWA needs every work to carry a stable, content-addressed version identifier that the service worker can use for cache keying and that annotations can use as anchoring targets.

This is an integration problem, not a greenfield one. The `tl` pipeline already exists and works. The Eleventy build already exists and works. The PWA architecture requires certain metadata to be present in the post-Eleventy build output. This plan determines how to bridge them with the least friction.

**Read these documents before running this brief:**
- `./local-first-architecture.md` (the four data layers and their version contract)
- `./tl-pipeline-integration.md` (the resolved design — this brief is the planning prompt, that file is the source of truth for the manifest schema, version scheme, `relatedWiki`, wiki-previews bundle, and works.json)
- `./wiki-integration.md` (why the wiki-previews bundle and `relatedWiki` exist and how the PWA consumes them)
- `CLAUDE.md` (the scaled architecture model; the new pipeline scripts live in the Layer-1 family alongside `extract-graph.py` and `extract-frontmatter.py`)

## The brief

```
/ultraplan Design the integration between the existing tl ebook production
pipeline (a modified Standard Ebooks toolset, documented at
/mnt/skills/user/ebook-creator/SKILL.md and /mnt/skills/user/manual/SKILL.md)
and the tolstoy.life PWA's content-addressed versioning scheme. The goal
is to ensure every work published to the site carries a stable, verifiable
version identifier that the service worker can use for cache keying and
that annotations can use as stable anchoring targets across content
updates.

Background:

The tl pipeline produces XHTML chapter files and content.opf metadata
following a strict manual of style. Works are published from a monorepo
where each work is a directory with source text, metadata, and build
artefacts. The pipeline includes typogrification, semanticisation, EPUB
building, and linting.

The PWA architecture requires (and the resolved design in
tl-pipeline-integration.md spells out):

1. Each published version of a work has a deterministic identifier of the
   form `v<YYYY-MM-DD>-<hash6>`. The date is the first-commit date for
   this content; the hash is a 6-char SHA-256 prefix over the canonically
   sorted set of post-Eleventy artefact hashes for the work.

2. URIs that reference specific versions look like
   `urn:tolstoy-life:war-and-peace:book-1-chapter-3#v2026-03-01-a3f5c8`.
   Chapter URIs are declared explicitly in chapter frontmatter — never
   derived from URL or position.

3. When a work gets a new version, the old version remains addressable
   for at least the served-retention window (current + 2 prior versions
   on the live site; older only via git). Annotations anchored to an
   older version use TextQuoteSelector + TextPositionSelector fallback to
   re-anchor.

4. Per-work asset manifests at `/<work>/<version>/manifest.json` (and an
   unversioned alias at `/<work>/manifest.json` pointing to current) tell
   the PWA exactly what to fetch for offline availability. Each manifest
   includes the work's `relatedWiki` list (deduplicated wiki article slugs
   referenced by any chapter).

5. A site-wide `works.json` lists every work with its current version,
   prior served versions, manifest URL, and a top-level pointer to the
   current wiki-previews bundle URL.

6. A wiki-previews bundle (`wiki-previews-v<YYYY-MM-DD>-<hash6>.json`)
   ships with the app shell, containing summary stubs for every wiki
   article in the vault. Hashed URL means the file is immutable per build.

The resolved scope of `tl`'s involvement: **none of the above is added
to `tl`.** All five new artefacts are produced by Layer-1 scripted pipeline
generators in Python that run *after* Eleventy renders the site. The `tl`
toolset stays focused on EPUB production. `tl export-wiki` continues to
emit plain markdown only — wikilink infusion is a separate downstream
LLM + LightRAG pass, not part of `tl`.

Specific design questions the plan should answer:

- Concrete pseudocode for each Layer-1 generator:
  `generate-wiki-previews.py`, `generate-related-wiki.py`,
  `generate-asset-manifests.py`, `generate-works-index.py`. The shape is
  in tl-pipeline-integration.md §6.2 — refine into runnable specs.

- The canonical-JSON serialiser used across all four generators (sort
  keys, fixed encoding, integer bytes, no floats). Same module, used
  consistently, so determinism is testable.

- The wikilink resolver in `generate-related-wiki.py`. It must match
  Eleventy's resolution rules exactly (Obsidian-compatible name lookup,
  including aliases). The resolver should share a code path with the
  rendering layer rather than re-implementing.

- The CI determinism test: build twice from the same git revision; every
  artefact must be byte-identical. Where does this run? How does it report
  failure?

- Netlify build environment: confirm Python availability and concurrency
  characteristics. Should the generators run as a Netlify build plugin or
  as a build-script step shelled out from Eleventy's `before` event?

- The `Cache-Control` headers Netlify must emit for `works.json`,
  per-work `manifest.json`, the immutable hashed `wiki-previews-v*.json`,
  and the immutable hashed work-version subtrees. Any `netlify.toml`
  overrides needed?

- Retroactive versioning for works already on the site at the moment
  this rolls out. They get `v<rollout-date>-<hash6>` on first build — the
  first-commit date logic should fall back to the rollout date when no
  prior content history exists in the manifest.

- Multi-translation handling: separate work URIs (e.g.,
  `urn:tolstoy-life:war-and-peace-maude` vs
  `urn:tolstoy-life:war-and-peace-garnett`)? What does the works.json
  shape look like with multiple translations as siblings?

- Content-change scope: a typo fix in one chapter changes the work's
  content hash (because one of the chapter file hashes is now different),
  so the whole work gets a new version. Confirm this is the intended
  semantics and document it.

- Wiki-previews bundle rotation policy: when the bundle hash changes
  (new wiki article added, old summary edited), how many previous
  bundles stay in the build output? Working assumption: one previous, so
  service workers mid-swap can still resolve their precached URL — but
  is that enough?

Constraints:

- The existing `tl` pipeline is not modified. All new artefacts come from
  Layer-1 Python scripts that run after Eleventy, not from `tl`
  subcommands. The `tl` toolset stays focused on EPUB production.

- The existing manual of style must not be modified. The ebook-creator
  and manual skills are authoritative for EPUB production.

- Chapter frontmatter gains exactly one new required field: `chapterUri`.
  The build fails loudly if any chapter is missing it. This is a
  vault-content change, not a `tl` change.

- Version identifiers must be deterministic and stable across rebuilds.
  Running the whole pipeline twice on unchanged sources must produce
  byte-identical manifests, previews, and works-index.

- The system must be explainable to a reader. A user who asks "what
  version of War and Peace am I reading?" deserves a clear answer. The
  `v<date>-<hash6>` format is designed to be displayable; the hash prefix
  is short enough to be glance-readable.

- Canonical URLs stay stable: `/war-and-peace/book-1/chapter-3/` always
  points at the current version. Versioned URLs
  (`/war-and-peace/v2026-03-01-a3f5c8/book-1/chapter-3/`) exist in parallel
  for readers who want to link to a specific historical version.

- The manifest carries schema version markers (`manifestFormat: v1`,
  `indexFormat: v1`) so the schema itself can evolve without ambiguity.

- Git-based workflow must be preserved. The `generate-asset-manifests.py`
  script reads git for the first-commit date used in version strings.
  Clients never require git access.

Deliverables the plan should produce:

1. Layer-1 generator specs: runnable Python specifications for
   `generate-wiki-previews.py`, `generate-related-wiki.py`,
   `generate-asset-manifests.py`, `generate-works-index.py`, including
   the canonical-JSON serialiser they share, the wikilink resolver, and
   the first-commit-date helper.

2. Manifest and index schemas: formal schemas (JSON Schema or equivalent)
   for the per-work manifest and the top-level `works.json`, with
   examples for a small work, a large work, a work with multiple served
   prior versions, and a multi-translation case.

3. Build integration: where the generators slot into the Netlify build
   (Eleventy plugin hook vs shelled-out script), the dependency order,
   the fail-fast behaviour if a step errors.

4. URL structure and Netlify headers: canonical URLs, versioned URLs,
   hashed immutable URLs, the `netlify.toml` Cache-Control overrides and
   any rewrite rules.

5. Service worker contract: the exact shape of what the service worker
   expects to find at `/works.json`, `/<work>/manifest.json`, and
   `/wiki-previews-v*.json`, cross-referenced with
   stage-1-implementation.md §6.

6. Annotation anchoring: concrete example of how an annotation created
   on `v2026-03-01-a3f5c8` re-anchors when the user later opens
   `v2026-06-15-d4e9f1` of the same work — both TextPositionSelector
   (exact byte offsets, fragile) and TextQuoteSelector (short prefix +
   exact + short suffix, robust) are compared with the new version's
   rendered text; the TextQuoteSelector wins when the position drifts.

7. Retroactive versioning: the plan for assigning version identifiers
   to works already on the site, including the fallback logic when no
   prior git history is available.

8. Determinism test: the CI step that builds twice and compares byte-for-
   byte, what it asserts, what it reports on failure.

9. Migration plan for the pipeline itself: a staged rollout that doesn't
   break existing workflows, with rollback points.

10. Testing: how to verify that version hashes are stable, manifests are
    correct, the service worker can follow manifests, `relatedWiki` is
    complete (no wikilink goes unreferenced), the wiki-previews bundle
    contains every article referenced, and annotation re-anchoring works
    across real version transitions.

Produce a plan that treats this as an integration problem between three
existing systems (tl pipeline, Eleventy build, service worker). Be
explicit about the contract between each layer. Diagrams showing data
flow from source text to published manifest to client cache would help.
Do not write code. Do not redesign the tl pipeline beyond what's
necessary for this integration.
```

## How to use this brief

This is the most complex of the three briefs because it touches three existing systems (tl, Eleventy, service worker) and has to respect the manual of style. Consider running it with the "deep" variant of `/ultraplan` if you can, or explicitly prompting for multi-agent exploration by adding "Use multi-agent exploration — spawn parallel agents to explore the tl pipeline, the Eleventy build, and the service worker architecture before synthesising." to the end of the brief.

Because this brief references the skills at `/mnt/skills/user/ebook-creator/SKILL.md` and `/mnt/skills/user/manual/SKILL.md`, make sure those skills are accessible in the cloud environment. If they aren't, consider copying the relevant sections into the repo as documentation before running `/ultraplan`, or including the key constraints directly in the brief.

Of the three briefs, this is the one most likely to benefit from multiple iteration rounds in the browser review surface — the design space is large and the constraints come from multiple directions. Plan to spend time on inline comments.

## Sequencing the three briefs

Three briefs have been produced:

1. `ultraplan-brief-01-sync.md` — the Yjs schema and sync relay (Stage 4).
2. `ultraplan-brief-02-stage-1.md` — offline works (Stage 1).
3. `ultraplan-brief-03-tl-integration.md` — this brief (the build-pipeline contract Stage 1 depends on).

**Implementation order: brief 3 → brief 2 → brief 1.**

Brief 3 must complete first: it defines the pipeline outputs (asset manifest, `relatedWiki`, wiki-previews bundle, works.json) that Stage 1 consumes. Stage 1 has graceful fallbacks if some pipeline outputs aren't ready (stage-1-implementation.md §12), but the clean path needs all of them.

Brief 2 follows immediately: Stage 1 is the foundation that gives the service worker its real job and exercises the pipeline contract end-to-end.

Brief 1 is the long-term goal — Stage 4, the sync layer, building on Stages 1–3. Don't run it last for ordering reasons; run it last because the prior stages may surface insights that change the sync layer's requirements.

If running them in parallel for exploration, that's also fine — they address somewhat independent concerns and the plans will reconcile naturally when implementation begins.
