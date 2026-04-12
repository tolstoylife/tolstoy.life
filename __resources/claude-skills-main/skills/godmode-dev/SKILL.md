---
name: godmode-dev
description: Execute Python and Node.js code, install packages, and run npm scripts via GODMODE MCP. Tools — python_exec, pip_install, pip_list, node_exec, npm_install, npm_run.
allowed-tools: Read, Bash
---

# Godmode Development Tools

Code execution via GODMODE MCP.

## Tools

| Tool | Args | Description |
|------|------|-------------|
| `python_exec` | `code`, `timeout?` (60s default) | Execute Python code |
| `pip_install` | `package`, `upgrade?` | Install Python package |
| `pip_list` | `outdated?` | List installed packages |
| `node_exec` | `code`, `timeout?` (60s default) | Execute Node.js code |
| `npm_install` | `package`, `global?`, `dev?` | Install npm package |
| `npm_run` | `script`, `cwd` | Run npm script |
