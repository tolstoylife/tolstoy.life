#!/bin/bash
# Session Commit Hook - Auto-commit pending changes

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
STATE_FILE="$CLAUDE_DIR/.git/session-state.json"
PENDING_FILE="$CLAUDE_DIR/.git/pending-changes.jsonl"

# Check for pending changes
if [ ! -f "$PENDING_FILE" ] || [ ! -s "$PENDING_FILE" ]; then
  echo "No pending changes to commit"
  exit 0
fi

# Read session state
SESSION_ID=$(jq -r .session_id "$STATE_FILE" 2>/dev/null || echo "unknown")
START_COMMIT=$(jq -r .start_commit "$STATE_FILE" 2>/dev/null || echo "HEAD~1")

# Collect unique files
FILES=$(cat "$PENDING_FILE" | jq -r .file | sort -u)
FILE_COUNT=$(echo "$FILES" | wc -l | tr -d ' ')

# Generate commit message
COMMIT_MSG=$(cat << EOF
session($SESSION_ID): $FILE_COUNT files modified

Changes:
$(echo "$FILES" | sed 's|'"$CLAUDE_DIR"'/||g' | sed 's/^/  - /')

Statistics:
$(git -C "$CLAUDE_DIR" diff --stat "$START_COMMIT" 2>/dev/null | tail -1 || echo "  (new session)")

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)

# Stage and commit
git -C "$CLAUDE_DIR" add -A
git -C "$CLAUDE_DIR" commit -m "$COMMIT_MSG" || echo "Nothing to commit"

# Merge to main
CURRENT_BRANCH=$(git -C "$CLAUDE_DIR" branch --show-current)
if [[ "$CURRENT_BRANCH" == session/* ]]; then
  git -C "$CLAUDE_DIR" checkout main
  git -C "$CLAUDE_DIR" merge --no-ff -m "Merge $CURRENT_BRANCH" "$CURRENT_BRANCH"
  git -C "$CLAUDE_DIR" branch -d "$CURRENT_BRANCH"
fi

# Cleanup
rm -f "$PENDING_FILE"
rm -f "$STATE_FILE"

# Push if remote configured
git -C "$CLAUDE_DIR" push origin main 2>/dev/null || true

echo "Session committed: $SESSION_ID ($FILE_COUNT files)"
