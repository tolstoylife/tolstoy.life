---
name: shell-script-linter
description: Review and fix shell scripts for correctness, portability, and security. Catches common bash pitfalls like unquoted variables, missing error handling, and POSIX incompatibilities.
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

# Shell Script Linter

Review shell scripts for bugs, security issues, and portability problems.

## When to Use

- Writing or reviewing bash/zsh/sh scripts
- Script works on one machine but fails on another
- Need to make a script more robust (error handling, edge cases)
- Converting between bash and POSIX sh

## What It Checks

- **Quoting** — Unquoted variables, word splitting, glob expansion
- **Error handling** — Missing `set -euo pipefail`, unchecked commands
- **Portability** — Bashisms in #!/bin/sh scripts, macOS vs Linux differences
- **Security** — Command injection via eval, unvalidated input, temp file races
- **Style** — Consistent indentation, function declarations, variable naming
- **Performance** — Unnecessary subshells, useless use of cat/echo

## Workflow

1. Read the script
2. Identify interpreter (bash, zsh, sh, dash)
3. Flag issues with severity (error, warning, info)
4. Provide fixed version with explanations
5. Suggest shellcheck directives where appropriate
