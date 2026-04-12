#!/bin/bash
# Test the Obsidian skill implementation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}🧪 Obsidian Skill Test Suite${NC}"
echo "================================"
echo ""

tests_passed=0
tests_failed=0

# Test function
test_check() {
    local name="$1"
    local condition="$2"

    if eval "$condition"; then
        echo -e "${GREEN}✓${NC} $name"
        tests_passed=$((tests_passed + 1))
    else
        echo -e "${RED}✗${NC} $name"
        tests_failed=$((tests_failed + 1))
    fi
}

# 1. SKILL.md Structure Tests
echo -e "${YELLOW}1. SKILL.md Frontmatter Tests${NC}"

test_check "Has name field" \
    "grep -q '^name: obsidian$' '$SCRIPT_DIR/SKILL.md'"

test_check "Has description field" \
    "grep -q '^description:' '$SCRIPT_DIR/SKILL.md'"

test_check "Has context: fork" \
    "grep -q '^context: fork$' '$SCRIPT_DIR/SKILL.md'"

test_check "Has agent: obsidian-file-agent" \
    "grep -q '^agent: obsidian-file-agent$' '$SCRIPT_DIR/SKILL.md'"

test_check "Has model: sonnet" \
    "grep -q '^model: sonnet$' '$SCRIPT_DIR/SKILL.md'"

test_check "Has user-invocable: true" \
    "grep -q '^user-invocable: true$' '$SCRIPT_DIR/SKILL.md'"

test_check "Has hooks configuration" \
    "grep -q '^hooks:$' '$SCRIPT_DIR/SKILL.md'"

test_check "Has allowed-tools list" \
    "grep -q '^allowed-tools:$' '$SCRIPT_DIR/SKILL.md'"

test_check "Has Directory Index in body (for head -100 discovery)" \
    "grep -q '^## Directory Index' '$SCRIPT_DIR/SKILL.md'"

echo ""

# 2. Agent Tests
echo -e "${YELLOW}2. Specialized Agents Tests${NC}"

test_check "obsidian-file-agent.md exists" \
    "[ -f '$SCRIPT_DIR/agents/obsidian-file-agent.md' ]"

test_check "obsidian-markdown.md exists" \
    "[ -f '$SCRIPT_DIR/agents/obsidian-markdown.md' ]"

test_check "obsidian-bases.md exists" \
    "[ -f '$SCRIPT_DIR/agents/obsidian-bases.md' ]"

test_check "obsidian-canvas.md exists" \
    "[ -f '$SCRIPT_DIR/agents/obsidian-canvas.md' ]"

test_check "Agents installed globally" \
    "ls ~/.claude/agents/obsidian-*.md >/dev/null 2>&1"

# Check agent frontmatter
test_check "File agent has skills: obsidian" \
    "grep -q '^skills: obsidian$' '$SCRIPT_DIR/agents/obsidian-file-agent.md'"

test_check "File agent has model: sonnet" \
    "grep -q '^model: sonnet$' '$SCRIPT_DIR/agents/obsidian-file-agent.md'"

test_check "File agent has permissions" \
    "grep -q '^permissions:$' '$SCRIPT_DIR/agents/obsidian-file-agent.md'"

echo ""

# 3. Sub-skill Tests
echo -e "${YELLOW}3. Sub-skill Tests${NC}"

test_check "Markdown sub-skill has Directory Index in body" \
    "grep -q '^## Directory Index' '$SCRIPT_DIR/markdown/obsidian-markdown.md'"

test_check "Bases sub-skill has Directory Index in body" \
    "grep -q '^## Directory Index' '$SCRIPT_DIR/bases/obsidian-bases.md'"

test_check "Canvas sub-skill has Directory Index in body" \
    "grep -q '^## Directory Index' '$SCRIPT_DIR/canvas/obsidian-canvas.md'"

echo ""

# 4. Hook Tests
echo -e "${YELLOW}4. Hooks Tests${NC}"

test_check "session-start.sh exists and executable" \
    "[ -x '$SCRIPT_DIR/scripts/hooks/session-start.sh' ]"

test_check "post-tool-use.sh exists and executable" \
    "[ -x '$SCRIPT_DIR/scripts/hooks/post-tool-use.sh' ]"

test_check "session-end.sh exists and executable" \
    "[ -x '$SCRIPT_DIR/scripts/hooks/session-end.sh' ]"

test_check "memory-manager.py exists" \
    "[ -f '$SCRIPT_DIR/scripts/hooks/memory-manager.py' ]"

test_check "hooks.json exists" \
    "[ -f '$SCRIPT_DIR/hooks/hooks.json' ]"

echo ""

# 5. Memory System Tests
echo -e "${YELLOW}5. Memory System Tests${NC}"

test_check "Memory file initialized" \
    "[ -f '$SCRIPT_DIR/.claude/obsidian-memory.json' ]"

test_check "Memory has valid JSON structure" \
    "python3 -c \"import json; json.load(open('$SCRIPT_DIR/.claude/obsidian-memory.json'))\""

echo ""

# 6. Validation Scripts
echo -e "${YELLOW}6. Validation Scripts Tests${NC}"

test_check "validate-all.sh executable" \
    "[ -x '$SCRIPT_DIR/scripts/validate-all.sh' ]"

test_check "validate-canvas.sh executable" \
    "[ -x '$SCRIPT_DIR/scripts/validate-canvas.sh' ]"

test_check "validate-base.sh executable" \
    "[ -x '$SCRIPT_DIR/scripts/validate-base.sh' ]"

test_check "install-agents.sh executable" \
    "[ -x '$SCRIPT_DIR/scripts/install-agents.sh' ]"

test_check "uninstall-agents.sh executable" \
    "[ -x '$SCRIPT_DIR/scripts/uninstall-agents.sh' ]"

echo ""

# Summary
echo "================================"
total=$((tests_passed + tests_failed))
echo -e "Tests: ${GREEN}$tests_passed passed${NC}, ${RED}$tests_failed failed${NC} (total: $total)"

if [ $tests_failed -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ All tests passed! Skill implementation is complete.${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Some tests failed. Please review the output above.${NC}"
    exit 1
fi
