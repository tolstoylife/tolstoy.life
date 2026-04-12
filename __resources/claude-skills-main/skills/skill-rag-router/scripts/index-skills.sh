#!/bin/bash
# Index all skills for semantic search using ck
# Run on SessionStart to ensure index is current

set -e

SKILL_DIR="${HOME}/.claude/skills"
INDEX_DIR="${HOME}/.claude/.skill-index"
CK_BIN="${HOME}/.cargo/bin/ck"

# Ensure index directory exists
mkdir -p "$INDEX_DIR/cache"

# Check if ck is available
if [ ! -f "$CK_BIN" ]; then
    echo "[WARN] ck binary not found at $CK_BIN, skipping skill indexing" >&2
    exit 0
fi

# Build/update ck semantic index
# ck handles delta indexing automatically
"$CK_BIN" --sem "init" "$SKILL_DIR" --quiet >/dev/null 2>&1 || true

# Extract metadata from SKILL.md files for fast lookup
METADATA_FILE="$INDEX_DIR/cache/skill-metadata.jsonl"
: > "$METADATA_FILE"  # Clear file

find "$SKILL_DIR" -name "SKILL.md" -type f 2>/dev/null | while read -r skill_path; do
    skill_name=$(dirname "$skill_path" | xargs basename)

    # Extract description from frontmatter
    description=$(sed -n '/^---$/,/^---$/p' "$skill_path" | grep -E '^description:' | sed 's/^description:[[:space:]]*//' | tr -d '"' | head -c 200)

    # Extract location (user or plugin)
    if echo "$skill_path" | grep -q "plugins"; then
        location="plugin"
    else
        location="user"
    fi

    echo "{\"name\":\"$skill_name\",\"path\":\"$skill_path\",\"location\":\"$location\",\"description\":\"$description\"}" >> "$METADATA_FILE"
done

skill_count=$(wc -l < "$METADATA_FILE" | tr -d ' ')
echo "[INFO] Indexed $skill_count skills" >&2
