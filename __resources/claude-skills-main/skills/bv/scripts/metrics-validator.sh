#!/usr/bin/env bash
#
# metrics-validator.sh - Validate bv metrics output structure and content
#
# Usage:
#   ./metrics-validator.sh <json-file>
#   bv --robot-insights | ./metrics-validator.sh -
#
# Exit codes:
#   0 = Valid
#   1 = Invalid structure
#   2 = Invalid values
#   3 = Missing required fields

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Validation counters
ERRORS=0
WARNINGS=0

# Helper functions
error() {
    echo -e "${RED}❌ ERROR: $1${NC}" >&2
    ((ERRORS++))
}

warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}" >&2
    ((WARNINGS++))
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

info() {
    echo "ℹ️  $1"
}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    error "jq is required but not installed. Install with: brew install jq"
    exit 3
fi

# Read input
if [ $# -eq 0 ]; then
    error "Usage: $0 <json-file> or pipe JSON via stdin"
    exit 3
fi

if [ "$1" = "-" ]; then
    INPUT=$(cat)
else
    if [ ! -f "$1" ]; then
        error "File not found: $1"
        exit 3
    fi
    INPUT=$(cat "$1")
fi

# Parse JSON
if ! JSON=$(echo "$INPUT" | jq '.' 2>/dev/null); then
    error "Invalid JSON format"
    exit 1
fi

info "Validating bv metrics output structure..."
echo ""

# ============================================================================
# Structure Validation
# ============================================================================

# Check for error response
if echo "$JSON" | jq -e '.error == true' &>/dev/null; then
    ERROR_MSG=$(echo "$JSON" | jq -r '.message')
    ERROR_CODE=$(echo "$JSON" | jq -r '.code')
    error "bv returned error: [$ERROR_CODE] $ERROR_MSG"
    exit 1
fi

# Validate top-level fields
info "Checking top-level structure..."

REQUIRED_FIELDS=(
    "timestamp"
    "graphStats"
    "metrics"
    "cycles"
    "topologicalSort"
    "recommendations"
)

for field in "${REQUIRED_FIELDS[@]}"; do
    if ! echo "$JSON" | jq -e "has(\"$field\")" &>/dev/null; then
        error "Missing required field: $field"
    else
        success "Field present: $field"
    fi
done

# ============================================================================
# Graph Stats Validation
# ============================================================================

echo ""
info "Validating graphStats..."

GRAPH_STATS_FIELDS=(
    "totalIssues"
    "openIssues"
    "closedIssues"
    "totalDependencies"
    "density"
)

for field in "${GRAPH_STATS_FIELDS[@]}"; do
    if ! echo "$JSON" | jq -e ".graphStats | has(\"$field\")" &>/dev/null; then
        error "Missing graphStats.$field"
    fi
done

# Validate density structure
if echo "$JSON" | jq -e '.graphStats.density | has("density")' &>/dev/null; then
    DENSITY=$(echo "$JSON" | jq -r '.graphStats.density.density')

    # Check density range (0.0 - 1.0)
    if (( $(echo "$DENSITY < 0.0" | bc -l) )) || (( $(echo "$DENSITY > 1.0" | bc -l) )); then
        error "Density out of range [0.0-1.0]: $DENSITY"
    else
        success "Density valid: $DENSITY"
    fi

    # Check interpretation
    INTERPRETATION=$(echo "$JSON" | jq -r '.graphStats.density.interpretation')
    VALID_INTERPRETATIONS=("sparse" "balanced" "dense" "over_coupled")

    if [[ ! " ${VALID_INTERPRETATIONS[@]} " =~ " ${INTERPRETATION} " ]]; then
        warning "Unexpected density interpretation: $INTERPRETATION"
    else
        success "Density interpretation: $INTERPRETATION"
    fi
else
    error "Missing density structure"
fi

# Validate counts
TOTAL_ISSUES=$(echo "$JSON" | jq -r '.graphStats.totalIssues')
OPEN_ISSUES=$(echo "$JSON" | jq -r '.graphStats.openIssues')
CLOSED_ISSUES=$(echo "$JSON" | jq -r '.graphStats.closedIssues')

if [ "$TOTAL_ISSUES" -ne $((OPEN_ISSUES + CLOSED_ISSUES)) ]; then
    error "Total issues ($TOTAL_ISSUES) != open ($OPEN_ISSUES) + closed ($CLOSED_ISSUES)"
else
    success "Issue counts consistent"
fi

# ============================================================================
# Metrics Validation
# ============================================================================

echo ""
info "Validating metrics structure..."

METRIC_TYPES=(
    "pageRank"
    "betweenness"
    "hits"
    "criticalPath"
    "eigenvector"
    "degree"
)

for metric in "${METRIC_TYPES[@]}"; do
    if ! echo "$JSON" | jq -e ".metrics | has(\"$metric\")" &>/dev/null; then
        error "Missing metric: $metric"
    else
        COUNT=$(echo "$JSON" | jq ".metrics.$metric | length")
        success "Metric $metric: $COUNT entries"
    fi
done

# Validate PageRank scores (0.0 - 1.0)
info "Validating PageRank scores..."
INVALID_PAGERANK=$(echo "$JSON" | jq '[.metrics.pageRank[] | select(.score < 0.0 or .score > 1.0)] | length')
if [ "$INVALID_PAGERANK" -gt 0 ]; then
    error "Found $INVALID_PAGERANK PageRank scores out of range [0.0-1.0]"
else
    success "All PageRank scores valid"
fi

# Validate Betweenness scores (0.0 - 1.0)
info "Validating Betweenness scores..."
INVALID_BETWEENNESS=$(echo "$JSON" | jq '[.metrics.betweenness[] | select(.score < 0.0 or .score > 1.0)] | length')
if [ "$INVALID_BETWEENNESS" -gt 0 ]; then
    error "Found $INVALID_BETWEENNESS Betweenness scores out of range [0.0-1.0]"
else
    success "All Betweenness scores valid"
fi

# Validate HITS scores
info "Validating HITS scores..."
INVALID_HITS=$(echo "$JSON" | jq '[.metrics.hits[] | select(.hubScore < 0.0 or .hubScore > 1.0 or .authorityScore < 0.0 or .authorityScore > 1.0)] | length')
if [ "$INVALID_HITS" -gt 0 ]; then
    error "Found $INVALID_HITS HITS scores out of range [0.0-1.0]"
else
    success "All HITS scores valid"
fi

# Validate Degree centrality
info "Validating Degree centrality..."
INVALID_DEGREE=$(echo "$JSON" | jq '[.metrics.degree[] | select(.inDegree < 0 or .outDegree < 0)] | length')
if [ "$INVALID_DEGREE" -gt 0 ]; then
    error "Found $INVALID_DEGREE Degree entries with negative values"
else
    success "All Degree values valid"
fi

# Check degree consistency (totalDegree = inDegree + outDegree)
INCONSISTENT_DEGREE=$(echo "$JSON" | jq '[.metrics.degree[] | select(.totalDegree != (.inDegree + .outDegree))] | length')
if [ "$INCONSISTENT_DEGREE" -gt 0 ]; then
    error "Found $INCONSISTENT_DEGREE Degree entries with inconsistent totals"
else
    success "All Degree totals consistent"
fi

# ============================================================================
# Cycles Validation
# ============================================================================

echo ""
info "Validating cycles..."

CYCLE_COUNT=$(echo "$JSON" | jq '.cycles | length')

if [ "$CYCLE_COUNT" -gt 0 ]; then
    warning "Found $CYCLE_COUNT cycles (circular dependencies)"

    # Validate cycle structure
    for i in $(seq 0 $((CYCLE_COUNT - 1))); do
        CYCLE_LENGTH=$(echo "$JSON" | jq -r ".cycles[$i].length")
        PATH_LENGTH=$(echo "$JSON" | jq ".cycles[$i].path | length")

        if [ "$CYCLE_LENGTH" -ne "$PATH_LENGTH" ]; then
            error "Cycle $i: length ($CYCLE_LENGTH) != path length ($PATH_LENGTH)"
        fi

        # Check severity
        SEVERITY=$(echo "$JSON" | jq -r ".cycles[$i].severity")
        if [[ "$SEVERITY" != "critical" && "$SEVERITY" != "warning" ]]; then
            error "Cycle $i: invalid severity '$SEVERITY'"
        fi
    done
else
    success "No cycles detected (healthy DAG)"
fi

# ============================================================================
# Topological Sort Validation
# ============================================================================

echo ""
info "Validating topological sort..."

if echo "$JSON" | jq -e '.topologicalSort | has("order")' &>/dev/null; then
    IS_VALID=$(echo "$JSON" | jq -r '.topologicalSort.isValid')
    ORDER_LENGTH=$(echo "$JSON" | jq '.topologicalSort.order | length')

    if [ "$CYCLE_COUNT" -gt 0 ] && [ "$IS_VALID" = "true" ]; then
        error "Topological sort marked valid but cycles exist"
    elif [ "$CYCLE_COUNT" -eq 0 ] && [ "$IS_VALID" = "false" ]; then
        error "Topological sort marked invalid but no cycles detected"
    elif [ "$IS_VALID" = "true" ]; then
        success "Topological sort valid: $ORDER_LENGTH issues in order"
    else
        warning "Topological sort invalid due to cycles"
    fi
else
    error "Missing topological sort structure"
fi

# ============================================================================
# Recommendations Validation
# ============================================================================

echo ""
info "Validating recommendations..."

RECOMMENDATION_FIELDS=(
    "highImpactIssues"
    "bottleneckIssues"
    "foundationalIssues"
)

for field in "${RECOMMENDATION_FIELDS[@]}"; do
    if echo "$JSON" | jq -e ".recommendations | has(\"$field\")" &>/dev/null; then
        COUNT=$(echo "$JSON" | jq ".recommendations.$field | length")
        success "Recommendation $field: $COUNT issues"
    else
        error "Missing recommendation field: $field"
    fi
done

# ============================================================================
# Summary
# ============================================================================

echo ""
echo "================================================================"
echo "Validation Summary"
echo "================================================================"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    success "ALL CHECKS PASSED"
    echo ""
    info "Metrics summary:"
    echo "  Total Issues: $(echo "$JSON" | jq -r '.graphStats.totalIssues')"
    echo "  Density: $(echo "$JSON" | jq -r '.graphStats.density.density') ($(echo "$JSON" | jq -r '.graphStats.density.interpretation'))"
    echo "  Cycles: $CYCLE_COUNT"
    echo "  Topological Sort: $(echo "$JSON" | jq -r '.topologicalSort.isValid')"
    echo ""
    exit 0
elif [ $ERRORS -eq 0 ]; then
    warning "$WARNINGS warning(s) found"
    echo ""
    exit 0
else
    error "$ERRORS error(s), $WARNINGS warning(s) found"
    echo ""
    exit 2
fi
