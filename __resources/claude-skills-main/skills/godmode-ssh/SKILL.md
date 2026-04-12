---
name: godmode-ssh
description: Execute commands on remote servers via SSH, transfer files with SCP, and create SSH tunnels via GODMODE MCP. Tools — ssh_exec, scp_transfer, ssh_tunnel.
allowed-tools: Read, Bash
---

# Godmode SSH & Remote Operations

Remote server tools via GODMODE MCP.

## Tools

| Tool | Args | Description |
|------|------|-------------|
| `ssh_exec` | `host`, `command`, `user?`, `key_file?`, `port?` | Run command on remote server |
| `scp_transfer` | `source`, `destination`, `direction` (upload/download), `recursive?` | SCP file transfer |
| `ssh_tunnel` | `host`, `local_port`, `remote_port`, `user?` | Create SSH tunnel |
