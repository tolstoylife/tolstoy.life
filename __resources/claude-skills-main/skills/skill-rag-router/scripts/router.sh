#!/bin/bash
# Main skill router logic using ck semantic search
# Usage: router.sh "query" [top_k] [threshold]

set -e

QUERY="$1"
TOP_K="${2:-5}"
THRESHOLD="${3:-0.6}"
SKILL_DIR="${HOME}/.claude/skills"
CK_BIN="${HOME}/.cargo/bin/ck"

if [ -z "$QUERY" ]; then
    echo "Usage: router.sh <query> [top_k] [threshold]" >&2
    exit 1
fi

# Check if ck is available
if [ ! -f "$CK_BIN" ]; then
    echo '{"error": "ck binary not found", "suggestions": []}'
    exit 0
fi

# Semantic search for matching skills
RESULTS=$("$CK_BIN" --sem "$QUERY" "$SKILL_DIR" \
    --jsonl \
    --top-k "$TOP_K" \
    2>/dev/null || echo "")

if [ -z "$RESULTS" ]; then
    echo '{"query": "'"$QUERY"'", "suggestions": []}'
    exit 0
fi

# Parse results and format as JSON
echo "$RESULTS" | jq -s '
    {
        query: "'"$QUERY"'",
        suggestions: map({
            skill: (.path | split("/") | .[-2]),
            path: .path,
            score: .score,
            line: .line
        }) | sort_by(-.score)
    }
'
