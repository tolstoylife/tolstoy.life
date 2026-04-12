#!/bin/bash
# Worktree Manager - Create, list, switch, cleanup worktrees

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
WORKTREE_BASE="$HOME/.claude-worktrees"
ACTION="${1:-list}"
NAME="${2:-}"

case "$ACTION" in
  create)
    if [ -z "$NAME" ]; then
      echo "Usage: worktree-manager.sh create <name>"
      exit 1
    fi
    WORKTREE_PATH="$WORKTREE_BASE/$NAME"
    BRANCH_NAME="worktree/$NAME"

    mkdir -p "$WORKTREE_BASE"
    git -C "$CLAUDE_DIR" worktree add -b "$BRANCH_NAME" "$WORKTREE_PATH"
    bd add "Worktree created: $NAME" --tags experiment 2>/dev/null || true

    echo "Created worktree at $WORKTREE_PATH"
    echo "Branch: $BRANCH_NAME"
    ;;

  list)
    git -C "$CLAUDE_DIR" worktree list
    ;;

  switch)
    if [ -z "$NAME" ]; then
      echo "Usage: worktree-manager.sh switch <name>"
      exit 1
    fi
    WORKTREE_PATH="$WORKTREE_BASE/$NAME"

    if [ -d "$WORKTREE_PATH" ]; then
      echo "CLAUDE_DIR=$WORKTREE_PATH"
      echo "To use: export CLAUDE_DIR=$WORKTREE_PATH"
    else
      echo "Worktree not found: $NAME"
      exit 1
    fi
    ;;

  cleanup)
    # Remove worktrees older than 7 days
    if [ -d "$WORKTREE_BASE" ]; then
      find "$WORKTREE_BASE" -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \;
    fi
    git -C "$CLAUDE_DIR" worktree prune
    echo "Cleaned up stale worktrees"
    ;;

  remove)
    if [ -z "$NAME" ]; then
      echo "Usage: worktree-manager.sh remove <name>"
      exit 1
    fi
    WORKTREE_PATH="$WORKTREE_BASE/$NAME"
    BRANCH_NAME="worktree/$NAME"

    git -C "$CLAUDE_DIR" worktree remove "$WORKTREE_PATH" 2>/dev/null || rm -rf "$WORKTREE_PATH"
    git -C "$CLAUDE_DIR" branch -D "$BRANCH_NAME" 2>/dev/null || true

    echo "Removed worktree: $NAME"
    ;;

  *)
    echo "Usage: worktree-manager.sh {create|list|switch|cleanup|remove} [name]"
    exit 1
    ;;
esac
