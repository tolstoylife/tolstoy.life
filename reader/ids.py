"""The one ID-numbering rule, shared by the segmenter and serve.py so they never drift.
Spec: paragraph p-{section}-{n} is the public citable coordinate; sentence
p-{section}-{n}-s{k} is read-along plumbing; typed counters are per-section."""

def section_id(n): return f"sec-{n}"
def paragraph_id(section, n): return f"p-{section}-{n}"
def sentence_id(paragraph_id, k): return f"{paragraph_id}-s{k}"
def typed_id(prefix, section, n): return f"{prefix}-{section}-{n}"
def epigraph_id(section, n): return typed_id("e", section, n)   # section 0 = the whole work
def note_id(n): return f"note-{n}"
def noteref_id(n): return f"noteref-{n}"
