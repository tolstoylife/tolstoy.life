---
title: Source mode — per-fact footnotes
lastUpdated: 2026-05-11
changelog:
  - 2026-05-11 — initial draft. Defines the markup, the licence-tag rule, the toggle behaviour, and the relationship to `fieldSources` frontmatter.
layer: reference
tags: [editorial]
---

# Source mode — per-fact footnotes

How wiki and works pages cite their sources. Two requirements meet in one mechanism: editorial verifiability (every claim traceable) and copyright transparency (every CC BY-SA fact visibly attributed).

The companion to this document is `website/schema/wiki-schema.md`, which defines `fieldSources` for structured frontmatter fields. This file defines the prose-side mechanism.

---

## Markup

Standard markdown footnotes, inline in the prose, with a References section auto-collected at the end of the file by markdown-it.

```md
Sophia Tolstaya was born on 3 October 1844 in Pokrovskoye-Streshnevo.[^1]
She was Tolstoy's wife of 48 years and principal manuscript copyist.[^2]

[^1]: Jubilee Edition, vol. 83, p. 12. (PD)
[^2]: tolstoydigital/TEI, `personList.xml` entry Q2917962. (CC BY-SA 4.0)
```

No prefix on the footnote ID. No custom shortcode. Markdown-it handles the rendering; Obsidian renders the same syntax natively in preview.

One footnote per claim-cluster, not per word. A single sentence may carry one footnote even when it asserts several facts, provided they all come from the same source.

---

## The licence tag rule

Every footnote ends with a parenthetical licence tag. This is what makes the mechanism do double duty as copyright transparency.

| Tag | Meaning |
|---|---|
| `(PD)` | Public domain. No restrictions. |
| `(CC BY-SA 4.0)` | Creative Commons Attribution-ShareAlike 4.0. |
| `(CC BY 4.0)` | Creative Commons Attribution 4.0. |
| `(fair use)` | Used under fair use / fair dealing. Provide rationale on the source card. |
| `(restricted)` | Used by permission. Do not redistribute the source text. |

A footnote with no tag is a lint error. The tag is the contract: the reader can see the copyright status of every fact without leaving the page, and a downstream republisher can filter for compliance.

---

## Toggle behaviour

Footnotes are **off by default**. The site is for reading; verification is on demand.

Two states, cycled by a small button in the page header:

| State | Prose | Page footer |
|---|---|---|
| Off (default) | Clean. No `[1]` markers visible. | "Sources used on this page" summary block — one line per unique source, with licence tag. |
| On | Wikipedia-style `[1]` markers. | Full "References" section with every footnote. |

State persists in `localStorage` so a reader who turns it on stays in that mode across the site.

CSS does the swap. JavaScript is ~15 lines: cycle the `data-sources="off|on"` attribute on `<html>` and persist it. No framework, no dependency.

The summary block (off-state footer) is auto-generated at build time by collecting the unique sources referenced in the footnotes, deduplicated and ordered by first appearance. It is not a frontmatter field — there is nothing to maintain.

---

## Source IDs and source cards

Footnote text uses plain prose. The structured registry lives in `website/src/sources/` — one source card per major source, as defined in `wiki-schema.md`. Footnotes can wikilink the source name to its card:

```md
[^3]: [[Birukoff Biography]], vol. 1, p. 22. (PD)
```

This gives a reader who clicks through a stable destination (the source card) that describes the source itself.

A future lint step may enforce that every wikilinked source in a footnote resolves to an existing source card. Not required for source mode to ship.

---

## Relationship to `fieldSources` frontmatter

Two parallel mechanisms, both kept:

| Mechanism | Where | Purpose |
|---|---|---|
| `fieldSources:` frontmatter | YAML | Per-structured-field citation for dates, identifiers, etc. Machine-readable. Used by indexes, exports, and integrity checks. |
| `[^n]` prose footnotes | body | Per-prose-claim citation for narrative content. Human-readable. Surfaced through source mode. |

A page that has both is fully cited. A page with only `fieldSources` is structurally cited but the prose is uncited — acceptable for `recordStatus: draft`, not acceptable for `recordStatus: verified`.

---

## What source mode does not do

It does not assert that the page's prose is itself CC BY-SA. The prose remains under the project's SDG dedication. The licence tag in a footnote describes the *source* of the fact, not the *page that cites it*. Facts are not copyrightable; citing a CC BY-SA source does not propagate ShareAlike to the citing page. See `LICENSE` for the boundary rules.

It does not replace page-level attribution. The footer summary in the off-state is the page-level attribution display — it satisfies the attribution (BY) obligation regardless of whether a reader ever turns footnotes on.
