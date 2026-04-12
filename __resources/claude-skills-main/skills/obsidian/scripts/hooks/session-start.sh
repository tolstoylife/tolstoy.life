#!/bin/bash
# session-start.sh - Load Obsidian skill memory and detect vault context
#
# This hook runs at session start to:
# 1. Detect if we're in an Obsidian vault (look for .obsidian directory)
# 2. Load skill memory from persistent storage
# 3. Set environment variables for the session

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MEMORY_FILE="${CLAUDE_PROJECT_DIR:-.}/.claude/obsidian-memory.json"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$SCRIPT_DIR/../..}"

# Initialize memory file if it doesn't exist
init_memory() {
    local memory_dir
    memory_dir="$(dirname "$MEMORY_FILE")"

    if [ ! -d "$memory_dir" ]; then
        mkdir -p "$memory_dir"
    fi

    if [ ! -f "$MEMORY_FILE" ]; then
        cat > "$MEMORY_FILE" << 'EOF'
{
  "version": "1.0.0",
  "created": null,
  "lastUpdated": null,
  "sessions": {
    "total": 0,
    "lastSessionDate": null
  },
  "patterns": {
    "markdown": {
      "wikilinks": 0,
      "callouts": 0,
      "embeds": 0,
      "properties": 0,
      "tags": 0
    },
    "bases": {
      "filters": 0,
      "formulas": 0,
      "views": 0,
      "summaries": 0
    },
    "canvas": {
      "textNodes": 0,
      "fileNodes": 0,
      "linkNodes": 0,
      "groupNodes": 0,
      "edges": 0
    }
  },
  "userPreferences": {
    "preferredCalloutTypes": [],
    "commonProperties": [],
    "frequentFilters": [],
    "favoriteColors": []
  },
  "learnings": [],
  "vaultContext": {
    "hasVault": false,
    "pluginsDetected": []
  }
}
EOF
        # Set creation timestamp
        local now
        now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        if command -v jq &> /dev/null; then
            tmp=$(mktemp)
            jq --arg now "$now" '.created = $now | .lastUpdated = $now' "$MEMORY_FILE" > "$tmp" && mv "$tmp" "$MEMORY_FILE"
        fi
    fi
}

# Detect Obsidian vault
detect_vault() {
    local has_vault="false"
    local plugins_detected="[]"

    # Check for .obsidian directory
    if [ -d "${CLAUDE_PROJECT_DIR:-.}/.obsidian" ]; then
        has_vault="true"

        # Detect common plugins
        local obsidian_dir="${CLAUDE_PROJECT_DIR:-.}/.obsidian"
        local plugins=()

        [ -d "$obsidian_dir/plugins/dataview" ] && plugins+=("dataview")
        [ -d "$obsidian_dir/plugins/templater-obsidian" ] && plugins+=("templater")
        [ -d "$obsidian_dir/plugins/obsidian-kanban" ] && plugins+=("kanban")
        [ -d "$obsidian_dir/plugins/breadcrumbs" ] && plugins+=("breadcrumbs")
        [ -d "$obsidian_dir/plugins/graph-analysis" ] && plugins+=("graph-analysis")

        if [ ${#plugins[@]} -gt 0 ]; then
            plugins_detected=$(printf '%s\n' "${plugins[@]}" | jq -R . | jq -s .)
        fi

        echo "export OBSIDIAN_VAULT_DETECTED=true" >> "$CLAUDE_ENV_FILE"
    fi

    # Update memory with vault context
    if command -v jq &> /dev/null && [ -f "$MEMORY_FILE" ]; then
        tmp=$(mktemp)
        jq --argjson vault "$has_vault" --argjson plugins "$plugins_detected" \
           '.vaultContext.hasVault = $vault | .vaultContext.pluginsDetected = $plugins' \
           "$MEMORY_FILE" > "$tmp" && mv "$tmp" "$MEMORY_FILE"
    fi
}

# Update session counter
update_session_count() {
    if command -v jq &> /dev/null && [ -f "$MEMORY_FILE" ]; then
        local now
        now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        tmp=$(mktemp)
        jq --arg now "$now" '.sessions.total += 1 | .sessions.lastSessionDate = $now | .lastUpdated = $now' \
           "$MEMORY_FILE" > "$tmp" && mv "$tmp" "$MEMORY_FILE"
    fi
}

# Generate context message
generate_context() {
    local context=""

    if [ -f "$MEMORY_FILE" ] && command -v jq &> /dev/null; then
        local sessions total_patterns has_vault
        sessions=$(jq -r '.sessions.total' "$MEMORY_FILE" 2>/dev/null || echo "0")
        has_vault=$(jq -r '.vaultContext.hasVault' "$MEMORY_FILE" 2>/dev/null || echo "false")

        # Count total pattern usage
        total_patterns=$(jq '[.patterns | .. | numbers] | add // 0' "$MEMORY_FILE" 2>/dev/null || echo "0")

        if [ "$sessions" -gt 1 ]; then
            context="[Obsidian Skill Memory] Session #$sessions | Total patterns used: $total_patterns"

            # Add vault status
            if [ "$has_vault" = "true" ]; then
                local plugins
                plugins=$(jq -r '.vaultContext.pluginsDetected | join(", ")' "$MEMORY_FILE" 2>/dev/null || echo "")
                context="$context | Vault detected"
                [ -n "$plugins" ] && context="$context (plugins: $plugins)"
            fi

            # Get top used patterns
            local top_markdown top_bases top_canvas
            top_markdown=$(jq -r '[.patterns.markdown | to_entries | sort_by(-.value) | .[0:2] | .[].key] | join(", ")' "$MEMORY_FILE" 2>/dev/null || echo "")
            top_bases=$(jq -r '[.patterns.bases | to_entries | sort_by(-.value) | .[0:2] | .[].key] | join(", ")' "$MEMORY_FILE" 2>/dev/null || echo "")
            top_canvas=$(jq -r '[.patterns.canvas | to_entries | sort_by(-.value) | .[0:2] | .[].key] | join(", ")' "$MEMORY_FILE" 2>/dev/null || echo "")

            local favorites=""
            [ -n "$top_markdown" ] && favorites="md:$top_markdown"
            [ -n "$top_bases" ] && favorites="$favorites base:$top_bases"
            [ -n "$top_canvas" ] && favorites="$favorites canvas:$top_canvas"
            [ -n "$favorites" ] && context="$context | Frequent:$favorites"
        fi
    fi

    [ -n "$context" ] && echo "$context"
}

# Main execution
main() {
    init_memory
    detect_vault
    update_session_count

    # Generate and output context
    context=$(generate_context)
    if [ -n "$context" ]; then
        echo "$context"
    fi
}

main
