"""Epigraphs stay outside the paragraph numbering; change marks reach a second, marked display field, one complete mark per sentence."""
import xml.dom.minidom as minidom
from reader.segment import parse
from reader.build_xhtml import render_section_xhtml

MD = """> Ныне ваше время и власть тьмы.
> — Лука, XXII, 53.

## I

> First quotation, first paragraph.
>
> First quotation, second paragraph.
> — Isaiah LIX.

> {++A restored epigraph.++}
> {++— Origen.++}

Plain start. {++Added one. Added two.++} Back to {~~printed~>restored~~} words.

One. {--A cut sentence.--} Two.

{>>A hidden slot note, never shown.<<}

## II

No epigraph here.
"""

def test_epigraphs_are_not_paragraphs():
    doc = parse(MD)
    sec = doc["sections"][0]
    assert [p["id"] for p in sec["paragraphs"]] == ["p-1-1", "p-1-2", "p-1-3"]
    assert [e["id"] for e in sec["epigraphs"]] == ["e-1-1", "e-1-2"]
    assert [x["display"] for x in sec["epigraphs"][0]["paragraphs"]] == ["First quotation, first paragraph.", "First quotation, second paragraph."]
    assert sec["epigraphs"][0]["source"] == {"display": "— Isaiah LIX."}
    assert "epigraphs" not in doc["sections"][1]

def test_title_epigraph_before_first_heading():
    e = parse(MD)["epigraphs"][0]
    assert e["id"] == "e-0-1" and e["source"]["display"] == "— Лука, XXII, 53."

def test_restored_epigraph_carries_marks():
    e = parse(MD)["sections"][0]["epigraphs"][1]
    assert e["paragraphs"][0] == {"display": "A restored epigraph.", "displayMarked": "{++A restored epigraph.++}"}
    assert e["source"]["displayMarked"] == "{++— Origen.++}"

def test_insertion_over_two_sentences_is_split_per_sentence():
    s = parse(MD)["sections"][0]["paragraphs"][0]["sentences"]
    assert [x["display"] for x in s] == ["Plain start.", "Added one.", "Added two.", "Back to restored words."]
    assert "displayMarked" not in s[0]
    assert s[1]["displayMarked"] == "{++Added one.++}"
    assert s[2]["displayMarked"] == "{++Added two.++}"
    assert s[3]["displayMarked"] == "Back to {--printed--}{++restored++} words."
    assert s[3]["speech"] == "Back to restored words."

def test_cut_sentence_rides_on_the_next_one():
    s = parse(MD)["sections"][0]["paragraphs"][1]["sentences"]
    assert [x["display"] for x in s] == ["One.", "Two."]
    assert s[1]["displayMarked"] == "{--A cut sentence. --}Two."

def test_hidden_note_stays_hidden():
    assert parse(MD)["sections"][0]["paragraphs"][2]["sentences"] == []

def test_epub_section_shows_epigraphs():
    seg = {"work": "w", "version": "en", **parse(MD)}
    html = render_section_xhtml(seg, "sec-1", "W", "en")
    minidom.parseString(html)
    assert 'id="e-0-1"' in html and 'id="e-1-2"' in html
    assert "First quotation, second paragraph." in html
    assert 'id="p-1-1"' in html and 'class="sentence" id="e-' not in html
