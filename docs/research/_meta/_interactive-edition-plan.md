# Interactive Reader's Editions — Spec 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make a finished corpus-dive renderable as an interactive reader's edition in the local `serve.py` preview, and prove it end-to-end on one chapter of The Great Sin (overview + all three versions, with real cut/softening/wikilink marks, toggleable over a clean default).

**Architecture:** Two phases. Phase 1 is the rendering engine — `serve.py` gains CriticMarkup, footnotes, and wikilinks rendering, a clean-by-default reader template, and a toggle rail (test-first Python). Phase 2 is a vertical slice of content — the overview distilled from `index.md`, plus chapter I of The Great Sin in Russian (the canonical spine), 1905 English, and machine English, marked up from the dossier and aligned on shared section anchors (verification-gated, human-present). Remaining chapters and the cross-dive generator are explicit follow-ups, not in this plan.

**Tech Stack:** Python 3, Python-Markdown (`markdown`) + `pymdown-extensions` (CriticMarkup), the existing `docs/serve.py`, `docs/research/lib/verify_quotes.py`.

## Global Constraints

- **Spine = the Russian PSS established text** (canonical); the 1905 English and machine English are *derived versions* measured against it. Copied from spec verbatim: "The spine is the Russian PSS established text — always."
- **Default reading state is bare** — the marks live in the file, but the default view shows none of them. Wikilinks, footnotes, cut-reveals, version-switch are all opt-in.
- **Tolstoy's voice, not the mainstream filter** — present what he wrote in his terms; neither soften with mainstream labels nor sharpen past what he said.
- **`primary-sources/**` and the dive's `extracts/**` are untouched.** The reader text is a derived edition; the Russian version's prose, with marks stripped, must match the source extract exactly.
- **One file per version**, sharing the same `{#sec-N}` heading anchors (the spine's chapter structure sets them).
- **Editorial notes inline** in `{>>…<<}` for now.
- **Commit, do not push.** Johan pushes himself. Plain language in anything Johan reads.

> **TDD adaptation.** Phase 1 (Python) follows test-first. Phase 2 is research/content production — it has no unit tests; each task ends with an explicit verification gate (mark-stripped fidelity diff, `verify_quotes`, render-and-inspect) instead. Phase 2 is human-present work in the dive discipline, not unattended subagent output.

---

## Phase 1 — the rendering engine

### Task 1: CriticMarkup + footnotes + wikilinks in `serve.py`

**Files:**
- Modify: `docs/serve.py:35` (add a `require`), `docs/serve.py:485-492` (the `MD` extension list), `docs/serve.py:536-537` (extract a render seam)
- Test: `docs/tests/test_render.py` (create)

**Interfaces:**
- Produces: `serve.render_body(text: str) -> str` — converts a Markdown string (incl. CriticMarkup, footnotes, `[[wikilinks]]`) to an HTML fragment. Consumed by `md_to_html` and by Task 2.

- [ ] **Step 1: Write the failing tests**

```python
# docs/tests/test_render.py
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # docs/
import serve

def test_critic_deletion_renders_del():
    html = serve.render_body("a {--cut here--} b")
    assert "<del" in html and "cut here" in html

def test_critic_substitution_renders_old_and_new():
    html = serve.render_body("x {~~springs from~>is connected with~~} y")
    assert "springs from" in html and "is connected with" in html

def test_critic_comment_renders_note():
    html = serve.render_body("x {>>Chertkov softened this<<} y")
    assert "Chertkov softened this" in html

def test_footnote_renders():
    html = serve.render_body("Body text[^1]\n\n[^1]: the footnote")
    assert "the footnote" in html and ("footnote" in html)

def test_wikilink_renders_link():
    html = serve.render_body("the single tax that [[Henry George]] proposed")
    assert "Henry George" in html and "wikilink" in html
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd docs && python3 -m pytest tests/test_render.py -v`
Expected: FAIL — `AttributeError: module 'serve' has no attribute 'render_body'`

- [ ] **Step 3: Add the dependency and extensions, extract the seam**

After `docs/serve.py:35` (`require("markdown")`), add:

```python
require("pymdownx", "pymdown-extensions")
```

Replace the `MD = markdown.Markdown(...)` block at `docs/serve.py:485-492` with:

```python
from markdown.extensions.wikilinks import WikiLinkExtension

MD = markdown.Markdown(extensions=[
    TableExtension(),
    FencedCodeExtension(),
    # ponytail: no nl2br — a single newline in wrapped source is a soft wrap, not a
    # <br> (Markdown spec). Intended breaks still work via two trailing spaces.
    "sane_lists",
    "attr_list",
    "footnotes",            # the work's own authorial/translator notes ([^n])
    "pymdownx.critic",      # editorial marks: {--cut--} {++add++} {~~a~>b~~} {>>note<<} {==hi==}
    WikiLinkExtension(base_url="/wiki/", end_url=".html", html_class="wikilink"),
])

def render_body(text: str) -> str:
    """Convert a Markdown string (CriticMarkup, footnotes, [[wikilinks]]) to an HTML fragment."""
    MD.reset()
    return MD.convert(text)
```

Then at `docs/serve.py:536-537`, replace:

```python
    MD.reset()
    body_html = MD.convert(text)
```

with:

```python
    body_html = render_body(text)
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd docs && python3 -m pytest tests/test_render.py -v`
Expected: PASS (5 passed). On first run `require()` pip-installs `pymdown-extensions`.

- [ ] **Step 5: Commit**

```bash
git add docs/serve.py docs/tests/test_render.py
git commit -m "feat(serve): render CriticMarkup, footnotes, and wikilinks"
```

---

### Task 2: clean-by-default reader chrome + CSS

**Files:**
- Modify: `docs/serve.py` (the `CSS` string ~`docs/serve.py:60-481`; the page template in `md_to_html` ~`docs/serve.py:557-578`)
- Test: `docs/tests/test_render.py` (extend)

**Interfaces:**
- Consumes: `serve.render_body` (Task 1).
- Produces: `serve.reader_chrome(body_html: str) -> str` — returns the toggle-rail HTML + script when the page contains editorial marks/wikilinks/footnotes, else `""`. Consumed by `md_to_html`.

- [ ] **Step 1: Write the failing tests**

```python
# append to docs/tests/test_render.py
def test_reader_chrome_present_when_marks_exist():
    chrome = serve.reader_chrome('<p>x <del class="critic">cut</del> y</p>')
    assert "Show cuts" in chrome and "data-layer" in chrome

def test_reader_chrome_absent_for_plain_text():
    assert serve.reader_chrome("<p>just prose</p>") == ""
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd docs && python3 -m pytest tests/test_render.py -k reader_chrome -v`
Expected: FAIL — `module 'serve' has no attribute 'reader_chrome'`

- [ ] **Step 3: Add `reader_chrome` and wire it into the template**

Add this function just below `render_body` in `docs/serve.py`:

```python
def reader_chrome(body_html: str) -> str:
    """Toggle rail for reader-edition pages; empty for ordinary docs."""
    has_marks = ('class="critic"' in body_html or 'class="wikilink"' in body_html
                 or 'class="footnote' in body_html or 'id="fn' in body_html)
    if not has_marks:
        return ""
    return """
<div id="reader-rail">
  <button data-layer="wikilinks">Wikilinks</button>
  <button data-layer="cuts">Show cuts</button>
  <button data-layer="notes">Notes</button>
  <button data-layer="footnotes">Footnotes</button>
</div>
<script>
(function(){
  var b=document.body;
  document.querySelectorAll('#reader-rail button').forEach(function(btn){
    btn.addEventListener('click',function(){
      var on=b.classList.toggle('show-'+btn.dataset.layer);
      btn.classList.toggle('active',on);
    });
  });
})();
</script>"""
```

In the `md_to_html` return template (`docs/serve.py:575-577`), change:

```python
<main>
{body_html}
</main>
```

to:

```python
<main class="reader-main">
{body_html}
</main>
{reader_chrome(body_html)}
```

- [ ] **Step 4: Add the CSS (clean default, reveal on toggle)**

Append to the `CSS` string (before its closing `"""` at `docs/serve.py:481`):

```css
/* Reader edition — clean by default, layers opt-in */
.reader-main { max-width: 38rem; margin: 0 auto; font-size: 1.12rem; line-height: 1.85; }
.reader-main del.critic { display: none; }                 /* cuts hidden */
body.show-cuts .reader-main del.critic {
  display: inline; background: #FAEEDA; color: #633806;
  border-left: 3px solid #EF9F27; padding: 0 .3em; font-style: italic;
}
.reader-main ins.critic { text-decoration: none; }
body.show-cuts .reader-main ins.critic { background: #E1F5EE; }
.reader-main .critic.comment, .reader-main .critic.subst del { display: none; }
body.show-notes .reader-main .critic.comment { display: inline; color: #854F0B; }
body.show-cuts .reader-main .critic.subst del { display: inline; }
.reader-main a.wikilink { color: inherit; text-decoration: none; border: 0; }
body.show-wikilinks .reader-main a.wikilink { color: #185FA5; border-bottom: 1px solid #85B7EB; }
.reader-main .footnote, .reader-main sup[id^="fnref"] { display: none; }
body.show-footnotes .reader-main .footnote,
body.show-footnotes .reader-main sup[id^="fnref"] { display: revert; }
#reader-rail { position: sticky; bottom: 1rem; display: flex; gap: .5rem;
  justify-content: center; margin-top: 2rem; flex-wrap: wrap; }
#reader-rail button.active { background: #185FA5; color: #fff; }
```

> Note: confirm `pymdownx.critic`'s emitted class names against the rendered output (open one fixture page); the spec assumes `del.critic` / `ins.critic` / `.critic.comment`. Adjust the selectors to the actual classes if they differ — this is the one place to verify, not assume.

- [ ] **Step 5: Run tests + build a smoke fixture**

```bash
cd docs && python3 -m pytest tests/test_render.py -v        # all pass
printf '%s\n' '---' 'title: Critic smoke' '---' '# Critic smoke' \
  'Poverty {~~springs from~>is connected with~~}{>>Chertkov softened this<<} this.' \
  '{--A cut sentence.--}{>>var. 8<<} The tax [[Henry George]] proposed.[^1]' '' \
  '[^1]: a footnote.' > /tmp/smoke.md
python3 -c "import serve,pathlib; print('show-cuts' in serve.md_to_html(pathlib.Path('/tmp/smoke.md')))"
```
Expected: tests pass; the last command prints `True` (the rail/CSS hooks are present).

- [ ] **Step 6: Commit**

```bash
git add docs/serve.py docs/tests/test_render.py
git commit -m "feat(serve): clean-by-default reader chrome with opt-in layers"
```

---

## Phase 2 — The Great Sin vertical slice (chapter I)

> Human-present, dive-discipline work. Ground in `docs/research/1905-the-great-sin/dossier.yaml` and `extracts/`. No mainstream framing in any prose (governing principle).

### Task 3: the overview page, distilled from `index.md`

**Files:**
- Read: `docs/research/1905-the-great-sin/index.md`
- Create: `docs/research/1905-the-great-sin/reader/overview.md`

- [ ] **Step 1:** Copy `index.md` to `reader/overview.md`.
- [ ] **Step 2:** Trim the research scaffolding — remove the `coverage`, `needsReview`, `archivesConsulted`, methodology, and any "triangulate against scholarship" passages. Keep: a light orientation paragraph first, then the factual genesis/reception detail (progressive disclosure).
- [ ] **Step 3:** Voice pass — remove any mainstream label Tolstoy refused; keep his terms. Add a "Read the work" line linking to `the-great-sin.en-1905.md` (created in Task 5).
- [ ] **Step 4 (gate):** `cd docs && python3 -c "import serve,pathlib; serve.md_to_html(pathlib.Path('research/1905-the-great-sin/reader/overview.md'))"` renders without error; read the output and confirm it opens light then deepens, with no mainstream-filter prose.
- [ ] **Step 5:** `git add docs/research/1905-the-great-sin/reader/overview.md && git commit -m "content(great-sin): reader overview distilled from index.md"`

---

### Task 4: the Russian version (the spine), chapter I

**Files:**
- Read: `docs/research/1905-the-great-sin/extracts/v36_206_230_Velikij_greh.txt`, `…/dossier.yaml` (evidence rows E15/E16/E17 and the softening row)
- Create: `docs/research/1905-the-great-sin/reader/the-great-sin.ru.md`

**Interfaces:**
- Produces: the shared section-anchor scheme — each chapter heading carries `{#sec-N}` (intro = `{#sec-0}`, I = `{#sec-1}`, … IX = `{#sec-9}`). Tasks 5 and 6 reuse the exact same anchors.

- [ ] **Step 1:** Create the file with frontmatter (`title`, `titleRu: Великий грех`, `type: work`, `version: ru`, `spine: true`) and the chapter-I heading `## I {#sec-1}`.
- [ ] **Step 2:** Paste chapter I's Russian prose verbatim from the extract (byte-true — this is the spine).
- [ ] **Step 3:** Insert the marks from the dossier *into* that prose, in Russian: the softening as `{~~происходят от~>связаны с~~}{>>…Chertkov, 8 Jul 1905…<<}`, and each cut (E15/E16/E17, var. 15/13/8) as `{--…cut Russian text from the variants extract…--}{>>var. N, cut…<<}` at its seam. Wikilink entities as `[[Генри Джордж]]` etc.
- [ ] **Step 4 (gate — fidelity):** strip the marks and confirm the prose still matches the source extract:

```bash
cd docs && python3 - <<'PY'
import re, pathlib
raw = pathlib.Path('research/1905-the-great-sin/reader/the-great-sin.ru.md').read_text(encoding='utf-8')
raw = raw.split('---',2)[-1]                       # drop frontmatter
raw = re.sub(r'\{>>.*?<<\}','',raw,flags=re.S)     # drop notes
raw = re.sub(r'\{--(.*?)--\}',r'\1',raw,flags=re.S)# cut text restored
raw = re.sub(r'\{\+\+(.*?)\+\+\}',r'\1',raw,flags=re.S)
raw = re.sub(r'\{~~(.*?)~>(.*?)~~\}',r'\2',raw,flags=re.S)  # substitution -> printed reading
raw = re.sub(r'\[\[(.*?)\]\]',r'\1',raw)
print("Stripped prose length:", len(raw.strip()))
PY
```
Compare the stripped chapter-I prose against the extract's chapter I — the printed-reading text must match the established PSS text word-for-word (the cuts restore the variant text, the substitution resolves to the printed «связаны с»). Eyeball the diff for the chapter.

- [ ] **Step 5:** `git add docs/research/1905-the-great-sin/reader/the-great-sin.ru.md && git commit -m "content(great-sin): Russian spine, chapter I, marked"`

---

### Task 5: the 1905 English version, chapter I

**Files:**
- Create: `docs/research/1905-the-great-sin/reader/the-great-sin.en-1905.md`
- Source: "A Great Iniquity" (Tchertkoff & Mayo, 1905) — public domain, on Wikisource (`https://en.wikisource.org/wiki/A_Great_Iniquity`)

- [ ] **Step 1:** Fetch the Wikisource text for chapter I; clean it (strip wiki chrome, keep the authorial/translator footnotes as `[^n]`).
- [ ] **Step 2:** Frontmatter (`version: en-1905`, `derivedFrom: ru`, no `spine`). Heading `## I {#sec-1}` — the **same anchor** as Task 4.
- [ ] **Step 3:** Port the marks into English: the softening as `{~~spring from~>is connected with~~}{>>…<<}`, the cuts as `{--…English of the cut passage…--}{>>var. N…<<}` (the 1905 English of the variant — machine-rendered and labelled if no period English of the variant exists), wikilinks as `[[Henry George]]`. Where the 1905 English *dropped* something present in the spine, mark it `{==…==}{>>dropped from the 1905 English<<}`.
- [ ] **Step 4 (gate):** renders via `serve.md_to_html`; the chapter-I anchor `{#sec-1}` matches Task 4's; read it beside the Russian to confirm alignment.
- [ ] **Step 5:** `git add … && git commit -m "content(great-sin): 1905 English version, chapter I, marked"`

---

### Task 6: the machine English version, chapter I

**Files:**
- Create: `docs/research/1905-the-great-sin/reader/the-great-sin.en-machine.md`

- [ ] **Step 1:** Generate a one-pass English translation of chapter I from the Russian spine prose (the cheap tier — no second-pass audit). Recipe: feed the chapter-I Russian to a translation prompt (in-session, or wrap `claude-cli` per the graphify finding), asking for a faithful, plain English rendering.
- [ ] **Step 2:** Frontmatter (`version: en-machine`, `derivedFrom: ru`, `label: "machine, unverified"`). Heading `## I {#sec-1}` — same anchor.
- [ ] **Step 3:** Carry the same cut/softening anchors (machine-rendered English of each), and a visible "machine, unverified" banner in the body top.
- [ ] **Step 4 (gate):** renders; the "machine, unverified" label is present; anchors match Tasks 4–5.
- [ ] **Step 5:** `git add … && git commit -m "content(great-sin): machine English version, chapter I"`

---

### Task 7: wire the slice into the preview and verify end-to-end

**Files:**
- Modify: `docs/research/1905-the-great-sin/reader/overview.md` (link the three versions)

- [ ] **Step 1:** In `overview.md`, add a "Versions" block linking `the-great-sin.en-1905.md` (default), `.en-machine.md`, `.ru.md`.
- [ ] **Step 2 (gate — build):** `cd docs && python3 serve.py --build-only` converts all four new files with no errors.
- [ ] **Step 3 (gate — behavior):** start `python3 serve.py`, open the 1905 English chapter I. Confirm: default view is clean (no marks, no wikilink underlines, no footnote markers); clicking **Show cuts** reveals the var. 8 excision and the softening's other reading; **Wikilinks** reveals the `[[Henry George]]` link; **Footnotes** reveals the translator notes; **Notes** reveals the `{>>…<<}` editorial notes.
- [ ] **Step 4 (gate — fidelity recap):** re-run the Task 4 strip-and-diff; zero prose differences in the Russian spine.
- [ ] **Step 5:** `git add … && git commit -m "content(great-sin): wire reader slice into preview, verified"`

---

## Self-review (done)

- **Spec coverage:** encoding (T1), clean-default + toggles (T2), overview-from-index.md (T3), spine + anchors + cuts-in-every-version (T4–6), machine pass (T6), serve.py preview (T1–2, T7). Governing principle enforced in T3–6 voice steps. Fidelity guardrail in T4/T7.
- **Deferred, by design (not gaps):** chapters II–IX (mechanical repetition of T4–6); the cross-dive generator that writes marks from the dossier at scale (spec's "scale step"); the full e-reader UI, My Library, progress, PWA, comments (spec 2).
- **Type consistency:** `render_body` / `reader_chrome` used consistently; `{#sec-N}` anchors identical across T4–6.

## Follow-up plans (not this plan)

1. **Finish The Great Sin** — chapters II–IX across the three versions (repeat T4–6).
2. **The cross-dive generator** — a companion step (skill or `--bundle-text`) that emits the version files + marks from a finished dive's dossier, runnable over the ~14 shipped dives. Build only after Johan reviews this pilot.
3. **Spec 2 — the e-reader website UI** (Eleventy): the docked rail, theming, TOC, My Library, reading progress, PWA offline, reader comments, update log. **→ Now specified and pulled forward into `serve.py` as a prototype: [`2026-07-03-interactive-reader-prototype-design.md`](../../superpowers/specs/2026-07-03-interactive-reader-prototype-design.md)** (v1 = the reading + annotation UX; the PWA pieces stay deferred to the `docs/pwa/` stages).
