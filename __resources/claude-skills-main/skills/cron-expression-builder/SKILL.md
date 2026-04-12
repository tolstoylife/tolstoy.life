---
name: cron-expression-builder
description: Build and explain cron expressions for scheduling. Converts natural language schedules to cron syntax. Supports standard cron, AWS EventBridge, GitHub Actions, launchd, and systemd timer formats.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - WebFetch
  - WebSearch
---

# Cron Expression Builder

Converts human-readable schedules into correct cron expressions across platforms.

## When to Use

- Need a cron expression for a scheduled job
- Can't read an existing cron expression
- Converting between cron formats (unix, AWS, GitHub Actions, launchd, systemd)

## Workflow

1. **Get schedule** — Natural language like "every weekday at 9am EST"
2. **Identify platform** — Standard 5-field, 6-field (with seconds), AWS, GitHub Actions, launchd, systemd
3. **Build expression** — Generate the cron string
4. **Verify** — Show next 5 execution times
5. **Handle timezone** — Cron is typically UTC; show conversion for local time
6. **Platform-specific output** — launchd `StartCalendarInterval`, systemd `OnCalendar=`

## Gotchas

- Day-of-week: 0=Sunday in standard cron, 1=Monday in some systems
- AWS EventBridge: 6 fields + year
- GitHub Actions: 5-field, UTC only
