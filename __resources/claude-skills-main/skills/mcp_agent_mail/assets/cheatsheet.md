# MCP Agent Mail - Quick Command Cheatsheet

One-page reference for most common operations.

---

## Agent Management

```bash
# Register new agent
agent-mail agents register \
  --id claude-architect-1 \
  --name "Claude Architect" \
  --role architect \
  --capabilities "system-design,typescript,python"

# Update agent status
agent-mail agents status --id <agent-id> --status active|idle|busy|offline

# List agents
agent-mail agents list                    # All agents
agent-mail agents list --role implementer # By role
agent-mail agents list --status active    # By status
agent-mail agents search --capability react

# Get agent info
agent-mail agents info --id <agent-id>
```

---

## Messaging

```bash
# Send direct message
agent-mail send \
  --from <my-agent-id> \
  --to <recipient-id> \
  --subject "Code review request" \
  --body "Please review PR #123" \
  --priority normal|high|urgent|low \
  --type request|response|task|update|question|notification

# Send broadcast
agent-mail broadcast \
  --subject "Deployment complete" \
  --body "Version 2.0 deployed to production" \
  --priority normal

# Reply to message
agent-mail reply --message-id <msg-id> --body "Acknowledged"

# List messages
agent-mail messages list                  # All messages
agent-mail messages list --unread         # Unread only
agent-mail messages list --priority urgent
agent-mail messages list --thread <thread-id>

# Mark as read
agent-mail messages read --id <msg-id>
```

---

## File Reservations

```bash
# Check reservation status
agent-mail reserve check <path>

# Reserve file (exclusive)
agent-mail reserve <path> \
  --agent <agent-id> \
  --purpose edit|read|delete|create|refactor \
  --mode exclusive \
  --expires-in 3600

# Reserve file (shared)
agent-mail reserve <path> \
  --agent <agent-id> \
  --purpose read \
  --mode shared \
  --expires-in 1800

# Release reservation
agent-mail release <reservation-id>
agent-mail release --agent <agent-id> --all

# List reservations
agent-mail reservations list              # All active
agent-mail reservations list --agent <id> # By agent
agent-mail reservations list --path <path>
agent-mail reservations audit --stale     # Find stale

# Extend reservation
agent-mail extend <reservation-id> --seconds 1800
```

---

## Threads

```bash
# Create thread
agent-mail threads create \
  --subject "Architecture discussion" \
  --participants agent-a,agent-b,agent-c

# List threads
agent-mail threads list                   # All threads
agent-mail threads list --status active
agent-mail threads list --participant <agent-id>

# Get thread messages
agent-mail threads messages --id <thread-id>

# Close thread
agent-mail threads close --id <thread-id> \
  --summary "Decision: Use microservices"
```

---

## Product Bus (Events)

```bash
# Emit event
agent-mail events emit \
  --product user-service \
  --event deployment \
  --data '{"version":"2.0","env":"production"}'

# Subscribe to events
agent-mail events subscribe \
  --product api-gateway \
  --events build_failure,breaking_change

# List subscriptions
agent-mail events subscriptions --agent <agent-id>
```

---

## Server Management

```bash
# Start server
agent-mail server start --port 9743

# Check server status
agent-mail server status
agent-mail server health
agent-mail server ping

# Stop server
agent-mail server stop

# View logs
agent-mail server logs --tail 100
agent-mail server logs --follow
```

---

## TypeScript API

### Agent Registration
```typescript
await tools.agent_mail.registerAgent({
  agent: {
    id: "claude-architect-1",
    name: "Claude Architect",
    role: "architect",
    capabilities: ["system-design", "typescript"],
    contactPolicy: {
      acceptsDirectMessages: true,
      acceptsBroadcasts: true,
      priority: ["urgent", "high", "normal"],
      autoRespond: true
    },
    status: "active"
  }
});
```

### Send Message
```typescript
await tools.agent_mail.sendMessage({
  from: "agent-a",
  to: "agent-b",
  subject: "Code review request",
  body: {
    text: "Please review PR #123",
    files: ["/src/feature.ts"]
  },
  priority: "normal",
  type: "request"
});
```

### Reserve File
```typescript
const reservation = await tools.agent_mail.reserveFile({
  agentId: "agent-a",
  path: "/src/auth.ts",
  purpose: "refactor",
  mode: "exclusive",
  expiresIn: 3600
});
```

### Release File
```typescript
await tools.agent_mail.releaseReservation({
  reservationId: reservation.id
});
```

---

## Common Workflows

### Task Assignment Flow
```bash
# 1. Coordinator sends task
agent-mail send --to implementer \
  --subject "Task: Implement OAuth2" \
  --type task \
  --priority high

# 2. Implementer acknowledges
agent-mail reply --message-id <msg-id> \
  --body "Acknowledged. ETA: 2 days"

# 3. Implementer reserves files
agent-mail reserve /src/auth/ \
  --agent implementer \
  --purpose create

# 4. Implementer completes work
# ... do work ...

# 5. Implementer sends update
agent-mail send --to coordinator \
  --subject "Task complete" \
  --type update

# 6. Implementer releases files
agent-mail release <reservation-id>
```

### Code Review Flow
```bash
# 1. Request review
agent-mail send --to reviewer \
  --subject "Review Request: PR #123" \
  --type request

# 2. Reviewer acknowledges
agent-mail reply --message-id <msg-id> \
  --body "Starting review"

# 3. Reviewer provides feedback
agent-mail reply --message-id <msg-id> \
  --body "Found 2 issues: ..."

# 4. Author fixes and notifies
agent-mail send --to reviewer \
  --subject "Re: Review - Addressed feedback" \
  --type update

# 5. Reviewer approves
agent-mail reply --message-id <msg-id> \
  --body "APPROVED"
```

### Emergency Hotfix Flow
```bash
# 1. Broadcast emergency
agent-mail broadcast \
  --subject "🚨 EMERGENCY: Production down" \
  --priority urgent \
  --body "Stop work. Release reservations."

# 2. All agents release
agent-mail release --agent <my-id> --all

# 3. Hotfix agent reserves critical files
agent-mail reserve /src/critical.ts \
  --agent hotfix \
  --purpose edit \
  --mode exclusive

# 4. Apply fix
# ... fix ...

# 5. Broadcast all-clear
agent-mail broadcast \
  --subject "✓ RESOLVED" \
  --priority high \
  --body "Resume normal operations"
```

---

## Priority Levels

| Priority | Response Time | Use Case |
|----------|---------------|----------|
| **urgent** | < 5 min | Production incident, critical blocker |
| **high** | < 1 hour | Important bug, release blocker |
| **normal** | Same day | Standard requests, code reviews |
| **low** | Best effort | FYI updates, suggestions |

---

## Reservation Modes

| Mode | Access | Use Case |
|------|--------|----------|
| **exclusive** | Only reserving agent | Editing, refactoring, deleting |
| **shared** | Multiple readers, no writers | Analysis, research, reading |

---

## Environment Variables

```bash
# Server configuration
export AGENT_MAIL_HOST=localhost
export AGENT_MAIL_PORT=9743
export AGENT_MAIL_WS=ws://localhost:9743/ws

# Storage
export AGENT_MAIL_DB_PATH=~/.agent-mail/data.db
export AGENT_MAIL_ARCHIVE_PATH=~/.agent-mail/archive/

# Logging
export AGENT_MAIL_LOG_LEVEL=info|debug|warn|error

# Defaults
export AGENT_MAIL_MESSAGE_EXPIRY_DAYS=30
export AGENT_MAIL_RESERVATION_EXPIRY_MINUTES=60
export AGENT_MAIL_MAX_THREAD_DEPTH=10
```

---

## Common Flags

```bash
# Output formats
--format json              # JSON output
--format table             # Table output
--format csv               # CSV output

# Filtering
--status active|idle|busy|offline
--priority urgent|high|normal|low
--type request|response|task|update|question|notification

# Options
--verbose                  # Detailed output
--quiet                    # Minimal output
--force                    # Force action (use with caution)
--all                      # Apply to all matching items
```

---

## Troubleshooting Quick Fixes

```bash
# Server not responding
agent-mail server status
agent-mail server restart

# Messages not delivered
agent-mail messages list --unread --verbose

# File can't be reserved
agent-mail reserve check <path>
# → Contact reservation owner or wait for expiry

# Stale reservations
agent-mail reservations audit --stale
agent-mail release <id> --force  # Coordinator only

# Database issues
sqlite3 ~/.agent-mail/data.db "PRAGMA integrity_check;"

# Archive issues
cd ~/.agent-mail/archive && git status
```

---

## Best Practices Summary

### Communication
- ✅ Use clear, descriptive subjects
- ✅ Choose appropriate priority
- ✅ Include context (files, PRs, rationale)
- ✅ Acknowledge important messages

### File Reservations
- ✅ Always check before reserving
- ✅ Reserve only what you'll modify
- ✅ Set expiry times
- ✅ Release immediately after work

### Coordination
- ✅ Announce intent before major work
- ✅ Update progress on long tasks
- ✅ Document decisions in threads
- ✅ Respect others' reservations

---

## Quick Links

- **Full Skill Guide:** `/mcp_agent_mail/SKILL.md`
- **Messaging Patterns:** `/mcp_agent_mail/references/messaging-patterns.md`
- **Reservation Protocol:** `/mcp_agent_mail/references/reservation-protocol.md`
- **Codebase Docs:** `/mcp_agent_mail-codebase/README.md`
- **Coordination Principles:** `/mcp_agent_mail-codebase/principles/agent-coordination.md`
- **Workflow Templates:** `/mcp_agent_mail-codebase/templates/coordination-workflow.md`

---

## Emergency Contacts

```bash
# Check server health
./scripts/server-health.sh --verbose

# Get help
agent-mail --help
agent-mail <command> --help

# Report issues
agent-mail send --to coordinator \
  --priority urgent \
  --subject "Issue: [description]"
```

---

**Remember:** Use mcp_agent_mail for ANY multi-agent coordination to prevent conflicts and ensure smooth collaboration!
