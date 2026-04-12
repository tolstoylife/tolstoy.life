#!/bin/bash
# validate-base.sh - Validates .base files are valid YAML
#
# Usage: ./validate-base.sh file1.base file2.base ...
#        ./validate-base.sh ../bases/examples/*.base

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

if [ $# -eq 0 ]; then
    echo "Usage: $0 <base-files...>"
    echo "Example: $0 ../bases/examples/*.base"
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

    # Check valid YAML using Python
    if python3 -c "import yaml; yaml.safe_load(open('$f'))" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $f"
    else
        echo -e "${RED}✗${NC} $f (invalid YAML)"
        errors=$((errors + 1))
    fi
done

echo ""
echo "Validated $total files: $((total - errors)) passed, $errors failed"

exit $errors
