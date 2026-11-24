---
layer: reference
lastUpdated: 2026-10-24
---

# Verifier report: Betänken Eder! in Sweden (Phase 5)

Independent check of `index.md`, `dossier.yaml`, `extracts/`, `visuals/` and the draft note `website/src/posts/notes/2026-10-24-betanken-eder-in-sweden.md`, run 2026-10-24.

## Verdict: CLEAN WITH FIXES (12 fixes)

## Checks run

- **Quote gate.** `verify_quotes.py` passed before and after the fixes: 53/53 quotes verbatim, 20 Swedish/catalogue rows skipped by design, 0 label warnings.
- **Re-derivation from TEI.** 15 TEI XML files were re-extracted fresh into a scratch folder with `extract_tei.py --choice=reg --notes=auto` (and `--notes=force` for the note-borne quotes). 24 Russian or French quotes in `index.md` were matched against those fresh extracts: 22 matched exactly. The other 2 were inline quotes in `index.md` that differed from the source (and from the dossier) by one character, and both are now fixed: a dropped footnote mark (`эпиграфов¹`) and straight apostrophes in the Langlet French. A further scan of all 27 inline «…» Russian quotes in `index.md` against `extracts/` found every one of them.
- **Swedish claims against `_sweep_swedish.md`.** Every claim about the 1904 press, SFSF and the publisher is backed by a numbered entry in the sweep or by a URL in the dossier. The web-check findings for 1909–10 carry URLs. *Döda icke!* pp. 1 and 16 were re-read on Runeberg, and both quotes (the SFSF central-board imprint and the "september förra året" preface) are confirmed. FOUND versus INFERRED is honoured, apart from three overstatements, all now fixed: the claim that every provincial reprint included chapter IX (it is seen in only three), that "only" the pamphlet lacks IX (Socialdemokraten's serial was not read in full), and the society's "line that autumn" (inferred from one issue's contents).
- **Working English.** The sampled translations (chapter IX, the Andersen passage, the Addition, Biryukov, Bergman, the Suttner letter in French, Makovitsky, the 1899 signatories, Varnavsky) are faithful. All are labelled, either "(working English)" or with the in-line gloss convention plus the Method note. One unlabelled quoted English sentence, the Varnavsky paraphrase, is now labelled.
- **Voice.** No movement labels appear in the dive's own voice. "Pacifists" is attributed to Biryukov, and "antimilitarism" is Tolstoy's own word. Tolstoy's views are given in his words. Four editorial phrases were cut or neutralised (see fixes).
- **Entities.** All `wikiType` values (person, institution, event) are valid under `website/schema/wiki-schema.md`. Each `vaultStatus` was checked against `website/src/wiki/` (14 pages, loose-matched): Chertkov, Birukoff, Lev Lvovich Tolstoy and Sophia Tolstaya exist; none of the 16 `missing` entities has a page under any spelling. The `jubilee-edition` source id exists.
- **Images.** All 5 images are 1904 KB newspapers, licence PD, in `visuals/`, which is git-ignored (`docs/.gitignore:26`). Nothing related is in `website/src/`. The dive folder is untracked; nothing was committed.
- **Build.** `docs/serve.py --build-only` ran clean (438 documents + 65 hand-authored).

## Fixes made (all in `index.md` unless stated)

1. Chertkov letter quote: restored the footnote mark `эпиграфов¹`, so the quote is byte-faithful to the TEI.
2. Langlet French quote: straight apostrophes changed to the source's ’.
3. Provincial reprints: no longer says all of them included chapter IX; it now names the three in which IX is seen (Falköpingsposten, Hessleholms tidning, Nya Lidköpingstidningen).
4. Pamphlet's last page: "Runeberg, p. 42" corrected to "p. 40; Runeberg scan 0042". Runeberg's scan 0042 is printed page 40.
5. "only the Björck & Börjesson pamphlet lacks it" changed to "of the Swedish texts checked", with Socialdemokraten's unread serial noted.
6. "The society's line that autumn was…" changed to "The issue's themes were neutrality and a cheap defence", which is what the source shows.
7. "Why this matters": removed "the era's sharpest anti-war letter", "a story that is easy to believe" and "cautiously".
8. The key-finding heading "explain why a peace society would hesitate" changed to "show his distance from peace societies".
9. "*Одумайтесь!* itself mocks the Hague conference's defenders" changed to "faults the speeches that reconciled the war with the Hague conference".
10. "this was not easy material to put its name to" changed to "this may have been hard material … (inferred)".
11. Gusev: "recorded the same day" (wrong: Gusev's entry is 9 July, the Varnavsky letter 10 July) changed to "had recorded on 9 July". The Varnavsky paraphrase is now labelled working English.
12. Bonde's repeat invitation "13 June" changed to "13 June (NS)", to match the PSS note and the dossier.

`dossier.yaml`: no data changed; one `needsReview` item added (below). The note needed no changes: its claims match the corrected index, and its voice is plain.

## Open items

- **Added to `needsReview`:** the third `scholarship.triangulation` entry sets Johan's own working premise against `sv_doda_icke_1910` as "contradicts", with an empty source. The 1904 negative evidence is what contradicts the premise, while *Döda icke!* moves the SFSF link to 1910. It needs a decision: keep it, point it at the 1904 rows, or move it out of triangulation.
- **Still in `needsReview` from the dive:** SFSF's 1904 board minutes and the undigitised *Fredsfanan* issues; whether Bergman and Bonde held SFSF office; who Dr J. Bergman was; who cut chapter IX; Socialdemokraten's opening translation; the bracketed line in the reader's empty chapter IX; the PSS PDF cross-check (not run).
- **Noted, not changed:** the `v36_426_435` variants quote keeps pre-reform spelling (`установленіе`, `политическаго`) even under `--choice=reg`. It matches the extract and passes the gate, so it is probably how the variants are printed, but a PDF look would settle it. The dossier's working English for «Сегодня же» ("That same day") is acceptable; "That very day" would be closer.
