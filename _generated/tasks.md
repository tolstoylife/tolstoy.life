# Uppgifter — Fas 2–3 Färdplan

Senast uppdaterad: 2026-04-10

Den här filen följer upp kommande arbete genom slutet av fas 2 (testomgång) och in i fas 3 (TEI-massimport). Den lagras i `_generated/` i projektroten.

Statusmarkeringar: `[ ]` öppen · `[x]` klar · `[~]` pågår · `[!]` blockerad / kräver beslut

---

## Innan Fas 2 — Projektinfrastruktur

Grundläggande filer och struktur som ska finnas på plats innan det faktiska innehållsarbetet tar fart.

- [x] **`_generated/`-mapp skapad** — samlingsplats för allt Claude producerar: dokument, analyser, anteckningar. Rot: `Tolstoy/_generated/`.
- [x] **`_generated/tasks.md`** — denna fil, på svenska.
- [x] **`manifest.md`** — beskriver projektets syfte och mening. Ligger i projektroten (`Tolstoy/manifest.md`) som en publik del av projektet.

---

## Fas 2 — Testomgång (slutför en välbelagd entitetsuppsättning)

Målet är att validera LLM Wiki-modellen i liten skala innan vi expanderar. Mål: ~10 nyckelentiteter fullständigt importerade, korsrefererade och granskade i Obsidian.

### Personer — kvarvarande sidor för den innersta kretsen

- [ ] **Ilja Lvovitj Tolstoj** (1866–1933) — son; saknas i TEI personList.xml. Källa: Birukoff-biografin.
- [ ] **Michail Lvovitj Tolstoj** (1879–1944) — son; saknas också i TEI. Källa: Birukoff-biografin.
- [ ] **Aylmer Maude** (1858–1938) — primär engelsk översättare och biograf. Inte i TEI. Källa: Maude-biografins metadata + Standard Ebooks.
- [ ] **Nikolaj Nikolajevitj Gusev** (1882–1967) — Tolstojs sekreterare 1907–1909; kanonisk avskrivare. Källa: TEI personList.xml (om befintlig) + Jubileumsutgåvans kreditering.

### Dataluckor från befintliga sidor (loggade öppna frågor)

- [ ] **Maria Tolstaja** — lägg till exakta födelsedag/dödsdag (TEI ger endast livstidsperiod 1871–1906). Källa: Birukoff.
- [ ] **Sergej, Lev, Andrej** — bekräfta Jasnaja Poljana som födelseort från namngiven källa (TEI saknar detta fält).
- [ ] **Aleksandra Tolstaja** — bekräfta dödsort (Valley Cottage, NY) från primärkälla.
- [ ] **Tänk efter!** — slå upp Wikidata QID och lägg till i frontmatter.
- [ ] **Tänk efter!** — verifiera Jubileumsutgåvans vol. 36 sidintervall från den faktiska volymen.
- [ ] **Tänk efter!** — identifiera medöversättaren "I. F. M." (möjligen Isabel F. Mayo). Källa: PG-utgåvans noter, samtida recensioner.
- [ ] **Tänk efter!** — fastställ datum för första lagliga rysk publikation.
- [ ] **Jasnaja Poljana** — kontrollera dateringen "1847 för arvet" mot Birukoff (TEI anger 1847).
- [ ] **Tatjana Tolstaja** — beslut: använd flicknamn eller gift namn (Suhótina) som primär sidtitel? Anteckna beslutet i loggen.

### Platser — nästa omgång

- [ ] **Moskva, Chamovniki-huset** — Tolstojs vinterbostad 1882–1901. Källa: TEI locationList.xml + Birukoff.
- [ ] **Optina Pustyn** — kloster; Tolstojs näst sista anhalt före Astapovo. Källa: TEI locationList.xml.
- [ ] **Sjamordino** — kloster där systern Maria var nunna; hans sista stopp före Astapovo. Källa: TEI locationList.xml.

### Verk — bootstrap-uppsättning

- [ ] **Krig och fred** — skapa översiktsartikel (frontmatter + prosastub). Källa: TEI bibllist_works.xml för datum; schema v5.
- [ ] **Uppståndelse** — skapa översiktsartikel. Källa: TEI bibllist_works.xml.
- [ ] **Ivan Iljitjs död** — skapa översiktsartikel. Källa: TEI bibllist_works.xml.
- [ ] **Hadji Murat** — skapa översiktsartikel. Källa: TEI bibllist_works.xml.
- [ ] **Bikt** — artikeln finns redan (`src/works/non-fiction/personal-papers/confession/`); granska frontmatter mot schema v5 och höj recordStatus från `draft` till `reviewed` om komplett.
- [ ] **Anna Karenina** — artikeln finns; samma granskning och statuslyft.

### Lintpass efter testomgången

- [ ] Kör ett lintpass över valvet (personer + verk). Kontrollera: föräldralösa sidor, saknade wikilänkar, motsägelser mellan sidor, inaktuella påståenden. Anteckna fynd i loggen.
- [ ] Uppdatera `src/sources/index.md` med alla nya sidor och statusändringar.

---

## Fas 3 — TEI-massimport

När fas 2 är validerad och stabil, skala upp till hela TEI-referensdatan.

### Personer (personList.xml — 3 113 poster)

Strategin är nivåindelad efter närheten till Tolstoj:

- [ ] **Nivå 1** — Innersta kretsen (~30 personer): familjemedlemmar, närmaste lärjungar, redaktörer, översättare. Många finns redan; granska och berika från TEI-posterna.
- [ ] **Nivå 2** — Utvidgad krets (~100–150 personer): brevskrivare, förläggare, konstnärer, politiska figurer som förekommer ofta i texterna.
- [ ] **Nivå 3** — Fullständigt dataset (återstående ~3 000): batch-skapa stubbar för alla återstående personList.xml-poster med minimal frontmatter (namn, datum, Wikidata QID, TEI-id). Dessa är platshållare som berikas allteftersom textimport fortskrider.

**Förutsättning:** Skriv ett litet skript (`tools/`) som tolkar personList.xml och genererar en sorterad lista med alla personer och deras omnämnandeantal i texterna, så att nivåprioriteringen bygger på data snarare än intuition.

### Platser (locationList.xml — 770 poster)

- [ ] **Nyckellokaliteter** (~20–30): platser som förekommer i flera verk eller har biografisk betydelse (Jasnaja Poljana, Astapovo, Chamovniki redan klara/planerade; lägg till Tula, Nikolskoje, Samaraegendomen, kaukasiska stationeringar m.fl.).
- [ ] **Fullständigt dataset**: batch-skapa stubbar för alla 770 platser med minimal frontmatter.

### Verk (bibllist_works.xml — 767 verk)

- [ ] **Tolka bibllist_works.xml** och ta fram en masterkontrolllista över alla Jubileumsutgåvans verk.
- [ ] **Granska befintliga verkfiler** mot kontrolllistan — identifiera luckor, verifiera datum och genreklassificeringar.
- [ ] **Skapa stubbar** för verk som ännu saknas i valvet, prioriterade efter läsarintresse (stora romaner → noveller → viktig facklitteratur → allt övrigt).

---

## Stagingmaterial (att importera eller arkivera)

Dessa filer finns i `src/_staging/` och har ännu inte importerats till wikin:

- [ ] **`notes/A CHRONOLOGY OF LEO TOLSTOY.md`** — kronologisk tidslinje. Bedöm noggrannhet och källhänvisning, använd sedan för att berika wikiartiklar och LT:s huvudsida.
- [ ] **`tolstoy-swan-pen/tolstoy-swan-pen.md`** — detaljerad referens om Tolstojs Swan-reservoarpenna (Mabie, Todd & Co.). Rikt primärkällmaterial. Skapa en wikibegreppsida `Tolstojs skrivredskap` eller liknande, och länka till Tjertkov, Jasnaja Poljana, Aleksandra Tolstaja.
- [ ] **`notes/Tolstoy (1828-1910)--10 books.md`** — granska innehåll; arkivera eller ta bort.
- [ ] **`notes/The First Step.md`** — staginganteckning för vegetarianismsessäet. Initiera import när redo.
- [ ] **`notes/There Are No Guilty People.md`** — staginganteckning. Arkivera eller importera.
- [ ] **`notes/Patrionism and Government.md`** — staginganteckning. Arkivera eller importera.
- [ ] **`Thread by @karpathy.md`** — inspiration/referens för LLM Wiki-modellen; kan arkiveras eller tas bort (metodiken är redan kodad i CLAUDE.md).

---

## Infrastruktur / verktyg

- [ ] **Wikilänksgranskning** — kontrollera att alla `[[wikilänkar]]` i befintliga sidor löser upp till faktiska filer. Identifiera och åtgärda trasiga länkar.
- [ ] **Schema v5-kontroll** — verifiera att all befintlig verkfrontmatter överensstämmer med schema v5 (tolstoy-works-schema.md). Flagga fält som är fel typ, saknar obligatoriska värden eller använder fritext i styrda vokabulärfält.
- [ ] **Sidovagnsfiler** — befintliga verkfiler (`Bethink Yourselves!.md`, `Anna Karenina.md`, `Confession.md` m.fl.) kanske saknar tillhörande `.data.yaml`-sidovagnsfiler. Skapa eller verifiera.
- [ ] **`tools/`-skript: tolka personList.xml** — generera sorterad omnämnandетabell för nivåprioritering (se fas 3 ovan).
