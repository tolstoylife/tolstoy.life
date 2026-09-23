#!/usr/bin/env bash
# Tests note-encoded-body recovery (v82_305, the 1910 note to the will, PSS Tom 82 pp. 227–231, body inside <note type="comments">) without pulling footnotes into normal extractions.
set -euo pipefail
export PYTHONUTF8=1   # force UTF-8 I/O; a C locale silently drops Cyrillic (see README)

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
EXTRACT="$HERE/extract_tei.py"
CORPUS="$REPO/primary-sources/tolstoydigital-TEI/texts/letters"

NOTE_DOC="$CORPUS/v82_305_Obyasnitelnayazapiskakzaveshhaniyu.xml"   # note-encoded body
NORMAL_DOC="$CORPUS/v78_170_N_A_SHejermanu.xml"                    # normal body + comments noteGrp

# --- 1. Note-encoded body IS recovered: the operative will provision must appear ---
OUT="$(python3 "$EXTRACT" "$NOTE_DOC")"
printf '%s\n' "$OUT" | grep -q 'Все его сочинения, литературные произведения' \
  || { echo "FAIL: v82_305 operative provision not recovered"; exit 1; }

# --- 2. Recovery is announced, not silent (banner names the apparatus source) ---
printf '%s\n' "$OUT" | grep -qi 'recovered' \
  || { echo "FAIL: v82_305 missing note-body recovery banner"; exit 1; }
printf '%s\n' "$OUT" | grep -q 'noteGrp' \
  || { echo "FAIL: recovery banner should name the noteGrp apparatus source"; exit 1; }

# --- 3. Genuine nested footnote (volume_editor note1, the 1927 committee) stays stripped ---
if printf '%s\n' "$OUT" | grep -q 'Комитет по исполнению воли'; then
  echo "FAIL: v82_305 leaked the nested volume_editor footnote into the body"; exit 1
fi

# --- 4. No pollution: a NORMAL letter's editorial apparatus must NOT leak ---
OUT2="$(python3 "$EXTRACT" "$NORMAL_DOC")"
if printf '%s\n' "$OUT2" | grep -q 'копировальной книге'; then
  echo "FAIL: normal extraction polluted with editorial commentary (noteGrp leaked)"; exit 1
fi

# --- 5. The normal letter's real <p> body is still extracted intact ---
printf '%s\n' "$OUT2" | grep -q 'Давно уже получил ваше письмо' \
  || { echo "FAIL: normal letter body went missing"; exit 1; }

# --- 6. Pre-reform <choice><orig>/<reg> resolution (the --choice flag) ---
FIX="$HERE/test-fixtures/prereform-choice.xml"

# reg mode resolves to the regularized (modern) reading and does NOT leak orig
REGOUT="$(python3 "$EXTRACT" "$FIX" --choice=reg)"
printf '%s\n' "$REGOUT" | grep -q 'старого' \
  || { echo "FAIL: --choice=reg did not resolve <reg> (старого missing)"; exit 1; }
printf '%s\n' "$REGOUT" | grep -q 'нового' \
  || { echo "FAIL: --choice=reg did not resolve the second <reg> (нового missing)"; exit 1; }
if printf '%s\n' "$REGOUT" | grep -q 'стараго'; then
  echo "FAIL: --choice=reg leaked the <orig> reading (стараго)"; exit 1
fi

# orig mode resolves to the pre-reform reading
ORIGOUT="$(python3 "$EXTRACT" "$FIX" --choice=orig)"
printf '%s\n' "$ORIGOUT" | grep -q 'стараго' \
  || { echo "FAIL: --choice=orig did not resolve <orig> (стараго missing)"; exit 1; }

# legacy default stays backward-compatible: it DROPS the pair (neither reading appears) ...
LEGOUT="$(python3 "$EXTRACT" "$FIX" 2>/dev/null)"
if printf '%s\n' "$LEGOUT" | grep -Eq 'старого|стараго'; then
  echo "FAIL: legacy default unexpectedly kept a pre-reform <choice> reading"; exit 1
fi
# ... but it must NOT be silent — a stderr nudge points at --choice=reg
LEGERR="$(python3 "$EXTRACT" "$FIX" 2>&1 >/dev/null)"
printf '%s\n' "$LEGERR" | grep -qi 'choice=reg' \
  || { echo "FAIL: legacy mode dropped pre-reform pairs without nudging about --choice=reg"; exit 1; }

# both mode emits reg reading AND orig reading in brackets
BOTHOUT="$(python3 "$EXTRACT" "$FIX" --choice=both)"
printf '%s\n' "$BOTHOUT" | grep -q 'старого' \
  || { echo "FAIL: --choice=both missing <reg> reading (старого)"; exit 1; }
printf '%s\n' "$BOTHOUT" | grep -q 'стараго' \
  || { echo "FAIL: --choice=both missing <orig> reading (стараго)"; exit 1; }

echo "PASS"
