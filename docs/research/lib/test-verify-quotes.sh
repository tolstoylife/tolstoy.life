#!/usr/bin/env bash
# Regression check for verify_quotes.py — run: bash docs/research/lib/test-verify-quotes.sh (prints PASS / FAIL)
# Asserts: (1) a clean dossier passes; (2) a tampered quoteRu fails; (3) a leading/trailing ellipsis quote passes; (4) an internal corruption is not masked by ellipsis handling.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL="$HERE/verify_quotes.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/extracts"

fail() { echo "FAIL: $1"; exit 1; }

# A tiny self-contained fixture: one extract file + dossiers that point at it.
cat > "$TMP/extracts/sample.txt" <<'TXT'
# sample
Дорогой брат! Пишу тебе о том, что не могу молчать.
Истина непременно победит, как бы её ни гнали.
TXT

mk_dossier() {  # $1=file  $2=quoteRu
  cat > "$1" <<YAML
topic: { slug: t, title: t }
evidence:
  - id: row1
    extract: extracts/sample.txt
    quoteRu: >-
      $2
    quoteEn: "x (working English)"
YAML
}

# 1. clean verbatim quote -> PASS
mk_dossier "$TMP/clean.yaml" "Истина непременно победит, как бы её ни гнали."
python3 "$TOOL" "$TMP/clean.yaml" --quiet >/dev/null 2>&1 \
  || fail "clean verbatim quote should pass (exit 0)"

# 2. tampered quote (wrong word in body) -> FAIL
mk_dossier "$TMP/tamper.yaml" "Истина обязательно победит, как бы её ни гнали."
python3 "$TOOL" "$TMP/tamper.yaml" --quiet >/dev/null 2>&1 \
  && fail "tampered quote should fail (exit 1)"

# 3. leading + trailing ellipsis (mid-sentence excerpt) -> PASS
mk_dossier "$TMP/boundary.yaml" "…Истина непременно победит…"
python3 "$TOOL" "$TMP/boundary.yaml" --quiet >/dev/null 2>&1 \
  || fail "boundary-ellipsis quote should pass after stripping"

# 4. internal bracketed elision, both fragments present -> PASS
mk_dossier "$TMP/elision.yaml" "Дорогой брат! [...] не могу молчать."
python3 "$TOOL" "$TMP/elision.yaml" --quiet >/dev/null 2>&1 \
  || fail "valid internal [...] elision should pass"

# 5. internal corruption hidden behind an elision -> still FAIL
mk_dossier "$TMP/elision-bad.yaml" "Дорогой брат! [...] не могу ЛГАТЬ."
python3 "$TOOL" "$TMP/elision-bad.yaml" --quiet >/dev/null 2>&1 \
  && fail "corrupted fragment must fail even with elision"

echo "PASS"
