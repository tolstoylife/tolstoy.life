---
title: research.tolstoy.life — the docs folder as open research
date: 2026-09-22
---

# research.tolstoy.life — the docs folder as open research

Two steps, in this order. **Step 1** puts the `docs/` site online so Johan can read, listen to and annotate *A Confession* on his iPad while travelling. **Step 2** turns the same site into a soft public launch: open research that people can follow and help with. Step 1 is decided below; Step 2 is being discussed and will be added to this document when settled.

## What we found (2026-09-22)

- **The text is already public.** `tolstoylife/tolstoy.life` is a public GitHub repository and every markdown file in `docs/` is in it. Publishing the rendered pages adds readability and findability, not new exposure.
- **Two things are kept out of git on purpose:** the dive images (577 files, 340 MB in `research/**/visuals/`, some possibly not free to share) and the reader audio + read-along timing (`reader/**/build/`, about 230 MB). A site built on Johan's Mac would include both unless told not to.
- **61 HTML files in `docs/` have no markdown source in this branch** — leftovers from moved or deleted files, including the chapters of the Birukoff Vol IV translation that only exists on the unmerged `biryukov-vol4` branch. Copying the folder as it stands would publish them.
- **The 1,395 `.txt` extracts come from the tolstoydigital corpus**, licensed CC BY-SA. Republishing them needs a visible credit line.
- **Every page links from the site root** (`/reader/…`, `/research/…`), so the site must sit at the top of an address, not in a sub-folder.
- **Notes can't be made with a finger.** The note pop-up opens on a mouse-button release ([annotations.js:386](../../reader/assets/annotations.js)); selecting text by touch on an iPad doesn't produce one.
- **Notes are saved per page address**, so notes exported on the iPad import into the same page on Johan's local copy.
- **Safari deletes a site's saved notes after 7 days without a visit.** Regular reading keeps them; exporting now and then is the safeguard.
- **No Xcode on this Mac**, so there's no iPad simulator. Touch testing happens in the in-app browser (simulated) and on Johan's real iPad.

## Step 1 — A Confession on the iPad (decided)

**Address.** `research.tolstoy.life`, a new Netlify site of its own. The "Coming 2028" splash stays on `tolstoy.life` untouched. tolstoy.life's DNS is already on Netlify, so adding the address is one step in Netlify's web interface.

**Visibility.** Not linked from anywhere and marked "don't index" for search engines, so it can be shared by link but not found by searching. The marker carries an `@until launch` note in the code so it's found and removed at launch.

**What goes on the site.** Exactly three kinds of file:

1. files git tracks in `docs/`
2. the HTML that `serve.py` generates from tracked markdown
3. the reader bundles' audio and read-along timing (`reader/**/build/`)

Left out: dive images, HTML without a tracked source, scripts and tests, The Great Sin's `_audition/` test recordings, hidden files. A small script (`docs/publish.py`) builds the pages and gathers these into `_site/` at the repository root (already ignored by git).

**Credit.** The front page (`INDEX.html`) gets a line crediting the tolstoydigital corpus (CC BY-SA 4.0) and pointing to the project's public-domain dedication.

**Who publishes.** Johan runs the Netlify commands himself: first to a draft address for checking, then live. This follows his rule that he is the one who sends work off his machine.

**Online only.** Johan will mostly have a connection. No offline mode, no Home Screen app setup.

**Audio: unchanged.** Each section downloads in full before it plays. That costs a few seconds at each section start, but a dropped connection can't interrupt a section that has started.

**Notes by touch.** On a touch or Pencil selection, the note pop-up opens once the selection handles stop moving (about half a second), placed just below the selection and without pulling up the keyboard. Mouse and trackpad behaviour is unchanged.

**Getting notes home.** Nothing to build. On the iPad: Notes → "Copy JSON-LD". On the Mac, the same page on the local server → Notes → "Import…" and paste. With the same Apple ID on both, Universal Clipboard makes this a straight copy and paste.

**Testing.**

- The touch path is checked in the in-app browser with a simulated touch selection.
- Johan's iPad reaches the Mac's local server over home Wi-Fi (`http://Johans-Mac-mini.local:7877/…`) for a real touch check before anything is uploaded.
- After upload to the draft address, Johan checks on the iPad:
  - notes: save, reload, still there; export
  - audio: play a section and let it run into the next one
  - locked screen: does audio carry on? The least predictable part.

**Known limits, accepted for now.**

- 45 dive pages show broken images until Step 2 decides which images to publish.
- Some dive links point into `website/` and won't resolve on the site.
- The front page still describes itself as a "build log" mirrored to tolstoy.life/notes/, which doesn't exist yet. Step 2 rewrites it.

## Step 2 — the soft launch (to be discussed)

Open questions carried into the discussion:

- **Front door.** What tolstoy.life shows, and how it relates to research.tolstoy.life.
- **Images.** Which dive images to publish.
- **Working files.** Which to hide or tidy away: verifier reports, search logs, AI planning documents, Johan's `annotations.md` files.
- **Helpers.** How people can offer help.
- **Search.** When to let search engines in.

The launch checklist starts with `rg '@until launch' docs`, which finds every switch set for the unlisted period (at present, the "don't index" header in `publish.py`).
