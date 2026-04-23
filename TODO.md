# Tolstoy Research Platform — Backlog

Last updated: 2026-04-22

---

## Active priorities

### 1. `tl`-kommandon för ebook-produktionspipelinen
Tre nya kommandon behöver byggas för att komplettera Phase A–C i Johan-workflow.md. Byggs i en sammanhållen session (alla tre parallellt). Birukoff-biografin är det tänkta första testet när kommandona är klara.

**Kommandon att bygga:**
- `tl convert-scans` — JP2 → JPEG + självständig `index.html` scan-browser för split-screen korrekturläsning
- `tl lint-ocr` — detekterar och auto-fixar OCR-artefakter (saknade apostrofer, avstavningar, misreads, löpande sidhuvuden); stöd för bokspecifik `.tl-lint-ocr.yaml`
- `tl detect-italics` — kursivigenkänning i två lägen: `--mode phrase-list` (kända titlar/fraser) och `--mode hocr` (Tesseract hOCR-konfidensbaserat); plus `tl ocr-confidence-report`

**Referens:** `projects/birukoff-biography/` + `uploads/johan-workflow.md`

### 2. LightRAG + Ollama — kvarstående steg
Grundinstallation klar (2026-04-18). Qwen2.5:7b + nomic-embed-text operativt. Första ingestion av 29 filer OK (43 min, 192 noder, 196 kanter). Se `_generated/lightrag-performance-report-2026-04-18.md`.

**Kvarstående:**
- ~~Byt embedding-modell till bge-m3 (1024d) för ryska+engelska~~ — Klart.
- Sätt upp nattligt cron-job för `sync.py`
- Testa inkrementell sync efter wiki-redigeringar
- Committa LightRAG-scaffolden (staged i git)

### 3. GitHub Projects för `projects/`-mappen
Bethink Yourselves, Birukoff-biografin och Korrektur ligger i `projects/` men är exkluderade från parent-repot via `.gitignore`. Undersök hur GitHub Projects kan användas för att tracka och organisera dessa produktionsprojekt — issues, boards, milestones. Kolla om varje projekt bör ha ett eget repo under `tolstoylife/` eller om ett gemensamt projekt-board räcker.

### 4. TEI-data ingestion (fas 3)
3 113 personer och 770 platser i tolstoydigital/TEI-repot. Börja med Tolstoys närmaste krets och arbeta utåt i tiers. Se implementationsplanen i CLAUDE.md.

**Nästa batch:**
- Skapa wiki-sidor för Ilya Lvovich Tolstoy och Mikhail Lvovich Tolstoy (saknas i TEI — källa: Birukoff)
- Nyckelplatser: Moscow Khamovniki house, Optina Pustyn, Shamordino
- Verifiera födelsedatum/-platser för befintliga barnsidor (Sergei, Lev, Maria, Andrei)
- Verifiera Alexandra Tolstayas deathPlace (Valley Cottage, NY)

### 5. PWA-arkitektur — follow-up efter 2026-04-23 review
Revisionen är klar. Se `_generated/PWA/architecture-review.html` (renderad rapport) och `_generated/PWA/handoff-2026-04-23.md` (handoff). Följande gaps behöver åtgärdas innan Stage 1 kan skeppas — rankade efter severity.

**Blockers för Stage 1:**
- [ ] **Fix the wiki-previews/manifest cascade** (critical) — exclude `manifest.json` and all generated cross-references from the work-hash input. Compute content hash over rendered chapters/CSS/images only. Without this, every wiki edit re-versions every work and the 3-version retention discipline collapses. See architecture-review.html Part 7.
- [ ] **Reconcile `yjs-schema-and-sync.md` §2.3 vs §8** — decision log says Y.Text, §2.3 says Y.Array of plain objects. They have different concurrency semantics. Pick one before Stage 4 implementation begins; a Y.Array of plain objects produces silent duplicates on concurrent edit.
- [ ] **Publish deterministic-build CI test** — build twice, diff SHA-256 trees, block merge on mismatch. Referenced throughout `tl-pipeline-integration.md` but not wired in.
- [ ] **Add `chapterUri` validator + one-shot migration** — no corpus files have `chapterUri` yet; the fail-loud rule (§8.1) would block every deploy on rollout. Need an `assign-chapter-uris.py` script with `--confirm-assign` gate, plus a uniqueness checker.
- [ ] **Replace `git_first_commit_date_for_dir` with stateful `contentDate`** in `works.json` — current approach breaks on Netlify's shallow clones.
- [ ] **Adopt a canonical JSON encoder** (`rfc8785`) and NFC-normalise all strings before hashing.

**Infrastructure decisions (committed 2026-04-23):**
- [ ] Sign up for Cloudflare Pages account ✓ (done)
- [ ] Connect `tolstoylife/website` repo to CF Pages as a parallel deploy target (verify builds match Netlify byte-for-byte)
- [ ] Transfer domain to Cloudflare Registrar at next Netlify renewal (~$22/yr saved; CF at $28.20, Netlify at ~$50)
- [ ] Add `netlify.toml` with `[build.processing] skip_processing = true` (minimum-change determinism fix — see architecture-review.html)
- [ ] Add `_headers` file with per-path Cache-Control (immutable for versioned, short max-age for `works.json`/`manifest.json`)
- [ ] Implement cached file-hashing in `generate-asset-manifests.py` (keyed by mtime+size) before Phase 3 ingestion

**Stage-4 fixes (before sync ships — not urgent yet):**
- [ ] HKDF key separation for HMAC / AEAD / export (currently one key used for multiple purposes — crypto footgun)
- [ ] SAS confirmation handshake replacing the yes/no pairing confirm (real MITM protection vs theatre)
- [ ] Device-registration authorisation — existing device must sign new-device registration (otherwise revocation is a placebo)
- [ ] Rate-limit pairing attempts at the Durable Object; one-use BIP-39 tokens
- [ ] Resolve the "relay doesn't parse user data" contradiction (can't be literally true if server-side snapshot compaction is enabled)
- [ ] Promote BIP-39 pairing to iOS-primary (BarcodeDetector is not available on iOS Safari as earlier drafts assumed)
- [ ] `history.replaceState` on `/pair` to mitigate iCloud Tabs fragment leak
- [ ] Dormant-user heartbeat (keep relay room alive while paired devices are active)

**Referens:** `_generated/PWA/architecture-review.html` är den kanoniska renderingen; `_generated/PWA/handoff-2026-04-23.md` är orienteringsdokumentet för nästa session.

### 6. EPUB 3.3 & Accessibility 1.1 — compliance and wikilink strategy
*From W3C spec review 2026-04-22. Full findings: `_generated/epub-a11y-w3c-review-2026-04-22.md`*

EPUB Accessibility 1.1 is now a W3C Recommendation and mandatory for all EPUB 3.3 publications. Several gaps identified in the `tl` toolset and in how wikilinks are handled in distributed EPUBs.

**Tasks:**

- [ ] **Audit `tl create-draft` templates** against EPUB A11y 1.1 mandatory metadata checklist — `accessMode`, `accessibilityFeature`, `accessibilityHazard`, `accessibilitySummary`
- [ ] **Add schema.org accessibility metadata defaults** to `content.opf` template (pre-populated with sensible values + clear placeholders for per-book overrides)
- [ ] **Add `<nav epub:type="page-list">` support** to `tl build-toc` — required for print-replica ebooks (Birukoff biography and similar scan-based projects); enables `printPageNumbers` accessibilityFeature declaration
- [ ] **Define wikilink strategy for distributed EPUBs** — choose between: (a) in-EPUB condensed wiki/glossary spine document linked via `doc-glossref`, or (b) strip wikilinks from distributed EPUBs and replace with endnotes. Decision needed before Birukoff epub goes to distribution.
- [ ] **Update chapter XHTML templates** to use `epub:type` + `role` pairs on all interactive reference elements — never `epub:type` alone. Key pairs: `noteref`/`doc-noteref`, `glossref`/`doc-glossref`, `footnote`/`doc-footnote`
- [ ] **Document `doc-glossref` as canonical wikilink representation** in the Manual of Style skill (`skills/manual/`) — the pattern for how wikilinks appear in EPUB output vs. in the PWA

---

## Open questions (from log)

### Concept pages (2026-04-10)
- "Tolstoyism"-avvisningsbrevet: vilken volym i Jubilee Edition? Mottagare? År?
- *On Anarchy* (1900): Jubilee Edition vol. 34 eller annanstans? Hitta den ryska fulltexten.
- Vilka specifika 1894-recensioner myntade "Christian anarchism"? Kolla Christoyannopoulos.
- Ska Aylmer Maude få en egen personsida? Refereras i båda konceptsidorna men saknar wiki-entry.

### Bethink Yourselves (2026-04-07)
- Första ryska publiceringsdatumet okänt — cirkulerade via Chertkovs London-kanaler.
- Wikidata QID saknas.
- Medöversättaren "I. F. M." oidentifierad — Isabel F. Mayo?

### TEI ingestion (2026-04-06–07)
- Tatyana Tolstaya: gift Sukhótin — vilken namnform ska vara primärtitel? Bör vara konsekvent med citeringar.
- Yasnaya Polyana: TEI anger "1847" för att Tolstoj ärvde godset — dubbelkolla mot Birukoff.
- TEI-personbeskrivningar är enbart ryska — engelsk prosa syntetiserad men overifierad. Alla sidor har `recordStatus: draft`.

---

## Brainstorming

### Institutionsgranskning — stresstesta projektet
Gå igenom projektet ur en kritisk akademisk institutions perspektiv. Identifiera svaga punkter innan de hittas utifrån. Fokusområden:

- **Källkritik:** Är varje faktapåstående i wikin spårbart till en namngiven primärkälla? Finns det sidor med ogrundade påståenden?
- **Upphovsrätt:** Finns det material i projektet som kan ifrågasättas juridiskt? Bilder, texter, skanningar — vad är public domain och vad är oklart?
- **Akademisk trovärdighet:** Hur ser projektet ut för en forskare som granskar det? Vilka svagheter skulle de peka på?
- **Tonläge:** Finns det formuleringar i wikin som kan uppfattas som ideologiska snarare än sakliga?

Se PRINCIPLES.md för projektets hållning till dessa frågor.


---

## Completed

- ~~Testa end-of-day-skillen~~ — Testad 2026-04-14. Triggar korrekt, flödet fungerar.
- ~~Korrektur-app: pipeline-design~~ — Pipeline-workflow (typogrify → clean → semanticate som batch) designat och testat 2026-04-15. 30 Playwright-tester gröna. Appen byggs vidare av Johan (se prio 1).
- ~~Skalbarhet-rapport~~ — Färdig 2026-04-15. Slutsats: Obsidian som redigeringsverktyg, LightRAG + Ollama som nödvändigt query-lager. LightRAG-setup nu aktiv prioritet (prio 2).
- ~~PRINCIPLES.md~~ — Skapad 2026-04-16. Redaktionell hållning, tonläge, förhållningssätt till institutioner, beredskap för kritik.
- ~~LightRAG grundinstallation~~ — 2026-04-18. Qwen2.5:7b (14B passar inte 24 GB). Första ingestion OK. Prestandarapport i `_generated/`.
- ~~Korrektur Slice 1.C~~ — 2026-04-18. Autosave, git checkpoint, search & replace. 19+59 tester gröna.
- ~~Korrektur-appen~~ — Lagd på is 2026-04-22. Ersätts av macOS split-screen + git som checkpoint-system (se johan-workflow.md).

---

## Deferred (low priority)

- 15 works saknar `.data.yaml`-sidecar-filer (skapas när djup metadata finns tillgänglig)
- De flesta works-sidor har minimal prosa — wikilink-densiteten ökar i takt med att prosa skrivs
- Byta till PR-workflow (fas 6 i implementationsplanen — inte aktuellt under R&D-fasen)
