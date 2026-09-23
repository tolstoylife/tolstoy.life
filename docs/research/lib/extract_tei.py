#!/usr/bin/env python3
"""Extract plain prose from a tolstoydigital-TEI XML file.

Usage:
  extract_tei.py <xml>                    # prints full body text + metadata
  extract_tei.py <xml> <substring>        # prints paragraphs containing substring
  extract_tei.py <xml> [--notes=MODE]     # control note-encoded-body recovery
  extract_tei.py <xml> [--choice=MODE]    # resolve pre-reform <choice><orig>/<reg>

Most documents carry their text in <p> body elements, with <note>/<noteGrp>
holding editorial footnotes that are stripped. A handful of PSS letters and
documents instead encode the document's own text inside <noteGrp type="comments">
apparatus (the body has no <p> at all). For those, --notes recovers that text:

  --notes=auto  (default)  recover note-encoded text only when the body has no
                           real <p>/<closer> prose — surgical, never pollutes a
                           normal extraction with its footnotes.
  --notes=off              legacy behaviour: never recover; strip all notes.
  --notes=force            also dump <noteGrp type="comments"> apparatus after a
                           normal body (for inspecting the editorial commentary).

Recovered paragraphs are tagged [note] and flagged by a banner — they mix the
document's own text with editorial commentary, so verify against the source PDF.

--choice controls pre-reform <choice><orig>/<reg> orthographic pairs:
  --choice=legacy (default)  drop the pair (historical behaviour); warns on stderr
                             so a forgetful run is not silently gutted.
  --choice=reg               resolve to the <reg> (modern-orthography) reading —
                             recommended for any pre-1918 text (all Prophet-period works).
  --choice=orig              resolve to the <orig> (pre-reform) reading.
  --choice=both              emit the <reg> reading with the <orig> in [brackets].
Editorial <choice><sic>/<corr> pairs are unaffected (always resolved to <corr>).
"""
import re
import sys
from lxml import etree

NS = {
    "t": "http://www.tei-c.org/ns/1.0",
    "xml": "http://www.w3.org/XML/1998/namespace",
}

SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def normalise_paragraph(p, choice_mode="legacy"):
    """Walk a <p> element and return its visible Russian prose, resolving <choice>/<sic>/<corr>."""
    parts = []
    for node in p.iter():
        tag = etree.QName(node).localname

        # Editorial <choice>: keep <corr>, skip <sic>; skip <note> bodies entirely.
        if tag == "note":
            # ⚠ Skip the footnote body but keep its .tail — the prose after a note anchor is Tolstoy's, and lxml's .clear() would wipe it.
            tail = node.tail
            node.clear()  # destructive but we don't reuse the tree
            node.tail = tail
            continue

    # Re-iterate cleanly: prefer <corr> over <sic>, drop <note>.
    text = []

    def walk(node):
        tag = etree.QName(node).localname
        if tag == "note":
            return
        if tag == "choice":
            # Editorial sic/corr: always prefer the corrected reading (unchanged).
            corr = node.find("t:corr", NS)
            if corr is not None:
                walk(corr)
                return
            # Pre-reform orig/reg spelling pairs: legacy mode drops them; reg/orig/both resolve them per --choice.
            reg = node.find("t:reg", NS)
            orig = node.find("t:orig", NS)
            if reg is not None or orig is not None:
                if choice_mode == "reg":
                    walk(reg if reg is not None else orig)
                elif choice_mode == "orig":
                    walk(orig if orig is not None else reg)
                elif choice_mode == "both":
                    if reg is not None:
                        walk(reg)
                        if orig is not None:
                            text.append(" [")
                            walk(orig)
                            text.append("]")
                    elif orig is not None:
                        # Degenerate: no <reg>; emit orig unbracketed (same as --choice=orig).
                        walk(orig)
                # choice_mode == "legacy": drop (preserve historical behaviour)
                return
            return
        if tag == "sic":
            return  # sibling of <corr>, already handled above
        # Footnote anchors: both digit-only markups the corpus uses get PSS-style superscript —
        #   <hi>1</hi>                     (Eltzbacher, Sacy letters)
        #   <ref target="#note1">1</ref>   (Schmitt, Stakhovich, Germogen, …)
        is_hi_anchor = (
            tag == "hi" and not node.get("style") and (node.text or "").strip().isdigit()
        )
        is_ref_anchor = (
            tag == "ref"
            and (node.get("target") or "").startswith("#note")
            and (node.text or "").strip().isdigit()
        )
        if is_hi_anchor or is_ref_anchor:
            t = node.text.strip()
            # eat trailing whitespace so the superscript binds to the preceding word
            while text and text[-1] and text[-1][-1:].isspace():
                text[-1] = text[-1].rstrip()
                if not text[-1]:
                    text.pop()
            text.append(t.translate(SUPERSCRIPT))
            return  # parent will handle node.tail
        if node.text:
            text.append(node.text)
        for child in node:
            walk(child)
            if child.tail:
                text.append(child.tail)

    walk(p)
    out = " ".join("".join(text).split())
    # Collapse space-before-punctuation produced by inline <title>/<emph> tails.
    out = re.sub(r"\s+([.,;:!?»])", r"\1", out)
    out = re.sub(r"([«])\s+", r"\1", out)
    # Repair boundaries TEI markup eats, e.g.  <name>(Paul Eltzbacher)</name>.1900 г.  →  "). 1900 г."
    out = re.sub(r"\)\.(\d)", r"). \1", out)
    #   ".1901г. Июля 28"   →   ". 1901 г. Июля 28"   (rare TEI source quirk)
    out = re.sub(r"(\d{4})г\.", r"\1 г.", out)
    return out


def recover_note_body(body, choice_mode="legacy"):
    """Recover paragraphs from <noteGrp type="comments"> apparatus that carries the
    document's own text.

    A few PSS documents (e.g. the 1910 Explanatory Note to Tolstoy's will, v82_305)
    encode their whole body inside <noteGrp type="comments"> rather than in <p>. The
    body-bearing notes are the <note type="comments"> children of the noteGrp; genuine
    footnotes nested deeper (e.g. <note resp="volume_editor" xml:id="note1">, the
    referenced editorial note) carry no type="comments" and are skipped — both because
    we only descend into the direct children here, and because normalise_paragraph()
    drops any <note> it walks into. Returns [(\"note\", text), ...] in document order.
    """
    recovered = []
    # ⚠ Snapshot the noteGrps first: normalise_paragraph() below mutates note subtrees.
    notegrps = list(body.iter("{http://www.tei-c.org/ns/1.0}noteGrp"))
    for notegrp in notegrps:
        if notegrp.get("type") != "comments":
            continue
        for note in notegrp.findall("t:note[@type='comments']", NS):
            for p in note.findall("t:p", NS):
                txt = normalise_paragraph(p, choice_mode)
                if txt:
                    recovered.append(("note", txt))
    return recovered


def extract(path, notes_mode="auto", choice_mode="legacy"):
    tree = etree.parse(path)
    root = tree.getroot()

    bibl = root.find(".//t:title[@type='bibl']", NS)
    main_title = root.find(".//t:title[@type='main']", NS)
    sub_title = root.find(".//t:title[@type='sub']", NS)
    file_id_el = root.find(".//t:title[@xml:id]", NS)

    bibl_text = bibl.text.strip() if bibl is not None and bibl.text else ""
    title_text = ""
    if main_title is not None and main_title.text:
        title_text = main_title.text.strip()
    if sub_title is not None and sub_title.text:
        title_text = (title_text + " " + sub_title.text.strip()).strip()

    file_id = ""
    if file_id_el is not None:
        file_id = file_id_el.get("{http://www.w3.org/XML/1998/namespace}id", "")

    paragraphs = []
    body = root.find(".//t:body", NS)
    if body is None:
        return file_id, title_text, bibl_text, [], 0, 0

    def inside_note(el):
        cur = el.getparent()
        while cur is not None and cur is not body:
            if etree.QName(cur).localname in ("note", "noteGrp"):
                return True
            cur = cur.getparent()
        return False

    # Collect openers and paragraphs in document order; skip any wrapped in editorial <note>.
    for el in body.iter():
        tag = etree.QName(el).localname
        if tag in ("opener", "p", "closer", "head"):
            if inside_note(el):
                continue
            txt = normalise_paragraph(el, choice_mode)
            if txt:
                paragraphs.append((tag, txt))

    # Note-encoded bodies: "auto" reads the comments apparatus only when the body has no real prose, so normal extractions never pick up footnotes; "force" always appends it.
    has_real_body = any(tag in ("p", "closer") for tag, _ in paragraphs)
    recovered = 0
    if notes_mode == "force" or (notes_mode == "auto" and not has_real_body):
        note_paras = recover_note_body(body, choice_mode)
        paragraphs.extend(note_paras)
        recovered = len(note_paras)
    prereform_pairs = sum(
        1
        for ch in body.iter("{http://www.tei-c.org/ns/1.0}choice")
        if (ch.find("t:reg", NS) is not None or ch.find("t:orig", NS) is not None)
        and ch.find("t:corr", NS) is None
    )
    return file_id, title_text, bibl_text, paragraphs, recovered, prereform_pairs


def main():
    notes_mode = "auto"
    choice_mode = "legacy"
    positional = []
    for arg in sys.argv[1:]:
        if arg.startswith("--notes="):
            notes_mode = arg.split("=", 1)[1]
        elif arg == "--no-notes":
            notes_mode = "off"
        elif arg.startswith("--choice="):
            choice_mode = arg.split("=", 1)[1]
        else:
            positional.append(arg)
    if not positional:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    if notes_mode not in ("auto", "off", "force"):
        print(f"invalid --notes mode: {notes_mode!r} (use auto|off|force)", file=sys.stderr)
        sys.exit(2)
    if choice_mode not in ("legacy", "reg", "orig", "both"):
        print(f"invalid --choice mode: {choice_mode!r} (use legacy|reg|orig|both)", file=sys.stderr)
        sys.exit(2)
    path = positional[0]
    needle = positional[1] if len(positional) > 1 else None

    file_id, title, bibl, paragraphs, recovered, prereform_pairs = extract(
        path, notes_mode, choice_mode
    )
    if choice_mode == "legacy" and prereform_pairs:
        print(
            f"# warning: dropped {prereform_pairs} pre-reform <choice><orig>/<reg> "
            f"pair(s) — re-run with --choice=reg to resolve them to modern orthography",
            file=sys.stderr,
        )
    print(f"# {title}")
    print(f"# id: {file_id}")
    print(f"# bibl: {bibl}")
    if recovered:
        print(
            f'# note-body: recovered {recovered} paragraph(s) from '
            f'<noteGrp type="comments"> apparatus — mixes document text with '
            f"editorial commentary; verify against the source PDF."
        )
    print()
    for tag, txt in paragraphs:
        if needle and needle.lower() not in txt.lower():
            continue
        prefix = f"[{tag}] " if tag != "p" else ""
        print(prefix + txt)
        print()


if __name__ == "__main__":
    main()
