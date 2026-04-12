---
name: makefile-generator
description: Generate Makefiles and Justfiles for project automation. Creates targets for build, test, lint, deploy, and development workflows with proper dependency chains.
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

# Makefile Generator

Create project automation files (Makefile or Justfile) tailored to your stack.

## When to Use

- New project needs standard build/test/lint/deploy commands
- Want to standardize team workflows with simple commands
- Migrating from npm scripts or shell scripts to Make
- Need a Justfile (just command runner) instead of Make

## Workflow

1. **Detect stack** — Language, framework, package manager, test runner
2. **Generate targets** — build, test, lint, format, clean, dev, deploy
3. **Add help** — Self-documenting targets with `make help`
4. **Handle deps** — Proper prerequisite chains (build before test)
5. **Variables** — Configurable via environment or CLI overrides

## Output Formats

- **Makefile** — POSIX Make with .PHONY declarations
- **Justfile** — just command runner (simpler syntax, no tab requirement)
- Either format includes: help target, variable defaults, phony declarations
