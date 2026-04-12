#!/usr/bin/env bash
# DSPy Code Validation Script
# Validates DSPy modules for correctness and best practices

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
ERRORS=0
WARNINGS=0
SUGGESTIONS=0

# Print functions
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_error() {
    echo -e "${RED}✗ ERROR: $1${NC}"
    ((ERRORS++))
}

print_warning() {
    echo -e "${YELLOW}⚠ WARNING: $1${NC}"
    ((WARNINGS++))
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_suggestion() {
    echo -e "${BLUE}💡 SUGGESTION: $1${NC}"
    ((SUGGESTIONS++))
}

# Usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS] <file_or_directory>

Validate DSPy code for correctness and best practices.

OPTIONS:
    -h, --help          Show this help message
    -v, --verbose       Verbose output
    -s, --strict        Strict mode (warnings as errors)
    -f, --fix           Auto-fix simple issues
    --check-imports     Check import statements
    --check-signatures  Check signature format
    --check-modules     Check module structure
    --check-metrics     Check metric functions
    --check-all         Run all checks (default)

EXAMPLES:
    $0 module.py                    # Validate single file
    $0 modules/                     # Validate directory
    $0 --strict module.py           # Strict mode
    $0 --check-signatures *.py      # Check signatures only
EOF
}

# Parse arguments
VERBOSE=false
STRICT=false
AUTOFIX=false
CHECK_IMPORTS=false
CHECK_SIGNATURES=false
CHECK_MODULES=false
CHECK_METRICS=false
CHECK_ALL=true

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -s|--strict)
            STRICT=true
            shift
            ;;
        -f|--fix)
            AUTOFIX=true
            shift
            ;;
        --check-imports)
            CHECK_IMPORTS=true
            CHECK_ALL=false
            shift
            ;;
        --check-signatures)
            CHECK_SIGNATURES=true
            CHECK_ALL=false
            shift
            ;;
        --check-modules)
            CHECK_MODULES=true
            CHECK_ALL=false
            shift
            ;;
        --check-metrics)
            CHECK_METRICS=true
            CHECK_ALL=false
            shift
            ;;
        --check-all)
            CHECK_ALL=true
            shift
            ;;
        *)
            TARGET="$1"
            shift
            ;;
    esac
done

# Validate target
if [[ -z "$TARGET" ]]; then
    echo "Error: No file or directory specified"
    usage
    exit 1
fi

if [[ ! -e "$TARGET" ]]; then
    echo "Error: $TARGET does not exist"
    exit 1
fi

# Enable all checks if CHECK_ALL
if [[ "$CHECK_ALL" == "true" ]]; then
    CHECK_IMPORTS=true
    CHECK_SIGNATURES=true
    CHECK_MODULES=true
    CHECK_METRICS=true
fi

print_header "DSPy Code Validation"
echo "Target: $TARGET"
echo ""

# Check 1: Import statements
if [[ "$CHECK_IMPORTS" == "true" ]]; then
    print_header "Checking Import Statements"

    # Check for dspy import
    if grep -qr "import dspy" "$TARGET"; then
        print_success "DSPy import found"
    else
        print_error "No 'import dspy' statement found"
    fi

    # Check for common anti-patterns
    if grep -qr "from openai import" "$TARGET"; then
        print_warning "Direct OpenAI import found - consider using dspy.OpenAI() instead"
        print_suggestion "Replace: from openai import ... → Use dspy.OpenAI(model=...)"
    fi

    if grep -qr "anthropic.Anthropic" "$TARGET"; then
        print_warning "Direct Anthropic import found - consider using dspy.Claude() instead"
        print_suggestion "Replace: anthropic.Anthropic() → dspy.Claude(model=...)"
    fi

    echo ""
fi

# Check 2: Signature format
if [[ "$CHECK_SIGNATURES" == "true" ]]; then
    print_header "Checking Signature Format"

    # Find all signature definitions
    signatures=$(grep -rn "dspy\.\(Predict\|ChainOfThought\|ProgramOfThought\|ReAct\)" "$TARGET" 2>/dev/null || true)

    if [[ -z "$signatures" ]]; then
        print_warning "No DSPy predictors found"
    else
        # Check signature format: "input1, input2 -> output1, output2"
        while IFS= read -r line; do
            if echo "$line" | grep -q '".*->.*"'; then
                print_success "Valid signature format found: $(echo $line | grep -o '"[^"]*"')"
            elif echo "$line" | grep -q '".*"' && ! echo "$line" | grep -q '->'; then
                print_error "Invalid signature (missing '->'): $(echo $line | grep -o '"[^"]*"')"
                print_suggestion "Signatures must use format: 'input -> output' or 'input1, input2 -> output1, output2'"
            fi
        done <<< "$signatures"
    fi

    echo ""
fi

# Check 3: Module structure
if [[ "$CHECK_MODULES" == "true" ]]; then
    print_header "Checking Module Structure"

    # Find class definitions
    classes=$(grep -rn "^class.*dspy\.Module" "$TARGET" 2>/dev/null || true)

    if [[ -z "$classes" ]]; then
        print_warning "No DSPy module classes found"
    else
        while IFS= read -r line; do
            class_name=$(echo "$line" | sed -n 's/^.*class \([^(]*\).*/\1/p')
            file=$(echo "$line" | cut -d: -f1)

            # Check for __init__ method
            if grep -q "def __init__" "$file"; then
                print_success "Module $class_name has __init__ method"
            else
                print_error "Module $class_name missing __init__ method"
            fi

            # Check for forward method
            if grep -q "def forward" "$file"; then
                print_success "Module $class_name has forward method"
            else
                print_error "Module $class_name missing forward method (required)"
            fi

            # Check for super().__init__()
            if grep -q "super().__init__()" "$file"; then
                print_success "Module $class_name calls super().__init__()"
            else
                print_warning "Module $class_name should call super().__init__()"
            fi

            # Check for return type annotation
            if grep -q "def forward.*-> dspy\.Prediction" "$file"; then
                print_success "Module $class_name has return type annotation"
            else
                print_suggestion "Consider adding return type: def forward(...) -> dspy.Prediction"
            fi
        done <<< "$classes"
    fi

    echo ""
fi

# Check 4: Metric functions
if [[ "$CHECK_METRICS" == "true" ]]; then
    print_header "Checking Metric Functions"

    # Find metric function definitions
    metrics=$(grep -rn "def.*metric\|def.*accuracy\|def.*f1_score" "$TARGET" 2>/dev/null || true)

    if [[ -z "$metrics" ]]; then
        print_warning "No metric functions found"
        print_suggestion "Define metric functions for evaluation: def metric(example, prediction, trace=None)"
    else
        while IFS= read -r line; do
            func_name=$(echo "$line" | sed -n 's/^.*def \([^(]*\).*/\1/p')

            # Check function signature
            if echo "$line" | grep -q "(example, prediction, trace=None)"; then
                print_success "Metric function $func_name has correct signature"
            elif echo "$line" | grep -q "(example, prediction)"; then
                print_warning "Metric function $func_name missing trace parameter"
                print_suggestion "Add trace parameter: def $func_name(example, prediction, trace=None)"
            else
                print_error "Metric function $func_name has invalid signature"
                print_suggestion "Use signature: def $func_name(example, prediction, trace=None)"
            fi
        done <<< "$metrics"
    fi

    echo ""
fi

# Additional checks
print_header "Additional Checks"

# Check for common anti-patterns
if grep -qr "\.format(" "$TARGET"; then
    print_warning "String .format() found - consider using f-strings"
fi

# Check for hardcoded prompts
if grep -qr "\".*Please.*answer.*\"" "$TARGET"; then
    print_warning "Hardcoded prompt text found - use DSPy signatures instead"
    print_suggestion "Replace hardcoded prompts with signatures: dspy.ChainOfThought('input -> output')"
fi

# Check for direct LLM calls
if grep -qr "openai\.chat\.completions\.create\|anthropic\.messages\.create" "$TARGET"; then
    print_error "Direct LLM API calls found - use DSPy modules instead"
    print_suggestion "Replace direct calls with DSPy predictors"
fi

# Check for monolithic functions
long_functions=$(grep -rn "^def " "$TARGET" 2>/dev/null | while read line; do
    file=$(echo "$line" | cut -d: -f1)
    line_num=$(echo "$line" | cut -d: -f2)

    # Count lines in function (until next def or class)
    func_lines=$(awk -v start="$line_num" '
        NR == start { in_func=1 }
        in_func && /^(def |class )/ && NR > start { exit }
        in_func { count++ }
        END { print count }
    ' "$file")

    if [[ $func_lines -gt 100 ]]; then
        echo "$file:$line_num:Function has $func_lines lines (>100)"
    fi
done)

if [[ -n "$long_functions" ]]; then
    print_warning "Long functions detected:"
    echo "$long_functions"
    print_suggestion "Consider breaking long functions into smaller, composable modules"
fi

echo ""

# Summary
print_header "Validation Summary"
echo "Errors:      $ERRORS"
echo "Warnings:    $WARNINGS"
echo "Suggestions: $SUGGESTIONS"
echo ""

# Exit code
if [[ $ERRORS -gt 0 ]]; then
    echo -e "${RED}Validation FAILED${NC}"
    exit 1
elif [[ $STRICT == "true" && $WARNINGS -gt 0 ]]; then
    echo -e "${RED}Validation FAILED (strict mode)${NC}"
    exit 1
else
    echo -e "${GREEN}Validation PASSED${NC}"
    exit 0
fi
