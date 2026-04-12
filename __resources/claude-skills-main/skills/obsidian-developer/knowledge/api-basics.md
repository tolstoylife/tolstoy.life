# Obsidian API Basics for Automation

## Global Context
In the Obsidian developer console (and via `Runtime.evaluate`), the primary entry point is the global `app` object.

## Core Components

### `app.vault` (File System)
Handles reading, writing, and listing files.
- `app.vault.getFiles()`: Returns array of `TFile` objects (all files in vault).
- `app.vault.getAbstractFileByPath("folder/note.md")`: Get `TFile` or `TFolder`.
- `app.vault.read(tFile)`: Async. Read content of a file.
- `app.vault.modify(tFile, newContent)`: Async. Update a file.
- `app.vault.create(path, content)`: Async. Create a new file.

**Example: List all Markdown files**
```javascript
app.vault.getFiles()
  .filter(f => f.extension === 'md')
  .map(f => f.path)
```

### `app.workspace` (UI & Layout)
Manages leaves (tabs/panes) and view state.
- `app.workspace.getActiveFile()`: Returns `TFile` of the currently focused note.
- `app.workspace.getLeavesOfType("markdown")`: Get all markdown editing panes.
- `app.workspace.openLinkText(linktext, sourcePath, newLeaf)`: Open a note.

**Example: Get active file content**
```javascript
const file = app.workspace.getActiveFile();
if (file) {
  app.vault.read(file).then(content => console.log(content));
}
```

### `app.metadataCache` (Indexing)
Fast access to frontmatter, tags, and links without reading files.
- `app.metadataCache.getFileCache(tFile)`: Returns `{frontmatter, tags, links, ...}`.
- `app.metadataCache.resolvedLinks`: Map of all link dependencies.

### `app.plugins` (Plugin Management)
- `app.plugins.manifests`: Dictionary of installed plugins and their metadata.
- `app.plugins.enabledPlugins`: Set of enabled plugin IDs.
- `app.plugins.plugins`: Access to the actual plugin instances (API access).

**Example: Check if Dataview is enabled**
```javascript
app.plugins.enabledPlugins.has("dataview")
```

## Common "gotchas"
1. **Async Operations**: Most vault operations are async. When using `Runtime.evaluate`, always wrap in an async IIFE or rely on the tool's promise handling.
2. **Path handling**: Obsidian uses vault-relative paths (e.g., `Folder/Note.md`), not absolute system paths.
3. **Safe Mode**: The MCP server may block destructive `vault` methods. Check `SECURITY.md`.
