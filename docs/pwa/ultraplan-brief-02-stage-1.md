---
title: "Ultraplan brief: Stage 1 — offline works"
description: "A detailed prompt to feed to /ultraplan for implementing the first local-first capability: user-initiated offline caching of works in the Tolstoy e-reader."
date: 2026-04-20
status: draft
tags: [ultraplan, pwa, offline, service-worker, tolstoy-life]
---

# Ultraplan brief: Stage 1 — offline works

This is the prompt to feed to `/ultraplan` for implementing Stage 1 of the local-first PWA roadmap: user-initiated offline caching of individual works. This is the first functional upgrade to the existing PWA and lays the foundation for everything that follows.

## Context for this brief

Stage 1 adds a "make available offline" capability to each work on tolstoy.life. The existing PWA already has a service worker that caches the shell and static assets; this stage extends caching to the works themselves (XHTML chapters, images, CSS specific to each work) plus the wiki articles each work references, and gives the user explicit control over what gets stored.

This is not about caching everything aggressively. It's about giving the user a deliberate choice: "I want this specific work available offline," followed by a visible representation of storage usage. When a user downloads a work, they also get the wiki articles referenced from any of its chapters, automatically deduplicated against any wiki content already cached from earlier downloads.

**Read these documents before running this brief:**
- `./local-first-architecture.md` (the four data layers, Workbox §5.8, decision log)
- `./stage-1-implementation.md` (the resolved Stage 1 design — this brief is the planning prompt, that file is the design source)
- `./wiki-integration.md` (the shared wiki cache and bundled previews)
- `./tl-pipeline-integration.md` (the asset manifest, `relatedWiki`, wiki-previews bundle, works.json that Stage 1 depends on)

## The brief

```
/ultraplan Implement Stage 1 of the Tolstoy e-reader's local-first
architecture: user-initiated offline caching of individual works. The site
is at tolstoy.life, built with Eleventy, following CUBE CSS methodology,
Every Layout primitives, and lean-web principles (HTML and CSS first,
JavaScript only where genuinely needed). An existing service worker already
caches the app shell and static assets. This plan extends caching to cover
full works on user request.

User-facing behaviour:

1. On each work's page, a "Make available offline" button appears near the
   title with a size estimate that includes the work plus any of its
   referenced wiki articles not already cached. When the user taps it, the
   download coordinator fetches all XHTML chapters, images, work-specific
   assets, and the work's `relatedWiki` articles. Progress is shown
   (e.g., "Downloading 12 of 47 chapters · 8 wiki articles to go").

2. After download, the button becomes "Available offline" with a small
   indicator. A secondary action lets the user remove the offline copy.

3. A settings page lists all downloaded works with their storage footprint
   and a one-tap removal option for each. A single line below the work
   list shows the shared wiki cache (article count, total bytes — not
   broken down per work because the cache is shared and deduplicated). An
   aggregate "Total storage used" figure is shown, alongside the browser's
   quota if available via the Storage API. An advanced section in settings
   has a separate "Download the entire wiki" toggle for users who want
   the full wiki offline independent of any work download.

4. When the user is offline and navigates to a work they have downloaded,
   the reading experience is indistinguishable from online. Navigation
   between chapters works. Images load. The table of contents works.
   Wikilink modal previews show the bundled summary instantly for any
   wiki article in the previews bundle, and full content for articles in
   the shared wiki cache.

5. When the user is offline and navigates to a work they have not
   downloaded, a clear, friendly message appears explaining what's
   available and offering to download a related work they do have. Not an
   error modal — a real page.

Core requirements:

- Adopt Workbox (workbox-routing, workbox-strategies, workbox-precaching)
  for the routing and caching-strategy layer. Hand-roll only the
  project-specific bits — principally, the matcher that checks whether a
  request targets an asset of a downloaded work via IndexedDB lookup. See
  local-first-architecture.md §5.8 and stage-1-implementation.md §6 for
  rationale and the routing-rules table.

- Use the Cache API for storing fetched resources. One named cache per
  work-version (e.g., `tolstoy-work-v1:war-and-peace:v2026-03-01-a3f5c8`).
  One shared wiki cache (`tolstoy-wiki-v<bundle-version>`) holding wiki
  articles referenced by any downloaded work, deduplicated. This makes it
  trivial to evict a single work's cache without affecting others, while
  the shared wiki cache reflects the union of references.

- Versions are content-addressed by the build pipeline (date + 6-char
  content hash). When a new version of a work is published, old caches
  are preserved until the user explicitly updates. This protects users
  who downloaded an edition they want to keep. The served-version
  retention is current + 2 prior; older versions remain in git only.

- The wiki-previews bundle (`/wiki-previews-v<YYYY-MM-DD>-<hash6>.json`) is precached
  with the app shell — its URL is discovered from `/works.json` on first
  load. This is what makes wikilink modal previews work offline from
  first visit, even before any work is downloaded.

- Request persistent storage via navigator.storage.persist() *after* the
  user's first successful download. Explain to the user that this protects
  their downloaded books from being evicted under storage pressure.

- Show accurate storage information via navigator.storage.estimate() when
  available. Gracefully handle browsers that don't support it.

- Do not cache anything automatically beyond the existing shell and the
  wiki-previews bundle. The user must explicitly choose to store works
  offline. This respects their device and is philosophically consistent
  with the project's values. (The wiki-previews bundle is small — single
  hashed JSON file, comparable in size to the app shell — and is treated
  as part of the shell.)

- The service worker's routing table (Workbox `registerRoute`) covers
  these patterns at minimum:
  * Shell assets (CSS, JS, fonts): StaleWhileRevalidate (Workbox precache)
  * `/works.json`: StaleWhileRevalidate, 5-minute max-age
  * `/wiki-previews-v*.json`: CacheFirst, immutable (hashed URL)
  * Asset of a downloaded work: CacheFirst against the work's named cache
    (matcher does an IndexedDB lookup against the downloadedWorks store)
  * Asset of a non-downloaded work: NetworkOnly with the offline-fallback
    page
  * Wiki article in the shared wiki cache: CacheFirst against
    `tolstoy-wiki-v*`
  * Other site pages (essays, posts, work overview pages): NetworkFirst
    with cache fallback

Specific design questions the plan should answer:

- IndexedDB schema for the downloadedWorks object store (which the
  service-worker matcher reads on every request). Keyed by work URI,
  storing {version, cacheName, title, downloadedAt, totalBytes, status}.
  Indexes needed for the settings-page list view.

- Download coordinator: the client module that orchestrates the work
  fetch (chapters + assets + relatedWiki). How does it stream progress
  back to the UI (postMessage from the page-driven fetch, not from the
  service worker)? Concurrency limit (6 parallel fetches per coordinator)?
  Cancellation semantics (abort, delete partial cache, remove IndexedDB
  record — no resume in Stage 1)?

- Wiki deduplication logic: when downloading a work, for each slug in the
  work's `relatedWiki`, check the shared wiki cache; fetch only slugs not
  already present. Size estimate shown in UI must reflect only the new
  articles, not the total `relatedWiki` size.

- Wiki cache lifecycle on work removal: recommended default is automatic
  pruning (a wiki article with zero referencing downloaded works is
  removed on the next storage check), with an explicit "Keep all
  downloaded wiki articles" override in settings.

- Wikilink modal preview resolution order: (1) full article in shared
  wiki cache → show full content; (2) summary in wiki-previews bundle →
  show summary with "read more" link; (3) nothing → graceful fallback
  (link works as a regular link; offline users see a friendly message).

- How to gracefully handle the case where the user's browser evicts a
  cache without warning (persistent storage was denied or revoked)?
  Service-worker fetch handler detects cache-miss for a work marked
  "ready" in downloadedWorks → mark status as "damaged" → UI offers
  re-download.

- How to present the "this work is not available offline" message in a
  way that's helpful rather than blocking? Link to downloaded works?
  Offer to download this one if they're actually online?

- What's the upgrade path when a work gets a new version? Passive banner
  on the work's page, not an automatic upgrade. The user chooses when to
  migrate to the new version; existing annotations anchored to the old
  version continue to work because the old cache and the old versioned
  URL both still exist.

- Wiki-previews bundle rotation: when the bundle gets a new hash (new
  wiki article added), the app shell is updated and the new bundle is
  precached. The old bundle stays in the build output for one cycle so
  existing service workers can still fetch their precached URL during the
  swap. Define the exact Workbox precache behaviour for this case.

Constraints:

- Follow the lean-web principle: no JavaScript unless it's load-bearing.
  The "Make available offline" button's UI can be progressive — a basic
  version works without JS; richer progress UI enhances when JS is
  available.

- Follow CUBE CSS and Every Layout. Any new UI (download button, progress
  bar, settings panel, wikilink modal preview) must be built with existing
  primitives and utility tokens where possible. Don't introduce new CSS
  architecture.

- The existing service worker must be upgraded, not replaced. Existing
  cached assets should survive the upgrade if possible, or be invalidated
  cleanly if not. Migration from today's hand-rolled service worker to a
  Workbox-based one is part of the plan, not an afterthought.

- Bundle budget for the service worker layer (including Workbox):
  30 KB gzipped. That accommodates Workbox's routing, strategies, and
  precaching modules plus the project-specific matcher code.

- Do not break the existing site for users on browsers with limited or
  no Cache API support. The download feature can be unavailable in those
  browsers, but reading online must continue to work. Wikilink modal
  previews should work on every modern browser without BarcodeDetector
  or any unusual API.

- Depends on three pipeline outputs produced by
  tl-pipeline-integration.md: the per-work asset manifest with
  `relatedWiki`, the hashed wiki-previews bundle, and the works.json index
  with `wikiPreviewsUrl`. If any of these isn't ready, Stage 1 has graceful
  fallbacks (see stage-1-implementation.md §12), but the clean path
  assumes all three.

Deliverables the plan should produce:

1. Service worker architecture: the Workbox routing registrations, the
   downloaded-work matcher (async IndexedDB lookup), the shared wiki cache
   strategy, the message-passing protocol between the page and the worker
   for download progress.

2. Cache naming convention: exact format for work caches
   (`tolstoy-work-v1:<slug>:<version>`), the shared wiki cache
   (`tolstoy-wiki-v<bundle-version>`), and the Workbox-managed shell
   precache.

3. Download coordinator module: state machine (idle, fetching,
   verifying, writing, complete, cancelled, failed), the IndexedDB
   transactions for downloadedWorks + wikiCacheRefCount (if we track
   reference counts for auto-pruning), and the progress-event contract
   to the UI.

4. UI design: the Make-available-offline button states (idle,
   downloading, available, updating, error), the settings page layout
   including the shared-wiki-cache line and the advanced "Download the
   entire wiki" toggle, the wikilink modal preview component (summary →
   full content → fallback), the offline-unavailable page. Mermaid state
   diagrams where useful.

5. Wiki integration handling: how `relatedWiki` is fetched, deduplicated
   against the shared cache, counted for size estimates, pruned on work
   removal.

6. Storage quota handling: when to request persistence, how to surface
   quota info, how to compute the combined size of work + new wiki
   articles for the pre-download estimate, what to do when approaching
   the limit.

7. Upgrade flow: how a user with a Stage 0 PWA (current site) transitions
   smoothly to a Workbox-based Stage 1 service worker without losing
   cached shell assets and without breaking active sessions.

8. Testing strategy: how to verify offline behaviour across Chrome,
   Safari, Firefox, and mobile variants; how to simulate quota
   exhaustion; how to test the service worker update cycle; how to test
   wiki deduplication (download two works sharing articles) and preview
   fallback chains.

9. Analytics / observability: the minimum the operator needs to know
   about how offline caching is being used, without compromising privacy.
   Likely: nothing, or only aggregate success/failure counters with no
   user ID.

10. Edge cases: partial downloads, cache eviction, service worker update
    mid-download, user running out of storage during download, wiki
    article removed from the vault between a user's downloads (the
    previews bundle has a newer hash than the work's manifest references),
    the `relatedWiki` list being empty for a work that has wikilinks
    (build bug — the plan should say what the client does).

Produce a plan that's implementation-ready, with clear acceptance criteria
for each component, architecture diagrams where they help, and explicit
handling of failure modes. This is a focused, bounded scope — it should not
drift into Stage 2 (annotations) or Stage 4 (sync). Do not write code.
```

## How to use this brief

Paste the block above into `/ultraplan` from your tolstoy.life repo. Because this stage is small and focused, even the "simple" variant of `/ultraplan` should produce a useful plan. Stage 1 is the right scope for `/ultraplan` because it's bounded enough to fit in a single implementation session and important enough to be worth careful review before touching the service worker (a component where bugs have long blast radii).

After reviewing the plan in the browser, consider using "teleport back to terminal" with the "Start new session" option — implementing a service worker benefits from a clean context without architectural discussion in it.
