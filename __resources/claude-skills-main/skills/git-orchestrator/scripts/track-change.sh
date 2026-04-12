#!/bin/bash
# Track Change Hook - Log file modifications

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
PENDING_FILE="$CLAUDE_DIR/.git/pending-changes.jsonl"
FILE_PATH="${CLAUDE_INPUT:-$1}"

# Only track changes within ~/.claude
if [[ "$FILE_PATH" != "$CLAUDE_DIR"* ]]; then
  exit 0
fi

# Append to pending changes
echo "{\"file\": \"$FILE_PATH\", \"time\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"tool\": \"${CLAUDE_TOOL:-unknown}\"}" >> "$PENDING_FILE"

# Track significant changes with bd
if [[ "$FILE_PATH" == *"SKILL.md"* ]] || [[ "$FILE_PATH" == *"/agents/"* ]]; then
  bd add "Modified: $(basename "$FILE_PATH")" --tags config,significant 2>/dev/null || true
fi
