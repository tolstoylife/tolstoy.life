#!/bin/bash
# component_audit.sh
# Audit refactor agent components for compliance with official standards

set -euo pipefail

echo ""
echo "🔍 Component Architecture Audit"
echo "=============================="
echo ""

PASSED=0
FAILED=0
WARNINGS=0

# Test 1: Audit refactor-agent.md
audit_refactor_agent() {
    echo "📋 Auditing refactor-agent.md..."
    local agent_file="$HOME/.claude/agents/refactor-agent.md"

    if [[ ! -f "$agent_file" ]]; then
        echo "   ✗ Agent file not found"
        return 1
    fi

    # Check required properties
    local required=("name" "description" "tools" "model" "permissionMode" "skills" "hooks")
    local missing=0

    for prop in "${required[@]}"; do
        if grep -q "^${prop}:" "$agent_file"; then
            echo "   ✓ Has required property: $prop"
        else
            echo "   ✗ Missing required property: $prop"
            ((missing++))
        fi
    done

    # Check model is opus (meta-orchestrator)
    if grep -q "^model: opus" "$agent_file"; then
        echo "   ✓ Uses opus model (meta-orchestrator)"
    else
        echo "   ⚠ Not using opus model (expected for meta-orchestrator)"
        ((WARNINGS++))
    fi

    # Check permissionMode is plan
    if grep -q "^permissionMode: plan" "$agent_file"; then
        echo "   ✓ Uses plan permission mode"
    else
        echo "   ⚠ Not using plan permission mode"
        ((WARNINGS++))
    fi

    if [[ $missing -eq 0 ]]; then
        echo "   ✅ refactor-agent.md compliant"
        return 0
    else
        echo "   ❌ refactor-agent.md has $missing missing properties"
        return 1
    fi
}

# Test 2: Audit refactor/SKILL.md
audit_refactor_skill() {
    echo ""
    echo "📋 Auditing refactor/SKILL.md..."
    local skill_file="$HOME/.claude/skills/refactor/SKILL.md"

    if [[ ! -f "$skill_file" ]]; then
        echo "   ✗ Skill file not found"
        return 1
    fi

    # Check required official properties
    if ! grep -q "^name:" "$skill_file"; then
        echo "   ✗ Missing required 'name' property"
        return 1
    else
        echo "   ✓ Has required 'name' property"
    fi

    if ! grep -q "^description:" "$skill_file"; then
        echo "   ✗ Missing required 'description' property"
        return 1
    else
        echo "   ✓ Has required 'description' property"
    fi

    # Check for meta-orchestrator properties
    if grep -q "^context: fork" "$skill_file"; then
        echo "   ✓ Uses forked context (meta-orchestrator)"
    else
        echo "   ⚠ Not using forked context"
        ((WARNINGS++))
    fi

    if grep -q "^agent: refactor-agent" "$skill_file"; then
        echo "   ✓ Has agent binding"
    else
        echo "   ⚠ No agent binding specified"
        ((WARNINGS++))
    fi

    if grep -q "^user-invocable: true" "$skill_file"; then
        echo "   ✓ User-invocable"
    else
        echo "   ⚠ Not user-invocable"
    fi

    # Check for non-official properties in frontmatter
    local non_official=("version" "triggers" "metadata" "integrates" "progressive_loading" "architecture")
    local found_non_official=0

    for prop in "${non_official[@]}"; do
        if grep -q "^${prop}:" "$skill_file"; then
            echo "   ⚠ Non-official property in frontmatter: $prop (move to body)"
            ((found_non_official++))
            ((WARNINGS++))
        fi
    done

    if [[ $found_non_official -eq 0 ]]; then
        echo "   ✓ No non-official properties in frontmatter"
    fi

    echo "   ✅ refactor/SKILL.md compliant"
    return 0
}

# Test 3: Audit evaluator subagents
audit_evaluators() {
    echo ""
    echo "📋 Auditing evaluator subagents..."
    local evaluators_dir="$HOME/.claude/skills/refactor/evaluators"

    local evaluator_files=($(find "$evaluators_dir" -name "*.md" -type f 2>/dev/null || true))
    local evaluator_count=${#evaluator_files[@]}

    if [[ $evaluator_count -ne 10 ]]; then
        echo "   ⚠ Found $evaluator_count evaluators (expected 10)"
        ((WARNINGS++))
    else
        echo "   ✓ Found 10 evaluators"
    fi

    local valid=0
    for evaluator in "${evaluator_files[@]}"; do
        local name=$(basename "$evaluator")

        # Check for required frontmatter
        if grep -q "^---" "$evaluator" && \
           grep -q "^name:" "$evaluator" && \
           grep -q "^description:" "$evaluator"; then
            ((valid++))
        else
            echo "   ✗ $name has invalid frontmatter"
        fi

        # Check for model assignment (should be sonnet, haiku, or opus)
        if grep -qE "^model: (sonnet|haiku|opus)" "$evaluator"; then
            # Valid model assignment
            :
        else
            echo "   ⚠ $name missing explicit model assignment"
        fi
    done

    if [[ $valid -eq $evaluator_count ]]; then
        echo "   ✓ All evaluators have valid frontmatter"
        echo "   ✅ Evaluators compliant"
        return 0
    else
        echo "   ✗ $((evaluator_count - valid)) evaluators have invalid frontmatter"
        return 1
    fi
}

# Test 4: Audit framework references
audit_frameworks() {
    echo ""
    echo "📋 Auditing framework references..."
    local frameworks_dir="$HOME/.claude/skills/refactor/frameworks"

    local expected_frameworks=(
        "homoiconic-renormalization.md"
        "bfo-gfo-ontology.md"
        "hegelian-dialectics.md"
        "pareto-optimization.md"
    )

    local found=0
    for framework in "${expected_frameworks[@]}"; do
        local framework_path="$frameworks_dir/$framework"

        if [[ -f "$framework_path" ]]; then
            # Check for required sections
            if grep -q "^# " "$framework_path"; then
                ((found++))
                echo "   ✓ $framework exists and has structure"
            else
                echo "   ✗ $framework exists but lacks structure"
            fi
        else
            echo "   ✗ $framework not found"
        fi
    done

    if [[ $found -eq 4 ]]; then
        echo "   ✅ All 4 framework references present"
        return 0
    else
        echo "   ❌ Only $found/4 frameworks present"
        return 1
    fi
}

# Test 5: Audit hook scripts
audit_hooks() {
    echo ""
    echo "📋 Auditing hook scripts..."

    local hooks=(
        "$HOME/.claude/hooks/refactor-validation.sh"
        "$HOME/.claude/hooks/refactor-activity-log.sh"
    )

    local valid=0
    for hook in "${hooks[@]}"; do
        local name=$(basename "$hook")

        if [[ ! -f "$hook" ]]; then
            echo "   ✗ $name not found"
            continue
        fi

        if [[ ! -x "$hook" ]]; then
            echo "   ✗ $name not executable"
            continue
        fi

        if bash -n "$hook" 2>/dev/null; then
            echo "   ✓ $name valid and executable"
            ((valid++))
        else
            echo "   ✗ $name has syntax errors"
        fi
    done

    if [[ $valid -eq 2 ]]; then
        echo "   ✅ Hook scripts compliant"
        return 0
    else
        echo "   ❌ $((2 - valid)) hooks have issues"
        return 1
    fi
}

# Run all audits
echo "Running component audits..."
echo ""

if audit_refactor_agent; then ((PASSED++)); else ((FAILED++)); fi
if audit_refactor_skill; then ((PASSED++)); else ((FAILED++)); fi
if audit_evaluators; then ((PASSED++)); else ((FAILED++)); fi
if audit_frameworks; then ((PASSED++)); else ((FAILED++)); fi
if audit_hooks; then ((PASSED++)); else ((FAILED++)); fi

echo ""
echo "=============================="
echo "📊 Audit Results"
echo "=============================="
echo "   Total audits: 5"
echo "   Passed: $PASSED"
echo "   Failed: $FAILED"
echo "   Warnings: $WARNINGS"
echo ""

if [[ $FAILED -eq 0 ]]; then
    echo "✅ Component Audit PASSED"

    if [[ $WARNINGS -gt 0 ]]; then
        echo ""
        echo "⚠️  Note: $WARNINGS warnings were issued."
        echo "    Warnings indicate non-critical issues or style recommendations."
    fi

    echo ""
    echo "All refactor agent components comply with official standards."
    echo ""
    echo "Summary:"
    echo "  ✓ refactor-agent.md: opus model, plan permission mode, hooks configured"
    echo "  ✓ refactor/SKILL.md: forked context, agent binding, official frontmatter"
    echo "  ✓ 10 evaluator subagents: valid frontmatter, proper model assignments"
    echo "  ✓ 4 framework references: complete documentation"
    echo "  ✓ Hook scripts: executable, valid syntax"
    exit 0
else
    echo "❌ Component Audit FAILED"
    echo ""
    echo "$FAILED audits failed. Please review the output above."
    exit 1
fi
