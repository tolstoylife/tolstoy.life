#!/bin/bash
# test_launchd_schedule.sh
# Unit test to verify launchd plist file is valid

set -euo pipefail

echo ""
echo "⏰ Testing Launchd Schedule Configuration..."
echo ""

PLIST_FILE="$HOME/.claude/launchd/com.claude.refactor.plist"
PASSED=0
FAILED=0

# Test 1: Plist file exists
test_plist_exists() {
    if [[ -f "$PLIST_FILE" ]]; then
        echo "   ✓ Plist file exists: $PLIST_FILE"
        return 0
    else
        echo "   ✗ Plist file NOT found: $PLIST_FILE"
        return 1
    fi
}

# Test 2: Plist has valid XML syntax
test_plist_syntax() {
    if plutil -lint "$PLIST_FILE" > /dev/null 2>&1; then
        echo "   ✓ Plist has valid XML syntax"
        return 0
    else
        echo "   ✗ Plist has INVALID XML syntax"
        plutil -lint "$PLIST_FILE" 2>&1 | head -5
        return 1
    fi
}

# Test 3: Required keys present
test_required_keys() {
    local required_keys=("Label" "ProgramArguments" "StartInterval")

    for key in "${required_keys[@]}"; do
        if /usr/libexec/PlistBuddy -c "Print :$key" "$PLIST_FILE" > /dev/null 2>&1; then
            echo "   ✓ Required key '$key' present"
        else
            echo "   ✗ Required key '$key' MISSING"
            return 1
        fi
    done

    return 0
}

# Test 4: StartInterval is 24 hours (86400 seconds)
test_interval() {
    local interval=$(/usr/libexec/PlistBuddy -c "Print :StartInterval" "$PLIST_FILE" 2>/dev/null)

    if [[ "$interval" == "86400" ]]; then
        echo "   ✓ StartInterval is 24 hours (86400 seconds)"
        return 0
    else
        echo "   ✗ StartInterval is $interval (expected 86400)"
        return 1
    fi
}

# Test 5: Log paths are valid
test_log_paths() {
    local stdout_path=$(/usr/libexec/PlistBuddy -c "Print :StandardOutPath" "$PLIST_FILE" 2>/dev/null || echo "")
    local stderr_path=$(/usr/libexec/PlistBuddy -c "Print :StandardErrorPath" "$PLIST_FILE" 2>/dev/null || echo "")

    if [[ -n "$stdout_path" ]]; then
        local log_dir=$(dirname "$stdout_path")
        if [[ -d "$log_dir" ]] || mkdir -p "$log_dir" 2>/dev/null; then
            echo "   ✓ Log directory accessible: $log_dir"
        else
            echo "   ⚠ Log directory not accessible: $log_dir"
        fi
    fi

    return 0
}

echo "Running launchd plist validation tests..."
echo ""

if test_plist_exists; then ((PASSED++)); else ((FAILED++)); fi
if test_plist_syntax; then ((PASSED++)); else ((FAILED++)); fi
if test_required_keys; then ((PASSED+=3)); else ((FAILED++)); fi
if test_interval; then ((PASSED++)); else ((FAILED++)); fi
if test_log_paths; then ((PASSED++)); else ((FAILED++)); fi

echo ""
echo "📊 Results:"
echo "   Passed: $PASSED"
echo "   Failed: $FAILED"

if [[ $FAILED -eq 0 ]]; then
    echo ""
    echo "✅ Test PASSED: Launchd plist is valid"
    echo ""
    echo "To enable the 24-hour auto-trigger:"
    echo "   1. Load: launchctl load $PLIST_FILE"
    echo "   2. Verify: launchctl list | grep com.claude.refactor"
    echo "   3. Unload (if needed): launchctl unload $PLIST_FILE"
    exit 0
else
    echo ""
    echo "❌ Test FAILED: $FAILED launchd validation tests failed"
    exit 1
fi
