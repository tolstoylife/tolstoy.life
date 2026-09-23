---
layer: reference
lastUpdated: 2026-05-11
tags: [research]
---

# PSS Tom number → local PDF file mapping

> Companion to the [Jubilee Edition + tolstoydigital TEI corpus](jubilee-edition-tei-corpus/) reference dive, which tells the edition's history and the structure of the collections. This file remains the canonical Tom-number ↔ local-PDF resolver.

Date: 2026-05-10
Context: The local copies of the Jubilee Edition (*Полное собрание сочинений*, PSS) at `primary-sources/jubilee-edition/volNN/volNN.pdf` are named in the **chronological publication order of the 90-volume project (1928–1958)**, not by Tom number. This document is the lookup table that resolves a Tom number cited in scholarly literature or in the tolstoydigital TEI corpus to the local PDF file that contains it.

The TEI files in `primary-sources/tolstoydigital-TEI/texts/` use filenames of the form `vNN_NNN_*.xml` where `NN` is the **Tom number**. The local PDFs use `volNN` where `NN` is the **publication-order index**. They are not the same number.

---

## How the mapping was built

For each `volNN/volNN.pdf` the auto-generated cover page from the *Весь Толстой в один клик* (All Tolstoy in One Click) digitisation project carries a header reading `Полное собрание сочинений. Том NN.` which gives the canonical Tom number. A bulk scan with `pdftotext -l 4` and a regex against this header produced 88 of 90 entries directly. Two volumes (vol33 and vol52) lacked the cover header on the first pages but were resolved from the body text of the editorial preface or front matter. One Tom (Tom 31) is still unresolved at the time of writing — see TODO at the end.

---

## Lookup table

The 90-volume Jubilee Edition (PSS) is divided by the [tolstoy-jubilee-edition-guide.pdf](../../primary-sources/jubilee-edition/tolstoy-jubilee-edition-guide.pdf) into three parts plus a supplementary volume:

- Part 1 — Fiction and essays (Tom 1–45)
- Part 2 — Diaries and notebooks (Tom 46–57)
- Part 3 — Letters (Tom 58–89)
- Tom 90 — Miscellaneous and supplementary material
- Tom 91 — Indexes (1964 supplement)

The local file numbering reflects publication-order, which loosely tracks Tom number for the main run and then jumps for the loose-end volumes published last.

| Tom | Local PDF | Tom | Local PDF | Tom | Local PDF |
| --- | --- | --- | --- | --- | --- |
| Tom 1 | vol62 | Tom 32 | vol01 | Tom 63 | vol29 |
| Tom 2 | vol63 | Tom 33 | vol02 | Tom 64 | vol30 |
| Tom 3 | vol64 | Tom 34 | vol03 | Tom 65 | vol31 |
| Tom 4 | vol65 | Tom 35 | vol04 | Tom 66 | vol32 |
| Tom 5 | vol66 | Tom 36 | vol05 | Tom 67 | vol33 |
| Tom 6 | vol67 | Tom 37 | vol06 | Tom 68 | vol34 |
| Tom 7 | vol68 | Tom 38 | vol07 | Tom 69 | vol52 |
| Tom 8 | vol69 | Tom 39 | vol08 | Tom 70 | vol35 |
| Tom 9 | vol70 | Tom 40 | vol49 | Tom 71 | vol53 |
| Tom 10 | vol71 | Tom 41 | vol09 | Tom 72 | vol36 |
| Tom 11 | vol72 | Tom 42 | vol10 | Tom 73 | vol37 |
| Tom 12 | vol73 | Tom 43 | vol11 | Tom 74 | vol54 |
| Tom 13 | vol74 | Tom 44 | vol12 | Tom 75 | vol38 |
| Tom 14 | vol75 | Tom 45 | vol13 | Tom 76 | vol55 |
| Tom 15 | vol76 | Tom 46 | vol14 | Tom 77 | vol39 |
| Tom 16 | vol61 | Tom 47 | vol15 | Tom 78 | vol56 |
| Tom 17 | vol77 | Tom 48 | vol16 | Tom 79 | vol40 |
| Tom 18 | vol78 | Tom 49 | vol50 | Tom 80 | vol57 |
| Tom 19 | vol79 | Tom 50 | vol17 | Tom 81 | vol41 |
| Tom 20 | vol80 | Tom 51 | vol51 | Tom 82 | vol58 |
| Tom 21 | vol81 | Tom 52 | vol18 | Tom 83 | vol42 |
| Tom 22 | vol82 | **Tom 53** | **vol19** | Tom 84 | vol43 |
| Tom 23 | vol83 | Tom 54 | vol20 | Tom 85 | vol44 |
| Tom 24 | vol84 | Tom 55 | vol21 | Tom 86 | vol45 |
| Tom 25 | vol85 | Tom 56 | vol22 | Tom 87 | vol46 |
| Tom 26 | vol86 | Tom 57 | vol23 | Tom 88 | vol47 |
| Tom 27 | vol87 | Tom 58 | vol24 | Tom 89 | vol59 |
| Tom 28 | vol88 | Tom 59 | vol25 | Tom 90 | vol48 |
| Tom 29 | vol89 | Tom 60 | vol26 | Tom 91 | vol60 |
| Tom 30 | vol90 | Tom 61 | vol27 | | |
| (Tom 31 — see TODO) | | Tom 62 | vol28 | | |

The bolded row marks **Tom 53 → vol19**, the diaries 1895–1899 volume that contains the 27 March 1895 will-as-diary-entry referenced in [the copyright-renunciation research](../copyright-renunciation/).

---

## Examples of use

To find the printed page that corresponds to a TEI letter file:

```sh
# TEI: letters/v66_036_RedaktoramgazetRusskievedomosti.xml
# bibl: ...Полное собрание сочинений: в 90 тт. Т. 66. ... С. 47–48.
# Tom 66 → vol32

pdftoppm -r 220 -f 50 -l 60 -png \
  primary-sources/jubilee-edition/vol32/vol32.pdf \
  /tmp/page
# (The TEI bibl gives the printed page range — use it to find which PDF page to extract.)
```

To find which Tom a local file actually contains, inspect the auto-generated cover header:

```sh
pdftotext -l 2 primary-sources/jubilee-edition/vol19/vol19.pdf - | head
# Полное собрание сочинений. Том 53.
# Дневники и записные книжки 1895–1899
```

---

## TODO

- **Tom 31 unresolved.** A first-pages scan of all 90 PDFs did not return a `Том 31` header. Two possibilities: (a) the local PDF for Tom 31 has a different cover format that the regex missed, (b) Tom 31 is held at a publication-order index whose first pages start with content rather than the standard cover. A targeted page-by-page scan or visual inspection would resolve it. Recorded here so it does not get lost.
- **Promote to a script.** This mapping is currently a static markdown table. A small `tools/pss-volume.py` that takes a Tom number and returns the local PDF path (or vice versa) would make round-trip lookups trivial during research sessions. Generation script could re-derive the table from the cover headers each run, so the mapping stays correct if the local PDF set is replaced.
- **Verify Tom 47 attribution.** The Jubilee Edition guide flags Tom 47 (diaries and notebooks) as the most extensively commented volume in the entire PSS — worth annotating that here when the script lands.
