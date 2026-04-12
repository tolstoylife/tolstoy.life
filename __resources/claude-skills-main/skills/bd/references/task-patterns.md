# Common Task Patterns

Quick reference for frequently used bd task operations.

## Issue Creation Patterns

### Basic Task

```bash
bd create "Task title"
bd create "Task title" --type task
```

### Bug Report

```bash
bd create "Bug: Login fails on Safari" \
  --type bug \
  --priority 1 \
  --labels backend,browser \
  --description "Steps to reproduce: ..."
```

### Feature Request

```bash
bd create "Add dark mode" \
  --type feature \
  --priority 2 \
  --assignee alice \
  --acceptance "- Dark mode toggle in settings
- Persists across sessions
- Applies to all pages"
```

### Epic with Subtasks

```bash
# Create epic
bd create "Redesign authentication" --type epic --priority 0

# Create subtasks
EPIC="bd-1"
bd create "Design auth schema" --parent $EPIC
bd create "Implement backend" --parent $EPIC --deps bd-2
bd create "Update frontend" --parent $EPIC --deps bd-3
```

### Chore/Maintenance

```bash
bd create "Upgrade dependencies" \
  --type chore \
  --priority 3 \
  --labels tech-debt
```

## Status Update Patterns

### Start Work

```bash
bd update bd-5 --status in_progress
bd comment bd-5 "Starting implementation"
```

### Mark Blocked

```bash
bd update bd-5 --status blocked
bd comment bd-5 "Waiting on API design approval (bd-3)"
```

### Complete Work

```bash
bd close bd-5
bd comment bd-5 "Completed in commit abc123"
```

### Reopen

```bash
bd reopen bd-5
bd comment bd-5 "Bug regressed in v2.1.0"
```

## Dependency Patterns

### Sequential Work

```bash
# Design -> Implementation -> Tests
bd create "Design API" --priority 0
bd create "Implement API" --deps bd-1
bd create "Write tests" --deps bd-2
```

### Parallel Work with Shared Dependency

```bash
# Infrastructure required by multiple features
bd create "Setup Redis" --priority 0
bd create "Cache sessions" --deps bd-1
bd create "Cache API responses" --deps bd-1
# bd-2 and bd-3 can be parallel after bd-1
```

### Discovery Tracking

```bash
# Found while working on bd-10
bd create "Fix edge case in parser" \
  --type bug \
  --deps discovered-from:bd-10
```

### Blocking Relationships

```bash
# This blocks that
bd dep add bd-5 blocks bd-7
bd dep add bd-5 blocks bd-8

# Check what's blocked
bd blocked
```

## Query Patterns

### My Work

```bash
bd list --assignee $USER --status open,in_progress
```

### High Priority Open Issues

```bash
bd list --status open --priority-min 0 --priority-max 1 --sort priority
```

### Sprint Work

```bash
bd list --label sprint-5
bd list --label sprint-5 --status open  # Remaining work
```

### Ready to Start

```bash
bd ready
bd ready --assignee alice  # Alice's unblocked work
```

### Blocked Issues

```bash
bd blocked
bd blocked --assignee bob  # Bob's blocked issues
```

### Recent Activity

```bash
bd list --updated-after $(date -u -d '7 days ago' +%Y-%m-%d)
bd list --created-after $(date -u -d '1 day ago' +%Y-%m-%d)
```

### Unassigned Work

```bash
bd list --status open --no-assignee --sort priority
```

### Issues Needing Attention

```bash
bd list --empty-description --status open  # Missing details
bd stale --older-than 30d                   # Not updated recently
```

## Label Patterns

### Add Labels

```bash
bd label add urgent bd-5
bd label add backend,security bd-5,bd-7,bd-9
```

### Remove Labels

```bash
bd label remove urgent bd-5
```

### Query by Labels

```bash
bd list --label backend              # Must have backend
bd list --label backend,security     # Must have BOTH
bd list --label-any urgent,high      # Must have AT LEAST ONE
```

### Label Taxonomy

Common label schemes:

```bash
# Component labels
backend, frontend, infra, database, api, ui

# Priority labels
urgent, high, medium, low

# Type labels (in addition to --type)
bug, feature, enhancement, refactor, docs

# Status labels
needs-review, needs-testing, needs-design

# Sprint labels
sprint-1, sprint-2, Q1-2024, Q2-2024

# Team labels
team-platform, team-product, team-infra
```

## Batch Operations

### Update Multiple Issues

```bash
bd update bd-1,bd-2,bd-3 --priority 0
bd update bd-5,bd-7,bd-9 --assignee alice
bd close bd-10,bd-11,bd-12
```

### Add Label to Multiple Issues

```bash
bd label add sprint-5 bd-1,bd-2,bd-3,bd-4,bd-5
```

### Bulk Create from File

```bash
cat > tasks.md <<EOF
# Tasks

## Task 1
Type: task
Priority: 1

## Task 2
Type: feature
Priority: 2
EOF

bd create --file tasks.md
```

## Comment Patterns

### Progress Update

```bash
bd comment bd-5 "Completed authentication logic, starting tests"
```

### Blocker Information

```bash
bd comment bd-5 "Blocked: Waiting on API spec from design team"
```

### Link to Resources

```bash
bd comment bd-5 "Design doc: https://docs.example.com/auth-redesign"
bd comment bd-5 "PR: https://github.com/org/repo/pull/123"
```

### Multi-line Comment

```bash
bd comment bd-5 --body "## Progress Update

Completed:
- JWT token generation
- Refresh token flow

In Progress:
- Rate limiting
- Token revocation

Blocked:
- Waiting on Redis setup (bd-3)"
```

## Git Integration Patterns

### Issue in Commit Message

```bash
git commit -m "Implement JWT auth (bd-5)"
git commit -m "Fix login bug (closes bd-12)"
```

### Commit Issues Together

```bash
# Work on code
git add src/

# Commit code and issues together
git add .beads/
git commit -m "Add authentication system

Closes bd-5, bd-7
Blocked on bd-3"
```

### Branch Naming

```bash
git checkout -b bd-5-jwt-auth
git checkout -b issue/bd-12-login-fix
```

## Export/Import Patterns

### Backup All Issues

```bash
bd export > backup-$(date +%Y%m%d).jsonl
```

### Export Subset

```bash
bd export --status closed --created-after 2024-01-01 > archive-2024.jsonl
```

### Import Issues

```bash
bd import backup-20240102.jsonl
```

### Migrate Between Repos

```bash
bd migrate-issues --from ~/old-project --to ~/new-project
```

## Search Patterns

### Text Search

```bash
bd search "authentication"
bd search "JWT"
```

### Filter + Search

```bash
bd list --status open --title-contains "login"
bd list --desc-contains "security" --label backend
```

### JSON Processing

```bash
# Count by priority
bd list --json | jq 'group_by(.priority) | map({priority: .[0].priority, count: length})'

# Find issues with no dependencies
bd list --json | jq '.[] | select(.dependencies | length == 0)'

# Extract issue IDs
bd list --status open --json | jq -r '.[].id'
```

## Daemon Patterns

### Check Daemon Status

```bash
bd daemon status
```

### Restart Daemon

```bash
bd daemon stop
bd daemon start
```

### Force Direct Mode

```bash
bd --no-daemon list
bd --no-daemon create "New issue"
```

## Visualization Patterns

### Interactive Graph

```bash
bv .beads/beads.jsonl
```

### Dependency Tree

```bash
bd dep tree bd-1
bd dep tree bd-1 --long  # More detail
```

### Export Graph

```bash
# Graphviz DOT
bd list --format dot > issues.dot
dot -Tpng -o issues.png issues.dot

# Digraph format
bd list --format digraph > issues.txt
```

## Cleanup Patterns

### Compact Old Issues

```bash
bd compact --older-than 90d
```

### Delete Closed Issues

```bash
bd cleanup --older-than 30d
```

### Purge Issue Completely

```bash
bd delete bd-5 --purge  # Removes from JSONL too
```

### Clean Git Artifacts

```bash
bd clean  # Remove merge artifacts
```

## Health Check Patterns

### Quick Validation

```bash
bd validate
```

### Full Health Check

```bash
bd doctor
```

### Repair Dependencies

```bash
bd repair-deps --dry-run  # Preview
bd repair-deps            # Execute
```

### Detect Cycles

```bash
bd dep cycles
```

### Check for Duplicates

```bash
bd duplicates
bd duplicates --auto-merge
```

## Template Patterns

### Create Template

```bash
bd template create bug-report \
  --type bug \
  --priority 2 \
  --description "## Steps to Reproduce\n\n## Expected\n\n## Actual"
```

### Use Template

```bash
bd create "New bug" --from-template bug-report
```

### List Templates

```bash
bd template list
```

## Multi-Repo Patterns

### Configure Repos

```bash
bd repo add backend ~/repos/backend --prefix api
bd repo add frontend ~/repos/frontend --prefix ui
```

### Create in Specific Repo

```bash
bd create "Add endpoint" --repo backend
```

### Cross-Repo Dependencies

```bash
# In frontend repo
bd dep add ui-5 blocked_by api-10
```

## Agent Automation Patterns

### Find Ready Work

```bash
READY=$(bd ready --json --assignee agent)
ISSUE_ID=$(echo $READY | jq -r '.[0].id')
```

### Auto-Create from TODOs

```bash
rg "TODO:" --json | jq -c '.[] | select(.type == "match")' | \
while read line; do
  TEXT=$(echo $line | jq -r '.data.lines.text' | sed 's/.*TODO: //')
  bd create "$TEXT" --type task --labels auto-generated
done
```

### Batch Close Completed

```bash
bd list --status in_progress --json | jq -r '.[].id' | \
while read id; do
  # Check if actually complete (custom logic)
  if is_complete $id; then
    bd close $id
  fi
done
```

## Quick Reference

| Operation | Command |
|-----------|---------|
| Create task | `bd create "Title"` |
| Create with metadata | `bd create "Title" --type feature --priority 1 --assignee alice` |
| List open issues | `bd list --status open` |
| Update status | `bd update bd-5 --status in_progress` |
| Close issue | `bd close bd-5` |
| Add dependency | `bd dep add bd-1 blocks bd-2` |
| Show ready work | `bd ready` |
| Show blocked issues | `bd blocked` |
| Add comment | `bd comment bd-5 "Progress update"` |
| Add label | `bd label add urgent bd-5` |
| Search | `bd search "keyword"` |
| Export | `bd export > backup.jsonl` |
| Validate | `bd validate` |

## See Also

- [SKILL.md](../SKILL.md) - Complete skill documentation
- [daemon-mode.md](daemon-mode.md) - RPC and daemon integration
- [cheatsheet.md](../assets/cheatsheet.md) - One-page reference
