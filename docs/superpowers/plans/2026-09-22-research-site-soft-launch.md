---
title: research.tolstoy.life, Step 2 — the soft launch
date: 2026-09-22
---

# research.tolstoy.life, Step 2 — the soft launch: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Open the work to readers and listeners: a short landing page at tolstoy.life that points at the two finished editions, a research site that holds back the working papers and the images whose rights are unclear, and a *Send* button so a reader can post their notes back to the project.

**Architecture:** Everything on the research site is still decided by `docs/publish.py` — this plan adds three rules to it (hold back working papers, publish only images a dossier records as free, write the form the host needs) and reorders the front page for readers. The *Send* button is a few lines in `annotations.js` posting to Netlify's own form handling; no server of our own. The landing page is a separate small job in the splash project (`splash/tl`, Astro), which also loses the stale copy of the docs it has been serving since May.

**Tech Stack:** Python 3 (standard library, plus PyYAML which the docs build already uses), pytest, vanilla JavaScript, Astro 5 (splash only), Netlify CLI 26 and Netlify Forms.

**Spec:** [2026-09-22-research-site-design.md](../specs/2026-09-22-research-site-design.md), section "Step 2 — the soft launch". Read it first. Step 1's plan, for how the site is built and uploaded: [2026-09-22-research-site-ipad.md](./2026-09-22-research-site-ipad.md).

## Global Constraints

- **Johan publishes.** Never run `netlify deploy`, `git push` or `gh pr create`. Give Johan the exact command and wait. Committing is fine.
- **Two repositories.** The research site lives in this repository; the landing page lives in `splash/tl` (remote `pjedlund/tl`), which is its own git repository with its own commits and its own push.
- **No other changes.** Don't touch `primary-sources/**`, `website/src/_staging/**`, or the TEXT zone of any work text. `docs/` itself is never altered by the publishing rules — holding a file back or hiding an image happens in the uploaded copy only.
- **Plain language.** Comments are one short unwrapped line each. Prose in markdown is one line per paragraph, never hard-wrapped.
- **No new dependencies.** PyYAML is already installed and used by the docs build; nothing else is added, and no JavaScript libraries.
- **research.tolstoy.life stays unlisted** through this whole plan. The landing page at tolstoy.life is public and may be found by search engines; the research site keeps its "don't index" header. Lifting it is a separate decision — Task 8, Step 4 puts the question to Johan rather than assuming.
- **The address** is `research.tolstoy.life`, Netlify site name `tolstoy-research`. Upload commands always carry `--no-build`, or the Netlify tool tries to build the repository first.
- **Tests run with** `python3 -m pytest docs/tests -q` from the repository root.

---

### Task 0: Start from the right place

**Files:** none changed.

- [ ] **Step 1: Check the working tree.** Run `git status --short`. `docs/INDEX.html` changes on every build (its "Generated" timestamp), so it may show as modified; that's expected. Only ever `git add` named paths, never `git add -A`.
- [ ] **Step 2: Check where Step 1's work ended up.** Run `git log --oneline -1 main` and `git branch --contains e023c4b5 2>/dev/null`.
  - Step 1 finished on branch `research-site` (8 commits, ending with the front-page text `588d593f`). If Johan has merged it into `main`, branch from `main`; if not, branch from `research-site`:

```bash
git switch research-site
git switch -c research-soft-launch
```

- [ ] **Step 3: Record the test baseline.** Run `python3 -m pytest docs/tests -q`.
  - At plan time: `1 failed, 13 passed`, the failure being `test_overview_page_links_and_folder_index`, which still expects a "Read" button the 2026-08 nav rework removed. A separate session was started on 2026-09-22 to update it. If that fix has landed, expect `14 passed`. Either way, note the number here and don't let this plan change it.
- [ ] **Step 4: Confirm the live site is the one Step 1 left.** Run `curl -sI https://research.tolstoy.life/ | grep -iE '^HTTP|x-robots-tag'`. Expected: `HTTP/2 200` and `x-robots-tag: noindex`.

---

### Task 1: Hold back the working papers

**Files:**
- Modify: `docs/publish.py` (add `held_back()`, call it from `publishable()`)
- Test: `docs/tests/test_publish.py` (append)

**Interfaces:**
- Produces: `publish.held_back(rel: PurePosixPath) -> bool`, true for a path that stays off the site. `publishable()` filters with it.

The spec's list, and what it covers in this repository at plan time (121 files: 108 under `research/`, 13 under `superpowers/`):

| Rule | What it catches |
|---|---|
| `annotations.md` | Johan's reading annotations on a dive |
| anything under `superpowers/` | the AI planning documents, this plan among them |
| a name containing `_verifier-report` | the machine verifier's own output |
| a name starting `_sweep`, or containing `_visuals-sweep` / `_visuals_sweep` / `_witness_sweep` | corpus search logs |
| a name starting `session-log` or `handoff-` | session logs and handoffs inside the research folders |

- [ ] **Step 1: Write the failing test.** Append to `docs/tests/test_publish.py`:

```python
def test_held_back_covers_the_working_papers():
    import pathlib
    held = [
        "research/themes/crisis/annotations.md",
        "superpowers/plans/2026-09-22-research-site-soft-launch.md",
        "research/works/x/_verifier-report.md",
        "research/works/x/extracts/_sweep_diaries.md",
        "research/themes/y/visuals/_visuals-sweep.md",
        "research/themes/y/_witness_sweep.md",
        "research/_meta/z/session-log.md",
        "research/_meta/z/handoff-2026-05-28.md",
    ]
    kept = [
        "research/themes/crisis/index.md",
        "reader/non-fiction/personal-papers/confession/overview.md",
        "research/works/x/dossier.yaml",
        "editorial/editorial.md",
    ]
    for rel in held:
        assert publish.held_back(pathlib.PurePosixPath(rel)), rel
    for rel in kept:
        assert not publish.held_back(pathlib.PurePosixPath(rel)), rel
```

- [ ] **Step 2: Run it and watch it fail.** Run `python3 -m pytest docs/tests/test_publish.py -q -k held_back`. Expected: FAIL with `AttributeError: module 'publish' has no attribute 'held_back'`.

- [ ] **Step 3: Add the rule to `docs/publish.py`.** Put this next to the other constants:

```python
HELD_PREFIXES = ("_sweep", "session-log", "handoff-")  # search logs, session logs, handoffs
HELD_MARKERS = ("_verifier-report", "_visuals-sweep", "_visuals_sweep", "_witness_sweep")
```

and this function above `publishable()`:

```python
def held_back(rel: PurePosixPath) -> bool:
    """Working papers: on GitHub, not on the site — reading annotations, planning docs, verifier output, search logs, session logs."""
    name = rel.name
    return (name == "annotations.md" or rel.parts[0] == "superpowers"
            or name.startswith(HELD_PREFIXES) or any(m in name for m in HELD_MARKERS))
```

  Add `PurePosixPath` to the existing `from pathlib import Path` line so it reads `from pathlib import Path, PurePosixPath`.

- [ ] **Step 4: Call it from `publishable()`.** In the filter loop, change the condition to also require `not held_back(PurePosixPath(rel.as_posix()))`:

```python
        if (f.is_file() and f.suffix not in SKIP_SUFFIXES and not rel.name.startswith(".")
                and not SKIP_PARTS & set(rel.parts) and not held_back(PurePosixPath(rel.as_posix()))):
            keep.append(rel)
```

- [ ] **Step 5: Run the test and watch it pass.** Run `python3 -m pytest docs/tests/test_publish.py -q`. Expected: `2 passed`.

- [ ] **Step 6: Check it against the real repository.** Run:

```bash
python3 -c "import sys;sys.path.insert(0,'docs');import publish;p=publish.publishable();print(len(p));print([x.as_posix() for x in p if 'annotations' in x.name or x.parts[0]=='superpowers'])"
```

  Expected: a count around 2,180 (it was 2,314 before this rule) and an empty list.

- [ ] **Step 7: Commit.**

```bash
git add docs/publish.py docs/tests/test_publish.py
git commit -m "docs: hold the working papers back from the site"
```

---

### Task 2: A page for links that lead nowhere

**Files:**
- Create: `docs/404.md`
- Modify: `docs/publish.py` (docstring only — record that Netlify serves `404.html`)
- Test: `docs/tests/test_publish.py` (append)

Holding files back leaves 23 links on 18 published pages pointing at something that is no longer there (the front page's own 121 links disappear by themselves, because `publish.py` builds the published front page from published files only). Netlify serves `/404.html` for any address it can't find, and `serve.py` generates `404.html` from `404.md` like any other page.

- [ ] **Step 1: Write the failing test.** Append to `docs/tests/test_publish.py`:

```python
def test_site_carries_a_not_found_page():
    import pathlib
    docs = pathlib.Path(__file__).resolve().parents[1]
    assert (docs / "404.md").exists(), "404.md is the page Netlify serves for a link that leads nowhere"
    assert "404.html" in [p.as_posix() for p in publish.publishable()]
```

- [ ] **Step 2: Run it and watch it fail.** Run `python3 -m pytest docs/tests/test_publish.py -q -k not_found`. Expected: FAIL on the first assert.

- [ ] **Step 3: Write the page.** Create `docs/404.md` (one line per paragraph, no hard wrapping):

```markdown
---
title: This page isn't on the site
---

# This page isn't on the site

Some of the project's working papers stay off the public site: reading annotations, planning documents, the machine verifier's reports, corpus search logs, and session logs. They are all still in the [public repository](https://github.com/tolstoylife/tolstoy.life), where anyone can read them.

A link may also simply be old. Either way, the way back is the [front page](/INDEX.html), which lists everything the site does carry.
```

- [ ] **Step 4: Keep it off the front page's own listing.** It's a page for accidents, not something to browse to. In `docs/serve.py`, add it to the constant that already keeps `serve.py` itself out (at plan time line 57):

```python
SKIP_FILES = {"serve.py", "404.md"}
```

  ⚠ `collect_md_files()` uses `SKIP_FILES` for both the listing *and* the build, so after this `serve.py --build-only` no longer generates `404.html` from `404.md`. Generate it once by hand and commit it, and note in `docs/404.md`'s own text that it is built by hand:

```bash
python3 -c "import sys;sys.path.insert(0,'docs');import serve,pathlib;p=pathlib.Path('docs/404.md');pathlib.Path('docs/404.html').write_text(serve.md_to_html(p),encoding='utf-8')"
```

- [ ] **Step 5: Build and check.** Run `python3 docs/serve.py --build-only`, then `python3 -m pytest docs/tests/test_publish.py -q`. Expected: `3 passed`. Then `grep -c "404.html" docs/INDEX.html` — expected `0`, the page isn't listed.

- [ ] **Step 6: Commit.**

```bash
git add docs/404.md docs/404.html docs/serve.py docs/tests/test_publish.py docs/INDEX.html
git commit -m "docs: a plain page for links that lead nowhere"
```

---

### Task 3: Publish only the images whose rights are recorded

**Files:**
- Modify: `docs/publish.py` (add `cleared_images()` and `hide_withheld_images()`, use both in `main()`)
- Test: `docs/tests/test_publish.py` (append)

**Interfaces:**
- Produces: `publish.cleared_images(docs: Path) -> set[Path]` (absolute paths of images that may go on the site) and `publish.hide_withheld_images(html: str, page_dir: Path, cleared: set[Path]) -> str`.

**What's actually on disk at plan time** — the spec's estimate ("450 published, 74 withheld") was written before anyone counted, and the real picture differs:

- `docs/.gitignore` line 26 ignores `research/**/visuals/`, so **no dive image is published today at all**. This task starts publishing the free ones.
- 575 files sit under `research/**/visuals/`. Of those, 396 are listed in a dive's `dossier.yaml` with a public-domain or CC0 licence, 13 are listed with another licence (CC BY-SA, CC BY 4.0, unknown), and **166 are not listed in any dossier**, so nothing records their rights.
- 30 dossier entries name a file that isn't on disk. They need no handling: no file, nothing to copy.
- Separately, 47 images under `research/**/extracts/` **are** tracked by git and are already on the site — page scans from the Jubilee Edition. They stay, because they are already public in the repository; see the decision point below.

**Decision point for Johan, before this task is coded:** those 47 Jubilee Edition page scans are photographs of a 1928–64 edition. They are already public in the repository and already on the site, so this plan leaves them alone — but if Johan wants them treated like the dive images, that's a one-line change here and a separate sweep of the repository, which this plan does not do.

- [ ] **Step 1: Write the failing test.** Append to `docs/tests/test_publish.py`:

```python
def test_only_recorded_free_images_are_cleared(tmp_path):
    dive = tmp_path / "research" / "themes" / "d"
    (dive / "visuals").mkdir(parents=True)
    for name in ["free.jpg", "restricted.jpg", "unrecorded.jpg"]:
        (dive / "visuals" / name).write_bytes(b"x")
    (dive / "dossier.yaml").write_text(
        "visuals:\n"
        "  - id: V01\n    licence: PD\n    localPath: visuals/free.jpg\n"
        "  - id: V02\n    licence: CC-BY-SA\n    localPath: visuals/restricted.jpg\n")

    cleared = publish.cleared_images(tmp_path)

    assert (dive / "visuals" / "free.jpg").resolve() in cleared
    assert (dive / "visuals" / "restricted.jpg").resolve() not in cleared
    assert (dive / "visuals" / "unrecorded.jpg").resolve() not in cleared


def test_withheld_images_become_a_note(tmp_path):
    dive = tmp_path / "research" / "themes" / "d"
    (dive / "visuals").mkdir(parents=True)
    free = dive / "visuals" / "free.jpg"
    free.write_bytes(b"x")
    html = ('<figure><img src="visuals/free.jpg" alt="kept"><img src="visuals/restricted.jpg" alt="gone">'
            '<img src="https://example.org/remote.jpg" alt="remote"></figure>')

    out = publish.hide_withheld_images(html, dive, {free.resolve()})

    assert '<img src="visuals/free.jpg" alt="kept">' in out
    assert 'visuals/restricted.jpg' not in out
    assert "Image not shown — rights unclear" in out
    assert 'https://example.org/remote.jpg' in out
```

- [ ] **Step 2: Run them and watch them fail.** Run `python3 -m pytest docs/tests/test_publish.py -q -k image`. Expected: FAIL with `AttributeError: module 'publish' has no attribute 'cleared_images'`.

- [ ] **Step 3: Write the two functions** in `docs/publish.py`, above `main()`:

```python
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
FREE_LICENCES = ("PD", "CC0", "PUBLIC DOMAIN")
IMG_TAG = re.compile(r'<img\s[^>]*?src="([^"]+)"[^>]*>')
WITHHELD_NOTE = '<span class="img-withheld">Image not shown — rights unclear</span>'


def cleared_images(docs: Path = DOCS) -> set[Path]:
    """Dive images a dossier records as public domain or CC0. Everything else stays home, including images no dossier lists."""
    cleared = set()
    for dossier in docs.glob("research/**/dossier.yaml"):
        try:
            data = yaml.safe_load(dossier.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:  # a malformed dossier withholds its images rather than breaking the build
            print(f"  ! {dossier.relative_to(docs)}: {exc}", file=sys.stderr)
            continue
        for v in data.get("visuals") or []:
            if not isinstance(v, dict) or not v.get("localPath"):
                continue
            licence = str(v.get("licence") or v.get("license") or "").strip().upper()
            if licence.startswith("PD") or licence in FREE_LICENCES or "PUBLIC DOMAIN" in licence:
                cleared.add((dossier.parent / str(v["localPath"])).resolve())
    return cleared


def hide_withheld_images(html: str, page_dir: Path, cleared: set[Path]) -> str:
    """In the uploaded copy only: an image that isn't cleared becomes a short note in its place."""
    def replace(m):
        src = m.group(1)
        if src.startswith(("http:", "https:", "data:", "//")):
            return m.group(0)
        target = (page_dir / unquote(src.split("?")[0])).resolve()
        if target.suffix.lower() not in IMAGE_SUFFIXES or target in cleared:
            return m.group(0)
        return WITHHELD_NOTE
    return IMG_TAG.sub(replace, html)
```

  Add the imports this needs at the top of the file: `import re`, `import sys` (already there), `from urllib.parse import unquote`, and `import yaml`.

- [ ] **Step 4: Run the tests and watch them pass.** Run `python3 -m pytest docs/tests/test_publish.py -q -k image`. Expected: `2 passed`.

- [ ] **Step 5: Publish the cleared images and rewrite the pages.** In `publishable()`, after the reader-audio line, add the images (they are gitignored, like the audio, and ours to publish):

```python
    files |= cleared_images(docs)  # dive images a dossier records as free; the rest stay home
```

  And in `main()`, replace the plain copy with one that rewrites HTML on the way out. Keep tracked images cleared too, so nothing that is already public in the repository disappears:

```python
    cleared = cleared_images() | {DOCS / rel for rel in pub if rel.suffix.lower() in IMAGE_SUFFIXES}
    for rel in pub:
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if rel.suffix == ".html":
            dest.write_text(hide_withheld_images((DOCS / rel).read_text(encoding="utf-8"), (DOCS / rel).parent, cleared), encoding="utf-8")
        else:
            shutil.copy2(DOCS / rel, dest)
        total += dest.stat().st_size
```

- [ ] **Step 6: Give the note a style.** In `docs/reader/assets/shell.css`, next to the other figure styles, add one rule:

```css
.img-withheld { display: block; padding: 1rem; border: 1px dashed var(--rule-soft); color: var(--ink-faint); font-size: .85rem; text-align: center; }
```

- [ ] **Step 7: Build and count.** Run `python3 docs/publish.py`, then:

```bash
find _site -path '*/visuals/*' -type f | wc -l
grep -rl "img-withheld" _site --include='*.html' | wc -l
```

  Expected: about 396 images published, and roughly 30–60 pages carrying at least one note. If the image count is 0, `cleared_images()` isn't finding the dossiers; if it's 575, the licence test is letting everything through.

- [ ] **Step 8: Look at one page.** Open `_site/research/_meta/tolstoy-in-photographs/index.html` in the in-app browser (serve `_site` with `python3 -m http.server 7888 --directory _site` from Bash, then `preview_start` at `http://localhost:7888/research/_meta/tolstoy-in-photographs/index.html`). That page's images are the unrecorded ones, so it should show the notes rather than pictures, and still read sensibly. Stop the server afterwards.

- [ ] **Step 9: Commit.**

```bash
git add docs/publish.py docs/tests/test_publish.py docs/reader/assets/shell.css
git commit -m "docs: publish the dive images a dossier records as free, and name the rest as withheld"
```

---

### Task 4: A front page that leads with reading

**Files:**
- Modify: `docs/serve.py`, `build_index()`'s body template (at plan time lines 1095–1105) and the nav-card builder (lines 964–980)
- Test: `docs/tests/test_render.py` (append)

Today the page opens with the corpus timeline, then "Browse", then dated notes, then reference documents. For a reader arriving from the landing page, the first thing should be what there is to read and listen to.

The spec also asks for the stale "mirrored to tolstoy.life/notes/" line to go. That was done on 2026-09-22 in commit `588d593f`, which replaced the whole opening paragraph; nothing to do here.

- [ ] **Step 1: Write the failing test.** Append to `docs/tests/test_render.py`:

```python
def test_front_page_leads_with_reading():
    html = serve.build_index(serve.merge_doc_files(serve.collect_md_files(), serve.collect_orphan_html_files()))
    read_at = html.index("Read and listen")
    assert read_at < html.index("viz-frame"), "the reading section comes before the timeline chart"
    assert read_at < html.index('<h2>Notes</h2>'), "the reading section comes before the dated notes"
    assert "/reader/non-fiction/personal-papers/confession/" in html
```

- [ ] **Step 2: Run it and watch it fail.** Run `python3 -m pytest docs/tests/test_render.py -q -k leads_with_reading`. Expected: FAIL with `ValueError: substring not found`.

- [ ] **Step 3: Add the reading section** to `build_index()`'s template, directly after `</header>` and *before* `{viz_html}`:

```html
<section class="reading">
  <h2>Read and listen</h2>
  <div class="nav-grid">
    <a class="nav-card" href="/reader/non-fiction/personal-papers/confession/">
      <div class="nc-title">A Confession</div>
      <div class="nc-meta">1879–82 · Russian, Wiener's 1904 English, project English · read-along audio</div>
    </a>
    <a class="nav-card" href="/reader/non-fiction/essays-and-criticism/the-great-sin/">
      <div class="nc-title">A Great Iniquity</div>
      <div class="nc-meta">1905 · Russian, the 1905 English, project English · read-along audio</div>
    </a>
    <a class="nav-card" href="/reader/index.html">
      <div class="nc-title">The whole library</div>
      <div class="nc-meta">every work, with what exists for each</div>
    </a>
  </div>
</section>
```

- [ ] **Step 4: Move the dated notes below the reference documents.** In the same template, swap the two blocks so the order reads: reading section, `{viz_html}`, Browse, `{ref_html}`, then the Notes section:

```html
{viz_html}
<section>
  <h2>Browse</h2>
  <div class="nav-grid">{nav_cards}
  </div>
</section>
{ref_html}
<section>
  <h2>Notes</h2>
  {blog_html}
</section>
```

- [ ] **Step 5: Run the tests.** Run `python3 -m pytest docs/tests -q`. Expected: the Task 0 baseline plus one more pass.

- [ ] **Step 6: Look at it.** Rebuild with `python3 docs/serve.py --build-only`, restart the local server (`lsof -ti tcp:7877 | xargs -r kill`, then `python3 docs/serve.py --port 7877` from Bash in the background — ⚠ a running server keeps serving the old code), and open `http://localhost:7877/INDEX.html` in the in-app browser. The three reading cards should be the first thing under the opening paragraphs.

- [ ] **Step 7: Commit.**

```bash
git add docs/serve.py docs/tests/test_render.py docs/INDEX.html
git commit -m "docs: the front page leads with what there is to read and listen to"
```

---

### Task 5: "Send" in the Notes panel

**Files:**
- Modify: `docs/serve.py`, the `NOTES_PANEL` constant (at plan time lines 106–118)
- Modify: `docs/reader/assets/annotations.js`, next to the existing `notes-export` handler (around line 327)
- Modify: `docs/reader/assets/shell.css` (one rule for the email row)
- Modify: `docs/publish.py` (`main()` writes the form page Netlify registers)
- Test: no JavaScript test setup in this project; the check is Step 7 in the in-app browser and Task 8 on the live site.

**Interfaces:**
- Consumes: `exportText()` and `exportCollection()`, both already in `annotations.js`.
- Netlify registers a form by finding it in the uploaded HTML, so `publish.py` writes `_site/__forms.html` with the form's shape. The button posts to the reader's own page address with `form-name=reader-notes`. If Task 8's live check shows nothing arriving, try `/__forms.html` as the address instead — the form name is what matters to the host, not the path.

- [ ] **Step 1: Add the button and the email row** to `NOTES_PANEL` in `docs/serve.py`, inside `<div class="notes-actions">` and after the `notes-import` button:

```html
    <button id="notes-send">Send to the project</button>
```

  and directly after the `</div>` that closes `notes-actions`:

```html
  <div id="notes-send-row" hidden>
    <input type="email" id="notes-email" placeholder="Your email, if you'd like a reply" autocomplete="email">
    <p class="notes-send-note">Sends the notes on this page and its address. Nothing else is collected, and the email is optional.</p>
    <button class="primary" id="notes-send-go">Send</button>
  </div>
```

- [ ] **Step 2: Style the row.** In `docs/reader/assets/shell.css`, next to the `.notes-actions` rules:

```css
#notes-send-row { margin-top: .6rem; display: grid; gap: .4rem; }
#notes-send-row input { width: 100%; font: inherit; padding: .4rem; }
.notes-send-note { color: var(--ink-faint); font-size: .8rem; margin: 0; }
```

- [ ] **Step 3: Wire it up** in `docs/reader/assets/annotations.js`, after the `bindClick('notes-import', …)` block:

```js
  // ⚠ The Send button only exists on the published site — Netlify handles the form, and a local server would 404.
  const sendRow = document.getElementById('notes-send-row');
  const sendBtn = document.getElementById('notes-send');
  if (sendBtn && !location.hostname.endsWith('tolstoy.life')) sendBtn.hidden = true;
  bindClick('notes-send', () => { sendRow.hidden = !sendRow.hidden; });
  bindClick('notes-send-go', btn => {
    const anns = loadDoc();
    if (!anns.length) { alert('There are no notes on this page yet.'); return; }
    const body = new URLSearchParams({
      'form-name': 'reader-notes',
      page: location.pathname,
      email: document.getElementById('notes-email').value,
      text: exportText(),
      jsonld: JSON.stringify(exportCollection()),
      'bot-field': '',
    });
    btn.disabled = true;
    // ⚠ Posts to the page's own address, not "/" — the site rewrites "/" to INDEX.html, which can swallow the submission.
    fetch(location.pathname, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body })
      .then(r => { btn.textContent = r.ok ? 'Sent, thank you' : 'Sending failed — try again later'; })
      .catch(() => { btn.textContent = 'Sending failed — try again later'; })
      .finally(() => { setTimeout(() => { btn.disabled = false; btn.textContent = 'Send'; sendRow.hidden = true; }, 4000); });
  });
```

  The notes stay in the reader's browser: nothing here clears them.

- [ ] **Step 4: Write the form page** in `docs/publish.py`. Add the constant next to `HEADERS`:

```python
# Netlify registers a form by finding it in the uploaded site; the reader posts to it from JavaScript.
FORM_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Form registration</title><meta name="robots" content="noindex"></head>
<body>
<form name="reader-notes" data-netlify="true" netlify-honeypot="bot-field" hidden>
  <input type="text" name="page">
  <input type="email" name="email">
  <input type="text" name="bot-field">
  <textarea name="text"></textarea>
  <textarea name="jsonld"></textarea>
</form>
</body></html>
"""
```

  and write it in `main()`, beside the `_headers` and `_redirects` lines:

```python
    (OUT / "__forms.html").write_text(FORM_PAGE)
```

- [ ] **Step 5: Run the tests.** Run `python3 -m pytest docs/tests -q`. Expected: unchanged from Task 4.

- [ ] **Step 6: Build.** Run `python3 docs/publish.py`, then `ls _site/__forms.html` and `grep -c reader-notes _site/__forms.html`. Expected: the file exists and the name appears.

- [ ] **Step 7: Check the local behaviour in the in-app browser.** With the local server running (Task 4, Step 6), open a reader page and run with `javascript_tool`:

```js
document.getElementById('notes-panel') && ({ hidden: document.getElementById('notes-send').hidden, host: location.hostname })
```

  Expected: `hidden: true` on `localhost` — the button must not offer to send from Johan's own machine. The live check is Task 8.

- [ ] **Step 8: Commit.**

```bash
git add docs/serve.py docs/reader/assets/annotations.js docs/reader/assets/shell.css docs/publish.py
git commit -m "reader: a Send button that posts a reader's notes to the project"
```

---

### Task 6: The landing page at tolstoy.life

**Files (all in `splash/tl`, a separate git repository):**
- Modify: `src/components/Splash.astro`
- Create: `public/_redirects`
- Delete: `src/pages/docs/`, `src/content/docs/`, `src/content.config.ts`, `src/layouts/DocsLayout.astro`, `src/data/docs-index.html`, `public/docs/`, `scripts/sync-docs.sh`, `scripts/strip-frontmatter.py`, and the `sync-docs` line in `package.json`

The splash is one dark page (`#121738`) with the T and a single sentence. It keeps that look; the new words sit under the existing heading. The Umami counter in `src/layouts/Layout.astro` stays as it is — it sets no cookies, so no consent banner is needed.

- [ ] **Step 1: Draft the words.** Johan edits these before they ship; put them in front of him as part of this task rather than after:

```
The life and works of Leo Tolstoy. Coming 2028.

Open research, in the open, while it is being made.

Read and listen now
  A Confession (1879–82) — Tolstoy's account of his own crisis, in Leo Wiener's 1904 English, with read-along audio.
  A Great Iniquity (1905) — on land and property, in the English of its own year, with read-along audio.

Follow the research
  Every source dive, dossier and working note behind the editions.

Help
  Read or listen. When something is wrong or unclear, select it, write a note, and press Send. It reaches us with the passage attached.

Everything here is free to use: Tolstoy renounced the copyright to his work, and this project dedicates its own to the public domain.
```

- [ ] **Step 2: Put them on the page.** In `src/components/Splash.astro`, after the `<h1>` inside `#hero`, add the sections and links (addresses exactly as below — they are the overview pages, not the reader pages):

```html
			<p class="lede">Open research, in the open, while it is being made.</p>
			<section class="block">
				<h2>Read and listen now</h2>
				<p><a href="https://research.tolstoy.life/reader/non-fiction/personal-papers/confession/">A Confession</a> (1879–82) — Tolstoy's account of his own crisis, in Leo Wiener's 1904 English, with read-along audio.</p>
				<p><a href="https://research.tolstoy.life/reader/non-fiction/essays-and-criticism/the-great-sin/">A Great Iniquity</a> (1905) — on land and property, in the English of its own year, with read-along audio.</p>
			</section>
			<section class="block">
				<h2>Follow the research</h2>
				<p><a href="https://research.tolstoy.life/research/index.html">Every source dive, dossier and working note</a> behind the editions.</p>
			</section>
			<section class="block">
				<h2>Help</h2>
				<p>Read or listen. When something is wrong or unclear, select it, write a note, and press <em>Send</em>. It reaches us with the passage attached.</p>
			</section>
			<p class="foot">Everything here is free to use: Tolstoy renounced the copyright to his work, and this project dedicates its own to the <a href="https://github.com/tolstoylife/tolstoy.life/blob/main/LICENSE">public domain</a>.</p>
```

  and the matching styles inside the existing `<style>` block, keeping the splash's own scale:

```css
	#hero { max-width: 34rem; text-align: left; }
	.lede { color: #c9cbe0; margin-top: .4rem; }
	.block { margin-top: 1.6rem; }
	.block h2 { font-size: 15px; letter-spacing: .04em; text-transform: uppercase; color: #8d92b5; margin-bottom: .3rem; }
	.block p { margin: .25rem 0; color: #e7e8f2; font-size: 15px; line-height: 1.5; }
	a { color: #f0d9a8; }
	.foot { margin-top: 2rem; color: #8d92b5; font-size: 13px; }
```

- [ ] **Step 3: Forward the old docs addresses.** Create `public/_redirects` (Astro copies `public/` into the built site):

```
/docs/*  https://research.tolstoy.life/:splat.html  301
```

- [ ] **Step 4: Remove the stale docs copy.** From `splash/tl`:

```bash
git rm -r -q src/pages/docs src/content/docs src/layouts/DocsLayout.astro src/data/docs-index.html public/docs src/content.config.ts scripts/sync-docs.sh scripts/strip-frontmatter.py
```

  Then take the `"sync-docs": "bash scripts/sync-docs.sh"` line out of `package.json`'s `scripts`, leaving the JSON valid.

- [ ] **Step 5: Build it.** From `splash/tl`, run `npm run build`. Expected: it finishes with no error and no mention of a missing `docs` collection. If Astro complains about `content.config.ts` being gone, check that nothing else imports `astro:content`: `grep -rn "astro:content" src`.

- [ ] **Step 6: Look at it.** Run the dev server via the Browser pane rather than Bash: add a `splash` entry to `.claude/launch.json` with `runtimeExecutable` `npm`, `runtimeArgs` `["run","dev","--prefix","splash/tl"]` and port `4321`, then `preview_start` with name `splash`. Check at phone width too (`resize_window` preset `mobile`): the T, the heading, then the three blocks, all readable, links visible against the dark background. Reset the viewport to `desktop` afterwards.

- [ ] **Step 7: Commit in the splash repository.**

```bash
cd splash/tl
git add -A
git commit -m "landing page: read and listen now, follow the research, help — and retire the stale docs copy"
cd -
```

- [ ] **Step 8: Hand Johan the push.** He publishes the landing page himself:

```bash
cd /Volumes/Graugear/Tolstoy/splash/tl && git push
```

  Wait for him to confirm it's live before Task 8's checks. ⚠ This publishes tolstoy.life, which is public and indexed — the landing page will name research.tolstoy.life in public for the first time.

---

### Task 7: Build and check the site before it's uploaded

**Files:** none changed.

- [ ] **Step 1: Build.** Run `python3 docs/publish.py`. Expected: it ends with a size around 400 MB — larger than Step 1's 334 MB, because roughly 396 dive images are now included.

- [ ] **Step 2: Check what landed.** From the repository root, each line on its own:

```bash
find _site -name 'annotations.html' -o -name 'annotations.md' | wc -l
find _site/superpowers -type f 2>/dev/null | wc -l
find _site -name '_sweep*' -o -name '*_verifier-report*' -o -name 'session-log.*' -o -name 'handoff-*' | wc -l
find _site -path '*/visuals/*' -type f | wc -l
ls _site/404.html _site/__forms.html _site/_headers _site/_redirects
```

  Expected: the first three are 0, the image count is about 396, and all four files exist.

- [ ] **Step 3: Check no link points at something held back.** Run:

```bash
cd _site && python3 - <<'PY'
import re, pathlib, urllib.parse, collections
missing = collections.Counter()
for p in pathlib.Path(".").rglob("*.html"):
    for u in re.findall(r'(?:href|src)="([^"#?]+)', p.read_text(errors="ignore")):
        if u.startswith(("http", "mailto:", "data:", "javascript:", "blob:")) or "{" in u: continue
        t = pathlib.Path(urllib.parse.unquote(u.lstrip("/") if u.startswith("/") else str(p.parent / u)))
        if not (t.is_file() or (t / "index.html").is_file()): missing[str(t)] += 1
print(sum(missing.values()), "links to something absent")
for k, v in missing.most_common(10): print(" ", v, k)
PY
cd -
```

  Expected: the count is well down from Step 1's ~320 (the dive images are now published, so those stop appearing), and what remains are held-back working papers — which is the point of Task 2's page. ⚠ If a *reader* page appears in that list, stop and fix it before uploading.

- [ ] **Step 4: Hand Johan the draft upload.** He runs it; wait for the address:

```bash
netlify deploy --no-build --dir _site --site tolstoy-research
```

---

### Task 8: Go live (Johan publishes and sets the switches)

**Files:** none changed until Step 6.

- [ ] **Step 1: Johan turns on form handling.** In Netlify's web interface, on the `tolstoy-research` site: Forms → enable form detection, and add an email notification to Johan's address for the `reader-notes` form. Netlify only registers a form on a deploy made *after* detection is on, so this comes before the live upload.

- [ ] **Step 2: Check the draft address** (`$D` = the address from Task 7):

```bash
curl -sI "$D/" | grep -iE '^HTTP|x-robots-tag'
curl -s -o /dev/null -w '%{http_code} 404 page\n' "$D/research/themes/crisis/annotations.html"
curl -s "$D/404.html" | grep -c "isn't on the site"
curl -s -o /dev/null -w '%{http_code} a published image\n' "$D/research/works/fiction/novellas/1884-1886-the-death-of-ivan-ilyich/visuals/commons-leo-tolstoi-1887.jpg"
```

  Expected: `200` and `noindex` for the front page; `404` for the held-back page; `1` for the 404 page's text; `200` for the image.

- [ ] **Step 3: Johan uploads to the live address.**

```bash
netlify deploy --no-build --prod --dir _site --site tolstoy-research
```

- [ ] **Step 4: Ask Johan the one open question.** Run `rg '@until' docs` and show him the list — at plan time it is the `noindex` switch in `publish.py`. The spec keeps research.tolstoy.life unlisted through the soft launch, so the default is to leave it. Ask plainly whether he now wants search engines to find the research site, and do nothing unless he says yes. If he says yes: delete the `X-Robots-Tag` line from `HEADERS` in `publish.py` along with its `@until` comment, rebuild, commit, and he uploads again.

- [ ] **Step 5: Check the whole path as a reader would.** With Johan:
  - tolstoy.life shows the landing page, and its two reading links open the overview pages.
  - `https://tolstoy.life/docs/architecture/architecture-review` forwards to research.tolstoy.life.
  - On a reader page: select a sentence, write a note, Notes → **Send to the project**. It should say "Sent, thank you", and the submission should appear in Netlify's Forms panel with the page address, the readable notes and the JSON. Johan pastes that JSON into Notes → "Import…" on his local copy and sees the note land in the right place.
  - A page with withheld images shows the plain note instead of a broken image.

- [ ] **Step 6: Record it.** Add one paragraph to `TODO.md` under the reader-editions items, saying: the soft launch is live; what the site now holds back (working papers, images without recorded rights) and where that rule lives (`docs/publish.py`); that the landing page is in the splash repository and publishes on Johan's push; how a reader's notes arrive (Netlify Forms → email → "Import…"); and whether the research site is still unlisted after Step 4. Then:

```bash
git add TODO.md
git commit -m "TODO: the soft launch is live"
```

- [ ] **Step 7: Update the memory.** In `project_research_site.md`, replace the "Step 1 is LIVE" paragraph with the soft-launch state: both addresses, what is held back, where the *Send* notes arrive, and whether `noindex` is still on. Keep the one-line entry in `MEMORY.md` in step.

- [ ] **Step 8: Tell Johan the branch is ready.** He pushes and merges it himself (the `branch-sweep` skill can help when he asks). Remember there are two repositories to push: this one and `splash/tl`.

---

## What this plan deliberately leaves out

- **The organisation page on GitHub** already describes the project and now mentions the reader's editions; adding a research.tolstoy.life link there is a one-line change Johan can make whenever he likes, and it belongs with the launch rather than in the build.
- **The 150-odd links inside `docs/` that were already broken** before any of this. They have their own task.
- **Johan's Apple Books highlights** of A Confession (Maude's translation, so they can only be placed paragraph by paragraph). Separate, and waiting on his call.
- **Making `annotations.md` truly private**, which would mean removing it from the repository and its history. The spec records this as not decided.
