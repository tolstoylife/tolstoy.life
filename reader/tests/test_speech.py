from reader.speech import to_speech

def test_semicolon_before_conjunction_becomes_comma():
    assert to_speech("pahать time; and the horse is gone") == "pahать time, and the horse is gone"

def test_bare_semicolon_becomes_full_stop():
    assert to_speech("one thing; another follows") == "one thing. Another follows"

def test_respell_known_words():
    assert "Labooshair" in to_speech("the MP Labouchere spoke")
    assert "Yasnaya Polyahna" in to_speech("near Yasnaya Poliana")

def test_strips_footnote_marker():
    assert to_speech("leading a cow.[^1] I knew her.") == "leading a cow. I knew her."

def test_ellipsis_normalised():
    assert to_speech("well... maybe") == "well… maybe"

def test_respell_kvass():
    assert to_speech("Just enough for Kvas.") == "Just enough for quahss."

def test_money_spelled_out():
    assert "one dollar forty a day" in to_speech("work for an average of $1.40 a day, it is no wonder")

def test_professions_list_gets_full_stops():
    out = to_speech('These men—the nobles, merchants, Government officials, doctors, '
                    'engineers, professors, teachers, artists, students, advocates, '
                    'chiefly townspeople, the so-called "intellectuals"—are now in Russia')
    assert "the nobles. Merchants." in out
    assert "Chiefly townspeople. The so-called" in out

def test_welfare_list_gets_full_stops():
    out = to_speech(
        "For the welfare of the people we endeavor to abolish the censorship of books, "
        "arbitrary banishments, and to organize everywhere schools, common and agricultural, "
        "to increase the number of hospitals, to cancel passports and monopolies, to institute "
        "strict inspection in the factories, to reward maimed workers, to mark boundaries "
        "between properties, to contribute through banks to the purchase of land by peasants, "
        "and much else.")
    assert "banishments. And to organize" in out          # item boundary -> full stop
    assert "agricultural. To increase" in out              # internal commas kept, item split
    assert out.rstrip().endswith("And much else.")

def test_god_comma_becomes_pause():
    # page keeps the comma; speech gets a full stop so Kokoro pauses after "God"
    out = to_speech("God, Whom they have served and are serving so zealously, has expressed")
    assert out.startswith("God. Whom they have served")

def test_parasites_ending_gets_emdash():
    # comma -> em-dash in speech only, so the closing "their parasites" tag falls
    out = to_speech("in order to support us, their parasites.")
    assert "support us — their parasites." in out

def test_years_spoken_as_years():
    assert to_speech("in 1838, 1900 and 1905.") == "in eighteen thirty-eight, nineteen hundred and nineteen oh five."

def test_french_quote_marked_for_french_voice():
    assert to_speech("woman: “*Rien ne forme un jeune homme, comme une liaison avec une femme comme il faut.*” Another") == "woman: “‹fr›Rien ne forme un jeune homme, comme une liaison avec une femme comme il faut.‹/fr›” Another"

def test_italic_asterisks_not_spoken():
    assert to_speech("And *he* was amused.") == "And he was amused."

def test_german_marked_for_german_pronunciation():
    assert "‹de›Wille zum Leben‹/de›" in to_speech("that same wish to live—*Wille zum Leben*—which")
