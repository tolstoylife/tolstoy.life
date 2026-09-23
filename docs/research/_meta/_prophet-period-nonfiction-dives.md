---
layer: reference
lastUpdated: 2026-06-13
tags: [research, planning]
title: "Prophet-period non-fiction — the corpus-dive backlog (essays, articles & other works)"
---

The Prophet period's **fiction and drama** are dived out, and so are the **major treatises** (Confession, What I Believe, On Life, The Kingdom of God Is Within You, What Is Art?, The Slavery of Our Times, What Is Religion?, Bethink Yourselves!, The Law of Violence and the Law of Love, plus the gospel translation and the thematic dives). What is left is the long tail of Tolstoy's non-fiction: the **essays, articles, prefaces, public appeals, autobiography, and compilations** he wrote between 1880 and 1910 that never got a dedicated dive. This file is the plan for working through them.

It is the non-fiction successor to [`_prophet-period-remaining-dives.md`](_prophet-period-remaining-dives.md) (which covered the last four fiction/drama works and is now complete). That file's closing note named "the mid-size late essays without a dedicated work-dive" as the never-queued remainder — this file queues them, and everything around them.

## Decisions locked with Johan (2026-06-13)

- **Coverage:** everything — a complete inventory of the undived Prophet-period non-fiction, not just the marquee pieces.
- **Structure:** hybrid — the **major essays each get their own work-dive** (the same pattern the treatises used); the **many short articles bundle into thematic theme-dives** (the same pattern *Stories for the People* and the *1903 folk tales* used for fiction).
- **Each dive proposes its `works/` record's creation** (almost none of these has a record yet) — the dive never writes the vault.

## How to use this file

1. Pick a dive from [the plan](#the-plan) below (run order is suggested, not binding).
2. If it is one of the **first-wave dives**, a full paste-ready `/corpus-dive` prompt is written out under [Paste-ready prompts](#paste-ready-prompts). Paste it into a fresh session with accept-edits (the proven path), or append `--auto --confirm-scope` to detach.
3. If it is a **later dive**, expand its one-line scope block (in the plan table) into a full prompt using the [shared template](#prompt-template) — every piece it covers, with TEI path and Tom, is in [the inventory](#the-inventory) so you don't have to re-find anything.
4. Each prompt is self-contained on purpose: the new session can't see this file or the conversation that produced it.

**A note on dates.** The TEI file headers carry the *PSS publication* year (1936–58), **not** composition — so every prompt tells the dive to pin the composition window itself in Phase 0 (from the work's own commentary), and the dated slugs below are best-estimates to confirm, not facts. This is the same `tei-diary-filename-year` caution the project already knows.

**A note on translation status.** Most of the short polemical articles already have a published English translation (the Free Age Press / Maude machine kept pace — see the [translation-gap ledger](../late-voice-encryption-compression/translation-gaps.md)). The dives are therefore mostly about *primary-source grounding, genesis, and vault records*, not about filling a translation gap — except where flagged.

---

## What's already dived (the baseline — do not re-dive)

Non-fiction work-dives done: `1879-1880-examination-of-dogmatic-theology`, `1879-1882-a-confession`, `gospel-translation`, `1882-1884-what-i-believe`, `1882-1886-what-then-must-we-do`, `1886-1887-on-life`, `1890-1893-the-kingdom-of-god-is-within-you`, `1893-1894-christianity-and-patriotism`, `1897-1898-what-is-art`, `1900-the-slavery-of-our-times`, `1901-1902-what-is-religion`, `1904-bethink-yourselves`, `1908-the-law-of-violence-and-the-law-of-love`.

Thematic dives that already cover some non-fiction ground (cross-link, don't overlap): `copyright-renunciation` (Posrednik, the public-domain gift, the 1891 copyright letter), `doukhobors`, `crisis` (the 1880s turn), `tolstoyanism`, `christian-anarchism`, `christian-communism-socialism`, `fire-metaphor`, `lords-prayer`, `late-voice-encryption-compression` (the 1900–1910 voice + the anthology/letter translation map).

---

## The inventory {#the-inventory}

Every undived Prophet-period non-fiction piece in the corpus, grouped by the dive it feeds. `path` is under `primary-sources/tolstoydigital-TEI/texts/works/`. **Comp.** = best-estimate composition window (confirm in Phase 0). **EN** = published English translation status (✓ = exists, mostly Maude/Free Age Press; ? = check). **★** marks the marquee piece that anchors (or becomes) a standalone work-dive.

### A · Art & aesthetics → 1 standalone + 1 cluster

| | Title (EN) | RU | path (`vNN_…`) | Tom | Comp. | EN |
|---|---|---|---|---|---|---|
| ★ | On Shakespeare and the Drama | О Шекспире и о драме | `v35_216_272_O_Shekspire_i_o_drame.xml` | 35 | 1903–04 | ✓ 1906 |
| | Preface to the Works of Maupassant | Предисловие к сочинениям Гюи де Мопассана | `v30_003_024_Predislovie_k_sochinenijam_Gjui_de_Mopassana.xml` | 30 | 1893–94 | ? |
| | Preface to the English ed. of *What Is Art?* | Предисловие к английскому изданию ЧТИ | `v30_204_206_…Chto_takoe_iskusstvo.xml` | 30 | 1898 | ✓ |
| | On Gogol | О Гоголе | `v38_050_053_O_Gogole.xml` (+ `v26_648_651`) | 38/26 | 1909 | ? |
| | Preface to Carpenter's "Modern Science" | Предисловие к статье Карпентера | `v31_087_095_…Eduarda_Karpentera_Sovremennaja_nauka.xml` | 31 | 1898 | ? |

### B · Religion & the Church — the 1901 rupture → 1 standalone + 1 cluster

| | Title (EN) | RU | path | Tom | Comp. | EN |
|---|---|---|---|---|---|---|
| ★ | The Christian Teaching | Христианское учение | `v39_117_191_Hristianskoe_uchenie.xml` | 39 | 1894–96 | ✓ 1898 |
| | Reply to the Synod's Edict | Ответ на определение Синода | `v34_245_253_Otvet_na_opredelenie_Sinoda….xml` | 34 | 1901 | ✓ |
| | To the Clergy | К духовенству | `v34_299_318_K_duhovenstvu.xml` | 34 | 1902 | ✓ |
| | The Restoration of Hell | Разрушение ада и восстановление его | `v34_100_115_Razrushenie_ada_i_vosstanovlenie_ego.xml` | 34 | 1902 | ✓ 1903 |
| | Religion and Morality | Религия и нравственность | `v39_003_026_Religija_i_nravstvennost.xml` | 39 | 1893 | ? |
| | How to Read the Gospels | Как читать евангелие | `v39_113_116_Kak_chitat_evangelie….xml` | 39 | 1896 | ? |
| | The Teaching of Christ for Children | Учение Христа изложенное для детей | `v37_097_147_Uchenie_Hrista_izlozhennoe_dlja_detej.xml` | 37 | 1907–08 | ? |
| | On Religious Tolerance | О веротерпимости | `v34_291_298_O_veroterpimosti.xml` | 34 | 1901 | ? |

### C · Land, labour & the social question → 1 standalone + 1 cluster

| | Title (EN) | RU | path | Tom | Comp. | EN |
|---|---|---|---|---|---|---|
| ★ | The Great Sin (the land monopoly) | Великий грех | `v36_206_230_Velikij_greh.xml` | 36 | 1905 | ✓ |
| | To the Working People | К рабочему народу | `v35_121_156_K_rabochemu_narodu.xml` | 35 | 1902 | ✓ |
| | The First Step (diet & the moral ladder) | Первая ступень | `v29_057_085_Pervaja_stupen.xml` | 29 | 1891 | ✓ |
| | The Only Possible Solution of the Land Question | Единственное возможное решение земельного вопроса | `v36_283_289_….xml` | 36 | 1906 | ? |
| | Letter to a Peasant on the Land (Henry George) | Письмо к крестьянину о земле | `v90_075_076_Pismo_k_krestjaninu_o_zemle….xml` | 90 | 1905 | ? |
| | Preface to Henry George | Предисловие к Генри Джорджу | `v36_300_303_….xml` | 36 | 1906 | ? |
| | How the Working People Can Free Themselves | Как освободиться рабочему народу | `v90_069_074_Kak_osvoboditsja_rabochemu_narodu.xml` | 90 | 1905 | ? |

### D · 1905 — revolution, the state & non-participation → 1 standalone + 1 cluster

| | Title (EN) | RU | path | Tom | Comp. | EN |
|---|---|---|---|---|---|---|
| ★ | The End of the Age | Конец века | `v36_231_277_Konets_veka.xml` | 36 | 1905 | ✓ 1906 |
| | On the Significance of the Russian Revolution | О значении русской революции | `v36_315_362_O_znachenii_russkoj_revoljutsii.xml` | 36 | 1906 | ? |
| | The One Thing Needful | Единое на потребу | `v36_166_205_Edinoe_na_potrebu.xml` | 36 | 1905 | ? |
| | An Appeal to the Russian People | Обращение к русским людям | `v36_304_314_Obraschenie_k_russkim_ljudjam….xml` | 36 | 1906 | ? |
| | To Statesmen / Political Activists | К политическим деятелям | `v35_199_215_K_politicheskim_dejateljam.xml` | 35 | 1903 | ? |
| | On the Social Movement in Russia | Об общественном движении в России | `v36_156_165_Ob_obschestvennom_dvizhenii_v_Rossii.xml` | 36 | 1905 | ? |
| | The Inevitable Revolution | Неизбежный переворот | `v38_072_099_Neizbezhnyj_perevorot.xml` | 38 | 1909 | ? |
| | On the State | О государстве | `v38_291_293_O_gosudarstve.xml` | 38 | 1909 | ? |

### E · War, peace & patriotism → 1 standalone + 1 cluster

| | Title (EN) | RU | path | Tom | Comp. | EN |
|---|---|---|---|---|---|---|
| ★ | Patriotism and Government | Патриотизм и правительство | `v90_425_444_Patriotizm_i_pravitelstvo.xml` | 90 | 1900 | ✓ |
| | Patriotism, or Peace? | Патриотизм или мир | `v90_045_053_Patriotizm_ili_mir.xml` | 90 | 1896 | ✓ |
| | Two Wars | Две войны | `v31_097_101_Dve_vojny.xml` | 31 | 1898 | ? |
| | Carthago delenda est | Carthago delenda est | `v39_197_205_Carthago_delenda_est.xml` | 39 | 1898 | ? |
| | Address to the Stockholm Peace Congress | Доклад для конгресса мира в Стокгольме | `v38_119_125_Doklad…kongressa_mira_v_Stokgolme.xml` | 38 | 1909 | ? |
| | On the Annexation of Bosnia & Herzegovina | О присоединении Боснии и Герцеговины к Австрии | `v37_222_242_O_prisoedinenii_Bosnii_i_Gertsegoviny….xml` | 37 | 1908 | ? |
| | The Soldiers' / Officers' Memorandum | Солдатская памятка / Офицерская памятка | `v34_280_283` / `v34_284_290` | 34 | 1901 | ? |
| | Letter to a Non-Commissioned Officer | Письмо к фельдфебелю | `v90_054_059_Pismo_k_feldfebelju.xml` | 90 | 1899 | ? |

### F · Capital punishment & the late conscience (1900–1910) → 1 standalone + 1 cluster

| | Title (EN) | RU | path | Tom | Comp. | EN |
|---|---|---|---|---|---|---|
| ★ | I Cannot Be Silent | Не могу молчать | `v37_083_096_Ne_mogu_molchat.xml` | 37 | 1908 | ✓ 1908 |
| | Thou Shalt Not Kill | Не убий | `v34_200_205_Ne_ubij.xml` | 34 | 1900 | ✓ 1900 |
| | Thou Shalt Not Kill Anyone | Не убий никого | `v37_039_054_Ne_ubij_nikogo.xml` | 37 | 1907 | ✓ 1907 |
| | Capital Punishment and Christianity | Смертная казнь и христианство | `v38_039_048_Smertnaja_kazn_i_hristianstvo.xml` | 38 | 1908–09 | ? |
| | To the Tsar and His Assistants | Царю и его помощникам | `v34_239_244_Tsarju_i_ego_pomoschnikam.xml` | 34 | 1901 | ✓ 1903 |
| | The Only Means | Единственное средство | `v34_254_269_Edinstvennoe_sredstvo.xml` | 34 | 1901 | ? |
| | Three Days in the Village | Три дня в деревне | `v38_005_022_Tri_dnja_v_derevne…` (3 files) | 38 | 1909–10 | ? |

### G · A Letter to a Hindu & the global appeals (the Gandhi text) → 1 standalone

| | Title (EN) | RU | path | Tom | Comp. | EN |
|---|---|---|---|---|---|---|
| ★ | A Letter to a Hindu | Письмо к индусу | `v37_245_272_Letter_to_a_Hindoo_Pismo_k_indusu.xml` | 37 | 1908 | ✓ 1909 |
| | Letter to a Chinese | Письмо к китайцу | `v36_290_299_Pismo_k_kitajtsu.xml` | 36 | 1906 | ? |
| | An Address to the Chinese People | Обращение к китайскому народу | `v34_339_342_Obraschenie_k_kitajskomu_narodu.xml` | 34 | 1900 | ? |

This dive carries the **Gandhi correspondence thread** (PSS letter Toms 80/81/82 — three letters, 25 Sep 1909 / 25 Apr 1910 / 7 Sep 1910) and is the natural follow-on to the [Prophet-period essay visualisations](../../../_generated/research/session-prophet-essays-viz-2026-06-12/) made on 2026-06-12.

### H · Autobiography & memoir → 1 standalone

| | Title (EN) | RU | path | Tom | Comp. | EN |
|---|---|---|---|---|---|---|
| ★ | Reminiscences | Воспоминания | `v34_345_393_Vospominanija.xml` (+ synopsis `v34_343_344`) | 34 | 1903–06 | partial |
| | Notes for Biryukov's *Biography* | Вставки и замечания к рукописи Биографии… Бирюкова | `v34_394_400_….xml` | 34 | 1905–08 | — |
| | Reminiscences of N. Ya. Grot | Воспоминания о Н. Я. Гроте | `v38_421_425_Vospominanija_o_N_Ja_Grote.xml` | 38 | 1910 | ? |

Cross-link `biryukov-biography-editions` and `biryukov-sofia-relationship` heavily — the *Reminiscences* were written *for* Biryukov's biography.

### I · The famine relief writings (1891–93, with the 1898 echo) → 1 cluster

| | Title (EN) | RU | path | Tom | Comp. | EN |
|---|---|---|---|---|---|---|
| | On the Famine | О голоде | `v29_086_116_O_golode.xml` | 29 | 1891 | ✓ |
| | A Terrible Question | Страшный вопрос | `v29_117_125_Strashnyj_vopros.xml` | 29 | 1891 | ? |
| | On Means of Helping the Population | О средствах помощи населению… | `v29_126_144_….xml` | 29 | 1892 | ? |
| | The relief reports (4) | Отчёты… | `v29_145_156`, `v29_157_168`, `v29_169_172`, `v29_202_204` | 29 | 1892–93 | ? |
| | Famine or No Famine? | Голод или не голод | `v29_215_230_Golod_ili_ne_golod.xml` | 29 | 1898 | ? |
| | Afterword to the appeal "Help!" | Послесловие к воззванию «Помогите» | `v39_192_196_….xml` | 39 | 1896 | ? |

Cross-link `copyright-renunciation` (the same 1891 moment) and `doukhobors` ("Help!" was the Doukhobor appeal).

### J · The wisdom anthologies — the compiler Tolstoy → 1 cluster (see caveat)

| | Title (EN) | RU | path | Tom | Comp. | EN |
|---|---|---|---|---|---|---|
| | Thoughts of Wise People for Every Day | Мысли мудрых людей на каждый день | `v40_069_216_….xml` | 40 | 1903 | untranslated |
| | The Circle of Reading (daily aphorisms) | Круг чтения | Toms 41–42 (`krug_chtenija/`) | 41–42 | 1904–08 | selection |
| | For Every Day | На каждый день | `v43_…`, `v44_…` | 43–44 | 1909 | uncertain |
| | The Path of Life | Путь жизни | `v45_013_496_Put_zhizni.xml` | 45 | 1910 | ✓ |

**Caveat:** the [late-voice dive](../late-voice-encryption-compression/) already mapped these heavily (translation status, the compression argument, the weekly-tale layer is its own dive `1905-1906-krug-chtenija-tales`). This cluster may be better run as a **Phase-3 enrichment of the late-voice dive** (add the `workRecord` proposals + a compiler-focused genesis section) than as a fresh dive. Decide at run time.

### K · Science, education & culture — the catch-all → 1 cluster (lowest priority)

| | Title (EN) | RU | path | Tom | Comp. | EN |
|---|---|---|---|---|---|---|
| | On Science | О науке | `v38_132_149_O_nauke.xml` | 38 | 1909 | ? |
| | On Education | О воспитании | `v38_062_069_O_vospitanii.xml` | 38 | 1909 | ? |
| | Letter to a Student on Law | Письмо студенту о праве | `v38_054_061_Pismo_studentu_o_prave.xml` | 38 | 1909 | ? |
| | On *Vekhi* | О Вехах | `v38_285_290_O_Vehah.xml` | 38 | 1909 | ? |
| | On Socialism | О социализме | `v38_426_432_O_sotsializme.xml` | 38 | 1910 | ? |
| | A Conversation with Children on Moral Questions | Беседа с детьми по нравственным вопросам | `v37_031_038_….xml` | 37 | 1908 | ? |
| | Our Understanding of Life | Наше жизнепонимание | `v37_023_030_Nashe_zhizneponimanie.xml` | 37 | 1907 | ? |

Tom 38 holds many more one- and two-page late pieces (letters-to-editors, replies, fragments) — sweep the whole Tom in this dive's Phase 1 and let the dive decide which earn an evidence row. The cluster is a **catch-all** by design.

---

## The plan {#the-plan}

Fourteen dives — **8 standalone work-dives** (the marquee essays) + **6 thematic theme-dives** (the clusters). Suggested run order interleaves a marquee dive with the related cluster so each pair shares a freshly-built context base.

| # | Dive | Kind | Slug | Members | Prompt |
|---|---|---|---|---|---|
| 1 | **A Letter to a Hindu** | work-dive | `1908-a-letter-to-a-hindu` | G★ + 2 | [full ↓](#p1) |
| 2 | **I Cannot Be Silent** | work-dive | `1908-i-cannot-be-silent` | F★ | [full ↓](#p2) |
| 3 | Against the death penalty | theme | `death-penalty` | F cluster (6) | [full ↓](#p3) |
| 4 | **On Shakespeare and the Drama** | work-dive | `1903-1906-on-shakespeare-and-the-drama` | A★ | [full ↓](#p4) |
| 5 | Art & aesthetics satellites | theme | `art-aesthetics-satellites` | A cluster (4) | [full ↓](#p7) |
| 6 | **The Christian Teaching** | work-dive | `1894-1896-the-christian-teaching` | B★ | [full ↓](#p5) |
| 7 | The break with the Church (1901) | theme | `1901-break-with-the-church` | B cluster (7) | [full ↓](#p6) |
| 8 | **The Great Sin** | work-dive | `1905-the-great-sin` | C★ | [full ↓](#p8) |
| 9 | The land question & Henry George | theme | `land-question-henry-george` | C cluster (6) | template |
| 10 | **The End of the Age** | work-dive | `1905-the-end-of-the-age` | D★ | template |
| 11 | 1905: revolution & the state | theme | `1905-revolution-and-the-state` | D cluster (7) | template |
| 12 | **Patriotism and Government** | work-dive | `1900-patriotism-and-government` | E★ | template |
| 13 | Against patriotism & war | theme | `against-patriotism-and-war` | E cluster (7) | template |
| 14 | **Reminiscences** | work-dive | `1903-1906-reminiscences` | H★ + 2 | template |
| — | The famine relief writings | theme | `1891-1893-famine-relief` | I cluster (8) | template |
| — | Science, education & culture | theme | `science-education-culture` | K cluster (7+) | template |
| — | The wisdom anthologies | theme *or* late-voice Phase-3 | `wisdom-anthologies` | J cluster (4) | see [caveat](#j--the-wisdom-anthologies--the-compiler-tolstoy--1-cluster-see-caveat) |

**Why this order.** Start with the two pieces tied to current momentum and Johan's stated interest — *A Letter to a Hindu* (the Gandhi text, follow-on to the 2026-06-12 visualisations) and *I Cannot Be Silent* (the most famous late essay). Then alternate marquee + cluster so the theme-dive inherits the marquee dive's freshly-gathered context (e.g. run *I Cannot Be Silent* → *Against the death penalty*, which reuses it). The famine, science/education, and anthologies clusters are lowest-value-per-effort and sit at the end.

---

## Prompt template {#prompt-template}

For any dive marked "template" above, expand it into a full prompt with this skeleton. The inventory gives every member's TEI path + Tom; drop them in.

**Standalone work-dive (marquee essay):**

```
/corpus-dive --novel? NO — a work-subject dive but NOT a novel; it is a non-fiction essay. [TITLE] ([Russian title]), Tolstoy's [year] [essay/treatise]. Main text: works/[path] (PSS Tom [N]).

KEY FACTS to pin in Phase 0:
- Composition window: [estimate] — read the Tom's commentary (история писания) to pin it; set the dated slug from the COMPOSITION window, not publication.
- No works/ record exists yet → the workRecord PROPOSES creation ([genre/category — non-fiction/essays-and-criticism or /treatises, judge by length]).
- Marquee-question candidate (test as hypothesis, don't assert): [the essay's central claim] — triangulate confirms/complicates/contradicts/extends.
- English translation: [status from the inventory; if ✓, defer to the published edition and don't re-translate beyond working glosses].

Cross-link prior dives: [the related sibling dives]. Ground in primary + prior dives before mainstream scholarship.

Gates: --choice=reg --notes=auto, verify_quotes.py exit 0, record-creating workRecord, Genesis + reception + marquee sections, bare voice, no vault writes, separate-pass verifier, Phase 6 + 7 handoffs. Commit, don't push. Plain language.
```

> Note: these essays are **not** `--novel` — that flag is only for novels/long narratives. They are ordinary work-subject dives (single work → one `workRecord`), which carry the genesis/reception/marquee spine without the novel-mode re-weighting.

**Thematic theme-dive (cluster):**

```
/corpus-dive [THEME NAME] — a multi-work theme dive carrying several workRecord proposals (like docs/research/1903-folk-tales/ and docs/research/stories-for-the-people/). NOT --novel.

SCOPE (the cluster, all confirmed):
- [Title] — works/[path] (Tom [N], [year])
- [Title] — works/[path] (Tom [N], [year])
  […every member from the inventory…]

No works/ records exist for any of these → each workRecord PROPOSES creation (derive recordPath from genre/category; flag any anthology/subcategory shelving gap in needsReview, don't invent vocab).

Read the prior sibling dives first and cross-link them (ground in the project before the mainstream): [related dives]. 

Gates: --choice=reg --notes=auto, verify_quotes.py exit 0, bare voice, no vault writes (propose only), separate-pass verifier, Phase 6 run-report + Phase 7 handoff. Commit, do NOT push. Plain language.
```

---

## Paste-ready prompts

The first-wave dives, written out in full. Each is self-contained.

### P1 — A Letter to a Hindu (run first) {#p1}

```
/corpus-dive A Letter to a Hindu (Письмо к индусу), Tolstoy's 1908 open letter — a work-subject dive (single work → one workRecord), NOT --novel. Main text: works/v37_245_272_Letter_to_a_Hindoo_Pismo_k_indusu.xml (PSS Tom 37; the TEI carries both the English title and the Russian «Письмо к индусу»).

KEY FACTS to pin in Phase 0:
- Written Dec 1908 as a reply to Tarak Nath Das (editor of Free Hindustan); pin the exact composition/redaction dates from the v37 commentary (история писания). Set the dated slug 1908-a-letter-to-a-hindu.
- No works/ record exists yet → the workRecord PROPOSES creation (non-fiction; essays-and-criticism or open-letters — judge by the works schema).
- THE GANDHI THREAD IS THE CENTRE OF THE RECEPTION STORY. Gandhi read this letter, asked Tolstoy's permission to reprint it, and published it in Indian Opinion (1909) with his own preface; it shaped his satyagraha. Sweep the Gandhi correspondence: letters/v80_149_MaxatmeGandiMohandasGandhi.xml (25 Sep 1909), letters/v81_318_M_GandiM_Gandhi.xml (25 Apr 1910), letters/v82_178_GandiGandhi.xml (7 Sep 1910 — the long non-resistance letter). Route Gandhi as a person entity (ingestionPriority 1). The published EN exists (Indian Opinion 1909) — confirm the translator/edition; use working glosses only for passages you quote.
- Companion pieces to cross-reference (don't deep-dive here, they belong to their own cluster): Letter to a Chinese (works/v36_290_299_Pismo_k_kitajtsu.xml, 1906) and An Address to the Chinese People (works/v34_339_342, 1900) — Tolstoy's wider "letter to the colonised East" gesture.
- Marquee-question candidate (test, don't assert): the letter's claim that India is held by a handful of Englishmen only because Indians consent to participate in violence — non-resistance as the lever of liberation. Triangulate confirms/complicates/extends against the Gandhi scholarship.

Cross-link prior dives: 1908-the-law-of-violence-and-the-law-of-love (the same year's systematic statement), 1890-1893-the-kingdom-of-god-is-within-you (the non-resistance root Gandhi also read), christian-anarchism, tolstoyanism. Reuse the 2026-06-12 Prophet-essay visualisation data if useful (_generated/research/session-prophet-essays-viz-2026-06-12/). Ground in primary + prior dives before mainstream scholarship.

Gates: --choice=reg --notes=auto, verify_quotes.py exit 0, record-creating workRecord, Genesis + Reception (the Gandhi story) + marquee sections, heavy on the correspondence, bare voice, no vault writes, separate-pass verifier, Phase 6 + 7 handoffs. Commit, don't push. Plain language.
```

### P2 — I Cannot Be Silent {#p2}

```
/corpus-dive I Cannot Be Silent (Не могу молчать), Tolstoy's 1908 essay against capital punishment — a work-subject dive (single work → one workRecord), NOT --novel. Main text: works/v37_083_096_Ne_mogu_molchat.xml (PSS Tom 37). Variants: works/v37_391_399_Ne_mogu_molchat_Varianty.xml.

KEY FACTS to pin in Phase 0:
- Written May–July 1908, provoked by a newspaper report of twenty (or twelve) hangings; pin the exact dates and the triggering report from the v37 commentary. Set the dated slug 1908-i-cannot-be-silent.
- No works/ record exists yet → the workRecord PROPOSES creation (non-fiction; essays-and-criticism).
- Publication is itself the story: it was published abroad and in fragments in the Russian press (with passages cut), and Tolstoy invited his own prosecution. Cover the censorship/printing history as reception.
- English translation exists (L. & A. Maude, Free Age Press, same year 1908) — defer to it; working glosses only for quoted passages.
- Marquee-question candidate (test, don't assert): the personal-complicity argument — Tolstoy demands to be hanged alongside the condemned because the executions are carried out in his name. Triangulate confirms/complicates/extends.

Cross-link prior dives: 1908-the-law-of-violence-and-the-law-of-love (the twin 1908 statement). This dive seeds the death-penalty theme-dive (P3) — note that in the handoff so the cluster reuses it. Ground in primary + prior dives before mainstream.

Gates: --choice=reg --notes=auto, verify_quotes.py exit 0, record-creating workRecord, Genesis + censorship/reception + marquee sections, bare voice, no vault writes, separate-pass verifier, Phase 6 + 7 handoffs. Commit, don't push. Plain language.
```

### P3 — Against the death penalty (theme-dive) {#p3}

```
/corpus-dive Against the death penalty — Tolstoy's writings against capital punishment and state killing, 1900–1910 — a multi-work theme dive carrying several workRecord proposals (like docs/research/1903-folk-tales/). NOT --novel.

SCOPE (the cluster, all confirmed):
- Thou Shalt Not Kill — works/v34_200_205_Ne_ubij.xml (Tom 34, 1900; on the assassination of King Humbert / regicide)
- Thou Shalt Not Kill Anyone — works/v37_039_054_Ne_ubij_nikogo.xml (Tom 37, 1907)
- Capital Punishment and Christianity — works/v38_039_048_Smertnaja_kazn_i_hristianstvo.xml (Tom 38, 1908–09)
- To the Tsar and His Assistants — works/v34_239_244_Tsarju_i_ego_pomoschnikam.xml (Tom 34, 1901)
- The Only Means — works/v34_254_269_Edinstvennoe_sredstvo.xml (Tom 34, 1901)
- Three Days in the Village — works/v38_005_012, v38_012_018, v38_019_022 (the three "days", Tom 38, 1909–10; poverty + the gallows as its end-point)

Treat I Cannot Be Silent (the 1908 marquee, dived separately at docs/research/1908-i-cannot-be-silent/ if P2 ran first) as the cluster's centrepiece — cross-reference it, don't re-extract. No works/ records exist for the cluster members → each workRecord PROPOSES creation (non-fiction/essays-and-criticism). Most have published English (Maude/Free Age Press) — confirm per piece; working glosses only.

Read the prior sibling dives first and cross-link: 1908-i-cannot-be-silent, 1908-the-law-of-violence-and-the-law-of-love, 1889-1899-resurrection (the courts/punishment), christian-anarchism. Ground in the project before the mainstream.

Gates: --choice=reg --notes=auto, verify_quotes.py exit 0, bare voice, no vault writes (propose only), separate-pass verifier, Phase 6 run-report + Phase 7 handoff. Commit, do NOT push. Plain language.
```

### P4 — On Shakespeare and the Drama {#p4}

```
/corpus-dive On Shakespeare and the Drama (О Шекспире и о драме), Tolstoy's essay — a work-subject dive (single work → one workRecord), NOT --novel. Main text: works/v35_216_272_O_Shekspire_i_o_drame.xml (PSS Tom 35). Variants: works/v35_557_577_Varianty_k_state_O_Shekspire_i_o_drame.xml.

KEY FACTS to pin in Phase 0:
- Written 1903–04, published 1906 (as the preface to Ernest Crosby's "Shakespeare and the Working Classes"); pin the dates from the v35 commentary. Set the dated slug 1903-1906-on-shakespeare-and-the-drama.
- No works/ record exists yet → the workRecord PROPOSES creation (non-fiction; essays-and-criticism).
- This is the practical sequel to What Is Art? (dived: 1897-1898-what-is-art) — the famous attack on King Lear and on Shakespeare's reputation as a case study of the theory. Cross-link it heavily; the marquee tension is whether the Shakespeare essay confirms or over-extends the What Is Art? doctrine.
- English translation exists (Tchertkoff & I. F. Mayo, Funk & Wagnalls 1906, published with the Russian) — defer to it; working glosses only.
- Marquee-question candidate (test, don't assert): Tolstoy's claim that Shakespeare's fame is a collective hypnotic suggestion and that his drama fails the religious-art test — sincerity vs. craft.

Cross-link prior dives: 1897-1898-what-is-art (the governing theory), and note Ernest Crosby (works/v40_339_340 records Tolstoy's first acquaintance with Crosby) as a person entity. Ground in primary + prior dives before mainstream Shakespeare scholarship (which is overwhelmingly hostile to this essay — attribute, read critically).

Gates: --choice=reg --notes=auto, verify_quotes.py exit 0, record-creating workRecord, Genesis + reception + marquee sections, bare voice, no vault writes, separate-pass verifier, Phase 6 + 7 handoffs. Commit, don't push. Plain language.
```

### P5 — The Christian Teaching {#p5}

```
/corpus-dive The Christian Teaching (Христианское учение), Tolstoy's systematic exposition of his religion — a work-subject dive (single work → one workRecord), NOT --novel. Main text: works/v39_117_191_Hristianskoe_uchenie.xml (PSS Tom 39).

KEY FACTS to pin in Phase 0:
- Written 1894–96 (a long, much-redrafted catechism-style statement); pin the window from the v39 commentary. Set the dated slug 1894-1896-the-christian-teaching.
- No works/ record exists yet → the workRecord PROPOSES creation (non-fiction; treatises).
- This is the calm, ordered restatement of the doctrine that The Kingdom of God Is Within You (dived: 1890-1893-the-kingdom-of-god-is-within-you) argued polemically — cross-link it as the systematic sibling. English translation exists (The Christian Teaching, Free Age Press 1898) — confirm; working glosses only.
- Marquee-question candidate (test, don't assert): whether the work softens or systematises the Kingdom-of-God ethic — doctrine as catechism vs. doctrine as polemic.

Cross-link prior dives: 1890-1893-the-kingdom-of-god-is-within-you, 1901-1902-what-is-religion, gospel-translation, christian-anarchism. Ground in primary + prior dives before mainstream.

Gates: --choice=reg --notes=auto, verify_quotes.py exit 0, record-creating workRecord, Genesis + marquee sections, bare voice, no vault writes, separate-pass verifier, Phase 6 + 7 handoffs. Commit, don't push. Plain language.
```

### P6 — The break with the Church, 1901 (theme-dive) {#p6}

```
/corpus-dive The break with the Church — Tolstoy, the Holy Synod, and the 1901 excommunication — a multi-work theme dive carrying several workRecord proposals (like docs/research/1903-folk-tales/). NOT --novel.

SCOPE (the cluster, all confirmed):
- Reply to the Synod's Edict — works/v34_245_253_Otvet_na_opredelenie_Sinoda….xml (Tom 34, 1901; the direct reply to the 20–22 Feb 1901 excommunication)
- To the Clergy — works/v34_299_318_K_duhovenstvu.xml (Tom 34, 1902)
- The Restoration of Hell — works/v34_100_115_Razrushenie_ada_i_vosstanovlenie_ego.xml (Tom 34, 1902; the satirical legend on the church as the devils' restoration of hell)
- Religion and Morality — works/v39_003_026_Religija_i_nravstvennost.xml (Tom 39, 1893)
- How to Read the Gospels — works/v39_113_116_Kak_chitat_evangelie….xml (Tom 39, 1896)
- The Teaching of Christ for Children — works/v37_097_147_Uchenie_Hrista_izlozhennoe_dlja_detej.xml (Tom 37, 1907–08)
- On Religious Tolerance — works/v34_291_298_O_veroterpimosti.xml (Tom 34, 1901)

No works/ records exist → each workRecord PROPOSES creation (non-fiction/essays-and-criticism or /treatises by length). Several have published English (Maude, "My Reply to the Synod"; Tchertkoff, "The Restoration of Hell"/"The Overthrow of Hell") — confirm per piece; working glosses only. The 1901 excommunication is the spine event — give the Synod's edict and the Russian society/church reaction a dedicated reception pass.

Read the prior sibling dives first and cross-link: 1901-1902-what-is-religion, 1890-1893-the-kingdom-of-god-is-within-you, 1894-1896-the-christian-teaching (if P5 ran), gospel-translation, christian-anarchism. Ground in the project before the mainstream; don't let "heretic"/"apostate" framings stick in the dive's own voice — attribute them to the Synod and press.

Gates: --choice=reg --notes=auto, verify_quotes.py exit 0, bare voice, no vault writes (propose only), separate-pass verifier, Phase 6 run-report + Phase 7 handoff. Commit, do NOT push. Plain language.
```

### P7 — Art & aesthetics satellites (theme-dive) {#p7}

```
/corpus-dive Art & aesthetics satellites — the short pieces orbiting What Is Art?, where Tolstoy applies his religious-art test to specific writers and cases — a multi-work theme dive carrying several workRecord proposals (like docs/research/1903-folk-tales/ and docs/research/stories-for-the-people/). NOT --novel.

SCOPE (the cluster, all confirmed):
- Preface to the Works of Maupassant (Предисловие к сочинениям Гюи де Мопассана) — works/v30_003_024_Predislovie_k_sochinenijam_Gjui_de_Mopassana.xml (Tom 30, 1893–94); variants works/v30_273_302_Predislovie_k_sochinenijam_Gjui_de_Mopassana_Varianty.xml
- Preface to the English edition of What Is Art? (Предисловие к английскому изданию ЧТИ) — works/v30_204_206_Predislovie_k_anglijskomu_izdaniju_traktata_Chto_takoe_iskusstvo.xml (Tom 30, 1898; published English exists — defer to it, working glosses only)
- On Gogol (О Гоголе) — works/v38_050_053_O_Gogole.xml (Tom 38, 1909), with the earlier piece works/v26_648_651_O_Gogole.xml (Tom 26) and variants works/v38_280_280_O_Gogole_Varianty.xml
- Preface to Carpenter's "Modern Science" (Предисловие к статье Эдуарда Карпентера «Современная наука») — works/v31_087_095_Predislovie_k_state_Eduarda_Karpentera_Sovremennaja_nauka.xml (Tom 31, 1898)

SUPPORTING DRAFTS (fold in as genesis material — do NOT give these their own workRecords): the What Is Art? genesis-draft cluster — works/v30_213_215_…, v30_216_225_…, v30_226_230_…, v30_231_239_Nauka_i_iskusstvo.xml, v30_240_242_O_nauke_i_iskusstve.xml, v30_243_270_O_tom_chto_nazyvajut_iskusstvom.xml. Use them to show how the doctrine took shape; they belong to What Is Art?, not to this cluster's records.

KEY FACTS to pin in Phase 0:
- Confirm each piece's composition window from its Tom's commentary (история писания); the TEI headers carry PSS publication years, not composition. Set each dated slug from the COMPOSITION window. Cluster slug: art-aesthetics-satellites.
- No works/ records exist for any of these → each workRecord PROPOSES creation (non-fiction; essays-and-criticism, or prefaces if the schema has a subcategory — flag any shelving gap in needsReview, don't invent vocab).
- Connective tissue (test as hypotheses, don't assert): each piece is the religious-art test applied to a case — Maupassant a writer Tolstoy admired despite himself; Gogol the religious-turn writer; Carpenter the science-vs-art boundary. Triangulate confirms/complicates/extends against the What Is Art? doctrine; note where a case strains the theory.
- Route Guy de Maupassant, Nikolai Gogol, and Edward Carpenter as person entities. Ernest Crosby already appears in the Shakespeare dive — cross-reference, don't duplicate.

Read the prior sibling dives first and cross-link them (ground in the project before the mainstream): 1897-1898-what-is-art (the governing theory this cluster orbits) and 1903-1906-on-shakespeare-and-the-drama (the marquee case-study, already dived — this cluster is its satellites). Don't let mainstream aesthetic-criticism framings stick in the dive's own voice; attribute and read critically.

Gates: --choice=reg --notes=auto, verify_quotes.py exit 0, bare voice, no vault writes (propose only), separate-pass verifier, Phase 6 run-report + Phase 7 handoff. Commit, do NOT push. Plain language.
```

### P8 — The Great Sin {#p8}

```
/corpus-dive The Great Sin (Великий грех), Tolstoy's 1905 essay on the private ownership of land — a work-subject dive (single work → one workRecord), NOT --novel. Main text: works/v36_206_230_Velikij_greh.xml (PSS Tom 36). Variants: works/v36_464_475_Velikij_greh_Varianty.xml. Commentary (история писания): comments/v36_656_665_Velikij_greh.xml.

KEY FACTS to pin in Phase 0:
- Written 1905, during and about the Revolution of 1905; pin the exact composition window and redaction dates from the v36 commentary (история писания) — the TEI header carries the PSS publication year, not composition. Set the dated slug 1905-the-great-sin from the COMPOSITION window.
- No works/ record exists yet → the workRecord PROPOSES creation (non-fiction; essays-and-criticism — it is essay-length, ~25 pp, Tom 36 pp. 206–230; judge essays-and-criticism vs treatises by length/form and flag any shelving doubt in needsReview, don't invent vocab).
- Marquee-question candidate (test as hypothesis, don't assert): Tolstoy's claim that private property in land is «великий грех» — the great sin/iniquity at the root of the people's poverty and the 1905 unrest — and that Henry George's single tax (единый налог / land-value taxation) is its just and practical remedy. THE CONTESTED TENSION TO TRIANGULATE: this is the clearest case of Tolstoy the Christian anarchist — who denies the state any legitimate coercive role — endorsing a STATE-administered fiscal reform. Does The Great Sin confirm, complicate, or contradict his anti-statism (does he frame the single tax as a transitional concession, a lesser evil, or a genuine exception)? Triangulate confirms/complicates/contradicts/extends against The Kingdom of God Is Within You and The Slavery of Our Times.
- HENRY GEORGE IS THE CENTRE OF THE INTELLECTUAL DEBT. Route Henry George (1839–1897, American political economist, Progress and Poverty 1879, the single-tax movement) as a person entity (ingestionPriority 1); Tolstoy had read and championed George since the 1880s. This dive SEEDS the land-question theme-dive (P9, land-question-henry-george) — note that in the Phase 7 handoff so the cluster reuses it; do NOT deep-dive the cluster satellites here (To the Working People, The First Step, the George prefaces, etc. — they belong to P9), only cross-reference them.
- English translation exists — "A Great Iniquity" (1905; it appeared in The Times of London and as a single-tax-movement pamphlet). Confirm the translator/edition from the commentary or scholarship; defer to the published edition, use working glosses only for quoted passages.

Cross-link prior dives: 1900-the-slavery-of-our-times (the economic/labour critique this extends), 1890-1893-the-kingdom-of-god-is-within-you (the anti-statism the single tax tests), christian-communism-socialism, christian-anarchism, copyright-renunciation (the renunciation-of-property strand). Ground in primary + prior dives before mainstream scholarship.

Gates: --choice=reg --notes=auto, verify_quotes.py exit 0, record-creating workRecord, Genesis + reception (the 1905 context + Russian/foreign reception) + marquee sections, bare voice, no vault writes, separate-pass verifier, Phase 6 + 7 handoffs. Commit, don't push. Plain language.
```

The remaining dives (9–14, famine, science/education, anthologies) use the [template](#prompt-template) — every member, path, and Tom is in [the inventory](#the-inventory).

---

## Out of scope (raise with Johan separately)

- **The unfinished late fiction fragments** — *Notes of a Madman* (`v26_466`), *Khodynka* (`v38_205`), *The Posthumous Notes of Fyodor Kuzmich* (`v36_059`), *Father Vasily* (`v36_086`), *There Are No Guilty People in the World* (`v38_181/203/245`). These are **fiction**, not essays — they belong to a separate fiction-fragments backlog, not this non-fiction file. Named here only so they're not lost.
- **The "What Is Art?" genesis-draft cluster** (`v30_213`–`v30_270`) — a dozen short art-theory drafts. Folded into dive 5 (art satellites) as supporting drafts, not their own dive.
- **The wisdom anthologies** (group J) — likely better as a Phase-3 enrichment of the existing late-voice dive than a fresh dive; see the caveat above.

## Skills for the next session

- **`corpus-dive`** — the engine for every dive here (`--auto --confirm-scope` to detach; plain `/corpus-dive` for the in-session accept-edits path).
- **`start-of-day`** — to pick the next dive and confirm scope before running.
- After a batch of dives ships, **`obsidian-*` / the LLM wiki ingestion method** turns the finished dossiers into vault pages (the separate, human-in-the-loop step the dives deliberately stop short of).
