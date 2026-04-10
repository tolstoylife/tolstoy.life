# Tolstoy Wiki — Person Schema

**Project:** tolstoy.life  
**Convention:** camelCase (YAML frontmatter)  
**Date:** 2026-04-03 (v1)

---

## 1. Core Identity

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | ✓ | Unique slug, e.g. `vladimir-chertkov` |
| `recordStatus` | string | ✓ | `draft` · `reviewed` · `verified` |
| `nameEn` | string | ✓ | Primary English name |
| `nameRu` | string | ✓ | Russian name in Cyrillic |
| `nameAlternatives` | object[] | | Other known names, spellings, maiden names |
| `nameAlternatives[].name` | string | | Alternative name |
| `nameAlternatives[].type` | string | | `maiden` · `alias` · `transliteration` · `variant` |
| `nameAlternatives[].language` | string | | ISO 639-1 |

```yaml
id: "vladimir-chertkov"
recordStatus: "draft"
nameEn: "Vladimir Grigoryevich Chertkov"
nameRu: "Владимир Григорьевич Чертков"
nameAlternatives:
  - name: "Tchertkoff"
    type: "transliteration"
    language: "en"
```

---

## 2. Vital Dates

> **Calendar note:** Same dual-calendar rule as works. All dates Gregorian (NS) with Julian (OS) companion fields.

| Field | Type | Required | Description |
|---|---|---|---|
| `dateBorn` | string | ✓ | ISO 8601: `YYYY-MM-DD` · `YYYY-MM` · `YYYY` |
| `dateBornOldStyle` | string | | Julian (OS) date |
| `dateBornApproximate` | boolean | | `true` if uncertain |
| `placeBorn` | string | | City/town of birth |
| `countryBorn` | string | | Country of birth |
| `dateDied` | string | | ISO 8601 |
| `dateDiedOldStyle` | string | | Julian (OS) date |
| `dateDiedApproximate` | boolean | | `true` if uncertain |
| `placeDied` | string | | City/town of death |
| `countryDied` | string | | Country of death |
| `causeOfDeath` | string | | Free text |

```yaml
dateBorn: "1854-11-22"
dateBornOldStyle: "1854-11-10"
dateBornApproximate: false
placeBorn: "Saint Petersburg"
countryBorn: "Russia"
dateDied: "1936-11-09"
dateDiedOldStyle: ""
dateDiedApproximate: false
placeDied: "Moscow"
countryDied: "Soviet Union"
causeOfDeath: ""
```

---

## 3. Relationship to Tolstoy

| Field | Type | Required | Description |
|---|---|---|---|
| `relationToTolstoy` | string | ✓ | `family` · `disciple` · `friend` · `editor` · `translator` · `publisher` · `correspondent` · `critic` · `physician` · `secretary` · `adversary` · `other` |
| `relationshipDescription` | string | | One-sentence summary of the relationship |
| `periodOfContact` | object | | Date range of primary contact with Tolstoy |
| `periodOfContact.from` | string | | ISO 8601 year or date |
| `periodOfContact.to` | string | | ISO 8601 year or date |
| `periodOfContact.notes` | string | | Free text |
| `authorityTier` | integer | | Source authority tier: `1` = highest (Birukoff, Chertkov, inner circle), `2` = trusted secondary, `3` = fact-check only |

```yaml
relationToTolstoy: "disciple"
relationshipDescription: >
  Tolstoy's closest disciple, literary executor, and publisher. Founded the
  Free Age Press in England to publish Tolstoy's banned works uncensored.
periodOfContact:
  from: "1883"
  to: "1910"
  notes: "Met Tolstoy in 1883; present at his deathbed in Astapovo."
authorityTier: 1
```

---

## 4. Biography Summary

| Field | Type | Description |
|---|---|---|
| `occupation` | string[] | Free keyword tags, e.g. `["publisher", "editor", "pacifist"]` |
| `nationality` | string | ISO 3166-1 alpha-2, e.g. `ru` |
| `religion` | string | Free text |
| `politicalViews` | string | Free text |
| `synopsis` | string | Brief biographical summary (2–4 sentences) |

```yaml
occupation:
  - "publisher"
  - "editor"
  - "Tolstoyan activist"
nationality: "ru"
religion: "Tolstoyan Christianity"
politicalViews: "Christian anarchism, pacifism"
synopsis: >
  Vladimir Chertkov was a Russian aristocrat who became Tolstoy's closest
  collaborator and literary executor. He founded the Free Age Press in England
  to publish Tolstoy's late works free of Russian censorship, and edited the
  authoritative 1917 English edition of Tolstoy's early diaries.
```

---

## 5. Key Works Associated

| Field | Type | Description |
|---|---|---|
| `worksAuthored` | string[] | `id` slugs of works this person authored |
| `worksTranslated` | string[] | `id` slugs of works this person translated |
| `worksEdited` | string[] | `id` slugs of works this person edited |
| `worksTranscribed` | string[] | `id` slugs of works this person transcribed |

```yaml
worksAuthored:
  - "the-last-days-of-tolstoy"
worksTranslated:
  - "tolstoy-diaries-1847-1852"
worksEdited:
  - "the-kingdom-of-god-is-within-you"
  - "what-is-art"
worksTranscribed: []
```

---

## 6. Identifiers

| Field | Type | Description |
|---|---|---|
| `identifiers.wikidata` | string | Wikidata QID |
| `identifiers.viaf` | string | VIAF ID |
| `identifiers.lccn` | string | Library of Congress authority ID |
| `identifiers.bnf` | string | Bibliothèque nationale de France ID |

```yaml
identifiers:
  wikidata: "Q236956"
  viaf: ""
  lccn: ""
  bnf: ""
```

---

## 7. Field Sources

Same `fieldSources` pattern as works schema — maps field names to `sourceId` values from `sources.yaml`.

```yaml
fieldSources:
  dateBorn:
    - sourceId: "birukoff-biography"
      volume: "1"
      page: ""
      quote: ""
      notes: ""
  relationToTolstoy:
    - sourceId: "chertkov-last-days"
      page: ""
      quote: ""
      notes: ""
```

---

## Full Blank Template

```yaml
# ── Core Identity ────────────────────────────────────────────
id: ""
recordStatus: "draft"
nameEn: ""
nameRu: ""
nameAlternatives: []

# ── Vital Dates ──────────────────────────────────────────────
dateBorn: ""
dateBornOldStyle: ""
dateBornApproximate: false
placeBorn: ""
countryBorn: ""
dateDied: ""
dateDiedOldStyle: ""
dateDiedApproximate: false
placeDied: ""
countryDied: ""
causeOfDeath: ""

# ── Relationship to Tolstoy ──────────────────────────────────
relationToTolstoy: ""
relationshipDescription: ""
periodOfContact:
  from: ""
  to: ""
  notes: ""
authorityTier: 2

# ── Biography ────────────────────────────────────────────────
occupation: []
nationality: ""
religion: ""
politicalViews: ""
synopsis: ""

# ── Works ────────────────────────────────────────────────────
worksAuthored: []
worksTranslated: []
worksEdited: []
worksTranscribed: []

# ── Identifiers ──────────────────────────────────────────────
identifiers:
  wikidata: ""
  viaf: ""
  lccn: ""
  bnf: ""

# ── Field Sources ─────────────────────────────────────────────
fieldSources:
  id:
    - sourceId: ""
      page: ""
      quote: ""
      notes: ""
```
