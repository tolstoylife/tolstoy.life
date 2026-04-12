#!/bin/bash
# Initialize ~/.claude as git repository (idempotent)

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"

# Already initialized?
if [ -d "$CLAUDE_DIR/.git" ]; then
  echo "Repository already initialized at $CLAUDE_DIR"
  exit 0
fi

cd "$CLAUDE_DIR"

# Initialize
git init --initial-branch=main

# Create comprehensive .gitignore
cat > .gitignore << 'EOF'
# Session state (transient)
.git/session-state.json
.git/pending-changes.jsonl

# Secrets and credentials
*.secret
*.key
*.pem
secrets/
credentials/

# API tokens in settings
settings.local.json

# Cache directories
.cache/
plugins/cache/

# Large binary files
*.db
*.sqlite
*.fdb

# OS files
.DS_Store
Thumbs.db

# Editor files
*.swp
*.swo
*~

# Worktree state (managed separately)
../.claude-worktrees/
EOF

# Initial commit
git add -A
git commit -m "$(cat << 'EOF'
init: Initialize ~/.claude as version-controlled repository

This repository contains Claude Code configuration including:
- Skills (SKILL.md files)
- Agents (agent definitions)
- Commands (slash commands)
- Hooks (lifecycle hooks)
- Rules (core rules)
- Settings (non-secret configuration)

Managed by git-orchestrator meta-skill.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"

# Create main branches
git checkout -b develop
git checkout main

echo "Repository initialized at $CLAUDE_DIR"
echo "Branches: main (stable), develop (active)"
