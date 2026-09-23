---
layer: reference
lastUpdated: 2026-06-03
tags: [architecture, eleventy, wikilinks, migration]
---

# Migration: interlinker → parse-level wikilinks + pre-computed backlinks

Replaces `@photogabble/eleventy-plugin-interlinker` (currently active at `website/eleventy.config.js:58`) with a small in-repo module that resolves `[[wikilinks]]` at **markdown-parse time** and serves backlinks from a graph built **once** — so it never re-enters Eleventy's render pipeline. This removes the scaling wall (and the silent-blank async-shortcode bug) the plugin carries.

Companion: `eleventy-interlinker-scaling-warning.md` (why this is needed).

## Why — measured

Throwaway benchmark, N synthetic notes × 10 wikilinks, Eleventy 3.1.5 / Node 22. Build time + peak resident memory:

| Notes | plain Eleventy | **parse-level (this)** | interlinker |
|------:|---------------:|-----------------------:|------------:|
| 1,000 | 0.48 s / 174 MB | **0.44 s / 176 MB** | 1.80 s / 742 MB |
| 2,000 | 0.77 s / 190 MB | **0.73 s / 202 MB** | 3.75 s / 1,246 MB |
| 4,000 | 1.49 s / 248 MB | **1.39 s / 273 MB** | 7.70 s / 2,140 MB |
| 8,000 | 3.16 s / 368 MB | **3.05 s / 403 MB** | 20.84 s / 4,181 MB |

The parse-level approach tracks **plain Eleventy** almost exactly (negligible overhead). At 8k notes it is **~7× faster and ~10× less memory** than interlinker. Extrapolated to Phase 5 (~26,500) and full scope (100k+), interlinker hits ~12–14 GB then ~40–50 GB peak RAM (OOM); the parse-level approach stays near Eleventy's own linear baseline (sub-GB, minutes), well within CI limits.

## Parity — validated against interlinker on an identical corpus

- **Inline resolution: identical.** Every `[[ ]]` resolves to the same URL (300/300 in the test). Supports `[[Target]]`, `[[Target|Label]]`, `[[Target#Heading]]`. Resolves by **page title** (matches the wiki convention where filename = title), using Eleventy's **real `.url`** — so the `/wiki/{{ id }}/` permalink scheme is honored without re-derivation.
- **Backlinks: identical except self-links.** Same `{ url, title }` shape `partials/backlinks.njk` already consumes. The only difference: interlinker lists a page as its own backlink when it links to itself; this module omits self-backlinks (more correct, and self-wikilinks don't occur in real wiki content). Trivially configurable if exact parity is wanted.
- **Dead-link report: preserved.** `deadLinkReport: 'json'` writes `.dead-links.json` (same filename), so any existing tooling keeps working.
- **Transclusion `![[ ]]`: not implemented.** Confirmed unused in content (the only `![[` in the repo is a JS template literal). If ever needed, add a block rule that inlines the target's content from the same index.

## How it works (no render re-entry)

1. **One collection callback** (`_wikilinkIndex`) runs in the collection phase — before any template renders — and builds two maps from `api.getAll()`: `byTitle` (normalized title → real URL) and `backlinks` (URL → sources). `api.getAll()` gives each page's resolved `.url` and `.data.title`; outbound `[[ ]]` are read from each page's raw source (`rawInput`, file fallback). Single O(pages) pass, no per-page re-render.
2. **A markdown-it inline rule** resolves `[[ ]]` at parse time from `byTitle` (ready by render time).
3. **A filter** (`wikiBacklinks`) serves backlinks at render time.

Contrast with interlinker, which registers a *per-page* `eleventyComputed` function that calls `page.template.read()` and depends on `collections.all` — i.e. it re-reads/re-renders every page and rescans the whole collection once per page. That is the source of both its O(N²)-ish cost and the async-shortcode drop.

## The module (already placed, inert until wired)

Files are in `website/src/_config/plugins/wikilinks/` — they do nothing until imported and registered (steps below). Full source, for review/portability:

### `wikilinks/util.js`
```js
export const normalizeTitle = (s) =>
  String(s ?? '').toLowerCase().replace(/\s+/g, ' ').trim();

export const escapeHtml = (s) =>
  String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

export const slugifyHeading = (s) =>
  String(s ?? '').toLowerCase().trim().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
```

### `wikilinks/markdown-rule.js`
```js
import { normalizeTitle, escapeHtml, slugifyHeading } from './util.js';

export function installWikilinkRule(md, index) {
  md.inline.ruler.before('link', 'wikilink', (state, silent) => {
    const { src, pos } = state;
    if (src.charCodeAt(pos) !== 0x5b /* [ */ || src.charCodeAt(pos + 1) !== 0x5b) return false;
    const close = src.indexOf(']]', pos + 2);
    if (close < 0) return false;
    const inner = src.slice(pos + 2, close);
    if (inner.includes('[') || inner.includes('\n')) return false;

    if (!silent) {
      let [targetRaw, labelRaw] = inner.split('|');
      let heading = '';
      const hash = targetRaw.indexOf('#');
      if (hash >= 0) { heading = targetRaw.slice(hash + 1); targetRaw = targetRaw.slice(0, hash); }
      const target = targetRaw.trim();
      const label = (labelRaw ?? targetRaw).trim();
      const hit = index.byTitle.get(normalizeTitle(target));

      const token = state.push('html_inline', '', 0);
      if (hit) {
        const href = heading ? `${hit.url}#${slugifyHeading(heading)}` : hit.url;
        token.content = `<a class="wikilink" href="${href}">${escapeHtml(label)}</a>`;
      } else {
        index.dead.push({ target });
        token.content = `<a class="wikilink wikilink--dead" href="#" aria-disabled="true" title="No page named &quot;${escapeHtml(target)}&quot;">${escapeHtml(label)}</a>`;
      }
    }
    state.pos = close + 2;
    return true;
  });
}
```

### `wikilinks/index.js`
```js
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { installWikilinkRule } from './markdown-rule.js';
import { normalizeTitle } from './util.js';

const WIKILINK = /\[\[([^\]\n]+)\]\]/g;

export default function wikilinks(eleventyConfig, options = {}) {
  const opts = { deadLinkReport: 'none', ...options };
  const index = { byTitle: new Map(), backlinks: new Map(), dead: [] };

  eleventyConfig.addCollection('_wikilinkIndex', (api) => {
    buildIndex(api.getAll(), index);
    return [];
  });

  eleventyConfig.amendLibrary('md', (md) => installWikilinkRule(md, index));

  eleventyConfig.addFilter('wikiBacklinks', (url) => index.backlinks.get(url) ?? []);

  if (opts.deadLinkReport === 'json') {
    eleventyConfig.on('eleventy.after', () => {
      writeFileSync(join(process.cwd(), '.dead-links.json'), JSON.stringify(index.dead, null, 2));
    });
  } else if (opts.deadLinkReport === 'console') {
    eleventyConfig.on('eleventy.after', () => {
      for (const d of index.dead) console.warn(`[wikilinks] dead link [[${d.target}]]`);
    });
  }
}

function buildIndex(pages, index) {
  index.byTitle.clear(); index.backlinks.clear(); index.dead.length = 0;

  for (const page of pages) {
    const title = page.data?.title;
    if (title && page.url) index.byTitle.set(normalizeTitle(title), { url: page.url, title });
  }
  for (const page of pages) {
    const raw = rawOf(page);
    if (!raw) continue;
    const fromUrl = page.url;
    const fromTitle = page.data?.title ?? fromUrl;
    const seen = new Set();
    let m;
    while ((m = WIKILINK.exec(raw))) {
      const target = m[1].split('|')[0].split('#')[0].trim();
      const hit = index.byTitle.get(normalizeTitle(target));
      if (!hit) { index.dead.push({ from: fromUrl, target }); continue; }
      if (hit.url === fromUrl) continue;     // no self-backlink
      if (seen.has(hit.url)) continue;       // dedupe per source page
      seen.add(hit.url);
      const list = index.backlinks.get(hit.url) ?? [];
      list.push({ url: fromUrl, title: fromTitle });
      index.backlinks.set(hit.url, list);
    }
  }
}

function rawOf(page) {
  if (typeof page.rawInput === 'string') return page.rawInput;
  try { return readFileSync(page.inputPath, 'utf8'); } catch { return ''; }
}
```

## Wiring it in — four edits (apply + test in the real build)

These touch live build files, so they're left for you to apply and verify:

1. **`src/_config/plugins.js`** — import + export the module alongside the others:
   ```js
   import wikilinks from './plugins/wikilinks/index.js';
   // ...add `wikilinks` to the default export object
   ```
2. **`eleventy.config.js:58`** — swap the plugin registration:
   ```diff
   - eleventyConfig.addPlugin(plugins.interlinker, { deadLinkReport: 'json' });
   + eleventyConfig.addPlugin(plugins.wikilinks, { deadLinkReport: 'json' });
   ```
   (`amendLibrary` composes with the `setLibrary('md', …)` on line 91 — same as
   interlinker does today, so the markdown rule attaches to the custom lib.)
3. **`src/_includes/partials/backlinks.njk`** — backlinks now come from a filter, not interlinker's computed `data.backlinks`. Add one line at the top:
   ```diff
   + {%- set backlinks = page.url | wikiBacklinks -%}
     {% if backlinks.length > 0 %}
   ```
4. **`package.json`** — drop the dependency once the swap verifies:
   ```diff
   - "@photogabble/eleventy-plugin-interlinker": "^1.1.0",
   ```
   then `npm install` to prune it.

## Verify

1. `npx @11ty/eleventy` — clean build, exit 0.
2. Spot-check a wiki page: `[[ ]]` rendered as `<a class="wikilink" href="/wiki/…/">`, and the Backlinks list present on a linked page.
3. Compare `.dead-links.json` before/after — same dead targets (the report is preserved). Style `.wikilink--dead` (e.g. muted/struck) if you want dead links visible.
4. Optional: diff backlink counts vs an interlinker build — expect identical except any self-links (which this omits by design).

## Rollback

Revert the four edits and `npm install`. The `wikilinks/` module can stay in the tree (inert) or be deleted.

## Relation to the Layer-1 Python plan

`architecture-review.html` intends wikilink/graph work to live in a Python Layer-1 generator (`generate-related-wiki.py`). This JS module is the same principle — **pre-compute the graph, don't resolve links during render** — kept inside the Eleventy build so it needs no Python at build time. If you later move the graph to Python, have it emit a `links.json` and point the markdown rule + `wikiBacklinks` filter at that file instead of building the index from collections; the rule and template wiring stay the same.
