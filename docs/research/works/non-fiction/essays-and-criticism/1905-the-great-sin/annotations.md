---
layer: reference
title: "Reader annotations — The Great Sin (2026-07-03 read-through)"
lastUpdated: 2026-07-03
tags: [research, annotations, the-great-sin]
---

# Reader annotations — The Great Sin

Reader (Johan) annotations captured while reading the finished English read-along
edition (*A Great Iniquity*, the 1905 Chertkov & Mayo translation) in Thorium on
2026-07-03. Per the convention, annotations are **interpretive steer**, kept out of
the bare dive (`index.md` / `dossier.yaml` unchanged). They steer the next
session — a re-dive/enrichment pass and the wiki ingestion that follows.

Raw Thorium export preserved beside this file as `annotations.thorium-export.json`
(18 highlights). Each item below cites the sentence ID in the reader edition so a
future session can find the exact spot.

The items sort into three destinations:
- **A — Re-dive / ingestion steer** (the interpretive digs; the bulk).
- **B — Reader-edition text fixes** (missing emphasis, wanted footnotes).
- **C — Audio** (pronunciation + pausing; these join the audio backlog in the
  reader bundle's `alignment-notes.md`, not the dive).

---

## The standing steer (the headline)

> "Here's why the new title *A Great Iniquity* is very bad: 'iniquity' resides in a
> system of money and ownership and governments. 'Sin' is a religious word, so
> changing *The Great Sin* is completely rever[s]ing the perspective. Also notice
> how 'A' instead of 'The' is softening the stance. We need to investigate what
> influence the editor of *The London Times* had on T/Chertkov, if any."
> — on `p-10-14-s1` (Part IX)

Johan's central concern: the English title reframes the work. «Великий грех» = *the*
great **sin** (religious, absolute); *A Great Iniquity* = *an* **iniquity**
(one wrong among many, systemic/legal). The re-dive should treat the title itself
as an interpretive act and trace who chose it.

**What the dive already has** (build on this, don't re-derive): `dossier.yaml`
`workRecord.titleAlternatives` records *A Great Iniquity* as the 1905 English
translation by **V. G. Chertkov & Isabella Fyvie Mayo**, first published in **The
Times (London), 1 Aug 1905**, and reprinted as the Free Age Press pamphlet
(Internet Archive `greatiniquity00tolsuoft`). The conditional-endorsement
translator's footnote is already noted in the scholarship layer.

**For the re-dive:** (1) trace the title choice — was "Iniquity/A" Chertkov & Mayo's,
or shaped by *The Times* (editor 1905 = George Earle Buckle) as a condition of
running it? Look for Chertkov↔Times correspondence and the pamphlet's own front
matter. (2) Add **Isabella Fyvie Mayo** as an entity (co-translator, not yet in the
10-entity set) — she is central to this question. (3) Record the title-as-reframing
finding; the works-schema `titleAlternatives` field already exists to hold the
variant, but the *interpretation* (why the English softens) is dive/ingestion work.

---

## A — Re-dive / ingestion steer

### A1. The keystone reservation, "footnote 13", and two questions the essay leaves open
`p-10-11-s2` (Part IX) — on *"…the method of solving the land problem has been
elaborated by Henry George to such a degree of perfection that, under the existing
State organization and compulsory taxation it is impossible to invent any other
better, more just, practical, and peaceful solution."*

> "The key sentence in the whole essay and emphasized in the online version. […]
> This is an important point: T doesn't see this as the full solution. The religious
> awakening is the solution, not Henry George's practical solution for a world with
> governments and landed property. The sentence is confusing though since it praises
> HG's proposal as 'perfection', 'impossible to invent any better' etc. Perhaps we
> can look in the drafts to find out if T used different phrasings. My personal
> reflection: this is one of two major unresolved issues that are never addressed in
> the essay. #2: how can you have money if you remove the evils of landed property?"

Johan also transcribed the full **translator's footnote** (his "footnote 13") from
the online English version — the note explaining that Tolstoy recommends George's
scheme *only* under conditions of state organisation and compulsory taxation, and
that under his Christian teaching there would be neither.

**Dive status:** this is the dive's own keystone clause (index Stage 4; the «при
существующем государственном строе…» quote) and the translator's footnote is
already cited in the scholarship layer. So the *tension* is known.

**For the re-dive:** (1) pull the key sentence's wording from the **variants**
already extracted (`extracts/v36_464_475_Velikij_greh_Varianty.txt`) — did Tolstoy
phrase the reservation more sharply in a draft? (2) Quote footnote 13 in full in the
enriched dive (it is Chertkov/Mayo's own gloss, 1905 apparatus — primary, not later
scholarship). (3) Name Johan's **two open questions** explicitly in the dive's
`needsReview`/`notCovered` or a "questions the essay leaves open" note:
(a) George's "perfection" vs. the religious-awakening remedy — praise and reservation
in one breath; (b) money itself — how a moneyed order survives once landed property
is abolished. These are reader-facing framings the dive can hold honestly without
resolving.

### A2. Henry George as a religious, not merely economic, figure
`p-10-13` (Part IX) — on *"The ground is plowed; the seed is set; the good tree will
grow. So little now; only the eye of faith can see it."*

> "The solution of Henry George is often labelled as 'Single tax' but he keeps
> repeating the same words as T about faith and religion as the means to remove
> landed property."

**For ingestion:** enrich the **Henry George** entity (already ingested) with this —
George's own faith/"eye of faith" language, which Tolstoy quotes approvingly. Sharpens
why Tolstoy adopted him: not as an economist but as a fellow religious reformer. Ties
to the title question (A2 is why "sin" fits George too, not just Tolstoy).

### A3. Tolstoy's own definition of "religion"
`p-8-6-s1`, `p-8-7`, `p-8-8-s1` (Part VII).

> "being religious is leading a rational life." — on *"rational life"* (`p-8-6-s1`)
>
> "The definition of Religion from T should not be confused with neither the academic
> nor theological explanation." — on *"Without religion one cannot really love men…"*
> (`p-8-7`)
>
> "another explanation of what T considers Religion and this is including people
> outside of 'Christian' nations." — on *"religious people—that is, by people who are
> serious, simple, laborious… for the fulfillment before God of their human
> vocation"* (`p-8-8-s1`)

**For ingestion:** "religion as the ground of social change" is already a listed theme,
but Johan wants Tolstoy's **definition** surfaced as its own thread — religion ≠
academic/theological doctrine; = a rational life lived before God; a capacity that
crosses the Christian/non-Christian line. A candidate concept page (or a sharpened
theme note) for the vault. This is the hinge of Part VII (why reformers "have no
religion" and so cannot love or know what the people need).

### A4. Anti-governmental / anarchism
`p-8-6-s1` (Part VII) — on *"these men, both governmental and anti-governmental, who
are organizing the welfare of the people, have no religion."*

> "important point and the core of T. anti-governmental could be referring to the
> anarchists."

**For the re-dive:** the "anti-governmental" reformers Tolstoy faults alongside the
governmental ones — does he mean the anarchists? Connects directly to the dive's
existing scholarship anchor (**Wenzer 1997**, who reads Tolstoy's single-tax
endorsement against his "Christian anarchism"). Worth a note distinguishing Tolstoy's
position from political anarchism, read critically (per the "ground in primary, not
mainstream" convention — don't let the "anarchist" label stick uncritically).

### A5. Reads differently now — "none of this happened"
`p-10-4-s1` (Part IX) — on *"It is this feeling in regard to landed property which
must awaken in the well-to-do classes."*

> "The change will occur through an inner awakening. We of course know nowadays that
> none of this happened."

**For the dive:** a reception / critical-distance note — the essay stakes everything
on a moral awakening that history did not deliver. Not a correction to make, but a
frame the enriched dive can acknowledge (how the conscience-not-legislation thesis
reads a century on).

### A6. Phrasings flagged "wording" (candidate keystone quotes)
Johan tagged several passages simply "wording" — read these as the quotable/keystone
lines to make sure ingestion captures, and to cross-check against the online version's
emphasis (see B1):

- `p-4-1-s5` (Part III) — *"most obvious evil, private property in land"*
- `p-5-8-s2` (Part IV) — *"private landed property is an evil which should be abolished"*
- `p-6-6-s1` (Part V) — *"parasites"* (the «русские паразиты» self-indictment thread —
  already in the dive)
- `p-6-8-s1` (Part V) — *"pseudo-defenders of the people"*
- `p-7-3` (Part VI) — the Theology-vs-Science passage (*"…the teaching which they call
  Science… already on their conscience there lie rivers of blood…"*)
- `p-7-7-s2` (Part VI) — *"Hence stakes, inquisitions, slaughters in the former case,
  and executions, imprisonments, revolutions, and manslaughters in the latter."*
  (Johan: "Wording about Church and Science respectively.")
- `p-10-9-s6` (Part IX) — *"As then the Church justified the serf right, so now that
  which occupies the place of the Church—Science—justifies landed property."*

The Church↔Science parallel (`p-7-3`, `p-7-7-s2`, `p-10-9-s6`) recurs three times —
a strong candidate for a keystone quote / theme thread in ingestion.

---

## B — Reader-edition text fixes (not the dive)

**B1. Missing emphasis (transcription fidelity).** The reader `.md` carries **no
emphasis markup at all** (0 italics), but the online English version italicises key
phrases. Johan flagged two:
- `p-3-12-s4` (Part II) — *"minimum"* — tagged **Transcription**, "is emphasized in the
  online version."
- `p-10-11-s2` (Part IX) — the keystone reservation sentence (A1) — "emphasized in the
  online version."

Decide which English edition's emphasis is authoritative (the 1905 Times/Free Age Press
text vs. the "online version" Johan compared), then restore italics in
`the-great-sin.en-1905.md`. Restoring emphasis also re-synthesises those sentences'
audio (same wav-cache rule as the pronunciation fixes — delete the clip's wav).

**B2. Wanted footnotes / glosses.**
- `p-4-7` (Part III), the Labouchère passage — "I feel this p should get more
  explanation + footnote." (Labouchère is a candidate vault person too.)
- `p-5-2-s1` (Part IV), *"political economy"* — "means what exactly and what did it mean
  to T?" — a gloss/footnote clarifying the 19th-c. sense.

---

## C — Audio (joins the backlog in `../../reader/.../alignment-notes.md`)

- `p-10-6-s1` (Part IX) — **"Alexander II"** is read as letters; should be "Alexander
  the Second." Tagged **Pronounciation**. Fix like Kvas: a respelling in
  `reader/speech.py` `_SUBS` (e.g. `Alexander the Second`) + delete that clip's wav.
- Carried over from Johan's 2026-07-03 listen: the **Kvas** and **"I asked"** items
  (already logged), **"other pronunciations"**, and **pausing between paragraphs and
  after headings** (the `PARA_GAP` / `CHAP_GAP` tuning). All deferred, not blocking.

---

## Derived work-order for the re-dive session

1. **Title provenance (the headline).** Trace who chose "A Great Iniquity"/"A" over
   "The Great Sin"/"The" — Chertkov & Mayo, or *The Times*? Start from the dive's own
   leads (Times 1 Aug 1905; IA `greatiniquity00tolsuoft`). Add **Isabella Fyvie Mayo**
   as an entity.
2. **The keystone reservation.** Pull the sentence's wording from the variants extract;
   quote footnote 13 in full; name Johan's two open questions in the dive.
3. **Enrich two entities / concepts:** Henry George (his faith/religion language, A2);
   Tolstoy's definition of "religion" (A3) as a concept thread; note the anarchism
   question (A4).
4. **Keystone quotes.** Fold the "wording"-flagged lines (A6), especially the
   Church↔Science parallel, into ingestion.
5. **Route B & C out of the dive:** the reader-text emphasis/footnotes (B) and the
   audio items (C) are not dive work — they land in the reader bundle. Listed here so
   nothing is lost.

---

## Second read-through (2026-07-04)

A finer pass over the finished edition, listening and reading line by line. The
first five notes (the professions list, the two "I asked" clips, Kvas, "$1.40")
were already resolved by the 2026-07-03 audio pass and are not repeated here. The
new digs below extend — they do not replace — sections A/B/C above.

### New re-dive / ingestion steer

- **The title is Tolstoy's own phrase, used inside the body.** `p-9-3-s1`
  ("undoing **the great sin**") and the peasant scene in Part VII ("the great, the
  old sin") show «великий грех» recurring in the text itself. So the English title
  *A Great Iniquity* diverges from a phrase Tolstoy repeats in his own voice —
  concrete support for the standing title-reframing concern (headline, top of file).

- **"Employment" is Henry George's English, not a translation artifact** (`p-3-8`,
  Part II). That whole passage — including "$1.40 a day" and "Adam had no difficulty
  in finding employment, neither had Robinson Crusoe" — is Tolstoy *quoting George*.
  The oddity Johan flagged (Crusoe had *work* but could not have *employment*) is in
  George's own text; in the Russian essay Tolstoy quotes George in Russian, and the
  Chertkov/Mayo edition restores George's English wording. For the re-dive: identify
  the George source of the Part II quotations and note this as a translation-layer
  point, not a mistranslation.

- **Two registers for the wrong of private property: "sin/evil" (religious) and
  "injustice" (secular).** `p-4-1-s5` "most obvious evil, private property in land";
  `p-4-3-s1` "the evil and injustice of private property"; `p-5-8-s2` "an evil which
  should be abolished"; `p-4-4-s2` "fundamental injustice be destroyed". Tolstoy
  leans on the religious register but reaches for the legal/secular one too. Johan
  flags "destroyed" (`p-4-4-s2`) as unclear — what mechanism of abolition is meant
  (and is it Tolstoy or George being quoted there?). Extends A6.

- **Who is entitled to the land: those who cultivate it.** `p-8-10-s12`
  "the seizure of the land by those who do not cultivate it is a great sin", and the
  recurring "lawful / legitimate right to the land" (`p-9-8` area, `p-10-5-s2`). This
  is the use-right / labour-desert principle. Johan's question on `p-10-5-s2`: *which*
  law — natural/God's law (a birthright to use land) or State statute (which denies
  it)? Worth surfacing as its own thread; ties to Henry George's natural-rights case.

- **"Government became ashamed" — change by conscience, not legislation** (`p-9-8-s1`,
  the serfdom-emancipation analogy). Reinforces A5 and the Alexander II passage
  (`p-10-6`): emancipation came from men who felt the sin, not from the decree.

- **Phrases flagged for the translation-diagnostic / voice notes:**
  - `p-5-4-s2` "strength of nations" — reads oddly against Tolstoy's rejection of
    patriotism; here it is descriptive/critical (militarism and commerce *exhaust*
    the nations' strength), not an endorsement of national greatness. Confirm against
    the Russian.
  - `p-5-5-s2` "Russian people in Russia" — redundant in English; likely «русский
    народ в России» distinguishing the home peasantry from Russians/Europeans abroad.
  - `p-6-10-s2` "dying-out" — "the dying-out and entangled European and American
    nations"; Tolstoy's decay-of-the-West framing.
  - `p-4-1-s5` "flesh-eating" — listed among the evils (with militarism and war) but
    set below private property in land as the "most obvious". A vegetarianism touch;
    keep it period-accurate, don't harden into a later label (cf. ingestion-accuracy).

- **`political economy`** (`p-5-2-s1`) — Johan wants this as a concept/wikilink: the
  19th-c. discipline vs. what the term meant to Tolstoy. Carried from B2; now a
  concept-page candidate for ingestion.

- **The keystone reservation, reconfirmed** (`p-10-11-s2`) — the italics are the
  **author's own** (the translator's footnote states the words were "italicised by
  the author himself"). So restoring the emphasis in the reader text (B1) is faithful
  to Tolstoy, not to the translators. The tension and Johan's two open questions are
  already logged at A1.

### Audio — this session

Resolved in `reader/speech.py` + the edition `.md` (pending the next audio rebuild):
- `bytheir` → `by their` (`p-6-11-s1`, text typo).
- `Alexander II.` → `Alexander II` in the text; speech respell → "Alexander the Second".
- `per cent.` — kept on the page (archaic abbreviation), speech drops the dot's stop.
- Part IV policy list (`p-5-4-s1`) — full-stop-flattened for air, like the Part I list.

Still open — **short-phrase pitch ceiling** (Kokoro rises on a 2–4 word clip
synthesized alone): section headers "Part I / Part IV…", "But we are wrong."
(`p-7-3-s1`), "Why is this?" (`p-8-4-s1`), the terminal "…their parasites."
(`p-6-6-s1`), and the wanted pause after "God," (`p-7-8-s2`). The welfare list
(`p-6-7-s1`) is an infinitive-phrase list, messier than the two noun lists — not a
clean full-stop flatten. These need the audio-only merge mechanism (a `speechGroup`
field that keeps read-along granularity) or acceptance as a model limit.

---

## Dive-index read-through (2026-07-11)

The first pass Johan made over the **dive `index.md` itself** (not the reader
edition). IDs like `[p-0-1]` are the index's own rendered paragraphs. Where the
earlier sections A/B/C steered *what to add*, most of these steer *how the dive's own
prose frames the work* — so they land differently (see "the scope question" below).

**The throughline — the dive prose editorialises.** The recurring charge across
these notes: the index imports modern political-economic labels that are **not in
Tolstoy's text** — *land monopoly*, *single tax as its remedy*, *Socialist-
Revolutionaries*, *George-derived*, *Georgist-Tolstoyan* — and by doing so files a
religious/moral argument under libertarian/economic categories. Worse, the academic-
debate framing (note 8 → 7) stages a false binary ("does the single tax compromise
his anarchism?") that **misdirects from the question Johan holds central: why is
landed property a sin but not money or other private property?** Johan reads this as
the same move as priests who call themselves Christian — correct labels used to
divert from the property critique. This is calibration for the overview and the wiki
ingestion, and (open question) possibly for the dive prose itself.

### The notes

1. **`[p-0-1]` "he calls land monopoly"** — Tolstoy speaks of land "completely
   monopolised" in passing but overwhelmingly calls landed property *cruel and
   sinful*; he does not frame it as "land monopoly." Using that keyword ties T/Henry
   George to a modern libertarian/anarchist reading. *(New — objects to the index's
   word, not the source.)*

2. **`[p-0-1]` "endorses Henry George's single tax as its remedy"** — "single tax"
   never appears in the text. Tolstoy endorses George's *plan*, but as a measure
   *under present conditions*; the actual remedy is the voluntary religious awakening
   by which owners come to see landed property as immoral and abandon it — as chattel
   slavery came to be seen. Single tax is not "the remedy." **Explicitly not a request
   to change the overview** — Johan's point is calibration: "we need to be very careful
   with what words we use; the last thing I want is people being told what Tolstoy
   thinks before they've read him." *(Substance logged at A1; newly aimed at the index
   prose + stated as a principle.)*

3. **`[p-1-3]` "Tolstoy endorses Henry George's single tax"** — same: he endorses HG's
   *plan*, does not mention a single tax. *(Same as 2, second index spot.)*

4. **`[p-1-6]` «Необходимый переворот» — translation.** = **"A Necessary Revolution"**
   (literally *a necessary overturning/upheaval*). The title Chertkov gave the cut
   paragraph he printed separately. *(New; the index glosses it lower down but not at
   this first occurrence — a Russian-gloss-consistency point.)*

5. **`[p-6-2]` the variants = "the essay Tolstoy would have preferred to print"** —
   Johan: since tolstoy.life wants to be the voice of Tolstoy, we should somehow
   *feature* the cut material (PSS variants, Tom 36 pp. 464–475). *(New — a
   product/editorial idea, ties to A1's "pull the variant wording.")*

6. **`[p-6-1]` "Gorbachev"** — the cut-analysis rests on the PSS scholar's (Gorbachev's)
   textual research; Johan doesn't doubt it but feels we lack **Tolstoy's and Chertkov's
   own voices and their dialogue about the cuts.** *(New — foreground the primary
   exchange over the secondary apparatus; the dive has «Мне жалко» + «стоит в
   противоречии» but wants more.)*

7. **`[p-7-11]` "contradiction of Tolstoy's 'anarchism'"** — for Johan the big
   contradiction in the text is between **landed property and money / other private
   property** — a *religious* question. Framing it as T's "hypocritical anarchism"
   shifts focus off "why is money not also evil." "I feel this is a deliberate
   misdirection." *(Extends A1 open-Q #2 + A4; the misdirection charge is new.)*

8. **`[p-9-2]` "Academics split over whether the single tax compromises Tolstoy's
   'anarchism'…"** — "This is the misdirection in full bloom. The academics debate two
   sides of the text in order to establish that one of them must be right." *(New — the
   scholarship framing itself is the problem.)*

9. **`[p-10-2]` "moral-economy register ('iniquity') rather than the literal 'sin'"** —
   Johan: "I've added a note on these two titles before." *(Already logged — the title
   headline at the top of this file.)*

10. **`[p-11-1]` "Socialist-Revolutionaries"** — odd narrowing. Tolstoy's "revolutionists"
    include the anarchists/libertarian socialists **and** the Marxist communists and
    socialists; he faults them all — plus Social Democrats and Liberals (and, Johan
    adds, Conservatives) — as hypocrites who use reform to avoid abolishing landed
    property outright. If the dive calls the socialists/communists/anarchists sinful it
    must include the reformist camps too. *(New.)*

11. **`[p-11-1]` "Tolstoy's George-derived position rejected both as sinful"** — "Really
    bad sentence." Tolstoy doesn't call them sinful *because he read Henry George and
    derived that opinion from him.* Reducing a religious conviction to an economic
    borrowing is "editorializing that I don't like." *(New.)*

12. **`[p-11-2]` "Georgist-Tolstoyan"** — "Too categorizing. T is not a follower of HG,
    he's a follower of Christ." *(New — extends the "don't let labels stick" rule.)*

13. **`[p-13-1]` «Мне жалко» — translation.** = **"I regret it"** / literally "I feel
    sorry." Diary, 6 June 1905, over Chertkov's cuts. *(New; glossed earlier in the
    index, bare at this paragraph.)*

### Resolved (2026-07-11): leave the old dive; the corrections live in the re-dive

Johan's decision: **we are doing a re-dive, so the old machine dive stays untouched** —
`index.md` and `dossier.yaml` remain the honest-but-tool-shaped substrate (loaded labels
and all), kept as the historical record. The corrected framing does **not** get edited
into the old dive; it is carried into the **re-dive products** — the refined overview, the
wiki entities, and the works record.

So notes 1, 2, 3, 7, 8, 10, 11, 12 become a **constraint on the re-dive, not an edit to
the substrate.** The re-dive must not reproduce the phrases that *misstate the text*:

- **"land monopoly"** (dive `[p-0-1]`, Stage 3 head) — Tolstoy names *private ownership
  of land / landed property* the great sin; "land monopoly" is not his framing.
- **"single tax as its remedy" / single tax as the remedy** (`[p-0-1]`, Stage 4 head) —
  the remedy is the moral/religious awakening by which owners come to abandon landed
  property; George's scheme is only a conditional measure "under the existing state and
  its taxes." (The dive's own Key-Findings bullet already states this correctly — the
  offenders are the abstract lede and the stage heads.)
- **"Socialist-Revolutionaries" / "Marxists… rejected both as sinful"** (`[p-11-1]`) —
  too narrow: Tolstoy's "revolutionists" span the anarchists/libertarian socialists *and*
  the Marxist communists/socialists, and he faults the reformist camps too (Social
  Democrats, Liberals). The re-dive should not single out two parties as "the" targets.
- **"George-derived position"** (`[p-11-1]`) — a religious conviction, not an economic
  opinion borrowed from George. Don't reduce the moral judgment to its practical source.
- **"Georgist-Tolstoyan"** (`[p-11-2]`) — don't categorise Tolstoy as a Georgist; "he is
  not a follower of Henry George, he is a follower of Christ." Name the reception strand
  by its works, not the label.

The interpretive steer (the misdirection critique, the money-vs-land religious question,
featuring the variants, foregrounding the Chertkov–Tolstoy cutting dialogue, and the
enrichments in sections A/B) also feeds the re-dive, not the old substrate.

## Wiki page notes — Giuseppe Mazzini (2026-10-02)

Johan's notes on `docs/research/wiki/Giuseppe Mazzini.md`, kept as steer for this and later wiki pages.

1. `[p-1-1]` The ch. VIII epigraph. Minimise Russian in the sentence and move it to a footnote. The quotation is an important part of the text and deserves a pull quote; there, the Russian can be revealed on demand instead of footnoted.
   - Tolstoy would point out that "religious movement" means people's own convictions, not the established church, which serves the legal and economic system. Most people take "the church" to mean organised religion.
   - Bears on the "Christian anarchist" label: for Tolstoy, as for Jesus, change comes from inside (*The Kingdom of God Is Within You*), from faith, not from political action, least of all the violent methods associated with anarchists.
   - Open question: was Tolstoy more inclined to quote political activists in this period than in *The Great Sin*? The smallest change of wording can change how a message is perceived. Wiener turning "a Christian" into "Christianity" in Tolstoy's preface to *The Kingdom of God* is one example. Wordings that make Tolstoy political instead of religious need weighing with caution. His definition of religion is not the conventional one either, so calling him "religious" can be used to pull his stand toward the mainstream. These moves are at work on Wikipedia and in the Standard Ebooks text of *The Kingdom of God Is Within You* (Wiener).
2. `[p-2-1]` «Избранные мысли Иосифа Мадзини» needs a translation.

### What was done (2026-10-02)

- Pull quote: decided as at most one per page, only where the quotation is the subject's tie to Tolstoy; the Russian opens under it (`<details>`). Mazzini is the first.
- "Religious movement": answered from the essay itself — ch. VIII's next paragraphs say what the movement is and what it is not (reforms, socialism, revolution, philanthropy, government). No interpretation added.
- The PSS commentary calls the epigraph a "paraphrased and shortened" quotation (anthology p. 5, thought 4).
- Not on this page: Tolstoy's definition of religion vs the Church, and "Christian anarchist" — each wants its own page from his definitions. The quoting-political-figures question is a dive, logged as an open question on the page.
