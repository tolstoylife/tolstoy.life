---
name: godmode-files
description: Read, write, search, and watch files via GODMODE MCP. Get directory trees, file info, and monitor for changes. Tools — file_read, file_write, file_search, file_info, directory_tree, file_watch.
allowed-tools: Read, Bash
---

# Godmode File Operations

File system tools via GODMODE MCP.

## Tools

| Tool | Args | Description |
|------|------|-------------|
| `file_read` | `path`, `start_line?`, `end_line?`, `encoding?` | Read file contents |
| `file_write` | `path`, `content`, `mode?` (write/append) | Write/append to file |
| `file_search` | `directory`, `pattern?` (glob), `content?` (grep), `recursive?` | Search files |
| `file_info` | `path` | Size, modified, permissions, owner |
| `directory_tree` | `path`, `depth?`, `show_hidden?` | Directory structure as tree |
| `file_watch` | `path`, `timeout?` | Watch for changes (returns on first change) |
