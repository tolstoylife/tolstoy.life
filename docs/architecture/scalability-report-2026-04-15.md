# Skalbarhet: Obsidian, RAG och migrationsvägen

Rapport: 2026-04-15

Denna rapport undersöker fem frågor: (1) klarar Obsidian av TEI-datasetets volym (4 600+ filer)? (2) Vilka RAG-system kan komplettera eller ersätta det? (3) Hur lätt är det att flytta den befintliga LLM-wikidatan till ett RAG-system? (4) Vad kostar de olika alternativen? (5) Hur tungt blir det att hålla RAG-indexet synkat vid stora wiki-ingesteringar?

---

## 1. Obsidian vid 4 600+ filer: prestanda och gränser

### Vad fungerar bra

Obsidian desktop hanterar stora vaults bättre än man kanske förväntar sig. Laddtiden för en vault med 17 000+ filer ligger under 500 ms i Obsidian 1.10+, och användare rapporterar att 50 000+ filer med 40+ aktiva plugins fungerar utan större problem på desktop.

Backlink-indexering och sökning fungerar väl efter initial indexering. Det finns inget dokumenterat prestandaklippan för link resolution vid 10 000+ wikilinks.

### Kända flaskhalsar

**Link autocomplete** är den allvarligaste begränsningen. Vid stora vaults uppstår 4-sekunders fördröjning per tangenttryckning vid `[[not-namn`-inmatning. Block-referenser (`[[^^`) kan bli oanvändbara. Detta påverkar det dagliga redigeringsarbetet direkt.

**Graph view** blir trög vid 5 000+ noder. Ingen hård gräns finns publicerad, men global graph view kräver filtrering (per mapp eller tagg) för att vara användbar vid den volymen.

**Icke-markdown-filer** drar ner prestanda oproportionerligt. En vault med 2 700 markdown-filer men 570 000 totala filer (bilder, binärer) ger hög RAM/CPU-användning. Det totala antalet filer, inte bara markdown-filer, är avgörande. Det här är relevant för oss om vi har scannade sidor och OCR-output i närheten av vaulten.

**Mobil** försämras kraftigt. 50 000+ filer ger ca 3 minuters starttid och 27 minuters omindexering. En lazy-loader-plugin (som cachar metadata i IndexedDB) kan ta ner det till 2-3 sekunder för 30 000+ filer.

### Bedömning för Tolstoy-projektet

Vid 4 600 markdown-filer (wiki + works) bör desktop-Obsidian fungera väl. Starttid, sökning och backlänkar är inom bekväma gränser. **Graph view och link autocomplete kommer att vara märkbart långsammare**, men hanterbart med filtrering. Om vi lägger till text/-filer för varje verk (kapitelvis) kan totalen nå 10 000+, vilket fortfarande är inom desktop-gränsen men pushsar autocomplete-problemet.

Rekommendation: **Obsidian räcker som redigeringsverktyg**, men vi behöver ett kompletterande query-lager för programmatisk sökning, korsreferenser och analys vid den volymen.

---

## 2. RAG-system som komplement

### Alternativ jämförelse

| System | Lokal/offline | Ollama-stöd | Markdown-ingestion | Inkrementella uppdateringar | Status (april 2026) |
|--------|:------------:|:-----------:|:------------------:|:--------------------------:|:-------------------:|
| **LightRAG** | Ja (med OpenSearch) | Ja | Via LLM-extraktion | 50 % snabbare än GraphRAG | Aktiv (v1.4.14) |
| **GraphRAG** (Microsoft) | Delvis | Via wrapper | Textblock | Full omindexering, dyr | Aktiv |
| **nano-graphrag** | Ja | Ja | Via extraktion | Flexibel | Underhållen |
| **Cognee** | Ja | Via LlamaIndex | 30+ format | Strömmande ingestion | Aktiv |
| **txtai** | Ja | Via integration | Text-embeddings | Inkrementell | Underhållen |

### LightRAG i detalj

LightRAG är det mest relevanta alternativet för oss. Accepterat vid EMNLP 2025, aktivt underhållet med release 1.4.14 (12 april 2026). Stödjer OpenSearch, MongoDB, PostgreSQL som backend, och har RAGAS-evaluering och Langfuse-tracing.

Jämfört med Microsofts GraphRAG: 50 % snabbare inkrementella uppdateringar, ca 30 % lägre query-latens (80 ms vs 120 ms), dramatiskt lägre kostnad ($0.15 per dokument vs $4). Nackdelen är lägre "relational fidelity" — för komplex resonering över djupa relationer är GraphRAG starkare.

### LightRAGs lagringsarkitektur — behövs OpenSearch?

**Kort svar: nej.** OpenSearch är ett valfritt backend, inte ett krav. LightRAG har fyra oberoende lagringslager, och vart och ett kan konfigureras separat:

| Lagringslager | Funktion | Standardbackend (lokalt) | Alternativ |
|---------------|----------|:------------------------:|------------|
| **KV (key-value)** | Lagrade dokument, metadata | JsonKVStorage (JSON-filer) | PostgreSQL, Redis, MongoDB, OpenSearch |
| **Graf** | Entiteter och relationer | NetworkXStorage (in-memory + fil) | Neo4j, PostgreSQL+AGE, Memgraph, OpenSearch |
| **Vektor** | Embeddings för semantisk sökning | NanoVectorDB (lokal fil) | FAISS, PostgreSQL, MongoDB, Milvus, Qdrant, OpenSearch |
| **Dokumentstatus** | Vilka filer som är indexerade | JsonDocStatusStorage (JSON-fil) | PostgreSQL, MongoDB, OpenSearch |

**Standardinstallationen** sparar allt i en lokal `WORKING_DIR/` — JSON-filer för KV och status, NetworkX-graf serialiserad till disk, NanoVectorDB för vektorer. Inga externa beroenden, kör direkt på en Mac.

**OpenSearch** (tillagt mars 2026) är ett *unified backend* som täcker alla fyra lagren i ett: KV-lagring, graflagring via dokumentrelationer, k-NN vektorsökning och full-text-sökning. Poängen med OpenSearch är horisontell skalning — distribuerade kluster, sub-100ms latens vid terabyte-skala, och flera samtidiga användare.

**När behövs OpenSearch?** Typiskt vid 10M+ dokument eller krav på låg latens under hög belastning. För vårt projekt (5 000 markdown-filer, en enda användare) är standardbackendsen mer än tillräckliga. Vi behöver aldrig betala $360–720/månad för ett AWS OpenSearch-kluster.

**Alternativa uppskalningsvägar** om vi vill gå bortom standardbackends utan OpenSearch:

- **Neo4j** för grafen — kraftfullare Cypher-queries, men kräver en separat server
- **FAISS** för vektorer — snabbare än NanoVectorDB vid >100k vektorer
- **PostgreSQL** — kan täcka alla fyra lagren med pgvector + AGE-tillägget, i en enda databas

För Tolstoy-projektet rekommenderas att **börja med standardbackends** och bara byta ut enskilda lager om och när prestanda blir ett problem.

### nano-graphrag

Lätt alternativ (~1 100 rader kod). Stödjer Ollama, FAISS som vektorlager, asynkron bearbetning. Bra mellanting mellan enkelhet och kapabilitet. Mindre community men lättare att förstå och modifiera.

### Rekommendation

**LightRAG** är förstahandsvalet: bäst prestanda/kostnad, stark inkrementell uppdatering (kritiskt för vårt arbetsflöde), och fullt Ollama-stöd för lokal drift. **nano-graphrag** är reserv om LightRAG visar sig för komplext att sätta upp.

---

## 3. Migrationsväg: från LLM-wiki till RAG

### Vad vi har idag

Vår wiki består av markdown-filer med:

- YAML-frontmatter (strukturerad metadata: datum, platser, identifierare, relationer)
- `[[wikilinks]]` genom all prosa (implicit kunskapsgraf)
- Filer organiserade i `wiki/` (personer, platser, händelser, koncept) och `works/` (bibliografi med `text/`-undermappar)
- Unika slug-ID:n i frontmatter

### Hur svårt är det att migrera?

**Kort svar: ganska enkelt.** Våra wikilinks ÄR redan grafkanter. Fronmatter-YAML:en ÄR redan strukturerad metadata. Migrationen handlar om att extrahera det som redan finns snarare än att skapa nytt.

### Steg 1: Extrahera den implicita grafen

Parsa `[[wikilinks]]` med regex, bygg en adjacency-lista per fil. Varje wikilink blir en kant i grafen. Frontmatter-fält som `relatedArticles`, `authoringLocations` etc. ger typade relationer. Det här är en enkel Python-scriptövning — ett par hundra rader.

### Steg 2: Mata in i RAG-systemet

Varken LightRAG eller GraphRAG förstår wikilinks nativt. Men det spelar mindre roll:

- **LightRAG** accepterar rå markdown och extraherar entiteter/relationer automatiskt via LLM. Man behöver inte konvertera till tripplar först — LLM:en gör det. Wikilinkarna hjälper LLM:en att identifiera entiteter korrekt.
- Alternativt kan man förbearbeta filerna till en enklare representation (en fil per entitet med relationer som metadata) innan ingestion.

### Steg 3: Dual-system med filövervakning

Den rekommenderade arkitekturen är att behålla Obsidian som redigeringsverktyg och lägga till RAG som query-lager:

```
Obsidian (redigering) → git commit → file watcher → RAG re-index (inkrementell)
                                                          ↓
                                                    Query-API för Claude
```

Konkreta verktyg för filövervakning:

- **Vault MCP Server** (`robbiemu/vault-mcp`) — live-sync med inkrementell omindexering
- **Python watchdog** — enkel filovervakare som triggar LightRAG-ingestion vid filändring
- **MCP Markdown RAG** — omindexerar automatiskt bara ändrade filer

### Steg 4: Embeddings för historiskt innehåll

Standard-embeddings (OpenAI, Sentence-Transformers) fungerar rimligt väl men kan förbättras:

- **HistWords** (Stanford) specialiserar sig på diakrona embeddings — hur ord ändrar betydelse över tid
- Flerspråkiga modeller anpassade via contrastive learning förbättrar retrieval för historiska texter
- För ett projekt av vår storlek räcker troligen en standardmodell (t.ex. `all-MiniLM-L6-v2` via Sentence-Transformers) med Ollama

---

## 4. Kostnader

### Jämförelsetabell

| System | Initial indexering (5 000 dok) | Inkrementell uppdatering (50 filer) | Per query | Infrastruktur/månad | 100 % lokalt med Ollama? |
|--------|:------------------------------:|:-----------------------------------:|:---------:|:-------------------:|:------------------------:|
| **nano-graphrag** | $0 (lokal beräkning) | $0 | $0 | $0 (kör på Mac) | Ja |
| **txtai** | $0 (lokal beräkning) | $0 | $0 | $0 (SQLite) | Ja |
| **LightRAG** | $0 lokalt / ~$15 med API | $0 lokalt / ~$0.15 med API | $0 lokalt | $0 (lokala backends räcker) | Ja |
| **GraphRAG (Microsoft)** | $350–500 (GPT-4o-mini) | Dyr (full omindexering) | ~$0.01–0.10 | $0–50/mån | Nej (kräver API) |
| **LazyGraphRAG** | $0.35–0.50 (1000x billigare) | Billigare än GraphRAG | ~$0.01 | $0–50/mån | Nej (kräver API) |
| **Cognee** | ~€210 (cloud) / €1 970/mån (on-prem) | Ingår | Ingår | €1 970/mån | Nej |
| **Gemini Vertex AI RAG** | ~$30–60 (Gemini 2.5 Pro) | ~$0.50–5 | ~$0.01–0.05 | $50–200/mån (estimat) | Nej |

### Detaljkommentarer

**nano-graphrag + Ollama** är det billigaste alternativet — bokstavligen gratis förutom el och CPU-tid. Det kör på en Mac med 6 GB VRAM, använder FAISS som vektorlager, och stödjer modeller som `gemma2:2b` via Ollama. Nackdelen är mindre community och färre features.

**txtai** är liknande — helt lokalt, open source, använder SQLite. Enklare men mer beprövat.

**LightRAG** kan köras helt lokalt med Ollama och standardbackends (JSON-filer + NetworkX + NanoVectorDB) — kostnad $0. OpenSearch är ett valfritt backend för horisontell skalning vid 10M+ dokument, men är irrelevant för vårt projekt (se sektion 2 för detaljer). En utvecklare rapporterade $2 300/år totalkostnad för en produktionsmiljö med API-baserade embeddings (jämfört med $39 600 med OpenAI-API:er) — med Ollama lokalt hade det varit $0.

**GraphRAG (Microsoft)** är dyrt: $350–500 för initial indexering av 5 000 dokument med GPT-4o-mini. En bok på 32 000 ord kostar ~$7 att indexera. Inkrementella uppdateringar kräver ofta full omindexering, vilket gör det opraktiskt för vårt arbetsflöde med frekventa wikiediteringar. **LazyGraphRAG** är 1 000x billigare men fortfarande molnberoende.

**Cognee** riktar sig mot enterprise — €1 970/månad för on-premises är orimligt för ett forskningsprojekt.

### Gemini Multimodal RAG

Google erbjuder **Vertex AI RAG Engine** som en del av Vertex AI (serverless, public preview). Det är inte en fristående produkt utan ett API integrerat med Gemini-modellerna.

**Multimodal kapabilitet:** Vertex AI RAG Engine stödjer textfiler (upp till 25 MB per fil) från Cloud Storage, Drive, Slack, Jira och SharePoint. Bildingestion (skannade sidor) är dock inte explicit dokumenterat — skannade JP2/JPEG-sidor skulle sannolikt behöva OCR-förbearbetning (via Google Cloud Document AI) innan ingestion. Det går alltså inte att direkt fråga mot både OCR-text och originalskanningar i en enda sökning utan mellanlager.

**Priser (april 2026):** Gemini 2.5 Pro kostar $1.25/M input-tokens och $10/M output-tokens. Gemini 2.0 Flash är billigare. Vertex AI Vector Search tar betalt för indexbygge, strömmande uppdateringar och lagring — exakta per-GB-priser kräver kontakt med Google sales. Free tier finns för Gemini API (1 500 requests/dag för Flash, 25/dag för Pro) men täcker inte Vertex AI RAG Engine.

**Bedömning:** Gemini Multimodal RAG är intressant konceptuellt men tillför lite mervärde jämfört med LightRAG + Ollama för vårt projekt. Den huvudsakliga fördelen — multimodal sökning över text och bild — kräver ändå OCR-förbearbetning, och vi har redan den pipelinen. Kostnaden ($50–200/månad estimerat) är svår att motivera när lokala alternativ är gratis. Det finns inget "magiskt" multimodalt lager som söker i skannade sidor utan OCR.

**Undantag:** Om Google lanserar äkta bildförståelse i RAG Engine (fråga direkt mot skanningar utan OCR) kan det bli värt att utvärdera igen — men det finns inte idag.

---

## 5. Belastning vid wiki-ingesteringar: hur tungt blir det?

### Problemet

Varje ingestion i LLM-wikin innebär att Claude läser en ny källa och uppdaterar 10–15 wikisidor åt gången. Vid full TEI-ingestion (3 113 personer + 770 platser) kommer tusentals filer att skapas eller uppdateras. Om vi har ett RAG-system som komplement måste det hänga med.

### Embedding-beräkning

För `all-MiniLM-L6-v2` (22 MB modell, 384 dimensioner) via Ollama eller Sentence-Transformers:

- En markdown-fil (~500 ord / ~100 tokens) tar under 30 ms att embeddas
- 5 000 dokument i batch: **2,5–5 minuter på CPU**, snabbare med GPU
- Inkrementell omembedding av 50 ändrade filer: **under 2 sekunder**

Embedding-steget är försumbart — det är inte flaskhalsen.

### Entitetsextraktion (LightRAG)

LightRAG använder en LLM för att extrahera entiteter och relationer vid indexering. Med en lokal 7B-modell via Ollama:

- Exakta benchmarks per dokument saknas i publicerad litteratur
- Rimlig uppskattning: 5–15 sekunder per dokument med en 7B-modell på Apple Silicon
- 4 600 dokument × 10 sek/dok = **~13 timmar** för full initial indexering
- Inkrementell uppdatering av 50 filer: **~8 minuter**

Med en snabbare modell (gemma2:2b) halveras tiden ungefär. Med API (GPT-4o-mini) blir det sekunder per dokument men kostar pengar.

### Batch vs inkrementell

**Initial TEI-ingestion:** Kör som en batch — full omindexering en gång. ~13 timmar med 7B-modell lokalt, eller ~30 minuter med API (kostnad ~$5–15). Det är en engångskostnad.

**Dagligt arbete:** Inkrementella uppdateringar. LightRAG stödjer detta utan full omindexering — nya dokument adderas och entiteter dedupliceras mot befintlig graf. 10–50 filändringar per session = **under 10 minuter lokalt**.

### Scenario: full TEI-ingestion med RAG-sync

```
Fas 3 (TEI-ingestion):
  3 113 personsidor + 770 platssidor = ~3 883 nya markdown-filer
  
  Steg 1: Claude skapar filerna i batchar (wiki-operationen)
  Steg 2: File watcher detekterar ändringar
  Steg 3: LightRAG indexerar inkrementellt
  
  Om vi skapar 50 filer per session:
    78 sessioner × ~8 min RAG-sync = ~10 timmar total RAG-tid (fördelat över veckor)
  
  Om vi kör full batch-indexering efter allt är klart:
    ~13 timmar engångskostnad (kan köras över natten)
```

### Rekommendation

Kör RAG-indexeringen **efter** varje daglig session snarare än i realtid — en cron-job eller manuellt trigger som re-indexerar ändrade filer. Det behöver inte vara synkront med redigeringen.

### Kan det köras som ett cron-job utan tokenkostnad?

**Ja, med en viktig nyans.** LightRAG körs som ett vanligt Python-script (CLI) — det finns inget krav på en webbserver eller molntjänst. Ett nattligt cron-job kan se ut så här:

```bash
# cron: 02:00 varje natt
python3 lightrag_sync.py --working-dir ./rag-index --source-dir ./website/src/
```

Scriptet identifierar ändrade filer sedan senaste körningen och kör inkrementell indexering. **Det kostar inga API-tokens** om man kör med Ollama lokalt.

Däremot är indexeringen inte *helt* passiv beräkning. Den har två steg:

1. **Embedding-beräkning** (vektorer) — ren matematik via en lokal embedding-modell (`all-MiniLM-L6-v2` eller liknande). Snabbt, lätt, inga LLM-anrop.
2. **Entitetsextraktion** (grafen) — kräver en LLM för att läsa varje dokument och identifiera entiteter och relationer. Med Ollama körs detta lokalt på din Mac:s GPU/CPU. Gratis i pengar, men kräver att Ollama-servern är igång och att maskinen är vaken.

I praktiken: om din Mac står på och Ollama körs som bakgrundsprocess, fungerar ett nattligt cron-job utan problem. 50 ändrade filer × ~10 sek/fil = ~8 minuters körning, helt tyst i bakgrunden, noll kronor.

---

## 6. Rekommenderad plan

### Fas A: Behåll Obsidian, testa skalan

Skapa tomma stubs för alla TEI-entiteter (3 113 personer, 770 platser) och mät vault-prestanda i Obsidian. Om autocomplete och graph view är acceptabla, fortsätt med Obsidian som enda verktyg under R&D-fasen.

### Fas B: Lägg till RAG som query-lager

När vaulten närmar sig 2 000+ filer med rik prosa:

1. Välj system: **nano-graphrag + Ollama** (enklast, gratis) eller **LightRAG + Ollama** (mer features, fortfarande gratis)
2. Skriv ett ingestion-script som läser alla `.md`-filer från `wiki/` och `works/`
3. Sätt upp en file watcher (watchdog) med 5-minuters debounce för inkrementell omindexering
4. Exponera RAG-systemet som ett API som Claude kan fråga vid wiki-operationer (query, lint)
5. Kör initial batch-indexering över natten (~13 timmar med 7B-modell lokalt)

### Fas C: Utvärdera om Obsidian kan bytas ut

Om autocomplete-problemen blir outhärdliga vid 5 000+ filer, utvärdera alternativa redigerare (VS Code med Foam, Logseq) som klarar volymen bättre. Markdown-filerna och wikilinks fungerar i alla dessa verktyg.

### Vad vi inte behöver

- **Gemini Multimodal RAG** — tillför inget utöver det vi redan har med OCR-pipeline + lokalt RAG. Kostar $50–200/mån utan tydligt mervärde.
- **GraphRAG (Microsoft)** — för dyrt och kräver full omindexering vid varje ändring. Oförenligt med vårt arbetsflöde.
- **Cognee** — enterprise-prissättning, orimligt för ett forskningsprojekt.

---

## Källor

- Obsidian Forum: "Terabyte size, million notes vaults? How scalable is Obsidian?" (2024)
- Obsidian Forum: "Obsidian with very large vaults / Performance results" (2023)
- Obsidian Forum: "Graph view doesn't work for a large vault" (2025)
- 2025 Obsidian Report Card (practicalpkm.com)
- Lazy-cached vault load plugin (GitHub: d7sd6u/obsidian-lazy-cached-vault-load)
- LightRAG GitHub (HKUDS/LightRAG, v1.4.14, april 2026)
- Maarga Systems: "Understanding GraphRAG vs LightRAG" (2025)
- nano-graphrag GitHub (gusye1234/nano-graphrag)
- Cognee Documentation (docs.cognee.ai)
- Vault MCP Server (GitHub: robbiemu/vault-mcp)
- DasRoot: "RAG for Personal Knowledge Management: Obsidian Integration" (2025)
- Stanford NLP: HistWords — Word Embeddings for Historical Text
- ACL Anthology: "Adapting Multilingual Embedding Models to Historical Text" (2025)
- Jon Roosevelt: "RAG System Cost Savings" — LightRAG kostnadsreduktion (2025)
- Microsoft Tech Community: "GraphRAG Costs Explained" (2025)
- Microsoft Research: "LazyGraphRAG: Setting a New Standard for Quality and Cost" (2025)
- Cognee pricing page (cognee.ai)
- txtai GitHub (neuml/txtai)
- Vertex AI RAG Engine overview (Google Cloud docs, 2026)
- Gemini API Pricing (ai.google.dev, 2026)
- MetaCTO: "The True Cost of Google Gemini" (2026)
- LightRAG paper: arxiv.org/abs/2410.05779 (EMNLP 2025)
- Hugging Face: all-MiniLM-L6-v2 model card
- Stratagem Systems: "RAG Implementation Cost ROI Analysis" (2026)
- LightRAG GitHub: Storage backend documentation och konfigurationsguide
- DEV Community: "Hands-on Experience with LightRAG" (2025)
- PyPI: lightrag-hku paketbeskrivning (backend-alternativ)
- AWS OpenSearch Service: Sizing domains guide
