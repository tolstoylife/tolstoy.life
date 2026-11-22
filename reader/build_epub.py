# reader/build_epub.py
"""Package a version's XHTML + timing.json into a read-along EPUB3.
ebooklib only zips the container; the SMIL media overlay and the media:* metadata
are hand-built (ebooklib's EpubSMIL is a content carrier only)."""
from reader import ids   # noqa: F401 (kept for parity; ids used by callers)

def clock(seconds):
    h = int(seconds // 3600); m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:06.3f}"

def section_duration(section_id, timing):
    ends = [c["end"] for c in timing["clips"].values() if c["section"] == section_id]
    return max(ends) if ends else 0.0

_SMIL = """<?xml version="1.0" encoding="utf-8"?>
<smil xmlns="http://www.w3.org/ns/SMIL" xmlns:epub="http://www.idpf.org/2007/ops" version="3.0">
<body>
<seq id="seq-{sec}" epub:textref="{xhtml}" epub:type="chapter">
{pars}
</seq>
</body></smil>"""

def build_smil(section_id, xhtml_href, audio_href, timing):
    pars = []
    clips = [(cid, c) for cid, c in timing["clips"].items() if c["section"] == section_id]
    for cid, c in clips:
        pars.append(
            f'<par id="par-{cid}">'
            f'<text src="{xhtml_href}#{cid}"/>'
            f'<audio src="{audio_href}" clipBegin="{clock(c["begin"])}" '
            f'clipEnd="{clock(c["end"])}"/></par>')
    return _SMIL.format(sec=section_id, xhtml=xhtml_href, pars="\n".join(pars))

def page_list_nav(seg):
    items = []
    for sec in seg["sections"]:
        for p in sec["paragraphs"]:
            if p.get("pss"):
                anchor = "page-" + p["pss"].replace(":", "-")
                items.append(f'<li><a href="text/{sec["id"]}.xhtml#{anchor}">'
                             f'PSS {p["pss"]}</a></li>')
    return ('<nav epub:type="page-list" hidden="hidden"><ol>'
            + "".join(items) + "</ol></nav>")

import os
from ebooklib import epub
from reader.build_xhtml import render_section_xhtml

_READER_CSS = """\
body { font-family: Palatino, "Iowan Old Style", Georgia, serif; line-height: 1.55; }
h2 { font-size: 1.25em; margin: 1.4em 0 0.7em; }
p { margin: 0 0 0.9em; }
aside { display: block; font-size: 0.88em; color: #555; margin: 0.6em 0; }
blockquote.epigraph { margin: 0 0 1em 2em; font-size: 0.9em; color: #444; }
.epigraph-source { text-align: right; font-variant: small-caps; }
/* current sentence during read-along — named by media:active-class in the OPF */
.-epub-media-overlay-active { background-color: #fff2a8; color: inherit; }
"""

_A11Y = [   # schema.org accessibility metadata (EPUB Accessibility 1.1 / WCAG 2.1 AA)
    ("schema:accessMode", "textual"), ("schema:accessMode", "auditory"),
    ("schema:accessModeSufficient", "textual"),
    ("schema:accessModeSufficient", "textual,auditory"),
    ("schema:accessibilityFeature", "synchronizedAudioText"),
    ("schema:accessibilityFeature", "readingOrder"),
    ("schema:accessibilityFeature", "structuralNavigation"),
    ("schema:accessibilityFeature", "displayTransformability"),
    ("schema:accessibilityHazard", "none"),
    ("schema:accessibilitySummary",
     "Read-along edition with sentence-level synchronized narration."),
]

def build_epub(seg, timing, out_path, meta, audio_root="."):
    book = epub.EpubBook()
    book.set_identifier(f"tolstoy-life-{seg['work']}-{seg['version']}")
    book.set_title(meta["title"]); book.set_language(meta["lang"])
    book.add_author(meta["author"])
    book.add_metadata("DC", "source", meta["source"])
    # EPUB3: a MARC relator can't be a bare role= attribute on dc:contributor;
    # it must be a refines meta pointing at the contributor's id.
    book.add_metadata("DC", "contributor", meta["translator"], {"id": "translator"})
    book.add_metadata(None, "meta", "trl",
                      {"refines": "#translator", "property": "role",
                       "scheme": "marc:relators"})
    book.add_metadata("DC", "date", meta["date"])
    book.add_metadata(None, "meta", "EPUB Accessibility 1.1",
                      {"property": "dcterms:conformsTo"})
    for prop, val in _A11Y:
        book.add_metadata(None, "meta", val, {"property": prop})
    book.add_metadata(None, "meta", "-epub-media-overlay-active",
                      {"property": "media:active-class"})

    # the stylesheet each section's XHTML links (../styles/reader.css); it must
    # exist in the package and define the active-class, or EPUBCheck CSS-030 fires.
    book.add_item(epub.EpubItem(uid="reader-css", file_name="styles/reader.css",
                                media_type="text/css",
                                content=_READER_CSS.encode("utf-8")))

    spine, total = ["nav"], 0.0
    for sec in seg["sections"]:
        sid = sec["id"]
        x = render_section_xhtml(seg, sid, meta["title"], meta["lang"])
        item = epub.EpubHtml(title=sec["heading"], file_name=f"text/{sid}.xhtml",
                             lang=meta["lang"])
        # ebooklib must get bytes: it feeds str content to lxml, which rejects the
        # <?xml encoding?> declaration and silently yields an empty body (then its
        # pagebreak scan crashes). Bytes parse cleanly.
        item.content = x.encode("utf-8")
        # ebooklib rebuilds the <head> from its own link registry on serialize and
        # drops any inline <link> in the content, so register the stylesheet via its
        # API — otherwise the read-along highlight CSS never reaches the document
        # (EPUBCheck CSS-030) and the active sentence has no defined highlight.
        item.add_link(href="../styles/reader.css", rel="stylesheet", type="text/css")
        audio_href = "../" + timing["audio"][sid]
        # SMIL lives in smil/; its text+audio srcs resolve relative to that folder,
        # so the xhtml (in text/) needs the ../text/ prefix or Books can't tie
        # narration to text and shows no read-along control.
        smil = build_smil(sid, f"../text/{sid}.xhtml", audio_href, timing)
        smil_item = epub.EpubSMIL(uid=f"smil-{sid}", file_name=f"smil/{sid}.smil",
                                  content=smil.encode("utf-8"))
        item.media_overlay = smil_item.get_id()
        dur = section_duration(sid, timing); total += dur
        book.add_metadata(None, "meta", clock(dur),
                          {"property": "media:duration",
                           "refines": f"#{smil_item.get_id()}"})
        # audio file as an EpubItem
        ap = os.path.join(audio_root, timing["audio"][sid])
        audio_bytes = open(ap, "rb").read() if os.path.exists(ap) else b"\x00"
        book.add_item(epub.EpubItem(uid=f"audio-{sid}",
            file_name=timing["audio"][sid], media_type="audio/mp4",
            content=audio_bytes))
        book.add_item(smil_item); book.add_item(item)
        spine.append(item)
    book.add_metadata(None, "meta", clock(total), {"property": "media:duration"})

    book.toc = [epub.Link(f"text/{s['id']}.xhtml", s["heading"], s["id"])
                for s in seg["sections"]]
    book.add_item(epub.EpubNcx()); book.add_item(epub.EpubNav())
    book.spine = spine
    epub.write_epub(out_path, book)
    return out_path


def main():
    """CLI: segments.json + timing.json + a meta.json -> read-along EPUB3.
    The last step of the build chain (reader.segment -> build_audiobook -> here)."""
    import argparse, json
    from pathlib import Path
    ap = argparse.ArgumentParser(description="segments.json + timing.json -> read-along EPUB3")
    ap.add_argument("--seg", required=True, help="segments.json for this version")
    ap.add_argument("--timing", required=True, help="timing.json from the audiobook build")
    ap.add_argument("--meta", required=True,
                    help="JSON with: title, author, lang, source, translator, date")
    ap.add_argument("-o", "--out", required=True, help="output .epub path")
    ap.add_argument("--audio-root", default=None,
                    help="dir holding audio/ (default: the timing.json's folder)")
    a = ap.parse_args()
    seg = json.loads(Path(a.seg).read_text(encoding="utf-8"))
    timing = json.loads(Path(a.timing).read_text(encoding="utf-8"))
    meta = json.loads(Path(a.meta).read_text(encoding="utf-8"))
    audio_root = a.audio_root or str(Path(a.timing).parent)
    out = build_epub(seg, timing, a.out, meta, audio_root=audio_root)
    print(f"wrote {out} ({len(seg['sections'])} sections, {len(timing['clips'])} synced clips)")


if __name__ == "__main__":
    main()
