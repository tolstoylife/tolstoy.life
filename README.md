# tolstoy.life

**A freely available reference work on the life and writings of Leo Tolstoy.**

→ [tolstoy.life](https://tolstoy.life)

---

Leo Nikolaevich Tolstoy (1828–1910) wrote some of the most widely read novels in human history — and then, in the last three decades of his life, turned away from them. He underwent a profound spiritual transformation, renounced the copyright to all his writings, and produced an enormous body of religious, philosophical, and social work that has never received the same attention as *War and Peace* or *Anna Karenina*.

This project exists to change that.

**tolstoy.life** is an attempt to build the most complete and accurately sourced English-language resource on Tolstoy that has ever existed — and to make it available to everyone, without a paywall, online and offline.

---

## What it covers

The project covers the full factual record: dates, places, manuscripts, publications, correspondents, translations, and historical context. It includes the major novels, but its particular focus is the late period — from *Confession* (1879–82) onward — where the scholarly record tends to be thinner and where English-language access to Tolstoy's own writings is most uneven.

Where sources disagree, both versions are recorded with their origins. Uncertain information is flagged openly. Opinion is kept out as much as possible.

---

## How it is built

The knowledge base is maintained by [Claude](https://claude.ai) (Anthropic's AI) under the ongoing human review of [Johan Edlund](https://johanedlund.se), following the [LLM Wiki model](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Raw sources — TEI/XML archives, EPUBs, primary texts — are read and processed. Key findings are extracted and integrated into a structured [Obsidian](https://obsidian.md) vault that serves as the single source of truth for all metadata and prose. The vault compiles into a PWA (progressive web app) via [Eleventy](https://www.11ty.dev/), deployed on [Netlify](https://netlify.com).

Every factual claim requires a named primary source. Sources are weighed in a fixed order of authority:

1. Jubilee Edition (*Полное собрание сочинений*, 90 vols., 1928–1964)
2. Tolstoy's own diaries and letters
3. Birukoff biography
4. Chertkov correspondence
5. Maude biography

---

## Repositories

| Repo | Description |
|------|-------------|
| [`tolstoy.life`](https://github.com/tolstoylife/tolstoy.life) | Parent repo — shared schema, CLAUDE.md, and project documentation |
| [`website`](https://github.com/tolstoylife/website) | Eleventy PWA, Obsidian vault, e-reader frontend |
| [`splash`](https://github.com/tolstoylife/splash) | Temporary splash site (pre-launch placeholder) |
| [`tools`](https://github.com/tolstoylife/tools) | Utilities and helper scripts |

---

## Project status

The project is in active development. Pages carry an explicit status marker — `draft`, `reviewed`, or `verified` — so it is always clear what has been checked against primary sources and what has not. A draft page is better than no page; but the distinction is kept visible.

---

## Contributing

All of Tolstoy's writings are in the public domain — a status he anticipated and welcomed. From 1891 onward he renounced the copyright to his works, insisting that knowledge and art belong to everyone. This project honours that conviction.

The code is open. The content is free.

Contributions are welcome via **GitHub Issues**. There are templates for:

- **Factual corrections** — cite your source and describe what is wrong
- **Prose suggestions** — wording, clarity, missing context
- **Missing works or sources** — point to something that should be here

For contributors comfortable with git, pull requests are welcome. Any PR touching wiki prose or work metadata must cite the specific primary source for every claim. A maintainer reviews the diff before merging.

---

## Primary sources used

- [tolstoydigital TEI/XML](https://github.com/tolstoydigital/TEI) (CC BY-SA) — 3,113 persons, 770 locations, 767 works
- [Standard Ebooks](https://standardebooks.org/ebooks/leo-tolstoy) — free, carefully formatted Tolstoy editions; toolchain at [standardebooks/tools](https://github.com/standardebooks/tools)
- [Project Gutenberg](https://www.gutenberg.org/) — English translations
- British Library digitised editions
- Yasnaya Polyana Museum open archive

---

*Maintained by [Johan Edlund](https://johanedlund.se) with Claude (Anthropic). April 2026.*
