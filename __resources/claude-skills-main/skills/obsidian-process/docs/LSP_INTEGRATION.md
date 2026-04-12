# LSP Integration for Obsidian Vault Processing

Comprehensive LSP (Language Server Protocol) integration leveraging markdown-oxide LSP through Claude Code's native LSP tool.

## Prerequisites

```bash
# Enable Claude Code LSP tool support
export ENABLE_LSP_TOOL=1

# Ensure markdown-oxide LSP is installed and configured
# See: https://github.com/Feel-ix-343/markdown-oxide
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      LSPClient                           │
│  - goto_definition()  - find_references()  - hover()    │
│  - document_symbol()  - workspace_symbol()              │
│  - prepare_call_hierarchy()  - incoming/outgoing_calls()│
└──────────────────┬──────────────────────────────────────┘
                   │
     ┌─────────────┼─────────────────┐
     │             │                 │
     ▼             ▼                 ▼
┌──────────┐  ┌──────────┐  ┌───────────────┐
│Markdown  │  │Recursive │  │VaultLSP       │
│Oxide     │  │LSP       │  │Analyzer       │
│Integration  │          │  │(BatchProcessor)│
└──────────┘  └──────────┘  └───────────────┘
```

## Quick Start

### 1. Find References to a Symbol

```bash
python scripts/lsp_integration.py references \
  --vault ~/Documents/Obsidian \
  --file Projects/Main.md \
  --line 5 \
  --char 10
```

**Output:**
```json
[
  {
    "file": "Daily/2024-01-15.md",
    "line": 12,
    "character": 8,
    "range": {
      "start": {"line": 12, "char": 8},
      "end": {"line": 12, "char": 20}
    }
  },
  {
    "file": "Notes/Related.md",
    "line": 3,
    "character": 15,
    "range": {
      "start": {"line": 3, "char": 15},
      "end": {"line": 3, "char": 27}
    }
  }
]
```

### 2. Build Recursive Backlink Graph

```bash
python scripts/lsp_integration.py recursive-backlinks \
  --vault ~/Documents/Obsidian \
  --file Index.md \
  --depth 3 \
  --output backlink_graph.json
```

**Output Structure:**
```json
{
  "file": "Index.md",
  "depth": 3,
  "backlinks": [
    {
      "file": "Projects/Project1.md",
      "line": 10,
      "character": 5,
      "recursive_backlinks": {
        "file": "Projects/Project1.md",
        "depth": 2,
        "backlinks": [...]
      }
    }
  ]
}
```

### 3. Analyze Vault Structure

```bash
python scripts/lsp_integration.py analyze-vault \
  --vault ~/Documents/Obsidian \
  --output vault_analysis.json
```

**Output:**
```json
{
  "total_files": 247,
  "total_links": 1534,
  "orphan_count": 12,
  "orphan_percentage": 4.9,
  "orphaned_files": [
    "Archive/Old_Note.md",
    "Temp/Draft.md"
  ],
  "strongly_connected_components": 3,
  "hub_notes": [
    {
      "file": "Index.md",
      "incoming_links": 45
    },
    {
      "file": "Projects/Main.md",
      "incoming_links": 32
    }
  ]
}
```

### 4. Search Vault Symbols

```bash
python scripts/lsp_integration.py search \
  --vault ~/Documents/Obsidian \
  --query "machine learning"
```

**Output:**
```json
[
  {
    "name": "Machine Learning Basics",
    "kind": "Function",
    "file": "Notes/ML_Basics.md",
    "location": {"line": 0, "character": 0},
    "container": "Learning"
  },
  {
    "name": "#machine-learning",
    "kind": "String",
    "file": "Projects/AI_Project.md",
    "location": {"line": 15, "character": 5},
    "container": null
  }
]
```

### 5. Get Heading Tree

```bash
python scripts/lsp_integration.py heading-tree \
  --vault ~/Documents/Obsidian \
  --file Research/Paper.md
```

**Output:**
```json
{
  "file": "Research/Paper.md",
  "symbols": [
    {
      "name": "Introduction",
      "kind": "Function",
      "range": {
        "start": {"line": 0, "char": 0},
        "end": {"line": 5, "char": 0}
      },
      "children": [
        {
          "name": "Background",
          "kind": "Function",
          "children": []
        }
      ]
    }
  ]
}
```

## Python API

### Basic Usage

```python
from pathlib import Path
from lsp_integration import (
    MarkdownOxideIntegration,
    RecursiveLSP,
    VaultLSPAnalyzer
)

# Initialize integration
vault = Path("~/Documents/Obsidian").expanduser()
integration = MarkdownOxideIntegration(vault, verbose=True)

# Find backlinks to a note
backlinks = integration.find_backlinks(vault / "Index.md")
print(f"Found {len(backlinks)} backlinks")

# Search vault
results = integration.search_vault("project management")
for result in results:
    print(f"{result['name']} in {result['file']}")

# Get heading tree
tree = integration.get_heading_tree(vault / "Notes.md")
print(json.dumps(tree, indent=2))
```

### Recursive Operations

```python
from lsp_integration import RecursiveLSP, MarkdownOxideIntegration

integration = MarkdownOxideIntegration(vault)
recursive = RecursiveLSP(integration)

# Build recursive backlink graph
graph = recursive.recursive_backlinks(
    vault / "Main.md",
    max_depth=3
)

# Find orphaned notes
md_files = list(vault.glob("**/*.md"))
orphans = recursive.find_orphans(md_files)
print(f"Orphaned notes: {orphans}")

# Build complete link graph
link_graph = recursive.build_link_graph(md_files)
print(f"Nodes: {link_graph['node_count']}")
print(f"Edges: {link_graph['edge_count']}")

# Find strongly connected components (circular references)
components = recursive.find_strongly_connected(md_files)
for i, component in enumerate(components):
    print(f"Component {i}: {component}")
```

### Vault Analysis

```python
from lsp_integration import VaultLSPAnalyzer

# Create analyzer
analyzer = VaultLSPAnalyzer(vault, verbose=True)

# Run comprehensive analysis
result = analyzer.process(output_path=Path("analysis.json"))

if result.success:
    print(f"Processed {result.files_processed} files")
    print(f"Orphans: {result.metadata['analysis']['orphan_count']}")
    print(f"Hubs: {result.metadata['analysis']['hub_notes'][:5]}")
```

## Advanced Features

### Custom LSP Operations

```python
from lsp_integration import LSPClient

client = LSPClient(vault)

# Go to definition
file_path = vault / "Notes.md"
definitions = client.goto_definition(file_path, line=10, character=5)

# Get hover information
hover = client.hover(file_path, line=10, character=5)
if hover:
    print(hover.contents)

# Document symbols
symbols = client.document_symbol(file_path)
for symbol in symbols:
    print(f"{symbol.name} ({symbol.kind_name})")

# Workspace symbol search
workspace_symbols = client.workspace_symbol("TODO")
```

### Call Hierarchy

```python
# Prepare call hierarchy for a symbol
items = client.prepare_call_hierarchy(file_path, line=5, character=10)

if items:
    item = items[0]

    # Get incoming calls (references)
    incoming = client.incoming_calls(item)
    print(f"Incoming calls: {len(incoming)}")

    # Get outgoing calls (dependencies)
    outgoing = client.outgoing_calls(item)
    print(f"Outgoing calls: {len(outgoing)}")
```

### Batch Processing Integration

```python
from batch_processor import VaultContext
from lsp_integration import VaultLSPAnalyzer

analyzer = VaultLSPAnalyzer(vault)

# Use VaultContext for rollback support
with VaultContext(vault) as ctx:
    # Analyze structure
    analysis = analyzer.analyze_vault_structure()

    # Find orphans
    orphans = analysis['orphaned_files']

    # Process orphans (e.g., add to archive)
    for orphan_path in orphans:
        file_path = vault / orphan_path
        # Process file...
        ctx.backup_file(file_path)

    # Commit changes
    ctx.commit()
```

## Integration with Existing Tools

### With WikilinkExtractor

```python
from wikilink_extractor import WikilinkExtractor
from lsp_integration import VaultLSPAnalyzer

# Extract wikilinks
extractor = WikilinkExtractor(vault)
wikilink_result = extractor.process()

# Analyze with LSP
analyzer = VaultLSPAnalyzer(vault)
lsp_result = analyzer.process()

# Compare results
print("Wikilink extraction found:", wikilink_result.metadata['statistics']['total_links'])
print("LSP analysis found:", lsp_result.metadata['analysis']['total_links'])
```

### With TagNormalizer

```python
from tag_normalizer import TagNormalizer
from lsp_integration import MarkdownOxideIntegration

# Search for tags via LSP
integration = MarkdownOxideIntegration(vault)
tag_results = integration.search_vault("#")

# Extract unique tags
tags = set(r['name'] for r in tag_results if r['name'].startswith('#'))

# Normalize tags
normalizer = TagNormalizer(vault)
result = normalizer.process(case_normalization='lower')
```

## Performance Considerations

### Large Vaults

For vaults with >1000 files:

```python
# Use batch processing with progress tracking
from tqdm import tqdm

md_files = list(vault.glob("**/*.md"))
results = []

for file_path in tqdm(md_files, desc="Analyzing files"):
    tree = integration.get_heading_tree(file_path)
    if tree:
        results.append(tree)
```

### Caching

```python
# Cache workspace symbol results
from functools import lru_cache

class CachedIntegration(MarkdownOxideIntegration):
    @lru_cache(maxsize=128)
    def search_vault(self, query: str):
        return super().search_vault(query)
```

## Troubleshooting

### LSP Tool Not Available

If you see "LSP tool not enabled" warnings:

```bash
# Enable LSP tool
export ENABLE_LSP_TOOL=1

# Verify environment
python -c "import os; print(os.environ.get('ENABLE_LSP_TOOL'))"
```

### Mock Mode

The integration runs in mock mode if LSP tool is unavailable:

```python
integration = MarkdownOxideIntegration(vault)
if integration.client.mock_mode:
    print("Running in mock mode - LSP features disabled")
```

### Debugging

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

integration = MarkdownOxideIntegration(vault, verbose=True)
# Detailed logs will be printed
```

## LSP Capabilities Reference

| Capability | Method | Description |
|------------|--------|-------------|
| Document Symbols | `document_symbol()` | Hierarchical heading tree |
| Workspace Symbols | `workspace_symbol()` | Fuzzy search (files, tags, headings) |
| References | `find_references()` | Find wikilink references |
| Go-to-Definition | `goto_definition()` | Resolve wikilink targets |
| Hover | `hover()` | Preview content with backlinks |
| Call Hierarchy | `prepare_call_hierarchy()` | Prepare call hierarchy |
| Incoming Calls | `incoming_calls()` | Get incoming references |
| Outgoing Calls | `outgoing_calls()` | Get outgoing dependencies |

## Data Structures

### LSPPosition

```python
@dataclass
class LSPPosition:
    line: int        # 0-indexed line number
    character: int   # 0-indexed character offset
```

### LSPRange

```python
@dataclass
class LSPRange:
    start: LSPPosition  # Range start
    end: LSPPosition    # Range end
```

### DocumentSymbol

```python
@dataclass
class DocumentSymbol:
    name: str                      # Symbol name
    kind: int                      # SymbolKind enum
    range: LSPRange                # Full range
    selection_range: LSPRange      # Identifier range
    detail: Optional[str]          # Additional details
    children: List[DocumentSymbol] # Child symbols
```

## Best Practices

1. **Use LSP for complex queries**: References, workspace search, call hierarchy
2. **Combine with BatchProcessor**: Leverage existing vault operations
3. **Cache results**: Workspace symbols and document symbols rarely change
4. **Handle mock mode**: Gracefully degrade when LSP unavailable
5. **Validate file paths**: Always resolve relative to vault root
6. **Log extensively**: Use verbose mode for debugging

## Examples

See `/Users/mikhail/.claude/skills/obsidian-process/examples/` for:

- `lsp_backlink_analysis.py`: Comprehensive backlink analysis
- `lsp_orphan_detection.py`: Find and handle orphaned notes
- `lsp_link_validation.py`: Validate all wikilinks
- `lsp_workspace_search.py`: Advanced workspace search
- `lsp_call_graph.py`: Build call/reference graphs

## Testing

```bash
# Run test suite
python scripts/test_lsp_integration.py

# Run specific test
python -m unittest test_lsp_integration.TestLSPClient
```

## Contributing

When extending LSP integration:

1. Follow existing BatchProcessor patterns
2. Add comprehensive error handling
3. Include tests for new features
4. Update documentation
5. Maintain backward compatibility
