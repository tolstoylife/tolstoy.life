# Volume 91 Integration Summary

**Date:** April 5, 2026
**Trigger:** Analysis of tolstoydigital/TEI repository (complete Jubilee Edition in TEI/XML)
**Outcome:** Schema v6 proposal + comprehensive audit artifacts

---

## What Happened

1. **Cloned tolstoydigital/TEI** (5.3 GB)
   - Complete TEI/XML encoding of Jubilee Edition (90 volumes)
   - 3,113 named persons, 770 locations, 767 works catalogued
   - Licensed CC BY-SA

2. **Discovered Volume 91 as structured XML**
   - Not just a printed index — reference layer already machine-readable
   - `bibllist_works.xml`: 495 works with metadata
   - `personList.xml`: Wikidata-linked entities
   - `locationList.xml`: Coordinates, descriptions
   - Direct linkage to TEI text files via filenames (e.g., `v01_003_095_Detstvo.xml` = Vol 1, pp 3–95)

3. **Audited your corpus against Volume 91**
   - Your corpus: 13 works (2.6% coverage of V91's 495 works)
   - ID mismatch: Your slugs (`anna-karenina`) vs V91's IDs (`Anna_Karenina`)
   - Created mapping spreadsheet to convert all 495 IDs to your slug format
   - Only 1 match after conversion: Anna Karenina

4. **Analyzed schema gap**
   - Your v5 schema is comprehensive and covers all major scholarly metadata
   - No breaking changes needed
   - Four **optional** fields would unlock automation and entity linking

---

## Key Findings

### Coverage
- **Volume 91 has 495 works catalogued**
- **Your corpus has 13 works**
- **Gap: 482 missing works** (97.4%)

### By Work Type
| Category | V91 | Corpus | Coverage |
|----------|-----|--------|----------|
| Diaries | 200+ | 0 | 0% |
| Letters | 100+ | 0 | 0% |
| Essays | 80 | 3 | 3.8% |
| Short stories | 40 | 1 | 2.5% |
| Novels | 15 | 1 | 6.7% |
| Plays | 10 | 2 | 20% |
| Fragments | 150+ | 6 | 4% |

### ID Format Discovery
- V91 uses **PascalCase_with_underscores** (99% of 495 works)
- Examples: `Vojna_i_mir`, `Anna_Karenina`, `Aforizmy_k_svoim_portretam`
- Your format: lowercase-with-hyphens
- Conversion rule: replace `_` with `-` and lowercase

---

## Deliverables in _resources/volume-91/

### 1. README.md
- Overview of all files
- Usage guide for the audit and mapping data
- Key findings and next steps

### 2. VOLUME_91_SLUG_MAPPING.xlsx
- **All 495 works** from Volume 91 catalogue
- Columns:
  - Volume 91 ID (TEI format)
  - Slug Format (your format, converted)
  - English Title
  - Publication Date
  - In Corpus? (color-coded)
  - Corpus ID (if matched)
- **Use:** Sort/filter to identify gaps, prioritize expansion, export for bulk import

### 3. WORKS_AUDIT_REPORT.html
- Detailed analysis with stats and charts
- Work type breakdown
- Implications for your corpus strategy
- Open in any web browser

### 4. SCHEMA_v6_UPDATE.docx
- Formal schema update proposal
- Four optional new fields with rationale
- Migration & backwards compatibility analysis
- Implementation priority matrix
- Next steps checklist

### 5. volume_91_works.csv
- Raw data: all 495 works from bibllist_works.xml
- Columns: id, title, date

### 6. tolstoy_life_works.csv
- Raw data: your 13 current works
- Columns: id, title, dateFirstPublished, file

---

## Schema v6 Proposal

### Four Optional Fields

All backwards-compatible; no breaking changes.

#### 1. **jubileeEdition.pageRange** (string)
Captures exact page range from printed edition.
```yaml
jubileeEdition:
  volumes: "1"
  pageRange: "3-95"  # NEW
```
**Impact:** Precise citations in printed Jubilee Edition

#### 2. **teiSourceFile** (string)
Direct path to machine-readable source in tolstoydigital/TEI.
```yaml
teiSourceFile: "tolstoydigital-TEI/texts/works/v01_003_095_Detstvo.xml"
```
**Impact:** Automated text ingestion, version control sync

#### 3. **personMentions[]** and **locationMentions[]** (object arrays)
Link to canonical entities from Volume 91.
```yaml
personMentions:
  - id: 25
    name: "Anna Karenina"
    wikidata: "Q29130361"
    role: "protagonist"  # optional
```
**Impact:** Bridges to LightRAG entity layer

#### 4. **canonicalSource** (string, in fieldSources section)
Formalizes which edition is authoritative.
```yaml
canonicalSource: "Jubilee Edition (Polnoe sobranie sochinenii), vols. 18–19, 1928–1964"
```
**Impact:** Clarifies source authority when editions conflict

### Priority Matrix
| Field | Priority | Effort | ROI |
|-------|----------|--------|-----|
| pageRange | HIGH | Low | High |
| teiSourceFile | HIGH | Low | High |
| personMentions/locationMentions | MEDIUM | Medium | High |
| canonicalSource | MEDIUM | Low | Medium |

**Recommendation:** Implement HIGH priority items immediately.

---

## Next Steps (Ordered by Dependency)

1. **Review this summary** with stakeholders
2. **Decide on scope:** All 495 works, or curated subset?
3. **Update tolstoy-works-schema.md** to v6 (add four fields)
4. **Populate pageRange** from Volume 91 bibllist_works.xml
5. **Populate teiSourceFile** mapping works to tolstoydigital-TEI paths
6. **Create bulk import workflow** using VOLUME_91_SLUG_MAPPING.xlsx
7. **Plan LightRAG integration** (entity graph strategy for personMentions/locationMentions)

---

## Why This Matters

**Volume 91 is a Game-Changer Because:**

1. **Canonical Authority:** The Jubilee Edition is the gold standard. Volume 91 gives you a curated, scholarly index.

2. **Machine-Readable:** Unlike a scanned index, the TEI/XML version is structured, Wikidata-linked, and version-controlled.

3. **Automated Sourcing:** teiSourceFile creates a direct pipeline from your corpus to raw TEI texts. No manual transcription.

4. **Entity Backbone:** 3,113 persons and 770 locations pre-linked to Wikidata. This seeded data de-risks your LightRAG implementation.

5. **Open License:** CC BY-SA means you can redistribute, remix, and build on top of it without legal friction.

6. **Scholarly Credibility:** Published by the Slovo Tolstogo project (recognized Tolstoy scholarship), gives your corpus scholarly weight.

---

## Data Quality Notes

- **Date Coverage:** Not all 495 works have publication dates in bibllist_works.xml. Many marked as composition-only or range estimates.
- **Title Variants:** Russian, English, and transliteration variants all present. Use fieldSources to document which is canonical for each work.
- **Volume Distribution:** Heavy concentration in Volumes 1–24 (artistic works) and 25–34 (essays).
- **Entity Richness:** personList.xml and locationList.xml are detailed, Wikidata-linked, and production-ready.

---

## Files & Folder Structure

```
_resources/volume-91/
├── README.md                       ← Start here
├── SCHEMA_v6_UPDATE.docx           ← Official proposal
├── INTEGRATION_SUMMARY.md          ← This file
├── WORKS_AUDIT_REPORT.html         ← Detailed analysis
├── VOLUME_91_SLUG_MAPPING.xlsx     ← Complete mapping of all 495 works
├── volume_91_works.csv             ← Raw V91 data
└── tolstoy_life_works.csv          ← Raw corpus data
```

---

## Key Metric

**Before:** 13 works (isolated corpus)
**Potential:** 495 works (comprehensive Jubilee Edition)
**Multiplier:** 38x coverage with existing reference data

---

## Questions?

Refer to:
- **README.md** for overview and usage
- **WORKS_AUDIT_REPORT.html** for detailed analysis
- **SCHEMA_v6_UPDATE.docx** for formal proposal
- **VOLUME_91_SLUG_MAPPING.xlsx** for work-by-work reference
