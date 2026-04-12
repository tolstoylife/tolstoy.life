#!/bin/bash
# Skill suggestion script for UserPromptSubmit hook
# Analyzes user prompt and returns skill suggestions for system prompt injection
# Usage: suggest-skills.sh

set -e

SKILL_DIR="${HOME}/.claude/skills"
CK_BIN="${HOME}/.cargo/bin/ck"
THRESHOLD="0.65"
TOP_K="3"

# Read prompt from stdin or arguments
if [ -n "$1" ]; then
    PROMPT="$1"
else
    PROMPT=$(cat)
fi

# Skip if no prompt or too short
if [ -z "$PROMPT" ] || [ ${#PROMPT} -lt 20 ]; then
    exit 0
fi

# Skip if explicit skill request (let direct invocation handle it)
if echo "$PROMPT" | grep -qiE '^/[a-z]|use skill|run skill|invoke skill'; then
    exit 0
fi

# Calculate simple complexity score
WORD_COUNT=$(echo "$PROMPT" | wc -w | tr -d ' ')
HAS_MULTI_STEP=$(echo "$PROMPT" | grep -cE 'then|after|first|next|finally|step' || echo 0)

# Only suggest for complex-ish prompts
if [ "$WORD_COUNT" -lt 10 ] && [ "$HAS_MULTI_STEP" -eq 0 ]; then
    exit 0
fi

# Check if ck is available
if [ ! -f "$CK_BIN" ]; then
    exit 0
fi

# Semantic search for matching skills
RESULTS=$("$CK_BIN" --sem "$PROMPT" "$SKILL_DIR" \
    --jsonl \
    --top-k "$TOP_K" \
    --threshold "$THRESHOLD" \
    2>/dev/null || echo "")

if [ -z "$RESULTS" ]; then
    exit 0
fi

# Parse results and format for system prompt
SUGGESTIONS=$(echo "$RESULTS" | head -3 | jq -rs '
    map({
        skill: (.path | split("/") | .[-2]),
        score: (.score * 100 | floor)
    }) |
    map("- **\(.skill)** (\(.score)% match)") |
    join("\n")
')

if [ -n "$SUGGESTIONS" ]; then
    cat << EOF
## Skill Suggestions

Based on your prompt, these skills may help:
$SUGGESTIONS

Invoke with: \`/skill-name\` or include in your request.
EOF
fi
