---
name: git-bisect-debugger
description: Automate git bisect to find the exact commit that introduced a bug. Builds test scripts, runs binary search across commit history, and identifies the breaking change with minimal manual effort.
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

# Git Bisect Debugger

Automates `git bisect` workflows to pinpoint the exact commit that introduced a regression or bug.

## When to Use

- A feature that was working is now broken and you don't know when it broke
- Tests started failing and you need to find the culprit commit
- Performance degraded at some unknown point in history

## Workflow

1. **Identify symptoms** — Get the failing test command or reproduction steps from the user
2. **Find known-good commit** — Use `git log` to help user identify last known working state
3. **Build bisect script** — Create a shell script that returns 0 (good) or 1 (bad) for automated bisect
4. **Run bisect** — Execute `git bisect start`, `git bisect bad HEAD`, `git bisect good <commit>`, `git bisect run <script>`
5. **Analyze result** — Show the breaking commit, its diff, and explain what changed
6. **Clean up** — Run `git bisect reset` to restore working tree

## Key Principles

- Always create a standalone test script (not inline commands) for reproducibility
- Handle build failures gracefully (return 125 to skip unbuildable commits)
- Preserve user's working tree state with stash before starting
- Show estimated number of steps before starting (log2 of commit range)
