"""Markdown (one version of a work) -> segments.json (the shared contract).
Each sentence gets a stable two-layer ID, its faithful display text, and its
speech text. The spine (Russian) defines the paragraph coordinate; translations
are validated as paragraph-parallel."""
import re, json, sys, argparse
from pathlib import Path
from reader import ids
from reader.speech import to_speech, MERGE_FORWARD

# ── CriticMarkup → reading text ────────────────────────────────────────────────
def resolve_reading_text(md):
    md = re.sub(r"\{>>.*?<<\}", "", md, flags=re.S)         # notes: drop
    md = re.sub(r"\{--(.*?)--\}", "", md, flags=re.S)       # deletions: drop
    md = re.sub(r"\{\+\+(.*?)\+\+\}", r"\1", md, flags=re.S)# insertions: keep
    md = re.sub(r"\{~~(.*?)~>(.*?)~~\}", r"\2", md, flags=re.S)  # change: keep new
    md = re.sub(r"\{==(.*?)==\}", r"\1", md, flags=re.S)    # highlight: keep
    md = re.sub(r"\[\[([^\]]+)\]\]", r"\1", md)             # wikilink: keep label
    return re.sub(r"[ \t]{2,}", " ", md).strip()

# ── Sentence split (ported from build_audiobook.split_sents) ───────────────────
def split_sentences(text):
    text = re.sub(r"(\d)\.(\d)", r"\1<DOT>\2", text)        # protect 1.40
    # `…?" I asked.` is one sentence: keep the attribution glued to its quote.
    # (Split off, "I asked." is a 2-word clip Kokoro can't land — it rises
    # instead of falling. Voice notes 2026-07-03; finding 12 in the audio doc.)
    text = re.sub(r'(?<=["”])\s+(?=I\s+(?:asked|said|replied|answered|repeated|exclaimed|thought)\b)',
                  "<ATTR>", text)
    # Split on whitespace after terminal punctuation. A footnote marker may sit
    # between the punctuation and the space ("cow.[^1] I") — keep it glued to the
    # sentence it ends, then split on a sentinel so the boundary still fires.
    text = re.sub(r'(?<=[.!?"])(\[\^\w+\])?\s+(?=["“(A-ZА-Я])', r"\1<SPLIT>", text)
    parts = text.split("<SPLIT>")
    return [p.replace("<DOT>", ".").replace("<ATTR>", " ").strip() for p in parts if p.strip()]

# ── Heading spoken form (ported from build_audiobook.spoken_header) ────────────
_ROMAN = {"I":"One","II":"Two","III":"Three","IV":"Four","V":"Five",
          "VI":"Six","VII":"Seven","VIII":"Eight","IX":"Nine","X":"Ten",
          "XI":"Eleven","XII":"Twelve","XIII":"Thirteen","XIV":"Fourteen","XV":"Fifteen",
          "XVI":"Sixteen","XVII":"Seventeen","XVIII":"Eighteen","XIX":"Nineteen","XX":"Twenty"}

def heading_speech(heading):
    m = re.match(r"(Part )?([IVX]+)\.?\s*$", heading.strip())
    if m and m.group(2) in _ROMAN:
        # ⚠ a bare numeral is spoken "Chapter …" — Kokoro reads "I" as "eye" and "II" as "Roman two".
        return f"{(m.group(1) or 'Chapter ').strip()} {_ROMAN[m.group(2)]}."
    return heading.strip().rstrip(".") + "."

# ── Structure parse ────────────────────────────────────────────────────────────
def _note_defs(md):
    """Pull '[^label]: text' definitions out; return (body_without_defs, notes)."""
    notes, n = [], 0
    def repl(m):
        nonlocal n
        n += 1
        notes.append({"id": ids.note_id(n), "label": m.group(1),
                      "html": m.group(2).strip()})
        return ""
    body = re.sub(r"^\[\^(\w+)\]:[ \t]*(.+)$", repl, md, flags=re.M)
    return body, notes

def merge_speech_groups(sentences):
    """Glue each MERGE_FORWARD sentence into the next one in its paragraph: joined
    display + joined speech, keeping the first id. Runs before segments.json is
    written, so clips / timeline / SMIL stay consistent (1 sentence = 1 clip = 1
    <par>) — the merged pair is just one small read-along unit (Option A). A flagged
    sentence with no following sentence is left alone (can't merge forward)."""
    out, i = [], 0
    while i < len(sentences):
        s = sentences[i]
        if s["id"] in MERGE_FORWARD and i + 1 < len(sentences):
            nxt = sentences[i + 1]
            out.append({"id": s["id"],
                        "display": s["display"] + " " + nxt["display"],
                        "speech": s["speech"] + " " + nxt["speech"]})
            i += 2
        else:
            out.append(s)
            i += 1
    return out

def parse(md):
    body, notes = _note_defs(md)
    # split into sections on '## ' headings; text before the first heading is ignored here
    chunks = re.split(r"^##\s+(.+)$", body, flags=re.M)
    sections = []
    # chunks = [pre, heading1, body1, heading2, body2, ...]
    sec_n = 0
    for i in range(1, len(chunks), 2):
        sec_n += 1
        heading = chunks[i].strip()
        sec = {"id": ids.section_id(sec_n), "heading": heading,
               "headingSpeech": heading_speech(heading), "paragraphs": []}
        paras = [p.strip() for p in re.split(r"\n\s*\n", chunks[i + 1]) if p.strip()]
        for pn, raw in enumerate(paras, start=1):
            pid = ids.paragraph_id(sec_n, pn)
            reading = resolve_reading_text(raw)
            sentences = []
            for sk, sent in enumerate(split_sentences(reading), start=1):
                sentences.append({"id": ids.sentence_id(pid, sk),
                                  "display": sent, "speech": to_speech(sent)})
            sec["paragraphs"].append({"id": pid,
                                      "sentences": merge_speech_groups(sentences)})
        sections.append(sec)
    return {"sections": sections, "notes": notes}

def segment(md_path, version, work, spine="ru", spine_doc=None):
    doc = parse(Path(md_path).read_text(encoding="utf-8"))
    if spine_doc is not None:
        for s_sec, t_sec in zip(spine_doc["sections"], doc["sections"]):
            if len(s_sec["paragraphs"]) != len(t_sec["paragraphs"]):
                raise ValueError(
                    f"paragraph count mismatch in {t_sec['id']}: spine has "
                    f"{len(s_sec['paragraphs'])}, {version} has {len(t_sec['paragraphs'])}")
        if len(spine_doc["sections"]) != len(doc["sections"]):
            raise ValueError("section count mismatch between spine and " + version)
    return {"work": work, "version": version, "spine": spine, **doc}

def main():
    ap = argparse.ArgumentParser(description="Markdown -> segments.json")
    ap.add_argument("md")
    ap.add_argument("--version", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--spine", default="ru")
    ap.add_argument("--spine-json", help="segments.json of the spine, to align against")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    spine_doc = json.loads(Path(a.spine_json).read_text()) if a.spine_json else None
    doc = segment(a.md, version=a.version, work=a.work, spine=a.spine, spine_doc=spine_doc)
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {a.out}: {len(doc['sections'])} sections, "
          f"{sum(len(s['paragraphs']) for s in doc['sections'])} paragraphs")

if __name__ == "__main__":
    main()
