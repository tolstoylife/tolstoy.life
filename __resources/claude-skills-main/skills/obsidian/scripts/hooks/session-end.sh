#!/bin/bash
# session-end.sh - Save Obsidian skill learnings at session end
#
# This hook runs at session end to:
# 1. Update last session timestamp
# 2. Capture any notable learnings
# 3. Clean up temporary data

set -euo pipefail

MEMORY_FILE="${CLAUDE_PROJECT_DIR:-.}/.claude/obsidian-memory.json"

# Exit if memory file doesn't exist
[ ! -f "$MEMORY_FILE" ] && exit 0

# Update last session timestamp
update_timestamp() {
    local now
    now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    if command -v jq &> /dev/null; then
        tmp=$(mktemp)
        jq --arg now "$now" '.lastUpdated = $now' "$MEMORY_FILE" > "$tmp" && mv "$tmp" "$MEMORY_FILE"
    fi
}

# Calculate session statistics
calculate_stats() {
    if command -v jq &> /dev/null; then
        local total_patterns session_count
        total_patterns=$(jq '[.patterns | .. | numbers] | add // 0' "$MEMORY_FILE" 2>/dev/null || echo "0")
        session_count=$(jq -r '.sessions.total' "$MEMORY_FILE" 2>/dev/null || echo "0")

        if [ "$total_patterns" -gt 0 ] && [ "$session_count" -gt 0 ]; then
            echo "[Obsidian Skill] Session complete. Total patterns tracked: $total_patterns across $session_count sessions."
        fi
    fi
}

# Prune old learnings (keep last 50)
prune_learnings() {
    if command -v jq &> /dev/null; then
        local learning_count
        learning_count=$(jq '.learnings | length' "$MEMORY_FILE" 2>/dev/null || echo "0")

        if [ "$learning_count" -gt 50 ]; then
            tmp=$(mktemp)
            jq '.learnings = .learnings[-50:]' "$MEMORY_FILE" > "$tmp" && mv "$tmp" "$MEMORY_FILE"
        fi
    fi
}

# Derive user preferences from patterns
derive_preferences() {
    if command -v jq &> /dev/null; then
        # Find most used patterns per category
        tmp=$(mktemp)
        jq '
        # Get top markdown patterns
        .userPreferences.topMarkdownPatterns = [
            .patterns.markdown | to_entries | sort_by(-.value) | .[0:3] | .[].key
        ] |
        # Get top bases patterns
        .userPreferences.topBasesPatterns = [
            .patterns.bases | to_entries | sort_by(-.value) | .[0:3] | .[].key
        ] |
        # Get top canvas patterns
        .userPreferences.topCanvasPatterns = [
            .patterns.canvas | to_entries | sort_by(-.value) | .[0:3] | .[].key
        ]
        ' "$MEMORY_FILE" > "$tmp" && mv "$tmp" "$MEMORY_FILE"
    fi
}

# Main execution
main() {
    update_timestamp
    derive_preferences
    prune_learnings
    calculate_stats
}

main
