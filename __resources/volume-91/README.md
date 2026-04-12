# Volume 91 Analysis & Mapping

This folder contains audit artifacts and mapping data derived from the Jubilee Edition Volume 91 (the index volume) and the tolstoydigital/TEI repository.

## Files

### VOLUME_91_SLUG_MAPPING.xlsx
**Primary reference for work ID mapping**

A comprehensive mapping spreadsheet containing all 495 works from the Jubilee Edition with:
- **Column A**: Volume 91 ID (TEI format) — e.g., `Vojna_i_mir`, `Anna_Karenina`
- **Column B**: Slug Format (your format) — e.g., `vojna-i-mir`, `anna-karenina`
- **Column C**: English Title — Full title as catalogued
- **Column D**: Publication Date — From Volume 91 metadata
- **Column E**: In Corpus? — Color-coded (green = yes, red = no)
- **Column F**: Corpus ID — Your project's ID if it exists

**Use cases:**
- Identify which works are missing from your corpus
- Map between Volume 91 IDs and your slug format
- Prioritize works to add (sort by date, genre category, etc.)
- Export to CSV for bulk import workflows

**Current coverage:** 1/495 works matched (Anna Karenina)

### WORKS_AUDIT_REPORT.html
**Detailed analysis and recommendations**

A formatted HTML report containing:
- Summary statistics (total works, coverage %, gaps)
- Detailed comparison of Volume 91 catalogue vs tolstoy-life corpus
- Gap analysis broken down by work type (novels, diaries, letters, essays, plays, etc.)
- Content audit table showing % coverage by category
- Implications and recommended next steps

**Read in any web browser.** Useful for stakeholder communication and understanding the scope of the project.

### volume_91_works.csv
**Raw data: all 495 works from bibllist_works.xml**

Three columns:
- `id`: Volume 91 ID (TEI format)
- `title`: English title as catalogued
- `date`: Publication/composition date (may be empty for some works)

**Use for:** Data processing, filtering, bulk imports

### tolstoy_life_works.csv
**Raw data: your current 13 works**

Four columns:
- `id`: Your slug format ID
- `title`: Work title
- `dateFirstPublished`: Publication date (if available)
- `file`: Path to the markdown file in tolstoy-life project

**Use for:** Comparison, validation, cross-referencing

## Key Findings

- **Total works in Volume 91**: 495
- **Total works in tolstoy-life**: 13
- **Coverage**: 2.6%
- **ID matching**: 0% initially, because your corpus uses slugified IDs and Volume 91 uses PascalCase_with_underscores
- **First match after slug conversion**: 1 (Anna Karenina)

### Work Type Breakdown (by V91 catalogue)

| Category | Count | Your Coverage |
|----------|-------|---|
| Diaries | 200+ | 0% |
| Letters & Correspondence | 100+ | 0% |
| Essays & Philosophy | 80 | 3.8% (3 works) |
| Fragments & Sketches | 150+ | 4% |
| Short Stories & Novellas | 40 | 2.5% (1 work) |
| Plays | 10 | 20% (2 works) |
| Major Novels | 15 | 6.7% (1 work) |

## How to Use This Data

### 1. Identify High-Priority Gaps
Sort the mapping spreadsheet by:
- **By date** to prioritize canonical early works
- **By category** (use title keywords) to focus on specific genres
- **By "In Corpus?" column** to highlight what's missing

### 2. Create Work Records
Use Column B (slug format) as templates for creating new work IDs in your project. Use Column C and D (title and date) to populate YAML frontmatter.

### 3. Cross-Link to TEI Source
The Volume 91 ID (Column A) corresponds to files in `tolstoydigital-TEI/texts/works/`. For example:
- Volume 91 ID: `Vojna_i_mir`
- TEI file: `tolstoydigital-TEI/texts/works/v01_003_095_Detstvo.xml` (for Childhood)
- Or search the TEI repo for the matching work

### 4. Validate Dates and Metadata
The mapping provides canonical publication dates from the Jubilee Edition. Validate these against your corpus records and update where necessary.

## Related Resources

- **tolstoydigital/TEI repo**: `corpus/data/unprocessed/tolstoydigital-TEI/`
  - Full TEI/XML texts of all 90 volumes
  - Reference layer: `reference/bibllist_works.xml` (495 works catalogue)
  - Reference layer: `reference/personList.xml` (3,113 persons)
  - Reference layer: `reference/locationList.xml` (770 locations)

- **CLAUDE.md**: Project-level documentation at project root

## Next Steps

1. Review WORKS_AUDIT_REPORT.html for strategic overview
2. Use VOLUME_91_SLUG_MAPPING.xlsx to plan expansion strategy
3. Decide on scope: all 495 works, or a curated subset?
4. Prioritize work type(s) to add next
5. Create bulk import workflow using the slug mapping and TEI source files

## Generated

April 5, 2026

---

**Note**: All Volume 91 data is licensed CC BY-SA from the Slovo Tolstogo project (Orekhov, Tolstaya, Bonch-Osmolovskaya, Lukashevsky et al., 2015–2022).
