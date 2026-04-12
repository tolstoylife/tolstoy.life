#!/bin/bash
# issue-validator.sh - Validate bd issue structure and health
#
# Usage:
#   ./issue-validator.sh                    # Validate current repo
#   ./issue-validator.sh --db /path/to/db   # Validate specific database
#   ./issue-validator.sh --fix              # Attempt auto-repair

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BD_DB="${1:-}"
FIX_MODE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --db)
      BD_DB="$2"
      shift 2
      ;;
    --fix)
      FIX_MODE=true
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [--db /path/to/db] [--fix]"
      echo ""
      echo "Options:"
      echo "  --db PATH    Specify database path"
      echo "  --fix        Attempt to fix issues automatically"
      echo "  -h, --help   Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Helper functions
error() {
  echo -e "${RED}✗ ERROR:${NC} $1"
}

warning() {
  echo -e "${YELLOW}⚠ WARNING:${NC} $1"
}

success() {
  echo -e "${GREEN}✓ SUCCESS:${NC} $1"
}

info() {
  echo "ℹ INFO: $1"
}

# Check if bd is installed
if ! command -v bd &> /dev/null; then
  error "bd is not installed or not in PATH"
  exit 1
fi

# Find .beads directory
if [ -z "$BD_DB" ]; then
  if [ ! -d ".beads" ]; then
    error ".beads directory not found. Run 'bd init' first."
    exit 1
  fi
  BD_DIR=".beads"
else
  BD_DIR="$(dirname "$BD_DB")"
fi

info "Validating bd installation in: $BD_DIR"
echo ""

# Validation checks
ERRORS=0
WARNINGS=0

# 1. Check JSONL file exists
echo "1. Checking JSONL file..."
if [ -f "$BD_DIR/beads.jsonl" ]; then
  success "JSONL file exists"
else
  error "JSONL file missing: $BD_DIR/beads.jsonl"
  ((ERRORS++))
fi

# 2. Validate JSONL syntax
echo "2. Validating JSONL syntax..."
if command -v jq &> /dev/null; then
  if cat "$BD_DIR/beads.jsonl" 2>/dev/null | jq '.' > /dev/null 2>&1; then
    LINE_COUNT=$(wc -l < "$BD_DIR/beads.jsonl" | tr -d ' ')
    success "JSONL is valid ($LINE_COUNT events)"
  else
    error "JSONL has syntax errors"
    ((ERRORS++))
  fi
else
  warning "jq not found, skipping JSON validation"
  ((WARNINGS++))
fi

# 3. Check SQLite database
echo "3. Checking SQLite database..."
DB_FILE=$(find "$BD_DIR" -name "*.db" -type f 2>/dev/null | head -1)
if [ -n "$DB_FILE" ]; then
  success "Database found: $DB_FILE"

  # Check database integrity
  if command -v sqlite3 &> /dev/null; then
    if sqlite3 "$DB_FILE" "PRAGMA integrity_check;" | grep -q "ok"; then
      success "Database integrity OK"
    else
      error "Database integrity check failed"
      ((ERRORS++))
      if [ "$FIX_MODE" = true ]; then
        info "Attempting to rebuild database from JSONL..."
        rm -f "$DB_FILE"
        bd migrate
        success "Database rebuilt"
      fi
    fi
  else
    warning "sqlite3 not found, skipping integrity check"
    ((WARNINGS++))
  fi
else
  warning "No SQLite database found (JSONL-only mode?)"
  ((WARNINGS++))
fi

# 4. Check for dependency cycles
echo "4. Checking for dependency cycles..."
if bd dep cycles 2>&1 | grep -q "No cycles detected"; then
  success "No dependency cycles found"
else
  error "Dependency cycles detected!"
  bd dep cycles
  ((ERRORS++))
fi

# 5. Check for orphaned dependencies
echo "5. Checking for orphaned dependencies..."
if bd repair-deps --dry-run 2>&1 | grep -q "No orphaned"; then
  success "No orphaned dependencies"
else
  warning "Orphaned dependencies found"
  bd repair-deps --dry-run
  ((WARNINGS++))
  if [ "$FIX_MODE" = true ]; then
    info "Fixing orphaned dependencies..."
    bd repair-deps
    success "Orphaned dependencies removed"
  fi
fi

# 6. Check git configuration
echo "6. Checking git integration..."
if [ -f ".git/config" ]; then
  if git config --get merge.beads.driver > /dev/null 2>&1; then
    success "Git merge driver configured"
  else
    warning "Git merge driver not configured"
    ((WARNINGS++))
    if [ "$FIX_MODE" = true ]; then
      info "Installing git hooks..."
      bd hooks install
      success "Git hooks installed"
    fi
  fi
else
  warning "Not in a git repository"
  ((WARNINGS++))
fi

# 7. Check for stale issues
echo "7. Checking for stale issues..."
STALE_COUNT=$(bd stale --older-than 90d 2>/dev/null | wc -l | tr -d ' ')
if [ "$STALE_COUNT" -eq 0 ]; then
  success "No stale issues (>90 days)"
else
  warning "Found $STALE_COUNT stale issues (not updated in 90+ days)"
  ((WARNINGS++))
fi

# 8. Validate issue structure
echo "8. Validating issue structure..."
if bd validate 2>&1 | grep -q "All checks passed"; then
  success "All validation checks passed"
else
  error "Validation checks failed"
  bd validate
  ((ERRORS++))
fi

# 9. Check daemon status
echo "9. Checking daemon status..."
if bd daemon status 2>&1 | grep -q "running"; then
  success "Daemon is running"
else
  info "Daemon is not running (direct mode)"
fi

# 10. Database statistics
echo "10. Database statistics..."
if [ -f "$BD_DIR/beads.jsonl" ]; then
  TOTAL=$(bd count 2>/dev/null || echo "unknown")
  OPEN=$(bd count --status open 2>/dev/null || echo "unknown")
  CLOSED=$(bd count --status closed 2>/dev/null || echo "unknown")
  BLOCKED=$(bd blocked 2>/dev/null | wc -l | tr -d ' ')

  info "Total issues: $TOTAL"
  info "Open: $OPEN, Closed: $CLOSED, Blocked: $BLOCKED"
fi

# Summary
echo ""
echo "=========================================="
echo "Validation Summary"
echo "=========================================="

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
  success "All checks passed! ✓"
  exit 0
elif [ $ERRORS -eq 0 ]; then
  warning "Validation passed with $WARNINGS warning(s)"
  exit 0
else
  error "Validation failed with $ERRORS error(s) and $WARNINGS warning(s)"
  echo ""
  if [ "$FIX_MODE" = false ]; then
    info "Run with --fix to attempt automatic repairs"
  fi
  exit 1
fi
