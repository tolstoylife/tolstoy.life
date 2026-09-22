---
layer: reference
lastUpdated: 2026-06-23
tags: [research, planning, design, website-launch]
title: "Interactive reader's editions — bundling each dive's text (design)"
---

This is the design for bundling the **text of the work** into each corpus-dive folder as an
enriched, marked-up Markdown file — so a finished dive carries not just the research index and
dossier, but a draft of the **work's overview page** and a draft of the **work itself**, ready
to become an interactive reader's edition on the site.

It is the worked-out successor to the deferred brainstorm note (`project_dive_bundled_text_brainstorm`,
2026-06-22). The pilot is **The Great Sin** (`docs/research/1905-the-great-sin/`).

---

## The split: this is spec 1 of 2

The conversation produced two clearly separable pieces. **This spec covers only the first.**

- **Spec 1 — dive-side content (this file).** What a dive produces on disk: the marked-up text
  file, the overview-page draft, the machine-translation pass, and the small `serve.py` changes
  that let us *see* the reading page in the research preview. This is the durable thing. Build it first.
- **Spec 2 — the e-reader website UI (later).** Focus mode, the docked settings rail, theming,
  table of contents, bookmarks, highlights, persistence. A website-launch build on top of spec 1's
  files. Mocked during brainstorm, not designed here.

The reason the split is safe: **one durable file, two renderers.** Everything the e-reader does is
*rendering*. Underneath sits one thing the dive produces — the marked-up text plus the dossier. Two
renderers read it: `serve.py` today (research preview) and the Eleventy e-reader later. The reader UI
can grow for years and **the content is never redone.** So what we design and produce per dive is that
one file, not the e-reader.

## The north star (context, not scope)

`tolstoy.life` becomes a **new interactive edition of Tolstoy's works**: a clean e-reader by default,
with toggleable layers summoned from a side rail — wikilinks, the passages Tolstoy or his editors or
the censor cut, edition and translation differences, modal info boxes on the entities. Spec 1 produces
the content those layers render; spec 2 builds the reader (now specified as a `serve.py` prototype: [`2026-07-03-interactive-reader-prototype-design.md`](../../superpowers/specs/2026-07-03-interactive-reader-prototype-design.md)).

## Governing principle — Tolstoy's voice, not the mainstream filter

The reading text, the overview page, and the dives all present the work **in Tolstoy's own terms** —
his voice, his version. Too many resources treat him as a specimen, filtering his words through the
mainstream society's vocabulary and values to explain what he "really meant." We don't.

The anti-example (Standard Ebooks' overview of *The Kingdom of God Is Within You*): "the most
influential work of Christian anarchism… if it didn't itself claim to merely be pointing out Christian
anarchism as the plain meaning of the gospels." It reaches for a label Tolstoy refused, *notices* he'd
refuse it, and applies it anyway. Exactly the failure to avoid.

This is already the dives' rule (`corpus-dive-ground-in-primary-not-mainstream`): lead with Tolstoy's /
Biryukov's / Chertkov's words; mainstream scholarship is contrast to read critically, never a baseline
to confirm. The guardrail that keeps it honest cuts **both** ways: present what he wrote in his terms —
neither softened by mainstream labels nor sharpened past what he actually said (`ingestion-accuracy-both-directions`).

## Where the text lives — `works/`, not `wiki/`

The site already has the destination in skeleton:

```
website/src/works/<mainCategory>/<subcategory>/<work-slug>/
        ├─ Work-Title.md     ← the record + overview page (big schema frontmatter)
        └─ text/             ← the work's enriched text (CLAUDE.md already reserves works/**/text/)
```

`wiki/` is for the **entities the text points at** — persons, concepts, places. The work itself is
never a wiki page. The dive folder is a **staging area**: we draft the overview body and the text
markdown inside `docs/research/<dive>/`, then promote both into `works/.../` at ingestion — the same
research → human-in-the-loop ingest discipline the dives already use.

**Fix needed:** CLAUDE.md currently calls `works/**/text/` "source text, do not modify." That wording
is wrong for this design — the reading text is an **enriched reader's edition**, edited on purpose
(wikilinks, cut-markers). The unaltered archive is `primary-sources/`. Reword the CLAUDE.md line to
"don't corrupt the words," not "no markup," when this lands.

## What a dive additionally produces

Three deliverables, staged in the dive folder:

1. **The enriched text — one file per version.** A work has several *versions* of the same text:
   the **Russian** (Tolstoy's original, from the corpus), the **1905 English** (the period translation
   made in his lifetime, where a public-domain one exists), and a **machine English** (fresh, neutral).
   Each version is its **own standalone file** (`<slug>.ru.md`, `<slug>.en-1905.md`, `<slug>.en-machine.md`)
   so two can sit side by side in a split-view later and the Russian is never buried under the English.
   All version files share the **same section anchors** (the work's own structure — Great Sin is intro +
   I–IX) so the columns line up. The editorial marks and wikilinks are written into each version *in its
   own language* — the Russian carries the byte-true variant from `extracts/`, the English carries a
   labelled machine rendering of it — all **derived from the one dossier**, not hand-duplicated.
   Default version the reader opens: the 1905 English where it exists, machine English otherwise, with
   Russian one click away.
2. **The overview-page draft** — the reader-facing "about this work" page, **distilled from the dive's
   `index.md`** (phase 1: mostly as-is, with the research scaffolding — coverage, needs-review,
   methodology — trimmed off). **Dense with fact, lean on opinion, in Tolstoy's terms** (see the
   governing principle). Progressive disclosure, like the e-reader: a light orientation first, the
   detail beneath. The dossier's `workRecord` supplies the schema frontmatter; this is the prose around
   it. This page **is** the work's node in the graph — see "The work's page" below.
3. **The machine-translation pass** — a one-pass English translation, labelled "machine, unverified,"
   serving as the machine-English version and as the neutral third reference for the translation
   diagnostic. Optional per work; see Machine translation below.

## The canonical edition (the spine)

Two different roles hide under "which version":

- **Spine = the canonical edition** — what the work *is*. The authoritative text the marks anchor to.
- **Default-to-open** — what *loads first* in the reader. A reading convenience (set to the 1905 English).

**The spine is the Russian PSS established text — always.** Four reasons, all pointing the same way:

1. **His voice.** The governing principle: the Russian is what Tolstoy wrote; every translation is one
   filter removed. The canonical text has to be his words.
2. **The marks are defined against it.** A cut *is* a passage absent from the PSS established text; a
   softening *is* a change to it. The Russian PSS is the ruler everything else is measured with;
   translations are projections of it.
3. **Translations are plural and each is biased** — nothing derivative can be canonical, by definition.
4. **The PSS editors already did the edition-scholarship.** Where two Russian editions differ
   (Русская мысль vs «Свободное слово»), they established the base text and recorded the other as
   variants. We defer to that — we don't re-adjudicate which Russian edition is "right."

So translations never compete for spine; they are *derived versions* measured against it. Among multiple
Russian editions, the PSS established text is the spine and the others are edition-diffs against it.
The spine's chapter structure also sets the **section anchors** every version aligns to in split-view.
This doesn't fight the English mission: English is how we *serve* the work; Russian is what it *is*.

## The encoding vocabulary

The marks are **CriticMarkup** — an existing plain-text standard for editorial change-tracking (deleted /
inserted / changed / commented text) — plus the project's existing `[[wikilink]]`. Nothing invented.
The marks map one-to-one onto the textual facts the dive already extracts into the dossier.

| Mark | CriticMarkup | Encodes | Renders as |
|---|---|---|---|
| Excision | `{--…--}` | A passage cut before print (Tolstoy, an editor, or the censor) | Ghost block at the seam |
| Insertion | `{++…++}` | A passage added in a later draft/proof | Revealed addition (the text growing) |
| Softening / edition diff | `{~~old~>new~~}` | A word/phrase changed between draft and print, **or** between two editions | Dotted printed word; reveal shows the other reading |
| Note | `{>>…<<}` | The editorial fact — who, when, why | The modal/info card |
| Wikilink | `[[Entity]]` | A person/concept/place | Toggleable link → entity modal |

Three conventions on top:

- **One mark, three stories.** A `{--cut--}` means different things depending only on who the note
  names — the **state censor**, an **editor** (e.g. Chertkov), or **Tolstoy revising himself**. The
  reader UI can color them (red = censored, amber = edited, blue = self-revised); the encoding is one
  mechanism carrying the whole textual life of the work.
- **Notes inline, for now.** The note text sits in the `{>>…<<}` comment — no second file to keep in
  sync. If drift between the text and the dossier ever bites, move notes to a dossier reference id later.
  (Lazy first; known upgrade path.)
- **Translation diagnostic = a highlight + note.** Where the period English dropped or blunted
  something versus the Russian/machine reading: `{==clause==}{>>dropped from the 1905 English<<}`. The
  machine-translation thread rides the *same* encoding as the cuts.

Worked example (real Great Sin material; English wording illustrative):

```markdown
The poverty of the masses {~~springs from~>is connected with~~}{>>Chertkov softened this,
8 Jul 1905: the evil itself springs from a deeper evil, human egoism<<} this one cause.

{--Just as the slave-owner of old re-enacted his crime each day he held men as property, so the
landowner renews this sin each day he holds the earth.--}{>>var. 8, cut at Chertkov's suggestion<<}

the single tax that [[Henry George]] proposed.
```

## The `serve.py` render pass

`serve.py` uses Python-Markdown, so the rendering is mostly off-the-shelf extensions, not custom parsing:

- **CriticMarkup** → `pymdownx.critic` (from `pymdown-extensions`). Renders the four marks to
  `<ins>` / `<del>` / `<mark>` with classes we can style and toggle. Confirm the package is available;
  if not, a ~30-line inline pattern covers the four marks.
- **Footnotes** → the built-in `footnotes` extension. This closes the long-standing "serve.py renders
  no `[^n]`" gap. Keep `{>>…<<}` for *editorial/variant* notes; use real footnotes for the work's own
  authorial/translator footnotes (e.g. the ones in "A Great Iniquity").
- **Wikilinks** `[[ ]]` → the built-in `wikilinks` extension (or a small inline pattern) pointed at the
  `works/`/`wiki/` URL scheme. Dangling links (entity page not yet created) are fine — they mark future
  ingestion work, same as the vault tolerates today.

Plus a **minimal focus-mode reading template** and CSS so the layers are visible and toggleable in the
preview. This is preview-grade only — the real rail, theming, and bookmarks are spec 2.

**Default reading state is bare.** The marks live in the file, but the default view shows *none* of
them — clean focus mode, pleasing typography, the text alone. Wikilinks, footnotes, cut-reveals, and
the version switcher are all **opt-in**, summoned by the reader. For spec 1 this is free: default CSS
hides the marks; a toggle reveals them.

## Machine translation

- **Rides the dive.** When a work's text is bundled, generate its machine pass then. Never a
  corpus-wide batch — that's huge and pointless; do the works you're already touching.
- **Cheap per work.** A ~14k-word essay is ~35k tokens in + ~18k out — one context window. Roughly
  $2 at Opus / $0.40 at Sonnet via the API, or ~$0 marginal via the subscription `claude-cli` path
  (the graphify spike already proved a session can wrap `claude-cli`).
- **Two quality tiers.** One pass, labelled "machine, unverified," for the comparison column (cheap).
  Reserve the late-voice two-pass draft-then-audit only for passages promoted to finished translation.
- **Differently biased, not unbiased.** The machine reading has no stake in Chertkov's cuts, Free Age
  Press house-softening, or Victorian propriety — which is exactly what makes a period translator's
  softening *visible*. That is its job in the edition switcher.

## Fidelity and guardrails

- `primary-sources/**` and the dive's `extracts/**` (byte-faithful originals) are **untouched**. The
  enriched text is openly a reader's edition, derived from them.
- `verify_quotes.py` still guards every locked quote against the extracts — the existing gate is unchanged.
- The Russian version is the corpus text, not a re-typing; the English versions are the period
  translation and the labelled machine pass.

## How it's built and run

- **A separate post-dive step, not a change to the `corpus-dive` skill.** The dive skill is heavily
  validated; leave its internals alone. A companion step (a small skill or a `--bundle-text` mode) reads
  a *finished* dive folder — dossier + extracts — fetches the public-domain period English (Wikisource /
  Gutenberg / archive.org) where it exists, generates the machine pass, and writes the enriched text +
  overview draft. This also lets us run it **retroactively on the ~14 dives already shipped.**
- **Pilot: The Great Sin.** Its period English ("A Great Iniquity," trans. Tchertkoff & Mayo, *The Times*
  1905) is public-domain and identified on Wikisource; its cut/variant data is the richest in the corpus.

## The work's page (and wiki scope)

**One page, not two.** The overview page **is** the work's node in the graph — there is no separate
`wiki/` stub for the work. `[[The Great Sin]]` resolves to the overview page; backlinks collect there.

```
[[The Great Sin]] ──► works/non-fiction/.../The Great Sin.md   (type: work — the node itself)
                                  │  its text links out ▼
                                  └─► wiki/Henry George.md       (type: person — an entity)
```

`wiki/` stays for the entities a text points *at* — people, concepts, places. A **work** is a
first-class node too, but it lives in `works/` because it carries the schema record *and* the reading
experience (versions, library, progress) an entity never has. Give the overview a `type: work` so the
graph can tell a work-node from a person-node (the Tolstoy-Lab already found it wants that 13th type) —
but type is a label, not a second home. A separate `wiki/the-great-sin.md` would just be two pages
fighting over which is "the work," and they'd drift.

The reader edition **embeds** `[[wikilinks]]` (toggleable) and the dive **proposes** the `works/` record
(as it already does). It does **not** create the wiki *entity* pages — those stay the separate
human-in-the-loop ingestion step. Embedded wikilinks may point at not-yet-created entity pages; that's
expected and marks future work.

## Out of scope (spec 2 or beyond)

- The full e-reader UI: focus mode polish, the docked rail, theming, TOC, **bookmarks, highlights,
  personal annotations, persistence**. (Drawn in the rail from day one, built last.)
- **"My Library", reading progress (1% opened → 100% read), PWA offline caching, reader comments, and
  the per-work update/commit log.** All website-app features — the overview page is *designed to host*
  them, but they're built in spec 2.
- Corpus-wide machine translation as a batch job.
- The reader's *own* highlights/bookmarks baked into source files — that's browser state, not text.
- Editorial "this is important" highlighting — fights the bare-voice rule.
- Changes to `corpus-dive` internals beyond adding the companion step.

## Settled in this brainstorm

- **Spine (canonical edition)** = the Russian PSS established text — always; translations are derived versions.
- **Default version** = the 1905 English where it exists, machine English otherwise, Russian one click away.
- **Default reading state** = bare focus mode; all enrichments opt-in.
- **Overview** = distilled from `index.md` (phase 1: mostly as-is), dense fact / lean opinion, in Tolstoy's terms.
- **One file per version**, shared section anchors; cuts shown in every version, in its own language, all derived from the dossier.
- **One page per work** — the overview page is the graph node (`type: work`), homed in `works/`; no separate wiki stub.
- **Tolstoy's voice** is the governing principle for text, overview, and dives alike.

## Left for the implementation plan

- **Companion step shape** — a small standalone skill vs. a `--bundle-text` mode on a finished dive.
- **`pymdownx.critic` availability** — confirm the package is installed; else the ~30-line inline pattern.
- **Period-English sourcing/cleanup** — fetching and cleaning the PD translation (footnotes, section
  numbering) is real per-work work; budget for it.
- **Section-anchor scheme** — the exact mechanism that keeps version files aligned for split-view.
