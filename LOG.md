# Tolstoy Research Platform — Work log

Append-only, dated, short. Project-level decisions and context — "what happened, and why." Not "what code changed" (git already does that).

For content-level operations (source ingestions, wiki queries, lint passes), see `website/src/sources/log.md`.

---

## 2026-04-22

- Adopted the shared project template (`/Users/johanedlund/Projects/PROJECT-TEMPLATE.md`). Added LOG.md at the root and moved TODO.md from `_generated/project/TODO.md` to the project root. README.md and CLAUDE.md were already there.

## 2026-04-23

- Completed PWA architecture review (TODO priority 5). Produced `_generated/PWA/architecture-review.html` — a single-column serif reading artefact in ten parts: sync-model explainer, storage topology, install-UX (with CSS-only device mockups), sync-visibility UX, volume/bandwidth risk analysis, CRDT/QR sync problems, a build-pipeline cascade bug, hosting strategy, build-minute economics, and a ranked priority-fix list. Synthesised from five parallel research investigations run during the session.
- Committed to the **Cloudflare consolidation arc**: CF Pages as parallel deploy target now (primary later via DNS flip), CF Workers + Durable Objects for the Stage 4 sync relay (Paid tier required, $5/mo floor — the "free tier" claim in `yjs-schema-and-sync.md` §7 is aspirational), CF Registrar for the domain at next renewal (~$22/yr saved vs Netlify's retail $50), R2 for LightRAG + sync-relay backups. Netlify kept as passive standby; legacy free plan confirmed grandfathered at 100 GB/month indefinitely ("no action required" per Netlify's own docs).
- Identified a critical pipeline issue: the `wikiPreviewsUrl` field embedded in every per-work manifest means any wiki edit re-versions every work, collapsing the 3-version retention discipline. Must fix before Stage 1 ships. Plus `git_first_commit_date_for_dir` broken on Netlify's shallow clones; the §2.3/§8 spec conflict for annotation body shape will cause silent data loss at Stage 4. Full findings and action items in `_generated/PWA/handoff-2026-04-23.md`.
- Corrections to the earlier PWA docs where research contradicted them: BarcodeDetector is NOT in iOS Safari (BIP-39 must be primary iOS path, not fallback); Vercel is ruled out (Image Opt default-on breaks SHA-256 determinism); CF Pages has a 20,000-file / 25 MB-per-file cap that bites at Phase 5 (hence the Pages+R2 split is load-bearing, not optional).
