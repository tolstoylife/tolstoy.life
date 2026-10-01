"""Display text -> speech text. Ported from projects/audiobook/flow_preprocess.py
(phrasing fixes) and build_audiobook.py SUBS (pronunciation respellings), so the
segmenter owns these rules and segments.json carries final speech text.
The display text stays faithful; we only reshape what the TTS hears."""
import re

_CONJ = r"(?:and|but|or|nor|yet|so|for)\b"

# Audio-only sentence merges (speechGroup). A sentence whose id is here is glued
# into the NEXT sentence of its paragraph before segments.json is written, so a
# too-short leading clip gets spoken with its neighbour's context and stops rising
# in pitch. The pair then highlights as one read-along unit (Option A). Explicit by
# id, NOT a word-count rule — a blanket "short sentence" rule would wrongly flatten
# legitimate rising questions ("Why is this?", "Whence this dreadful perversity?").
# ponytail: forward-merge only; add backward-merge if a short paragraph-final clip
# ever needs it. Applied in reader/segment.py.
MERGE_FORWARD = {"p-7-3-s1"}   # "But we are wrong." -> glue into the long next sentence

# Pronunciation respellings for Kokoro's g2p (verbatim from build_audiobook.py SUBS).
_SUBS = [
    (r"\blive\b", "liv"),
    (r"\bKvas\b", "quahss"),                 # any kv- onset reads as "key-v…" (no English /kv/); quahss -> kwɑːs
    (r"\$1\.40", "one dollar forty"),        # spell out money — the decimal dot reads as a full stop
    (r"\bLabouchere\b", "Labooshair"),
    (r"\bRadischeff\b", "Rahdeeshef"),
    (r"Yasnaya Poliana", "Yasnaya Polyahna"),
    (r"\bAlexander II\b\.?", "Alexander the Second"),   # regnal number reads as letters; also kills the abbrev-dot's spoken stop
    (r"\bper cent\.", "per cent"),                       # the archaic abbreviation dot reads as a full stop
    # The Part IV policy list rushes like the Part I professions list — full-stop
    # each item (the one pause Kokoro honors). Voice note 2026-07-04.
    (r"Tariffs, colonies, income taxes, military and naval budgets, socialistic "
     r"assemblies, unions, syndicates, the election of presidents, diplomatic connections",
     "Tariffs. Colonies. Income taxes. Military and naval budgets. Socialistic "
     "assemblies. Unions. Syndicates. The election of presidents. Diplomatic connections"),
    (r"\(Matt[.,] xxiii\. 27, 28\)",
     "Matthew twenty-three, verses twenty-seven and twenty-eight"),
    # The Part I professions list rushes at reading speed; give each item a full
    # stop — the one pause Kokoro honors (never splice silence at commas: it
    # breaks the pitch contour). Voice note 2026-07-03.
    (r"the nobles, merchants, Government officials, doctors, engineers, "
     r"professors, teachers, artists, students, advocates, chiefly townspeople, the so-called",
     "the nobles. Merchants. Government officials. Doctors. Engineers. "
     "Professors. Teachers. Artists. Students. Advocates. Chiefly townspeople. The so-called"),
    # The welfare infinitive-list (p-6-7-s1) rushes like the two noun lists — full-stop
    # each "to …" item for air. Internal commas (books, arbitrary banishments; schools,
    # common and agricultural) are kept. Voice note 2026-07-04.
    (r"to abolish the censorship of books, arbitrary banishments, and to organize "
     r"everywhere schools, common and agricultural, to increase the number of hospitals, "
     r"to cancel passports and monopolies, to institute strict inspection in the factories, "
     r"to reward maimed workers, to mark boundaries between properties, to contribute "
     r"through banks to the purchase of land by peasants, and much else",
     "to abolish the censorship of books, arbitrary banishments. And to organize "
     "everywhere schools, common and agricultural. To increase the number of hospitals. "
     "To cancel passports and monopolies. To institute strict inspection in the factories. "
     "To reward maimed workers. To mark boundaries between properties. To contribute "
     "through banks to the purchase of land by peasants. And much else"),
    # Wanted pause after "God," (p-7-8-s2): the engine never splices at commas, so make
    # it a full stop in speech only (the page keeps the comma). Voice note 2026-07-04.
    (r"God, Whom they have served", "God. Whom they have served"),
    # "…support us, their parasites." (p-6-6-s1): after the comma Kokoro renders the
    # closing appositive as a HIGH rising tag (~149 Hz). An em-dash in speech only keeps
    # a beat but drops "their parasites" ~38 Hz so it falls. Page keeps the comma.
    # Picked by pitch measurement (parselmouth). Voice note 2026-07-04.
    (r"support us, their parasites\.", "support us — their parasites."),
    (r"\bSchopenhauer\b", "Shopenhower"),
    (r"\bWille zum Leben\b", "Villa tsoom Layben"),
    (r"\bkumys\b", "koomiss"),
    (r"\*(Rien ne forme un jeune homme, comme une liaison avec une femme comme il faut\.)\*", r"‹fr›\1‹/fr›"),   # ‹fr›…‹/fr› is voiced with French pronunciation by the audiobook builder
]

_TENS = "_ ten twenty thirty forty fifty sixty seventy eighty ninety".split()
_ONES = "_ one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()

def _year_words(m):
    # ⚠ Kokoro reads a bare year as "one thousand eight hundred…"; speak 18xx/19xx the way a year is said.
    n = int(m.group(2))
    tail = "hundred" if n == 0 else f"oh {_ONES[n]}" if n < 10 else _ONES[n] if n < 20 else _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    return f"{'eighteen' if m.group(1) == '18' else 'nineteen'} {tail}"

def _fix_ellipsis(t):
    t = t.replace("...", "…")
    return re.sub(r"\.\s*\.\s*\.", "…", t)

def _fix_semicolons(t):
    t = re.sub(rf";\s+({_CONJ})", r", \1", t)            # "; and" -> ", and"
    return re.sub(r";\s+([a-zA-Z])", lambda m: ". " + m.group(1).upper(), t)

def _fix_dashes(t):
    t = t.replace("—", " — ")
    return re.sub(r"\s{2,}", " ", t)

def _respell(t):
    for pat, rep in _SUBS:
        t = re.sub(pat, rep, t)
    return t

def to_speech(text):
    text = re.sub(r"\[\^\w+\]", "", text)                # drop footnote markers (skippable in audio)
    text = _fix_ellipsis(text)
    text = _fix_semicolons(text)
    text = _fix_dashes(text)
    text = _respell(text)
    text = re.sub(r"\b(18|19)(\d\d)\b", _year_words, text)
    return text.strip()
