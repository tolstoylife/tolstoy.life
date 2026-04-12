# LSP Patterns Reference for Obsidian Vault Processing

**Last Updated**: 2025-12-20
**markdown-oxide Version**: Latest (cargo install markdown-oxide)
**LSP Protocol Version**: 3.17

This document provides comprehensive patterns for integrating Language Server Protocol (LSP) capabilities with Obsidian vault batch processing using `markdown-oxide`, a specialized LSP server for Markdown and Obsidian.

---

## Table of Contents

1. [LSP Method Reference](#lsp-method-reference)
2. [Recursive Query Patterns](#recursive-query-patterns)
3. [Batch LSP Operations](#batch-lsp-operations)
4. [Integration Patterns](#integration-patterns)
5. [Performance Optimization](#performance-optimization)
6. [Troubleshooting](#troubleshooting)

---

## LSP Method Reference

### Core LSP Methods for Obsidian Vault Processing

| Method | Parameters | Return Type | Use Case |
|--------|-----------|-------------|----------|
| `initialize` | `rootUri`, `capabilities` | `InitializeResult` | Start LSP server, set vault root |
| `textDocument/hover` | `textDocument`, `position` | `Hover` | Get link preview, tag info, frontmatter details |
| `textDocument/definition` | `textDocument`, `position` | `Location[]` | Resolve wikilink target files |
| `textDocument/references` | `textDocument`, `position`, `includeDeclaration` | `Location[]` | Find backlinks to current note |
| `textDocument/documentSymbol` | `textDocument` | `DocumentSymbol[]` | Extract headers, tags, code blocks |
| `workspace/symbol` | `query` | `SymbolInformation[]` | Search all tags, headers, files by pattern |
| `textDocument/completion` | `textDocument`, `position` | `CompletionList` | Suggest wikilinks, tags during editing |
| `textDocument/publishDiagnostics` | - | `Diagnostic[]` | Detect broken links, invalid references |
| `textDocument/rename` | `textDocument`, `position`, `newName` | `WorkspaceEdit` | Rename notes, update all references |
| `textDocument/codeAction` | `textDocument`, `range`, `context` | `Command[]` | Fix broken links, create missing notes |

### markdown-oxide Specific Extensions

| Extension | Description | Use Case |
|-----------|-------------|----------|
| Tag Hierarchy | Parses nested tags (`#project/active/urgent`) | Tag normalization, taxonomy building |
| Wikilink Variants | Supports `[[Note]]`, `[[Note#Header]]`, `[[Note^block]]`, `![[embed]]` | Link extraction, validation |
| Frontmatter Parsing | YAML frontmatter as document symbols | Metadata analysis, template validation |
| Vault-wide Indexing | Maintains global graph of all notes | Backlink analysis, orphan detection |

---

## Recursive Query Patterns

### Backlink Chain Analysis

**Use Case**: Find all notes that reference a target note up to N levels deep.

```python
from typing import Dict, Set, List, Optional
from pathlib import Path
import json

class LSPClient:
    """Wrapper for markdown-oxide LSP client"""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.server = self._initialize_server()

    def _initialize_server(self):
        """Initialize markdown-oxide LSP server"""
        # Implementation: spawn subprocess, send initialize request
        pass

    def get_references(self, file_path: Path, position: Dict) -> List[Dict]:
        """Get all references to symbol at position"""
        return self._send_request("textDocument/references", {
            "textDocument": {"uri": f"file://{file_path.absolute()}"},
            "position": position,
            "context": {"includeDeclaration": True}
        })

    def get_backlink_chain(self, file: Path, depth: int = 3, visited: Optional[Set[Path]] = None) -> Dict:
        """
        Recursively find backlinks up to N levels deep.

        Args:
            file: Target file to find backlinks for
            depth: Maximum recursion depth (default: 3)
            visited: Set of already-visited files (prevents cycles)

        Returns:
            {
                "file": str,
                "level": int,
                "backlinks": [
                    {"file": str, "level": int, "backlinks": [...]}
                ]
            }
        """
        if visited is None:
            visited = set()

        if file in visited or depth == 0:
            return {"file": str(file), "level": depth, "backlinks": []}

        visited.add(file)

        # Get direct backlinks using LSP
        refs = self.get_references(file, {"line": 0, "character": 0})

        backlinks = []
        for ref in refs:
            ref_file = Path(ref["uri"].replace("file://", ""))
            if ref_file != file:  # Skip self-references
                child_chain = self.get_backlink_chain(ref_file, depth - 1, visited)
                backlinks.append(child_chain)

        return {
            "file": str(file),
            "level": depth,
            "backlinks": backlinks,
            "total_refs": len(refs)
        }

# Usage
client = LSPClient(Path("/path/to/vault"))
chain = client.get_backlink_chain(Path("/path/to/vault/Note.md"), depth=3)
print(json.dumps(chain, indent=2))
```

**Output Example**:
```json
{
  "file": "/vault/Projects/Main.md",
  "level": 3,
  "total_refs": 2,
  "backlinks": [
    {
      "file": "/vault/Daily/2024-01-15.md",
      "level": 2,
      "total_refs": 1,
      "backlinks": [
        {
          "file": "/vault/Weekly/2024-W03.md",
          "level": 1,
          "backlinks": []
        }
      ]
    }
  ]
}
```

### Reference Graph Building

**Use Case**: Build complete bidirectional reference graph of entire vault.

```python
from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import Dict, Set, List

@dataclass
class GraphNode:
    file: str
    outgoing_links: Set[str]
    incoming_links: Set[str]
    headers: List[str]
    tags: List[str]

class ReferenceGraphBuilder:
    def __init__(self, lsp_client: LSPClient):
        self.lsp = lsp_client
        self.graph: Dict[str, GraphNode] = {}

    def build_graph(self, vault_path: Path) -> Dict[str, GraphNode]:
        """
        Build complete reference graph using repeated LSP queries.

        Strategy:
        1. Get all markdown files
        2. For each file, extract document symbols (headers, tags)
        3. For each file, get all outgoing links via textDocument/definition
        4. For each file, get all incoming links via textDocument/references
        5. Combine into bidirectional graph
        """
        files = list(vault_path.rglob("*.md"))

        for file in files:
            node = self._process_file(file)
            self.graph[str(file)] = node

        return self.graph

    def _process_file(self, file: Path) -> GraphNode:
        """Extract all LSP data for single file"""

        # Get document symbols (headers, tags)
        symbols = self.lsp.get_document_symbols(file)
        headers = [s["name"] for s in symbols if s["kind"] == "heading"]
        tags = [s["name"] for s in symbols if s["kind"] == "tag"]

        # Get outgoing links (definitions of wikilinks)
        content = file.read_text()
        outgoing = set()
        for match in re.finditer(r'\[\[([^\]]+)\]\]', content):
            link_text = match.group(1)
            position = self._get_position_from_offset(content, match.start())
            definitions = self.lsp.get_definition(file, position)
            for defn in definitions:
                outgoing.add(defn["uri"].replace("file://", ""))

        # Get incoming links (references to this file)
        refs = self.lsp.get_references(file, {"line": 0, "character": 0})
        incoming = {ref["uri"].replace("file://", "") for ref in refs}

        return GraphNode(
            file=str(file),
            outgoing_links=outgoing,
            incoming_links=incoming,
            headers=headers,
            tags=tags
        )

    def _get_position_from_offset(self, content: str, offset: int) -> Dict:
        """Convert byte offset to LSP position (line, character)"""
        lines = content[:offset].split('\n')
        return {"line": len(lines) - 1, "character": len(lines[-1])}

    def export_json(self, output_path: Path):
        """Export graph as JSON"""
        serializable = {
            k: {
                "file": v.file,
                "outgoing_links": list(v.outgoing_links),
                "incoming_links": list(v.incoming_links),
                "headers": v.headers,
                "tags": v.tags
            }
            for k, v in self.graph.items()
        }
        output_path.write_text(json.dumps(serializable, indent=2))

# Usage
client = LSPClient(Path("/path/to/vault"))
builder = ReferenceGraphBuilder(client)
graph = builder.build_graph(Path("/path/to/vault"))
builder.export_json(Path("vault-graph.json"))
```

### Transitive Closure

**Use Case**: Find all notes transitively connected to a root note (A links to B, B links to C, etc.).

```python
def find_transitive_links(
    lsp_client: LSPClient,
    root_file: Path,
    direction: str = "forward",
    max_depth: int = 10
) -> Set[Path]:
    """
    Find all notes transitively connected via links.

    Args:
        root_file: Starting note
        direction: "forward" (outgoing) or "backward" (backlinks)
        max_depth: Maximum traversal depth

    Returns:
        Set of all connected file paths
    """
    visited = set()
    queue = [(root_file, 0)]

    while queue:
        current, depth = queue.pop(0)

        if current in visited or depth >= max_depth:
            continue

        visited.add(current)

        if direction == "forward":
            # Get outgoing links
            content = current.read_text()
            for match in re.finditer(r'\[\[([^\]]+)\]\]', content):
                position = _get_position_from_match(content, match)
                definitions = lsp_client.get_definition(current, position)
                for defn in definitions:
                    next_file = Path(defn["uri"].replace("file://", ""))
                    queue.append((next_file, depth + 1))
        else:
            # Get backlinks
            refs = lsp_client.get_references(current, {"line": 0, "character": 0})
            for ref in refs:
                next_file = Path(ref["uri"].replace("file://", ""))
                queue.append((next_file, depth + 1))

    return visited

# Usage: Find all notes in forward link chain
connected = find_transitive_links(
    lsp_client,
    Path("/vault/Projects/Main.md"),
    direction="forward",
    max_depth=5
)
print(f"Found {len(connected)} transitively connected notes")

# Usage: Find all notes that eventually reference this note
referrers = find_transitive_links(
    lsp_client,
    Path("/vault/Projects/Main.md"),
    direction="backward",
    max_depth=5
)
print(f"Found {len(referrers)} notes that transitively reference this note")
```

---

## Batch LSP Operations

### Sequential Processing

**Use Case**: Process large vaults efficiently with progress tracking.

```python
from tqdm import tqdm
import logging

class BatchLSPProcessor:
    def __init__(self, lsp_client: LSPClient, vault_path: Path):
        self.lsp = lsp_client
        self.vault = vault_path
        self.logger = logging.getLogger(__name__)

    def process_vault(self, operation_fn, batch_size: int = 50):
        """
        Process all markdown files with batching and progress tracking.

        Args:
            operation_fn: Function(file_path, lsp_client) -> result
            batch_size: Number of files to process before checkpointing
        """
        files = list(self.vault.rglob("*.md"))
        results = []

        with tqdm(total=len(files), desc="Processing vault") as pbar:
            for i, file in enumerate(files):
                try:
                    result = operation_fn(file, self.lsp)
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Error processing {file}: {e}")
                    results.append({"error": str(e), "file": str(file)})

                pbar.update(1)

                # Checkpoint every batch_size files
                if (i + 1) % batch_size == 0:
                    self._checkpoint(results, i + 1)

        return results

    def _checkpoint(self, results: List, count: int):
        """Save intermediate results"""
        checkpoint_file = self.vault / f".checkpoint_{count}.json"
        checkpoint_file.write_text(json.dumps(results, indent=2))
        self.logger.info(f"Checkpoint saved: {count} files processed")

# Example operation: Validate all wikilinks
def validate_wikilinks(file: Path, lsp: LSPClient) -> Dict:
    """Check if all wikilinks resolve to existing files"""
    content = file.read_text()
    wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)

    broken_links = []
    for link in wikilinks:
        position = _get_position_for_link(content, link)
        definitions = lsp.get_definition(file, position)
        if not definitions:
            broken_links.append(link)

    return {
        "file": str(file),
        "total_links": len(wikilinks),
        "broken_links": broken_links
    }

# Usage
processor = BatchLSPProcessor(lsp_client, Path("/path/to/vault"))
results = processor.process_vault(validate_wikilinks, batch_size=100)
```

### Result Aggregation

**Use Case**: Combine multiple LSP query results into vault statistics.

```python
class LSPAggregator:
    def __init__(self, lsp_client: LSPClient):
        self.lsp = lsp_client

    def aggregate_vault_statistics(self, vault_path: Path) -> Dict:
        """
        Combine results from multiple LSP queries into comprehensive stats.

        Returns:
            {
                "total_files": int,
                "total_links": int,
                "total_backlinks": int,
                "broken_links": List[Dict],
                "orphaned_notes": List[str],
                "tag_hierarchy": Dict,
                "most_referenced": List[Dict]
            }
        """
        files = list(vault_path.rglob("*.md"))

        stats = {
            "total_files": len(files),
            "total_links": 0,
            "total_backlinks": 0,
            "broken_links": [],
            "orphaned_notes": [],
            "tag_hierarchy": defaultdict(int),
            "most_referenced": []
        }

        file_ref_counts = {}

        for file in tqdm(files, desc="Aggregating statistics"):
            # Count outgoing links
            content = file.read_text()
            outgoing = len(re.findall(r'\[\[([^\]]+)\]\]', content))
            stats["total_links"] += outgoing

            # Count backlinks
            refs = self.lsp.get_references(file, {"line": 0, "character": 0})
            backlink_count = len(refs)
            stats["total_backlinks"] += backlink_count
            file_ref_counts[str(file)] = backlink_count

            # Identify orphans
            if backlink_count == 0 and outgoing == 0:
                stats["orphaned_notes"].append(str(file))

            # Extract tag hierarchy
            symbols = self.lsp.get_document_symbols(file)
            for symbol in symbols:
                if symbol.get("kind") == "tag":
                    tag = symbol["name"]
                    parts = tag.split("/")
                    for i in range(1, len(parts) + 1):
                        hierarchy_level = "/".join(parts[:i])
                        stats["tag_hierarchy"][hierarchy_level] += 1

        # Find most referenced notes
        stats["most_referenced"] = sorted(
            [{"file": k, "refs": v} for k, v in file_ref_counts.items()],
            key=lambda x: x["refs"],
            reverse=True
        )[:20]

        return stats

# Usage
aggregator = LSPAggregator(lsp_client)
stats = aggregator.aggregate_vault_statistics(Path("/path/to/vault"))
print(json.dumps(stats, indent=2))
```

### Error Handling

**Use Case**: Graceful degradation when LSP unavailable or slow.

```python
import time
from contextlib import contextmanager
from typing import Optional

class ResilientLSPClient:
    def __init__(self, vault_path: Path, timeout: int = 30):
        self.vault_path = vault_path
        self.timeout = timeout
        self.fallback_mode = False
        self._server = None

    @contextmanager
    def lsp_context(self):
        """Context manager for LSP operations with timeout and fallback"""
        try:
            if not self._server:
                self._server = self._start_server_with_timeout()
            yield self
        except Exception as e:
            logging.warning(f"LSP operation failed: {e}, falling back to regex parsing")
            self.fallback_mode = True
            yield self
        finally:
            self.fallback_mode = False

    def _start_server_with_timeout(self):
        """Start LSP server with timeout"""
        import subprocess
        import signal

        def timeout_handler(signum, frame):
            raise TimeoutError("LSP server startup timed out")

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self.timeout)

        try:
            # Start markdown-oxide
            proc = subprocess.Popen(
                ["markdown-oxide"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.vault_path)
            )
            # Send initialize request
            # ... implementation details
            return proc
        finally:
            signal.alarm(0)

    def get_definition(self, file: Path, position: Dict) -> List[Dict]:
        """Get definition with fallback to regex if LSP unavailable"""
        if not self.fallback_mode:
            try:
                return self._lsp_get_definition(file, position)
            except Exception as e:
                logging.warning(f"LSP definition query failed: {e}")
                self.fallback_mode = True

        # Fallback: regex-based link resolution
        return self._regex_get_definition(file, position)

    def _regex_get_definition(self, file: Path, position: Dict) -> List[Dict]:
        """Fallback link resolution using regex"""
        content = file.read_text()
        lines = content.split('\n')
        line_text = lines[position["line"]]

        # Extract wikilink at position
        match = re.search(r'\[\[([^\]]+)\]\]', line_text)
        if not match:
            return []

        link_text = match.group(1).split('|')[0].split('#')[0]

        # Search for matching files
        potential_targets = list(self.vault_path.rglob(f"*{link_text}*.md"))

        return [
            {"uri": f"file://{target.absolute()}"}
            for target in potential_targets
        ]

# Usage
with ResilientLSPClient(Path("/path/to/vault")).lsp_context() as lsp:
    results = lsp.get_definition(Path("/vault/Note.md"), {"line": 5, "character": 10})
    # Automatically falls back to regex if LSP fails
```

---

## Integration Patterns

### With WikilinkExtractor

**Pattern**: Validate extracted wikilinks using LSP goToDefinition to ensure accuracy.

```python
class LSPEnhancedWikilinkExtractor:
    def __init__(self, lsp_client: LSPClient):
        self.lsp = lsp_client

    def extract_and_validate(self, file: Path) -> Dict:
        """
        Extract wikilinks with LSP validation.

        Returns:
            {
                "file": str,
                "links": [
                    {
                        "text": str,
                        "target": str,
                        "valid": bool,
                        "resolved_path": Optional[str]
                    }
                ]
            }
        """
        content = file.read_text()
        links = []

        for match in re.finditer(r'\[\[([^\]]+)\]\]', content):
            link_text = match.group(1)
            position = self._get_position(content, match.start())

            # Use LSP to validate and resolve
            definitions = self.lsp.get_definition(file, position)

            links.append({
                "text": link_text,
                "target": link_text.split('|')[0].split('#')[0],
                "valid": len(definitions) > 0,
                "resolved_path": definitions[0]["uri"].replace("file://", "") if definitions else None
            })

        return {"file": str(file), "links": links}

# Usage
extractor = LSPEnhancedWikilinkExtractor(lsp_client)
result = extractor.extract_and_validate(Path("/vault/Note.md"))

# Filter to broken links
broken = [link for link in result["links"] if not link["valid"]]
print(f"Found {len(broken)} broken links")
```

### With TagNormalizer

**Pattern**: Use workspace/symbol to discover all tag usages before normalization.

```python
class LSPEnhancedTagNormalizer:
    def __init__(self, lsp_client: LSPClient):
        self.lsp = lsp_client

    def preview_normalization(self, vault_path: Path, rules: Dict) -> Dict:
        """
        Preview tag normalization using LSP workspace symbols.

        Args:
            rules: {"case": "lower"} or custom transformation rules

        Returns:
            {
                "affected_tags": List[str],
                "affected_files": List[str],
                "preview": Dict[str, str]  # old_tag -> new_tag
            }
        """
        # Use workspace/symbol to find all tags
        all_tags = self.lsp.workspace_symbol(query="#")

        tag_locations = defaultdict(list)
        for symbol in all_tags:
            if symbol["kind"] == "tag":
                tag_name = symbol["name"]
                tag_locations[tag_name].append(symbol["location"]["uri"])

        # Preview transformations
        preview = {}
        affected_files = set()

        for tag, locations in tag_locations.items():
            new_tag = self._apply_rules(tag, rules)
            if new_tag != tag:
                preview[tag] = new_tag
                affected_files.update(locations)

        return {
            "affected_tags": list(preview.keys()),
            "affected_files": list(affected_files),
            "preview": preview,
            "total_occurrences": sum(len(locs) for locs in tag_locations.values())
        }

    def _apply_rules(self, tag: str, rules: Dict) -> str:
        """Apply normalization rules to tag"""
        if rules.get("case") == "lower":
            return tag.lower()
        elif rules.get("case") == "upper":
            return tag.upper()
        # Add more transformation logic
        return tag

# Usage
normalizer = LSPEnhancedTagNormalizer(lsp_client)
preview = normalizer.preview_normalization(
    Path("/path/to/vault"),
    {"case": "lower"}
)
print(f"Will affect {len(preview['affected_tags'])} tags in {len(preview['affected_files'])} files")
```

### With FrontmatterProcessor

**Pattern**: Use hover to preview metadata changes before applying.

```python
class LSPEnhancedFrontmatterProcessor:
    def __init__(self, lsp_client: LSPClient):
        self.lsp = lsp_client

    def preview_frontmatter_change(self, file: Path, key: str, value: str) -> Dict:
        """
        Preview frontmatter change using LSP hover for context.

        Returns:
            {
                "current_value": Any,
                "new_value": str,
                "hover_info": str,  # LSP hover content
                "will_create": bool
            }
        """
        content = file.read_text()

        # Parse frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            return {
                "current_value": None,
                "new_value": value,
                "hover_info": "No frontmatter exists",
                "will_create": True
            }

        frontmatter = yaml.safe_load(frontmatter_match.group(1))
        current = frontmatter.get(key)

        # Use LSP hover to get context about this frontmatter field
        # (if markdown-oxide supports frontmatter hover)
        hover_info = self.lsp.hover(file, {"line": 1, "character": 0})

        return {
            "current_value": current,
            "new_value": value,
            "hover_info": hover_info.get("contents", ""),
            "will_create": key not in frontmatter
        }

# Usage
processor = LSPEnhancedFrontmatterProcessor(lsp_client)
preview = processor.preview_frontmatter_change(
    Path("/vault/Note.md"),
    "status",
    "published"
)
print(f"Current: {preview['current_value']} -> New: {preview['new_value']}")
```

### With VaultAnalyzer

**Pattern**: Enhance health scoring with LSP diagnostics for unresolved references.

```python
class LSPEnhancedVaultAnalyzer:
    def __init__(self, lsp_client: LSPClient):
        self.lsp = lsp_client

    def compute_health_score(self, vault_path: Path) -> Dict:
        """
        Compute vault health using LSP diagnostics.

        Health factors:
        - Broken link percentage (from diagnostics)
        - Orphaned note percentage
        - Tag consistency
        - Frontmatter completeness

        Returns:
            {
                "score": float (0-100),
                "factors": Dict[str, float],
                "issues": List[Dict]
            }
        """
        files = list(vault_path.rglob("*.md"))

        # Collect LSP diagnostics for all files
        all_diagnostics = []
        for file in files:
            diagnostics = self.lsp.get_diagnostics(file)
            all_diagnostics.extend(diagnostics)

        # Count issue types
        broken_links = [d for d in all_diagnostics if "link" in d.get("message", "").lower()]

        # Calculate factors
        broken_link_pct = len(broken_links) / len(files) * 100 if files else 0

        # Find orphans using references
        orphan_count = 0
        for file in files:
            refs = self.lsp.get_references(file, {"line": 0, "character": 0})
            content = file.read_text()
            outgoing = len(re.findall(r'\[\[', content))
            if len(refs) == 0 and outgoing == 0:
                orphan_count += 1

        orphan_pct = orphan_count / len(files) * 100 if files else 0

        # Compute health score (0-100)
        score = max(0, 100 - broken_link_pct - orphan_pct)

        return {
            "score": round(score, 2),
            "factors": {
                "broken_links": broken_link_pct,
                "orphaned_notes": orphan_pct,
                "total_files": len(files)
            },
            "issues": [
                {"file": d["uri"], "message": d["message"]}
                for d in all_diagnostics
            ]
        }

# Usage
analyzer = LSPEnhancedVaultAnalyzer(lsp_client)
health = analyzer.compute_health_score(Path("/path/to/vault"))
print(f"Vault Health Score: {health['score']}/100")
```

---

## Performance Optimization

### Caching LSP Results

**Pattern**: Cache frequently-used LSP queries to reduce overhead.

```python
from functools import lru_cache
import hashlib
import pickle

class CachedLSPClient:
    def __init__(self, lsp_client: LSPClient, cache_dir: Path):
        self.lsp = lsp_client
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)

    def _cache_key(self, method: str, params: Dict) -> str:
        """Generate cache key from method + params"""
        key_str = f"{method}:{json.dumps(params, sort_keys=True)}"
        return hashlib.sha256(key_str.encode()).hexdigest()

    def cached_query(self, method: str, params: Dict, ttl_seconds: int = 3600) -> Any:
        """
        Execute LSP query with file-based caching.

        Args:
            method: LSP method name
            params: Method parameters
            ttl_seconds: Cache time-to-live
        """
        cache_key = self._cache_key(method, params)
        cache_file = self.cache_dir / f"{cache_key}.pkl"

        # Check cache
        if cache_file.exists():
            cache_age = time.time() - cache_file.stat().st_mtime
            if cache_age < ttl_seconds:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)

        # Execute query
        result = self.lsp.send_request(method, params)

        # Cache result
        with open(cache_file, 'wb') as f:
            pickle.dump(result, f)

        return result

    @lru_cache(maxsize=1000)
    def get_references_cached(self, file_path: str, line: int, char: int) -> tuple:
        """In-memory cache for reference queries"""
        result = self.lsp.get_references(
            Path(file_path),
            {"line": line, "character": char}
        )
        # Convert to tuple for hashability
        return tuple(json.dumps(r) for r in result)

# Usage
cached_client = CachedLSPClient(lsp_client, Path("/tmp/lsp_cache"))
refs = cached_client.cached_query(
    "textDocument/references",
    {"textDocument": {"uri": "file:///vault/Note.md"}, "position": {"line": 0, "character": 0}},
    ttl_seconds=3600
)
```

### Incremental Updates

**Pattern**: Only re-query changed files using file modification tracking.

```python
class IncrementalLSPProcessor:
    def __init__(self, lsp_client: LSPClient, vault_path: Path):
        self.lsp = lsp_client
        self.vault = vault_path
        self.index_file = vault_path / ".lsp_index.json"
        self.index = self._load_index()

    def _load_index(self) -> Dict:
        """Load previously processed file index"""
        if self.index_file.exists():
            return json.loads(self.index_file.read_text())
        return {}

    def _save_index(self):
        """Save file index"""
        self.index_file.write_text(json.dumps(self.index, indent=2))

    def get_changed_files(self) -> List[Path]:
        """Identify files that changed since last run"""
        files = list(self.vault.rglob("*.md"))
        changed = []

        for file in files:
            file_key = str(file)
            current_mtime = file.stat().st_mtime

            if file_key not in self.index or self.index[file_key]["mtime"] < current_mtime:
                changed.append(file)
                self.index[file_key] = {"mtime": current_mtime}

        return changed

    def incremental_process(self, operation_fn):
        """Process only changed files"""
        changed = self.get_changed_files()

        print(f"Processing {len(changed)} changed files (out of {len(list(self.vault.rglob('*.md')))} total)")

        results = []
        for file in tqdm(changed, desc="Incremental processing"):
            result = operation_fn(file, self.lsp)
            results.append(result)

        self._save_index()
        return results

# Usage
processor = IncrementalLSPProcessor(lsp_client, Path("/path/to/vault"))
results = processor.incremental_process(validate_wikilinks)
print(f"Processed {len(results)} changed files")
```

### Parallel LSP Queries

**Pattern**: Concurrent LSP operations for large vaults.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class ParallelLSPProcessor:
    def __init__(self, lsp_client: LSPClient, max_workers: int = 8):
        self.lsp = lsp_client
        self.max_workers = max_workers
        self._lock = threading.Lock()

    def parallel_process(self, files: List[Path], operation_fn) -> List[Dict]:
        """
        Process files in parallel using thread pool.

        Note: markdown-oxide should support concurrent requests.
        If not, use process pool with separate LSP instances.
        """
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(operation_fn, file, self.lsp): file
                for file in files
            }

            # Collect results with progress
            with tqdm(total=len(files), desc="Parallel processing") as pbar:
                for future in as_completed(future_to_file):
                    file = future_to_file[future]
                    try:
                        result = future.result()
                        with self._lock:
                            results.append(result)
                    except Exception as e:
                        logging.error(f"Error processing {file}: {e}")
                    pbar.update(1)

        return results

# Usage
processor = ParallelLSPProcessor(lsp_client, max_workers=8)
files = list(Path("/path/to/vault").rglob("*.md"))
results = processor.parallel_process(files, validate_wikilinks)
```

---

## Troubleshooting

### Common Issues

#### Issue: LSP Server Not Starting

**Symptoms**: `TimeoutError` or `ConnectionRefusedError` when initializing.

**Solutions**:

1. Verify markdown-oxide installation:
   ```bash
   which markdown-oxide
   markdown-oxide --version
   ```

2. Test server manually:
   ```bash
   cd /path/to/vault
   markdown-oxide
   # Should start and wait for JSON-RPC input
   ```

3. Check stderr for initialization errors:
   ```python
   proc = subprocess.Popen(
       ["markdown-oxide"],
       stdin=subprocess.PIPE,
       stdout=subprocess.PIPE,
       stderr=subprocess.PIPE
   )
   _, stderr = proc.communicate(timeout=5)
   print(stderr.decode())
   ```

4. Ensure vault path is absolute and exists:
   ```python
   vault_path = Path("/path/to/vault").resolve()
   assert vault_path.exists(), "Vault path does not exist"
   ```

#### Issue: Slow Responses on Large Vaults

**Symptoms**: LSP queries take >5 seconds, especially for `workspace/symbol`.

**Solutions**:

1. Use incremental processing (see [Incremental Updates](#incremental-updates))

2. Limit query scope:
   ```python
   # Instead of workspace/symbol for all tags
   symbols = lsp.workspace_symbol("#project")  # Narrow query
   ```

3. Pre-build index once, then cache:
   ```python
   # Build comprehensive index
   graph = build_complete_graph(lsp, vault_path)
   # Save to disk
   save_graph(graph, "vault_index.json")
   # Use cached graph for subsequent queries
   ```

4. Use file-based filtering before LSP queries:
   ```python
   # Filter files first using fast tools (fd, rg)
   files_with_tags = subprocess.check_output(
       ["rg", "--files-with-matches", r"#\w+", str(vault_path)]
   ).decode().splitlines()
   # Then run LSP only on relevant files
   ```

#### Issue: Memory Issues with Deep Recursion

**Symptoms**: `RecursionError` or memory exhaustion during backlink chain analysis.

**Solutions**:

1. Limit recursion depth:
   ```python
   chain = get_backlink_chain(file, depth=3)  # Instead of depth=10
   ```

2. Use iterative approach instead of recursive:
   ```python
   def iterative_backlink_chain(file: Path, max_depth: int) -> Dict:
       queue = [(file, 0, [])]
       result_tree = {}

       while queue:
           current, depth, path = queue.pop(0)

           if depth >= max_depth or current in path:
               continue

           refs = lsp.get_references(current, {"line": 0, "character": 0})
           # Build tree iteratively
   ```

3. Stream results instead of building entire graph:
   ```python
   def stream_backlinks(file: Path) -> Iterator[Dict]:
       """Yield backlinks one at a time"""
       refs = lsp.get_references(file, {"line": 0, "character": 0})
       for ref in refs:
           yield {"file": ref["uri"], "line": ref["range"]["start"]["line"]}
   ```

### Diagnostic Commands

#### Verify LSP is Working Correctly

```bash
# Test LSP server health
python -c "
from lsp_client import LSPClient
from pathlib import Path

client = LSPClient(Path('/path/to/vault'))
print('LSP initialized:', client.initialized)

# Test basic queries
test_file = Path('/path/to/vault/Test.md')
refs = client.get_references(test_file, {'line': 0, 'character': 0})
print(f'References found: {len(refs)}')
"
```

#### Debug LSP Communication

```python
import logging

logging.basicConfig(level=logging.DEBUG)

class DebugLSPClient(LSPClient):
    def send_request(self, method: str, params: Dict) -> Any:
        logging.debug(f"Sending: {method} {json.dumps(params)}")
        result = super().send_request(method, params)
        logging.debug(f"Received: {json.dumps(result)[:200]}")
        return result

# Usage
debug_client = DebugLSPClient(Path("/path/to/vault"))
# All LSP traffic will be logged
```

#### Performance Profiling

```python
import cProfile
import pstats

def profile_lsp_operation():
    profiler = cProfile.Profile()
    profiler.enable()

    # Run operation
    client = LSPClient(Path("/path/to/vault"))
    graph = build_reference_graph(client, Path("/path/to/vault"))

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)

profile_lsp_operation()
```

#### Check Index Freshness

```bash
# Show files that need re-indexing
python -c "
from incremental_processor import IncrementalLSPProcessor
from pathlib import Path

processor = IncrementalLSPProcessor(lsp_client, Path('/path/to/vault'))
changed = processor.get_changed_files()
print(f'{len(changed)} files need re-processing')
for file in changed[:10]:
    print(f'  - {file}')
"
```

---

## Quick Reference

### Essential LSP Methods

| Need | LSP Method | Key Parameter |
|------|-----------|---------------|
| Resolve wikilink | `textDocument/definition` | `position` on `[[link]]` |
| Find backlinks | `textDocument/references` | `includeDeclaration: true` |
| Get all tags | `workspace/symbol` | `query: "#"` |
| Extract headers | `textDocument/documentSymbol` | Document URI |
| Detect broken links | `textDocument/publishDiagnostics` | Auto-published |
| Rename note | `textDocument/rename` | `newName` |

### Performance Tips

1. **Cache aggressively**: References and symbols rarely change
2. **Use incremental updates**: Only process changed files
3. **Parallelize when possible**: LSP supports concurrent requests
4. **Fallback to regex**: For non-critical queries, regex is faster
5. **Index once, query many**: Build graph upfront, query in-memory

### Best Practices

- Always validate LSP server is running before batch operations
- Use `try/except` with fallback for resilience
- Log LSP errors for debugging
- Checkpoint large batch operations
- Test on small vault subset before full run

---

## Appendix: Complete LSP Client Implementation

See `scripts/lsp_client.py` for production-ready implementation with:
- Initialization sequence
- Request/response handling
- Error recovery
- Graceful shutdown
- Type hints
- Comprehensive logging

---

**References**:
- [LSP Specification 3.17](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/)
- [markdown-oxide GitHub](https://github.com/Feel-ix-343/markdown-oxide)
- [Obsidian Syntax Guide](https://help.obsidian.md/Editing+and+formatting/Obsidian+Flavored+Markdown)
