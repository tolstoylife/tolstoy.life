#!/bin/bash
# validate-all.sh - Run all validators on examples and templates
#
# Usage: ./validate-all.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Obsidian Skills Validation ==="
echo ""

total_errors=0

# Validate Canvas files
echo "📄 Validating Canvas files (.canvas)..."
canvas_files=$(find ../canvas/examples ../canvas/templates -name "*.canvas" 2>/dev/null | sort)
if [ -n "$canvas_files" ]; then
    if ! ./validate-canvas.sh $canvas_files; then
        total_errors=$((total_errors + 1))
    fi
else
    echo "   No .canvas files found"
fi
echo ""

# Validate Base files
echo "📊 Validating Base files (.base)..."
base_files=$(find ../bases/examples ../bases/templates -name "*.base" 2>/dev/null | sort)
if [ -n "$base_files" ]; then
    if ! ./validate-base.sh $base_files; then
        total_errors=$((total_errors + 1))
    fi
else
    echo "   No .base files found"
fi
echo ""

# Check Markdown files exist (basic validation)
echo "📝 Checking Markdown files (.md)..."
md_count=$(find ../markdown/examples ../markdown/templates -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
echo "   Found $md_count Markdown files"
echo ""

# Summary
echo "=== Validation Complete ==="
if [ $total_errors -eq 0 ]; then
    echo "✅ All validations passed!"
    exit 0
else
    echo "❌ Some validations failed"
    exit 1
fi
