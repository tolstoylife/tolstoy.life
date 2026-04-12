#!/bin/bash
# validate-canvas.sh - Validates .canvas files are valid JSON with Canvas structure
#
# Usage: ./validate-canvas.sh file1.canvas file2.canvas ...
#        ./validate-canvas.sh ../canvas/examples/*.canvas

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

if [ $# -eq 0 ]; then
    echo "Usage: $0 <canvas-files...>"
    echo "Example: $0 ../canvas/examples/*.canvas"
    exit 1
fi

errors=0
total=0

for f in "$@"; do
    total=$((total + 1))

    if [ ! -f "$f" ]; then
        echo -e "${RED}✗${NC} $f (file not found)"
        errors=$((errors + 1))
        continue
    fi

    # Check valid JSON
    if ! jq -e . "$f" > /dev/null 2>&1; then
        echo -e "${RED}✗${NC} $f (invalid JSON)"
        errors=$((errors + 1))
        continue
    fi

    # Check Canvas structure (nodes and edges arrays exist)
    if ! jq -e 'has("nodes") and has("edges")' "$f" > /dev/null 2>&1; then
        echo -e "${RED}✗${NC} $f (missing nodes or edges array)"
        errors=$((errors + 1))
        continue
    fi

    # Check node structure
    invalid_nodes=$(jq '[.nodes[] | select(.id == null or .type == null or .x == null or .y == null)] | length' "$f" 2>/dev/null || echo "1")
    if [ "$invalid_nodes" != "0" ]; then
        echo -e "${RED}✗${NC} $f (nodes missing required fields: id, type, x, y)"
        errors=$((errors + 1))
        continue
    fi

    echo -e "${GREEN}✓${NC} $f"
done

echo ""
echo "Validated $total files: $((total - errors)) passed, $errors failed"

exit $errors
