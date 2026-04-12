#!/bin/bash
# MCP Agent Mail - Server Health Check Script
# Usage: ./server-health.sh [--verbose]

set -euo pipefail

# Configuration
AGENT_MAIL_HOST="${AGENT_MAIL_HOST:-localhost}"
AGENT_MAIL_PORT="${AGENT_MAIL_PORT:-9743}"
AGENT_MAIL_WS="${AGENT_MAIL_WS:-ws://localhost:9743/ws}"
VERBOSE=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
for arg in "$@"; do
  case $arg in
    --verbose|-v)
      VERBOSE=true
      shift
      ;;
  esac
done

# Helper functions
log_info() {
  echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
  echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
  echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
  echo -e "${RED}✗${NC} $1"
}

verbose_log() {
  if [ "$VERBOSE" = true ]; then
    echo -e "${BLUE}[DEBUG]${NC} $1"
  fi
}

# Check functions
check_server_process() {
  log_info "Checking server process..."

  if pgrep -f "agent-mail.*serve" > /dev/null; then
    local pid=$(pgrep -f "agent-mail.*serve" | head -1)
    log_success "Server process running (PID: $pid)"
    return 0
  else
    log_error "Server process not found"
    return 1
  fi
}

check_http_endpoint() {
  log_info "Checking HTTP endpoint..."

  local url="http://${AGENT_MAIL_HOST}:${AGENT_MAIL_PORT}/health"
  verbose_log "Connecting to: $url"

  if command -v curl > /dev/null; then
    local response=$(curl -s -w "\n%{http_code}" --max-time 5 "$url" 2>&1 || echo "000")
    local http_code=$(echo "$response" | tail -1)
    local body=$(echo "$response" | sed '$d')

    verbose_log "HTTP Status: $http_code"
    verbose_log "Response: $body"

    if [ "$http_code" = "200" ]; then
      log_success "HTTP endpoint healthy"

      if [ "$VERBOSE" = true ] && [ -n "$body" ]; then
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
      fi

      return 0
    else
      log_error "HTTP endpoint returned status $http_code"
      return 1
    fi
  else
    log_warning "curl not found, skipping HTTP check"
    return 2
  fi
}

check_websocket_endpoint() {
  log_info "Checking WebSocket endpoint..."

  verbose_log "Connecting to: $AGENT_MAIL_WS"

  # Simple WebSocket check using curl with upgrade headers
  if command -v curl > /dev/null; then
    local response=$(curl -s -i -N \
      -H "Connection: Upgrade" \
      -H "Upgrade: websocket" \
      -H "Sec-WebSocket-Version: 13" \
      -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
      --max-time 5 \
      "http://${AGENT_MAIL_HOST}:${AGENT_MAIL_PORT}/ws" 2>&1 || echo "")

    if echo "$response" | grep -q "101 Switching Protocols\|Upgrade: websocket"; then
      log_success "WebSocket endpoint available"
      return 0
    else
      log_error "WebSocket endpoint not responding"
      verbose_log "$response"
      return 1
    fi
  else
    log_warning "curl not found, skipping WebSocket check"
    return 2
  fi
}

check_database() {
  log_info "Checking database..."

  local db_path="${AGENT_MAIL_DB_PATH:-$HOME/.agent-mail/data.db}"
  verbose_log "Database path: $db_path"

  if [ ! -f "$db_path" ]; then
    log_error "Database file not found at $db_path"
    return 1
  fi

  if command -v sqlite3 > /dev/null; then
    # Check database integrity
    local integrity=$(sqlite3 "$db_path" "PRAGMA integrity_check;" 2>&1)

    if [ "$integrity" = "ok" ]; then
      log_success "Database integrity OK"

      if [ "$VERBOSE" = true ]; then
        # Get table counts
        echo ""
        echo "Database Statistics:"
        echo "==================="
        sqlite3 "$db_path" "SELECT 'Agents: ' || COUNT(*) FROM agents;"
        sqlite3 "$db_path" "SELECT 'Messages: ' || COUNT(*) FROM messages;"
        sqlite3 "$db_path" "SELECT 'Active Reservations: ' || COUNT(*) FROM reservations WHERE status = 'active';"
        sqlite3 "$db_path" "SELECT 'Threads: ' || COUNT(*) FROM threads;"
      fi

      return 0
    else
      log_error "Database integrity check failed"
      verbose_log "$integrity"
      return 1
    fi
  else
    log_warning "sqlite3 not found, skipping database check"
    return 2
  fi
}

check_git_archive() {
  log_info "Checking Git archive..."

  local archive_path="${AGENT_MAIL_ARCHIVE_PATH:-$HOME/.agent-mail/archive}"
  verbose_log "Archive path: $archive_path"

  if [ ! -d "$archive_path" ]; then
    log_error "Archive directory not found at $archive_path"
    return 1
  fi

  if [ ! -d "$archive_path/.git" ]; then
    log_warning "Archive directory is not a Git repository"
    return 2
  fi

  # Check if git repo is healthy
  if git -C "$archive_path" status > /dev/null 2>&1; then
    log_success "Git archive healthy"

    if [ "$VERBOSE" = true ]; then
      echo ""
      echo "Archive Statistics:"
      echo "==================="
      echo "Commits: $(git -C "$archive_path" rev-list --count HEAD 2>/dev/null || echo '0')"
      echo "Size: $(du -sh "$archive_path" 2>/dev/null | cut -f1)"
      echo "Last commit: $(git -C "$archive_path" log -1 --format='%cr' 2>/dev/null || echo 'N/A')"
    fi

    return 0
  else
    log_error "Git archive is corrupted"
    return 1
  fi
}

check_disk_space() {
  log_info "Checking disk space..."

  local data_dir="${AGENT_MAIL_DB_PATH:-$HOME/.agent-mail}"
  data_dir=$(dirname "$data_dir")

  if command -v df > /dev/null; then
    local usage=$(df -h "$data_dir" | tail -1 | awk '{print $5}' | sed 's/%//')

    verbose_log "Disk usage: ${usage}%"

    if [ "$usage" -lt 80 ]; then
      log_success "Disk space OK (${usage}% used)"
      return 0
    elif [ "$usage" -lt 90 ]; then
      log_warning "Disk space getting low (${usage}% used)"
      return 1
    else
      log_error "Disk space critical (${usage}% used)"
      return 1
    fi
  else
    log_warning "df not found, skipping disk space check"
    return 2
  fi
}

check_stale_reservations() {
  log_info "Checking for stale reservations..."

  local db_path="${AGENT_MAIL_DB_PATH:-$HOME/.agent-mail/data.db}"

  if [ ! -f "$db_path" ] || ! command -v sqlite3 > /dev/null; then
    log_warning "Cannot check reservations (database or sqlite3 not available)"
    return 2
  fi

  # Find reservations older than 2 hours that are still active
  local stale_count=$(sqlite3 "$db_path" "
    SELECT COUNT(*) FROM reservations
    WHERE status = 'active'
    AND datetime(created_at) < datetime('now', '-2 hours')
  " 2>/dev/null || echo "0")

  verbose_log "Stale reservations: $stale_count"

  if [ "$stale_count" -eq 0 ]; then
    log_success "No stale reservations"
    return 0
  else
    log_warning "Found $stale_count stale reservation(s)"

    if [ "$VERBOSE" = true ]; then
      echo ""
      echo "Stale Reservations:"
      echo "==================="
      sqlite3 "$db_path" "
        SELECT
          path,
          agent_id,
          purpose,
          datetime(created_at) as created,
          ROUND((julianday('now') - julianday(created_at)) * 24, 1) as hours_old
        FROM reservations
        WHERE status = 'active'
        AND datetime(created_at) < datetime('now', '-2 hours')
        ORDER BY created_at
      " | column -t -s'|'
    fi

    return 1
  fi
}

check_unread_urgent_messages() {
  log_info "Checking for unread urgent messages..."

  local db_path="${AGENT_MAIL_DB_PATH:-$HOME/.agent-mail/data.db}"

  if [ ! -f "$db_path" ] || ! command -v sqlite3 > /dev/null; then
    log_warning "Cannot check messages (database or sqlite3 not available)"
    return 2
  fi

  # Find urgent messages unread for more than 10 minutes
  local urgent_count=$(sqlite3 "$db_path" "
    SELECT COUNT(*) FROM messages
    WHERE priority = 'urgent'
    AND json_array_length(read_by) = 0
    AND datetime(timestamp) < datetime('now', '-10 minutes')
  " 2>/dev/null || echo "0")

  verbose_log "Unread urgent messages: $urgent_count"

  if [ "$urgent_count" -eq 0 ]; then
    log_success "No unread urgent messages"
    return 0
  else
    log_warning "Found $urgent_count unread urgent message(s)"

    if [ "$VERBOSE" = true ]; then
      echo ""
      echo "Unread Urgent Messages:"
      echo "======================="
      sqlite3 "$db_path" "
        SELECT
          from_agent,
          subject,
          datetime(timestamp) as sent,
          ROUND((julianday('now') - julianday(timestamp)) * 1440, 0) as minutes_old
        FROM messages
        WHERE priority = 'urgent'
        AND json_array_length(read_by) = 0
        AND datetime(timestamp) < datetime('now', '-10 minutes')
        ORDER BY timestamp
      " | column -t -s'|'
    fi

    return 1
  fi
}

# Main health check
main() {
  echo "======================================"
  echo "  MCP Agent Mail - Health Check"
  echo "======================================"
  echo ""

  local exit_code=0
  local warnings=0
  local errors=0

  # Run all checks
  check_server_process || ((errors++))
  echo ""

  check_http_endpoint || ((errors++))
  echo ""

  check_websocket_endpoint || { local ws_status=$?; [ $ws_status -eq 1 ] && ((errors++)) || ((warnings++)); }
  echo ""

  check_database || { local db_status=$?; [ $db_status -eq 1 ] && ((errors++)) || ((warnings++)); }
  echo ""

  check_git_archive || { local git_status=$?; [ $git_status -eq 1 ] && ((errors++)) || ((warnings++)); }
  echo ""

  check_disk_space || ((warnings++))
  echo ""

  check_stale_reservations || ((warnings++))
  echo ""

  check_unread_urgent_messages || ((warnings++))
  echo ""

  # Summary
  echo "======================================"
  echo "  Summary"
  echo "======================================"

  if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    log_success "All checks passed! Server is healthy."
    exit_code=0
  elif [ $errors -eq 0 ]; then
    log_warning "$warnings warning(s) detected. Server operational but needs attention."
    exit_code=1
  else
    log_error "$errors error(s) and $warnings warning(s) detected. Server has issues!"
    exit_code=2
  fi

  echo ""
  echo "Server: ${AGENT_MAIL_HOST}:${AGENT_MAIL_PORT}"
  echo "Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"

  return $exit_code
}

# Run main function
main
exit $?
