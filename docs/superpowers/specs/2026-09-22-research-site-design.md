---
title: research.tolstoy.life — the docs folder as open research
date: 2026-09-22
---

# research.tolstoy.life — the docs folder as open research

Two steps, in this order. **Step 1** puts the `docs/` site online so Johan can read, listen to and annotate *A Confession* on his iPad while travelling. **Step 2** turns the same site into a soft public launch: open research that people can follow and help with. Both steps are decided below; Step 1 has its own step-by-step plan, and Step 2 gets one after the trip.

## What we found (2026-09-22)

- **The text is already public.** `tolstoylife/tolstoy.life` is a public GitHub repository and every markdown file in `docs/` is in it. Publishing the rendered pages adds readability and findability, not new exposure.
- **Two things are kept out of git on purpose:** the dive images (577 files, 340 MB in `research/**/visuals/`, some possibly not free to share) and the reader audio + read-along timing (`reader/**/build/`, about 230 MB). A site built on Johan's Mac would include both unless told not to.
- **61 HTML files in `docs/` have no markdown source in this branch** — leftovers from moved or deleted files, including the chapters of the Birukoff Vol IV translation that only exists on the unmerged `biryukov-vol4` branch. Copying the folder as it stands would publish them.
- **The 1,395 `.txt` extracts come from the tolstoydigital corpus**, licensed CC BY-SA. Republishing them needs a visible credit line.
- **Every page links from the site root** (`/reader/…`, `/research/…`), so the site must sit at the top of an address, not in a sub-folder.
- **Notes can't be made with a finger.** The note pop-up opens on a mouse-button release ([annotations.js:386](../../reader/assets/annotations.js)); selecting text by touch on an iPad doesn't produce one.
- **Notes are saved per page address**, so notes exported on the iPad import into the same page on Johan's local copy.
- **Safari deletes a site's saved notes after 7 days without a visit.** Regular reading keeps them; exporting now and then is the safeguard.
- **tolstoy.life/docs/ is already live**, serving a May 2026 copy of 16 early engineering documents from the splash project. Step 2 retires it.
- **No Xcode on this Mac**, so there's no iPad simulator. Touch testing happens in the in-app browser (simulated) and on Johan's real iPad.

## Step 1 — A Confession on the iPad (decided)

**Address.** `research.tolstoy.life`, a new Netlify site of its own. The "Coming 2028" splash stays on `tolstoy.life` untouched. tolstoy.life's DNS is already on Netlify, so adding the address is one step in Netlify's web interface.

**Visibility.** Not linked from anywhere and marked "don't index" for search engines, so it can be shared by link but not found by searching. The switch carries an `@until research-listed` note in the code, so it's found and removed when Johan decides the research may be found by search engines.

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

## Step 2 — the soft launch (decided 2026-09-22, after the trip)

> Step-by-step plan: [2026-09-22-research-site-soft-launch.md](../plans/2026-09-22-research-site-soft-launch.md), written 2026-09-22. Writing it corrected two counts below: the images were never published at all (`docs/.gitignore` ignores `research/**/visuals/`), and of the 575 image files there, 396 are recorded in a dossier as public domain or CC0, 13 carry another licence, and 166 appear in no dossier at all. The held-back working papers come to 121 files, linked from 18 published pages.

**Who it's for.** Readers and listeners: people who read or listen to an edition and say what's wrong or unclear. Russian readers, scholars and builders aren't invited yet.

### A. tolstoy.life — a short landing page

- **Where it's built.** In the existing splash project (`splash/tl`, repository `pjedlund/tl`, Astro). It keeps the splash look: the dark page with the T. It publishes the way the splash does now, when Johan pushes.
- **Words.** Claude drafts them in the site's plain, factual voice; Johan edits. The page has:
  - one sentence on what the project is, with 2028 as the date for the full site
  - **Read and listen now**: *A Confession* (Wiener's 1904 English, with read-along audio) and *The Great Sin*, each linking to its overview page on research.tolstoy.life
  - **Follow the research**: a link to the research index
  - **Help**: read or listen, and when something is wrong or unclear, select it, write a note and press *Send*
  - a line on the public-domain dedication
- **The old docs copy.** Since May, tolstoy.life/docs/ has served a copy of 16 early engineering documents, synced by the splash's `scripts/sync-docs.sh`. Remove the copy and the script. Forward the old addresses to research.tolstoy.life (`/docs/*` → `https://research.tolstoy.life/:splat.html`, permanent). Documents that have since moved simply end on the research site's "not on this site" page.
- **Search engines.** Allowed on the landing page.
- **Visitor counts.** The Umami counter already on the splash stays. It sets no cookies, so no consent banner is needed.

### B. research.tolstoy.life — ready for readers

- **Front page.** `INDEX.html` is rewritten for readers:
  - it leads with the Library (read and listen) and the research index
  - the dated notes and reference docs come further down
  - the stale "mirrored to tolstoy.life/notes/" line goes
- **Held back from the site.** `publish.py` leaves out:
  - Johan's `annotations.md` files
  - `superpowers/` (AI planning documents)
  - the `_verifier-report` files
  - the search logs (`_sweep*`, `_visuals-sweep`, `_visuals_sweep`, `_witness_sweep`)
  - session logs and handoffs inside the research folders

  The front page must not list them. About 31 published pages mention one of these files; following such a link lands on a plain "This page isn't on the site" page (`404.html`) with a way back to the front page.
- **Still public on GitHub.** Held-back files remain in the public repository. Making `annotations.md` truly private would mean taking it out of the repository and its history, a separate decision not taken here.
- **Images.** `publish.py` reads each dive's `dossier.yaml`:
  - An image whose `licence` is public domain (`PD…`, `public domain`) or `CC0` is published.
  - Every other image (unknown, rights-reserved, CC BY-SA) is left out, and in the uploaded copy of the page its `<img>` becomes a short note: "Image not shown — rights unclear".

  `docs/` itself is never changed by this. At 2026-09-22 that's roughly 450 images published and 74 withheld.
- **Search engines.** research.tolstoy.life stays unlisted until Johan says the research is ready to be found. The "don't index" switch in `publish.py` is marked `@until research-listed`.

### C. "Send" in the Notes panel

- **What it sends.** A *Send* button in the Notes panel sends the page's notes to the project: the readable text (as "Copy as text" makes it), the page address, and the notes' import data (as "Copy JSON-LD" makes it). Johan can paste that into "Import…" on his local copy and see a reader's notes in place in the text.
- **Reply address.** An optional email field, "if you'd like a reply". One sentence says exactly what is sent and that nothing else is collected.
- **How it's delivered.** Netlify Forms, the host's built-in form handling: no server of our own, 100 submissions a month free, a spam filter plus a hidden trap field for bots. The form must exist as plain HTML in the uploaded site so Netlify registers it at upload; `publish.py` writes it. In Netlify's settings, Johan switches on form detection and email notifications for the site.
- **After sending.** The notes stay in the reader's browser and the panel says "Sent, thank you". The button only shows on the live site, not on Johan's local server.

### D. Who does what, and when

- **When.** After the trip. Step 2's step-by-step plan is written then, so it can take in what the iPad step taught.
- **Who.** Claude builds and commits. Johan pushes the splash repository (which publishes the landing page), runs the research-site upload, and does the Netlify settings.
- **Launch checklist.** It starts with `rg '@until' docs`, which lists every switch set for the unlisted period.
