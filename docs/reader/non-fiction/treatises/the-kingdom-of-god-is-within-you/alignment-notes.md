# The Kingdom of God Is Within You — alignment and capture notes

How the three texts in this bundle were made paragraph-parallel, so that paragraph N of section K points to the same place in the work in every version. This is **stage 1**: the preface and chapters I–III. Stages 2 (IV–VIII) and 3 (IX–XII) will add sections at the end; nothing here will need redoing.

- `the-kingdom-of-god-is-within-you.ru.md` — the Russian, PSS vol. 28 («Царство божие внутри вас», 1890–93). The spine every other version lines up to.
- `the-kingdom-of-god-is-within-you.en-garnett.md` — Constance Garnett's translation (Cassell, New York, 1894; Project Gutenberg #43302). The reading text and the read-along.
- `the-kingdom-of-god-is-within-you.en-machine.md` — the project's raw machine translation from the Russian file, one pass, unproofed.

All three segment to **4 sections / 357 paragraphs** and pass `reader.segment --spine-json`.

## Johan's decisions (2026-10-03)

1. **Tolstoy's chapter summaries are in.** Each chapter section opens with its title and short list of contents, in the Russian and the English. They are Tolstoy's own (PSS prints them as «Оглавление», vol. 28, pp. 294–306; Garnett prints them under each chapter number).
2. **The preface heading is ours.** The Russian preface has no heading; the reader needs one to make it a section. «Предисловие» / "Preface" (Garnett and Maude print "Preface"). The three Bible epigraphs open the preface section.
3. **Garnett's translator's preface (January 1894) is left out** of the reading text. It is mentioned in the overview.
4. **Garnett's slips get footnotes**, in A Confession's form: *Our note, not Garnett's.*, then the Russian and a literal English. Her wording is never changed.
5. **A machine translation is in the bundle**, as the third witness where the published translations disagree.
6. **Wiener is not in the bundle** for now. His text stays in `primary-sources/standard-ebooks/` for checks (quote his wording from the 1904 scan, not the e-text, which modernises words).

## Section and paragraph numbers

The preface is section 1, so **chapter I is section 2, chapter II section 3, chapter III section 4**. Paragraph ids follow: chapter I's paragraphs are `p-2-1`, `p-2-2`…; chapter III's are `p-4-…`. Annotations on this bundle carry these ids.

In each chapter, paragraph 1 is the chapter title and paragraph 2 Tolstoy's summary, so the first paragraph of the chapter text is paragraph 3. The ¶ numbers in the dive's `church-passages.md` count chapter III's text without the title and summary: **dive ¶n is paragraph n+2 here** (dive ¶33 = III.35 = `p-4-35`).

## The Russian

Extracted fresh from the TEI (`extract_tei.py --choice=reg --notes=auto`). The new extract is identical to the dive's of 2026-06-06 — the footnote fix of 2026-06-07 changed nothing in this work.

- **Chapter titles and summaries** come from the PSS contents (TEI file `v28_294_306_…_Oglavlenie.xml`). The body of the text has only the chapter numbers.
- **The two headings inside chapter I** — Garrison's «Провозглашение основ…» and Ballou's «Катехизис непротивления» — are plain lines in capitals, not `## ` headings, so chapter I stays one section. Neither the reader nor the EPUB renders bold, so there is no bold anywhere.
- **No italics**, as in A Confession's Russian: the extractor drops them. The PSS has about 120 italic passages in the whole work; they could be added later if wanted.
- **Footnotes.** The nine footnotes in stage 1 are Tolstoy's own (PSS notes 43–51; the extractor keeps their numbers but drops their text, so the text was taken from the TEI). Note 3 is the exception: its Russian «[Весь мир судить легкомысленно.]» is in square brackets in the PSS, meaning the editors supplied it, not Tolstoy. The brackets are kept.

### Text fixes (transmission errors only)

Checked against the scan of PSS vol. 28 in `primary-sources/jubilee-edition/vol88/vol88.pdf` (the folder numbers are offset: `vol88` is Tom 28). Printed page = PDF page − 42.

- **I.13 «Бостон, 1838 г.»** — the extractor turned the italic year into a footnote marker («Бостон,¹⁸³⁸ г.»). Restored.
- **I.112, Dymond: «Я не могу участвовать в совете правительства»** — "I cannot take part in the council of government". The TEI and the Jubilee fb2 both read «не могу *не* участвовать» ("I cannot help taking part"), which inverts the sense; the printed page (p. 19) has no second «не». Fixed in the Russian and the machine translation. Garnett has it right.
- **Note 9 (the Russian of the long Pressensé passage, III.66)** — the TEI note stops mid-sentence at «то разве мы не вправе», where the footnote runs on to the next printed page. The rest is restored from the Jubilee fb2 and checked against the scan (pp. 51–52).

### Oddities left as printed

- **The French of the Pressensé passage (III.66)** has misspellings: «Un tipe doctrinal», «on la dissent» (for *dissout*), «en voulant fair d'Epicure où de Zénon», «la doctrine universellement repoussé». They are printed so in the PSS (p. 51). Garnett's text has them corrected.

### Spot-checks against the scan

The preface (p. 1: epigraphs and first four paragraphs), Dymond's answer (p. 19), the Pressensé passage and note 9 (pp. 51–52): all match the Russian file word for word, apart from the fixes above. The Latin-letters-inside-Cyrillic sweep is empty.

## Garnett

From the local Gutenberg copy (`primary-sources/project-gutenberg/…constance-garnett.epub`), converted with its italics and footnotes. Her wording is untouched. Only paragraph breaks were moved, at sentence ends, and every paragraph's opening and close was read against the Russian, not just counted.

- **Front matter.** Her own "Translator's Preface" (which the Gutenberg file also heads "PREFACE.") is left out (decision 3). Her contents list is left out; the three epigraphs, which she prints after it, open the preface section. Tolstoy's preface ends in her edition with "L. Tolstoy. / Yasnaïa Poliana, *May 14/26, 1893*." The PSS prints no signature or date; they stay at the end of the last preface paragraph, as in A Confession with Maude's dates.
- **Headings.** "CHAPTER I." etc. become `## I`; the chapter title (in her capitals) and summary are paragraphs 1 and 2. Her inset headings "DECLARATION OF SENTIMENTS…" and "CATECHISM OF NON-RESISTANCE." are plain lines.

### Splits and joins

Garnett paragraphs differently from Tolstoy far more often than Maude did in A Confession. Chapter by chapter:

- **Chapter I** (Garnett 122 paragraphs → 136): Garrison's Declaration is Garrison's own English original, paragraphed differently from Tolstoy's Russian version: six joins and three splits there. In Ballou's quotations, three paragraphs joined into one (I.34). Splits through the Helchitsky, Dymond and Musser passages. Ballou's signature "Adin Ballou." joined to the last line of the catechism.
- **Chapter II** (54 → 76): splits only — most of them where Tolstoy opens a new paragraph after a colon, and the recruiting-board dialogue (II.41–52), which Garnett runs into three paragraphs.
- **Chapter III** (125 → 135): seventeen splits, eight joins and one empty paragraph (below). Garnett ends many paragraphs a sentence before or after Tolstoy: III.24, III.33, III.73, III.75, III.92, III.101 and III.105 are each two of her paragraphs; III.135 begins with the sentence she puts at the end of III.134.

The exact list is in the appendix at the end of this file.

### Places that could not be split cleanly

- **I.35/36 — half a sentence.** The Russian ends I.35 with «Но сколько именно нужно людей для этого?» and opens I.36 with «Вот в чем вопрос.». Garnett makes them one sentence ("But precisely how many people must there be to make it so?—that is the question."), which stays at the end of I.35.
- **II.38/39 — half a sentence.** The Russian ends II.38 with «И это удается.»; Garnett runs it into the next sentence ("And in this they are successful; for, indeed, how could…"), which opens II.39.
- **I.84/85 — split mid-sentence, as the Russian does.** Tolstoy breaks Ballou's last sentence before the motto: I.84 ends «…добровольно подчиняющейся закону Христа:» and I.85 is «Не противься злу насилием». Garnett's sentence is split at the same point ("…every soul who obeys willingly Christ's word," / ""Resist not evil." Adin Ballou.").
- **Two English paragraphs are empty.** Garnett has nothing for two Russian paragraphs. The English keeps an empty paragraph there (a hidden CriticMarkup note, which the reader and the audio skip), so the numbering stays in step, and the paragraph before carries an *Our note* footnote saying what is missing:
  - **I.56** «Вот предписания, о которых говорит Иисус» ("These are the precepts Jesus speaks of") — left out by Garnett (Wiener has it).
  - **III.120** «Положение их таково, что им нельзя не напрягать все усилия на то, чтобы скрыть учение Христа…» — Garnett folds III.119 and III.120 into one sentence ("Uniform is the attitude of all the churches to the teaching of Christ, whose name they assume for their own advantage."), losing "to hide the teaching of Christ". Found during this alignment; not in the dive's list.

### Footnotes

23 in stage 1. Seven are Garnett's: her English for Tolstoy's footnotes (his own remarks, and his translations of the French and German catechism and Pressensé passages, which she keeps in the original in the text). Sixteen are ours, each beginning *Our note, not Garnett's.*:

- **Her slips** (decision 4): the preface's "absence of any commandment" («непризнание заповеди», "non-recognition"); III.35 "the assertion of the Church" (plural «церквей»); III.37 "miracles" for «иерархией» ("hierarchy"); III.78 "Heresy makes its appearance in the Church" (drops «проявление движения», "a manifestation of movement") and, two sentences on, "understanding" without "fulfilling"; III.82 "stagnation" / "progress" for «неподвижность» / «движение»; III.103 "the holy love of Christ" for «нравственный закон Христа» ("Christ's moral law"); III.116 "the true teaching" for «истинного, деятельного учения» ("the true, active teaching"); III.134 "the men who constitute the Church" for «учреждение церквей» ("the institution of the churches"); and the new III.119/120 note above.
- **What she leaves out**: Tolstoy's own footnote to Ballou's catechism heading («Перевод сделан свободно, с некоторыми пропусками», "The translation is made freely, with some omissions"); the I.56 line.
- **Foreign words she leaves untranslated**: *securus judicat orbis terrarum* (Latin, Augustine), *du charmant docteur* (French, Renan), *Ubi Christus, ibi Ecclesia* (Latin), Arnold's German book title, *l'infâme* (French, Voltaire).

Each footnote says whose it is: *Tolstoy's note.* (in all three versions; «Примечание Толстого.» in the Russian), *The PSS editors' translation.* for note 3 of the Russian and machine versions, and *Our note, not Garnett's.* for ours. Garnett's text of Tolstoy's notes keeps her straight quotation marks; ours use curly ones.

## Machine translation

Translated from the Russian file, paragraph for paragraph, in one pass, unproofed, as for The Great Sin and A Confession. Literal where literal and readable conflict; Tolstoy's repetitions kept. The French, German and Latin stay as they stand in the Russian text, with Tolstoy's nine footnotes translated (note 3 keeps its brackets). The headings mirror the Russian: the chapter titles in capitals, the preface heading ours.

## Appendix — every split and join in Garnett

Each line names the words in Garnett where a paragraph break was added or removed, in the order applied. Generated from the build markers.

**Preface**

- joined, on its own line, to the paragraph before: “L. Tolstoy.”
- joined, on its own line, to the paragraph before: “Yasnaïa Poliana”

**Chapter I**

- joined to the paragraph before: “"The dogma that all the governments”
- new paragraph before: “If we cannot occupy a seat”
- joined to the paragraph before: “"We advocate no Jacobinical”
- new paragraph before: “It appears to us a self-evident truth”
- joined to the paragraph before: “"But while we shall adhere”
- joined to the paragraph before: “"Having thus stated our principles”
- new paragraph before: “We shall endeavor to promulgate”
- joined to the paragraph before: “"We expect to prevail”
- joined to the paragraph before: “"In entering upon the great work”
- joined to the paragraph before: “"For this we have a succession”
- joined to the paragraph before: “"I see all this”
- new paragraph before: “One man cannot plunder and pillage”
- empty paragraph after: “foot."—Deut. xix. 18, 21.”
- new paragraph before: “In this way, if all kept the ordinance”
- new paragraph before: “Peace, then, to all who seek peace”
- new paragraph after: “obeys willingly Christ's word,”
- joined, on its own line, to the paragraph before: “Adin Ballou.”
- new paragraph before: “In this laudatory notice”
- new paragraph before: “Precisely as it was with all the preaching”
- new paragraph before: “This primitive Church was his special”
- new paragraph before: “The greater fishes who broke”
- new paragraph before: “Helchitsky teaches precisely”
- new paragraph before: “But apart from its interest from every”
- new paragraph before: “But nothing of the kind has occurred, and the same fate”
- new paragraph before: “They say: "We give”
- new paragraph before: “But this is not right.”
- new paragraph before: “This book is devoted to the same question”
- new paragraph before: “"It is well known that there are many”
- new paragraph before: “"Bethink yourselves”
- new paragraph before: “As for the question of the principle itself”
- new paragraph before: “"Christians do not need government”
- new paragraph before: “Christ took his disciples out of the world”

**Chapter II**

- new paragraph before: “In my book I made it an accusation”
- new paragraph before: “According to these people's notions”
- new paragraph before: “This assertion is an absolute assumption”
- new paragraph before: “This is a very skillful device”
- new paragraph before: “This method of reply is employed”
- new paragraph before: “"Tolstoy came to the conclusion”
- new paragraph before: “You expect, then, that in answer”
- new paragraph before: “What this error consists in is not made clear”
- new paragraph before: “What a pity he has not”
- new paragraph before: “And in this they are successful”
- new paragraph before: “It is just what has taken place of late years”
- new paragraph before: “"What is he muttering?"”
- new paragraph before: “"Speak louder,"”
- new paragraph before: “"I—I as a Christian”
- new paragraph before: “And at last it appears that the young man”
- new paragraph before: “"Don't talk nonsense.”
- new paragraph before: “"Yes." "Reverend”
- new paragraph before: “"Reverend father, administer”
- new paragraph before: “"Go along, go along”
- new paragraph before: “And they lead the trembling youth away.”
- new paragraph before: “The freethinking Russian critics”
- new paragraph before: “The Russian advanced critics”

**Chapter III**

- new paragraph before: “Even the strongest current of water”
- new paragraph before: “Eighteen hundred years ago there appeared”
- new paragraph before: “In place of all the rules of the old religions”
- new paragraph before: “Instead of the threats of punishment which all”
- new paragraph before: “No proofs of this doctrine were offered”
- new paragraph before: “There are no acts in this doctrine”
- joined to the paragraph before: “Succeeding generations corrected”
- new paragraph before: “It was thus from the very earliest times of Christianity.”
- joined to the paragraph before: “That is, it was asserted that the correctness”
- new paragraph before: “If the Catholics assert that the Holy Ghost, at the time”
- new paragraph before: “And these bodies, having in course of time”
- new paragraph before: “"L'église est une libre association”
- joined to the paragraph before: “"Does not all history show”
- joined to the paragraph before: “"And is not the fact that there was no heresy”
- new paragraph before: “To instill into the people the formulas”
- joined to the paragraph before: “Then it is instilled into the child as it is brought up”
- new paragraph before: “All this is regarded as faith obligatory”
- joined to the paragraph before: “This was spoken of the Pharisees”
- joined to the paragraph before: “The teaching of every Church, with its redemption”
- new paragraph before: “There you have an epitome”
- new paragraph before: “And is not the same thing done in Anglicanism”
- empty paragraph after: “whose name they assume for their own advantage.”
- new paragraph before: “All these propositions, elaborated by men”
- new paragraph before: “They need special supernatural efforts.”
- new paragraph before: “It is only due to the intense zeal of the churches”
- joined to the paragraph before: “Let the Church stop its work”
