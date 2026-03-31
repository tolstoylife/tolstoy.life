# Obsidian → Eleventy Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Set up `src/` as an Obsidian vault with `src/wiki/` and `src/works/` content directories that Eleventy discovers and builds into pages.

**Architecture:** `src/` is opened directly as the Obsidian vault. Content created in Obsidian (markdown with YAML frontmatter) is consumed by Eleventy via two new collections (`allWiki`, `allWorks`). Directory data files apply layouts automatically so individual notes need minimal frontmatter. Wikilink resolution is deferred.

**Tech Stack:** Eleventy 3.x, Obsidian, Nunjucks layouts, YAML frontmatter

---

## File map

| Action | File | Responsibility |
|--------|------|---------------|
| Create | `src/.obsidian/app.json` | Vault settings — default folder, attachments, wikilinks |
| Create | `src/.obsidian/workspace.json` | Minimal stub so vault opens cleanly |
| Create | `src/wiki/wiki.11tydata.json` | Sets `layout: wiki` + `tags: [wiki]` for all wiki notes |
| Create | `src/works/works.11tydata.json` | Sets `layout: work` + `tags: [work]` for all works |
| Create | `src/_layouts/wiki.njk` | Layout for wiki entries — type badge, content |
| Create | `src/_layouts/work.njk` | Layout for work pages — dual-language title, content |
| Create | `src/wiki/index.njk` | Wiki index listing all entries |
| Create | `src/works/index.njk` | Works index listing all works |
| Create | `src/wiki/leo-tolstoy.md` | Sample wiki note (seed content for verification) |
| Create | `src/works/anna-karenina.md` | Sample work page (seed content for verification) |
| Modify | `.eleventyignore` | Add `src/.obsidian/` |
| Modify | `src/_config/collections.js` | Add `getAllWiki` and `getAllWorks` |
| Modify | `eleventy.config.js` | Import + register new collections; add `wiki`/`work` layout aliases |
| Modify | `src/_data/navigation.js` | Add Works and Wiki to top nav |

---

### Task 1: Ignore the Obsidian vault config from Eleventy

**Files:**
- Modify: `.eleventyignore`

- [ ] **Step 1: Add `.obsidian/` to eleventyignore**

Open `.eleventyignore` (currently 3 lines) and append:

```
/src/posts/notes/_fleeting
/src/posts/notes/_sources
src/.obsidian/
```

- [ ] **Step 2: Verify build still passes**

```bash
cd /Users/johanedlund/Projects/tolstoy-life
npm run build 2>&1 | tail -3
```

Expected: `Wrote N files in ...` with no errors.

- [ ] **Step 3: Commit**

```bash
git add .eleventyignore
git commit -m "chore: ignore Obsidian vault config from Eleventy build"
```

---

### Task 2: Add wiki and works collections

**Files:**
- Modify: `src/_config/collections.js`
- Modify: `eleventy.config.js`

- [ ] **Step 1: Add collection functions to collections.js**

Append to the end of `src/_config/collections.js`:

```js
/** All wiki entries as a collection. */
export const getAllWiki = collection => {
  return collection.getFilteredByGlob('./src/wiki/**/*.md').reverse();
};

/** All works as a collection. */
export const getAllWorks = collection => {
  return collection.getFilteredByGlob('./src/works/**/*.md').reverse();
};
```

- [ ] **Step 2: Import and register in eleventy.config.js**

Find the import line at the top of `eleventy.config.js`:

```js
import { getAllPosts, getAllArticles, getAllNotes, getAllReading, getAllListening, showInSitemap, tagList } from './src/_config/collections.js';
```

Replace with:

```js
import { getAllPosts, getAllArticles, getAllNotes, getAllReading, getAllListening, showInSitemap, tagList, getAllWiki, getAllWorks } from './src/_config/collections.js';
```

- [ ] **Step 3: Register collections in eleventy.config.js**

Find the collections block (look for `eleventyConfig.addCollection('tagList', tagList);`) and add after it:

```js
  eleventyConfig.addCollection('allWiki', getAllWiki);
  eleventyConfig.addCollection('allWorks', getAllWorks);
```

- [ ] **Step 4: Add layout aliases in eleventy.config.js**

Find the layout aliases block (look for `eleventyConfig.addLayoutAlias('tags', 'tags.njk');`) and add after it:

```js
  eleventyConfig.addLayoutAlias('wiki', 'wiki.njk');
  eleventyConfig.addLayoutAlias('work', 'work.njk');
```

- [ ] **Step 5: Verify build passes**

```bash
npm run build 2>&1 | tail -3
```

Expected: no errors. (Collections are empty — that's fine.)

- [ ] **Step 6: Commit**

```bash
git add src/_config/collections.js eleventy.config.js
git commit -m "feat: add allWiki and allWorks Eleventy collections"
```

---

### Task 3: Create wiki and work layouts

**Files:**
- Create: `src/_layouts/wiki.njk`
- Create: `src/_layouts/work.njk`

- [ ] **Step 1: Create wiki.njk**

```bash
cat > /Users/johanedlund/Projects/tolstoy-life/src/_layouts/wiki.njk << 'EOF'
---
layout: base
---
<article class="region wrapper flow prose wiki-entry" data-type="{{ type }}">
  <header class="wiki-entry__header">
    <h1>{{ title }}</h1>
    {% if type %}<span class="wiki-entry__type">{{ type }}</span>{% endif %}
  </header>
  <div class="wiki-entry__content flow">
    {{ content | safe }}
  </div>
</article>
EOF
```

- [ ] **Step 2: Create work.njk**

```bash
cat > /Users/johanedlund/Projects/tolstoy-life/src/_layouts/work.njk << 'EOF'
---
layout: base
---
<article class="region wrapper flow prose work-entry">
  <header class="work-entry__header">
    <h1>{{ title }}</h1>
    {% if titleRu %}<p class="work-entry__title-ru" lang="ru">{{ titleRu }}</p>{% endif %}
  </header>
  <div class="work-entry__content flow">
    {{ content | safe }}
  </div>
</article>
EOF
```

- [ ] **Step 3: Commit**

```bash
git add src/_layouts/wiki.njk src/_layouts/work.njk
git commit -m "feat: add wiki and work layouts"
```

---

### Task 4: Create directory data files and content directories

**Files:**
- Create: `src/wiki/wiki.11tydata.json`
- Create: `src/works/works.11tydata.json`

- [ ] **Step 1: Create src/wiki/ with directory data**

```bash
mkdir -p /Users/johanedlund/Projects/tolstoy-life/src/wiki
cat > /Users/johanedlund/Projects/tolstoy-life/src/wiki/wiki.11tydata.json << 'EOF'
{
  "layout": "wiki",
  "tags": ["wiki"]
}
EOF
```

- [ ] **Step 2: Create src/works/ with directory data**

```bash
mkdir -p /Users/johanedlund/Projects/tolstoy-life/src/works
cat > /Users/johanedlund/Projects/tolstoy-life/src/works/works.11tydata.json << 'EOF'
{
  "layout": "work",
  "tags": ["work"]
}
EOF
```

- [ ] **Step 3: Commit**

```bash
git add src/wiki/wiki.11tydata.json src/works/works.11tydata.json
git commit -m "feat: add wiki and works content directories with directory data"
```

---

### Task 5: Create index pages for wiki and works

**Files:**
- Create: `src/wiki/index.njk`
- Create: `src/works/index.njk`

Note: these are `.njk` not `.md` so they do NOT inherit the `wiki`/`work` layout from the directory data file — they set their own layout explicitly.

- [ ] **Step 1: Create wiki index**

```bash
cat > /Users/johanedlund/Projects/tolstoy-life/src/wiki/index.njk << 'EOF'
---
layout: page
title: Wiki
description: 'Encyclopedic reference on people, places, events, and concepts related to Leo Tolstoy.'
permalink: /wiki/
---
<ul class="flow">
  {%- for entry in collections.allWiki -%}
    <li><a href="{{ entry.url }}">{{ entry.data.title }}</a>{% if entry.data.type %} <span class="wiki-entry__type">{{ entry.data.type }}</span>{% endif %}</li>
  {%- else -%}
    <li>No wiki entries yet.</li>
  {%- endfor -%}
</ul>
EOF
```

- [ ] **Step 2: Create works index**

```bash
cat > /Users/johanedlund/Projects/tolstoy-life/src/works/index.njk << 'EOF'
---
layout: page
title: Works
description: 'Complete bibliography of works by Leo Tolstoy.'
permalink: /works/
---
<ul class="flow">
  {%- for work in collections.allWorks -%}
    <li>
      <a href="{{ work.url }}">{{ work.data.title }}</a>
      {%- if work.data.titleRu %} — <span lang="ru">{{ work.data.titleRu }}</span>{% endif %}
    </li>
  {%- else -%}
    <li>No works yet.</li>
  {%- endfor -%}
</ul>
EOF
```

- [ ] **Step 3: Verify both pages build**

```bash
npm run build 2>&1 | grep -E "wiki|works|error|Error" | head -10
```

Expected: Lines like `Writing ./dist/wiki/index.html` and `Writing ./dist/works/index.html` with no errors.

- [ ] **Step 4: Commit**

```bash
git add src/wiki/index.njk src/works/index.njk
git commit -m "feat: add wiki and works index pages"
```

---

### Task 6: Add seed content for verification

**Files:**
- Create: `src/wiki/leo-tolstoy.md`
- Create: `src/works/anna-karenina.md`

These are the first real Obsidian-managed content files. They prove the pipeline end-to-end.

- [ ] **Step 1: Create sample wiki note**

```bash
cat > /Users/johanedlund/Projects/tolstoy-life/src/wiki/leo-tolstoy.md << 'EOF'
---
title: Leo Tolstoy
type: person
description: 'Russian novelist and moral philosopher (1828–1910).'
---

Leo Nikolayevich Tolstoy (Лев Николаевич Толстой; 9 September 1828 – 20 November 1910) was a Russian novelist, short story writer, playwright, and essayist.

He is regarded as one of the greatest authors of all time, best known for the novels *War and Peace* (1869) and *Anna Karenina* (1878).
EOF
```

- [ ] **Step 2: Create sample work page**

```bash
cat > /Users/johanedlund/Projects/tolstoy-life/src/works/anna-karenina.md << 'EOF'
---
title: Anna Karenina
titleRu: Анна Каренина
id: anna-karenina
genre: novel
description: 'Novel by Leo Tolstoy, first published in 1878.'
---

*Anna Karenina* is a novel by Leo Tolstoy, first published in book form in 1878. Widely considered one of the greatest novels ever written, it explores themes of love, jealousy, family, marriage, and society in nineteenth-century Russia.
EOF
```

- [ ] **Step 3: Build and verify pages render**

```bash
npm run build 2>&1 | grep -E "anna-karenina|leo-tolstoy|error|Error"
```

Expected output includes:
```
[11ty] Writing ./dist/wiki/leo-tolstoy/index.html from ./src/wiki/leo-tolstoy.md
[11ty] Writing ./dist/works/anna-karenina/index.html from ./src/works/anna-karenina.md
```

- [ ] **Step 4: Spot-check the built HTML**

```bash
grep -A5 '<h1>' /Users/johanedlund/Projects/tolstoy-life/dist/wiki/leo-tolstoy/index.html | head -10
grep -A5 '<h1>' /Users/johanedlund/Projects/tolstoy-life/dist/works/anna-karenina/index.html | head -10
```

Expected: `<h1>Leo Tolstoy</h1>` and `<h1>Anna Karenina</h1>` appear in respective files.

- [ ] **Step 5: Verify wiki type badge renders**

```bash
grep 'wiki-entry__type' /Users/johanedlund/Projects/tolstoy-life/dist/wiki/leo-tolstoy/index.html
```

Expected: `<span class="wiki-entry__type">person</span>`

- [ ] **Step 6: Verify Russian title renders in works**

```bash
grep 'lang="ru"' /Users/johanedlund/Projects/tolstoy-life/dist/works/anna-karenina/index.html
```

Expected: `<p class="work-entry__title-ru" lang="ru">Анна Каренина</p>`

- [ ] **Step 7: Commit**

```bash
git add src/wiki/leo-tolstoy.md src/works/anna-karenina.md
git commit -m "feat: add seed wiki note and work page for pipeline verification"
```

---

### Task 7: Initialise the Obsidian vault

**Files:**
- Create: `src/.obsidian/app.json`
- Create: `src/.obsidian/workspace.json`

- [ ] **Step 1: Create .obsidian directory and app.json**

```bash
mkdir -p /Users/johanedlund/Projects/tolstoy-life/src/.obsidian
cat > /Users/johanedlund/Projects/tolstoy-life/src/.obsidian/app.json << 'EOF'
{
  "newFileLocation": "folder",
  "newFileFolderPath": "wiki",
  "attachmentFolderPath": "assets/images/wiki",
  "useMarkdownLinks": false,
  "newLinkFormat": "shortest"
}
EOF
```

- [ ] **Step 2: Create workspace.json stub**

```bash
cat > /Users/johanedlund/Projects/tolstoy-life/src/.obsidian/workspace.json << 'EOF'
{
  "main": {
    "id": "main",
    "type": "split",
    "children": []
  },
  "left": { "id": "left", "type": "split", "children": [], "collapsed": false },
  "right": { "id": "right", "type": "split", "children": [], "collapsed": true }
}
EOF
```

- [ ] **Step 3: Verify .obsidian does NOT appear in dist/**

```bash
npm run build 2>&1 | grep -i obsidian
ls /Users/johanedlund/Projects/tolstoy-life/dist/.obsidian 2>/dev/null || echo "correctly absent"
```

Expected: no Eleventy output mentions `.obsidian`; `ls` prints `correctly absent`.

- [ ] **Step 4: Commit**

```bash
git add src/.obsidian/app.json src/.obsidian/workspace.json
git commit -m "feat: initialise Obsidian vault at src/ with wiki as default note folder"
```

---

### Task 8: Update navigation

**Files:**
- Modify: `src/_data/navigation.js`

- [ ] **Step 1: Add Works and Wiki to top nav**

Replace the entire contents of `src/_data/navigation.js` with:

```js
export default {
  top: [
    {
      text: 'Works',
      url: '/works/'
    },
    {
      text: 'Wiki',
      url: '/wiki/'
    },
    {
      text: 'About',
      url: '/about/'
    }
  ],
  bottom: [
    {
      text: 'Accessibility',
      url: '/accessibility/'
    }
  ]
};
```

- [ ] **Step 2: Build and verify nav links appear**

```bash
npm run build 2>&1 | tail -3
grep -o 'href="/works/"' /Users/johanedlund/Projects/tolstoy-life/dist/index.html
grep -o 'href="/wiki/"' /Users/johanedlund/Projects/tolstoy-life/dist/index.html
```

Expected: build succeeds; both `href="/works/"` and `href="/wiki/"` appear.

- [ ] **Step 3: Commit and push**

```bash
git add src/_data/navigation.js
git commit -m "feat: add Works and Wiki to site navigation"
git push origin main
```
