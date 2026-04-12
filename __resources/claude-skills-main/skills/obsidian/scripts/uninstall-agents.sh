#!/bin/bash
# Uninstall Obsidian specialized agents from global agents directory

set -e

GLOBAL_AGENTS_DIR="$HOME/.claude/agents"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🗑️  Obsidian Skill - Agent Uninstallation"
echo "=========================================="
echo ""

# List of agents to uninstall
AGENTS=(
    "obsidian-file-agent.md"
    "obsidian-markdown.md"
    "obsidian-bases.md"
    "obsidian-canvas.md"
)

echo "Removing agents from: $GLOBAL_AGENTS_DIR"
echo ""

# Uninstall each agent
removed=0
skipped=0
for agent in "${AGENTS[@]}"; do
    target_file="$GLOBAL_AGENTS_DIR/$agent"

    if [ -e "$target_file" ]; then
        rm "$target_file"
        echo -e "${GREEN}✓${NC} Removed: $agent"
        ((removed++))
    else
        echo -e "${YELLOW}⚠${NC} Not found: $agent"
        ((skipped++))
    fi
done

echo ""
echo "=========================================="
echo -e "Removed: ${GREEN}$removed${NC} agents"
echo -e "Not found: ${YELLOW}$skipped${NC}"
echo ""

if [ "$removed" -gt 0 ]; then
    echo -e "${GREEN}Agents uninstalled successfully!${NC}"
    echo ""
    echo "The obsidian skill will now use the default general-purpose agent."
    echo "To reinstall agents, run: ./scripts/install-agents.sh"
else
    echo -e "${YELLOW}No agents were installed.${NC}"
fi
