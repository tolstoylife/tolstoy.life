#!/usr/bin/env python3
"""Byte-fidelity check for a corpus-dive dossier's evidence ledger.

Usage:
  verify_quotes.py <dossier.yaml>            # check every evidence row
  verify_quotes.py <dossier.yaml> --quiet    # only print failures + summary

What it checks, per `evidence[]` row:
  1. quoteRu byte-fidelity — the (whitespace-normalised) quoteRu must appear
     VERBATIM inside the named `extract` file. This is the dive's core
     credibility gate, made mechanical: no LLM judgement, no substring
     hand-rolling. Author-inserted elisions written as bracketed ellipses
     (`[…]` or `[...]`) are honoured — each fragment must be present, in order.
  2. facsimile existence — if `facsimile:` is set, the file must exist.
  3. translation label (soft) — quoteEn should carry the "(working English)"
     label; a missing label is a WARNING, not a failure.

Paths in the dossier (`extract`, `facsimile`) are resolved relative to the
dossier file's own directory, matching how a dive is laid out.

Exit codes:
  0  PASS — every quoteRu verbatim and every declared facsimile present
           (label warnings are allowed and do not fail the run)
  1  FAIL — at least one quoteRu mismatch or missing facsimile
  2  usage / parse error (bad path, unreadable YAML, missing PyYAML)

Run from anywhere:
  python3 docs/research/lib/verify_quotes.py docs/research/<slug>/dossier.yaml
"""
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("verify_quotes.py: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

# ⚠ Only bracketed ellipses count as the quoter's elision; a bare "…" mid-quote can be Tolstoy's own text.
ELLIPSIS_RE = re.compile(r"\[\s*(?:\.\.\.|…|\. \. \.)\s*\]")
# Leading/trailing ellipses (bare or bracketed) are stripped before matching; that only makes containment easier and never hides an error in the quote body.
LEAD_ELLIPSIS_RE = re.compile(r"^\s*(?:\[\s*(?:\.\.\.|…)\s*\]|\.\.\.|…)\s*")
TRAIL_ELLIPSIS_RE = re.compile(r"\s*(?:\[\s*(?:\.\.\.|…)\s*\]|\.\.\.|…)\s*$")
WORKING_EN = "(working English)"
MIN_FRAGMENT = 8  # ignore elision shards shorter than this (chars)


def normalise(s):
    """Collapse all runs of whitespace to single spaces and strip."""
    return " ".join((s or "").split())


def strip_boundary_ellipsis(s):
    """Drop a leading and/or trailing ellipsis (bare or bracketed) — the
    mid-sentence-start / mid-sentence-end marker — leaving the quote body."""
    return TRAIL_ELLIPSIS_RE.sub("", LEAD_ELLIPSIS_RE.sub("", s))


def longest_prefix_divergence(fragment, haystack):
    """Find where `fragment` stops being a prefix-substring of `haystack`.

    Returns (matched_text, first_diverging_word) so a mismatch report can point
    at the exact word that breaks containment — the thing you need to fix.
    """
    words = fragment.split()
    lo, hi, best = 0, len(words), 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid == 0 or " ".join(words[:mid]) in haystack:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    matched = " ".join(words[:best])
    diverging = words[best] if best < len(words) else "(end-of-quote)"
    return matched, diverging


def check_quote(quote_ru, extract_text):
    """Return (ok, detail). detail is None on success, else a mismatch report."""
    haystack = normalise(extract_text)
    quote_core = strip_boundary_ellipsis(quote_ru)
    needle = normalise(quote_core)
    if not needle:
        return False, "empty quoteRu"
    if needle in haystack:
        return True, None

    # Try internal author elisions: split on bracketed ellipsis, match each fragment in order.
    raw_frags = ELLIPSIS_RE.split(quote_core)
    frags = [normalise(f) for f in raw_frags]
    frags = [f for f in frags if len(f) >= MIN_FRAGMENT]
    if len(frags) >= 2:
        pos = 0
        for i, frag in enumerate(frags):
            idx = haystack.find(frag, pos)
            if idx < 0:
                matched, diverging = longest_prefix_divergence(frag, haystack)
                return False, (
                    f"elided fragment {i + 1}/{len(frags)} not found in order; "
                    f"diverges after “…{matched[-60:]}” at: “{diverging}”"
                )
            pos = idx + len(frag)
        return True, None

    matched, diverging = longest_prefix_divergence(needle, haystack)
    return False, f"diverges after “…{matched[-60:]}” at: “{diverging}”"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    quiet = "--quiet" in sys.argv[1:]
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(2)

    dossier_path = args[0]
    if not os.path.isfile(dossier_path):
        print(f"verify_quotes.py: no such file: {dossier_path}", file=sys.stderr)
        sys.exit(2)

    base = os.path.dirname(os.path.abspath(dossier_path))
    try:
        with open(dossier_path, encoding="utf-8") as fh:
            dossier = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        print(f"verify_quotes.py: YAML parse error: {exc}", file=sys.stderr)
        sys.exit(2)

    evidence = (dossier or {}).get("evidence") or []
    if not evidence:
        print(f"verify_quotes.py: no evidence rows in {dossier_path}", file=sys.stderr)
        sys.exit(2)

    print(f"verify_quotes.py — byte-fidelity check")
    print(f"dossier: {dossier_path}")
    print(f"{len(evidence)} evidence rows\n")

    quote_ok = quote_fail = skipped = 0
    fac_ok = fac_missing = 0
    label_warn = 0
    failures = []

    for row in evidence:
        rid = row.get("id", "<no-id>")
        quote_ru = row.get("quoteRu")
        extract_rel = row.get("extract")

        # 1. quoteRu byte-fidelity
        if not quote_ru or not extract_rel:
            skipped += 1
            if not quiet:
                print(f"  – {rid:42s} SKIP (no quoteRu/extract)")
        else:
            extract_path = os.path.join(base, extract_rel)
            if not os.path.isfile(extract_path):
                quote_fail += 1
                msg = f"extract file missing: {extract_rel}"
                failures.append((rid, msg))
                print(f"  ✗ {rid:42s} {msg}")
            else:
                with open(extract_path, encoding="utf-8") as fh:
                    text = fh.read()
                ok, detail = check_quote(quote_ru, text)
                if ok:
                    quote_ok += 1
                    if not quiet:
                        print(f"  ✓ {rid:42s} quoteRu verbatim in {extract_rel}")
                else:
                    quote_fail += 1
                    failures.append((rid, detail))
                    print(f"  ✗ {rid:42s} MISMATCH — {detail}")

        # 2. facsimile existence
        fac_rel = row.get("facsimile")
        if fac_rel:
            fac_path = os.path.join(base, fac_rel)
            if os.path.isfile(fac_path):
                fac_ok += 1
            else:
                fac_missing += 1
                failures.append((rid, f"facsimile missing: {fac_rel}"))
                print(f"  ✗ {rid:42s} facsimile missing: {fac_rel}")

        # 3. translation label (soft)
        quote_en = row.get("quoteEn")
        if quote_en and WORKING_EN not in quote_en:
            label_warn += 1
            if not quiet:
                print(f"  ⚠ {rid:42s} quoteEn missing \"{WORKING_EN}\" label")

    print()
    verdict = "PASS" if (quote_fail == 0 and fac_missing == 0) else "FAIL"
    print(
        f"SUMMARY: {quote_ok}/{quote_ok + quote_fail} quotes verbatim, "
        f"{fac_ok} facsimile(s) ok, {fac_missing} facsimile(s) missing, "
        f"{skipped} skipped, {label_warn} label warning(s) — {verdict}"
    )
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
