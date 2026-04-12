---
name: godmode-system
description: Execute shell commands, manage processes, get system info, and run batch operations via the GODMODE MCP server (port 7865). Tools — shell_exec, process_list, process_kill, system_info, batch_exec.
allowed-tools: Read, Bash
---

# Godmode System & Shell

System automation via GODMODE MCP (`http://127.0.0.1:7865/sse`).

## Tools

| Tool | Args | Description |
|------|------|-------------|
| `shell_exec` | `command`, `cwd?`, `timeout?` | Execute any shell command |
| `process_list` | `sort_by?` (cpu/memory/pid) | List processes with CPU/memory |
| `process_kill` | `pid` or `name`, `signal?` (TERM/KILL) | Kill a process |
| `system_info` | — | Hostname, OS, CPU, memory, disk, uptime, load |
| `batch_exec` | `commands[]`, `parallel?`, `stop_on_error?` | Run multiple commands |

## Example

```json
{"tool": "shell_exec", "arguments": {"command": "df -h", "timeout": 30}}
{"tool": "batch_exec", "arguments": {"commands": ["git pull", "npm install", "npm test"], "stop_on_error": true}}
```
