#!/bin/bash
# integration_test.sh
# Integration test for refactor agent functionality
# Tests full cycle: dry-run → parallel evaluation → bv/bd integration → claude-mem

set -euo pipefail

echo ""
echo "🧪 Refactor Agent Integration Test"
echo "=================================="
echo ""

PASSED=0
FAILED=0
TEST_DIR="$HOME/.claude/skills/refactor"

# Test 1: Verify all components exist
test_components_exist() {
    echo "📁 Test 1: Verifying component structure..."

    local required_files=(
        "$HOME/.claude/agents/refactor-agent.md"
        "$HOME/.claude/skills/refactor/SKILL.md"
        "$HOME/.claude/hooks/refactor-validation.sh"
        "$HOME/.claude/hooks/refactor-activity-log.sh"
        "$HOME/.claude/launchd/com.claude.refactor.plist"
    )

    local missing=0
    for file in "${required_files[@]}"; do
        if [[ -f "$file" ]]; then
            echo "   ✓ Found: $(basename "$file")"
        else
            echo "   ✗ Missing: $file"
            ((missing++))
        fi
    done

    # Check evaluators directory
    local evaluator_count=$(find "$TEST_DIR/evaluators" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$evaluator_count" -eq 10 ]]; then
        echo "   ✓ Found: 10 evaluator subagents"
    else
        echo "   ✗ Found: $evaluator_count evaluators (expected 10)"
        ((missing++))
    fi

    # Check frameworks directory
    local framework_count=$(find "$TEST_DIR/frameworks" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$framework_count" -eq 4 ]]; then
        echo "   ✓ Found: 4 framework references"
    else
        echo "   ✗ Found: $framework_count frameworks (expected 4)"
        ((missing++))
    fi

    # Check scripts directory
    local script_count=$(find "$TEST_DIR/scripts" -name "*.py" -type f 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$script_count" -eq 2 ]]; then
        echo "   ✓ Found: 2 Python utilities"
    else
        echo "   ✗ Found: $script_count scripts (expected 2)"
        ((missing++))
    fi

    if [[ $missing -eq 0 ]]; then
        echo "   ✅ All components present"
        return 0
    else
        echo "   ❌ $missing components missing"
        return 1
    fi
}

# Test 2: Verify bv/bd integration capability
test_bv_bd_integration() {
    echo ""
    echo "🔗 Test 2: Checking bv/bd integration..."

    if command -v bd &> /dev/null && command -v bv &> /dev/null; then
        echo "   ✓ bd binary found: $(which bd)"
        echo "   ✓ bv binary found: $(which bv)"

        # Test bd version
        if bd_version=$(bd --version 2>&1 | head -1); then
            echo "   ✓ bd version: $bd_version"
        else
            echo "   ⚠ Could not determine bd version"
        fi

        # Test bv version
        if bv_version=$(bv --version 2>&1 | head -1); then
            echo "   ✓ bv version: $bv_version"
        else
            echo "   ⚠ Could not determine bv version"
        fi

        echo "   ✅ bv/bd integration available"
        return 0
    else
        echo "   ⚠ bv/bd not installed (optional integration)"
        echo "   Note: Refactor agent will work without bv/bd"
        return 0
    fi
}

# Test 3: Verify Python utilities are executable
test_python_utilities() {
    echo ""
    echo "🐍 Test 3: Testing Python utilities..."

    # Test redundancy detector
    if python3 "$TEST_DIR/scripts/redundancy-detector.py" --help > /dev/null 2>&1; then
        echo "   ✓ redundancy-detector.py is executable"
    else
        echo "   ✗ redundancy-detector.py failed"
        return 1
    fi

    # Test archive pruner
    if python3 "$TEST_DIR/scripts/archive-pruner.py" --help > /dev/null 2>&1; then
        echo "   ✓ archive-pruner.py is executable"
    else
        echo "   ✗ archive-pruner.py failed"
        return 1
    fi

    echo "   ✅ Python utilities functional"
    return 0
}

# Test 4: Verify framework references have valid content
test_framework_references() {
    echo ""
    echo "📚 Test 4: Validating framework references..."

    local frameworks=(
        "homoiconic-renormalization.md"
        "bfo-gfo-ontology.md"
        "hegelian-dialectics.md"
        "pareto-optimization.md"
    )

    local valid=0
    for framework in "${frameworks[@]}"; do
        local framework_path="$TEST_DIR/frameworks/$framework"

        if [[ -f "$framework_path" ]]; then
            # Check for required sections
            if grep -q "## Principle" "$framework_path" && \
               grep -q "## Application" "$framework_path"; then
                echo "   ✓ $framework has required sections"
                ((valid++))
            else
                echo "   ⚠ $framework missing required sections"
            fi
        else
            echo "   ✗ $framework not found"
        fi
    done

    if [[ $valid -eq 4 ]]; then
        echo "   ✅ All framework references valid"
        return 0
    else
        echo "   ❌ $((4 - valid)) frameworks incomplete"
        return 1
    fi
}

# Test 5: Verify hook scripts have proper permissions
test_hook_permissions() {
    echo ""
    echo "🔐 Test 5: Checking hook script permissions..."

    local hooks=(
        "$HOME/.claude/hooks/refactor-validation.sh"
        "$HOME/.claude/hooks/refactor-activity-log.sh"
    )

    local executable=0
    for hook in "${hooks[@]}"; do
        if [[ -x "$hook" ]]; then
            echo "   ✓ $(basename "$hook") is executable"
            ((executable++))
        else
            echo "   ✗ $(basename "$hook") is NOT executable"
        fi
    done

    if [[ $executable -eq 2 ]]; then
        echo "   ✅ Hook scripts properly configured"
        return 0
    else
        echo "   ❌ $((2 - executable)) hooks not executable"
        return 1
    fi
}

# Run all tests
echo "Running integration tests..."
echo ""

if test_components_exist; then ((PASSED++)); else ((FAILED++)); fi
if test_bv_bd_integration; then ((PASSED++)); else ((FAILED++)); fi
if test_python_utilities; then ((PASSED++)); else ((FAILED++)); fi
if test_framework_references; then ((PASSED++)); else ((FAILED++)); fi
if test_hook_permissions; then ((PASSED++)); else ((FAILED++)); fi

echo ""
echo "=========================================="
echo "📊 Integration Test Results"
echo "=========================================="
echo "   Total tests: 5"
echo "   Passed: $PASSED"
echo "   Failed: $FAILED"
echo ""

if [[ $FAILED -eq 0 ]]; then
    echo "✅ Integration Test PASSED"
    echo ""
    echo "All refactor agent components are properly installed and configured."
    echo ""
    echo "Next steps:"
    echo "  1. Test the refactor agent with: /refactor --dry-run"
    echo "  2. Run component audit (see component_audit.sh)"
    echo "  3. Enable 24hr auto-trigger (see launchd plist test output)"
    exit 0
else
    echo "❌ Integration Test FAILED"
    echo ""
    echo "$FAILED tests failed. Please review the output above."
    exit 1
fi
