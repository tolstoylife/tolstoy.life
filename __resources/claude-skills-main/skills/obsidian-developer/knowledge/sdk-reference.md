# Obsidian SDK Reference

Python SDK for programmatic Obsidian automation via CDP.

## Overview

The `ObsidianClient` SDK provides high-level abstractions over the raw CDP connection, enabling type-safe vault operations without manual JavaScript string construction.

## Installation

The SDK is bundled with the `obsidian-devtools` MCP server:

```python
from obsidian_devtools.client import CDPClient
from obsidian_devtools.sdk import ObsidianClient

client = CDPClient(port=9222)
await client.connect()
sdk = ObsidianClient(client)
```

## Core Classes

### ObsidianClient

Main entry point for all vault operations.

```python
class ObsidianClient:
    def __init__(self, cdp_client: CDPClient):
        """Initialize with an active CDP connection."""

    # Vault Operations
    async def get_vault_name(self) -> str
    async def list_files(self, extension: str = None) -> List[str]
    async def read_file(self, path: str) -> str
    async def write_file(self, path: str, content: str) -> None
    async def create_file(self, path: str, content: str) -> None
    async def delete_file(self, path: str, trash: bool = True) -> None
    async def rename_file(self, old_path: str, new_path: str) -> None

    # Workspace Operations
    async def get_active_file(self) -> Optional[str]
    async def open_file(self, path: str, new_leaf: bool = False) -> None
    async def get_open_files(self) -> List[str]

    # Metadata Operations
    async def get_frontmatter(self, path: str) -> Dict[str, Any]
    async def update_frontmatter(self, path: str, key: str, value: Any) -> None
    async def get_tags(self, path: str) -> List[str]
    async def get_links(self, path: str) -> List[str]

    # Plugin Operations
    async def list_plugins(self) -> List[Dict]
    async def is_plugin_enabled(self, plugin_id: str) -> bool
    async def get_plugin_api(self, plugin_id: str) -> Any

    # Canvas Operations
    async def create_canvas(self, path: str, nodes: List[Dict], edges: List[Dict] = None) -> None
    async def read_canvas(self, path: str) -> Dict
    async def add_canvas_node(self, canvas_path: str, node: Dict) -> None

    # Discovery
    async def discover_api(self, object_path: str) -> Dict[str, List[str]]
```

## Vault Operations

### Reading Files

```python
# Get vault name
vault = await sdk.get_vault_name()
print(f"Connected to: {vault}")

# List all markdown files
files = await sdk.list_files(extension="md")
print(f"Found {len(files)} markdown files")

# Read specific file
content = await sdk.read_file("Notes/Example.md")
```

### Writing Files

```python
# Create new file
await sdk.create_file(
    path="Notes/NewNote.md",
    content="# New Note\n\nCreated via SDK."
)

# Update existing file
await sdk.write_file(
    path="Notes/Existing.md",
    content="# Updated Content\n\nModified via SDK."
)

# Rename file
await sdk.rename_file("Notes/OldName.md", "Notes/NewName.md")

# Delete file (to trash)
await sdk.delete_file("Notes/ToDelete.md", trash=True)
```

### Safety Mode

By default, destructive operations are blocked. The SecurityGuard checks:

```python
BLOCKED_PATTERNS = [
    r'\bfs\.',           # Node.js filesystem
    r'\bchild_process',  # Process spawning
    r'vault\.delete',    # Vault deletion
    r'vault\.trash',     # Trash operations (configurable)
]
```

To enable writes, configure the server with `safe_mode=False`.

## Metadata Operations

### Frontmatter

```python
# Get all frontmatter
fm = await sdk.get_frontmatter("Notes/Example.md")
# Returns: {"title": "Example", "tags": ["test"], "date": "2024-01-01"}

# Update single key
await sdk.update_frontmatter("Notes/Example.md", "status", "complete")

# Update complex value
await sdk.update_frontmatter("Notes/Example.md", "related", [
    "[[Note A]]",
    "[[Note B]]"
])
```

### Tags and Links

```python
# Get tags (including inline)
tags = await sdk.get_tags("Notes/Example.md")
# Returns: ["#topic/subtopic", "#status/active"]

# Get outgoing links
links = await sdk.get_links("Notes/Example.md")
# Returns: ["Note A", "Note B", "Folder/Note C"]
```

## Workspace Operations

```python
# Get currently active file
active = await sdk.get_active_file()
if active:
    print(f"Currently editing: {active}")

# Open a file
await sdk.open_file("Notes/Target.md")

# Open in new pane
await sdk.open_file("Notes/Target.md", new_leaf=True)

# Get all open files
open_files = await sdk.get_open_files()
```

## Plugin Integration

### Listing Plugins

```python
plugins = await sdk.list_plugins()
for p in plugins:
    print(f"{p['name']} v{p['version']} - {p['description']}")
```

### Checking Plugin Status

```python
if await sdk.is_plugin_enabled("dataview"):
    print("Dataview is available")
```

### Accessing Plugin APIs

```python
# Get Dataview API
dv_api = await sdk.get_plugin_api("dataview")

# Run Dataview query (via eval)
result = await client.evaluate("""
    const dv = app.plugins.plugins.dataview.api;
    dv.pages('#topic').map(p => p.file.name);
""")
```

## Discovery (Reflection)

The `discover_api` method enables runtime introspection:

```python
# Discover app.vault methods
vault_api = await sdk.discover_api("app.vault")
print("Methods:", vault_api["methods"])
print("Properties:", vault_api["properties"])

# Discover plugin API
dv_api = await sdk.discover_api("app.plugins.plugins.dataview.api")
```

### Output Format

```python
{
    "methods": ["getFiles", "read", "modify", "create", "delete", ...],
    "properties": ["adapter", "config", "configDir", ...],
    "prototype_methods": ["on", "off", "trigger", ...]  # Inherited
}
```

## Error Handling

```python
from obsidian_devtools.errors import (
    ConnectionError,
    SecurityError,
    FileNotFoundError,
    PluginNotFoundError
)

try:
    content = await sdk.read_file("NonExistent.md")
except FileNotFoundError:
    print("File does not exist")

try:
    await sdk.write_file("Test.md", "content")
except SecurityError as e:
    print(f"Blocked by Safe Mode: {e}")
```

## Async Patterns

### Batch Operations

```python
import asyncio

async def batch_update_frontmatter(files, key, value):
    """Update frontmatter across multiple files."""
    tasks = [
        sdk.update_frontmatter(f, key, value)
        for f in files
    ]
    await asyncio.gather(*tasks)

# Usage
files = await sdk.list_files(extension="md")
await batch_update_frontmatter(files[:10], "reviewed", True)
```

### Progress Tracking

```python
async def process_with_progress(files):
    total = len(files)
    for i, f in enumerate(files):
        content = await sdk.read_file(f)
        # Process...
        print(f"Progress: {i+1}/{total}")
```

## Integration with MCP Tools

The SDK methods map directly to MCP tools:

| SDK Method | MCP Tool |
|------------|----------|
| `get_vault_name()` | `obsidian_eval("app.vault.getName()")` |
| `list_files()` | `obsidian_eval("app.vault.getFiles()...")` |
| `get_frontmatter()` | `obsidian_get_frontmatter` |
| `update_frontmatter()` | `obsidian_update_frontmatter` |
| `discover_api()` | `obsidian_discover_api` |
| `create_canvas()` | `obsidian_create_canvas` |

## Best Practices

1. **Always await**: All SDK methods are async
2. **Handle errors**: Wrap in try/except for production use
3. **Batch wisely**: Use `asyncio.gather` for parallel operations
4. **Respect Safe Mode**: Don't disable unless necessary
5. **Use discovery**: Query APIs at runtime rather than assuming

---

See also:
- [api-basics.md](api-basics.md) - Raw JavaScript API reference
- [canvas-api.md](canvas-api.md) - Canvas-specific operations
- [cdp-protocol.md](cdp-protocol.md) - Low-level CDP details
