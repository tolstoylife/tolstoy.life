import re
from reader.build_xhtml import render_section_xhtml
from reader.segment import segment

def _seg():
    return segment("reader/tests/fixtures/mini.en-1905.md",
                   version="en-1905", work="the-great-sin")

def test_sentence_spans_have_typed_ids():
    html = render_section_xhtml(_seg(), "sec-1", "The Great Sin", "en")
    assert '<span class="sentence" id="p-1-1-s1">' in html
    assert 'id="p-1-2"' in html            # paragraph id
    assert 'id="sec-1"' in html            # heading anchor

def test_footnote_becomes_noteref_and_aside():
    html = render_section_xhtml(_seg(), "sec-1", "The Great Sin", "en")
    assert 'epub:type="noteref"' in html
    assert '<aside epub:type="footnote"' in html
    assert 'A cow without milk.' in html
    # marker text [^1] must NOT survive literally
    assert "[^1]" not in html

def test_is_wellformed_xml():
    import xml.dom.minidom as m
    html = render_section_xhtml(_seg(), "sec-1", "The Great Sin", "en")
    m.parseString(html)   # raises on malformed XML

def test_italics_become_em():
    from reader.build_xhtml import _render_sentence
    assert _render_sentence("And *he* was amused.") == "And <em>he</em> was amused."
