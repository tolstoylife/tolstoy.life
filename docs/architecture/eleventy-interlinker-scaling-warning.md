---
layer: reference
lastUpdated: 2026-06-03
tags: [architecture, eleventy, performance, wikilinks]
---

# Eleventy interlinker — scaling & async-shortcode warning

> **Source:** found while debugging a sibling Eleventy-Excellent site (JEDEE / johanedlund.se)
> on 2026-06-03, then benchmarked. Shared here because the same plugin is wired into
> Tolstoy's `website/` build. Companion reading: `internal-operations.md` (capacity),
> `architecture-review.html` (build-time budget).

## TL;DR for Tolstoy

`@photogabble/eleventy-plugin-interlinker` is **currently active** in the website build (`website/eleventy.config.js:58` → `addPlugin(plugins.interlinker, { deadLinkReport: 'json' })`, v1.1.2). At today's **~81 markdown files it's completely fine.** But the plugin resolves wikilinks by **re-entering Eleventy's render pipeline once per page** — a per-page `eleventyComputed` function that calls `page.template.read()` and depends on `collections.all`. That design does not survive the planned vault size. **It must be replaced with a pre-compute step before Phase 3/5, or the build will run out of memory and die.**

This also matches the architecture's own stated plan: `architecture-review.html` lists `generate-related-wiki.py` (a **Python Layer-1 generator** that "parses every chapter for wikilinks") as the intended mechanism. The website has simply drifted from that plan — the render-time plugin sneaked in. The recommendation below realigns the two.

## Why it doesn't scale — measured

Throwaway benchmark: N synthetic notes, 10 wikilinks each, Eleventy 3.1.5 / interlinker 1.1.2 / Node 22. Interlinker **OFF vs ON**, build time + peak resident memory:

| Notes | Wikilinks | OFF time | ON time | OFF peak RAM | ON peak RAM |
|------:|----------:|---------:|--------:|-------------:|------------:|
| 100   | 1,000     | 0.26 s   | 0.39 s  | 170 MB       | 217 MB |
| 250   | 2,500     | 0.27 s   | 0.63 s  | 168 MB       | 313 MB |
| 500   | 5,000     | 0.34 s   | 1.04 s  | 172 MB       | 435 MB |
| 1,000 | 10,000    | 0.48 s   | 1.80 s  | 174 MB       | 742 MB |
| 2,000 | 20,000    | 0.77 s   | 3.75 s  | 190 MB       | 1,246 MB |
| 4,000 | 40,000    | 1.49 s   | 7.70 s  | 248 MB       | 2,140 MB |
| 8,000 | 80,000    | 3.16 s   | 20.84 s | 368 MB       | **4,181 MB** |

- **Memory is the binding constraint.** Baseline Eleventy stays flat (~370 MB at 8k files); interlinker's overhead roughly doubles every time the corpus doubles — **4.2 GB at 8k files.**
- **Time** is linear until ~4k files, then turns super-linear (the `collections.all`-per-page term, ≈O(N²), takes over).
- The **OFF** column is a fair proxy for what a parse-level / pre-compute approach costs — it never re-enters the render pipeline.

### Extrapolated to Tolstoy's targets (beyond the 8k measured ceiling)

| Scale | interlinker peak RAM | Verdict |
|---|---|---|
| Phase 3 (~8,000 files) | ~4 GB *(measured)* | already heavy |
| Phase 5 (~26,500 articles) | **~12–14 GB** | OOMs Netlify build containers; stresses the 24 GB Mac Mini |
| Full scope (100,000+ files) | **~40–50 GB** | infeasible — the build dies before finishing |

Netlify build containers are memory-capped; a multi-GB peak doesn't make the build *slow*, it makes it **fail** (OOM-killed → failed deploy). This lands well before Phase 5.

## Second, smaller risk: silent blank renders

Interlinker also **silently drops the output of an `async` shortcode** when that shortcode is reached through an `{% include %}` wrapped in an `{% if %}` / `{% for %}` block. The included template renders to **zero bytes, with no error**. On JEDEE this blanked the entire main nav (an `async` `{% svg %}` chevron inside a conditionally-included partial). If any Tolstoy template calls an async shortcode (`{% image %}`, an async `{% svg %}`, etc.) from a conditionally-included partial, watch for partials that render empty with a clean build. Mitigation: keep should-be-sync shortcodes synchronous; don't put async shortcodes inside `{% if %}`-wrapped includes.

## Recommendation

1. **Don't scale interlinker.** It's fine now; schedule its removal from the render path **before Phase 3 ingestion** (the doc projects ~8k files at Phase 3, already the painful zone). Retrofitting later means doing it under build-failure pressure.
2. **Resolve wikilinks/backlinks in a pre-build step**, exactly as `architecture-review.html` already intends with `generate-related-wiki.py`. Two clean shapes:
   - **Inline `[[ ]]` rendering** → a `markdown-it` rule (parse-time, O(content), no render pass). Reference implementations: the `eleventy-notes` starter's wikilink module (markdown-it rule + `node-html-parser` backlink scan), or a custom rule fed by the Python generator's output.
   - **Backlinks / related** → compute the graph once in Python (or a single post-render HTML scan) and write it to a data file (`*.json`) that Eleventy reads. No per-page re-render.
3. **Keep `deadLinkReport` if you like it** — the `.dead-links.json` report is a nice feature; the Python generator can emit the same artifact. The report isn't the problem; the render-reentry is.

## Reproduce

The benchmark harness is four small files (a minimal Eleventy project, a `gen.mjs N K` note generator, and a sweep runner that toggles `INTERLINKER=1` and captures peak RSS via `/usr/bin/time -l`). Ask the JEDEE side for it, or regenerate: any minimal Eleventy site + interlinker + N interlinked notes reproduces the curve.
