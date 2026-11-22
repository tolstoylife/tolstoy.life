# Bethink Yourselves! — alignment notes

How the three versions in this bundle share one paragraph coordinate (paragraph N in any version points to the same place in the work): the 1904 English of Chertkov and Mayo (`bethink-yourselves.en-1904.md`, the read-along edition), the Russian of PSS Tom 36 (`bethink-yourselves.ru.md`), and the 1904 Swedish *Betänken Eder!* (`bethink-yourselves.sv-1904.md`).

The English defines the shape: 13 sections (I–XII and the postscript), 117 paragraphs. It was taken from Project Gutenberg #27189 (Ginn & Company for the International Union, Boston, 1904, reprinted from *The Times*); page markers were removed, the three translators' notes became footnotes, and the heading "Postscript" was added. Its wording is otherwise untouched.

The Russian and the Swedish were fitted to it. In both, only paragraph breaks were moved; the words are unchanged and were checked word for word by script against their sources. Where a version has nothing opposite an English paragraph, the slot holds a hidden note (`{>>…<<}`), as in The Kingdom of God, so the numbering stays in step.

**Decisions taken by Johan (2026-10-24):** the Swedish goes on the research site lined up with the other two, keeping every 1904 Swedish chapter title; Johan's ePub (`projects/betanken-eder/`) keeps the 1904 layout.

**Engine changes made for this bundle:** `reader.segment --missing-tail N` lets a version end N sections early (the Swedish has no postscript); the sentence splitter now also starts a sentence at Å, Ä, Ö and » (checked: no other edition's sentences changed). Swedish sentences that end inside a closing » are still not split, so some Swedish read units are long.

## The Russian


How `bethink-yourselves.ru.md` («Одумайтесь!», PSS Tom 36, pp. 100–148) was made paragraph-parallel to `bethink-yourselves.en-1904.md` (Chertkov & Mayo, 1904), so the two share one paragraph coordinate. Same method as The Great Sin (`the-great-sin/alignment-notes.md`).

Source: `docs/research/works/non-fiction/essays-and-criticism/1904-bethink-yourselves/extracts/v36_100_148_Odumajtes.txt`. The English is the incumbent and defines the shape; the Russian wording is untouched and only paragraph breaks were moved, always at a sentence end.

**Result:** `reader.segment --spine-json build/segments.en-1904.json` → "13 sections, 117 paragraphs", no count error. Every paragraph pair was checked by first and last sentence (all 117 correspond). A script confirmed the file's words, minus headings, footnote syntax and the one hidden note, equal the extract's main-text words minus the epigraphs, in order, and also character-for-character once whitespace is normalised. The only things removed from the main text are the PSS superscript note numbers ²⁷ and ²⁸, which became `[^1]` and `[^2]`.

**Totals:** 45 merges, 4 splits, 1 empty placeholder paragraph (XI).

### Break adjustments per section

"Native" = main-text paragraphs in the extract after the epigraphs are removed. R0, R1… number those native paragraphs from 0.

| Section | Native | Target | Adjustment |
|---|---|---|---|
| I | 5 | 5 | merge R1+R2+R3 («Люди, десятками тысяч…» + «Что же это такое?…» + «Но нет, это не сон…»); split R4 twice: before «Но как могут так называемые просвещенные люди…» and before «Все знают, не могут не знать главного…» (2 merges, 2 splits) |
| II | 7 | 7 | split R1 before «Ученые юристы, господа Муравьев и Мартенс…» and merge its first two sentences (the tsar's and the Japanese emperor's proclamations) onto R0 «Совершается что-то непонятное…» (1 merge, 1 split) |
| III | 7 | 5 | merge «Вспомнишь всё это…» + «То, что единственно отличает человека…»; merge «Непосредственное чувство…» + «И ошалевшие, озверевшие люди…» (2 merges) |
| IV | 7 | 5 | merge «Спросите журналистов…» + «Точно так же объяснят…» + «То же скажет кажущийся виновником всего дела царь…» (2 merges) |
| V | 10 | 7 | merge «Ничто очевиднее речей господина Муравьева…» + «Мы разогнались к пропасти…»; merge «Для всякого разумного человека…» + «Не говоря уже об экономических…» + «Так что же делать?» (3 merges) |
| VI | 7 | 6 | merge the Emperor's speech: «Прежде чем меня короновали…» + «Люди говорят мне, что я должен делать это…» (1 merge) |
| VII | 5 | 4 | merge «Человеку нет выбора…» + «А большинство людей нашего времени лишено ее.» (1 merge) |
| VIII | 10 | 7 | merge «Возможно ли это?» + «Не только возможно, — отвечу я…» + «Невозможно людям не одуматься…»; merge «Ответ этот в скрытом состоянии…» + «Только бы уничтожились эти два обмана…» (3 merges) |
| IX | 10 | 9 | merge «Вы с ужасом говорите…» + first sentence of «Но если справедливо то…»; split that paragraph before «Так что даже становясь на вашу шаткую точку зрения…»; merge «В этом особенность деятельности религиозных людей.» + «И потому-то и спасение людей…» (2 merges, 1 split) |
| X | 13 | 11 | merge «Любить желтых людей…» + «И что же мы делали и делаем с ними?..»; merge «А между тем религия, отвечающая требованиям…» + «Так что единственно верное средство…» (2 merges) |
| XI | 21 | 19 | merge «Пешая саранча…» + «И вот первый нижний слой…»; merge «И что же, начинают понимать свой грех…» + «Толкуют о потере храброго Макарова…»; merge «Разве не ясно…» + «Ищите Царствия Божия…»; add an empty placeholder paragraph at the end opposite the English dateline (3 merges, 1 placeholder) |
| XII | 45 | 30 | merge the «Котлин» appeal with its last line «Довольно сентиментальничать»; merge «И начатое ужасное дело продолжается…» + «Царь, главное ответственное лицо…» + the Soyen Shaku paragraph (2); merge «Но нет, они не говорят этого…» + «Убьют ли, искалечат ли…»; merge «Он задумался.» + «— Как же быть-то?…»; merge «Вчера я получил… два письма.» + «Вот первое:»; first letter, 4 paragraphs into 1 (3); second letter, 4 paragraphs into 1 (3); merge «Я спросил:» + «— Что это, телеграмма?»; merge «Он остановился.» + «— Это вчерашняя…» + «Он достал другую из кармана…» (2). Dateline «30 Апреля 1904 г.» kept as its own paragraph opposite "13 May, 1904." (15 merges) |
| Постскриптум | 9 | 2 | ¶1 = «Я никогда бы не кончил…»; ¶2 = the sailor's letter plus everything after it, merged: the address line, the four closing paragraphs («Прямо словами я не могу ответить…» to «…великая радость.») and the date «8 Мая 1904 г.» (8 merges) |

### Epigraphs

The 1904 English has none of them, and at first the Russian left them out too, so the two would line up. Since 2026-11-22 they are back in the Russian (189 extract lines: the title epigraph and 46 chapter epigraphs). Each is a quoted block (`> …`) under its heading, its source on a last line starting with "— "; the reader keeps epigraphs out of the paragraph numbering, so no paragraph moved. A script confirmed that every epigraph line is a line of the extract and that, with the epigraphs taken out again, the file is the same as before apart from the note numbers (see Footnotes). The list below gives the number of quoted sources per chapter.

Chapter V: the TEI and the Jubilee fb2 both print the sources «Hardouin.» and «(Из частного письма русской матери. Март, 1904 г.)» together after the mother's letter, although the eyewitness passage is Hardouin's (the PSS notes name his article in *Le Matin*; Maude puts "Hardouin" after it). The file keeps the order of the PSS e-texts, as one epigraph with both source lines; worth a look at the page image.

- **Title (1):** «Ныне ваше время и власть тьмы». — Лука, XXII, 53.
- **I (3, 8 lines):** «Только беззакония ваши были средостением…» (Исаия); «Ограничимся тем, что напомним…» (Молинари); «Но война более уважаема, чем когда-либо…» (Гюи де Мопассан).
- **II (4, 17 lines):** «И Микромегас сказал…» (Вольтер); «Безумие современных войн…» (Анатоль Франс); «Дикий инстинкт военного убийства…» (Летурно); «Иногда один властелин нападает на другого…» (Джонатан Свифт).
- **III (5, 16 lines):** «Война образует людей, перестающих быть гражданами…» (Чаннинг); «Наступил возраст военной службы…» (Альфонс Карр); «Они берут человека во всей силе…» and «Ты, может быть, по неопытности…» (Клод Тилье); «И я понял дисциплину…» (Эркман-Шатриан); «Я купил негра, он мой…» (Questions sur l'Encyclopédie… Art. Esclavage).
- **IV (4, 11 lines):** «Удивительно, до какой степени, благодаря дипломатии…» (Рише); «Может ли быть что-нибудь нелепее…» (Паскаль); «Обитатели земной планеты…» (Фламмарион); «Когда изучаешь не поверхностно…» (Патрис Ларрок).
- **V (4, 23 lines):** «Мысль о ужасом останавливается…» (Э. Род; «о» for «с» is the extract's); «Очевидец рассказывает…» (Hardouin); «В «Русских Ведомостях» я прочла…» (Из частного письма русской матери. Март, 1904 г.); «Вы спрашиваете, необходима ли еще война…» (Гастон Мох). The extract puts «Hardouin.» after the mother's letter, not after the eyewitness passage; immaterial here since all of it is dropped.
- **VI (6, 13 lines):** «Заканчивая свою миссию, Иисус…» (Ламенэ); «Нельзя не признать того, что XIX век…» (Кетлэ); «Все люди одного происхождения…» (Иосиф Мадзини); «...Нет, призываю в свидетели возмущение совести…» (Альфред де Виньи); «Человек так же мало сотворен…» (Консидеран); «Если бы мои солдаты начали думать…» (Фридрих II).
- **VII (5, 17 lines):** «Существует распространенное мнение…» (Саведж); «Религия есть высший и благороднейший деятель…» and «В глубине всех вер…» (Морис Флюгел); «Ни одно общество не может существовать…» (Мадзини); «Человек может рассматривать себя…» and «Истинная религия есть…» (Л. Толстой); «Религия (рассматриваемая объективно)…» (Кант).
- **VIII (5, 15 lines):** «Не делай того, что осуждает твоя совесть…» and three more (Марк Аврелий); «Просвещение есть выход человека…» (Кант); «Нужно высвободить ту религию…» (Амиель); «Я признаю следующее положение…» (Кант); «В сущности есть только одно средство почитания Бога…» (Лихтенберг).
- **IX (3, 41 lines):** «Письма крестьянина, отказавшегося от военной службы» / «1895 года Октября 15-го дня…» (Из книги «Письма П. А. Ольховика»); «27-го Января 1894 года в больнице Воронежской тюрьмы…» (Из книги «Жизнь и смерть Дрожжина»); «Облекитесь во всеоружие Божие…» (Послание Павла к Эфесянам).
- **X (4, 17 lines):** «...Божьи люди это та таинственная соль…» (Ориген против Цельзия); «Я сознаю в себе силу…» (Кросби); «Можно с полным основанием сказать…» (Кант); «Когда я говорю тебе о Боге…» (Эпиктет).
- **XI (4, 9 lines):** «Изумительное и ужасное совершается в сей земле…» (Иеремия V, 30, 31); «Народ сей ослепил глаза свои…» (Иоан. XII, 40); «Самое прекрасное оружие…» (Лао-Тзе); «Если бы путешественник увидал…» (Лихтенберг).
- **XII:** none.

Attribution of a few multi-part quotations (III Тилье, VII Флюгел and «Л. Толстой») is read from the order of lines in the extract, not checked against the page; it doesn't affect the spine.

### A later English with the epigraphs (checked 2026-11-22)

Aylmer Maude's translation in *Recollections and Essays* (Oxford, World's Classics, 1937; Tolstoy Centenary Edition, pp. 204–271; [archive.org scan](https://archive.org/details/recollectionsand035475mbp), also [the 1937 printing](https://archive.org/details/in.ernet.dli.2015.76705)) prints the title epigraph and the chapter epigraphs, so it is a witness for how they read in English. It follows the printed pamphlet, not the manuscript: no Origen epigraphs in VIII, the X Origen epigraph without its opening, none of the XI ¶8 ending, none of the two Novikov passages in XII. It does have the postscript's closing paragraphs and the date "May 8th, 1904". Maude's footnotes are signed "A. M." and none mention Chertkov's changes. No Free Age Press English with the epigraphs was found. Read from the archive.org text (OCR), not the page images.

The PSS already prints the chapter IV epigraphs in the manuscript order (Richet, Pascal, Flammarion, Larroque), so Chertkov's change 1 needs only a note in the restored version, not a change of text.

### Footnotes

The extract keeps the PSS note numbers but not their text; the text was taken from the TEI (`primary-sources/tolstoydigital-TEI/texts/works/v36_100_148_Odumajtes.xml`), which holds only the first paragraph of each note, and completed from the Jubilee fb2 (`primary-sources/jubilee-edition/vol05/vol05.fb2`, sections n27 and n28). Labels follow The Kingdom of God's Russian file.

- **[^2] (XI, PSS note 27, after «…et voilà tout.»)** Two parts: *Перевод редакции ПСС.* — the editors' bracketed Russian for the four French lines; then *Примечание Толстого.* — «Вылежинский прибавляет от себя: «Фельдмаршал не думал тогда…». The second part is the 1904 English's footnote 1. In the fb2 everything after the first French line is in pre-reform spelling; I modernised it mechanically (ъ, ѣ, і, -аго), and replaced two Latin «c» inside «уcтупокъ» and «манифеcтъ» with Cyrillic. The closing » of the Vylezhinsky quotation is missing in the fb2 and is left missing. The italic «х» in «условия<em>х</em>» is kept as printed. Worth a check against the page image.
- **[^3] (XII, PSS note 28, after «…нужно воевать и убивать людей.»)** *Примечание Толстого.* — «В статье сказано: «Тройной мир принадлежит мне…» … («The Open Court», May, 1904. Buddhist Views of War. The Right Rev. Soyen Shaku).» Matches the 1904 English footnote 2. The TEI stops after the first paragraph; the remaining six paragraphs are from the fb2, joined into one line. One fix: «(То the bitter end.)» had a Cyrillic «То», changed to Latin «To». Not yet checked against the scan.
- PSS note 26 («[Имей мужество быть мудрым.]», the editors' translation of Kant's «Sapere aude») sits in the VIII Kant epigraph. It came back with the epigraphs on 2026-11-22 as [^1], so the notes are numbered in reading order: the two notes described above are now [^2] (XI) and [^3] (XII).
- The 1904 English footnote 3 (now [^4]: "The letter is written in a most illiterate way… (Trans.)") is the translators' own; the printed "(Trans.)" was dropped 2026-11-22, since the label *Translators' note.* says the same; the Russian has nothing there, and needs nothing, since it prints the sailor's spelling as is.

### Content the English leaves out (Russian kept)

- **Postscript, after the sailor's letter:** the address line («Следует адрес: Порт-Артур…») and Tolstoy's four closing paragraphs, «Прямо словами я не могу ответить этому милому, серьезному человеку…» through «И знать и чувствовать это — великая радость.», plus the date «8 Мая 1904 г.». All merged into postscript ¶2. The PSS commentary dates the «Прямо словами я не могу ответить» insertion to 20 May 1904, the last addition to the article, which likely explains why the 1904 English lacks it.
- **XI ¶6:** Dibich's accented repeat «Tis mille hommes et foilà dout» — the English gives only his words in English and moves on.
- The English also translates the French dialogue (XI ¶3–6) into English in the text; the Russian prints the French, with the editors' translation in [^1].
- Smaller differences inside paragraphs (one Russian sentence rendered as two, or two as one) were not itemised. A length check across all 117 pairs found no other paragraph that looked short on either side.

### Content the Russian lacks

- **End of XI, "May 2, 1904."** The PSS reading text has no dateline after chapter XI. The Russian gets an empty paragraph there, a hidden CriticMarkup note that the reader and audio skip, as The Kingdom of God's English does for its gaps, so the numbering stays in step. No wording was invented. If a dateline is wanted, the attested one is Tolstoy's own on the typed copy of chapter XI, «17 апреля 1904 г.» per the PSS commentary (`v36_604_621`); that is 30 April by the western calendar, not 2 May, so the English date's source is unclear. Open for Johan.
- The XII dateline: English "13 May, 1904." and Russian «30 Апреля 1904 г.» are the same day in the two calendars.

### Not touched (worth a look)

- Two Latin letters sitting inside Cyrillic words in the main text, left as in the extract because the wording rule is byte-for-byte: **«нe»** (IX, Latin e) and **«зa»** (XI, Latin a). The Great Sin repaired the same kind of fault; these are candidates for the same fix.
- The heading of chapter I in the extract uses a Greek capital iota («Ι.»); irrelevant to the file, which uses `## I`.

## The restored Russian

`bethink-yourselves.ru-restored.md` (2026-11-22) is the text as Tolstoy left it in his corrected manuscript: the PSS text with V. G. Chertkov's proof-stage changes undone, as the PSS commentary lists them (N. V. Gorbachev, vol. 36, pp. 613–616). It keeps the PSS paragraph slots, so it lines up with the other three versions (13 sections, 117 paragraphs). The "Editorial changes" switch shows each restoration: switch off, a clean text; switch on, the restored words in green and what the print had instead struck through.

**Check:** a script took the restored file, dropped every addition, put back every struck-through word and removed the tolstoy.life notes; the result is exactly `bethink-yourselves.ru.md`. The restored passages themselves are copied from the commentary extract (`docs/research/works/…/1904-bethink-yourselves/extracts/v36_604_621_Odumajtes_comments.txt`).

**What was restored**, numbered as in the commentary:

1. **IV, epigraph order.** The PSS already prints the manuscript order, so nothing changes; a note says the first edition had them in the wrong order.
2. **VIII, two Origen epigraphs; X, the opening of the Origen epigraph.** Put back in full. The commentary does not say where in chapter VIII the two stood, so they follow the printed epigraphs; the source line «[Ориген против Цельзия.]» is ours, in square brackets. In X the printed «...» after the restored opening is kept.
3. **V, the paragraph «Мы разогнались к пропасти…».** In the manuscript it follows the paragraph ending «могущественные орудия истребления» (slot 4); Chertkov moved it to the end of slot 6. The restored version adds it at the end of slot 4 and strikes it through at the end of slot 6. ⚠ This one paragraph sits in a different slot in the restored version than in the PSS, English and Swedish.
4. **XI, the end of the paragraph «И что же, начинают понимать свой грех…»** («Видят ли те несчастные… с которой не может бороться человек.»).
5. **XII, the beginning and end of the second paragraph of Novikov's second letter.** The second paragraph is the one beginning «Я никак не могу установить внутреннего равновесия» (it opens with a new «). The commentary quotes the cut beginning only up to «так как...»; whether it went on is not known.
6. **XII, «множество» back to «несколько тысяч».**

**Not restored:** «большею частью пьяных» and «проклятые», which Chertkov proposed cutting before the proofs at Tolstoy's own request. They are not in the PSS text and nothing shows where they stood. A note in XII (on the last sentence of the first paragraph) says so.

**Notes.** Each restoration has a *tolstoy.life note.* in Russian (as the Swedish notes are in Swedish) giving the change, Chertkov's reason as the commentary reports it, and Tolstoy's approval of 1 July 1904 after the fact. The notes are numbered in reading order with the three PSS notes: 11 in all.

**Open for Johan:**
- The commentary prints «бог» in lower case in the restored passages (Origen: «истинного бога», «у бога», «богу»), as Soviet editions did; the PSS main text capitalises it («Божьи люди»). Kept as the commentary prints it for now; the manuscript surely had capitals.
- Two Latin letters in the commentary e-text were set as Cyrillic: «зa того» (Origen) and «a проявление» (XI). Nothing else in the restored passages was touched.
- In the Novikov letter the restored version is split into sentences differently from the PSS version (sentence ids are per version; there is no audio for the restored version).

## The Swedish

Output: `docs/reader/non-fiction/essays-and-criticism/bethink-yourselves/bethink-yourselves.sv-1904.md`, built from `projects/betanken-eder/betanken-eder.md` (read only, not edited). Coordinate: `bethink-yourselves.en-1904.md` (I–XII, 115 paragraphs without the Postscript).

### The big finding: the Swedish has no chapter IX

Swedish ch. 8 «»Du skall älska din nästa såsom dig själf.»» ends exactly where English VIII ends («…samt erkänna samma plikter såsom härledande sig ur lifvets innebörd.» = «…recognize one and the same duties as flowing from this meaning.»), and Swedish ch. 9 «Huru skall mänskligheten räddas…» opens with English X's first line («»Men hvad skola vi göra med de fiender som anfalla oss?»» = "But how about the enemies that attack us?"). None of English IX's nine paragraphs ("How are we to act now…", "But before the work of war was commenced…", "A religious man acts thus…") is anywhere in the Swedish; a search for its key phrases found nothing.

So the Swedish has 105 paragraphs of real text for 115 slots. To keep Tolstoy's chapters I–XII and pass the segmenter without inventing words, the ten empty slots hold a CriticMarkup comment paragraph, the same device the Kingdom of God Garnett file already uses («{>>Garnett has no counterpart to the Russian paragraph here…<<}»). The segmenter drops the comment, so each slot becomes a paragraph with no sentences:

- `## IX.` — nine slots: `{>>The 1904 Swedish has no counterpart to this paragraph: it leaves out chapter IX entirely.<<}`
- XI paragraph 19 — one slot: the English dateline "May 2, 1904." has no Swedish counterpart (ch. 10 ends without a date).

The first IX slot also carries one visible editorial line in brackets, so the reader sees why the chapter is empty: *[Kapitel IX finns inte i den svenska utgåvan 1904. Det kan läsas i den engelska eller ryska versionen.]* Apart from the footnotes (word glosses by the editor of the Swedish edition, each labelled *tolstoy.life note.*, added 2026-11-22 under AGENTS.md → "Footnotes in texts"), it is the only text in the Swedish file that is not from 1904. ⚠ If the file is ever rebuilt from `projects/betanken-eder/betanken-eder.md`, put the labels back. Whether IX should stay like this is open for Johan.

### Per section (native Swedish paragraphs → target)

Merges join adjacent Swedish paragraphs with a single space; splits cut at a sentence boundary. Native counts are after joining the four stray single line breaks in the source (ch. 1 «…talat om detta. / För att icke tala om Haag-konferensen…»; ch. 2 «Alla förära / hvarandra…»; ch. 3 «…barbari. / Och, än mer…»; ch. 3 «…i djupet af sin själ / känner…»).

- **I** (ch. 1): 6 → 5. Merge 2+3: «…vakna upp ifrån den.» + «Men nej, det är icke en dröm…» (English keeps "But no, it is not a dream" in paragraph 2).
- **II** (ch. 2): 7 → 7. No change.
- **III** (ch. 3): 7 → 5. Merge 2+3: «…insikten om det mänskliga förnuftets vanmakt.» + «Det enda, som skiljer människan från djuret…». Merge 6+7: «…icke längre kan underlåta att fullfölja det.» + «Och bländade, förvildade människor fortsätta sitt fasansfulla verk.»
- **IV** (ch. 4): 5 → 5. No change.
- **V** (ch. 5): 10 → 7. Merge 6+7: «…förbipasserande hund, som icke deltager i striden.» + «Vi störta framåt mot afgrunden…». Merge 8+9+10: «För hvarje förnuftig man…» + «För att icke nämna de ekonomiska problem…» + «Hvad är då att göra?»
- **VI** (ch. 6): 7 → 6. Merge 4+5: «»Innan jag kröntes, erkändes som kejsare»…» + «De bestå, sådana de uttryckts i den kristna lagen…».
- **VII** (ch. 7): 5 → 4. Merge 4+5: «…ty blott religionen gör människan fri.» + «Och flertalet af vår tids människor äro beröfvade densamma.»
- **VIII** (ch. 8): 11 → 7. Merge 2+3+4: «Är detta möjligt?…» + «Det är omöjligt för människorna att icke betänka sig…» + «I vår tid framlockar den inre motsägelsen…». Merge 5+6: «Detta svar lefver på ett latent sätt…» + «Om endast dessa två villfarelser utrotades…». Merge 9+10: «För att bringa det därhän, att vår tids människor enhälligt…» + «Människor, hvilka afsiktligt eller oafsiktligt fördumma folket…».
- **IX** (no Swedish text): 0 → 9 empty slots (see above). Heading `## IX.`
- **X** (ch. 9): 12 → 11. Merge 5+6: «Att älska de gula folken…» + «Och hvad hafva vi varit sysselsatta med att göra mot dem…».
- **XI** (ch. 10): 20 → 19. Merge 8+9+10: «För att hålla japanerna ifrån Mandschuriet…» + «För att eröfra andra folks land…» + «Ej nog med att dessa tusendens dödande…». Merge 12+13: «När krälande skaldjur passera en flod…» + «Det första undre lagret har redan börjat drunkna…». Merge 14+15: «Och hafva detta förfärliga verks upphofsmän…» + «Man talar om förlusten af den tappre Makarov…». Split ch. 10 paragraph 16 into three, one per newspaper quote: after «skrifver Novoje Vremja.» and after «skrifver Petersburgskija Vjädomosti.» (third part ends «skrifver Russ[^24]. O. s. v.»). Paragraph 19 = empty slot (dateline).
- **XII** (ch. 11 + ch. 12): 9 + 31 = 40 → 30. Ch. 11: merge 1+2 («Jag hade just afsändt det föregående…» + «Åter hafva slafvars råa och servila slafvar…»); merge 5+6+7+8 («Det rysliga verket fortsättes.» + «Tsaren, den främst ansvarige…» + «Militärerna, som äro upptränade…» + «På samma sätt går det till i Japan.…»). Ch. 12 begins at **XII paragraph 6** («När skall detta upphöra…» = "When will this cease…"); there it is now an ordinary paragraph break. Ch. 12: merge 1+2 («När skall detta upphöra…» + «Det vore så naturligt att säga detta nu…»); 3+4 («Men nej, de säga icke så…» + «»Huruvida vi skola blifva dödade», så tänka de…»); 10+11 («Han funderade en stund.» + «— Men hvad skall man göra, hvart kan man komma undan?»); 14+15 («I går mottog jag två bref…» + «Det första lydde så här:»); 17+18 («Det andra brefvet lydde så:» + «»Snälle Leo Nikolajevitsch!…»); 28+29 («På sin tid suckade Jesus i förväntan och sade:» + «»Jag har kommit för att kasta eld…»»). The dialogue lines 6–9 («— Farväl med dig…», «— Jaså, ämnar du slåss?», «— Ja, någon skall väl göra det!», «— Ingen behöfver slåss!») already match English 9–12 one to one. Paragraph 30 = «Leo Tolstoy.» in the slot of "13 May, 1904."
- **Postscript**: not in the Swedish; left out (`--missing-tail 1`).

Totals: 27 merges, 2 splits (both in one paragraph), 10 empty slots. 130 native − 27 + 2 + 10 = 115.

### Content differences noticed

Checked by reading the first and last sentence of every paragraph pair, not every sentence in between, so smaller gaps inside long paragraphs may remain unnoticed.

- **IX**: the whole chapter is absent (see above).
- **XI**: no dateline "May 2, 1904." at the end of ch. 10.
- **XII**: the English dateline "13 May, 1904." is replaced by the signature «Leo Tolstoy.»
- **XII paragraph 23**: the Swedish lacks the peasant's line "'This is yesterday's,—but here is one of to-day.'" and starts at «Han tog fram ett annat ur fickan.»
- **II paragraph 2**: the Swedish lacks "because of the seizure of other peoples' lands" after «den nuvarande äggelsen[^1] till krig».
- **XI paragraph 12–14**: in the Swedish the three newspaper quotes run as one paragraph; split to match English (see XI above).
- **Postscript** ("I should never finish this paper…" and the letter after it): absent.


### Checks run

- `python3 -m reader.segment … --missing-tail 1` → "12 sections, 115 paragraphs", no error.
- Wording: the word sequence of the new file (minus headings, `[^n]` markers, note definitions and the `{>>…<<}` slots) equals the word sequence of `betanken-eder.md` minus headings and `^[…]` notes: 11,216 words, identical. The 31 note texts are identical and in order, numbered `[^1]`–`[^31]`.
- Alignment: first and last sentence of every English/Swedish paragraph pair read side by side; all correspond.
