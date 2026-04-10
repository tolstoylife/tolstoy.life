---
id: tei-reference-data
type: source
titleEn: "tolstoydigital TEI Reference Data"
titleRu: "Цифровой Толстой — справочные данные TEI"
author: "Anastasiya Bonch-Osmolovskaya, Fyokla Tolstaya, Boris Orekhov et al."
publicationDate: "2015–2025"
language: ru
format: xml
binaryPath: "corpus/data/unprocessed/tolstoydigital-TEI/reference/"
license: "CC BY-SA"
ingestionStatus: partial
ingestionDate: "2026-04-06"
pagesCreated:
  - sophia-tolstaya
  - vladimir-chertkov
  - pavel-birukoff
  - yasnaya-polyana
  - astapovo
pagesUpdated:
  - leo-tolstoy
notes: "Test run with 3 persons + 2 places from the inner circle. Full dataset: 3,113 persons, 770 locations. personList.xml and locationList.xml have Wikidata QIDs, birth/death dates, categories, and Russian descriptions. Location entries have lat/lon coordinates and narrative descriptions. Aylmer Maude not present as a dedicated entry — appears only in notes."
---

Structured reference data compiled by the tolstoydigital project (НИУ ВШЭ / HSE University, Moscow) accompanying the digital edition of Tolstoy's Complete Works in 90 volumes.

Contains:
- **personList.xml** — 3,113 persons connected to Tolstoy's life and works. Each entry includes Wikidata QID, birth/death dates, Russian description, and occupation/relationship categories.
- **locationList.xml** — 770 locations associated with Tolstoy. Each entry includes geographic coordinates, Russian place name, and a narrative description of Tolstoy's connection to the place.
- **worksList.xml** — 767 works in the Jubilee Edition.

License: Creative Commons Attribution Share-Alike (CC BY-SA). Original data at tolstoydigital.ru.

## Ingestion notes

### 2026-04-06 — Test run (5 entities)

First ingestion pass using the LLM Wiki model. Selected 3 persons from Tolstoy's immediate circle and 2 key locations.

Persons extracted: [[Sophia Tolstaya]], [[Vladimir Chertkov]], [[Pavel Birukoff]]. Updated: [[Leo Tolstoy]].
Locations extracted: [[Yasnaya Polyana]], [[Astapovo]].

The TEI date format uses Old Style (Julian) dates for pre-1918 Russian dates — all dates in this source are OS and require +12 or +13 days conversion to NS (Gregorian). Confirmed: Sophia Tolstaya born OS 1844-08-22 = NS 1844-09-03.
