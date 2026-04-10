# Tolstoy Works — Metadata Schema

**Project:** tolstoy.life
**Convention:** camelCase (YAML frontmatter) → snake_case (Supabase/PostgreSQL)
**Date:** 2026-03-31 (v5)

---

## 1. Core Identity

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | ✓ | Unique project slug, e.g. `anna-karenina` |
| `recordStatus` | string | ✓ | Editorial quality flag: `draft` · `reviewed` · `verified` |
| `titleEn` | string | ✓ | English title |
| `titleRu` | string | ✓ | Russian title in Cyrillic |
| `titleAlternatives` | object[] | | Working titles, translations, subtitles — see sub-fields below |
| `titleAlternatives[].title` | string | | The alternative title text |
| `titleAlternatives[].type` | string | | `working` · `translation` · `subtitle` · `variant` |
| `titleAlternatives[].language` | string | | ISO 639-1 language code, e.g. `fr` · `de` |

```yaml
id: "anna-karenina"
recordStatus: "draft"
titleEn: "Anna Karenina"
titleRu: "Анна Каренина"
titleAlternatives:
  - title: "Anna Karenine"
    type: "translation"
    language: "fr"
  - title: "A Young Lady's Story"
    type: "working"
    language: "en"
```

---

## 2. Type & Genre

| Field | Type | Required | Controlled Values |
|---|---|---|---|
| `genre` | string | ✓ | `novel` · `novella` · `short_story` · `parable` · `play` · `essay` · `philosophical` · `religious` · `diary` · `letter` · `poem` · `fragment` |
| `language` | string | ✓ | ISO 639-1, e.g. `ru` · `fr` |
| `completionStatus` | string | ✓ | `complete` · `incomplete` · `fragmentary` |
| `publishedDuringLifetime` | boolean | ✓ | `true` if published anywhere (in any language) before Tolstoy's death (November 1910) |
| `publishedInRussiaDuringLifetime` | boolean | ✓ | `true` if legally published in Russia before Tolstoy's death (November 1910). `false` if banned or only published abroad. |

```yaml
genre: "novel"
language: "ru"
completionStatus: "complete"
publishedDuringLifetime: true
publishedInRussiaDuringLifetime: true
```

---

## 3. Chronology

> **Calendar note:** All dates use the Gregorian calendar (New Style, NS) as the canonical value. Russia used the Julian calendar (Old Style, OS) until 1 February 1918. In the 19th century the Julian calendar ran 12 days behind Gregorian; from 1 March 1900 onward, 13 days behind. Always record the original Old Style date in the `...OldStyle` companion field to allow cross-checking against Russian sources and to catch dating errors.

> **Time of day:** The `time...` fields accept either an ISO 8601 time (`HH:MM`) or a descriptive value: `morning` · `afternoon` · `evening` · `night`. Most relevant for letters and diary entries where Tolstoy often noted the time of writing.

| Field | Type | Required | Description |
|---|---|---|---|
| `dateWritingStarted` | string | | Gregorian (NS). ISO 8601: `YYYY-MM-DD` · `YYYY-MM` · `YYYY` |
| `dateWritingStartedOldStyle` | string | | Julian (OS) date as recorded in Russian sources |
| `dateWritingStartedApproximate` | boolean | | `true` if exact date is uncertain |
| `timeWritingStarted` | string | | Time of day: ISO `HH:MM` or `morning` · `afternoon` · `evening` · `night` |
| `dateWritingCompleted` | string | | Gregorian (NS). ISO 8601: `YYYY-MM-DD` · `YYYY-MM` · `YYYY` |
| `dateWritingCompletedOldStyle` | string | | Julian (OS) date as recorded in Russian sources |
| `dateWritingCompletedApproximate` | boolean | | `true` if exact date is uncertain |
| `timeWritingCompleted` | string | | Time of day: ISO `HH:MM` or `morning` · `afternoon` · `evening` · `night` |
| `dateFirstPublished` | string | | Gregorian (NS). ISO 8601: `YYYY-MM-DD` · `YYYY-MM` · `YYYY` |
| `dateFirstPublishedOldStyle` | string | | Julian (OS) date as recorded in Russian sources |
| `dateFirstPublishedApproximate` | boolean | | `true` if exact date is uncertain |
| `firstPublishedVenue` | string | | Name of journal, newspaper, or publisher |
| `firstPublishedVenueType` | string | | `journal` · `newspaper` · `book` · `samizdat` |
| `dateFirstPublishedInRussia` | string | | Gregorian (NS). ISO 8601: date of first legal Russian publication — whether during Tolstoy's lifetime or posthumously. Leave blank only if never legally published in Russia at all. |
| `dateFirstPublishedInRussiaOldStyle` | string | | Julian (OS) date as recorded in Russian sources |
| `dateFirstPublishedInRussiaApproximate` | boolean | | `true` if exact date is uncertain |
| `firstPublishedInRussiaVenue` | string | | Name of journal, newspaper, or publisher of first Russian edition |
| `firstPublishedInRussiaVenueType` | string | | `journal` · `newspaper` · `book` · `samizdat` |

```yaml
dateWritingStarted: "1873-03-31"
dateWritingStartedOldStyle: "1873-03-19"
dateWritingStartedApproximate: false
timeWritingStarted: ""
dateWritingCompleted: "1877-04-29"
dateWritingCompletedOldStyle: "1877-04-17"
dateWritingCompletedApproximate: false
timeWritingCompleted: ""
dateFirstPublished: "1878-01-13"
dateFirstPublishedOldStyle: "1878-01-01"
dateFirstPublishedApproximate: false
firstPublishedVenue: "Русский вестник (Russkiy Vestnik)"
firstPublishedVenueType: "journal"
dateFirstPublishedInRussia: "1878-01-13"
dateFirstPublishedInRussiaOldStyle: "1878-01-01"
dateFirstPublishedInRussiaApproximate: false
firstPublishedInRussiaVenue: "Русский вестник (Russkiy Vestnik)"
firstPublishedInRussiaVenueType: "journal"
```

---

## 4. Authoring Locations

An ordered list. One entry per distinct location where the work was written.

| Field | Type | Description |
|---|---|---|
| `authoringLocations[].country` | string | Country name |
| `authoringLocations[].region` | string | Oblast, province, or region |
| `authoringLocations[].city` | string | City or town |
| `authoringLocations[].estate` | string | Estate or named property |
| `authoringLocations[].building` | string | Building name or type |
| `authoringLocations[].room` | string | Room name or type |
| `authoringLocations[].coordinates.lat` | number | Latitude (decimal degrees) |
| `authoringLocations[].coordinates.lng` | number | Longitude (decimal degrees) |
| `authoringLocations[].dateFrom` | string | Gregorian (NS). ISO 8601: start of time at this location |
| `authoringLocations[].dateFromOldStyle` | string | Julian (OS) date as recorded in Russian sources |
| `authoringLocations[].dateFromApproximate` | boolean | `true` if exact start date is uncertain |
| `authoringLocations[].dateTo` | string | Gregorian (NS). ISO 8601: end of time at this location |
| `authoringLocations[].dateToOldStyle` | string | Julian (OS) date as recorded in Russian sources |
| `authoringLocations[].dateToApproximate` | boolean | `true` if exact end date is uncertain |
| `authoringLocations[].notes` | string | Free text |

```yaml
authoringLocations:
  - country: "Russia"
    region: "Tula Oblast"
    city: "Yasnaya Polyana"
    estate: "Yasnaya Polyana Estate"
    building: "Main House"
    room: "Study"
    coordinates:
      lat: 54.0667
      lng: 37.5167
    dateFrom: "1873-03-31"
    dateFromOldStyle: "1873-03-19"
    dateFromApproximate: false
    dateTo: "1875-12-13"
    dateToOldStyle: "1875-12-01"
    dateToApproximate: false
    notes: "Primary location, drafts 1–4"
  - country: "Russia"
    region: "Moscow"
    city: "Moscow"
    estate: ""
    building: "Tolstoy House, Khamovniki"
    room: "Study"
    coordinates:
      lat: 55.7290
      lng: 37.5720
    dateFrom: "1875-12-13"
    dateFromOldStyle: "1875-12-01"
    dateFromApproximate: false
    dateTo: "1876-03-13"
    dateToOldStyle: "1876-03-01"
    dateToApproximate: false
    notes: "Winter 1875–76"
```

---

## 5. Manuscripts

One entry per known draft. Writing materials and scans are recorded at the individual manuscript level.

| Field | Type | Description |
|---|---|---|
| `manuscripts[].draftId` | string | Unique ID within this work, e.g. `ms-01` |
| `manuscripts[].draftNumber` | integer | Ordinal position |
| `manuscripts[].draftLabel` | string | `first-draft` · `intermediate-draft` · `final-draft` · `fair-copy` · `printers-copy` |
| `manuscripts[].dateCreated` | string | Gregorian (NS). ISO 8601: approximate date this draft was written |
| `manuscripts[].dateCreatedOldStyle` | string | Julian (OS) date as recorded in Russian sources |
| `manuscripts[].dateCreatedApproximate` | boolean | `true` if date is uncertain |
| `manuscripts[].timeCreated` | string | Time of day: ISO `HH:MM` or `morning` · `afternoon` · `evening` · `night` |
| `manuscripts[].numberOfFolios` | integer | Physical extent of the manuscript in folios |
| `manuscripts[].condition` | string | `good` · `fair` · `poor` · `damaged` · `lost` |
| `manuscripts[].currentRepository` | string | Full institution name |
| `manuscripts[].repositoryCity` | string | |
| `manuscripts[].repositoryCountry` | string | |
| `manuscripts[].repositoryCallNumber` | string | Shelf mark, fond/opis/delo, or archival reference |
| `manuscripts[].scans[]` | object[] | Array — one entry per digitisation |
| `manuscripts[].scans[].url` | string | Direct URL to scan or image |
| `manuscripts[].scans[].sourceInstitution` | string | Institution providing the scan |
| `manuscripts[].scans[].license` | string | e.g. `CC-BY 4.0` · `Public Domain` · `All rights reserved` |
| `manuscripts[].scans[].credit` | string | Attribution string |
| `manuscripts[].scans[].dateAccessed` | string | ISO 8601: `YYYY-MM-DD` |
| `manuscripts[].writingMaterials.pen` | string | e.g. `Steel-nib dip pen` |
| `manuscripts[].writingMaterials.ink` | string | e.g. `Iron gall ink, black` |
| `manuscripts[].writingMaterials.paper` | string | e.g. `Laid paper, cream, unlined, folio` |
| `manuscripts[].writingMaterials.notes` | string | Free text |

```yaml
manuscripts:
  - draftId: "ms-01"
    draftNumber: 1
    draftLabel: "first-draft"
    dateCreated: "1873"
    dateCreatedOldStyle: "1873"
    dateCreatedApproximate: true
    timeCreated: ""
    numberOfFolios: 0
    condition: "good"
    currentRepository: "State Museum of Leo Tolstoy"
    repositoryCity: "Moscow"
    repositoryCountry: "Russia"
    repositoryCallNumber: ""
    scans:
      - url: ""
        sourceInstitution: ""
        license: ""
        credit: ""
        dateAccessed: ""
    writingMaterials:
      pen: ""
      ink: ""
      paper: ""
      notes: ""
```

---

## 6. Transcriptions

One entry per known transcription. Transcriber is drawn from a controlled list.

**Controlled list — transcribers:**

| `transcriberId` | `transcriberName` |
|---|---|
| `sophia-tolstaya` | Sophia Andreevna Tolstaya |
| `tatyana-tolstaya` | Tatyana Lvovna Tolstaya |
| `maria-tolstaya` | Maria Lvovna Tolstaya |
| `nikolai-gusev` | Nikolai Nikolaevich Gusev |
| `leo-tolstoy` | Leo Nikolaevich Tolstoy (autograph) |
| `other` | Other (specify in `transcriberName`) |

| Field | Type | Description |
|---|---|---|
| `transcriptions[].sourceManuscriptId` | string | `draftId` of the manuscript this transcription was made from, e.g. `ms-01`. Leave blank if unknown. |
| `transcriptions[].transcriberId` | string | From controlled list above |
| `transcriptions[].transcriberName` | string | Full name (required when `transcriberId` is `other`) |
| `transcriptions[].relationToAuthor` | string | `wife` · `daughter` · `son` · `secretary` · `physician` · `friend` · `self` · `other` |
| `transcriptions[].dateTranscribed` | string | Gregorian (NS). ISO 8601: approximate date of transcription |
| `transcriptions[].dateTranscribedOldStyle` | string | Julian (OS) date as recorded in Russian sources |
| `transcriptions[].dateTranscribedApproximate` | boolean | `true` if date is uncertain |
| `transcriptions[].timeTranscribed` | string | Time of day: ISO `HH:MM` or `morning` · `afternoon` · `evening` · `night` |
| `transcriptions[].currentRepository` | string | Full institution name |
| `transcriptions[].repositoryCity` | string | |
| `transcriptions[].repositoryCountry` | string | |
| `transcriptions[].repositoryCallNumber` | string | Shelf mark or archival reference |
| `transcriptions[].scans[]` | object[] | Array — one entry per digitisation |
| `transcriptions[].scans[].url` | string | |
| `transcriptions[].scans[].sourceInstitution` | string | |
| `transcriptions[].scans[].license` | string | |
| `transcriptions[].scans[].credit` | string | |
| `transcriptions[].scans[].dateAccessed` | string | ISO 8601: `YYYY-MM-DD` |
| `transcriptions[].notes` | string | Free text |

```yaml
transcriptions:
  - sourceManuscriptId: "ms-01"
    transcriberId: "sophia-tolstaya"
    transcriberName: "Sophia Andreevna Tolstaya"
    relationToAuthor: "wife"
    dateTranscribed: "1873"
    dateTranscribedOldStyle: "1873"
    dateTranscribedApproximate: true
    timeTranscribed: ""
    currentRepository: "State Museum of Leo Tolstoy"
    repositoryCity: "Moscow"
    repositoryCountry: "Russia"
    repositoryCallNumber: ""
    scans:
      - url: ""
        sourceInstitution: ""
        license: ""
        credit: ""
        dateAccessed: ""
    notes: ""
```

---

## 7. Bibliographic

| Field | Type | Description |
|---|---|---|
| `dedicatedToEn` | string | Dedication recipient (English) |
| `dedicatedToRu` | string | Dedication recipient (Russian) |
| `epigraph` | string | Full epigraph text |
| `epigraphLanguage` | string | ISO 639-1 language code of the epigraph, e.g. `ru` · `fr` · `cu` (Church Slavonic) |
| `epigraphAuthor` | string | Author of epigraph |
| `epigraphSource` | string | Source work of epigraph |
| `themes` | string[] | Free keyword tags |
| `subjectHeadings` | string[] | Library of Congress Subject Headings (LCSH) |
| `synopsis` | string | Brief summary of the work |
| `bans[]` | object[] | Array — one entry per distinct banning event (one authority, one jurisdiction). Empty array if never banned. |
| `bans[].banningAuthority` | string | Full name of the authority that issued the ban |
| `bans[].authorityType` | string | `imperial-state` · `holy-synod` · `foreign-government` · `periodical-editor` · `other` |
| `bans[].jurisdiction` | string | Country or region where the ban applied, e.g. `Russia` · `United States` · `Russian Empire` |
| `bans[].scope` | string | `complete-ban` · `passages-cut` · `serialization-refused` · `confiscation` · `pre-publication-rejected` |
| `bans[].banDate` | string | Gregorian (NS). ISO 8601: date of ban |
| `bans[].banDateOldStyle` | string | Julian (OS) date of ban |
| `bans[].banDateApproximate` | boolean | `true` if exact ban date is uncertain |
| `bans[].banLiftedDate` | string | Gregorian (NS). ISO 8601: date ban was lifted |
| `bans[].banLiftedDateOldStyle` | string | Julian (OS) date ban was lifted |
| `bans[].banLiftedDateApproximate` | boolean | `true` if exact lift date is uncertain |
| `bans[].notes` | string | Free text — context, partial bans, regional variations |
| `samizdatCirculation` | boolean | `true` if the work circulated in handwritten or lithographed copies independently of official publication channels |
| `excommunicationRelated` | boolean | `true` if this work was cited in or directly affected by the 1901 Holy Synod excommunication decree |
| `censoredVersionExists` | boolean | `true` if a censored (cut) edition exists alongside an uncensored foreign or posthumous edition |
| `censoredVersionNotes` | string | Details of the censored edition — what was cut, which venue published the cut version, which editor intervened |
| `censorshipNotes` | string | Broader censorship narrative — history, context, reception, any aspects not captured in structured fields |
| `wordCount` | integer | Word count of canonical text |
| `wordCountEdition` | string | Edition the word count is based on, e.g. `Jubilee Edition, vol. 18` · `Maude translation (1918)` |
| `relatedWorks` | object[] | Links to related works with relationship type |
| `relatedWorks[].id` | string | tolstoy.life ID of the related work |
| `relatedWorks[].relationshipType` | string | `cycle` · `sequel` · `prequel` · `revision` · `source` · `companion` · `adaptation` |
| `notes` | string | General free-text remarks |

```yaml
dedicatedToEn: ""
dedicatedToRu: ""
epigraph: "Vengeance is mine; I will repay."
epigraphLanguage: "ru"
epigraphAuthor: ""
epigraphSource: "Romans 12:19"
themes:
  - "marriage"
  - "infidelity"
  - "Russian society"
  - "moral redemption"
subjectHeadings:
  - "Domestic fiction"
  - "Russia -- Social life and customs -- 19th century"
synopsis: ""
bans:
  - banningAuthority: "Main Administration for Press Affairs"
    authorityType: "imperial-state"
    jurisdiction: "Russia"
    scope: "pre-publication-rejected"
    banDate: ""
    banDateOldStyle: ""
    banDateApproximate: true
    banLiftedDate: "1905"
    banLiftedDateOldStyle: "1905"
    banLiftedDateApproximate: true
    notes: "Rejected before publication. First published abroad (Leipzig, 1894)."
  - banningAuthority: "Holy Synod of the Russian Orthodox Church"
    authorityType: "holy-synod"
    jurisdiction: "Russia"
    scope: "complete-ban"
    banDate: ""
    banDateOldStyle: ""
    banDateApproximate: true
    banLiftedDate: ""
    banLiftedDateOldStyle: ""
    banLiftedDateApproximate: false
    notes: "Ecclesiastical ban enforced independently of state censorship. Never formally lifted."
samizdatCirculation: false
excommunicationRelated: false
censoredVersionExists: false
censoredVersionNotes: ""
censorshipNotes: ""
wordCount: 349736
wordCountEdition: "Jubilee Edition, vol. 18–19"
relatedWorks:
  - id: "war-and-peace"
    relationshipType: "companion"
notes: ""
```

---

## 8. Identifiers

All known external identifiers. Values are strings unless marked as arrays.

| Field | Type | Description |
|---|---|---|
| `identifiers.wikidata` | string | Wikidata QID, e.g. `Q155756` |
| `identifiers.openLibrary` | string | Open Library Work ID, e.g. `/works/OL257943W` |
| `identifiers.goodreads` | string | Goodreads Work ID |
| `identifiers.librarything` | string | LibraryThing Work ID |
| `identifiers.gutenberg` | string[] | Project Gutenberg IDs |
| `identifiers.internetArchive` | string[] | Internet Archive identifiers |
| `identifiers.lccn` | string | Library of Congress Control Number |
| `identifiers.oclc` | string[] | OCLC/WorldCat numbers |
| `identifiers.viaf` | string | Virtual International Authority File ID |
| `identifiers.bnf` | string | Bibliothèque nationale de France ID |
| `identifiers.jubileeEdition.volumes` | string | Volume(s) in the 90-vol. *Полное собрание сочинений* (1928–1964), e.g. `18–19` |
| `identifiers.jubileeEdition.notes` | string | |

```yaml
identifiers:
  wikidata: "Q155756"
  openLibrary: "/works/OL257943W"
  goodreads: "15823480"
  librarything: "2722"
  gutenberg:
    - "1399"
  internetArchive:
    - "annakarenina00tols"
  lccn: "04017838"
  oclc:
    - "1258154"
  viaf: ""
  bnf: ""
  jubileeEdition:
    volumes: "18–19"
    notes: ""
```

---

## 9. Field Sources

Source attribution at the field level. References `id` values defined in the shared `sources.yaml` library. Each entry maps a field name to one or more sources that support the value in that field.

> Nested fields use dot notation. Array items use zero-based index notation, e.g. `manuscripts[0].currentRepository`.

| Sub-field | Type | Description |
|---|---|---|
| `fieldSources.<fieldName>[].sourceId` | string | `id` from `sources.yaml` |
| `fieldSources.<fieldName>[].volume` | string | Volume number, if applicable |
| `fieldSources.<fieldName>[].page` | string | Page or folio reference |
| `fieldSources.<fieldName>[].quote` | string | Relevant excerpt from the source |
| `fieldSources.<fieldName>[].notes` | string | Free text — context, caveats, conflicts between sources |

```yaml
fieldSources:
  titleRu:
    - sourceId: "jubilee-edition"
      volume: "28"
      page: ""
      quote: ""
      notes: ""
  dateWritingStarted:
    - sourceId: "jubilee-edition"
      volume: "28"
      page: "xii"
      quote: ""
      notes: ""
    - sourceId: "maude-biography-vol2"
      page: "312"
      quote: ""
      notes: "Conflicts with Jubilee Edition by approx. two weeks."
  manuscripts[0].currentRepository:
    - sourceId: "tolstoy-museum-moscow"
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
titleEn: ""
titleRu: ""
titleAlternatives:
  - title: ""
    type: ""
    language: ""

# ── Type & Genre ─────────────────────────────────────────────
genre: ""
language: "ru"
completionStatus: ""
publishedDuringLifetime: false
publishedInRussiaDuringLifetime: false

# ── Chronology ───────────────────────────────────────────────
dateWritingStarted: ""
dateWritingStartedOldStyle: ""
dateWritingStartedApproximate: false
timeWritingStarted: ""
dateWritingCompleted: ""
dateWritingCompletedOldStyle: ""
dateWritingCompletedApproximate: false
timeWritingCompleted: ""
dateFirstPublished: ""
dateFirstPublishedOldStyle: ""
dateFirstPublishedApproximate: false
firstPublishedVenue: ""
firstPublishedVenueType: ""
dateFirstPublishedInRussia: ""
dateFirstPublishedInRussiaOldStyle: ""
dateFirstPublishedInRussiaApproximate: false
firstPublishedInRussiaVenue: ""
firstPublishedInRussiaVenueType: ""

# ── Authoring Locations ──────────────────────────────────────
authoringLocations:
  - country: ""
    region: ""
    city: ""
    estate: ""
    building: ""
    room: ""
    coordinates:
      lat: 0
      lng: 0
    dateFrom: ""
    dateFromOldStyle: ""
    dateFromApproximate: false
    dateTo: ""
    dateToOldStyle: ""
    dateToApproximate: false
    notes: ""

# ── Manuscripts ──────────────────────────────────────────────
manuscripts:
  - draftId: "ms-01"
    draftNumber: 1
    draftLabel: "first-draft"
    dateCreated: ""
    dateCreatedOldStyle: ""
    dateCreatedApproximate: false
    timeCreated: ""
    numberOfFolios: 0
    condition: ""
    currentRepository: ""
    repositoryCity: ""
    repositoryCountry: ""
    repositoryCallNumber: ""
    scans:
      - url: ""
        sourceInstitution: ""
        license: ""
        credit: ""
        dateAccessed: ""
    writingMaterials:
      pen: ""
      ink: ""
      paper: ""
      notes: ""

# ── Transcriptions ───────────────────────────────────────────
transcriptions:
  - sourceManuscriptId: ""
    transcriberId: ""
    transcriberName: ""
    relationToAuthor: ""
    dateTranscribed: ""
    dateTranscribedOldStyle: ""
    dateTranscribedApproximate: false
    timeTranscribed: ""
    currentRepository: ""
    repositoryCity: ""
    repositoryCountry: ""
    repositoryCallNumber: ""
    scans:
      - url: ""
        sourceInstitution: ""
        license: ""
        credit: ""
        dateAccessed: ""
    notes: ""

# ── Bibliographic ────────────────────────────────────────────
dedicatedToEn: ""
dedicatedToRu: ""
epigraph: ""
epigraphLanguage: ""
epigraphAuthor: ""
epigraphSource: ""
themes: []
subjectHeadings: []
synopsis: ""
bans: []
samizdatCirculation: false
excommunicationRelated: false
censoredVersionExists: false
censoredVersionNotes: ""
censorshipNotes: ""
wordCount: 0
wordCountEdition: ""
relatedWorks:
  - id: ""
    relationshipType: ""
notes: ""

# ── Identifiers ──────────────────────────────────────────────
identifiers:
  wikidata: ""
  openLibrary: ""
  goodreads: ""
  librarything: ""
  gutenberg: []
  internetArchive: []
  lccn: ""
  oclc: []
  viaf: ""
  bnf: ""
  jubileeEdition:
    volumes: ""
    notes: ""

# ── Field Sources ─────────────────────────────────────────────
# Maps field names to source IDs from sources.yaml
fieldSources:
  id:
    - sourceId: ""
      page: ""
      quote: ""
      notes: ""
