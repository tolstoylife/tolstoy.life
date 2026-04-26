# Manifest

*tolstoy.life — a freely available reference work on the life and writings of Leo Tolstoy*

---

## What this is

Tolstoy.life is a reference work on Leo Nikolaevich Tolstoy (1828–1910) — his life, writings, manuscripts, and historical context. It is built as a public website and e-reader, freely accessible online and offline.

It is not a Wikipedia mirror. It is not a popular biography. It is an attempt to build the most complete and accurately sourced English-language resource on Tolstoy that has ever existed — and to make it available to anyone, without a paywall.

---

## Focus

The project centres on the final period of Tolstoy's life — the decades after his spiritual transformation in the late 1870s and 1880s, which he himself described as a rebirth. This is the period that produced his religious and philosophical writings, his social criticism, his later fiction, and his vast correspondence with people across the world who were grappling with the same questions he was.

This period is often treated as secondary to the great novels. This project does not share that view. It approaches Tolstoy's late work with the same seriousness and care as anything else he wrote — documenting it on its own terms, without editorial diminishment.

A particular priority is the English-language availability of these writings. The project aims to gather all existing English translations of the late period, identify what is missing, and — where possible — work toward filling those gaps.

A personal affinity with Tolstoy's late thinking is part of what drives the project.

---

## What it covers

The scope is the full factual record: names, places, dates, manuscripts, publications, correspondents, translations. The project approaches Tolstoy's critical and philosophical thinking with respect, while keeping its content factual and its descriptions of contested questions carefully sourced. Where religious and philosophical concepts require description — the various strands of Christianity, the Orthodox Church, movements such as anarchism or pacifism, groups such as the Doukhobors — they are treated neutrally and concisely, as context for understanding the people and events in the wiki rather than as subjects in their own right.

For Tolstoy's early and middle periods, the project follows established scholarship, which is broadly reliable and well-sourced. The late period — from roughly *Confession* (1879–82) onward — is where the academic record tends to be thinner, more selective, or less sympathetic to Tolstoy's own framing of his work. This is where the project applies the greatest care: documenting the writings of the late period completely, on their own terms, giving them the full weight they deserve.

Where sources disagree, both versions are recorded with their origins. Opinion is kept out as much as possible.

---

## How it is built

The knowledge base is maintained by [Claude](https://claude.ai) — Anthropic's AI — under the ongoing human review of [Johan Edlund](https://johanedlund.se), following the [**LLM Wiki model**](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Raw sources (TEI/XML, EPUBs, primary texts) are read in, key findings are extracted, and the results are integrated into a structured Obsidian vault that serves as the single source of truth for all metadata and prose content.

Every factual claim requires a named primary source. Uncertain information is flagged openly. Sources are weighed in a fixed order of authority: Jubilee Edition → Tolstoy's own diaries and letters → Birukoff biography → Chertkov correspondence → Maude biography.

The code is open. The content is free. Contributions are welcome via GitHub. Tolstoy's writings are in the public domain — a status he anticipated and welcomed. In his later years he sought to renounce copyright on his work; the clearest renunciations cover his religious-moral writings, but his stated position pointed further: he wanted his work to belong to no one. This project honours that conviction.

---

## What it is not

This project makes no claim to be exhaustive from day one. It grows incrementally, source-driven, with clear markers distinguishing what is verified from what is still a draft. A page with status `draft` is better than no page — but it is kept clearly separate from pages with status `reviewed` or `verified`.

It does not take positions on interpretive or theological questions. It does not position itself against any official or institutional account of Tolstoy. It simply tries to record what the sources say, as accurately as possible.

---

## Technical foundation

- **Vault:** Obsidian (`website/src/`) — wiki articles, work pages, source cards, and source texts in a single shared wikilink namespace.
- **Frontend:** Eleventy PWA, deployed on Netlify at tolstoy.life.
- **Schema:** Tolstoy Works Schema v5 (work metadata) + Wiki Schema (person, place, event, and concept pages).
- **Primary sources:** tolstoydigital TEI/XML (CC BY-SA), Project Gutenberg, British Library digitised editions, Yasnaya Polyana Museum open archive.

---

*Document created: April 2026.*
*Maintained by Johan Edlund with Claude (Anthropic).*
