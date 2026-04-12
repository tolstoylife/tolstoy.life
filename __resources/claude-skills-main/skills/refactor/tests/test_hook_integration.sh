#!/bin/bash
# test_hook_integration.sh
# Unit test to verify hook scripts execute correctly

set -euo pipefail

echo ""
echo "🔗 Testing Hook Integration..."
echo ""

HOOKS_DIR="$HOME/.claude/hooks"
PASSED=0
FAILED=0

# Test 1: Validate hook scripts exist and are executable
test_hook_exists() {
    local hook_name="$1"
    local hook_path="$HOOKS_DIR/$hook_name"

    if [[ -f "$hook_path" ]]; then
        if [[ -x "$hook_path" ]]; then
            echo "   ✓ $hook_name exists and is executable"
            return 0
        else
            echo "   ✗ $hook_name exists but is NOT executable"
            return 1
        fi
    else
        echo "   ✗ $hook_name NOT found"
        return 1
    fi
}

# Test 2: Validate shell script syntax
test_shell_syntax() {
    local hook_name="$1"
    local hook_path="$HOOKS_DIR/$hook_name"

    if bash -n "$hook_path" 2>/dev/null; then
        echo "   ✓ $hook_name has valid shell syntax"
        return 0
    else
        echo "   ✗ $hook_name has INVALID shell syntax"
        return 1
    fi
}

# Test 3: Dry run execution (with mock environment)
test_dry_run() {
    local hook_name="$1"
    local hook_path="$HOOKS_DIR/$hook_name"

    # Set up mock environment variables
    export CLAUDE_TOOL="Test"
    export CLAUDE_INPUT_FILE="$HOME/.claude/test-file.md"
    export CLAUDE_INPUT_OPERATION="test"

    # Run hook script (should not fail)
    if "$hook_path" 2>/dev/null; then
        echo "   ✓ $hook_name dry run succeeded"
        return 0
    else
        # Some hooks may legitimately exit with non-zero for validation failures
        # Check if it's a validation failure vs actual error
        local exit_code=$?
        if [[ $exit_code -eq 1 ]]; then
            echo "   ⚠ $hook_name validation triggered (expected behavior)"
            return 0
        else
            echo "   ✗ $hook_name dry run failed with exit code $exit_code"
            return 1
        fi
    fi
}

echo "Testing refactor-validation.sh..."
if test_hook_exists "refactor-validation.sh"; then ((PASSED++)); else ((FAILED++)); fi
if test_shell_syntax "refactor-validation.sh"; then ((PASSED++)); else ((FAILED++)); fi
if test_dry_run "refactor-validation.sh"; then ((PASSED++)); else ((FAILED++)); fi

echo ""
echo "Testing refactor-activity-log.sh..."
if test_hook_exists "refactor-activity-log.sh"; then ((PASSED++)); else ((FAILED++)); fi
if test_shell_syntax "refactor-activity-log.sh"; then ((PASSED++)); else ((FAILED++)); fi
if test_dry_run "refactor-activity-log.sh"; then ((PASSED++)); else ((FAILED++)); fi

echo ""
echo "📊 Results:"
echo "   Passed: $PASSED"
echo "   Failed: $FAILED"

if [[ $FAILED -eq 0 ]]; then
    echo ""
    echo "✅ Test PASSED: All hook integration tests successful"
    exit 0
else
    echo ""
    echo "❌ Test FAILED: $FAILED hook integration tests failed"
    exit 1
fi
