#!/bin/bash
# Install code governance hooks globally
#
# Usage:
#   bash ~/.claude/skills/code/scripts/install-hooks.sh
#
# This copies hookify rules from the skill's hooks/ directory
# to ~/.claude/ where they will be active globally.

set -e

HOOKS_DIR="$HOME/.claude"
SKILL_DIR="$HOME/.claude/skills/code/hooks"

echo "=== Code Governance Hooks Installer ==="
echo ""

# Ensure directories exist
mkdir -p "$HOOKS_DIR"

if [ ! -d "$SKILL_DIR" ]; then
    echo "Error: Skill hooks directory not found: $SKILL_DIR"
    exit 1
fi

# Count hooks to install
HOOK_COUNT=$(ls -1 "$SKILL_DIR"/*.local.md 2>/dev/null | wc -l)

if [ "$HOOK_COUNT" -eq 0 ]; then
    echo "No hooks found in $SKILL_DIR"
    exit 0
fi

echo "Installing $HOOK_COUNT hooks..."
echo ""

# Copy hook templates to global location
for hook in "$SKILL_DIR"/*.local.md; do
    if [ -f "$hook" ]; then
        cp "$hook" "$HOOKS_DIR/"
        echo "  Installed: $(basename "$hook")"
    fi
done

echo ""
echo "Hooks installed to: $HOOKS_DIR"
echo ""
echo "To verify installation:"
echo "  ls ~/.claude/hookify.*.local.md"
echo ""
echo "To disable a hook:"
echo "  Edit the file and set 'enabled: false'"
echo ""
echo "Code governance hooks installed"
