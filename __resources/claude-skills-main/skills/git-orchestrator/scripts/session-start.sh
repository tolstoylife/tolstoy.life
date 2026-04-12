#!/bin/bash
# Session Start Hook - Record initial git state

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
STATE_FILE="$CLAUDE_DIR/.git/session-state.json"

# Ensure repo is initialized
if [ ! -d "$CLAUDE_DIR/.git" ]; then
  "$CLAUDE_DIR/skills/git-orchestrator/scripts/init-repo.sh"
fi

# Record initial state
cat > "$STATE_FILE" << EOF
{
  "session_id": "$(date +%Y%m%d-%H%M%S)-$$",
  "start_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "start_commit": "$(git -C "$CLAUDE_DIR" rev-parse HEAD 2>/dev/null || echo 'initial')",
  "start_branch": "$(git -C "$CLAUDE_DIR" branch --show-current 2>/dev/null || echo 'main')",
  "pending_changes": []
}
EOF

# Create session branch
SESSION_BRANCH="session/$(date +%Y%m%d-%H%M%S)"
git -C "$CLAUDE_DIR" checkout -b "$SESSION_BRANCH" 2>/dev/null || true

echo "Session started: $(cat "$STATE_FILE" | jq -r .session_id 2>/dev/null || echo 'unknown')"
