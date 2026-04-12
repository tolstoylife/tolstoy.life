---
name: godmode-git-ops
description: Full git operations via GODMODE MCP — status, log, diff, clone, commit, push, pull, branch management, and stash. 9 git tools for repository management without CLI.
allowed-tools: Read, Bash
---

# Godmode Git Operations

Git tools via GODMODE MCP.

## Tools

| Tool | Args | Description |
|------|------|-------------|
| `git_status` | `repo_path` | Working tree status |
| `git_log` | `repo_path`, `count?`, `format?` (oneline/short/full), `branch?` | Commit history |
| `git_diff` | `repo_path`, `staged?` | Show diff |
| `git_clone` | `url`, `path?`, `branch?`, `depth?` | Clone repository |
| `git_commit` | `repo_path`, `message`, `files?`, `all?`, `amend?` | Stage and commit |
| `git_push` | `repo_path`, `remote?`, `branch?`, `force?` | Push to remote |
| `git_pull` | `repo_path`, `remote?`, `branch?`, `rebase?` | Pull from remote |
| `git_branch` | `repo_path`, `action` (list/create/delete/switch), `name?` | Branch management |
| `git_stash` | `repo_path`, `action` (push/pop/list/drop/apply) | Stash management |
