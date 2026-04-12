# bd Quick Reference Cheatsheet

## Installation & Setup

```bash
bd init                           # Initialize bd in current repo
bd config set prefix myapp        # Set custom issue prefix
bd daemon start                   # Start daemon (auto-starts by default)
bd hooks install                  # Install git hooks for auto-sync
```

## Issue Creation

```bash
bd create "Task title"                                    # Basic task
bd create "Bug fix" --type bug --priority 1              # Bug with priority
bd create "Feature" --type feature --assignee alice       # Feature with owner
bd create "Epic" --type epic                              # Epic for large work
bd create "Task" --parent bd-1                            # Subtask of epic
bd create "Task" --deps bd-1,bd-2                         # With dependencies
bd create --from-template bug-report                      # From template
bd create --file issues.md                                # Bulk from file
```

## Listing & Filtering

```bash
bd list                                       # All issues
bd list --status open                         # Open issues
bd list --status open,in_progress             # Multiple statuses
bd list --assignee alice                      # Alice's issues
bd list --priority-min 0 --priority-max 1     # High priority (0-1)
bd list --label backend                       # With backend label
bd list --label-any urgent,high               # With urgent OR high
bd list --no-assignee                         # Unassigned
bd list --empty-description                   # Missing descriptions
bd list --created-after 2024-01-01            # Created after date
bd list --sort priority --reverse             # Sort by priority desc
bd list --limit 10                            # First 10 results
bd list --json                                # JSON output
bd list --long                                # Detailed view
```

## Issue Updates

```bash
bd update bd-5 --status in_progress           # Change status
bd update bd-5 --priority 0                   # Change priority
bd update bd-5 --assignee bob                 # Reassign
bd update bd-5,bd-7,bd-9 --priority 1         # Batch update
bd update bd-5 --notes "Design notes..."      # Add notes
bd close bd-5                                 # Close issue
bd reopen bd-5                                # Reopen issue
bd delete bd-5                                # Delete (soft)
bd delete bd-5 --purge                        # Delete permanently
```

## Dependencies

```bash
bd dep add bd-1 blocks bd-2                   # bd-1 blocks bd-2
bd dep add bd-1 discovered-from bd-5          # Found while working on bd-5
bd dep remove bd-1 blocks bd-2                # Remove dependency
bd dep tree bd-1                              # Show dependency tree
bd dep cycles                                 # Detect cycles
bd ready                                      # Show unblocked work
bd blocked                                    # Show blocked issues
```

## Comments

```bash
bd comment bd-5 "Progress update"             # Add comment
bd comment bd-5 --body "Multi-line..."        # Multi-line comment
bd comments list bd-5                         # Show comments
```

## Labels

```bash
bd label add urgent bd-5                      # Add label
bd label add backend,security bd-5            # Add multiple
bd label remove urgent bd-5                   # Remove label
bd list --label backend                       # Filter by label
bd list --label backend,security              # Must have both (AND)
bd list --label-any urgent,high               # Must have one (OR)
```

## Search & Show

```bash
bd search "authentication"                    # Text search
bd show bd-5                                  # Show details
bd show bd-5 --json                           # JSON output
bd show bd-5 --long                           # Full details
```

## Git Integration

```bash
bd sync push                                  # Push to remote
bd sync pull                                  # Pull from remote
git add .beads/                               # Stage issues
git commit -m "Update issues"                 # Commit issues
git push                                      # Push to remote
```

## Export/Import

```bash
bd export > backup.jsonl                      # Export all
bd export --status closed > archive.jsonl     # Export subset
bd import backup.jsonl                        # Import issues
bd migrate-issues --from ~/old --to ~/new    # Migrate repos
```

## Daemon Management

```bash
bd daemon start                               # Start daemon
bd daemon stop                                # Stop daemon
bd daemon status                              # Check status
bd daemon logs                                # View logs
bd --no-daemon list                           # Bypass daemon
```

## Health & Maintenance

```bash
bd validate                                   # Validate database
bd doctor                                     # Health check
bd repair-deps                                # Fix orphaned deps
bd dep cycles                                 # Find cycles
bd compact --older-than 90d                   # Compact old issues
bd cleanup --older-than 30d                   # Delete old closed
bd stale --older-than 30d                     # Find stale issues
bd duplicates                                 # Find duplicates
```

## Statistics

```bash
bd stats                                      # Overall stats
bd count                                      # Total issues
bd count --status open                        # Count open
bd count --label urgent                       # Count by label
```

## Visualization

```bash
bv .beads/beads.jsonl                         # Interactive graph
bd dep tree bd-1                              # Dependency tree
bd list --format dot > issues.dot             # Graphviz export
dot -Tpng -o issues.png issues.dot            # Render graph
```

## Templates

```bash
bd template create bug-report ...             # Create template
bd template list                              # List templates
bd create "Bug" --from-template bug-report    # Use template
```

## Multi-Repository

```bash
bd repo add backend ~/repos/backend           # Add repo
bd repo list                                  # List repos
bd create "Task" --repo backend               # Create in repo
```

## Configuration

```bash
bd config list                                # Show config
bd config set prefix myapp                    # Set prefix
bd config set default_priority 2              # Set default
bd config set git.auto_sync true              # Enable auto-sync
```

## Global Flags

```bash
--json                      # JSON output
--db <path>                 # Database path
--no-daemon                 # Bypass daemon
--no-db                     # JSONL-only mode
--sandbox                   # Isolated mode
--quiet                     # Suppress output
--verbose                   # Debug output
--actor <name>              # Override actor
```

## Issue Types

- `task` - Work item (default)
- `bug` - Defect or error
- `feature` - New functionality
- `epic` - Large initiative
- `chore` - Maintenance work

## Issue Status

- `open` - Initial state
- `in_progress` - Being worked on
- `blocked` - Cannot proceed
- `closed` - Completed

## Priority Levels

- `0` / `P0` - Critical (highest)
- `1` / `P1` - High
- `2` / `P2` - Medium (default)
- `3` / `P3` - Low
- `4` / `P4` - Very low (lowest)

## Dependency Types

- `blocks` - This blocks that
- `blocked_by` - This is blocked by that
- `discovered-from` - Found while working on
- `parent` - Hierarchical parent
- `child` - Hierarchical child

## JSON Processing Examples

```bash
# Get issue IDs
bd list --json | jq -r '.[].id'

# Count by status
bd list --json | jq 'group_by(.status) | map({status: .[0].status, count: length})'

# High priority open issues
bd list --json | jq '.[] | select(.priority <= 1 and .status == "open")'

# Extract dependencies
bd show bd-5 --json | jq '.dependencies'
```

## Common Workflows

### Daily Workflow
```bash
git pull                                      # Sync issues
bd list --assignee $USER --status open        # Your work
bd update bd-5 --status in_progress           # Start work
# ... do work ...
bd close bd-5                                 # Complete
git add .beads/ && git commit -m "..." && git push
```

### Sprint Planning
```bash
bd list --status open --no-assignee           # Backlog
bd update bd-1,bd-2,bd-3 --assignee alice     # Assign work
bd label add sprint-5 bd-1,bd-2,bd-3          # Tag sprint
bd list --label sprint-5                      # Review sprint
```

### Bug Triage
```bash
bd create "Bug: ..." --type bug --priority 1  # Create bug
bd update bd-10 --assignee bob                # Assign
bd update bd-10 --status in_progress          # Start fix
bd close bd-10                                # Close when fixed
```

## File Locations

- `.beads/beads.jsonl` - Issue history (JSONL)
- `.beads/*.db` - SQLite database
- `.beads/config.json` - Local config
- `~/.config/bd/config.json` - Global config
- `~/Library/Logs/bd/daemon.log` - Daemon logs (macOS)

## Help & Documentation

```bash
bd help                                       # General help
bd <command> --help                           # Command help
bd quickstart                                 # Quick start guide
bd onboard                                    # Setup AGENTS.md
bd version                                    # Version info
```

## Keyboard Shortcuts (bv)

- `?` - Show help
- `f` - Filter by status
- `l` - Filter by label
- `r` - Reset filters
- `Space` - Toggle node details
- `q` - Quit

## Quick Tips

1. **Daemon auto-starts** - No need to manually start
2. **Commit issues with code** - Keep them in sync
3. **Use dependencies liberally** - Model real dependencies
4. **Label consistently** - Establish taxonomy early
5. **Sync daily** - `git pull` / `git push`
6. **Comment frequently** - Context decays over time
7. **Validate regularly** - `bd validate` weekly
8. **Compact old issues** - `bd compact --older-than 90d`

## Common Patterns

```bash
# My unblocked work
bd ready --assignee $USER

# High priority backlog
bd list --status open --no-assignee --priority-min 0 --priority-max 1

# Stale issues needing attention
bd stale --older-than 30d

# Recent activity
bd list --updated-after $(date -d '7 days ago' +%Y-%m-%d)

# Issues needing descriptions
bd list --empty-description --status open

# Sprint burndown
bd count --label sprint-5 --status closed
bd count --label sprint-5 --status open
```

## Performance

- **With daemon**: <10ms operations
- **Without daemon**: ~100ms operations
- **Search (10k issues)**: <100ms
- **Recommendation**: Always use daemon (default)

## URLs & Resources

- **Codebase**: `@bd-codebase/`
- **Type Definitions**: `@bd-codebase/types/core.ts`
- **Principles**: `@bd-codebase/principles/`
- **Workflows**: `@bd-codebase/templates/task-workflow.md`
- **Skill**: `@bd/SKILL.md`

---

**Version**: 0.28.0+
**Last Updated**: 2024-12-02
