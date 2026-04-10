# Tolstoy Wiki — Place Schema

**Project:** tolstoy.life  
**Convention:** camelCase (YAML frontmatter)  
**Date:** 2026-04-03 (v1)

---

## 1. Core Identity

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | ✓ | Unique slug, e.g. `yasnaya-polyana` |
| `recordStatus` | string | ✓ | `draft` · `reviewed` · `verified` |
| `nameEn` | string | ✓ | Primary English name |
| `nameRu` | string | ✓ | Russian name in Cyrillic |
| `nameAlternatives` | object[] | | Historical, variant, or translated names |
| `nameAlternatives[].name` | string | | Alternative name |
| `nameAlternatives[].type` | string | | `historical` · `transliteration` · `variant` · `translation` |
| `nameAlternatives[].language` | string | | ISO 639-1 |
| `placeType` | string | ✓ | `estate` · `city` · `town` · `village` · `region` · `country` · `building` · `room` · `station` · `monastery` · `other` |

```yaml
id: "yasnaya-polyana"
recordStatus: "draft"
nameEn: "Yasnaya Polyana"
nameRu: "Ясная Поляна"
nameAlternatives:
  - name: "Bright Glade"
    type: "translation"
    language: "en"
placeType: "estate"
```

---

## 2. Location

| Field | Type | Description |
|---|---|---|
| `country` | string | Country name |
| `region` | string | Oblast, province, or region |
| `city` | string | Nearest city or town |
| `coordinates.lat` | number | Latitude (decimal degrees) |
| `coordinates.lng` | number | Longitude (decimal degrees) |
| `coordinates.approximate` | boolean | `true` if coordinates are approximate |

```yaml
country: "Russia"
region: "Tula Oblast"
city: "Tula"
coordinates:
  lat: 54.0667
  lng: 37.5167
  approximate: false
```

---

## 3. Significance to Tolstoy

| Field | Type | Description |
|---|---|---|
| `roleInTolstoyLife` | string | `birthplace` · `primary-residence` · `writing-location` · `death-location` · `exile` · `visited` · `correspondence-destination` · `other` |
| `periodOfAssociation` | object | Date range of Tolstoy's primary association with this place |
| `periodOfAssociation.from` | string | ISO 8601 year or date |
| `periodOfAssociation.fromOldStyle` | string | Julian (OS) |
| `periodOfAssociation.to` | string | ISO 8601 year or date |
| `periodOfAssociation.toOldStyle` | string | Julian (OS) |
| `periodOfAssociation.notes` | string | Free text |
| `synopsis` | string | 2–4 sentence description of the place's role in Tolstoy's life |

```yaml
roleInTolstoyLife: "primary-residence"
periodOfAssociation:
  from: "1828"
  fromOldStyle: "1828"
  to: "1910"
  toOldStyle: "1910"
  notes: "Tolstoy's birthplace and lifelong home, except for periods in Moscow and travels."
synopsis: >
  Yasnaya Polyana (Bright Glade) was Tolstoy's ancestral estate in Tula Oblast
  and the centre of his entire life. He was born here in 1828, wrote both War
  and Peace and Anna Karenina here, ran his famous school for peasant children
  here, and departed from here in October 1910, never to return. The estate is
  now a national museum.
```

---

## 4. Works Written Here

| Field | Type | Description |
|---|---|---|
| `worksWrittenHere` | string[] | `id` slugs of works authored at this location |

```yaml
worksWrittenHere:
  - "war-and-peace"
  - "anna-karenina"
  - "a-confession"
  - "the-kingdom-of-god-is-within-you"
  - "what-is-art"
  - "resurrection"
```

---

## 5. Identifiers

| Field | Type | Description |
|---|---|---|
| `identifiers.wikidata` | string | Wikidata QID |
| `identifiers.geonames` | string | GeoNames ID |
| `identifiers.openStreetMap` | string | OpenStreetMap node/way/relation ID |

```yaml
identifiers:
  wikidata: "Q214491"
  geonames: ""
  openStreetMap: ""
```

---

## 6. Field Sources

```yaml
fieldSources:
  coordinates:
    - sourceId: "wikidata"
      page: ""
      quote: ""
      notes: "Q214491"
  periodOfAssociation.from:
    - sourceId: "birukoff-biography"
      volume: "1"
      page: ""
      quote: ""
      notes: "Tolstoy born at Yasnaya Polyana, 28 August 1828 (OS 16 August)."
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
placeType: ""

# ── Location ─────────────────────────────────────────────────
country: ""
region: ""
city: ""
coordinates:
  lat: 0
  lng: 0
  approximate: false

# ── Significance ─────────────────────────────────────────────
roleInTolstoyLife: ""
periodOfAssociation:
  from: ""
  fromOldStyle: ""
  to: ""
  toOldStyle: ""
  notes: ""
synopsis: ""

# ── Works ────────────────────────────────────────────────────
worksWrittenHere: []

# ── Identifiers ──────────────────────────────────────────────
identifiers:
  wikidata: ""
  geonames: ""
  openStreetMap: ""

# ── Field Sources ─────────────────────────────────────────────
fieldSources:
  id:
    - sourceId: ""
      page: ""
      quote: ""
      notes: ""
```
