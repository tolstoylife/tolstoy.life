# The Great Sin — Russian spine alignment notes

How `the-great-sin.ru.md` (PSS «Великий грех», t. 36, pp. 206–230) was made paragraph-parallel to `the-great-sin.en-1905.md` (the 1905 Mayo/Tchertkoff translation), so the two share one **paragraph coordinate** (paragraph N in either version points to the same place in the work).

Both versions now segment to **10 sections / 135 paragraphs** and pass `reader.segment --spine-json` (the per-section paragraph-count check).

## Which version defines the coordinate

The English is the incumbent: its read-along audio is already aligned to its paragraph/sentence structure. So the Russian was fitted to the English shape, not the other way round. The Russian wording is untouched — only paragraph **breaks** were moved (split or merged) to match where the English breaks.

## English repairs (3)

The pilot English edition had three places where a single sentence was split across a paragraph break (transcription defects — they read and speak wrong). These were rejoined:

- Part II: *"…those called the working people" + "were the people who lived in the poorest houses."*
- Part II: *"We naturally" + "despise poverty, and it is reasonable…"*
- Part IX: *"…with whom he comes in" + "contact."*

**Consequence — resolved 2026-07-02:** rejoining shifted 3 sentence boundaries in Part II and Part IX, which left the English audio + timing for those two chapters (`sec-3`, `sec-10`) out of sync with the renumbered text — the voice skipped and jumped while the highlight moved normally down the page. Both chapters were regenerated (re-synth in the `projects/audiobook` repo, then a `reader.build_epub` restitch). `build/` is regenerable and gitignored, so the fix left no tracked change beyond this note.

**Watch out — the wav cache is keyed by sentence ID, not by the text.** A plain rebuild does *not* fix this: `build_audiobook.py` reuses any `wav_full_bm_daniel/<id>.wav` that already exists without checking whether the text still matches, so once a rejoin renumbers the sentences, the old (wrong) recording sits under a reused ID and gets served again. The fix was to delete *all* of `sec-3` and `sec-10`'s cached wavs — every renumbered clip, not just the audibly-broken ones, because a shifted sentence that happens to be the same length would slip past a words-per-second check while still being the wrong recording — then let the build re-synthesize them from the corrected text. Only those two chapters were renumbered, so the other eight kept their cache and came out timing-identical. (Same trap applies to any future pronunciation respell: it won't take until you also delete that sentence's cached wav.)

Verified: the words-per-second check went from 13 impossible-rate sentences (7 in `sec-3`, 6 in `sec-10`) to 0 across all ten chapters; the eight untouched chapters' timing is byte-identical to before; every read-along slot fits inside its chapter's audio; EPUBCheck clean. Confirmed working by a full Thorium read-through (Johan, 2026-07-03).

**Deferred audio backlog (not blocking).** Voice-quality notes from the read-through, separate from the alignment fix — each pronunciation fix is a respelling in `reader/speech.py` `_SUBS` plus deleting that sentence's cached wav (the wav cache is keyed by sentence ID, not text, so the respell won't take until the wav is cleared):
- **"Kvas"** (Part I) — read as two beats "K-Vas"; want one syllable.
- **"Alexander II"** (Part IX, `p-10-6-s1`) — read as letters; should be "Alexander the Second."
- **"I asked"** dialogue tags — high-pitched where they should be flat (prosody, not a respelling; may not be worth chasing).
- **Other pronunciations** and **pausing between paragraphs / after headings** (the `PARA_GAP` / `CHAP_GAP` tuning) — flagged in the read-through, not yet itemised.

Reader-text and content items from the same read-through (missing italics, wanted footnotes, the English-title question) are filed as dive steer in `docs/research/works/non-fiction/essays-and-criticism/1905-the-great-sin/annotations.md`.

## Short-phrase pitch — the audio-only merge (2026-07-04)

Kokoro rises in pitch on a very short clip (2–4 words) synthesized on its own, where it should fall. We can't set pitch directly, so the only lever is **context**: hand the synthesizer more words at once. Two mechanisms now do this, both keeping the page text faithful and the read-along mapping intact.

**1. The sentence merge (`speechGroup`).** A too-short leading sentence is glued into the next sentence of its paragraph *before* `segments.json` is written — one combined clip, one highlight unit (the pair lights up together during read-along). Because the merge happens before the shared file, everything downstream (clips, timing, SMIL) stays consistent; no change to the audio or EPUB builders. Which sentences merge is an **explicit list** by ID in `reader/speech.py` (`MERGE_FORWARD`), *not* a word-count rule — a blanket "short sentence" rule would wrongly flatten legitimate rising **questions** ("Why is this?", "Whence this dreadful perversity?"). Configured here: `p-7-3-s1` "But we are wrong." → glued into its long following sentence.

**2. Two speech-only respellings** (`reader/speech.py` `_SUBS`; the page keeps its punctuation):
- **welfare list** (`p-6-7-s1`) — full-stop-flattened like the two noun lists, so the "to abolish… to organize… to increase…" run gets air. (It's an infinitive list, so it reads a touch more clipped than the noun lists; kept because the pacing win outweighs it. Revisit if a later ear-check disagrees.)
- **pause after "God,"** (`p-7-8-s2`) — "God," → "God." in speech only; the full stop gives the wanted pause.
- **"…their parasites."** (`p-6-6-s1`) — after the comma Kokoro rendered the closing appositive as a high rising tag (**~149 Hz**); an em-dash in speech only ("support us — their parasites.") keeps a beat but drops it to **~111 Hz** so it falls. Page keeps the comma. Picked by measuring the final-word pitch with **parselmouth** (praat) — the reusable way to settle "does it rise or fall" without guessing.

**Comma pause length is a Kokoro constant (~140 ms) — no lever.** Measured three ways: slowing to speed 0.93 keeps commas at ~145 ms (it stretches the *words*, not the pauses); commas→semicolons gives ~147 ms (Kokoro treats them the same). The only thing that lengthens a comma is a full stop, which resets pitch — so it's a per-spot tool (the lists, "God,"), never a global default. Comma pacing is accepted as-is.

**Accepted as Kokoro limits** (no clean lever; documented so they're not re-litigated):
- **Section headings** ("Part One." etc.) rise when spoken alone. Merging a heading (`<h2>`) into the first sentence (`<p>`) can't share one read-along highlight cleanly, so left as-is.
- **"Why is this?"** (`p-8-4-s1`) — a one-sentence paragraph with no neighbour to merge into; and it's a question, which is *meant* to rise.

Earlier backlog items are resolved: **Kvas** → "quahss", **Alexander II** → "Alexander the Second" (both in `_SUBS`).

## Russian break adjustments (per section)

Native PSS paragraphing → English coordinate. Every split/merge is at a real sentence boundary; no wording changed. The starting text is the native extract `docs/research/works/non-fiction/essays-and-criticism/1905-the-great-sin/extracts/v36_206_230_Velikij_greh.txt`; the committed `the-great-sin.ru.md` is the curated result (source of truth, not regenerated).

| Section | Native | Target | Adjustment |
|---|---|---|---|
| Introduction | 5 | 5 | — |
| Part I | 46 | 45 | split the "knacker's beast / in whose mine" turn (two speakers PSS ran together); merge the blind-man narration+question; merge "Я спросил:" + "— О чем?" |
| Part II | 15 | 14 | split the Henry George opening (attribution / quote); merge "Отчего это?" + "Оттого, что…"; merge the closing George question back onto its paragraph |
| Part III | 8 | 9 | split the Oxford passage before "Главными же орудиями…" |
| Part IV | 10 | 9 | merge the question "…хорошую жизнь народа?" + its answer |
| Part V | 12 | 11 | merge "…кормили нас." + "Наши грехи всегда перед нами." |
| Part VI | 9 | 8 | merge the two halves of the Matthew epigraph |
| Part VII | 10 | 10 | — |
| Part VIII | 5 | 8 | split R4 three ways and R5 two ways (English breaks each declarative sentence into its own paragraph) |
| Part IX | 14 | 16 | split the closing George quote before "Земля вспахана…"; add the dateline |

## Other spine cleanups

- Stripped one PSS editorial footnote marker (³⁷) at the Henry George citation in Part II — apparatus, not Tolstoy's text; the English carries no notes. (The printed scan also carries a *second* editorial footnote in Part II — marker ¹ on «своих статей», citing «Речи и статьи Генри Джорджа». Изд. «Посредника», стр. 143 и 144. — but that marker and its citation never entered the extract, so there was nothing to strip. Same apparatus category; noted for provenance.)
- Fixed 5 OCR homoglyphs (Latin letters sitting inside Cyrillic words): 3× «зa»→«за», «тело to человека»→«тело человека», «Ha-днях»→«На-днях». The two remaining Latin runs (Мф. **XXIII**, Александр **II**) are Roman numerals — kept.
- Added a closing dateline to parallel the English "Yasnaya Poliana, July, 1905." — the PSS reading text has none. First pass added the full **«Ясная Поляна, июль 1905 г.»** to visually match the English; on review (2026-07-01) that was reverted in favour of the **manuscript form, «Июль 1905»** (no place) — what A. L. Tolstaya actually signed, per the PSS commentary. Keeping strictly to the attested wording matches how every other spine fix was handled (breaks moved, wording untouched; OCR fixes correct transcription, they don't add content) — inventing "Ясная Поляна" would have been the one exception.

## Proofread against the scan (2026-07-01)

The Russian was machine-extracted from the TEI/PSS. It has now been checked paragraph-by-paragraph against the printed scan (PSS Tom 36 = `primary-sources/jubilee-edition/vol05/vol05.pdf`, pp. 206–230) — a full read plus a word-level automated diff against the scan's own independent OCR, with every disagreement adjudicated by rendering the actual page image and reading it. **Result: clean.** No wording errors beyond the fixes already listed above; every one of the ~35 raw diffs was either an already-recorded fix or noise in the scan's OCR layer (dropped letters, stray mid-word spaces, letter-spaced emphasis the OCR mangled) where the extract's wording was the correct one. All proper names and numbers (Александр II, Новиков, Радищев, Parnell, Toynbee, Gladstone, Spencer, Labouchère, Mazzini, the rent/wage/year figures) verified; the «Мф. XXIII» citation confirmed against the page image (OCR garbles it as «X X III»). The «Марфа, Марфа» epigraph on the same scan page belongs to the *preceding* essay («Конец века») and is correctly excluded here.

Caveat on the caveat: this is a verification pass (extract vs. scan-OCR + visual spot-check of every conflict), not a word-perfect human transcription against the physical book. It's strong evidence the text is right, not a proof.

## Spine defects found while translating (2026-08-10)

Rendering every sentence into English is the closest reading the text gets, and it surfaced a handful of small transmission faults in `the-great-sin.ru.md` that the July proofread did not catch. **None is repaired in the spine** — repairing the source text is a separate decision — and each is translated as intended in `the-great-sin.en-machine.md` rather than mirrored, so the English does not carry a digitization artefact forward as if it were Tolstoy's.

These need adjudicating against the page image rather than assuming, because the 2026-07-01 pass above reported the text clean. The likeliest explanation for the stray-space cases is that a word-level diff normalizes whitespace and so cannot see them; that pass explicitly treated mid-word spaces as noise in the *scan's* OCR layer, and these are in the extract.

- **`слитком` for `слишком` (II ¶7)** — «зарабатывает он слитком мало», immediately followed by the same phrase spelled correctly: «А зарабатывает он слишком мало». A single letter substitution, so a homoglyph sweep would not catch it. The identical typo was found in `confession.ru.md` (ch. I, para 4), which suggests a shared source or a shared OCR pass rather than a one-off.
- **`е сть` (VII ¶1)** — «есть» split by a stray space: «в жизни всего мира е сть одно наиболее назревшее».
- **`мог о бы` (II ¶10)** — «как мог о бы Он облегчить бедность», read as «как мог бы».
- **`я придумывают` for `и придумывают` (V ¶1)** — «люди начинают бояться… я придумывают различные средства». A я/и confusion; the grammar requires «и».
- **`придумывают` for `придумывать` (VII ¶9)** — «Такие люди не будут… придумывают такие или иные улучшения». After «не будут» the infinitive is required.
- **`с телегами` for `с телятами` (I ¶1)** — «Народ обозами едет на базар, с телегами, курами, лошадьми, коровами». «Обозами» already means *in trains of carts*, so «с телегами» ("with carts") is redundant, and every other item in the list is livestock. Read as «телятами» ("calves") — which is also what the 1905 English has. This one is a reading, not a certainty, and is the most worth checking against the page.
- **Stray comma in `торгуя, землями` (IX ¶5).**

## Quotation marks in the machine English (2026-08-10)

`the-great-sin.en-machine.md` uses curly double quotes; `the-great-sin.en-1905.md` uses straight ones. The Great Sin plan asked the machine layer to mirror the 1905 file's convention and described that convention as curly, which is not what the file actually contains. Rather than follow the description or the file, the machine layer follows **A Confession's machine leg**, which settled on curly quotes: the machine Englishes are the set that needs to read consistently with each other, and the difference also makes it visible at a glance which English column a reader is in. Dialogue that the Russian marks with an opening dash is rendered with quotation marks, as English convention and the Confession precedent both do.

Capitalization of «Бог» does not arise here: this spine already capitalizes throughout — «Бог», «Бога», «Богу» — so the English simply follows the source. That is worth noting alongside the opposite decision taken for A Confession, whose spine lowercases; see that bundle's alignment notes.
