# reader/build_xhtml.py
"""Render one section of a version's segments.json into EPUB-ready XHTML.
Resolved/static reading text (the split rule): footnotes become popup asides,
sentences carry stable IDs for the SMIL read-along. No JavaScript."""
import re, html
from reader import ids

_DOC = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{lang}" xml:lang="{lang}">
<head><meta charset="utf-8"/><title>{title}</title>
<link rel="stylesheet" type="text/css" href="../styles/reader.css"/></head>
<body epub:type="bodymatter chapter">
<section aria-labelledby="{sec}">
<h2 id="{sec}">{heading}</h2>
{paras}
{notes}
</section>
</body></html>"""

def noteref_html(label):
    nid = ids.note_id(int(label)) if label.isdigit() else f"note-{label}"
    rid = ids.noteref_id(int(label)) if label.isdigit() else f"noteref-{label}"
    return (f'<a epub:type="noteref" id="{rid}" href="#{nid}" '
            f'role="doc-noteref"><sup>{html.escape(label)}</sup></a>')

def aside_html(note):
    rid = note["id"].replace("note-", "noteref-")
    return (f'<aside epub:type="footnote" id="{note["id"]}" role="doc-footnote">'
            f'<p>{note["html"]} '
            f'<a href="#{rid}" epub:type="backlink" role="doc-backlink">↩</a></p></aside>')

def _render_sentence(text):
    # turn [^label] markers into noterefs, escape the rest
    text = re.sub(r"\[\[(?:[^\]|]+\|)?([^\]]+)\]\]", r"\1", text)   # ponytail: no wiki in the EPUB yet, keep the words
    parts = re.split(r"(\[\^\w+\])", text)
    out = []
    for p in parts:
        m = re.fullmatch(r"\[\^(\w+)\]", p)
        out.append(noteref_html(m.group(1)) if m else html.escape(p))
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", "".join(out))   # markdown italics

def epigraphs_xhtml(epigraphs):
    """Epigraphs as blockquotes: the reading text only (no marks in the EPUB yet), no sentence spans, so no read-along."""
    out = []
    for e in epigraphs or []:
        paras = "".join(f"<p>{_render_sentence(x['display'])}</p>" for x in e["paragraphs"])
        src = f'<p class="epigraph-source">{_render_sentence(e["source"]["display"])}</p>' if e.get("source") else ""
        out.append(f'<blockquote class="epigraph" id="{e["id"]}">{paras}{src}</blockquote>')
    return "\n".join(out)

def render_section_xhtml(seg, section_id, title, lang):
    sec = next(s for s in seg["sections"] if s["id"] == section_id)
    epis = (seg.get("epigraphs", []) if sec is seg["sections"][0] else []) + sec.get("epigraphs", [])   # the work's epigraph opens the first section
    epi_text = " ".join(x["display"] for e in epis for x in e["paragraphs"] + ([e["source"]] if e.get("source") else []))
    referenced = set(re.findall(r"\[\^(\w+)\]",
                     " ".join(s["display"] for p in sec["paragraphs"] for s in p["sentences"]) + " " + epi_text))
    paras = [epigraphs_xhtml(epis)] if epis else []
    for p in sec["paragraphs"]:
        spans = " ".join(
            f'<span class="sentence" id="{s["id"]}">{_render_sentence(s["display"])}</span>'
            for s in p["sentences"])
        pb = ""
        if p.get("pss"):
            anchor = "page-" + p["pss"].replace(":", "-")
            pb = (f'<span epub:type="pagebreak" id="{anchor}" role="doc-pagebreak" '
                  f'aria-label="PSS {p["pss"]}"></span>')
        paras.append(f'<p id="{p["id"]}">{pb}{spans}</p>')
    notes = [aside_html(n) for n in seg.get("notes", []) if n["label"] in referenced]
    return _DOC.format(lang=html.escape(lang), title=html.escape(title),
                       sec=section_id, heading=html.escape(sec["heading"]),
                       paras="\n".join(paras),
                       notes=("\n".join(notes)))
