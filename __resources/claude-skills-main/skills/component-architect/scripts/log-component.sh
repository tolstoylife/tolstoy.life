#!/bin/bash
# PostToolUse hook: Log component creation/modification
# Part of component-architect skill

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# Exit early if no file path
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Only log component files
case "$FILE_PATH" in
    */SKILL.md|*/agents/*.md|*/commands/*.md|*/hooks.json|*/hooks/hooks.json)
        ;;
    *)
        exit 0
        ;;
esac

# Create log directory if needed
LOG_DIR="$HOME/.claude/.component-logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/component-activity.log"

# Determine component type
case "$FILE_PATH" in
    */SKILL.md) COMPONENT_TYPE="skill" ;;
    */agents/*.md) COMPONENT_TYPE="agent" ;;
    */commands/*.md) COMPONENT_TYPE="command" ;;
    */hooks.json|*/hooks/hooks.json) COMPONENT_TYPE="hooks" ;;
    *) COMPONENT_TYPE="unknown" ;;
esac

# Log the activity
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "${TIMESTAMP} | ${TOOL_NAME} | ${COMPONENT_TYPE} | ${FILE_PATH}" >> "$LOG_FILE"

# Keep log file manageable (last 1000 entries)
if [ -f "$LOG_FILE" ]; then
    tail -n 1000 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
fi

exit 0
