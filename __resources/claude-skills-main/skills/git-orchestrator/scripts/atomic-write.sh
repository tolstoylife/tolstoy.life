#!/bin/bash
# Atomic Write - Safe file writes with temp → validate → rename pattern

set -euo pipefail

FILE_PATH="$1"
CONTENT="${2:-}"

if [ -z "$FILE_PATH" ]; then
  echo "Usage: atomic-write.sh <file_path> [content]"
  exit 1
fi

# Create temp file
TEMP_FILE="${FILE_PATH}.tmp.$$"

# Write content (from stdin if not provided)
if [ -n "$CONTENT" ]; then
  echo "$CONTENT" > "$TEMP_FILE"
else
  cat > "$TEMP_FILE"
fi

# Validate (basic checks)
if [ ! -s "$TEMP_FILE" ]; then
  echo "Error: Empty file generated"
  rm -f "$TEMP_FILE"
  exit 1
fi

# Atomic rename
mv "$TEMP_FILE" "$FILE_PATH"

echo "Atomic write successful: $FILE_PATH"
