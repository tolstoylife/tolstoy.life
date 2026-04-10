# wiki-schema.md — Wiki Article Schema

> **Version:** 1.0 (2026-04-06)
> **Companion to:** `schema/tolstoy-works-schema.md` (v5) for work metadata.

This document defines the structure, frontmatter templates, and conventions for wiki articles in `src/wiki/`. It also covers the source cards, index, and log files in `src/sources/`.

Works have their own schema (`schema/tolstoy-works-schema.md`). This file covers people, places, events, and concepts.

---

## Page types

Every wiki article has a `type` field in its frontmatter. The four types are:

| Type | What it covers | Examples |
|---|---|---|
| `person` | Historical individuals | Sophia Tolstaya, Ivan Turgenev, Aylmer Maude |
| `place` | Locations and buildings | Yasnaya Polyana, Moscow, Astapovo station |
| `event` | Historical events and incidents | Excommunication of Tolstoy, Emancipation reform of 1861 |
| `concept` | Ideas, movements, and themes | Christian anarchism, Tolstoyan movement, Non-resistance |

---

## Frontmatter conventions

All frontmatter follows these rules (inherited from the root CLAUDE.md):

- Fields use **camelCase**.
- Dates are **ISO 8601** (`YYYY-MM-DD`, `YYYY-MM`, or `YYYY`).
- Pre-1918 dates must have a `...OldStyle` companion field.
- Uncertain dates use a `...Approximate: true` companion.
- Empty optional fields use `""` (string) or `[]` (array) — never `null` or omitted.
- Prefer **Wikidata QIDs** as the primary external identifier.
- `id` is the canonical slug — kebab-case, unique across the entire vault.
- `recordStatus` is one of: `draft`, `reviewed`, `verified`.

---

## Person template

```yaml
---
id: sophia-tolstaya
recordStatus: draft
type: person
titleEn: Sophia Tolstaya
titleRu: Софья Андреевна Толстая
description: "Wife of Leo Tolstoy, diarist, and manuscript transcriber (1844–1919)."
birthDate: "1844-10-03"
birthDateOldStyle: "1844-09-21"
birthDateApproximate: false
deathDate: "1919-11-04"
deathDateOldStyle: ""
deathDateApproximate: false
birthPlace: "Pokrovskoye-Streshnevo, Moscow, Russia"
deathPlace: "Yasnaya Polyana, Tula Oblast, Russia"
nationality: Russian
roles:
  - diarist
  - transcriber
  - photographer
relationToTolstoy: wife
relatedWorks:
  -
    id: anna-karenina
    role: transcriber
  -
    id: war-and-peace
    role: transcriber
relatedArticles:
  - yasnaya-polyana
  - leo-tolstoy
themes:
  - Tolstoy family
  - manuscript transcription
identifiers:
  wikidata: Q2917962
  viaf: ""
fieldSources:
  birthDate:
    -
      sourceId: jubilee-edition
      volume: ""
      page: ""
      notes: ""
---

Prose content about this person. All claims cite primary sources.
Uses [[wikilinks]] to connect to other vault files.
```

---

## Place template

```yaml
---
id: yasnaya-polyana
recordStatus: draft
type: place
titleEn: Yasnaya Polyana
titleRu: Ясная Поляна
description: "Tolstoy's primary estate in Tula Oblast, Russia."
country: Russia
region: Tula Oblast
coordinates:
  lat: 54.0667
  lon: 37.5167
significancePeriod: "1828–1910"
relatedArticles:
  - leo-tolstoy
  - sophia-tolstaya
themes:
  - Tolstoy residences
  - Russian literary landmarks
identifiers:
  wikidata: Q830274
fieldSources: {}
---

Prose content about this place.
```

---

## Event template

```yaml
---
id: excommunication-of-tolstoy
recordStatus: draft
type: event
titleEn: Excommunication of Tolstoy
titleRu: Отлучение Толстого от церкви
description: "The Holy Synod's 1901 proclamation declaring Tolstoy outside the Orthodox Church."
date: "1901-02-24"
dateOldStyle: "1901-02-11"
dateApproximate: false
location: "Saint Petersburg, Russia"
relatedArticles:
  - leo-tolstoy
  - sophia-tolstaya
themes:
  - Russian Orthodox Church
  - censorship
  - Tolstoy's religious views
identifiers:
  wikidata: ""
fieldSources: {}
---

Prose content about this event.
```

---

## Concept template

```yaml
---
id: christian-anarchism
recordStatus: draft
type: concept
titleEn: Christian Anarchism
titleRu: Христианский анархизм
description: "Political philosophy combining Christianity with anarchism, heavily influenced by Tolstoy's later writings."
relatedArticles:
  - leo-tolstoy
  - the-kingdom-of-god-is-within-you
relatedWorks:
  -
    id: the-kingdom-of-god-is-within-you
    relationshipType: source
themes:
  - political philosophy
  - pacifism
  - non-resistance
identifiers:
  wikidata: Q192936
fieldSources: {}
---

Prose content about this concept.
```

---

## Source card template — `src/sources/`

Each major source gets a small `.md` stub in `src/sources/`. Source cards make sources visible in Obsidian's graph and wikilink-able from wiki articles and log entries. The binary file itself stays in `primary-sources/` at the project root.

```yaml
---
id: birukoff-biography
type: source
titleEn: "Leo Tolstoy: His Life and Work"
titleRu: "Биография Л.Н. Толстого"
author: "Paul Birukoff"
publicationDate: "1911"
language: en
format: epub
binaryPath: "primary-sources/birukoff/leo-tolstoy-his-life-and-work.epub"
ingestionStatus: pending
ingestionDate: ""
pagesCreated: []
pagesUpdated: []
notes: "Awaiting cleaned EPUB. Original OCR had spacing artifacts."
---

One of the earliest comprehensive biographies of Tolstoy, written by a close associate. Primary source for biographical dates and events up to 1910.

Covers: early life, education, military service, literary career, religious crisis, final years.
```

### Fields

- `ingestionStatus`: `pending` · `partial` · `complete`
- `binaryPath`: relative path from the project root to the actual file in `primary-sources/`
- `pagesCreated` / `pagesUpdated`: filled in by Claude after ingestion, creating a record of what this source contributed to the wiki
- The prose section is a brief description of the source's scope and relevance

### Rules

- One source card per major source (not per chapter or per file within an archive)
- For large archives (e.g., the TEI/XML collection), one card for the collection with notes on which subsets have been ingested
- Source cards are referenced from the log: `Ingested from [[Birukoff Biography]]`
- Source cards are referenced from wiki articles via fieldSources or inline citations

---

## Index file — `src/sources/index.md`

The index is a catalog of every content page in the vault. Claude reads this first when navigating the vault at the start of a session or when answering queries. It should be kept current — updated on every ingest operation.

### Format

```md
# Vault Index

Last updated: 2026-04-06

## People

- [[Sophia Tolstaya]] — Wife of LT, diarist, manuscript transcriber (1844–1919)
- [[Leo Tolstoy]] — Russian novelist and moral philosopher (1828–1910)

## Places

- [[Yasnaya Polyana]] — Tolstoy's primary estate, Tula Oblast

## Events

(none yet)

## Concepts

(none yet)

## Works

- [[Anna Karenina]] — Novel (1878), genre: novel, status: draft
- [[War and Peace]] — Novel (1869), genre: novel, status: draft

## Sources

- [[Birukoff Biography]] — Paul Birukoff, biography (1911), status: pending
- [[TEI Reference Data]] — tolstoydigital TEI/XML (persons, locations, works), status: partial
```

### Rules

- One line per entry: `- [[Title]] — one-line summary`
- Organised by type, then alphabetically within each type
- Summaries should be under 80 characters
- Include key metadata inline (dates, genre, status) so Claude can quickly assess relevance without opening the file
- Works entries link to the work overview file, not the text files

---

## Log file — `src/sources/log.md`

The log is an append-only chronological record of wiki operations. It provides narrative context that git history doesn't capture.

### Format

```md
# Wiki Operations Log

## [2026-04-06] ingest | TEI personList.xml (test run)

**Source:** `sources/tolstoydigital-TEI/reference/personList.xml`
**Pages created:** Sophia Tolstaya, Tatyana Tolstaya, Maria Tolstaya
**Pages updated:** Leo Tolstoy (added relatedArticles)
**Notes:** Test run with 3 entities from Tolstoy's immediate family. Wikidata QIDs confirmed for all three. Sophia's birth date cross-checked against Jubilee Edition vol. 83.
**Open questions:** Sophia's death date varies across sources — 1919-11-04 (Maude) vs 1919-11-04 (Birukoff). Both agree; recorded as verified.

## [2026-04-06] lint | Initial vault health check

**Pages reviewed:** 5
**Issues found:** Leo Tolstoy.md had frontmatter fields from the old Supabase schema that needed updating.
**Actions taken:** Updated frontmatter to match wiki-schema.md person template. Removed legacy zone marker from pre-LLM-Wiki era.
```

### Rules

- Each entry starts with `## [YYYY-MM-DD] operation | Subject`
- Operations: `ingest`, `query`, `lint`, `edit`
- Always record: source, pages touched, notes, open questions
- Parseable with grep: `grep "^## \[" log.md | tail -5`
- Append only — never edit or delete old entries

---

## Prose conventions

All wiki article prose follows these standards:

- **Hard facts only.** No literary interpretation, no aesthetic judgments, no unattributed claims.
- **Every claim cites a primary source.** Use inline parenthetical citations: `(Jubilee Edition, vol. 83, p. 12)` or `(Maude, *The Life of Tolstoy*, vol. 2, ch. 14)`.
- **Source authority order:** Jubilee Edition → Tolstoy's diaries and letters → Birukoff biography → Chertkov correspondence → Maude biography.
- **When sources conflict**, record both values and note the conflict explicitly. Never silently prefer one source.
- **NS/OS dates:** Use NS (Gregorian) as the primary date in prose. Include OS in parentheses on first mention: "9 September 1828 (OS: 28 August)".
- **Wikilinks:** Use `[[double brackets]]` to link to other vault files. Link on first meaningful mention per article, not every occurrence.
- **Russian names:** Use the most common English transliteration for the article title. Include the full Russian name in Cyrillic in the first sentence.

---

## Wikilink targets

Wikilinks must resolve to existing files in the vault. The target is the filename without extension:

- `[[Anna Karenina]]` → `src/works/fiction/novels/anna-karenina/Anna Karenina.md`
- `[[Sophia Tolstaya]]` → `src/wiki/Sophia Tolstaya.md`
- `[[Yasnaya Polyana]]` → `src/wiki/Yasnaya Polyana.md`

If a wikilink target doesn't exist yet, either create a stub page or use plain text (no brackets) and note the missing page in the index as a gap to fill.
