"""Markdown (one version of a work) -> segments.json (the shared contract).
Each sentence gets a stable two-layer ID, its faithful display text, and its
speech text. The spine (Russian) defines the paragraph coordinate; translations
are validated as paragraph-parallel."""
import re, json, sys, argparse
from pathlib import Path
from reader import ids
from reader.speech import to_speech, join_speech, MERGE_FORWARD, DASH_STOPS

# ── CriticMarkup → reading text ────────────────────────────────────────────────
def resolve_reading_text(md):
    md = re.sub(r"\{>>.*?<<\}", "", md, flags=re.S)         # notes: drop
    md = re.sub(r"\{--(.*?)--\}", "", md, flags=re.S)       # deletions: drop
    md = re.sub(r"\{\+\+(.*?)\+\+\}", r"\1", md, flags=re.S)# insertions: keep
    md = re.sub(r"\{~~(.*?)~>(.*?)~~\}", r"\2", md, flags=re.S)  # change: keep new
    md = re.sub(r"\{==(.*?)==\}", r"\1", md, flags=re.S)    # highlight: keep
    return re.sub(r"[ \t]{2,}", " ", md).strip()

# ── CriticMarkup → marked text, for the page's "Editorial changes" switch ──────
_MARK = re.compile(r"\{>>.*?<<\}|\{--(.*?)--\}|\{\+\+(.*?)\+\+\}|\{~~(.*?)~>(.*?)~~\}|\{==(.*?)==\}", re.S)
_HAS_CHANGE = re.compile(r"\{(\+\+|--|~~)")

def _marked_stream(md):
    """Kept characters with their kind ('plain'/'ins') and deleted runs anchored between them, collapsed and stripped exactly as resolve_reading_text does."""
    chars, dels = [], {}            # chars: [(ch, kind)]; dels: {index in chars: [deleted text]}
    def keep(text, kind):
        chars.extend((c, kind) for c in text)
    pos = 0
    for m in _MARK.finditer(md):
        keep(md[pos:m.start()], "plain")
        d, i, old, new, hi = m.groups()
        if d is not None:
            dels.setdefault(len(chars), []).append(d)
        elif i is not None:
            keep(i, "ins")
        elif old is not None:
            dels.setdefault(len(chars), []).append(old); keep(new, "ins")
        elif hi is not None:
            keep(hi, "plain")
        pos = m.end()
    keep(md[pos:], "plain")
    # collapse runs of 2+ spaces/tabs to one space, moving anchors with the kept characters
    out, odels, run = [], {}, 0
    for k in range(len(chars) + 1):
        if k in dels:
            odels.setdefault(len(out), []).extend(dels[k])
        if k == len(chars):
            break
        c, kind = chars[k]
        if c in " \t":
            run += 1
            if run >= 2:
                out[-1] = (" ", out[-1][1])
                continue
        else:
            run = 0
        out.append((c, kind))
    # strip leading/trailing whitespace
    lead = 0
    while lead < len(out) and out[lead][0].isspace():
        lead += 1
    end = len(out)
    while end > lead and out[end - 1][0].isspace():
        end -= 1
    final = {}
    for a, ds in odels.items():
        final.setdefault(min(max(a - lead, 0), end - lead), []).extend(ds)
    return out[lead:end], final

def _serialize(runs):
    """[(kind, text)] → text with {++…++} / {--…--} marks; neighbouring runs of one kind are merged."""
    merged = []
    for kind, text in runs:
        if text and merged and merged[-1][0] == kind:
            merged[-1] = (kind, merged[-1][1] + text)
        elif text:
            merged.append((kind, text))
    wrap = {"plain": "{}", "ins": "{{++{}++}}", "del": "{{--{}--}}"}
    return "".join(wrap[k].format(t) for k, t in merged)

def marked_text(md):
    """The marked twin of resolve_reading_text(md), or None when md has no change marks (notes and highlights don't count)."""
    if not _HAS_CHANGE.search(md):
        return None
    chars, dels = _marked_stream(md)
    runs = []
    for k in range(len(chars) + 1):
        runs.extend(("del", d) for d in dels.get(k, []))
        if k < len(chars):
            runs.append((chars[k][1], chars[k][0]))
    return _serialize(runs)

def marked_sentences(md, sentences):
    """Split the marked text of md along the given sentences (from split_sentences(resolve_reading_text(md))); each sentence gets complete marks of its own. Returns one marked string per sentence, or None for all when md has no change marks."""
    if not _HAS_CHANGE.search(md):
        return [None] * len(sentences)
    chars, dels = _marked_stream(md)
    reading = "".join(c for c, _ in chars)
    if reading != resolve_reading_text(md):
        raise ValueError("marked text does not resolve to the reading text: " + reading[:80])
    spans, c = [], 0                       # (start, end) of each sentence in reading
    for sent in sentences:
        while c < len(reading) and reading[c].isspace():
            c += 1
        start, j = c, 0
        while j < len(sent):
            if c < len(reading) and reading[c] == sent[j]:
                c += 1; j += 1
            elif c < len(reading) and reading[c].isspace() and sent[j].isspace():
                while c < len(reading) and reading[c].isspace():
                    c += 1
                while j < len(sent) and sent[j].isspace():
                    j += 1
            else:
                raise ValueError(f"cannot place sentence in its paragraph: {sent[:60]!r}")
        spans.append((start, c))
    # ⚠ a deletion belongs to the sentence it touches at the end, else to the next one
    owner = {}
    for a in sorted(dels):
        k = next((i for i, (_, e) in enumerate(spans) if a <= e), len(spans) - 1)
        owner.setdefault(k, []).append(a)
    out = []
    for i, (s, e) in enumerate(spans):
        runs = []
        mine = owner.get(i, [])
        for a in mine:
            if a <= s:                     # a cut before the sentence: keep a space between it and the sentence
                runs.extend(("del", d if d[-1:].isspace() else d + " ") for d in dels[a])
        for k in range(s, e):
            if k != s and k in dels and k in mine:
                runs.extend(("del", d) for d in dels[k])
            runs.append((chars[k][1], chars[k][0]))
        if e != s and e in dels and e in mine:
            runs.extend(("del", d) for d in dels[e])
        text = _serialize(runs)
        out.append(text if text != sentences[i] else None)
    return out

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
    text = re.sub(r'(?<=[.!?"])(\[\^\w+\])?\s+(?=["“(A-ZА-ЯÅÄÖ»]|\[\[)', r"\1<SPLIT>", text)
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

def merge_speech_groups(sentences, flagged=frozenset()):
    """Glue each flagged sentence into the next one in its paragraph: joined
    display + joined speech, keeping the first id. Runs before segments.json is
    written, so clips / timeline / SMIL stay consistent (1 sentence = 1 clip = 1
    <par>) — the merged run is just one small read-along unit (Option A). Consecutive
    flags chain into one sentence. A flagged last sentence is left alone."""
    out, i = [], 0
    while i < len(sentences):
        s = sentences[i]
        while sentences[i]["id"] in flagged and i + 1 < len(sentences):
            i += 1
            nxt = sentences[i]
            marked = (s.get("displayMarked") or s["display"]) + " " + (nxt.get("displayMarked") or nxt["display"])
            s = {"id": s["id"], "display": s["display"] + " " + nxt["display"],
                 "speech": join_speech(s["speech"], nxt["speech"]),
                 **({"displayMarked": marked} if "displayMarked" in s or "displayMarked" in nxt else {})}
        out.append(s)
        i += 1
    return out

def _text_pair(raw):
    """{display, displayMarked?} for a piece of text that isn't split into sentences."""
    d = {"display": resolve_reading_text(raw)}
    m = marked_text(raw)
    if m is not None and m != d["display"]:
        d["displayMarked"] = m
    return d

def _take_epigraphs(blocks, sec_n):
    """Peel the leading quoted blocks (every line starts with '>') off a section's blocks. Each becomes an epigraph: its paragraphs, and its source from a last line starting with '— '. Epigraphs are not paragraphs, so they never shift paragraph ids."""
    epigraphs = []
    while blocks and all(line.lstrip().startswith(">") for line in blocks[0].splitlines()):
        lines = [re.sub(r"^\s*>\s?", "", line) for line in blocks.pop(0).splitlines()]
        while lines and not lines[-1].strip():
            lines.pop()
        source = lines.pop().strip() if lines and re.match(r"(\{\+\+)?—\s", lines[-1].strip()) else None
        paras = [" ".join(x.strip() for x in chunk.splitlines()) for chunk in re.split(r"\n\s*\n", "\n".join(lines)) if chunk.strip()]
        epi = {"id": ids.epigraph_id(sec_n, len(epigraphs) + 1), "paragraphs": [_text_pair(x) for x in paras]}
        if source:
            epi["source"] = _text_pair(source)
        epigraphs.append(epi)
    return epigraphs, blocks

def parse(md, work=None, version=None):
    body, notes = _note_defs(md)
    flagged = MERGE_FORWARD.get(work, set()) | MERGE_FORWARD.get(f"{work}/{version}", set())
    dash_stops = DASH_STOPS.get(work, set()) | DASH_STOPS.get(f"{work}/{version}", set())
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
        epigraphs, paras = _take_epigraphs(paras, sec_n)
        if epigraphs:                      # before "paragraphs", as on the page
            sec = {k: v for k, v in sec.items() if k != "paragraphs"} | {"epigraphs": epigraphs, "paragraphs": []}
        for pn, raw in enumerate(paras, start=1):
            pid = ids.paragraph_id(sec_n, pn)
            reading = resolve_reading_text(raw)
            sentences = []
            split = split_sentences(reading)
            for sk, (sent, marked) in enumerate(zip(split, marked_sentences(raw, split)), start=1):
                st = {"id": ids.sentence_id(pid, sk), "display": sent, "speech": to_speech(sent)}
                if marked is not None:
                    st["displayMarked"] = marked
                sentences.append(st)
            if pid in dash_stops:
                for st in sentences:
                    st["speech"] = re.sub(r"\s*—\s*(\w)", lambda m: ". " + m.group(1).upper(), st["speech"])
            sec["paragraphs"].append({"id": pid,
                                      "sentences": merge_speech_groups(sentences, flagged)})
        sections.append(sec)
    doc = {"sections": sections, "notes": notes}
    title_epigraphs, _ = _take_epigraphs([p.strip() for p in re.split(r"\n\s*\n", chunks[0]) if p.strip()], 0)
    if title_epigraphs:                    # quoted blocks before the first heading: the whole work's epigraph
        doc = {"epigraphs": title_epigraphs, **doc}
    return doc

def segment(md_path, version, work, spine="ru", spine_doc=None, missing_tail=0):
    doc = parse(Path(md_path).read_text(encoding="utf-8"), work, version)
    if spine_doc is not None:
        for s_sec, t_sec in zip(spine_doc["sections"], doc["sections"]):
            if len(s_sec["paragraphs"]) != len(t_sec["paragraphs"]):
                raise ValueError(
                    f"paragraph count mismatch in {t_sec['id']}: spine has "
                    f"{len(s_sec['paragraphs'])}, {version} has {len(t_sec['paragraphs'])}")
        # missing_tail: a version printed without the spine's last N sections (e.g. the 1904 Swedish has no postscript)
        if len(spine_doc["sections"]) - missing_tail != len(doc["sections"]):
            raise ValueError("section count mismatch between spine and " + version)
    return {"work": work, "version": version, "spine": spine, **doc}

def main():
    ap = argparse.ArgumentParser(description="Markdown -> segments.json")
    ap.add_argument("md")
    ap.add_argument("--version", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--spine", default="ru")
    ap.add_argument("--spine-json", help="segments.json of the spine, to align against")
    ap.add_argument("--missing-tail", type=int, default=0, help="this version lacks the spine's last N sections")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    spine_doc = json.loads(Path(a.spine_json).read_text()) if a.spine_json else None
    doc = segment(a.md, version=a.version, work=a.work, spine=a.spine, spine_doc=spine_doc,
                  missing_tail=a.missing_tail)
    meta = Path(a.md).parent / f"meta.{a.version}.json"
    if meta.exists() and doc["sections"]:   # the narrator says the book's title before the first heading
        title = json.loads(meta.read_text(encoding="utf-8")).get("title")
        if title:
            stop = "" if title[-1] in ".!?" else "."
            doc["sections"][0]["headingSpeech"] = f"{title}{stop} {doc['sections'][0]['headingSpeech']}"
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {a.out}: {len(doc['sections'])} sections, "
          f"{sum(len(s['paragraphs']) for s in doc['sections'])} paragraphs")

if __name__ == "__main__":
    main()
