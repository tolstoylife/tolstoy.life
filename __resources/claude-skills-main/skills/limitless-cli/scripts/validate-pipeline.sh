#!/bin/bash
# Pipeline Validation Script
# Validates YAML pipeline syntax and structure

set -e

if [ -z "$1" ]; then
    echo "Usage: validate-pipeline.sh <pipeline.yaml>"
    echo ""
    echo "Examples:"
    echo "  validate-pipeline.sh templates/daily-digest.yaml"
    echo "  validate-pipeline.sh ./custom-pipeline.yaml"
    exit 1
fi

PIPELINE_FILE="$1"
PROJECT_DIR="${PROJECT_DIR:-$HOME/Projects/limitless-cli}"

echo "🔍 Validating Pipeline: $PIPELINE_FILE"
echo "======================================="
echo ""

# Check file exists
if [ ! -f "$PIPELINE_FILE" ]; then
    echo "❌ File not found: $PIPELINE_FILE"
    exit 1
fi
echo "✅ File exists"

# Check YAML syntax
if command -v yq &> /dev/null; then
    if yq eval '.' "$PIPELINE_FILE" > /dev/null 2>&1; then
        echo "✅ YAML syntax valid"
    else
        echo "❌ Invalid YAML syntax"
        yq eval '.' "$PIPELINE_FILE"
        exit 1
    fi
else
    echo "⚠️  yq not installed, skipping syntax check"
fi

# Check required fields
echo ""
echo "Checking required fields..."

check_field() {
    local field=$1
    local value
    value=$(yq eval "$field" "$PIPELINE_FILE" 2>/dev/null)
    if [ "$value" != "null" ] && [ -n "$value" ]; then
        echo "  ✅ $field: $value"
        return 0
    else
        echo "  ❌ Missing: $field"
        return 1
    fi
}

ERRORS=0

check_field ".apiVersion" || ((ERRORS++))
check_field ".kind" || ((ERRORS++))
check_field ".metadata.name" || ((ERRORS++))
check_field ".spec.nodes" || ((ERRORS++))

# Check nodes have required fields
echo ""
echo "Checking node definitions..."

NODE_COUNT=$(yq eval '.spec.nodes | length' "$PIPELINE_FILE" 2>/dev/null)
if [ "$NODE_COUNT" -gt 0 ]; then
    echo "  ✅ Found $NODE_COUNT nodes"

    # List node types
    echo ""
    echo "Node types:"
    yq eval '.spec.nodes | keys | .[]' "$PIPELINE_FILE" 2>/dev/null | while read -r node; do
        type=$(yq eval ".spec.nodes.$node.type" "$PIPELINE_FILE" 2>/dev/null)
        echo "  - $node: $type"
    done
else
    echo "  ❌ No nodes defined"
    ((ERRORS++))
fi

# Check edges if present
EDGE_COUNT=$(yq eval '.spec.edges | length' "$PIPELINE_FILE" 2>/dev/null || echo "0")
if [ "$EDGE_COUNT" != "null" ] && [ "$EDGE_COUNT" -gt 0 ]; then
    echo ""
    echo "  ✅ Found $EDGE_COUNT edges"
fi

# Summary
echo ""
echo "======================================="
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ Pipeline validation passed"
    exit 0
else
    echo "❌ Pipeline validation failed with $ERRORS error(s)"
    exit 1
fi
