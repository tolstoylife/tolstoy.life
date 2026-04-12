#!/bin/bash
# Lock Manager - Detect and fix stale git locks

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
LOCK_FILE="$CLAUDE_DIR/.git/index.lock"
MAX_AGE_SECONDS=300  # 5 minutes

if [ ! -f "$LOCK_FILE" ]; then
  echo "No lock file found"
  exit 0
fi

# Get lock file age
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS
  LOCK_AGE=$(($(date +%s) - $(stat -f %m "$LOCK_FILE")))
else
  # Linux
  LOCK_AGE=$(($(date +%s) - $(stat -c %Y "$LOCK_FILE")))
fi

if [ $LOCK_AGE -gt $MAX_AGE_SECONDS ]; then
  echo "Removing stale lock (age: ${LOCK_AGE}s > ${MAX_AGE_SECONDS}s)"
  rm -f "$LOCK_FILE"
  echo "Stale lock removed"
else
  echo "Lock is recent (age: ${LOCK_AGE}s), not removing"
  exit 1
fi
