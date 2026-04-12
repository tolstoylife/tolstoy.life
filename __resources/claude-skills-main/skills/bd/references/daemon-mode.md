# Daemon Mode & RPC Integration

## Overview

bd daemon is a long-running background process that provides:

1. **Hot SQLite Cache**: Keep database in memory for <10ms operations
2. **Multi-Workspace Support**: Handle multiple repositories simultaneously
3. **Background Sync**: Auto-sync JSONL with remote at intervals
4. **RPC Protocol**: JSON-RPC over Unix socket or TCP
5. **LSP-Inspired Design**: Request/response pattern with notifications

## Architecture

```
┌─────────────────────────────────────────────┐
│                                             │
│  bd CLI Client(s)                           │
│  (one or more terminal sessions)            │
│                                             │
└─────────────────────┬───────────────────────┘
                      │
                      │ JSON-RPC
                      │ (Unix socket or TCP)
                      │
┌─────────────────────▼───────────────────────┐
│                                             │
│  bd Daemon                                  │
│  - Hot SQLite cache                         │
│  - JSONL consistency                        │
│  - Multi-workspace routing                  │
│  - Background sync                          │
│                                             │
└─────────────────────┬───────────────────────┘
                      │
                      │ File I/O
                      │
┌─────────────────────▼───────────────────────┐
│                                             │
│  .beads/                                    │
│  ├── beads.jsonl  (source of truth)         │
│  ├── *.db         (SQLite cache)            │
│  └── config.json  (configuration)           │
│                                             │
└─────────────────────────────────────────────┘
```

## Starting the Daemon

### Automatic Start

Daemon starts automatically on first bd operation:

```bash
# First command starts daemon
bd list
# Daemon starts in background automatically

# Subsequent commands use daemon
bd create "New issue"  # <10ms via RPC
```

### Manual Start

```bash
# Start daemon explicitly
bd daemon start

# Start with specific port
bd daemon start --port 9876

# Start in foreground (for debugging)
bd daemon start --foreground
```

### Configuration

Set in `.beads/config.json` or `~/.config/bd/config.json`:

```json
{
  "daemon": {
    "enabled": true,
    "port": 0,  // 0 = auto-select
    "sync_interval": 300  // Auto-sync every 5 minutes
  }
}
```

## Daemon Operations

### Check Status

```bash
bd daemon status

# Output:
# Daemon is running
# Port: 9876
# Workspaces: 3
# Uptime: 2h 15m
# Version: 0.28.0
```

### Stop Daemon

```bash
# Graceful shutdown
bd daemon stop

# Force shutdown (if stuck)
bd daemon stop --force
```

### Restart Daemon

```bash
bd daemon stop
bd daemon start
```

### View Logs

```bash
# Daemon logs location (varies by OS)
bd daemon logs

# Typical locations:
# macOS: ~/Library/Logs/bd/daemon.log
# Linux: ~/.local/share/bd/daemon.log
```

## Multi-Workspace Support

### How It Works

Daemon can manage multiple repositories simultaneously:

```bash
# Terminal 1: Work in repo A
cd ~/repos/project-a
bd list  # Daemon serves from workspace A

# Terminal 2: Work in repo B (same daemon)
cd ~/repos/project-b
bd list  # Daemon serves from workspace B

# Daemon maintains separate SQLite cache per workspace
```

### Workspace Routing

Daemon automatically routes requests based on:

1. **Working Directory**: Detects `.beads/` in cwd or ancestors
2. **Explicit Path**: `--db /path/to/.beads/db`
3. **Config**: Multi-repo configuration

### Workspace Information

```bash
# Show active workspaces
bd daemon status

# Output includes:
# Workspaces:
#   /Users/alice/repos/project-a
#   /Users/alice/repos/project-b
#   /Users/alice/repos/project-c
```

## RPC Protocol

### Protocol Design

bd uses **JSON-RPC 2.0** over:

- **Unix Domain Socket** (default on Unix-like systems)
- **TCP** (fallback or remote access)

### Request Format

```json
{
  "jsonrpc": "2.0",
  "id": "req-123",
  "method": "issue.create",
  "params": {
    "title": "Add authentication",
    "type": "feature",
    "priority": 1
  }
}
```

### Response Format

```json
{
  "jsonrpc": "2.0",
  "id": "req-123",
  "result": {
    "id": "bd-a3f8e9",
    "title": "Add authentication",
    "type": "feature",
    "status": "open",
    "priority": 1,
    "created_at": "2024-01-15T10:00:00Z",
    ...
  }
}
```

### Error Format

```json
{
  "jsonrpc": "2.0",
  "id": "req-123",
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": "Priority must be 0-4"
  }
}
```

## RPC Methods

### Issue Operations

#### issue.create

```json
{
  "method": "issue.create",
  "params": {
    "title": "Task title",
    "type": "task",
    "priority": 2,
    "assignee": "alice",
    "labels": ["backend", "urgent"]
  }
}
```

#### issue.update

```json
{
  "method": "issue.update",
  "params": {
    "id": "bd-1",
    "status": "in_progress",
    "priority": 0
  }
}
```

#### issue.get

```json
{
  "method": "issue.get",
  "params": {
    "id": "bd-1"
  }
}
```

#### issue.list

```json
{
  "method": "issue.list",
  "params": {
    "status": ["open", "in_progress"],
    "assignee": "alice",
    "sort": "priority",
    "limit": 10
  }
}
```

#### issue.delete

```json
{
  "method": "issue.delete",
  "params": {
    "id": "bd-1",
    "purge": false
  }
}
```

### Dependency Operations

#### dep.add

```json
{
  "method": "dep.add",
  "params": {
    "source": "bd-1",
    "type": "blocks",
    "target": "bd-2"
  }
}
```

#### dep.remove

```json
{
  "method": "dep.remove",
  "params": {
    "source": "bd-1",
    "type": "blocks",
    "target": "bd-2"
  }
}
```

#### dep.tree

```json
{
  "method": "dep.tree",
  "params": {
    "id": "bd-1"
  }
}
```

### Sync Operations

#### sync.pull

```json
{
  "method": "sync.pull",
  "params": {}
}
```

Returns:
```json
{
  "result": {
    "updated": 5,
    "conflicts": ["bd-3", "bd-7"]
  }
}
```

#### sync.push

```json
{
  "method": "sync.push",
  "params": {}
}
```

Returns:
```json
{
  "result": {
    "pushed": 3
  }
}
```

### Daemon Management

#### daemon.status

```json
{
  "method": "daemon.status",
  "params": {}
}
```

Returns:
```json
{
  "result": {
    "running": true,
    "port": 9876,
    "workspaces": [
      "/Users/alice/repos/project-a",
      "/Users/alice/repos/project-b"
    ],
    "uptime": 7890,
    "version": "0.28.0"
  }
}
```

#### daemon.shutdown

```json
{
  "method": "daemon.shutdown",
  "params": {}
}
```

## Bypassing the Daemon

### Direct Mode

Force direct SQLite access (bypass daemon):

```bash
bd --no-daemon list
bd --no-daemon create "New issue"
```

**Use cases:**
- Debugging daemon issues
- Performance profiling
- Testing without daemon overhead

### JSONL-Only Mode

Skip SQLite entirely, read from JSONL:

```bash
bd --no-db list
bd --no-db show bd-1
```

**Use cases:**
- Corrupted database
- Read-only access
- Minimal dependencies

### Sandbox Mode

Disable daemon and auto-sync:

```bash
bd --sandbox list
bd --sandbox create "Test issue"
```

**Use cases:**
- Testing without side effects
- CI/CD pipelines
- Isolated environments

## Performance Characteristics

### With Daemon (Default)

- **Create**: <10ms
- **Update**: <5ms
- **List**: <50ms (10k issues)
- **Search**: <100ms (full-text)
- **Close**: <5ms

### Without Daemon (Direct Mode)

- **Create**: ~100ms
- **Update**: ~80ms
- **List**: ~150ms (10k issues)
- **Search**: ~200ms
- **Close**: ~80ms

**10-20x performance improvement with daemon.**

## Background Sync

### Auto-Sync Configuration

```json
{
  "daemon": {
    "sync_interval": 300  // Sync every 5 minutes
  },
  "git": {
    "auto_sync": true,
    "remote": "origin",
    "sync_branch": "main"
  }
}
```

### Sync Behavior

Every `sync_interval` seconds, daemon:

1. Checks for remote changes (`git fetch`)
2. Pulls if remote has new commits (`git pull`)
3. Merges `.beads/beads.jsonl` using custom driver
4. Rebuilds SQLite from merged JSONL
5. Pushes local changes (`git push`)

### Manual Sync

```bash
# Trigger sync immediately
bd sync pull
bd sync push

# Sync specific branch
bd sync pull --branch feature/new-auth
```

## Integration with AI Agents

### Agent RPC Client Example

```python
import json
import socket

class BdClient:
    def __init__(self, socket_path="/tmp/bd.sock"):
        self.socket_path = socket_path
        self.request_id = 0

    def call(self, method, params):
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": f"req-{self.request_id}",
            "method": method,
            "params": params
        }

        # Connect to daemon
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(self.socket_path)

        # Send request
        sock.sendall(json.dumps(request).encode() + b'\n')

        # Receive response
        response = sock.recv(4096)
        sock.close()

        return json.loads(response)

    def create_issue(self, title, **kwargs):
        params = {"title": title, **kwargs}
        return self.call("issue.create", params)

    def list_issues(self, **filters):
        return self.call("issue.list", filters)

    def ready_work(self):
        return self.call("issue.list", {
            "status": ["open", "in_progress"],
            "blocked_by": []
        })

# Usage
client = BdClient()

# Get ready work
ready = client.ready_work()
if ready["result"]:
    issue = ready["result"][0]
    print(f"Working on: {issue['id']} - {issue['title']}")

    # Update status
    client.call("issue.update", {
        "id": issue["id"],
        "status": "in_progress"
    })

    # ... do work ...

    # Close issue
    client.call("issue.update", {
        "id": issue["id"],
        "status": "closed"
    })
```

### Agent Benefits

1. **Low Latency**: <10ms RPC calls vs ~100ms direct
2. **No Database Contention**: Daemon handles locking
3. **Consistent State**: Single source of truth
4. **Background Sync**: Agent doesn't handle git
5. **Multi-Agent Support**: Multiple agents via same daemon

## Troubleshooting

### Daemon Won't Start

```bash
# Check for existing daemon
bd daemon status

# Check port availability
lsof -i :9876  # If using TCP

# Check logs
bd daemon logs

# Force restart
bd daemon stop --force
bd daemon start
```

### Daemon Crashed

```bash
# Check logs
bd daemon logs

# Look for errors:
# - Port conflicts
# - Database corruption
# - File permission issues

# Restart daemon
bd daemon start
```

### Performance Issues

```bash
# Profile daemon operations
bd --profile list

# Check database size
du -sh .beads/

# Compact old issues
bd compact --older-than 90d

# Rebuild database
rm .beads/*.db
bd migrate
```

### Multiple Daemons

```bash
# Check running daemons
ps aux | grep bd

# Kill specific daemon
bd daemon stop --workspace /path/to/repo

# Manage multiple daemons
bd daemons list
bd daemons stop --all
```

## Advanced Configuration

### Multi-Daemon Setup

For isolated environments (dev/staging/prod):

```bash
# Start daemon on custom port
bd daemon start --port 9876 --workspace ~/repos/dev

# Start another on different port
bd daemon start --port 9877 --workspace ~/repos/staging

# Connect to specific daemon
bd --db ~/repos/dev/.beads/db list
bd --db ~/repos/staging/.beads/db list
```

### Custom Socket Path

```bash
# Start with custom socket
bd daemon start --socket /tmp/bd-custom.sock

# Connect to custom socket
export BD_SOCKET=/tmp/bd-custom.sock
bd list
```

### Remote Daemon Access

```bash
# Start daemon with TCP (for remote access)
bd daemon start --tcp --port 9876 --host 0.0.0.0

# Connect from remote machine
export BD_HOST=remote.example.com
export BD_PORT=9876
bd list
```

**⚠️ Security Warning:** Daemon has no authentication. Use SSH tunneling for remote access:

```bash
# On remote machine
bd daemon start --port 9876

# On local machine
ssh -L 9876:localhost:9876 user@remote.example.com

# Local bd connects via tunnel
export BD_PORT=9876
bd list
```

## Best Practices

### 1. Let Daemon Auto-Start

Default behavior (auto-start) works for 95% of use cases.

### 2. Use Multi-Workspace

One daemon handles all repos. No need for multiple daemons.

### 3. Enable Auto-Sync

Background sync keeps team in sync without manual intervention.

### 4. Monitor Logs Periodically

Check logs for errors or performance issues:

```bash
tail -f ~/Library/Logs/bd/daemon.log
```

### 5. Restart After Upgrades

After upgrading bd, restart daemon:

```bash
bd daemon stop
# Upgrade bd
bd daemon start
```

### 6. Use Direct Mode for Debugging

If daemon misbehaves, use `--no-daemon` to isolate issue.

### 7. Profile for Performance

If slow, profile to identify bottleneck:

```bash
bd --profile list
```

## See Also

- [SKILL.md](../SKILL.md) - Complete skill documentation
- [task-patterns.md](task-patterns.md) - Common task operations
- [cheatsheet.md](../assets/cheatsheet.md) - Quick reference
