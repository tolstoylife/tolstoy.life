#!/bin/bash
# search-validator.sh - Validate osgrep search results for relevance and quality
#
# Usage:
#   ./search-validator.sh "query" [min_score] [min_results]
#
# Examples:
#   ./search-validator.sh "authentication logic" 0.7 5
#   ./search-validator.sh "error handling" 0.6 10
#
# Exit codes:
#   0 - Validation passed
#   1 - No results or insufficient quality
#   2 - Invalid arguments

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default thresholds
DEFAULT_MIN_SCORE=0.6
DEFAULT_MIN_RESULTS=3

# Parse arguments
QUERY="${1:-}"
MIN_SCORE="${2:-$DEFAULT_MIN_SCORE}"
MIN_RESULTS="${3:-$DEFAULT_MIN_RESULTS}"

# Validation
if [[ -z "$QUERY" ]]; then
  echo -e "${RED}Error: Query is required${NC}"
  echo "Usage: $0 \"query\" [min_score] [min_results]"
  exit 2
fi

# Validate numeric parameters
if ! [[ "$MIN_SCORE" =~ ^[0-9]*\.?[0-9]+$ ]]; then
  echo -e "${RED}Error: min_score must be a number${NC}"
  exit 2
fi

if ! [[ "$MIN_RESULTS" =~ ^[0-9]+$ ]]; then
  echo -e "${RED}Error: min_results must be an integer${NC}"
  exit 2
fi

echo -e "${BLUE}=== osgrep Search Validation ===${NC}"
echo -e "${BLUE}Query:${NC} $QUERY"
echo -e "${BLUE}Min Score:${NC} $MIN_SCORE"
echo -e "${BLUE}Min Results:${NC} $MIN_RESULTS"
echo ""

# Check if osgrep is available
if ! command -v osgrep &> /dev/null; then
  echo -e "${RED}Error: osgrep not found in PATH${NC}"
  exit 2
fi

# Check osgrep health
echo -e "${BLUE}Checking osgrep installation...${NC}"
if ! osgrep doctor &> /dev/null; then
  echo -e "${RED}Error: osgrep doctor check failed${NC}"
  osgrep doctor
  exit 2
fi
echo -e "${GREEN}✓ osgrep is healthy${NC}"
echo ""

# Check if current directory is indexed
echo -e "${BLUE}Checking index status...${NC}"
CURRENT_DIR=$(pwd)
if ! osgrep list | grep -q "$CURRENT_DIR"; then
  echo -e "${YELLOW}Warning: Current directory not indexed${NC}"
  echo -e "${YELLOW}Run 'osgrep index' to create an index${NC}"
  exit 1
fi
echo -e "${GREEN}✓ Current directory is indexed${NC}"
echo ""

# Perform search with JSON output
echo -e "${BLUE}Searching for: \"$QUERY\"${NC}"
TEMP_FILE=$(mktemp)
if ! osgrep "$QUERY" --json --max-count 20 > "$TEMP_FILE" 2>&1; then
  echo -e "${RED}Error: osgrep search failed${NC}"
  cat "$TEMP_FILE"
  rm "$TEMP_FILE"
  exit 1
fi

# Parse JSON results
TOTAL_RESULTS=$(jq -r '.results | length' "$TEMP_FILE")
SEARCH_TIME=$(jq -r '.searchTime' "$TEMP_FILE")
STORE=$(jq -r '.store' "$TEMP_FILE")

echo -e "${BLUE}Results:${NC} $TOTAL_RESULTS found in ${SEARCH_TIME}ms"
echo -e "${BLUE}Store:${NC} $STORE"
echo ""

# Check if we have minimum results
if [[ "$TOTAL_RESULTS" -lt "$MIN_RESULTS" ]]; then
  echo -e "${RED}✗ Insufficient results: $TOTAL_RESULTS < $MIN_RESULTS${NC}"
  echo -e "${YELLOW}Suggestion: Try a broader query${NC}"
  rm "$TEMP_FILE"
  exit 1
fi

# Calculate score statistics
HIGH_SCORE=$(jq -r '.results | map(.score) | max' "$TEMP_FILE")
LOW_SCORE=$(jq -r '.results | map(.score) | min' "$TEMP_FILE")
AVG_SCORE=$(jq -r '.results | map(.score) | add / length' "$TEMP_FILE")
ABOVE_THRESHOLD=$(jq -r ".results | map(select(.score >= $MIN_SCORE)) | length" "$TEMP_FILE")

echo -e "${BLUE}=== Score Analysis ===${NC}"
echo -e "${BLUE}Highest:${NC} $HIGH_SCORE"
echo -e "${BLUE}Lowest:${NC} $LOW_SCORE"
echo -e "${BLUE}Average:${NC} $AVG_SCORE"
echo -e "${BLUE}Above threshold ($MIN_SCORE):${NC} $ABOVE_THRESHOLD / $TOTAL_RESULTS"
echo ""

# Check score quality
if [[ "$ABOVE_THRESHOLD" -lt "$MIN_RESULTS" ]]; then
  echo -e "${YELLOW}Warning: Only $ABOVE_THRESHOLD results above score threshold${NC}"
  echo -e "${YELLOW}Suggestion: Lower min_score or refine query${NC}"
fi

# Check if average score is reasonable
AVG_CHECK=$(awk -v avg="$AVG_SCORE" -v min="$MIN_SCORE" 'BEGIN {print (avg >= min) ? "pass" : "fail"}')
if [[ "$AVG_CHECK" == "fail" ]]; then
  echo -e "${YELLOW}Warning: Average score ($AVG_SCORE) below threshold ($MIN_SCORE)${NC}"
  echo -e "${YELLOW}Suggestion: Query may be too vague - add more context${NC}"
fi

# Display top results
echo -e "${BLUE}=== Top Results ===${NC}"
jq -r '.results[:5] | .[] |
  "\(.path):\(.line) (score: \(.score | tostring | .[0:4]))"' "$TEMP_FILE"
echo ""

# Score distribution
echo -e "${BLUE}=== Score Distribution ===${NC}"
EXCELLENT=$(jq -r '.results | map(select(.score >= 0.8)) | length' "$TEMP_FILE")
GOOD=$(jq -r '.results | map(select(.score >= 0.6 and .score < 0.8)) | length' "$TEMP_FILE")
FAIR=$(jq -r '.results | map(select(.score >= 0.4 and .score < 0.6)) | length' "$TEMP_FILE")
POOR=$(jq -r '.results | map(select(.score < 0.4)) | length' "$TEMP_FILE")

echo -e "Excellent (≥0.8): ${GREEN}$EXCELLENT${NC}"
echo -e "Good (0.6-0.8):   ${GREEN}$GOOD${NC}"
echo -e "Fair (0.4-0.6):   ${YELLOW}$FAIR${NC}"
echo -e "Poor (<0.4):      ${RED}$POOR${NC}"
echo ""

# File diversity check
UNIQUE_FILES=$(jq -r '.results | map(.path) | unique | length' "$TEMP_FILE")
echo -e "${BLUE}File Diversity:${NC} $UNIQUE_FILES unique files"

if [[ "$UNIQUE_FILES" -eq 1 ]] && [[ "$TOTAL_RESULTS" -gt 5 ]]; then
  echo -e "${YELLOW}Warning: All results from single file${NC}"
  echo -e "${YELLOW}Suggestion: Pattern may be localized, consider --per-file limit${NC}"
fi
echo ""

# Generate recommendations
echo -e "${BLUE}=== Recommendations ===${NC}"

if (( $(echo "$AVG_SCORE > 0.75" | bc -l) )); then
  echo -e "${GREEN}✓ High-quality results - query is well-targeted${NC}"
elif (( $(echo "$AVG_SCORE > 0.55" | bc -l) )); then
  echo -e "${YELLOW}○ Moderate-quality results - query is acceptable${NC}"
  echo -e "${YELLOW}  Consider adding more context for better precision${NC}"
else
  echo -e "${RED}✗ Low-quality results - query may be too vague${NC}"
  echo -e "${RED}  Suggestions:${NC}"
  echo -e "${RED}  - Add domain-specific terms${NC}"
  echo -e "${RED}  - Be more specific about intent${NC}"
  echo -e "${RED}  - Use compound concepts (e.g., 'JWT token validation')${NC}"
fi

if [[ "$TOTAL_RESULTS" -lt 5 ]]; then
  echo -e "${YELLOW}○ Few results - consider broadening query${NC}"
elif [[ "$TOTAL_RESULTS" -gt 30 ]]; then
  echo -e "${YELLOW}○ Many results - consider narrowing scope or using path filter${NC}"
fi

if [[ "$EXCELLENT" -gt 0 ]]; then
  echo -e "${GREEN}✓ Excellent matches found - check top results first${NC}"
fi

if [[ "$POOR" -gt $((TOTAL_RESULTS / 2)) ]]; then
  echo -e "${YELLOW}○ Many low-score results - query may be picking up noise${NC}"
fi

# Final validation
echo ""
echo -e "${BLUE}=== Validation Result ===${NC}"

if [[ "$ABOVE_THRESHOLD" -ge "$MIN_RESULTS" ]] && (( $(echo "$AVG_SCORE >= $MIN_SCORE" | bc -l) )); then
  echo -e "${GREEN}✓ PASSED${NC}"
  echo -e "${GREEN}Search quality meets requirements${NC}"
  rm "$TEMP_FILE"
  exit 0
else
  echo -e "${RED}✗ FAILED${NC}"
  if [[ "$ABOVE_THRESHOLD" -lt "$MIN_RESULTS" ]]; then
    echo -e "${RED}Insufficient high-scoring results${NC}"
  fi
  if (( $(echo "$AVG_SCORE < $MIN_SCORE" | bc -l) )); then
    echo -e "${RED}Average score below threshold${NC}"
  fi
  rm "$TEMP_FILE"
  exit 1
fi
