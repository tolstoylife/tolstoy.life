from reader.segment import parse, heading_speech, merge_speech_groups

MD = open("reader/tests/fixtures/mini.en-1905.md").read()

def test_heading_speech():
    assert heading_speech("Part I") == "Part One."
    assert heading_speech("Part IV") == "Part Four."
    assert heading_speech("Introduction") == "Introduction."
    assert heading_speech("I") == "Chapter One."
    assert heading_speech("XVI") == "Chapter Sixteen."

def test_parse_structure():
    doc = parse(MD)
    assert len(doc["sections"]) == 1
    sec = doc["sections"][0]
    assert sec["id"] == "sec-1"
    assert sec["heading"] == "Part I"
    assert sec["headingSpeech"] == "Part One."
    assert [p["id"] for p in sec["paragraphs"]] == ["p-1-1", "p-1-2"]

def test_parse_sentence_ids_and_text():
    sec = parse(MD)["sections"][0]
    s = sec["paragraphs"][0]["sentences"]
    assert [x["id"] for x in s] == ["p-1-1-s1", "p-1-1-s2"]
    assert s[0]["display"] == "The other day I was walking along the high road to Tula."

def test_parse_resolves_marks_in_display():
    sec = parse(MD)["sections"][0]
    p2 = sec["paragraphs"][1]["sentences"]
    # wikilink label kept, footnote marker kept in display, stripped in speech
    assert "[[old woman]]" not in p2[1]["display"]
    assert "old woman" in p2[1]["display"]
    assert "[^1]" in p2[0]["display"]
    assert "[^1]" not in p2[0]["speech"]

def test_parse_collects_notes():
    notes = parse(MD)["notes"]
    assert notes == [{"id": "note-1", "label": "1", "html": "A cow without milk."}]

def test_merge_speech_groups_glues_flagged_sentence_forward():
    # p-7-3-s1 ("But we are wrong.") is the configured merge; it absorbs the next
    # sentence, keeps its own id, and the paragraph loses one sentence.
    sents = [
        {"id": "p-7-3-s1", "display": "But we are wrong.", "speech": "But we are wrong."},
        {"id": "p-7-3-s2", "display": "Among us there are many.", "speech": "Among us there are many."},
        {"id": "p-7-3-s3", "display": "The end.", "speech": "The end."},
    ]
    out = merge_speech_groups(sents)
    assert [s["id"] for s in out] == ["p-7-3-s1", "p-7-3-s3"]
    assert out[0]["display"] == "But we are wrong. Among us there are many."
    assert out[0]["speech"] == "But we are wrong. Among us there are many."

def test_merge_speech_groups_leaves_unflagged_untouched():
    sents = [{"id": "p-1-1-s1", "display": "A short one.", "speech": "A short one."},
             {"id": "p-1-1-s2", "display": "Another.", "speech": "Another."}]
    assert merge_speech_groups(sents) == sents

def test_merge_speech_groups_flagged_last_sentence_is_safe():
    # a flagged sentence with nothing after it can't merge forward — left alone
    sents = [{"id": "p-7-3-s1", "display": "But we are wrong.", "speech": "But we are wrong."}]
    assert merge_speech_groups(sents) == sents
