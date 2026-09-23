# Audiobook pipeline — reference & findings

Agent-facing reference for the local TTS audiobook pipeline. The working code, text, and a shorter README live in [`projects/audiobook/`](../projects/audiobook/). This doc is the durable record of *what was learned* and *why each setting is what it is*, so a future agent doesn't re-derive it.

Last updated: 2026-06-28.

## Goal

Publication-quality local audiobooks for tolstoy.life works — one `.m4b` per work, beside the existing EPUBs. Long-term: an incremental nightly job that generates audio only for new/changed works and writes `_generated/audio/<work>.m4b`.

## Status

- **A Great Iniquity** is fully built: `a_great_iniquity_bm_daniel.m4b` (54:45, 10 chapters, mastered, Books-importable).
- The central open question — *is Kokoro good enough, or do we need a heavier model?* — is **settled: Kokoro is enough.** No OpenAudio/Chatterbox needed.
- Narrator: **bm_daniel** (British male). Chosen deliberately over bm_emma, the strongest *performer*, because a narrator should disappear, not impress.

## Stack

- **kokoro-tts-tool** — Kokoro-82M, runs locally on Apple Silicon. 24 kHz native.
- **ffmpeg / ffprobe** — silence, concat, mastering, M4B mux.
- **espeak-ng** — Kokoro's g2p backend.

## Findings (the hard-won ones)

1. **Use `synthesize`, not `infinite`.** This was *the* fix that took the result from "improved" to "amazingly good." The `infinite` command (built for long-form streaming) adds a processing step that mangles the ends of long sentences — a pre-final pause plus a high-pitched last word. The plain `synthesize` command renders a single sentence cleanly. An A/B on two long sentences confirmed it; `synthesize` clips were also ~0.5 s tighter.

2. **Synthesize one sentence at a time; splice silence between.** Kokoro has no SSML. The W3C standard for pauses is SSML `<break>`, but Kokoro can't read markup — so explicit per-unit synthesis + inserted silence is the correct workaround, not a hack.

3. **Pause lengths** (seconds): sentence `0.45`, paragraph `0.85`, Part break `2.0`. Grounded in: ACX/Audible section breaks 2–2.5 s; TTS engine defaults ~0.3/0.4 s (too short for long-form); prosody research (period ≈ 0.8–1.2 s total incl. the voice's own fall). **Never insert silence at commas** — chopping intra-sentence destroys Kokoro's pitch contour and sounds robotic.

4. **Spell out Part headers.** Kokoro reads `Part II` as "Part two-eye." The build converts `Part <Roman>.` → "Part One/Two/…"; the M4B chapter *list* keeps Roman numerals (they read better visually).

5. **Spell out money.** `$1.40` → "one dollar forty" (done in the flow text, not the source — the source keeps the real characters).

6. **Respell the verb "live" → "liv".** Kokoro otherwise says /laɪv/ (as in "live broadcast"). Whole-word only; "lives/lived/living" untouched.

7. **Auto-join page-break-split paragraphs.** OCR/extraction splits some paragraphs mid-sentence. Rule: a paragraph not ending in `. ! ? " ) …` was split by a page break → glue it to the next. Replaces hardcoded per-chapter join indices.

8. **M4B must mux with `-movflags +faststart`** or iOS Books silently refuses to import it (moov atom must precede mdat).

9. **Mastering chain** (the LibriVox-fatigue fix — what makes spoken word pleasant): `highpass=f=70,deesser=i=0.4,loudnorm=I=-19:TP=-2:LRA=7`. Output 44.1 kHz, 128k AAC. Kokoro is 24 kHz native — that's the fidelity ceiling; higher bitrate is wasted.

10. **Per-call model reload (~5 s).** `kokoro-tts-tool` reloads Kokoro on every invocation, so the ~410-sentence book takes ~40 min cold. Fine for now (the build is resumable). For the nightly pipeline, batch synthesis in one process.

12. **Merge very short sentences into a neighbour — but at the SEGMENT level, not the build.** A 2–4 word clip synthesized alone rises instead of falling — Kokoro can't land a declarative cadence without runway ("But we are wrong."). The original `merge_short` lived in `build_audiobook.py` and was **removed**: merging *after* `segments.json` changed the sentence count, which broke the read-along contract (1 sentence = 1 SMIL `<par>` = 1 highlight). The correct home is `reader/segment.py` (`merge_speech_groups`), which glues the pair *before* `segments.json` is written — so clips, timing, and SMIL all stay consistent and the pair simply highlights as one read-along unit (2026-07-04). Which sentences merge is an **explicit id list** (`reader/speech.py` `MERGE_FORWARD`), **not** a word-count rule — a blanket "short sentence" rule would wrongly flatten legitimate rising *questions* ("Why is this?", "Whence this dreadful perversity?"). It does **not** fold "Part One." into the first sentence (that would span an `<h2>`+`<p>`, which one highlight can't) — headings that rise when spoken alone are an accepted limit; finding #4's Roman→word conversion still applies.

13. **Pronunciation respellings live in a `SUBS` dict in the build**, applied at synth time so the source text stays faithful (same place as `live`→`liv`). Validated by ear (auditioned against the raw reading): `Labouchere`→ `Labooshair`, `Radischeff`→`Rahdeeshef` (Radishchev), `Yasnaya Poliana`→ `Yasnaya Polyahna`, and the scripture ref `(Matt, xxiii. 27, 28)`→spoken "Matthew twenty-three, verses twenty-seven and twenty-eight". Novikoff, Komaroff, Decembrists, Toynbee, Parnell were auditioned and left as-is.

14. **Split over-long sentences** so Kokoro doesn't speed-read them (a ~90-word sentence gets compressed and rushed). The build now reads flow text generated with `flow_preprocess.py --split-long 45` — sentences over 45 words split once at the comma nearest the middle. Same fidelity trade-off as the semicolons (adds a full stop Tolstoy didn't write), accepted for listenability.

16. **Probe pronunciations with espeak-ng IPA before auditioning by ear.** `espeak-ng -v en-gb -q --ipa "<word>"` prints exactly what the g2p will hand the voice — respelling candidates can be screened in seconds without synthesizing anything. Found this way (2026-07-03, voice-notes pass): a word-initial **kv- cluster is unreachable** — English phonotactics has none, so espeak letter-names the K ("Kvas"/"kvass"/any kv-spelling → two-syllable "kay-v…"). Dictionary English kvass is /kvɑːs/ (like "kvetch"), but the closest the engine can be *spelled* into is `quahss` → /kwɑːs/ — accepted. espeak's raw-phoneme notation (`[[kvA:s]]`) works in espeak itself but is mangled by the phonemizer layer inside `kokoro-tts-tool`, and the CLI exposes no phoneme input — a true /kv/ would need driving kokoro-onnx directly with hand phonemes (one-off, cache-fragile; not done).

17. **Measure prosody with parselmouth — don't guess by ear alone.** `pip install praat-parselmouth`; `Sound(wav).to_pitch()` gives the F0 contour, short-time RMS gives pause lengths. The objective probe for "does this rise or fall" (companion to finding #16's espeak IPA probe). Settled two things this way (2026-07-04): (a) a **rising terminal appositive** — "…support us, their parasites." rose to ~149 Hz on the closing tag; swapping the comma for an **em-dash in speech only** ("support us — their parasites.", page keeps the comma) drops it to ~111 Hz so it falls. (b) **Comma pause length is a fixed Kokoro constant (~140 ms) — no lever.** Measured: slowing to `--speed 0.93` keeps commas at ~145 ms (it stretches the *words*); commas→semicolons gives ~147 ms (Kokoro treats them the same). The only thing that lengthens a comma is a full stop, which resets pitch — so it's a per-spot tool (finding #5's lists, the "God," pause), never a global default.

15. **The text we narrate is the 1905 Mayo/Tchertkoff translation, verbatim.** A line-by-line check against the Russian original confirmed the phrasings that sound odd ("clambered out" = слезла; "exhaustion of the strength of nations" = истощение сил народов; "Socialistic organisation" = социалистическое устройство — Tolstoy's own word for the educated classes' engineered future society, not a translator's narrowing) are faithful, not transcription errors. The only real defects were transcriber artifacts, now fixed in `chapters/`: the "Transcription/Markup: Andy Carloff" credit line (removed), a stray editorial "(?)" in ch03 (removed), and a missing space in ch04.

11. **Sideloaded audiobooks don't iCloud-sync** (by design). Manual import only: AirDrop → Files → Share → Copy to Books, or Finder cable sync. EPUBs/PDFs sync; audiobooks never have.

## Model landscape (June 2026), for the record

Better-than-Kokoro free models exist (Chatterbox, OpenAudio S1, Qwen3-TTS, Orpheus) but they win on *expressiveness*, which is a liability for neutral long-form Tolstoy (they "act," wander, and hallucinate words more). Kokoro ties commercial engines on clean-read naturalness (UTMOS ~4.48) and is notably clean — the right tool here. SSML only really exists in cloud engines; the one free high-quality SSML path is `edge-tts`, rejected because it's online + an undocumented endpoint (this pipeline is deliberately local).

## How to run

From `projects/audiobook/`:

- `python3 build_audiobook.py [voice]` — full book → `a_great_iniquity_<voice>.m4b` (resumable; reads `chapters_flow/`).
- `python3 build_audiobook.py --dry` — print chapter/sentence structure only.
- `python3 audition.py` — render the 3 hardest sentences in each listed voice.
- `python3 flow_preprocess.py` — semicolon/punctuation reshaping `chapters/` → `chapters_flow/`.

## Open questions / next

- **Semicolon fidelity** (philosophical, Johan's call): the build narrates the flow text, where George's semicolons are rewritten. Now that `synthesize` phrases well, test narrating the *original* punctuation and possibly retire `flow_preprocess` — resolving the fidelity question by making it moot.
- ~~**Short-sentence pitch wobble**~~ — **resolved** (finding #12, segment-level `speechGroup` in `reader/segment.py`; the old build-level `merge_short` was removed).
- ~~**Proper-noun pronunciation**~~ — **resolved by ear** for the names that actually fumbled (finding #13). Remaining names validated as fine. Read-along would still let a reader *see* any future fumble.
- **One footnote idea** (parked): "Socialistic organisation" is Tolstoy's literal word but his referent is the whole engineered Western future-society (liberal + social-democrat + socialist). Worth a translator's footnote in a future read-along/EPUB edition — not the audio.
- **Incremental nightly pipeline** — hash each work; regenerate on change; Whisper transcript validation (catches dropped/repeated/mispronounced words); per-work proper-noun substitution dict; `_generated/audio/<work>.m4b`.
- **Read-along** (synced text + audio highlight) — strongest for the philosophical works (anchors proper nouns). EPUB3 Media Overlays + per-sentence timing that falls out of this pipeline almost for free. See `projects/audiobook/IDEAS.md`.

## Decisions log

- Narrator is a **synthetic/actor voice, never Johan's own** (non-native; a publication edition needs a consistent neutral house voice).
- **Daniel over Emma** — fit over performance.
- Altering Tolstoy's punctuation for audio (semicolons → periods): **still open.**
