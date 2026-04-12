---
name: godmode-docker
description: Docker and Kubernetes operations via GODMODE MCP — container management, image listing, exec, run, logs, compose operations, and kubectl. 9 tools for container orchestration.
allowed-tools: Read, Bash
---

# Godmode Docker & Kubernetes

Container tools via GODMODE MCP.

## Docker Tools

| Tool | Args | Description |
|------|------|-------------|
| `docker_ps` | `all?`, `format?` (table/json) | List containers |
| `docker_images` | — | List images |
| `docker_exec` | `container`, `command` | Exec in container |
| `docker_run` | `image`, `ports?`, `volumes?`, `env?`, `detach?`, `rm?` | Run container |
| `docker_logs` | `container`, `tail?` | Get logs |
| `docker_stop` | `container` | Stop container |
| `docker_rm` | `container`, `force?` | Remove container |
| `docker_compose` | `action` (up/down/restart/logs/ps/build), `file?`, `services?` | Compose operations |

## Kubernetes

| Tool | Args | Description |
|------|------|-------------|
| `kubectl` | `command`, `namespace?`, `context?` | Any kubectl command |
