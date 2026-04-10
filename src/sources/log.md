# Wiki Operations Log

## [2026-04-07] ingest | pg27189.txt — *Bethink Yourselves!* (1904)

**Source:** [[Bethink Yourselves — Project Gutenberg]] (`src/_staging/pg27189.txt` → binary also in `primary-sources/works/non-fiction/essays/bethink-yourselves/`)
**Pages created:** [[Bethink Yourselves!]] (work overview + frontmatter), [[Bethink Yourselves — Project Gutenberg]] (source card)
**Pages updated:** none

**Text overview:** Anti-war essay in 12 numbered sections, written at [[Yasnaya Polyana]] in May 1904 during the Russo-Japanese War. Two internal composition dates (OS "May 2" = NS May 15; OS "May 13" = NS May 26). Translated by [[Vladimir Chertkov]] and "I. F. M."; first published in *The Times*, London; republished as pamphlet by Ginn & Company for the International Union (Boston, 1904). Not legally published in Russia during Tolstoy's lifetime.

**Key content points ingested:**
- Moral argument: every individual — soldier, officer, journalist, Tsar — evades the personal question of complicity by appealing to abstract collective duty (fatherland, faith, oath)
- Core prescription: "bethink yourselves" — interrupt activity, ask who you are and what your destiny is; the only realistic path to ending war is individual moral conscience, not political institutions
- Section XI: attack on Tsar Nicholas II and General Kuropatkin by name; estimates 50,000+ Russian deaths; "inexhaustible human material" formulation
- Section XII: two letters — reservist who promises "through me not one Japanese family shall be orphaned"; a seaman asking if God loves war; an encounter with a reservist on the road who says "where can one escape?"
- Epigraph: Luke xxii.53 ("This is your hour, and the power of darkness")
- Cites Dukhobors and other conscientious objectors as exemplary

**Date conversion:** Section XI date OS "May 2, 1904" = NS 1904-05-15; section XII date OS "13 May, 1904" = NS 1904-05-26. Both post-1900 pre-1918 → +13 days. Recorded `dateWritingCompleted` as NS 1904-05-13 (the OS date given at end of main body, before addendum).

**Jubilee Edition:** Vol. 36 (covers publicistic writings 1904–06). Specific page range not yet verified from the actual volume.

**Open questions:**
- Russian original title confirmed as «Одумайтесь!» — but the exact first Russian publication date is unknown. The work circulated via Chertkov's London channels. When was it first legally printed in Russia?
- Wikidata QID not yet added — should be looked up.
- The co-translator "I. F. M." is unidentified in the PG source. Could be Isabel F. Mayo? Needs verification.

## [2026-04-07] ingest | TEI Reference Data — LT's children (6 pages)

**Source:** [[TEI Reference Data]] (`corpus/data/unprocessed/tolstoydigital-TEI/reference/personList.xml`)
**Pages created:** [[Sergei Tolstoy]], [[Tatyana Tolstaya]], [[Lev Lvovich Tolstoy]], [[Maria Tolstaya]], [[Andrei Tolstoy]], [[Alexandra Tolstaya]]
**Pages updated:** [[Leo Tolstoy]] (added 6 children to relatedArticles), [[Sophia Tolstaya]] (added 6 children to relatedArticles)

**Date conversion note:** Pre-1900 OS dates +12 days (Sergei, Tatyana, Lev, Maria, Andrei birth dates); Andrei's 1916 death date is post-1900 pre-1918, so +13 days applied to OS date.

**Missing from TEI:** Ilya Lvovich Tolstoy (b. 1866) and Mikhail Lvovich Tolstoy (b. 1879) are not present in personList.xml as children of LT — TEI has an "Ilya Andreeevich" (a different Tolstoy) but not Ilya Lvovich. Both will need pages sourced from Birukoff biography.

**Data gaps:**
- Maria Tolstaya: no specific born/died dates in TEI (life period only: 1871–1906). Exact dates to be sourced from Birukoff.
- Sergei Tolstoy, Lev Lvovich, Andrei Tolstoy: birthplace stated as Yasnaya Polyana by convention — not confirmed by TEI, which gives no birthPlace field. Should be verified.
- Alexandra Tolstaya's deathPlace (Valley Cottage, NY) sourced from general knowledge, not TEI. Should be confirmed.

**Open questions:**
- Tatyana Tolstaya married Mikhail Suhótin — TEI records her under her married name. The wiki page uses her birth name as the primary title; this should be consistent with how she appears in citations.
- Two children (Ilya, Mikhail) still lack pages. Add to next batch.

**Next:** Add Ilya Lvovich Tolstoy and Mikhail Lvovich Tolstoy from Birukoff biography. Then ingest key locations (Moscow Khamovniki house, Optina Pustyn, Shamordino).

## [2026-04-06] ingest | TEI Reference Data — test run (5 entities)

**Source:** [[TEI Reference Data]] (`corpus/data/unprocessed/tolstoydigital-TEI/reference/`)
**Pages created:** [[Sophia Tolstaya]], [[Vladimir Chertkov]], [[Pavel Birukoff]], [[Yasnaya Polyana]], [[Astapovo]]
**Pages updated:** [[Leo Tolstoy]] (frontmatter migrated to new wiki-schema person template; legacy zone marker removed)

**Date conversion note:** All dates in personList.xml are Old Style (Julian). Applied +12 days to pre-1900 dates and +13 days to post-1900 dates for NS (Gregorian) canonical values. OS values recorded in `...OldStyle` companion fields.

**Open questions:**
- Aylmer Maude is not in personList.xml as a standalone entry. Will need to create his wiki page from a different source (Maude biography or Standard Ebooks metadata).
- The TEI person descriptions are in Russian only. English prose for wiki articles is synthesised from the Russian descriptions + general knowledge. These should be verified against primary sources (Jubilee Edition, Birukoff biography) before `recordStatus` is raised from `draft` to `reviewed`.
- locationList.xml description for Yasnaya Polyana uses "1847" for when Tolstoy inherited the estate — cross-check against Birukoff.

**Next:** Continue tiered ingestion of TEI persons. Suggested next batch: LT's children (Tatyana, Ilya, Lev, Maria, Andrei, Mikhail, Alexandra) + key locations (Moscow house on Khamovniki Lane, Optina Pustyn, Shamordino).
