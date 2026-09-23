# A Confession — alignment and capture notes

How `confession.ru.md` (PSS «Исповедь», t. 23, pp. 1–59) and `confession.en-wiener.md` (Leo Wiener's 1904 translation, *My Confession*, from the Complete Works of Count Tolstoy vol. 13) were made paragraph-parallel, so the two share one **paragraph coordinate** — paragraph N of chapter K in either version points to the same place in the work.

Both versions segment to **16 sections / 212 paragraphs** and pass `reader.segment --spine-json` (the per-section paragraph-count check).

## Which version defines the coordinate

The Russian is the spine. Unlike The Great Sin — where the English was the incumbent because its read-along audio was already aligned to it — nothing had been built here yet when the alignment was done, so the English was fitted to Tolstoy's paragraphing rather than the other way round. Wiener's wording is untouched throughout; only paragraph **breaks** were moved to match the Russian, and only at real sentence boundaries.

## Capture notes

These four notes were written during the 2026-07-17 alignment pass and originally sat inline in `confession.en-wiener.md` as HTML comments. They were moved here on 2026-08-09: the segmenter splits paragraphs on blank lines, so a standalone comment counted as a paragraph and broke the alignment check in all four chapters. `resolve_reading_text()` also strips CriticMarkup and wikilinks but *not* HTML comments, so leaving them attached to a paragraph instead would have leaked the note text into the reading display and the spoken audio. Two of the notes already pointed at this file by name.

### Chapter IV — a ~500-word gap, restored

The source e-text (and the underlying `tolstoyarchive.org` epub) dropped roughly 500 words: *"The thought"* ran straight into *"him."*, skipping the rest of that sentence, four whole paragraphs (the "complete happiness" / "stupid trick played on me" passage), and the opening of the well/dragon fable.

Restored verbatim — not re-translated — from the Wikisource proofread transcription of this same Wiener 1904 edition (`en.wikisource.org/wiki/The_Complete_Works_of_Count_Tolstoy/Volume_13/My_Confession`, itself transcluded from the scanned Complete Works vol. 13 djvu pages on the Internet Archive).

### Chapter V — a duplicated passage, removed

The source e-text repeats the preceding four paragraphs a second time verbatim — a scan/OCR duplication — with the repeat's first paragraph spliced onto the true opening of the next section (*"I must confess, there was a time when I believed all"* plus the tail end of the "experimental sciences" paragraph above). Confirmed as a defect in the source itself, not in our capture. The genuine next paragraph (Russian ch. V, para 13) resumes unaltered after the cut.

This is the same *kind* of defect as the still-open duplicate-narrative question in the Resurrection dive.

### Chapter VII — an omission that is Wiener's own

Wiener's translation omits Solomon's shorter "I commended mirth" saying (Ecclesiastes 8:15), which the Russian carries as «И похвалил я веселье…». Confirmed against the clean Wikisource transcription of this same edition, so this is the translator's own choice, not a digitization defect. Nothing restored — filling it from another translation's wording would misrepresent what a reader of Wiener 1904 actually saw.

### Chapter XI — a missing heading, restored

The "XI." heading is absent from the e-text; chapters X and XI run together there. Restored at the paragraph whose opening matches the Russian chapter XI opening («И вспомнив то, как те же самые верования отталкивали меня…»), and whose preceding paragraph matches the Russian chapter X ending.

## Open items

- **Verify the chapter XI heading against the printed page** (Wiener vol. XIII facsimile) when convenient. The placement is well-evidenced from both sides of the join, but it has not been checked against the scan.
- **`бог 1 и 3` (Russian ch. IX)** reads like an OCR-mangled "God, one and threefold" — «бог 1 и 3» where the numerals stand in for the Trinity formula. Worth a facsimile check against PSS t. 23; not repaired, since the reading is a guess. The machine translation renders it "God, one and three", following this reading.

## Spine defects found while translating (2026-08-10)

Three small transmission faults in `confession.ru.md` surfaced during the machine-translation pass. None is repaired in the spine — repairing the source text is a separate decision — and each is translated as intended rather than mirrored, so the English does not carry a digitization artefact forward as if it were Tolstoy's.

- **`слитком` (ch. I, para 4)** is a typo for `слишком`: "one should not take all this *too* seriously". A single letter substitution, so the homoglyph sweep would not have caught it.
  *Checked against the page image 2026-09-23 and repaired:* PSS Tom 23 (local `vol83/vol83.pdf`, PDF page 40, printed p. 2) reads «слишком». The scan's own text layer also says `слитком`, which is how the error got into the extract. The Great Sin had the same slip — see its alignment notes.
- **Unclosed `«` (ch. III, para 14)** — the paragraph opens `«Случилось то, что случается…` with no closing quote anywhere. The English renders the paragraph without the stray mark.
  *Checked against the page image 2026-09-23 and repaired:* the printed paragraph (Tom 23, PDF page 49, printed p. 11) has no opening quotation mark at all — the `«` was our extract's, so it is removed rather than closed.
- **Stray semicolon (ch. V, para 11)** — inside the sciences' reply, `мы не имеем; ответов и этим не занимаемся` splits "have no answers" across the punctuation. Read as `мы не имеем ответов`.
  *Checked against the page image 2026-09-23 and repaired:* the page (PDF page 56, printed p. 18) reads «мы не имеем ответов» with no punctuation — a small ink speck on the foot of the «м» is what the scan's text layer read as `;`.

## Open item from the translation

- **Capitalization of "God".** The PSS text lowercases `бог` throughout («бога нет», «бог есть жизнь»). That reads as a Soviet editorial convention rather than Tolstoy's manuscript, so the English capitalizes God: lowercasing it would carry an edition artefact into the translation as though it were authorial. Worth confirming against the printed page.

- **Evidence that the capitalization call was right.** The Great Sin's spine (PSS Tom 36, «Великий грех», 1905) capitalizes «Бог» throughout — «Бог», «Бога», «Богу», every occurrence — while this spine (Tom 23) lowercases throughout. The same edition series treating the same word differently from one volume to the next looks like a per-volume house decision rather than anything authorial, which supports capitalizing in the English here. Noted 2026-08-10 while translating The Great Sin; still worth confirming against the printed page.
