---
layer: reference
lastUpdated: 2026-06-11
tags: [research, corpus-dive, novel-dive, work-dive, drama, comedy, fiction, the-fruits-of-enlightenment, spiritualism, censorship]
---

# The Fruits of Enlightenment (Плоды просвещения, 1886–1890) — a corpus novel-dive

A single-work corpus dive on Tolstoy's four-act comedy *The Fruits of Enlightenment* (*Плоды просвещения*), written across 1886–1890 and first staged in the Yasnaya Polyana family theatricals on 30 December 1889. It is run in the `--novel` mode (drama flex): the whole comedy is read in full, while the heaviest effort goes to genesis, redaction history, and reception — the layers where the work's depth lives. It reads the play from its own text in the tolstoydigital TEI corpus (PSS Tom 27), reconstructs its genesis from the two plans, the first redaction *Исхитрилась!*, the Jubilee-Edition editorial history, and the 1884–1890 diaries and letters, and follows the work from a spiritualist séance Tolstoy attended to its uncensored 1891 publication, its stage-only ban, and the Stanislavski production that sits in the prehistory of the Moscow Art Theatre.

The dive prepares ingestion-ready material (this `index.md`, a machine-readable `dossier.yaml`, byte-faithful `extracts/`, a medium visual record, and a draft dev-blog note). It does not create vault pages; it plans them. The works record [The Fruits of Enlightenment](../../../../../../website/src/works/plays/comedy/the-fruits-of-enlightenment/) already exists as a draft stub — the dive proposes a `workRecord` fill (with two corrections) and adds a sixth `bans[].scope` value to the works schema.

---

## Key findings

- **The play grew from a real séance Tolstoy attended in contempt.** Its source was a spiritualist séance at N. A. Lvov's Moscow flat (no later than spring 1886), which Tolstoy went to "on his own initiative" and pre-judged: believing in mediums, he said, was "just the same as believing that if I suck my walking-stick, milk will flow from it." In the first two plans the spiritualist master simply *is* "Lvov," and the sceptic "Samarin" — the real names of the séance-goers.
- **It is the twin of *The Power of Darkness*.** The comedy (first titled *Исхитрилась!*, "She Contrived It!") was begun in the autumn of 1886, the apparatus says, "simultaneously or almost simultaneously" with the tragedy — in the same notebook, both sparked by A. A. Stakhovich reading Ostrovsky and Gogol aloud at Yasnaya. The tragedy and the comedy of Tolstoy's Prophet years were born together.
- **The title tracks a change of target.** The first redaction, *Исхитрилась!*, is named for the maid's trick — a plot-farce with a small cast. The heavy social-satire apparatus (the Professor's pseudo-science, the thought-reader, the dying Old Cook, the microbe-panic) was added only *after* the December 1889 staging, in 1890; the retitling to *Плоды просвещения* marks the work's growth from a servant's-trick farce into a satire of the educated class.
- **The satire's two edges are one.** The séance centrepiece skewers pseudo-science — the Professor derives "the energy of mediumism" and a "spiritual ether" whose particles are "the souls of the living, the dead, and the unborn"; beneath it, the servants' kitchen carries the human cost (the cast-off Old Cook, "die like a dog"). The idle, superstitious gentry are weighed against the peasants' material need — land — and found wanting. The "fruits of enlightenment" are bitter.
- **It was written by and for the satirised class.** At his daughter Tatyana's request, Tolstoy "patched up" the comedy for a home theatrical; his own daughters played the maid Tanya and the cook, before departing aristocratic guests and (April 1890) the court at Tsarskoye Selo. There was no peasant audience. He saw the irony and named it: the family "were doing, with clear consciences, in heightened measure, the very thing the comedy ridicules."
- **Print was free; the stage was banned.** First printed uncensored in 1891 (correcting the works-record stub), the comedy was barred from the *public* stage by Alexander III — "unsuitable for the stage, but on amateur theatres it may be permitted" — so a play mocking the gentry was, for a time, performable only by the gentry. The public stage opened at the Alexandrinsky on 26 September 1891.
- **It stands at the door of the Moscow Art Theatre.** Konstantin Stanislavski staged the comedy for his amateur Society of Art and Literature in February 1891, playing Zvezdintsev — by his own account his first independent directorial work, and the production that impressed his future MAT co-founder Nemirovich-Danchenko.

---

## Why this matters

*The Fruits of Enlightenment* is the comic face of Tolstoy's Prophet period — the laughter that runs alongside the sermons. Written in the same autumn and the same notebook as the tragedy [The Power of Darkness](../1886-the-power-of-darkness/index.html), and in parallel with [The Kreutzer Sonata](../1887-1889-the-kreutzer-sonata/index.html) and the essay that became [What Is Art?](../1897-1898-what-is-art/index.html), it turns on a single contrast Tolstoy was making everywhere in those years: a leisured, educated class amusing itself with séances and microbes and French chatter while the peasants who feed it cannot buy land enough "to let out a chicken." It is at once his only successful stage comedy, his sharpest piece of anti-pseudo-science satire, and — because it was written for his own family to perform — the work in which the satirist most plainly caught himself inside the target.

<figure>
<img src="visuals/commons-repin-portrait-1887.jpg" alt="Ilya Repin, Portrait of Leo Tolstoy, 1887">
<figcaption>Ilya Repin, <em>Portrait of Leo Tolstoy</em>, 1887 — within the years the comedy was written. State Tretyakov Gallery (public domain, via Wikimedia Commons).</figcaption>
</figure>

---

## The marquee question (hypothesis tested)

**The claim this dive set out to test:** *The Fruits of Enlightenment* is the satirical **inverse of *The Power of Darkness***. Where the tragedy was written *for* the people — in peasant speech, for the people's stage — and failed to reach them, the comedy was written *by and for Tolstoy's own class* (the family theatre, then the court) to laugh at itself, using the peasants not as audience but as the **moral measure** against which the "enlightened" gentry's spiritualist idleness is judged; the title's irony makes it Tolstoy's comic anti-pseudo-science companion to *What Is Art?*, and the stage-only ban then literally confined a play mocking the gentry to amateur (gentry) performance.

**Outcome: `confirms` on the play's targets and its external facts; `extends` on the interpretive spine — the audience-inversion, the *What Is Art?* continuity, and the stage-ban irony are corpus-grounded syntheses the scholarship pairs loosely or omits.**

**Confirmed — the targets and the audience.** The two targets are exactly what the literature names: Ernest Simmons calls the play "a merry comedy … in which high society and spiritualism were blisteringly satirized," with peasants who give "a combination of farce and genuine distress over their lack of land." And the audience-inversion is in the primary record, in Tolstoy's own words. The staged version exists because his daughter asked for it:

Date: 25 December 1889, to L. F. Annenkova.

> ...которая у меня давно была набросана. Таня дочь затеяла спектакль и попросила у меня, я согласился и вот поправил ее кое-как, и вот они играют у нас на праздниках.

*(working English)* "...[a comedy] I had long ago sketched. My daughter Tanya got up a play and asked me for it; I agreed and patched it up somehow, and now they are performing it over the holidays."

His daughters Tatyana and Maria played the maid Tanya and the cook; the gentry roles were taken by the family and its circle (N. V. Davydov, the séance-witness, directed and played the Professor). The play's reprises were a paid Tula benefit and the Chinese Theatre at Tsarskoye Selo (19 April 1890) before the Tsar and the court. There was no peasant audience — the precise opposite of the people's-stage intent of *The Power of Darkness*.

**Extended — the self-implicating irony.** The marquee's deepest point is one no mainstream source draws, because it lives in a private letter: Tolstoy knew the staging was the very thing he was mocking, and said so.

Date: 31 December 1889, to P. I. Biryukov.

> Делали с спокойной совестью в усиленной мере то самое, что осмеивается комедией. Маша играла кухарку необыкновенно хорошо

*(working English)* "With clear consciences we were doing, in heightened measure, the very thing the comedy ridicules. Masha played the cook remarkably well."

He was "ashamed the whole time, ashamed of this senseless extravagance amid poverty" (diary, 27 December 1889) — the séance-versus-landlessness contrast of the play, reproduced inside his own household. The satire turned on its author, and he recorded the turn.

**Extended — the anti-pseudo-science purpose, and the *What Is Art?* link.** That the play's object is superstition-among-the-educated is stated by Tolstoy himself, in the apology he sent the spiritualist zoologist N. P. Wagner, who had taken Professor Krugosvetlov for a portrait of himself and the late chemist Butlerov:

Date: 25 March 1890, to N. P. Wagner.

> И главное мое с годами всё усиливающееся отвращение, от которого я не отрекаюсь, ко всяким суевериям, к которым я причисляю спиритизм.

*(working English)* "And the main thing is my hatred, growing with the years, which I do not renounce, of every kind of superstition, among which I count spiritualism."

The comedy was written in the same months as the treatise on art — "I am writing both the comedy, and a story, and about art" (to N. N. Ge, 23 June 1889) — and the title's irony (*плоды просвещения*, the "fruits" of "enlightenment") makes the false-enlightenment continuity to [What Is Art?](../1897-1898-what-is-art/index.html) the dive's synthesis, grounded in the corpus where the scholarship does not draw it sharply.

**Extended — the stage-ban irony.** The mainstream reception is silent on the ban (neither Britannica nor Wikipedia mentions it); the censorship story is carried by the PSS apparatus. Its shape is the marquee made literal: a play satirising the idle gentry was permitted *only* on amateur theatres — that is, performable by the very class it mocked — and barred from the public stage (see *Publication, censorship & afterlife*).

The one place the marquee must not over-reach is *What Is Art?* itself: unlike *The Power of Darkness*, which Tolstoy designed as art *for the people*, *Fruits* is not a demonstration of accessible "good art" — it is a satire for the educated, which Tolstoy himself dismissed as "a very low and seductive occupation." The continuity is one of target (false enlightenment, false art), not of method.

---

## Genesis & composition

### The seed: a séance attended in contempt

The play came from a séance. In the mid-1880s Tolstoy had himself invited to a spiritualist sitting at the Moscow flat of N. A. Lvov, in the company of P. F. Samarin, K. Yu. Milioti, and the Tula prosecutor N. V. Davydov, who later described it.

Date: editorial commentary, PSS Tom 27.

> ...спиритического сеанса, бывшего в Москве на квартире Н. А. Львова, куда Толстой был приглашен по собственной инициативе.

*(working English)* "...a spiritualist séance held in Moscow at the flat of N. A. Lvov, to which Tolstoy had had himself invited on his own initiative."

He went already a scoffer. By Davydov's account, before the séance he compared belief in mediums to "believing that if I suck my walking-stick, milk will flow from it — which has never happened and cannot happen"; the séance failed, and confirmed him. Lvov is also in the diaries in person — on 19 April 1884, "Lvov told [me] of Blavatsky, transmigration of souls, spirit-forces … How can one not go mad amid such impressions?" Lvov died in 1887, which fixes the séance no later than that year; the apparatus dates it to the spring of 1886.

### The writing: the twin of the tragedy

Work began in the autumn of 1886, and it began beside *The Power of Darkness*:

Date: editorial commentary, PSS Tom 27.

> ...работа над комедией была начата осенью 1886 г., одновременно или почти одновременно с работой над «Властью тьмы»

*(working English)* "...work on the comedy was begun in the autumn of 1886, simultaneously or almost simultaneously with the work on *The Power of Darkness*."

The first redaction of the comedy was written into the same notebook as Act 1 of the tragedy, both prompted by the same visit — A. A. Stakhovich reading Ostrovsky and Gogol aloud at Yasnaya in mid-October 1886, while Tolstoy lay recovering from a leg injury. Then the comedy was put down. It surfaces in the diaries only intermittently across the next three years: a drafting surge at Prince S. S. Urusov's estate Spasskoye in late March 1889 ("Wrote the 4th act very badly … in the evening read the comedy to Urusov, he roared with laughter"), then revulsion ("At home I took up the comedy, but [it is] repugnant and shameful," 2 August 1889). It was the banning of *The Kreutzer Sonata* that gave it a destination: Tolstoy offered the comedy to the memorial collection *In Memory of S. A. Yuryev* in the Sonata's place.

### The family staging

The work was finished, in the end, to be performed at home.

<figure>
<img src="visuals/commons-programme-home-staging-1889.jpg" alt="Programme of the Yasnaya Polyana home staging of The Fruits of Enlightenment, December 1889">
<figcaption>Programme of the Yasnaya Polyana home staging, December 1889 — the family theatrical for which Tolstoy "patched up" the long-abandoned comedy (public domain, via Wikimedia Commons).</figcaption>
</figure>

The daughter Tatyana Lvovna, back from abroad, got up a holiday theatrical and asked her father for the play; he agreed and revised it for the occasion (see the marquee). The first performance took place at Yasnaya Polyana on 30 December 1889, directed by N. V. Davydov and cast almost wholly from the young Tolstoys and their friends:

Date: editorial commentary, PSS Tom 27 (the 30 December 1889 cast).

> М. Л. Толстую — кухарку, А. М. Новикова — буфетчика Якова, С. А. Лопухина — Звездинцева, С. Э. Мамонову — толстую барыню, Н. В. Давыдова — профессора Кругосветлова, Т. Л. Толстую — Таню

*(working English)* "...M. L. Tolstaya as the cook, A. M. Novikov as the butler Yakov, S. A. Lopukhin as Zvezdintsev, S. E. Mamonova as the fat lady, N. V. Davydov as Professor Krugosvetlov, T. L. Tolstaya as Tanya."

V. M. Lopatin, then a magistrate and later a Moscow Art Theatre actor, played the 3rd Peasant so well that Tolstoy expanded the role during rehearsals. It was the staging that triggered the play's real growth: through January–February 1890 Tolstoy added the figures and scenes that turn the farce into a satire (the Old Cook, the artel'-man, the baroness, the coachman; the thought-reader Shpyuler became Grossman; the Betsy-exposes-Tanya scene; the Act-4 charade), correcting proofs into June 1890.

---

## What the play says

The comedy is set over a single day in a rich Moscow house. Three peasants from Kursk have come to buy a parcel of the landowner Leonid Fyodorovich Zvezdintsev's land — they have the deposit and the commune's authority, and need only his signature — but he refuses the installment terms he had offered the year before, while the household spends freely on séances, a son's borzoi-breeding society, and a daughter's charade costume. The peasants' need is the play's ground note, repeated as a refrain:

> Земля наша малая, не то что скотину, — курицу, скажем, и ту выпустить некуда.

*(working English)* "Our land is so small that — not to speak of cattle — there's nowhere even to let out a chicken."

The plot engine is the maid Tanya, an orphan of the peasants' own village, in love with the buffet-lad Semyon. Knowing the master believes the village lad to be a "medium" (he "resembles Home," the famous medium), she resolves to fake the séance phenomena so that the "spirits" will order the deed signed: "He believed me, he believed me! … Now I'll do it, if only Semyon doesn't lose his nerve." The play's plain-sense verdict is given not to a master but to the educated valet Fyodor Ivanych, alone, turning over the spiritualist photograph album:

> Народные суеверия, грубые, истребляются, суеверия домовых, колдунов, ведьм... А ведь если вникнуть, ведь это такое же суеверие.

*(working English)* "Folk superstitions — coarse ones — are being stamped out: the superstitions of house-spirits, sorcerers, witches... And yet, if you look into it, this [spiritualism] is just the same kind of superstition." — closing: "Amazing — human weakness!"

**The centrepiece — the séance (Act 3).** The set-piece is the séance itself, and its comic heart is the Professor's lecture, which dresses the superstition in the language of physics — matter to molecules to atoms to "points of application of energy," then a fourth-plus kind of energy:

> ...один из таких новых, мало известных видов энергии и исследуется нами. Я говорю об энергии медиумизма.

*(working English)* "...one of these new, little-known kinds of energy is what we are investigating. I speak of the energy of mediumism."

He proceeds to a "spiritual ether" proven by the "brilliant experiments of the genius Hermann Schmidt and Joseph Schmatzhofen" (invented authorities), whose particles "are the souls of the living, the dead, and the unborn." Meanwhile Tanya, hidden under the sofa in a wallpaper-coloured dress, does the work — phosphorescent sparks from matches on Semyon's fingers, knocks on the wall, threads drawn over the guests' heads, the lampshade and pen thrown on the table, and at last the land-deed itself, while the coached Semyon "grabs and squeezes" whoever sits beside him until the master, asking the "spirit" Nikolai with two knocks for assent, signs:

> Оказывается что землю-то надо уступить крестьянам на их условиях.

*(working English)* "It turns out the land must be ceded to the peasants on their terms."

**The unfalsifiable finale (Act 4).** Exposed — the maid did everything — the believers cannot be moved. The Professor's defence is the satire's sharpest stroke:

> ...может быть, она что-нибудь и делала, но то, что она делала, — делала она, то, что было проявлением медиумической энергии, — было проявлением медиумической энергии.

*(working English)* "...maybe she did do something, but what she did, she did; and what was a manifestation of mediumic energy was a manifestation of mediumic energy."

The girl's fraud, he reasons, merely "solicited" the genuine energy; and he sweeps out with the title's irony in his mouth — "Yes — how far we still are from Europe!" — the Europhile who is himself the dupe. The deed stands. The peasants pay their money and bless the maid who got them the land: "She made us into human beings." The kind valet closes the play crediting her — "Thank Tanya. Had it not been for her, you'd be without land" — and Tanya wins her marriage and her escape from service.

Beneath the séance farce runs the play's darker register, in the servants' kitchen (Act 2): the gentry's gluttony and idleness catalogued from below, and two casualties of it — the maid Natalya, dismissed after she "slipped" and dead in hospital, and the Old Cook, once chef to the Emperor, now a discarded drunkard kept alive by a kitchen-maid's pity:

> Я у плиты тридцать лет прожарился. А вот не нужен стал: издыхай, как собака!.. Как же, пожалеют!

*(working English)* "I roasted thirty years at the stove. And now I'm not needed: die like a dog!.. Pity, indeed!"

---

## Redactions & textual history

The play passed through, by the apparatus's count, "not fewer than 7 or 8" redactions of the whole, but its decisive shift is legible in two stages. The two surviving plans (1886) already carry the entire mechanism — the séance against the peasants' land, the maid's contrivance, the medium — and they name the spiritualist master and the sceptic outright after the real séance-goers:

> вертит блюдечко о земле крестьянам. Самарин неверующий.

*(working English)* "[Lvov] spins the saucer about the peasants' land. Samarin the unbeliever." (The first plan.)

The keystone is the first full redaction, titled not for its target but for its plot:

> ИСХИТРИЛАСЬ!

*(working English)* "SHE CONTRIVED IT!"

*Исхитрилась!* is the servant's-trick farce: the household, the land, the séance, the maid's hoax — but with a far smaller cast. The Professor's pseudo-scientific lecture, the travelling thought-reader, the dying Old Cook, the baroness's microbe-panic — the apparatus that makes the play a *social* satire — were added only after the December 1889 staging, in the 1890 rewrite. The change of title, from the maid's verb *исхитрилась* ("she contrived it") to the bitter abstraction *плоды просвещения* ("the fruits of enlightenment"), is the change of the work itself: from a comedy about a clever servant to a comedy about a foolish class.

---

## Publication, censorship & afterlife

The censorship history runs in two channels that diverge as sharply as they did for *The Power of Darkness*: the print passed freely, the public stage did not.

**Print — free.** The comedy was first printed in 1891, uncensored:

> Впервые «Плоды просвещения» были напечатаны, видимо без каких-либо цензурных изъятий, в книге «В память Юрьева. Сборник, изданный друзьями покойного». М. 1891

*(working English)* "*The Fruits of Enlightenment* was first printed — apparently without any censorship excisions — in the book *In Memory of [S. A.] Yuryev. A collection issued by the late man's friends*, Moscow 1891." — reprinted the same year in Part 13 of the collected works.

This corrects the works-record stub, which had marked the play as not published in Tolstoy's lifetime and not published in Russia: it was both, in 1891, uncensored. (The only pre-print changes were two decency softenings introduced by S. A. Tolstaya in proof, which the PSS restores — author-side, not state censorship.)

**Stage — banned.** The public stage was a different matter. The dramatic censor had cleared the amateur Tula performance with a few words cut (including "monk," of the spirit Nikolai), but the Main Administration for Press Affairs overrode him: on the report of 26 April 1890, Alexander III ruled —

> эту пьесу неудобною для сцены, на любительских же театрах она может быть разрешена

*(working English)* "[His Majesty is pleased to find] this play unsuitable for the [public] stage, but on amateur theatres it may be permitted."

The Feoktistov circular of 28 April 1890 enforced it; it was reaffirmed in March 1891 after an unauthorised Kharkov staging. So a comedy mocking the idle gentry was, by imperial decree, performable *only* by amateurs — that is, by the leisured class it satirised. The public stage opened first at the Imperial Alexandrinsky (26 September 1891); provincial staging was allowed case-by-case from late 1893, and a general permission followed in 1894. The dive records this with a new `bans[].scope` value, `stage-ban` (works-schema v9), added for exactly this shape — print free, public stage closed — shared with *The Power of Darkness*.

**Translation.** The authorised English text is the Maudes', long catalogued under the title *The Fruits of Culture*; modern usage (and this dive) prefers *The Fruits of Enlightenment*, closer to *просвещение* and to the title's irony. The two are one play.

---

## Characters & prototypes

The cast is large and largely typological — the comedy of a *class*, not of individuals — so the dive routes as standalone `character` nodes only the figures that earn one (a principal, or a documented prototype) and folds the rest into the work's overview prose. Unusually, the satirised principals carry real prototypes drawn from the séance and its world:

- **Tanya** — the maid, the play's practical intelligence and the title-figure of the first redaction; an invented type, played at the première by Tolstoy's daughter Tatyana.
- **Leonid Fyodorovich Zvezdintsev** — the spiritualist master. Prototype: **N. A. Lvov**, the séance host, whose actual surname the character bears in the first two plans (editorial, documented).
- **Professor Krugosvetlov** — the "scientific" believer. Prototype: the chemist-spiritualist **A. M. Butlerov** (the draft surname Кутлеров echoes his) — but a *name-source*, not a portrait: Tolstoy explicitly denied targeting Butlerov or Wagner, calling the professor "a personification of comic contradiction." (editorial, probable; not over-claimed.)
- **Grossman** — the travelling hypnotist. Prototype: the celebrity thought-reader **O. I. Feldman**, whom Tolstoy met in April 1889 ("charlatanry," diary), down to the soundalike name; the Maly actor who later played him made up to look like Feldman was sued by him (editorial, documented).
- **Sakhatov** — the urbane sceptic. Prototype: **P. F. Samarin**, a real séance-goer whose surname the character bears in the plans (editorial, documented).
- **Semyon** — the peasant-lad taken for a medium, Tanya's betrothed; an invented type, present from the first plan.

The valet Fyodor Ivanych (the play's plain-sense moral voice), the Old Cook and the three Peasants (the social-cost and land-question figures), and the household — Anna Pavlovna, Betsy, Vasily Leonidych — are kept in the work's overview prose rather than minted as nodes; those calls, and the disambiguation of the character page-names, are logged in the dossier's `needsReview`.

---

## Themes

- **Spiritualism as the superstition of the educated.** The play's central target: the séance vogue (mediums, the "spiritual ether," scientist-believers) is, in Tolstoy's words to A. I. Apollov, the type-specimen of superstition surviving "not only among the unlearned but among the educated classes too (example — spiritualism)."
- **Pseudo-science.** The Professor's lecture and the doctors' microbe-panic are science misapplied — the form of rigour without its substance, "the comic contradiction between strict scientific method and the most fantastical assertions."
- **The land question.** The peasants' need for land is the material reality against which the gentry's amusements are measured; their refrain ("nowhere to let out a chicken") and their final blessing of Tanya ("she made us into human beings") give the play its moral floor.
- **The wisdom of the servants.** The practical intelligence and decency of the play belong below stairs — to Tanya and the valet Fyodor Ivanych — and the folly above; the social hierarchy is inverted by competence.
- **Use and discard.** The Old Cook and the dead maid Natalya are the human cost of the leisured household — the darker note beneath the farce.
- **False "enlightenment."** The title's irony: the "fruits" of education and Europeanisation are, in this house, superstition, idleness, and a peasantry kept landless — the false-enlightenment strand that runs to [What Is Art?](../1897-1898-what-is-art/index.html).

---

## Reception & afterlife

**A reception by the satirised class.** The play's first audiences were precisely the people it mocked. The amateur première (Yasnaya, 30 December 1889) was a family theatrical; the 1890 reprises were a paid Tula benefit and a court performance at the Chinese Theatre, Tsarskoye Selo (19 April 1890), before the Tsar, Tsaritsa, grand dukes, and capital nobility. There was no peasant audience — the play satirising the gentry was performed for and by the gentry, exactly as the stage ban then required.

<figure>
<img src="visuals/commons-stanislavski-fruits-1891.jpg" alt="Konstantin Stanislavski as Zvezdintsev in The Fruits of Enlightenment, 1891">
<figcaption>Konstantin Stanislavski as the spiritualist landowner Zvezdintsev, in his Society of Art and Literature production of <em>The Fruits of Enlightenment</em>, 1891 — by his own account his first independent directorial work (public domain, via Wikimedia Commons).</figcaption>
</figure>

**The Moscow Art Theatre prehistory.** The single most-cited fact in the English reception is the Stanislavski connection: in February 1891 Konstantin Stanislavski staged the comedy for his amateur Society of Art and Literature, playing Zvezdintsev himself, in what he later called his first fully independent directorial work (*My Life in Art*). Britannica frames the production as "a major Moscow theatrical event" that impressed Vladimir Nemirovich-Danchenko — the man with whom Stanislavski would found the Moscow Art Theatre in 1898. The comedy that began at a séance ends up at the door of modern Russian theatre.

**The professional stage.** The first public, Imperial performance was at the Alexandrinsky in St Petersburg on 26 September 1891 (the only hard professional-stage date in the PSS apparatus); the play transferred to the Maly Theatre, Moscow, in December 1891 (this date is secondary-sourced, not in the apparatus — see `needsReview`). Tolstoy attended the Maly in January 1892 and was, by report, dissatisfied with the actors' rendering of the three peasants — a detail that itself reinforces where he located the play's weight.

---

## Scholarly context

This section maps where the corpus evidence meets, confirms, or extends the received scholarly view; it attributes rather than asserts.

**The play's standing and targets are settled — and warmly.** Unusually for late Tolstoy, the English reception is uniformly positive: Simmons (*Introduction to Tolstoy's Writings*, 1968, ch. 11) reads it as Tolstoy's one successful stage comedy and the natural pendant to *The Power of Darkness*, "blisteringly" satirising "high society and spiritualism" while giving the peasants "genuine distress over their lack of land." Reference works file it as a satire of "unenlightened attitudes towards the peasants amongst the Russian landed aristocracy" (Wikipedia) and place it in the Russian social-comedy line of Gogol and Ostrovsky — a lineage the primary record supports, since it was Stakhovich's reading of Gogol and Ostrovsky that sparked the play. On these the dive `confirms`.

**The pseudo-science target is corroborated from outside the apparatus.** The history-of-science literature independently documents the chemist A. M. Butlerov and the zoologist N. P. Wagner as the eminent St-Petersburg scientist-spiritualists of exactly this milieu, divided from the sceptic Mendeleev (whose 1875–76 commission tried to debunk mediumism) — corroborating the PSS-stated prototype. Two cautions, both observed here: Tolstoy *denied* a personal portrait of Butlerov or Wagner, so Krugosvetlov is a composite of a type, not a caricature of a man; and Mendeleev's commission and the medium D. D. Home, though real and known to Tolstoy's readers, are **not** in the PSS Tom 27 apparatus — the play itself names "Home" (Юм), but the wider science-history frame is attributed strictly to general scholarship, never to the PSS.

**The interpretive spine is the dive's, grounded in the corpus.** Three of the marquee's claims `extend` past the scholarship. The mainstream *pairs* the comedy and the tragedy but does not draw the audience-inversion (written-for-the-people vs. written-by-the-class) sharply; that turn rests on the project's own [Power of Darkness](../1886-the-power-of-darkness/index.html) dive and on Tolstoy's own letters. The continuity to [What Is Art?](../1897-1898-what-is-art/index.html) — false enlightenment, false art — the literature does not draw at all. And the stage-ban irony the mainstream simply omits: neither Britannica nor Wikipedia carries Alexander III's ruling. (On the contested movement-labels Tolstoy's late work attracts, see [Tolstoyanism](../tolstoyanism/index.html).)

---

## Where the material clusters

**Works (PSS Tom 27).**

| TEI id | Material | Pages |
|---|---|---|
| `v27_095_250_Plody_prosveschenija` | The comedy (four acts) | 95–250 |
| `v27_433_435_..._Pervyj_plan` | First plan (master named "Lvov," sceptic "Samarin") | 433–435 |
| `v27_436_437_Vtoroj_plan_...` | Second plan | 436–437 |
| `v27_438_475_..._Ishitrilas` | The first redaction *Исхитрилась!* (the keystone variant) | 438–475 |
| `v27_476_480_Varianty_...` | Variants | 476–480 |
| `v27_647_670` (comments) | Editorial commentary «История писания» (genesis, prototypes, censorship, staging) | 647–670 |

**Letters (PSS Toms 64–65).**

| Tom | Date | Addressee | Material |
|---|---|---|---|
| 64 | 23 Jun 1889 | N. N. Ge | "I am writing both the comedy, and a story, and about art." |
| 64 | 25 Dec 1889 | L. F. Annenkova | The genesis of the staged version: Tatyana got up the play and asked for it. |
| 64 | 31 Dec 1889 | P. I. Biryukov | "...doing, in heightened measure, the very thing the comedy ridicules." |
| 65 | 22 Feb 1890 | A. I. Apollov | Spiritualism as superstition surviving among the educated. |
| 65 | 25 Mar 1890 | N. P. Wagner | The apology: no portrait of Butlerov/Wagner; his hatred of superstition, spiritualism included. |

**Diaries (PSS Toms 49–51).** The séance milieu (Lvov, 19 Apr 1884); the *Исхитрилась!* drafting at Spasskoye (Mar–Apr 1889); the shame at the family staging amid poverty (27 Dec 1889); the recurrent self-disparagement ("the comedy is poor — trash," 13 Apr 1890).

---

## The author's later verdict

Tolstoy never thought well of the comedy. Across its composition his diaries and letters call it "repugnant and shameful," "a very low and seductive occupation," and — even as it triumphed on the Tula stage — "poor, trash." His objection was not to the play's aim but to the activity of making and staging it: theatre, for the Tolstoy of these years, was "an amusement of rich and idle people," and a comedy got up by his own family for the holidays was that amusement in person. He let it be printed and staged, and it became his most successful stage work; but the gap between what he was satirising and what he was doing in satirising it was one he named in his own diary and never resolved. The play that began at a séance he despised ended as an entertainment he was ashamed of — and was, all the same, very good.

---

## Material not covered

- Full manuscript collation of all 7–8 redactions (the dive samples the two plans and the *Исхитрилась!* first redaction as the keystone, per novel mode).
- The play's later Soviet and world stage history beyond the 1911 Maly revival.
- A scene-level study of the Act-2 thought-reading "experiment" against the real Feldman/Cumberland thought-reading acts of the 1880s.
- *The First Distiller* (Первый винокур, 1886) and the folk-tale cycle as the sibling "art for the people" set — flagged for a cluster cross-link or a later theme-dive, not dived here.

---

## Visual & manuscript record

A medium sweep (Wikimedia Commons; Internet Archive) returned eight public-domain images, recorded with provenance and rights in the dossier `visuals` block and cached locally (the cache is git-ignored; `docs/fetch_visuals.py` repopulates it from the dossier URLs).

- **The staging:** the actual programme of the December 1889 Yasnaya Polyana home production, and Stanislavski in costume as Zvezdintsev in his 1891 Society of Art and Literature staging — the two keystone reception images.
- **Tolstoy, 1886–92:** Repin's 1887 oil portrait and a Scherer & Nabholz studio photograph (1887), both within the composition window; a group photograph of 1892.
- **The play in the repertory:** a Maly Theatre 1911 revival scene, an 1898 playbill, the 1892 Russian edition cover, and the title page of the 1891 New York English edition (via Internet Archive).

**Not openly available / follow-up:** no public-domain photograph or set design from the 1891 Alexandrinsky/Maly professional premières was located (likely held, rights-reserved, by the Bakhrushin and St-Petersburg theatre museums; Goskatalog not yet systematically queried); nor a photograph of the December 1889 family production (only the programme survives openly), nor the true 1891 Posrednik first-edition title page. These are recorded in the dossier as a visuals work-order.

---

## Method

A `--novel` work-subject dive (drama flex): the full comedy read act by act, with the heaviest effort on genesis, redaction history, and reception. Pre-reform orthography resolved with `extract_tei.py --choice=reg --notes=auto`. Composition-years witness sweep across the 1884–1890 diaries (Toms 49–51) and the 1889–1890 letters (Toms 64–65); genesis, prototypes, and censorship reconstructed from the PSS Tom 27 editorial apparatus, grounded against Tolstoy's own diary and letters before any mainstream scholarship. The marquee was stated up front and tested as a hypothesis. Every primary quotation is byte-verified against its extract (`verify_quotes.py`, 32/32 PASS); secondary claims are attributed. A medium visuals sweep. One schema change was made with the reader's approval: a sixth `bans[].scope` value, `stage-ban`, added to the works schema (v9) for the print-free / stage-banned shape this play shares with *The Power of Darkness*.

**Two source-cache cautions, logged for reuse.** (1) The diary entry on the séance milieu is filed under the TEI year 1883 but belongs to 19 April 1884 (the bibl header and PSS commentary agree) — a known filename-year gotcha. (2) The local Jubilee fb2 directory `jubilee-edition/vol27/` is mislabeled — it holds PSS Tom 61 (Letters), and the real Tom 27 is in `vol87/`; the offset is systematic in that range. Both are in the dossier's `needsReview`.

**Links.** Sibling dives: [The Power of Darkness](../1886-the-power-of-darkness/index.html) · [The Kreutzer Sonata](../1887-1889-the-kreutzer-sonata/index.html) · [What Is Art?](../1897-1898-what-is-art/index.html) · [copyright renunciation](../copyright-renunciation/index.html) · [Tolstoyanism](../tolstoyanism/index.html).

---

## References

**Primary.** Л. Н. Толстой, *Плоды просвещения*, ПСС Т. 27 (text pp. 95–250; first plan 433–435, second plan 436–437; first redaction *Исхитрилась!* 438–475; variants 476–480; editorial commentary «История писания и печатания» 647–670). Diaries, ПСС Тт. 49–51 (1884; 1889–90). Letters, ПСС Тт. 64–65 (1889–90) — to N. N. Ge, L. F. Annenkova, P. I. Biryukov, N. P. Wagner, A. I. Apollov, G. A. Rusanov.

**Background.** Ernest J. Simmons, *Introduction to Tolstoy's Writings* (1968), ch. 11 ("Dramatic Writings") — the standard English account. Konstantin Stanislavski, *My Life in Art* (1924) — the 1891 Society of Art and Literature production. Encyclopædia Britannica, "The Fruits of Enlightenment" (accessed June 2026). Wikipedia, "The Fruits of Enlightenment" and "Konstantin Stanislavski" (accessed June 2026). Encyclopedia.com, "A. M. Butlerov" and "D. I. Mendeleev"; *Annals of Science* (2025) on Russian scientific spiritualism — background context for the prototypes, not in the PSS. F. Raskolnikov, "Цензурные мытарства Л. Н. Толстого-драматурга," *Красная новь* кн. 11 (1928) — the stage-censorship dossier. Aylmer & Louise Maude, the standard English translation (as *The Fruits of Culture*); A. N. Wilson, *Tolstoy* (1988); Rosamund Bartlett, *Tolstoy: A Russian Life* (2010).

---

*Draft dev-blog note: [`2026-06-11-the-fruits-of-enlightenment.md`](../../../../../../website/src/posts/notes/2026-06-11-the-fruits-of-enlightenment.md) (draft).*
