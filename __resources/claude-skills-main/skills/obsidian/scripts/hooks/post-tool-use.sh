#!/bin/bash
# post-tool-use.sh - Track Obsidian pattern usage after Write/Edit operations
#
# This hook runs after Write/Edit tools to:
# 1. Detect if an Obsidian file was modified (.md, .base, .canvas)
# 2. Analyze content for Obsidian patterns
# 3. Update usage statistics in skill memory

set -euo pipefail

MEMORY_FILE="${CLAUDE_PROJECT_DIR:-.}/.claude/obsidian-memory.json"

# Read hook input from stdin
input=$(cat)

# Extract file path from tool input
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

# Exit if no file path or memory file doesn't exist
[ -z "$file_path" ] && exit 0
[ ! -f "$MEMORY_FILE" ] && exit 0

# Determine file type
case "$file_path" in
    *.md)
        file_type="markdown"
        ;;
    *.base)
        file_type="bases"
        ;;
    *.canvas)
        file_type="canvas"
        ;;
    *)
        exit 0  # Not an Obsidian file
        ;;
esac

# Extract content for analysis
content=$(echo "$input" | jq -r '.tool_input.content // empty' 2>/dev/null)
[ -z "$content" ] && exit 0

# Track patterns based on file type
track_markdown_patterns() {
    local patterns=""

    # Wikilinks [[...]]
    if echo "$content" | grep -qE '\[\[[^\]]+\]\]'; then
        patterns="$patterns wikilinks"
    fi

    # Embeds ![[...]]
    if echo "$content" | grep -qE '!\[\[[^\]]+\]\]'; then
        patterns="$patterns embeds"
    fi

    # Callouts > [!type]
    if echo "$content" | grep -qE '>\s*\[!'; then
        patterns="$patterns callouts"
    fi

    # Properties/Frontmatter ---
    if echo "$content" | grep -qE '^---'; then
        patterns="$patterns properties"
    fi

    # Tags #tag
    if echo "$content" | grep -qE '#[a-zA-Z][a-zA-Z0-9_/-]*'; then
        patterns="$patterns tags"
    fi

    echo "$patterns"
}

track_bases_patterns() {
    local patterns=""

    # Filters
    if echo "$content" | grep -qE 'filters:|file\.hasTag|file\.inFolder'; then
        patterns="$patterns filters"
    fi

    # Formulas
    if echo "$content" | grep -qE 'formulas:|formula\.'; then
        patterns="$patterns formulas"
    fi

    # Views
    if echo "$content" | grep -qE 'views:|type:\s*(table|cards|list|map)'; then
        patterns="$patterns views"
    fi

    # Summaries
    if echo "$content" | grep -qE 'summaries:'; then
        patterns="$patterns summaries"
    fi

    echo "$patterns"
}

track_canvas_patterns() {
    local patterns=""

    # Text nodes
    if echo "$content" | grep -qE '"type"\s*:\s*"text"'; then
        patterns="$patterns textNodes"
    fi

    # File nodes
    if echo "$content" | grep -qE '"type"\s*:\s*"file"'; then
        patterns="$patterns fileNodes"
    fi

    # Link nodes
    if echo "$content" | grep -qE '"type"\s*:\s*"link"'; then
        patterns="$patterns linkNodes"
    fi

    # Group nodes
    if echo "$content" | grep -qE '"type"\s*:\s*"group"'; then
        patterns="$patterns groupNodes"
    fi

    # Edges
    if echo "$content" | grep -qE '"edges"\s*:\s*\[' && echo "$content" | grep -qE '"fromNode"'; then
        patterns="$patterns edges"
    fi

    echo "$patterns"
}

# Update memory with pattern counts
update_memory() {
    local file_type="$1"
    local patterns="$2"

    [ -z "$patterns" ] && return

    # Build jq expression to increment counters
    local jq_expr=".lastUpdated = \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\""

    for pattern in $patterns; do
        jq_expr="$jq_expr | .patterns.$file_type.$pattern += 1"
    done

    # Update memory file atomically
    tmp=$(mktemp)
    if jq "$jq_expr" "$MEMORY_FILE" > "$tmp" 2>/dev/null; then
        mv "$tmp" "$MEMORY_FILE"
    else
        rm -f "$tmp"
    fi
}

# Main execution
main() {
    local patterns=""

    case "$file_type" in
        markdown)
            patterns=$(track_markdown_patterns)
            ;;
        bases)
            patterns=$(track_bases_patterns)
            ;;
        canvas)
            patterns=$(track_canvas_patterns)
            ;;
    esac

    if [ -n "$patterns" ]; then
        update_memory "$file_type" "$patterns"
        # Provide feedback (optional, can be suppressed)
        # echo "[Obsidian] Tracked patterns: $patterns"
    fi
}

main
