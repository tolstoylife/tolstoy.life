#!/bin/bash
# Secret Scanner - Pre-commit validation for secrets

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"

# Patterns to detect (extended regex)
PATTERNS=(
  'sk-[a-zA-Z0-9]{32,}'                     # API keys
  'AKIA[A-Z0-9]{16}'                        # AWS keys
  'password\s*=\s*["\'"'"'][^"'"'"']+["\'"'"']'  # Passwords
  'api[_-]?key\s*=\s*["\'"'"'][^"'"'"']+["\'"'"']'  # Generic API keys
  'secret\s*=\s*["\'"'"'][^"'"'"']+["\'"'"']'       # Generic secrets
  'token\s*=\s*["\'"'"'][^"'"'"']+["\'"'"']'        # Tokens
)

# Get staged files
STAGED_FILES=$(git -C "$CLAUDE_DIR" diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
  echo "No staged files to scan"
  exit 0
fi

VIOLATIONS=()

# Scan each staged file
while IFS= read -r file; do
  FILE_PATH="$CLAUDE_DIR/$file"

  # Skip binary files
  if file "$FILE_PATH" | grep -q "text"; then
    for pattern in "${PATTERNS[@]}"; do
      if grep -E "$pattern" "$FILE_PATH" >/dev/null 2>&1; then
        VIOLATIONS+=("$file: Potential secret detected (pattern: $pattern)")
      fi
    done
  fi
done <<< "$STAGED_FILES"

if [ ${#VIOLATIONS[@]} -gt 0 ]; then
  echo "⚠️  SECRET SCANNER VIOLATIONS:"
  for violation in "${VIOLATIONS[@]}"; do
    echo "  - $violation"
  done
  echo ""
  echo "Remediation: Remove secrets or add to .gitignore"
  exit 1
fi

echo "✓ No secrets detected in staged files"
exit 0
