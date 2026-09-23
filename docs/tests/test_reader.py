"""Reader v1 checks: the read-along sync mapping and the annotation shape.

Kept lean per the spec — one runnable check per risk, no framework beyond
pytest. Uses The Great Sin (the pilot bundle) as the fixture.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # docs/
import serve

BUNDLE = (pathlib.Path(__file__).resolve().parents[1]
          / "reader/non-fiction/essays-and-criticism/the-great-sin")


def _load(name):
    return json.loads((BUNDLE / "build" / name).read_text(encoding="utf-8"))


# ── Read-along: timing ↔ segments ↔ rendered page stay one coordinate system ──

def test_timing_maps_onto_segments_and_rendered_page():
    seg = _load("segments.en-1905.json")
    timing = _load("timing.en-1905.json")
    html = serve.md_to_html(BUNDLE / "the-great-sin.en-1905.md")
    rendered_ids = set(re.findall(r'id="([^"]+)"', html))

    section_ids = {s["id"] for s in seg["sections"]}
    sentence_ids = {snt["id"] for s in seg["sections"]
                    for p in s["paragraphs"] for snt in p["sentences"]}

    for clip_id, clip in timing["clips"].items():
        # every clip anchors to a real segment coordinate…
        assert clip_id in section_ids or clip_id in sentence_ids, clip_id
        # …that the work page actually renders
        assert clip_id in rendered_ids, f"{clip_id} not in rendered page"
        assert clip["end"] > clip["begin"] >= 0, clip_id
        assert clip["section"] in timing["audio"], clip_id

    # clips are section-relative and non-overlapping in reading order
    by_section = {}
    for clip_id, clip in timing["clips"].items():
        by_section.setdefault(clip["section"], []).append(clip)
    for sec, clips in by_section.items():
        clips.sort(key=lambda c: c["begin"])
        for a, b in zip(clips, clips[1:]):
            assert b["begin"] >= a["begin"], sec


def test_timing_words_per_second_sane():
    """The sanity guard that catches out-of-sync timing: spoken-word rate per
    sentence clip must be humanly plausible."""
    seg = _load("segments.en-1905.json")
    timing = _load("timing.en-1905.json")
    speech = {snt["id"]: snt["speech"] for s in seg["sections"]
              for p in s["paragraphs"] for snt in p["sentences"]}
    for clip_id, clip in timing["clips"].items():
        if clip_id not in speech:          # section-heading clips
            continue
        words = len(speech[clip_id].split())
        dur = clip["end"] - clip["begin"]
        wps = words / dur
        assert 0.3 < wps < 7, f"{clip_id}: {wps:.2f} words/s over {dur:.2f}s"


# ── Annotation: the W3C shape anchors back onto the rendered text ─────────────

def _make_annotation(doc_key, para_id, para_text, start, end, comment):
    """Python mirror of annotations.js makeAnnotation()."""
    return {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        "type": "Annotation",
        "motivation": "commenting",
        "body": [{"type": "TextualBody", "value": comment,
                  "format": "text/plain", "purpose": "commenting"}],
        "target": {
            "source": f"{doc_key}#{para_id}",
            "selector": [
                {"type": "TextQuoteSelector",
                 "exact": para_text[start:end],
                 "prefix": para_text[max(0, start - 30):start],
                 "suffix": para_text[end:end + 30]},
                {"type": "TextPositionSelector", "start": start, "end": end},
            ],
        },
    }


def test_annotation_round_trip_re_anchors():
    html = serve.md_to_html(BUNDLE / "the-great-sin.en-1905.md")
    # take a real paragraph's text the way the browser sees it
    m = re.search(r'<p id="(p-2-1)">(.*?)</p>', html, re.DOTALL)
    para_id, inner = m.group(1), m.group(2)
    para_text = re.sub(r"<[^>]+>", "", inner)

    ann = _make_annotation("docs/reader/…/the-great-sin.en-1905",
                           para_id, para_text, 10, 50, "check")

    # export → import: survives a JSON round trip intact
    ann2 = json.loads(json.dumps({"type": "AnnotationCollection",
                                  "items": [ann]}))["items"][0]

    # required W3C pieces present
    assert ann2["@context"] == "http://www.w3.org/ns/anno.jsonld"
    assert ann2["target"]["source"].endswith("#" + para_id)
    sel = {s["type"]: s for s in ann2["target"]["selector"]}
    assert "TextQuoteSelector" in sel and "TextPositionSelector" in sel

    # re-anchor: the quote is found at the stored position
    quote, pos = sel["TextQuoteSelector"], sel["TextPositionSelector"]
    assert para_text[pos["start"]:pos["end"]] == quote["exact"]
    assert para_text.index(quote["exact"]) <= pos["start"]


# ── Universal shell: works get transport, plain docs only the shell ───────────

def test_work_page_has_transport_and_sentences():
    html = serve.md_to_html(BUNDLE / "the-great-sin.en-1905.md")
    assert 'id="transport"' in html
    assert 'class="sentence"' in html
    assert "readalong.js" in html
    assert 'class="version-link' in html


def test_ru_page_has_no_transport():
    html = serve.md_to_html(BUNDLE / "the-great-sin.ru.md")
    assert 'id="transport"' not in html
    assert "readalong.js" not in html
    assert 'class="sentence"' in html          # still the segment render


def test_plain_doc_gets_shell_and_annotation_only():
    dive = (pathlib.Path(__file__).resolve().parents[1]
            / "research/works/non-fiction/essays-and-criticism/1905-the-great-sin/index.md")
    html = serve.md_to_html(dive)
    assert 'id="topbar"' in html and 'id="ann-popover"' in html
    assert 'id="transport"' not in html
    assert "version-link" not in html and "data-layer" not in html


# ── Overview page: the bundle's front page ────────────────────────────────────

def test_overview_page_links_and_folder_index():
    html = serve.md_to_html(BUNDLE / "overview.md")
    # top bar: Library; the Contents drawer lists the edition to read
    assert 'class="tb-lib" href="/reader/index.html"' in html
    assert 'href="/reader/non-fiction/essays-and-criticism/the-great-sin/the-great-sin.en-1905.html">English, 1905' in html
    assert 'id="transport"' not in html        # overview is a plain doc

    # the reading page points back at the overview, not the dive
    work_html = serve.md_to_html(BUNDLE / "the-great-sin.en-1905.md")
    assert 'href="/reader/non-fiction/essays-and-criticism/the-great-sin/overview.html"' in work_html
