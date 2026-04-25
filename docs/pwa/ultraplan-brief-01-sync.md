---
title: "Ultraplan brief: Yjs annotation schema and sync relay"
description: "A detailed prompt to feed to /ultraplan for designing the CRDT data model and minimal sync infrastructure for the Tolstoy e-reader's annotation layer."
date: 2026-04-20
status: draft
tags: [ultraplan, pwa, yjs, crdt, sync, tolstoy-life]
---

# Ultraplan brief: Yjs annotation schema and sync relay

This is a prompt to feed to `/ultraplan` when you're ready to design the CRDT-based annotation storage and sync infrastructure for the Tolstoy e-reader PWA. Copy everything under "The brief" below into your `/ultraplan` invocation.

## Context for this brief

This corresponds to Stage 4 of the PWA architecture document at `./local-first-architecture.md` — the opt-in sync layer. It assumes Stages 1–3 are already built: users can download works for offline reading, and annotations (bookmarks, highlights, notes, reading position) are stored locally in IndexedDB using the W3C Web Annotation Data Model.

This `/ultraplan` run should produce an implementation plan covering: the Yjs document structure, the IndexedDB persistence layer, the pairing-code flow for establishing sync between devices, the minimal sync relay (a Cloudflare Worker + Durable Object per room, `y-durableobjects` pattern), and the migration path from a non-synced Stage 3 install to a synced Stage 4 install.

**Read `./yjs-schema-and-sync.md` before running this brief.** That document carries the resolved design decisions — this brief is the planning prompt, not the design source.

## The brief

```
/ultraplan Design the CRDT-based sync layer for the Tolstoy e-reader PWA's
annotation system. The project is a local-first progressive web app at
tolstoy.life that lets readers annotate public-domain Tolstoy texts with
highlights, notes, bookmarks, and reading-position markers. Stages 1–3 are
already built: works are cached offline, annotations are stored locally in
IndexedDB following the W3C Web Annotation Data Model, and everything works
fully without an account. This plan covers adding opt-in cross-device sync.

Core requirements:

1. Annotation data model must remain W3C Web Annotation compliant. Export
   and import to/from standard JSON-LD must continue to work. The CRDT
   structure must represent these annotations without losing any W3C-defined
   fields (id, type, motivation, body, target with selectors, created,
   creator, modified).

2. Use Yjs as the CRDT library. Persist locally with y-indexeddb. Sync
   transport should use y-websocket. The Y.Doc is one-per-user with five
   top-level Y.Maps: annotations, workMeta, readingPositions, tags,
   preferences (see yjs-schema-and-sync.md §2).

3. Sync must be fully opt-in. Users who never enable sync must see no
   behavioural change. Users who enable sync on a new device must be able
   to pair with an existing device without an email, password, or account
   system. Pairing supports two equal paths: a fragment-URL QR code
   (https://tolstoy.life/pair#room=…&key=…&did=…&exp=…&sig=…) and a
   BIP-39 six-word phrase fallback. Both flows include a relay-mediated
   confirmation step before authorization completes (yjs-schema-and-sync.md
   §6).

4. The sync relay is a Cloudflare Worker + one Durable Object per room,
   following the y-durableobjects pattern with hibernatable WebSockets.
   It stores only opaque CRDT update blobs (with opt-in client-side AEAD
   encryption-at-rest), the room's authorized device-ID set, and basic
   metadata (last-update timestamp, connected-client count). It must never
   parse or interpret annotation contents. The goal is that the server
   code has no awareness of what users are reading or annotating — it is
   a dumb pipe (yjs-schema-and-sync.md §4).

5. Migration from Stage 3 to Stage 4 must be non-destructive. A user who has
   been using the app locally for months and then enables sync must have all
   their existing local annotations become the seed state of their Y.Doc,
   with no data loss.

6. Key management: the pairing flow produces a shared symmetric sync key.
   The room ID is derived from the key. Connection auth is HMAC-SHA-256 of
   a connect nonce. Encryption-at-rest of the CRDT blobs is opt-in for
   Stage 4 (AES-GCM with the sync key, per-update nonce) and is the
   recommended default once stable across browsers. Each device has a
   unique device ID issued at pairing; revocation drops the device ID
   from the Durable Object's authorized set (yjs-schema-and-sync.md §4.7).
   Key rotation is explicit and user-initiated (yjs-schema-and-sync.md §4.8).

7. Recovery: with no account system, the recovery hierarchy is
   sync-key export to file/paper-BIP-39 (default), encrypted backup to a
   user-controlled URL (opt-in), email magic link (opt-in, reluctant). The
   relay never holds recovery material (yjs-schema-and-sync.md §6.4).

8. Resilience: sync must degrade gracefully. If the relay is unreachable,
   the app continues to work locally and queues updates for later. If two
   devices annotate the same passage simultaneously while offline, the CRDT
   merge must produce a sensible result (both annotations present, not one
   overwriting the other).

The design decisions above are resolved. The plan should produce
implementation detail for them, not re-litigate them. Specific operational
questions the plan should answer:

- Snapshot cadence: when should the Durable Object compact its in-memory
  update log into a stored snapshot? (Working assumption: every ~100
  updates or 30 minutes, whichever first — confirm with reference numbers.)
- Pairing handshake message format: define the in-band WebSocket protocol
  (or out-of-band HTTP endpoints) for the relay-mediated confirmation step
  in §6.1 step 5 of yjs-schema-and-sync.md.
- Encrypted-backup snapshot format: raw Y.Doc state vs JSON-LD export of
  annotations? What does each enable for users restoring on a different
  app or with the project shut down?
- Wire-format schema versioning: the Y.Doc shape will evolve. What's the
  forward/backward compatibility plan if a future version adds a new
  top-level map or a new annotation field?
- The deletion model: tombstones from Yjs's default Y.Map deletion
  semantics — when (if ever) can they be GC'd given the multi-device
  story?
- Migration from a non-synced Stage 3 user (annotations live in a plain
  IndexedDB store) to a synced Stage 4 install: every existing annotation
  must seed the new Y.Doc atomically and idempotently, surviving partial
  failure.

Constraints:

- Work within the existing tolstoy.life codebase (Eleventy, minimal
  JavaScript, CUBE CSS, Every Layout primitives, lean-web principles).
  Do not propose frameworks like React or Vue.
- Total client-side bundle budget for the sync layer: under 100 KB
  gzipped, ideally under 50 KB. Yjs alone is ~30 KB gzipped; y-indexeddb
  and y-websocket are small. Budget must accommodate them.
- The sync relay must fit within Cloudflare Workers' free tier for expected
  traffic (dozens of users at first, room to grow to low thousands without
  infrastructure changes). Hibernatable WebSockets (no idle billing).
- No dependency on any Google, Facebook, or Apple service. No third-party
  analytics. No trackers.
- The pairing URL must be on the live origin (https://tolstoy.life/pair)
  with all sensitive parameters in the URL fragment so origin logs see
  only `/pair`. No custom URL scheme.
- BarcodeDetector is unavailable in Firefox and pre-Safari-17; the BIP-39
  fallback is a peer of the QR option, not a hidden last resort.
- Respect the project's typographic and design values: if any UI is
  introduced (pairing code display, sync status indicator, synced-devices
  list), it should be minimal and not disrupt the reading surface.

Deliverables the plan should produce:

1. Y.Doc schema: concrete structure (Y.Map vs Y.Array, key naming,
   field-level types), with a diagram showing how a few sample annotations
   map into the CRDT. (Most of this is already in yjs-schema-and-sync.md
   §2 — extend it with edge cases.)
2. IndexedDB integration: how y-indexeddb coexists with the existing
   annotations object store from Stage 3, and the atomic, idempotent
   migration step.
3. Pairing flow: UI states for both QR and BIP-39 paths, the relay-mediated
   confirmation handshake, cryptographic exchange, device-ID issuance.
4. Sync relay: Cloudflare Worker + Durable Object code structure
   (y-durableobjects pattern), hibernatable WebSocket lifecycle, snapshot
   compaction policy, rate limiting, abuse prevention.
5. Encryption-at-rest path: AES-GCM wrapper around update blobs, key
   derivation from sync key, opt-in toggle and migration path.
6. Device list and revocation: end-to-end flow from "Settings → Synced
   devices → Remove" through to the Durable Object dropping the device ID
   from the authorized set.
7. Recovery flows: sync-key export bundle format (room ID + raw key +
   BIP-39 phrase), encrypted-backup-to-user-URL upload/restore protocol,
   optional email magic-link path.
8. Key rotation: end-to-end flow from "Settings → Rotate sync key" through
   to all other devices being told to re-pair.
9. Testing strategy: how to verify CRDT convergence across multiple offline
   devices, how to test sync interruption and recovery, how to test
   pairing across browsers with and without BarcodeDetector.
10. Observability: what (minimal, privacy-respecting) telemetry the relay
    should log, and what the client should surface to the user about sync
    status.
11. Security and threat model: explicit statement of what an attacker with
    access to the relay database could learn (with and without
    encryption-at-rest), what they could not, and the attack scenarios
    each defence addresses.
12. Rollout plan: how to ship this to existing Stage 3 users without
    breaking anything.

Please produce a plan that's deep enough to implement from, with
architecture diagrams (Mermaid) where they clarify the design, and explicit
tradeoffs called out at each decision point. Do not write code — this is a
design plan, not an implementation.
```

## How to use this brief

Paste the block above into `/ultraplan` from inside your tolstoy.life git repository. Because this is architectural rather than immediate-implementation, you'll likely want to iterate on the plan in the browser review surface — leaving inline comments on specific sections, asking for revisions, and then teleporting the approved plan back to your terminal to implement piecewise.

Note: `/ultraplan` has three variants (simple, visual, deep) assigned by A/B testing. If you get the simple variant (no diagrams, short output), consider running it again — the brief above is written assuming you'll get the visual or deep variant, which produces the architecture diagrams and multi-section plans this design benefits from.
