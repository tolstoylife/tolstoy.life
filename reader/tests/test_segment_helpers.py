from reader.segment import resolve_reading_text, split_sentences

def test_resolve_criticmarkup():
    assert resolve_reading_text("I knew {--this--} the woman") == "I knew the woman"
    assert resolve_reading_text("a {++very ++}old woman") == "a very old woman"
    assert resolve_reading_text("the {~~horse~>cow~~}") == "the cow"
    assert resolve_reading_text("text {>>editor cut this<<}here") == "text here"
    assert resolve_reading_text("a {==dropped==} word") == "a dropped word"

def test_resolve_keeps_wikilink_and_footnote():
    assert resolve_reading_text("the [[old woman]] spoke") == "the [[old woman]] spoke"
    assert resolve_reading_text("a cow.[^1] I knew her.") == "a cow.[^1] I knew her."

def test_split_sentences_basic():
    out = split_sentences("First one. Second one! Third?")
    assert out == ["First one.", "Second one!", "Third?"]

def test_split_protects_decimals():
    out = split_sentences("It cost 1.40 rubles. That is dear.")
    assert out == ["It cost 1.40 rubles.", "That is dear."]

def test_split_keeps_quote_attribution_glued():
    out = split_sentences('"Why doesn\'t your son live at home?" I asked. He waved his hand.')
    assert out == ['"Why doesn\'t your son live at home?" I asked.', "He waved his hand."]

def test_split_after_quote_still_splits_without_attribution():
    out = split_sentences('"Where is he?" The peasant pointed.')
    assert out == ['"Where is he?"', "The peasant pointed."]

def test_split_before_a_sentence_opening_link():
    assert split_sentences("He left. [[Samara]] was far.") == ["He left.", "[[Samara]] was far."]
