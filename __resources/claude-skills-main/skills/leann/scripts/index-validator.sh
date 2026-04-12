#!/bin/bash
#
# LEANN Index Health Validator
# Comprehensive health checks and recommendations for LEANN indexes
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
INDEX="${1:-./leann.index}"
VERBOSE="${VERBOSE:-false}"
JSON_OUTPUT="${JSON_OUTPUT:-false}"
REPAIR="${REPAIR:-false}"

# Thresholds (configurable via environment)
COVERAGE_MIN="${COVERAGE_MIN:-0.70}"
COVERAGE_TARGET="${COVERAGE_TARGET:-0.80}"
QUANT_ERROR_MAX="${QUANT_ERROR_MAX:-0.05}"
BALANCE_MIN="${BALANCE_MIN:-0.70}"
DELTA_RATIO_MAX="${DELTA_RATIO_MAX:-10.0}"
HEALTH_SCORE_MIN="${HEALTH_SCORE_MIN:-60}"

# Usage
usage() {
  cat <<EOF
Usage: $0 [INDEX_PATH] [OPTIONS]

Validate LEANN index health and provide recommendations.

Arguments:
  INDEX_PATH          Path to LEANN index (default: ./leann.index)

Environment Variables:
  VERBOSE=true        Enable verbose output
  JSON_OUTPUT=true    Output results as JSON
  REPAIR=true         Attempt automatic repairs
  COVERAGE_MIN=0.70   Minimum coverage score
  QUANT_ERROR_MAX=0.05 Maximum quantization error
  BALANCE_MIN=0.70    Minimum utilization balance
  DELTA_RATIO_MAX=10  Maximum delta index ratio (%)

Examples:
  $0 ./leann.index
  VERBOSE=true $0 ./leann.index
  JSON_OUTPUT=true $0 ./leann.index > health.json
  REPAIR=true $0 ./leann.index

Exit Codes:
  0 - Healthy index
  1 - Degraded index (warnings)
  2 - Unhealthy index (critical issues)
  3 - Index not found or corrupted
EOF
  exit 1
}

# Check if index exists
if [[ ! -f "$INDEX" && ! -d "$INDEX" ]]; then
  echo -e "${RED}Error: Index not found at $INDEX${NC}"
  echo "Run: leann index create --help"
  exit 3
fi

# Logging functions
log_info() {
  if [[ "$JSON_OUTPUT" == "false" ]]; then
    echo -e "${BLUE}ℹ${NC} $1"
  fi
}

log_success() {
  if [[ "$JSON_OUTPUT" == "false" ]]; then
    echo -e "${GREEN}✓${NC} $1"
  fi
}

log_warning() {
  if [[ "$JSON_OUTPUT" == "false" ]]; then
    echo -e "${YELLOW}⚠${NC} $1"
  fi
}

log_error() {
  if [[ "$JSON_OUTPUT" == "false" ]]; then
    echo -e "${RED}✗${NC} $1"
  fi
}

# Check if leann is installed
if ! command -v leann &> /dev/null; then
  log_error "leann not found. Install: pip install leann"
  exit 3
fi

# Initialize results
declare -A RESULTS
ISSUES=()
WARNINGS=()
RECOMMENDATIONS=()
EXIT_CODE=0

# Header
if [[ "$JSON_OUTPUT" == "false" ]]; then
  echo ""
  echo "╔════════════════════════════════════════════════════════════╗"
  echo "║           LEANN Index Health Validator                    ║"
  echo "╚════════════════════════════════════════════════════════════╝"
  echo ""
  log_info "Index: $INDEX"
  echo ""
fi

# 1. Check Coverage Score
log_info "Checking anchor coverage..."
if COVERAGE_JSON=$(leann index validate "$INDEX" --metric coverage --json 2>&1); then
  COVERAGE=$(echo "$COVERAGE_JSON" | jq -r '.score // empty')

  if [[ -z "$COVERAGE" ]]; then
    log_error "Failed to retrieve coverage score"
    ISSUES+=("coverage_check_failed")
    EXIT_CODE=2
  else
    RESULTS["coverage"]="$COVERAGE"

    if (( $(echo "$COVERAGE >= $COVERAGE_TARGET" | bc -l) )); then
      log_success "Coverage: $COVERAGE (excellent, target: >$COVERAGE_TARGET)"
    elif (( $(echo "$COVERAGE >= $COVERAGE_MIN" | bc -l) )); then
      log_warning "Coverage: $COVERAGE (acceptable, target: >$COVERAGE_TARGET)"
      WARNINGS+=("coverage_below_target")
      RECOMMENDATIONS+=("Consider increasing anchor count for better coverage")
      EXIT_CODE=$(( EXIT_CODE > 0 ? EXIT_CODE : 1 ))
    else
      log_error "Coverage: $COVERAGE (too low, minimum: >$COVERAGE_MIN)"
      ISSUES+=("coverage_too_low")
      RECOMMENDATIONS+=("CRITICAL: Rebuild index with more anchors (current coverage: $COVERAGE)")
      EXIT_CODE=2
    fi
  fi
else
  log_error "Coverage check failed: $COVERAGE_JSON"
  ISSUES+=("coverage_check_error")
  EXIT_CODE=2
fi

# 2. Check Quantization Error
log_info "Checking quantization error..."
if QUANT_JSON=$(leann index validate "$INDEX" --metric quantization --json 2>&1); then
  QUANT_ERROR=$(echo "$QUANT_JSON" | jq -r '.error // empty')

  if [[ -z "$QUANT_ERROR" ]]; then
    log_error "Failed to retrieve quantization error"
    ISSUES+=("quantization_check_failed")
    EXIT_CODE=2
  else
    RESULTS["quantization_error"]="$QUANT_ERROR"

    if (( $(echo "$QUANT_ERROR <= $QUANT_ERROR_MAX" | bc -l) )); then
      log_success "Quantization Error: $QUANT_ERROR (good, target: <$QUANT_ERROR_MAX)"
    else
      log_error "Quantization Error: $QUANT_ERROR (too high, target: <$QUANT_ERROR_MAX)"
      ISSUES+=("quantization_error_high")
      RECOMMENDATIONS+=("Reduce PQ compression: use fewer subvectors or larger codebooks")
      EXIT_CODE=2
    fi
  fi
else
  log_error "Quantization check failed: $QUANT_JSON"
  ISSUES+=("quantization_check_error")
  EXIT_CODE=2
fi

# 3. Check Utilization Balance
log_info "Checking anchor utilization balance..."
if BALANCE_JSON=$(leann index validate "$INDEX" --metric balance --json 2>&1); then
  BALANCE=$(echo "$BALANCE_JSON" | jq -r '.score // empty')

  if [[ -z "$BALANCE" ]]; then
    log_error "Failed to retrieve balance score"
    ISSUES+=("balance_check_failed")
    EXIT_CODE=2
  else
    RESULTS["balance"]="$BALANCE"

    if (( $(echo "$BALANCE >= $BALANCE_MIN" | bc -l) )); then
      log_success "Utilization Balance: $BALANCE (good, target: >$BALANCE_MIN)"
    else
      log_warning "Utilization Balance: $BALANCE (imbalanced, target: >$BALANCE_MIN)"
      WARNINGS+=("balance_too_low")
      RECOMMENDATIONS+=("Some anchors are overloaded. Consider redistributing with max-coverage strategy")
      EXIT_CODE=$(( EXIT_CODE > 0 ? EXIT_CODE : 1 ))
    fi
  fi
else
  log_error "Balance check failed: $BALANCE_JSON"
  ISSUES+=("balance_check_error")
  EXIT_CODE=2
fi

# 4. Check Delta Index Size
log_info "Checking delta index size..."
if STATS_JSON=$(leann index stats "$INDEX" --json 2>&1); then
  DELTA_SIZE=$(echo "$STATS_JSON" | jq -r '.deltaIndexSize // 0')
  MAIN_SIZE=$(echo "$STATS_JSON" | jq -r '.mainIndexSize // 1')

  if [[ "$MAIN_SIZE" -gt 0 ]]; then
    DELTA_RATIO=$(echo "scale=2; $DELTA_SIZE / $MAIN_SIZE * 100" | bc)
    RESULTS["delta_ratio"]="$DELTA_RATIO"

    if (( $(echo "$DELTA_RATIO < $DELTA_RATIO_MAX" | bc -l) )); then
      log_success "Delta Index: ${DELTA_RATIO}% of main (healthy, rebuild at ${DELTA_RATIO_MAX}%)"
    else
      log_warning "Delta Index: ${DELTA_RATIO}% of main (exceeds threshold)"
      WARNINGS+=("delta_index_large")
      RECOMMENDATIONS+=("Delta index is large (${DELTA_RATIO}%). Schedule full rebuild")
      EXIT_CODE=$(( EXIT_CODE > 0 ? EXIT_CODE : 1 ))
    fi
  else
    log_warning "Could not determine delta index ratio"
  fi
else
  log_error "Stats check failed: $STATS_JSON"
  ISSUES+=("stats_check_error")
fi

# 5. Check Overall Health Score
log_info "Computing overall health score..."
if HEALTH_JSON=$(leann index validate "$INDEX" --json 2>&1); then
  HEALTH_SCORE=$(echo "$HEALTH_JSON" | jq -r '.healthScore // empty')

  if [[ -z "$HEALTH_SCORE" ]]; then
    log_error "Failed to retrieve health score"
    ISSUES+=("health_score_unavailable")
    EXIT_CODE=2
  else
    RESULTS["health_score"]="$HEALTH_SCORE"

    if (( $(echo "$HEALTH_SCORE >= 80" | bc -l) )); then
      log_success "Health Score: $HEALTH_SCORE/100 (excellent)"
    elif (( $(echo "$HEALTH_SCORE >= $HEALTH_SCORE_MIN" | bc -l) )); then
      log_warning "Health Score: $HEALTH_SCORE/100 (acceptable, target: >80)"
      EXIT_CODE=$(( EXIT_CODE > 0 ? EXIT_CODE : 1 ))
    else
      log_error "Health Score: $HEALTH_SCORE/100 (unhealthy, minimum: >$HEALTH_SCORE_MIN)"
      ISSUES+=("health_score_critical")
      EXIT_CODE=2
    fi
  fi
else
  log_error "Health score check failed: $HEALTH_JSON"
  ISSUES+=("health_check_error")
  EXIT_CODE=2
fi

# 6. Check Graph Connectivity (verbose only)
if [[ "$VERBOSE" == "true" && "$JSON_OUTPUT" == "false" ]]; then
  log_info "Checking graph connectivity (verbose mode)..."
  if CONNECTIVITY=$(leann index validate "$INDEX" --metric connectivity --json 2>&1 | jq -r '.score // empty'); then
    if [[ -n "$CONNECTIVITY" ]]; then
      RESULTS["connectivity"]="$CONNECTIVITY"
      if (( $(echo "$CONNECTIVITY >= 0.70" | bc -l) )); then
        log_success "Graph Connectivity: $CONNECTIVITY (well-connected)"
      else
        log_warning "Graph Connectivity: $CONNECTIVITY (sparse, consider increasing M parameter)"
      fi
    fi
  fi
fi

# Summary
if [[ "$JSON_OUTPUT" == "false" ]]; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""

  if [[ "${#ISSUES[@]}" -eq 0 && "${#WARNINGS[@]}" -eq 0 ]]; then
    log_success "Index is healthy!"
  elif [[ "${#ISSUES[@]}" -eq 0 ]]; then
    log_warning "Index has ${#WARNINGS[@]} warning(s)"
  else
    log_error "Index has ${#ISSUES[@]} critical issue(s) and ${#WARNINGS[@]} warning(s)"
  fi

  # Print recommendations
  if [[ "${#RECOMMENDATIONS[@]}" -gt 0 ]]; then
    echo ""
    echo "Recommendations:"
    for rec in "${RECOMMENDATIONS[@]}"; do
      echo "  • $rec"
    done
  fi

  echo ""
fi

# Attempt repairs if requested
if [[ "$REPAIR" == "true" && "${#ISSUES[@]}" -gt 0 ]]; then
  log_info "Attempting automatic repairs..."

  if [[ " ${ISSUES[*]} " =~ " coverage_too_low " ]]; then
    log_info "Rebuilding index with increased anchor count..."
    CURRENT_ANCHORS=$(leann index stats "$INDEX" --json | jq -r '.anchorCount // 0')
    NEW_ANCHORS=$(( CURRENT_ANCHORS * 2 ))

    if leann index rebuild \
      --index "$INDEX" \
      --new-anchor-count "$NEW_ANCHORS" \
      --output "${INDEX}.repaired" 2>&1; then

      log_success "Repaired index saved to: ${INDEX}.repaired"
      log_info "Validate with: $0 ${INDEX}.repaired"
    else
      log_error "Rebuild failed. Manual intervention required."
    fi
  fi

  if [[ " ${WARNINGS[*]} " =~ " delta_index_large " ]]; then
    log_info "Triggering full index rebuild (delta index too large)..."
    if leann index rebuild \
      --index "$INDEX" \
      --output "${INDEX}.rebuilt" 2>&1; then

      log_success "Rebuilt index saved to: ${INDEX}.rebuilt"
      log_info "Validate with: $0 ${INDEX}.rebuilt"
    else
      log_error "Rebuild failed. Manual intervention required."
    fi
  fi
fi

# JSON output
if [[ "$JSON_OUTPUT" == "true" ]]; then
  jq -n \
    --arg index "$INDEX" \
    --arg health_score "${RESULTS[health_score]:-null}" \
    --arg coverage "${RESULTS[coverage]:-null}" \
    --arg quant_error "${RESULTS[quantization_error]:-null}" \
    --arg balance "${RESULTS[balance]:-null}" \
    --arg delta_ratio "${RESULTS[delta_ratio]:-null}" \
    --arg connectivity "${RESULTS[connectivity]:-null}" \
    --argjson issues "$(printf '%s\n' "${ISSUES[@]}" | jq -R . | jq -s .)" \
    --argjson warnings "$(printf '%s\n' "${WARNINGS[@]}" | jq -R . | jq -s .)" \
    --argjson recommendations "$(printf '%s\n' "${RECOMMENDATIONS[@]}" | jq -R . | jq -s .)" \
    --arg exit_code "$EXIT_CODE" \
    '{
      index: $index,
      timestamp: (now | strftime("%Y-%m-%dT%H:%M:%SZ")),
      health_score: ($health_score | tonumber?),
      metrics: {
        coverage: ($coverage | tonumber?),
        quantization_error: ($quant_error | tonumber?),
        utilization_balance: ($balance | tonumber?),
        delta_index_ratio: ($delta_ratio | tonumber?),
        connectivity: ($connectivity | tonumber?)
      },
      issues: $issues,
      warnings: $warnings,
      recommendations: $recommendations,
      exit_code: ($exit_code | tonumber)
    }'
fi

exit "$EXIT_CODE"
