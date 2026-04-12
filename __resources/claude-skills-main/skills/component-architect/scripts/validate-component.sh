#!/bin/bash
# PreToolUse hook: Validate component before creation
# Part of component-architect skill

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // .tool_input.new_string // empty')

# Exit early if no file path
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Component type detection
case "$FILE_PATH" in
    */SKILL.md)
        COMPONENT_TYPE="skill"
        REQUIRED_FIELDS=("name" "description")
        OPTIONAL_FIELDS=("allowed-tools" "model" "context" "agent" "hooks" "user-invocable" "disable-model-invocation")
        ;;
    */agents/*.md|*/.claude/agents/*.md)
        COMPONENT_TYPE="agent"
        REQUIRED_FIELDS=("name" "description")
        OPTIONAL_FIELDS=("tools" "disallowedTools" "model" "permissionMode" "skills" "hooks")
        ;;
    */commands/*.md|*/.claude/commands/*.md)
        COMPONENT_TYPE="command"
        REQUIRED_FIELDS=()
        OPTIONAL_FIELDS=("description" "allowed-tools" "model" "argument-hint")
        ;;
    */hooks.json|*/hooks/hooks.json)
        COMPONENT_TYPE="hooks"
        # JSON validation would go here
        exit 0
        ;;
    *)
        # Not a component file, allow
        exit 0
        ;;
esac

# Check if content has frontmatter
if ! echo "$CONTENT" | head -1 | grep -q "^---$"; then
    echo "⚠️ No YAML frontmatter detected in ${COMPONENT_TYPE} file" >&2
    echo "   Add frontmatter with required fields: ${REQUIRED_FIELDS[*]}" >&2
    exit 0
fi

# Extract frontmatter (content between first two --- markers)
FRONTMATTER=$(echo "$CONTENT" | sed -n '/^---$/,/^---$/p' | tail -n +2 | head -n -1)

# Check required fields
MISSING_REQUIRED=()
for field in "${REQUIRED_FIELDS[@]}"; do
    if ! echo "$FRONTMATTER" | grep -qE "^${field}:"; then
        MISSING_REQUIRED+=("$field")
    fi
done

if [ ${#MISSING_REQUIRED[@]} -gt 0 ]; then
    echo "⚠️ Missing required field(s) in ${COMPONENT_TYPE} file: ${MISSING_REQUIRED[*]}" >&2
    echo "   See: https://code.claude.com/docs/en/${COMPONENT_TYPE}s" >&2
fi

# Check for non-official fields (warn only)
ALL_OFFICIAL=("${REQUIRED_FIELDS[@]}" "${OPTIONAL_FIELDS[@]}")
NON_OFFICIAL=()

# Extract field names from frontmatter
FIELDS=$(echo "$FRONTMATTER" | grep -E "^[a-zA-Z_-]+:" | sed 's/:.*$//')

for field in $FIELDS; do
    IS_OFFICIAL=false
    for official in "${ALL_OFFICIAL[@]}"; do
        if [ "$field" = "$official" ]; then
            IS_OFFICIAL=true
            break
        fi
    done
    if [ "$IS_OFFICIAL" = false ]; then
        NON_OFFICIAL+=("$field")
    fi
done

if [ ${#NON_OFFICIAL[@]} -gt 0 ]; then
    echo "ℹ️  Non-official frontmatter properties detected: ${NON_OFFICIAL[*]}" >&2
    echo "   Consider moving to markdown body for compatibility" >&2
fi

# Check for recommended architecture pattern (skills only)
if [ "$COMPONENT_TYPE" = "skill" ]; then
    if ! echo "$FRONTMATTER" | grep -qE "^context:\s*fork"; then
        echo "💡 Tip: Consider using 'context: fork' with a designated agent" >&2
        echo "   This enables the 'one skill = one agent' architecture pattern" >&2
    fi
fi

# Always exit 0 to allow the operation (we only warn, not block)
exit 0
