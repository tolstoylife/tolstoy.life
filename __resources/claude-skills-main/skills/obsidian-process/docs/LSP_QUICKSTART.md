# LSP Integration Quick Start

5-minute guide to using LSP features in obsidian-process skill.

## Setup

```bash
# 1. Enable LSP tool
export ENABLE_LSP_TOOL=1

# 2. Install markdown-oxide (optional, for actual LSP features)
# Without it, the module runs in mock mode
cargo install markdown-oxide
```

## Common Operations

### 1. Find All Backlinks to a Note

```bash
cd /Users/mikhail/.claude/skills/obsidian-process/scripts

python lsp_integration.py references \
  --vault ~/Documents/Obsidian \
  --file "Projects/Main.md" \
  --line 0 \
  --char 0
```

**Output**: JSON array of all files referencing Main.md

### 2. Detect Orphaned Notes

```bash
cd /Users/mikhail/.claude/skills/obsidian-process/examples

python lsp_orphan_detection.py \
  --vault ~/Documents/Obsidian \
  --list
```

**Output**: List of all notes with no incoming links

### 3. Build Recursive Backlink Graph

```bash
cd /Users/mikhail/.claude/skills/obsidian-process/scripts

python lsp_integration.py recursive-backlinks \
  --vault ~/Documents/Obsidian \
  --file "Index.md" \
  --depth 3 \
  --output backlink_graph.json
```

**Output**: JSON graph showing backlinks up to 3 levels deep

### 4. Analyze Vault Structure

```bash
cd /Users/mikhail/.claude/skills/obsidian-process/scripts

python lsp_integration.py analyze-vault \
  --vault ~/Documents/Obsidian \
  --output vault_analysis.json
```

**Output**: Comprehensive analysis including:
- Total files and links
- Orphaned notes
- Hub notes (most referenced)
- Circular reference groups
- Link graph

### 5. Search Vault Symbols

```bash
python lsp_integration.py search \
  --vault ~/Documents/Obsidian \
  --query "machine learning"
```

**Output**: All headings, files, and tags matching the query

### 6. Get Document Structure

```bash
python lsp_integration.py heading-tree \
  --vault ~/Documents/Obsidian \
  --file "Research/Paper.md"
```

**Output**: Hierarchical heading tree for the file

## Python API

### Basic Usage

```python
from pathlib import Path
from lsp_integration import MarkdownOxideIntegration

# Initialize
vault = Path("~/Documents/Obsidian").expanduser()
integration = MarkdownOxideIntegration(vault)

# Find backlinks
backlinks = integration.find_backlinks(vault / "Index.md")
print(f"Found {len(backlinks)} backlinks")

# Search vault
results = integration.search_vault("TODO")
for r in results:
    print(f"{r['name']} in {r['file']}")
```

### Recursive Operations

```python
from lsp_integration import RecursiveLSP

recursive = RecursiveLSP(integration)

# Find orphans
md_files = list(vault.glob("**/*.md"))
orphans = recursive.find_orphans(md_files)
print(f"Orphaned: {orphans}")

# Build link graph
graph = recursive.build_link_graph(md_files)
print(f"Nodes: {graph['node_count']}, Edges: {graph['edge_count']}")
```

### Vault Analysis

```python
from lsp_integration import VaultLSPAnalyzer

analyzer = VaultLSPAnalyzer(vault)
result = analyzer.process()

print(f"Files: {result.files_processed}")
print(f"Orphans: {result.metadata['analysis']['orphan_count']}")
```

## Workflows

### Workflow 1: Clean Up Orphans

```bash
# 1. Find orphans
python examples/lsp_orphan_detection.py --vault ~/vault --list

# 2. Generate report
python examples/lsp_orphan_detection.py --vault ~/vault --report orphans.md

# 3. Preview archive operation
python examples/lsp_orphan_detection.py --vault ~/vault --archive --dry-run

# 4. Execute archive
python examples/lsp_orphan_detection.py --vault ~/vault --archive
```

### Workflow 2: Analyze Vault Health

```bash
# 1. Full analysis
python examples/lsp_backlink_analysis.py \
  --vault ~/vault \
  --output analysis.json \
  --depth 3

# 2. Review hub notes and circular references in output
cat analysis.json | jq '.hub_notes[:5]'

# 3. Check directory statistics
cat analysis.json | jq '.directory_statistics'
```

### Workflow 3: Build Knowledge Graph

```python
from lsp_integration import RecursiveLSP, MarkdownOxideIntegration
from pathlib import Path
import json

vault = Path("~/vault").expanduser()
integration = MarkdownOxideIntegration(vault)
recursive = RecursiveLSP(integration)

# Build complete graph
md_files = list(vault.glob("**/*.md"))
graph = recursive.build_link_graph(md_files)

# Export for visualization (e.g., Obsidian Graph View, Gephi)
output = {
    'nodes': [
        {'id': node, 'incoming': data['incoming_links']}
        for node, data in graph['nodes'].items()
    ],
    'edges': [
        {'source': edge['from'], 'target': edge['to']}
        for edge in graph['edges']
    ]
}

Path("knowledge_graph.json").write_text(json.dumps(output, indent=2))
```

## Troubleshooting

### LSP Not Enabled

```
LSP tool not enabled. Set ENABLE_LSP_TOOL=1 environment variable.
```

**Solution**:
```bash
export ENABLE_LSP_TOOL=1
```

### Mock Mode

If you see "Running in mock mode" warnings, markdown-oxide LSP is not installed. The module runs in fallback mode with limited functionality.

**Solution**: Install markdown-oxide or use existing processors (WikilinkExtractor, etc.)

### Empty Results

If LSP operations return empty results:

1. Check vault path is correct
2. Verify markdown files exist
3. Enable verbose mode: `--verbose`

## Next Steps

- Read full documentation: `docs/LSP_INTEGRATION.md`
- Review example scripts: `examples/`
- Run tests: `python scripts/test_lsp_integration.py`
- Explore advanced features: Tarjan's algorithm, call hierarchy, diagnostics

## Architecture Overview

```
LSPClient (low-level protocol)
    ↓
MarkdownOxideIntegration (Obsidian operations)
    ↓
RecursiveLSP (graph algorithms)
    ↓
VaultLSPAnalyzer (batch processing)
```

Each layer builds on the previous, from raw LSP to high-level vault analysis.
