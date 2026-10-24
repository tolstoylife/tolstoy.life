# Session log — betanken-eder-in-sweden

## 2026-10-24 — sweeps, synthesis, mechanical gate

- Question as first asked by Johan: why SFSF (Svenska freds- och skiljedomsföreningen) was involved in *Betänken Eder!* (Stockholm 1904) and took the initiative to it, and what happened around it.
- Two sweeps ran first and were saved in `extracts/`: `_sweep_corpus.md` (tolstoydigital TEI, 1895–1910; extracts with `--choice=reg --notes=auto`, plus `--notes=force` copies where the editorial notes mattered) and `_sweep_swedish.md` (Svenska tidningar, LIBRIS, Runeberg, KB page images; FOUND vs INFERRED marked). Five 1904 newspaper images were saved to the git-ignored `visuals/`.
- Result for 1904: no source names SFSF or any society; the pamphlet was a commercial Björck & Börjesson job (5 July, 10,000 copies, 35,000 in two weeks, *Fria ord* no. 1) built on GHT's translation of 1 July, with chapter IX, the epigraphs, the datelines and the postscript left out.
- Mid-run correction from Johan: he now places SFSF's involvement with Tolstoy around the 1909 Stockholm peace congress (postponed by the general strike) and the 1910 invitation. The question was reframed, and the 1909–10 thread got its own section.
- Short web check on 1909–10 (seven searches, plus Runeberg pages, the KB data API and two Riksdag prints): FOUND that SFSF's central board published Tolstoy's Report as *Döda icke!* (1910), and that the 1908 state grant for the congress was requested by "Sveriges fredsförenings samarbetskommitté". NOT FOUND: the organising committee's roster, or whether Dr J. Bergman and Baron C. C. Bonde held SFSF office (to `needsReview`).
- Wrote `index.md`, `dossier.yaml` (73 evidence rows: 53 Russian/French quotes from extracts, 20 Swedish rows without quoteRu) and the draft note `website/src/posts/notes/2026-10-24-betanken-eder-in-sweden.md` (`draft: true`).
- Phase 5 mechanical gate: `verify_quotes.py` PASS, 53/53 verbatim, 0 label warnings. `serve.py --build-only` rendered `index.html`.
- Not done here (by instruction): the verifier pass, the Phase 6 research handoff and the Phase 7 session handoff. Nothing committed.
- Resume from: the dossier `coverage` ledger and `needsReview`, then `notCovered`.
