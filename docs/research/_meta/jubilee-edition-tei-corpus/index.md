---
layer: reference
lastUpdated: 2026-05-30
tags: [research]
---

# The Jubilee Edition and the tolstoydigital TEI/XML corpus

Date: 2026-05-30

Context: A reference dive on the two artifacts the platform's Russian-language text rests on — the printed **Jubilee Edition** (*Полное собрание сочинений*, the "PSS": 90 volumes, 1928–1958, plus a 1964 index volume) and the **tolstoydigital TEI/XML corpus** that digitised and semantically encoded it. It covers the history (who made each, why, and under what constraints), the structure of the collections (the TEI document model, the reference files, the genre breakdown), and exactly what tolstoy.life holds locally.

This dive consolidates and supersedes two earlier loose notes — `tolstoydigital-tei-reference.md` and `pss-volume-mapping.md` — which now point here. Unlike a thematic corpus-dive, the cited "evidence" is the corpus and edition *metadata itself* (TEI headers, the printed front matter, the reference files), each quotation byte-faithful from the local source.

---

## 1. Key findings

- **Two layers, one lineage.** A printed scholarly edition (90 vols, 1928–1958) and a digital TEI/XML edition (encoded 2015–2022) that re-publishes it with semantic markup. The data chain is: print PSS → scans from the Russian State Library → crowdsourced OCR + proofreading (2013–14) → free e-texts on tolstoy.ru → TEI/XML + semantic layers by Tolstoy Digital → `github.com/tolstoydigital/TEI` (CC BY-SA).
- **The edition was a Soviet-state project entrusted to Tolstoy's disciple.** Authorised by a Sovnarkom resolution of 23 June 1925 (not a ЦИК decree, as English summaries imply), it made **V. G. Chertkov editor-in-chief** — "that friend of the deceased writer whom he himself chose." Its founding principle was maximalist: reproduce *absolutely everything* Tolstoy wrote.
- **The edition carries its own free-reproduction notice.** Tom 1 prints «Перепечатка разрешается безвозмездно» / «Reproduction libre pour tous les pays» — a direct echo of Tolstoy's own renunciation of copyright, and the textual root of why this corpus is openly reusable today.
- **It is honest about its constraints.** The State Editorial Commission's preface openly reserves a right of omission — the Soviet-era editorial limit, stated in the edition's own front matter.
- **Print run: originally 5,000, raised to 10,000 (1934).** Never reprinted as a set, it became a bibliographic rarity — the motive for the 2010s digitisation.
- **The digital corpus is large and structured.** Locally: **16,573 TEI files** (works 767 · letters 9,087 · diaries 4,584 · notes 100 · krug_chtenija 444 · azbuka 784 · comments 807), mirrored 1:1 by a `texts_front/` display variant, plus a witness corpus (Gusev, Goldenweiser, Makovitski, S. A. Tolstaya). The reference layer is **3,113 persons**, **385 places**, work/bio bibliographies, a 125-category taxonomy, a rare-word dictionary, and a museum-photo catalogue.
- **Each person links out to Wikidata; the licence lives in the header.** persName carries a Wikidata Q-id — the corpus's one external authority anchor. The CC BY-SA grant is declared in the TEI header's `<availability>`, **not** as a repo LICENSE file.
- **For the vault.** The corpus is the structured source behind `website/src/wiki/` (persons, places) and `website/src/works/` (the work catalogue). This dive maps the people and institutions behind the edition as wiki-ingestion candidates and flags two schema gaps (no "edition" type; the corpus is not yet a registered source).

---

## 2. Why this matters for tolstoy.life

Almost every Russian-language string on tolstoy.life ultimately derives from these two artifacts. The wiki's persons and places come from the corpus's reference files; the works catalogue comes from its bibliography; the citation under a quotation ("PSS, Tom X, pp. Y") points at the printed edition. Knowing what the corpus *is* — how it was made, what it encodes, where it is reliable and where it is not — is therefore foundational rather than incidental.

It also matters for the platform's licence. tolstoy.life gives all its text away; the printed edition it builds on did the same, in 1935, on its own copyright page. Grounding the platform's openness in that lineage — Tolstoy's renunciation, the edition's free-reproduction notice, the corpus's CC BY-SA — is one of this dive's purposes.

A companion table, the Tom-number → local-PDF map, is preserved in [pss-volume-mapping.md](../pss-volume-mapping.md); the earlier corpus note is [tolstoydigital-tei-reference.md](../tolstoydigital-tei-reference.md).

---

## 3. The printed edition: history

### 3.1. What it is, and why "Jubilee"

The *Полное собрание сочинений* (Complete Collected Works) is the definitive scholarly edition of everything Tolstoy wrote — final and draft literary texts, essays, pedagogy, plays, diaries, notebooks, and letters — across **90 volumes of roughly 46,000 pages**, about half of them correspondence and personal papers. It is called the **Jubilee Edition** (Юбилейное издание) because it was conceived around, and its first volume issued near, **1928 — the centenary of Tolstoy's birth (1828)**.

The print run is best stated as **originally 5,000 copies, raised to 10,000** by a later resolution (1934), with per-volume variation. It was never reprinted as a set, which is why, by the 2010s, it had become a bibliographic rarity held mainly in research libraries.

### 3.2. The Soviet authorisation

The edition was a state project. English-language summaries compress its authorisation to "Lenin's affidavit (1918)" and a Stalin-era "state decree"; the documentary record (Osterman, 2000) is more precise: Lenin gave his *support* in 1918, but the decisive founding act was a **resolution of the Sovnarkom (Council of People's Commissars) of the RSFSR dated 23 June 1925**, allocating funds to the complete jubilee edition; a further Sovnarkom resolution of 8 August 1934 revived the stalled project and raised the print run. The imprint moved with the reorganisations of Soviet publishing — from **Госиздат (GIZ)** to **Государственное издательство «Художественная литература» (ГИХЛ / Гослитиздат)** — which is why the title pages read "Государственное издательство «Художественная литература»".

The edition's own front matter says this plainly. The State Editorial Commission's preface to Tom 1 records that the Soviet government entrusted the editing to the friend Tolstoy himself had chosen:

> Приступая к изданию собрания сочинений Л. Н . Толстого, Советское правительство признало необходимым обеспечить совершенно полное и объективное издание этих сочинений, поручив непосредственную работу по редактированию тому другу покойного писателя, которого он сам выбрал для этой цели…

> *Setting about the edition of the works of L. N. Tolstoy, the Soviet government recognised it necessary to ensure a completely full and objective edition of these works, entrusting the direct work of editing to that friend of the deceased writer whom he himself chose for this purpose…* (working English)

<figure>
<img src="extracts/pss-vol62-pages/page-005.png" alt="Facsimile: the State Editorial Commission preface, PSS Tom 1">
<figcaption>«ОТ ГОСУДАРСТВЕННОЙ РЕДАКЦИОННОЙ КОМИССИИ» — the State Editorial Commission's preface, PSS Tom 1 (1935). Public domain; rendered from the local PSS PDF.</figcaption>
</figure>

### 3.3. Chertkov and the editorial board

The friend was **Vladimir Grigoryevich Chertkov** (1854–1936), Tolstoy's closest [disciple](../tolstoyanism/index.html) and the keeper of his manuscripts, who served as **editor-in-chief (главный редактор)**. His own foreword to Tom 1 grounds the edition in Tolstoy's last wishes:

> Это же самое желание он затем подтвердил письменно в своем завещательном распоряжении от 31 июля 1910 г.

> *This same wish he then confirmed in writing in his testamentary disposition of 31 July 1910.* (working English)

That is the very document the platform's [copyright-renunciation dive](../copyright-renunciation/index.html) centres on — the edition descends directly from Tolstoy's renunciation of literary property. Chertkov died in 1936, mid-project; the work passed to N. S. Rodionov. The editorial board of Tolstoy scholars included **N. N. Gusev** (Tolstoy's secretary), **A. E. Gruzinsky**, **N. K. Gudzy**, **M. A. Tsyavlovsky**, **N. K. Piksanov**, and **A. L. Tolstaya** (Tolstoy's daughter and manuscript heir, before her emigration).

<figure>
<img src="visuals/commons-chertkov-portrait-repin.jpg" alt="Portrait of V. G. Chertkov by Ilya Repin, c. 1890">
<figcaption>V. G. Chertkov, editor-in-chief of the Jubilee Edition. Portrait by Ilya Repin, c. 1890. Public domain (Wikimedia Commons).</figcaption>
</figure>

### 3.4. Editorial principles and textology

The edition's governing credo was **completeness without exception**. Chertkov's foreword states it directly:

> Лев Николаевич никак не предполагал, что будет опубликовано все, что он когда-либо написал. А между тем … нам в настоящем издании приходится именно в таком полном виде воспроизводить решительно все, написанное Толстым.

> *Lev Nikolaevich never supposed that everything he ever wrote would be published. And yet … in the present edition we have to reproduce, in exactly such complete form, absolutely everything written by Tolstoy.* (working English)

Each text was established from Tolstoy's manuscript legacy (≈3,000 sources), presented in its canonical last-authorial form **plus variants and redactions (варианты, редакции)** and an extensive scholarly apparatus — introductions, textual histories, commentary. The depth of that apparatus varies sharply by volume: the *War and Peace* drafts (Tom 13) are comparatively bare, whereas the diary/notebook volumes (notably Tom 47) are the most heavily annotated in the set. This combination — manuscript-grounded text plus full apparatus — is why it remains the standard citation base to this day.

### 3.5. Criticism and Soviet-era constraints

The edition is not naïve about its own limits, and neither should we be. The same State Editorial Commission preface that promised "completeness and objectivity" reserves a right of omission:

> Редакция не может не иметь права делать такого рода пропуски.

> *The editorial board cannot but have the right to make omissions of this kind.* (working English)

The preface frames these as omissions touching living persons; in practice the Soviet apparatus also carried ideological framing (Osterman, 2000, records prefaces "stuffed" with lines about Tolstoy's "reactionariness" over an editor's objection). The characteristic Soviet compromise was *confinement rather than excision*: the banned religious-anarchist works were printed, but only in a small-run academic edition "not for millions of readers." The modern remedy is the 100-volume academic PSS begun in 2000 at the Gorky Institute (IMLI) — its scholarly successor, still in progress.

### 3.6. The shape of the 90 volumes

The edition is tripartite, with volume numbers running chronologically within each group:

| Group | Toma (approx.) | Contents |
| --- | --- | --- |
| Artistic works + essays | 1–45 | Final texts, drafts, and variants of the fiction and the religious-philosophical/pedagogical writing; *War and Peace* variants alone fill four volumes |
| Diaries & notebooks | 46–58 | The diaries from c. 1847 to 1910, plus notebooks; Tom 47 is the most heavily annotated |
| Letters | 58–89 | The largest section — correspondence, by period and recipient |
| Supplementary | 90 | Miscellaneous material |
| Index volume | 91 (1964) | Alphabetical indexes of works, addressees, and >16,000 proper names + a chronological index |

Exact cut-points between groups differ slightly across sources (the project guide, Osterman's plan, and the tolstoy.ru portal filter all draw the lines a little differently) because the plan shifted as volumes were doubled or merged. The robust statement is the tripartite shape and the approximate ranges; for a per-work locator the index volume (and `index.tolstoy.ru`) is authoritative.

---

## 4. The digital chain: from print to TEI

### 4.1. «Весь Толстой в один клик» — All Tolstoy in One Click (2013–2014)

Because the 90 volumes existed only in a small, never-reprinted run, **Fyokla Tolstaya** (Tolstoy's great-great-granddaughter), with the **State L. N. Tolstoy Museum** and **Yasnaya Polyana**, launched a crowdsourcing project in June 2013. **ABBYY** donated FineReader OCR; the scans came from the Russian State Library, as the digital covers record:

> Подготовлено на основе электронной копии 53-го тома Полного собрания сочинений Л. Н. Толстого, предоставленной Российской государственной библиотекой

> *Prepared on the basis of an electronic copy of volume 53 of the Complete Collected Works of L. N. Tolstoy, provided by the Russian State Library.* (working English)

Volunteers proofread 20-page packets via readingtolstoy.ru. The headline result, repeated across the project's sources: **~3,249 volunteers from 49 countries** proofread **46,820 pages (~14.5 million words)** — the initial mass pass in about two weeks, across three review rounds. The output went up free on tolstoy.ru as **761 e-book files** (PDF, EPUB, FB2, MOBI, HTML), fully online by December 2014.

<figure>
<img src="visuals/commons-fyokla-tolstaya.jpg" alt="Fyokla Tolstaya, 2018">
<figcaption>Fyokla Tolstaya, initiator of «Весь Толстой в один клик». Photo by Rodrigo Fernández, 2018 (Wikimedia Commons, CC BY-SA 4.0).</figcaption>
</figure>

### 4.2. «Слово Толстого» / Tolstoy Digital — the TEI encoding (2015–2022)

The free e-texts became the input for a digital-humanities edition. The **Tolstoy Digital** group at the **Higher School of Economics (HSE)**, under the project «Слово Толстого» (Word of Tolstoy), converted the texts to TEI/XML and added a semantic layer. Every file credits the same leadership:

> Анастасия Бонч-Осмоловская, Фёкла Толстая, Борис Орехов, Тимофей Лукашевский

> *Anastasia Bonch-Osmolovskaya, Fyokla Tolstaya, Boris Orekhov, Timofey Lukashevsky* — under "Идея, постановка задач, руководство" (idea, task-setting, leadership). (working English)

The header records the data chain in its own words: the documents were obtained from tolstoy.ru as HTML, converted to TEI, OCR errors fixed, and pre-reform orthography reconciled with modern spelling. The encoding ran 2015–2022; the public site slovotolstogo.ru launched in November 2022. The flagship method paper is Bonch-Osmolovskaya et al., "Tolstoy semanticized" (*Journal of Web Semantics*, 2019). The licence is **CC BY-SA**, declared in the header:

> Тексты и метатекстовая разметка доступны для свободного использования и распространения по лицензии Creative Commons Attribution Share-Alike (cc by-sa)

> *The texts and the metatextual markup are available for free use and distribution under the Creative Commons Attribution Share-Alike (cc by-sa) licence.* (working English)

Note the caveat: this grant lives in the TEI header, not as a repository LICENSE file (GitHub reports the repo licence as "None"), and the build-scripts repo the README points to (`Levabu/tolstoy_digital`) is now a dead link. The corpus itself is at `github.com/tolstoydigital/TEI`.

### 4.3. The "91st volume" web application

The 1964 index volume was separately digitised as a web app at **index.tolstoy.ru** (Orekhov, 2020): it preserves the index-of-names function and adds fuzzy search, a >16,000-name list, frequency heatmaps, and a **co-occurrence network graph** — two names appearing on the same printed page become a graph edge, surfacing Tolstoy's documented social network. Built 2016–2017 by HSE and the Tolstoy Museum.

---

## 5. The structure of the collections

This is the structural anatomy of the local TEI clone (`primary-sources/tolstoydigital-TEI/`).

### 5.1. Directory layout

| Folder | Size | Contents |
| --- | --- | --- |
| `texts/` | 387 MB | The Tolstoy corpus — 7 genre subdirs, 16,573 TEI files |
| `texts_front/` | 307 MB | A display/web variant of every `texts/` file (1:1) |
| `texts_txt/` | 86 MB | Plain-text extracts (Tolstoy's diaries + witness texts) |
| `tolstoy-bio/` + `tolstoy_bio_front/` | ~336 MB | TEI of the witness/testimony corpus (memoirists; S. A. Tolstaya) |
| `reference/` | 68 MB | The nine authority/reference files (§5.5) |
| `headers/` | 64 KB | 7 per-genre teiHeader templates + a person-list template |
| `images/` · `audio/` | 1.8 GB · 121 MB | Illustration/timeline image sets; timeline narration |
| `utils/` | 6.2 MB | ~50 Python build/QA scripts |

### 5.2. The `texts/` corpus by genre

| Genre | Files | Content |
| --- | --- | --- |
| works | 767 | Literary & non-fiction works, incl. variant redactions (*Варианты*) |
| letters | 9,087 | Tolstoy's outgoing correspondence |
| diaries | 4,584 | Diary entries (Дневники) |
| notes | 100 | Notebooks (Записные книжки) |
| krug_chtenija | 444 | *Круг чтения* (A Circle of Reading) daily readings |
| azbuka | 784 | *Азбука* / *Новая азбука* primer texts |
| comments | 807 | The PSS editorial apparatus (textual histories, manuscript descriptions) |

### 5.3. Filename grammar

The stem `vNN_` is always the **PSS volume (Tom) number**; where two numbers follow, they are the **page range** in that Tom. Letters are the exception — keyed by sequence-within-volume, not page range.

```
works    v01_003_095_Detstvo.xml                 vNN_startPage_endPage_Title
letters  v59_004_T_A_Ergolskoj.xml               vNN_sequenceNo_Addressee   (pages in header)
diaries  v46_003_004_1847_03_17.xml              vNN_startPage_endPage_YYYY_MM_DD
notes    v47_169_176_Zapisnaja_knizhka_...xml    vNN_startPage_endPage_Title
```

Note: the local PSS **PDFs** are numbered by *publication order* (`vol01`…`vol90`), which is **not** the Tom number — the resolver lives in [pss-volume-mapping.md](../pss-volume-mapping.md) (e.g. Tom 53 = local `vol19`).

### 5.4. TEI document anatomy

Every file is a `<TEI>` with a `teiHeader` (a near-identical credit/licence/source block) and a `<body>`. The header carries the canonical citation that joins the digital text back to print:

> Толстой Л. Н. Детство // Толстой Л. Н. Полное собрание сочинений: в 90 тт. Т. 1. М.: Гос. изд. «Художественная литература», 1935. С. 3–95.

In the body, the encoding is genuinely semantic, not just typographic:

- **Named entities** use `<name type="person" ref="N">` in running text (and `<persName>`/`<placeName>` in letter headers and the authority lists). The numeric `ref` is the `id` of a `<person>` in `personList.xml`.
- **Orthography** is dual-encoded: `<choice><reg>вот</reg><orig>вотъ</orig></choice>` pairs the modern reading with the pre-reform original, token by token.
- **Editorial corrections** use `<choice><sic>…</sic><corr>…</corr></choice>`; footnote anchors use `<ref target="#noteN">`; the PSS commentary sits in `<noteGrp type="comments">`.
- **Page boundaries** are marked `<pb n="N"/>` — the backbone for page-accurate citation (a quotation crossing a `<pb>` needs care, as words split across a page break are flagged).
- **Letters** carry a machine-readable `<correspDesc>` with sender/recipient/place/date — e.g. the recipient "Ергольская Татьяна Александровна" with a persName ref into the person list.

### 5.5. The nine reference files

These are the structured backbone — the machine-readable counterpart to the 1964 index volume.

| File | Size | Holds |
| --- | --- | --- |
| `personList.xml` | 4.3 MB | **3,113 persons** — `<person id="N">` with names, birth/death, occupation/era facets, descriptions, and a **Wikidata Q-id** anchor |
| `locationList.xml` | 185 KB | **385 places** — `<place xml:id>` with `<geo>` coordinates + prose |
| `bibllist_works.xml` | 2.2 MB | The works catalogue — one `<relatedItem>` per text (file-stem → titles → PSS bibl → date → volume) |
| `bibllist_bio.xml` | 35.6 MB | Bibliographic index for the witness/biography corpus |
| `sourceList.xml` | 954 KB | Sources cited in Gusev's chronicle |
| `Dictionary.xml` | 904 KB | Rare/archaic-word glossary with PSS attestations |
| `listMedia.xml` | 26.8 MB | Museum photo/media catalogue (the "Tolstoy social network" data) |
| `taxonomy.xml` / `taxonomy_front.xml` | 22 KB / 19 KB | The 125-category controlled vocabulary `xi:include`d by every text |

A person record, for example, carries structured facets and an external authority link:

> «Крупный российский промышленник, археолог-любитель, автор сочинений.» — the description of S. S. Abamelek-Lazarev (person id 15), whose `persName` also carries the Wikidata id **Q7449866**.

Two practical quirks worth recording: person links are **numeric ids** while place links are **string `xml:id`s** (asymmetric); and `Dictionary.xml` and `listMedia.xml` contain non-NCName `xml:id` values (e.g. `obinujas'`), so a strict XML parser fails on them — a recovering parser is required.

### 5.6. The witness corpora ("свидетельства о Толстом")

Beyond Tolstoy's own writing, the corpus holds the great memoir record of his daily life, encoded the same way: **N. N. Gusev's** *Летопись* (chronicle), **A. B. Goldenweiser's** *Вблизи Толстого*, **D. P. Makovitski's** *Яснополянские записки*, and **S. A. Tolstaya's** diaries and letters. These are tagged `testimonies` ("свидетельства о Толстом") and live in `tolstoy-bio/` and `texts_txt/`.

---

## 6. Scholarly context

There is surprisingly little dedicated English-language scholarship on the Jubilee Edition *as an object*. The fullest account is a Russian documentary history — L. A. Osterman's «Сражение за Толстого» (*The Battle for Tolstoy*, 2000) — supplemented by the "Tolstoy's Complete Works" chapter in *Tolstoy in Context* (Cambridge, 2022). Where the dive's primary evidence meets that literature:

- **On the authorisation.** The Cambridge chapter compresses the origin to "Lenin's affidavit" and a Stalin-era decree. Osterman *complicates* this: Lenin's role in 1918 was support, not a signed decree, and the founding act was a Sovnarkom resolution of 23 June 1925. The front-matter facsimile here confirms only that the *Soviet government* commissioned it and chose Chertkov — consistent with Osterman, looser than the English shorthand.
- **On the constraints.** Scholarship notes Soviet-era framing as a caveat; the commission's own «пропуски» (omissions) clause *extends* this — the constraint is visible in the edition's own front matter, not merely inferred. Osterman documents framing imposed over editors' objections.
- **On completeness.** Chertkov's "reproduce absolutely everything" *confirms* what scholars describe thematically as the edition's defining principle.
- **On the digital edition.** Bonch-Osmolovskaya et al. (2019) present Tolstoy Digital as a *semantic* edition — named-entity and relation layers, not a mere reproduction; the personList/Wikidata anchoring observed here *confirms* that account.
- **On the licence.** The corpus is commonly described as CC BY-SA; the header grant *confirms* the intent, but the absence of a repo LICENSE file *complicates* any formal reuse claim.

---

## 7. Material not covered

- The **100-volume academic PSS** (IMLI, 2000– ), the modern successor — contextual only; not held locally.
- A per-volume **apparatus-depth comparison** (Tom 13 vs Tom 47) beyond the headline.
- The **witness corpora as content** (Gusev/Goldenweiser/Makovitski/S. A. Tolstaya) — inventoried structurally, not read.
- **Wikidata reconciliation** of the 3,113 personList ids against the vault's identifiers (a separate ingestion task).
- **Tom 31 → local-PDF** resolution (still open in pss-volume-mapping).

---

## 8. Visual & manuscript record

The visual material here is chosen for historical interest — the people and places behind the edition — and the printed-edition facsimiles. Downloaded images live in the git-ignored `visuals/` cache (repopulated by `docs/fetch_visuals.py`); the PD facsimiles are committed under `extracts/`.

<figure>
<img src="visuals/commons-alexandra-tolstaya.jpg" alt="Alexandra Lvovna Tolstaya, c. 1905">
<figcaption>A. L. Tolstaya, Tolstoy's daughter, manuscript heir, and an original editorial-board member. Photograph c. 1905. Public domain (Wikimedia Commons).</figcaption>
</figure>

<figure>
<img src="visuals/commons-yasnaya-polyana-main-building.jpg" alt="The main house at Yasnaya Polyana, early 20th century">
<figcaption>Yasnaya Polyana — Tolstoy's main house, early 20th century. The estate from which most of the edition's manuscript base originates. Public domain (Wikimedia Commons).</figcaption>
</figure>

<figure>
<img src="visuals/commons-tolstoy-museum-moscow-facade.jpg" alt="State L. N. Tolstoy Museum, Moscow">
<figcaption>State Museum of L. N. Tolstoy, Prechistenka 11, Moscow — co-initiator of the digitisation and holder of the photo collection in listMedia.xml. Photo by NVO, 2007 (Wikimedia Commons, CC BY-SA 2.5).</figcaption>
</figure>

<figure>
<img src="extracts/pss-vol62-pages/page-004.png" alt="Facsimile: the free-reproduction notice, PSS Tom 1">
<figcaption>The edition's own free-reproduction notice: «Перепечатка разрешается безвозмездно / Reproduction libre pour tous les pays.» PSS Tom 1 (1935). Public domain.</figcaption>
</figure>

<figure>
<img src="extracts/pss-vol62-pages/page-006.png" alt="Facsimile: Chertkov's editor-in-chief foreword, PSS Tom 1">
<figcaption>«ОТ ГЛАВНОГО РЕДАКТОРА» — Chertkov's editor-in-chief foreword, citing Tolstoy's 31 July 1910 testamentary request. PSS Tom 1 (1935). Public domain.</figcaption>
</figure>

**Not openly available.** No Wikimedia Commons image was found for the board members **N. N. Gusev** or **N. K. Gudzy** (next step: the State Tolstoy Museum or RGALI). The modern Tolstoy Digital leads **Bonch-Osmolovskaya** and **Orekhov** have no free image located. A screenshot of `index.tolstoy.ru` would be rights-uncertain and was not captured.

---

## 9. Method

This was an atypical corpus-dive: the subject is the corpus and the edition *themselves*, so the "evidence" is metadata, not theme-bearing prose. The Phase-0 contract scoped two artifacts (the printed Jubilee Edition and the tolstoydigital TEI corpus), declared the local surface (90 PSS PDFs + the full TEI clone), and chose a history-plus-structure emphasis with a people-and-places visual sweep, on the reader's steer.

What happened: (1) local structural inspection of the TEI clone (directory inventory, filename grammar, document anatomy, the nine reference files, the witness corpora); (2) web scholarship on the edition's history (Osterman; Cambridge 2022) and the digital projects (Orekhov 2020; Bonch-Osmolovskaya et al.; the project sites); (3) byte-faithful extracts pulled directly from the local sources (TEI headers, the reference records, the printed front matter) and three PD facsimiles rendered with `pdftoppm`; (4) a Wikimedia Commons visual sweep, licences verified against the File: pages via the API; (5) synthesis into this document, the `dossier.yaml`, and a draft note. The mechanical byte-fidelity gate (`verify_quotes.py`) passes 21/21. Corrections to the project's earlier loose docs and to the common English summary of the edition's authorisation are recorded in the dossier's `contradictions` and `needsReview`.

---

## 10. References

**Primary**

- Толстой Л. Н. *Полное собрание сочинений: в 90 тт.* М.–Л.: Гос. изд. «Художественная литература», 1928–1958; Том 91 (*Указатели*), 1964. (local: `primary-sources/jubilee-edition/`)
- tolstoydigital TEI/XML corpus — Tolstoy Digital / «Слово Толстого» / HSE, CC BY-SA (header-scoped). `github.com/tolstoydigital/TEI` (local: `primary-sources/tolstoydigital-TEI/`)

**Background**

- Osterman, L. A. *Сражение за Толстого.* Moscow: Monolit, 2000. — documentary history of the edition (decrees, board, print run, censorship).
- "Tolstoy's Complete Works," ch. 34 in *Tolstoy in Context* (ed. Donskov / Berman). Cambridge University Press, 2022.
- Orekhov, B. V. "'Volume 91': an Electronic Index to the Complete Works of Leo Tolstoy." *Journal of Siberian Federal University. Humanities & Social Sciences* 13(12), 2020, 2049–2055. DOI 10.17516/1997-1370-0703.
- Bonch-Osmolovskaya, A.; Skorinkin, D.; Pavlova, I.; Kolbasov, M.; Orekhov, B. "Tolstoy semanticized: Constructing a digital edition for knowledge discovery." *Journal of Web Semantics* 59, 2019. DOI 10.1016/j.websem.2018.12.001.
- ABBYY / Russia Beyond (2013–2014) and readingtolstoy.ru — «Весь Толстой в один клик» project documentation.

---

*Draft dev-blog note: [2026-05-30-jubilee-edition-tei-corpus.md](../../../../website/src/posts/notes/2026-05-30-jubilee-edition-tei-corpus.md). Wiki ingestion of the entities mapped in `dossier.yaml` is a separate, human-in-the-loop step.*
