#!/bin/bash
# Install Obsidian specialized agents to global agents directory

set -e

# Get the script directory (skill root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENTS_DIR="$SCRIPT_DIR/agents"
GLOBAL_AGENTS_DIR="$HOME/.claude/agents"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔧 Obsidian Skill - Agent Installation"
echo "======================================"
echo ""

# Check if agents directory exists
if [ ! -d "$AGENTS_DIR" ]; then
    echo -e "${RED}Error: Agents directory not found at $AGENTS_DIR${NC}"
    exit 1
fi

# Create global agents directory if it doesn't exist
if [ ! -d "$GLOBAL_AGENTS_DIR" ]; then
    echo "Creating global agents directory: $GLOBAL_AGENTS_DIR"
    mkdir -p "$GLOBAL_AGENTS_DIR"
fi

# List of agents to install
AGENTS=(
    "obsidian-file-agent.md"
    "obsidian-markdown.md"
    "obsidian-bases.md"
    "obsidian-canvas.md"
)

echo "Installing agents to: $GLOBAL_AGENTS_DIR"
echo ""

# Install each agent
installed=0
skipped=0
for agent in "${AGENTS[@]}"; do
    source_file="$AGENTS_DIR/$agent"
    target_file="$GLOBAL_AGENTS_DIR/$agent"

    if [ ! -f "$source_file" ]; then
        echo -e "${YELLOW}⚠ Agent not found: $agent${NC}"
        continue
    fi

    # Check if target already exists
    if [ -e "$target_file" ]; then
        if [ -L "$target_file" ]; then
            # It's a symlink, check if it points to our file
            existing_target="$(readlink "$target_file")"
            if [ "$existing_target" = "$source_file" ]; then
                echo -e "${GREEN}✓${NC} $agent (already linked)"
                ((skipped++))
                continue
            fi
        fi
        # Different file exists, back it up
        echo -e "${YELLOW}⚠ Backing up existing: $agent → $agent.backup${NC}"
        mv "$target_file" "$target_file.backup"
    fi

    # Create symlink
    ln -s "$source_file" "$target_file"
    echo -e "${GREEN}✓${NC} $agent (installed)"
    ((installed++))
done

echo ""
echo "======================================"
echo -e "Installed: ${GREEN}$installed${NC} agents"
echo -e "Skipped:   ${YELLOW}$skipped${NC} (already installed)"
echo ""

# Verify installation
echo "Verifying installation..."
all_good=true
for agent in "${AGENTS[@]}"; do
    target_file="$GLOBAL_AGENTS_DIR/$agent"
    if [ -L "$target_file" ] && [ -f "$target_file" ]; then
        echo -e "  ${GREEN}✓${NC} $agent"
    else
        echo -e "  ${RED}✗${NC} $agent"
        all_good=false
    fi
done

echo ""
if [ "$all_good" = true ]; then
    echo -e "${GREEN}All agents installed successfully!${NC}"
    echo ""
    echo "The obsidian skill will now use the specialized agents."
    echo "Default agent: obsidian-file-agent (master agent for all file types)"
else
    echo -e "${RED}Some agents failed to install. Please check the errors above.${NC}"
    exit 1
fi
