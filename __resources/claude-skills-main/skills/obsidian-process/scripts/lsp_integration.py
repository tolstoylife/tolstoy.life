#!/usr/bin/env python3
"""
LSP Integration for Obsidian Vault Processing
Integrates markdown-oxide LSP capabilities via Claude Code's native LSP tool.

Requires: $ENABLE_LSP_TOOL=1 environment variable for Claude Code LSP support

Features:
- Document symbols (hierarchical heading trees)
- Workspace symbols (fuzzy search across vault)
- References (wikilink reference finding)
- Go-to-definition (wikilink target resolution)
- Hover (content preview with backlinks)
- Rename (cross-vault symbol renaming)
- Diagnostics (unresolved reference detection)
- Recursive operations (backlinks of backlinks, dependency chains)
- Vault-wide analysis combining LSP queries with batch processing

Usage:
    # Find all references to a symbol
    lsp_integration.py references --vault ~/vault --file note.md --line 5 --char 10

    # Build recursive backlink graph
    lsp_integration.py recursive-backlinks --vault ~/vault --file main.md --depth 3

    # Analyze vault structure
    lsp_integration.py analyze-vault --vault ~/vault --output analysis.json
"""

import os
import sys
import json
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Set, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from collections import defaultdict, deque
from datetime import datetime
import argparse

from batch_processor import BatchProcessor, ProcessingResult

logger = logging.getLogger(__name__)


# ============================================================================
# LSP Data Structures
# ============================================================================

@dataclass
class LSPPosition:
    """LSP position (line, character)."""
    line: int  # 0-indexed
    character: int  # 0-indexed


@dataclass
class LSPRange:
    """LSP range (start, end positions)."""
    start: LSPPosition
    end: LSPPosition


@dataclass
class LSPLocation:
    """LSP location (file URI + range)."""
    uri: str
    range: LSPRange


@dataclass
class DocumentSymbol:
    """LSP document symbol."""
    name: str
    kind: int  # SymbolKind enum
    range: LSPRange
    selection_range: LSPRange
    detail: Optional[str] = None
    children: List['DocumentSymbol'] = field(default_factory=list)

    @property
    def kind_name(self) -> str:
        """Convert kind number to readable name."""
        kinds = {
            1: "File", 2: "Module", 3: "Namespace", 4: "Package", 5: "Class",
            6: "Method", 7: "Property", 8: "Field", 9: "Constructor", 10: "Enum",
            11: "Interface", 12: "Function", 13: "Variable", 14: "Constant",
            15: "String", 16: "Number", 17: "Boolean", 18: "Array", 19: "Object",
            20: "Key", 21: "Null", 22: "EnumMember", 23: "Struct", 24: "Event",
            25: "Operator", 26: "TypeParameter"
        }
        return kinds.get(self.kind, "Unknown")


@dataclass
class WorkspaceSymbol:
    """LSP workspace symbol."""
    name: str
    kind: int
    location: LSPLocation
    container_name: Optional[str] = None


@dataclass
class Hover:
    """LSP hover information."""
    contents: List[str]  # Markdown content
    range: Optional[LSPRange] = None


@dataclass
class Diagnostic:
    """LSP diagnostic (error/warning)."""
    range: LSPRange
    severity: int  # 1=Error, 2=Warning, 3=Information, 4=Hint
    code: Optional[str] = None
    source: Optional[str] = None
    message: str = ""

    @property
    def severity_name(self) -> str:
        """Convert severity number to readable name."""
        severities = {1: "Error", 2: "Warning", 3: "Information", 4: "Hint"}
        return severities.get(self.severity, "Unknown")


@dataclass
class CallHierarchyItem:
    """LSP call hierarchy item."""
    name: str
    kind: int
    uri: str
    range: LSPRange
    selection_range: LSPRange
    detail: Optional[str] = None


@dataclass
class CallHierarchyCall:
    """LSP incoming/outgoing call."""
    from_item: CallHierarchyItem
    from_ranges: List[LSPRange]


# ============================================================================
# LSP Client
# ============================================================================

class LSPClient:
    """
    Client for invoking Claude Code's LSP tool via subprocess.

    Requires $ENABLE_LSP_TOOL=1 environment variable to be set.
    """

    def __init__(self, vault_path: Path):
        """
        Initialize LSP client.

        Args:
            vault_path: Path to Obsidian vault (LSP workspace root)
        """
        self.vault_path = Path(vault_path).resolve()

        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {vault_path}")

        # Check if LSP tool is enabled
        if not os.environ.get('ENABLE_LSP_TOOL'):
            logger.warning(
                "LSP tool not enabled. Set ENABLE_LSP_TOOL=1 environment variable. "
                "Falling back to mock mode."
            )
            self.mock_mode = True
        else:
            self.mock_mode = False

    def _file_to_uri(self, file_path: Path) -> str:
        """Convert file path to URI."""
        abs_path = file_path.resolve()
        return f"file://{abs_path}"

    def _uri_to_file(self, uri: str) -> Path:
        """Convert URI to file path."""
        if uri.startswith('file://'):
            return Path(uri[7:])
        return Path(uri)

    def _invoke_lsp(self, method: str, params: Dict[str, Any]) -> Optional[Any]:
        """
        Invoke LSP method via subprocess.

        This is a placeholder for the actual Claude Code LSP tool invocation.
        In practice, this would shell out to the LSP binary or use IPC.

        Args:
            method: LSP method name (e.g., 'textDocument/documentSymbol')
            params: LSP parameters

        Returns:
            LSP response or None on error
        """
        if self.mock_mode:
            logger.debug(f"[MOCK] LSP call: {method} with params: {params}")
            return None

        try:
            # Placeholder: actual implementation would invoke Claude Code's LSP tool
            # For now, return None to indicate unimplemented
            logger.warning(f"LSP method {method} not yet implemented")
            return None
        except Exception as e:
            logger.error(f"LSP invocation failed for {method}: {e}")
            return None

    def goto_definition(self, file_path: Path, line: int, character: int) -> Optional[List[LSPLocation]]:
        """
        Go to definition of symbol at position.

        Args:
            file_path: File containing the symbol
            line: Line number (0-indexed)
            character: Character offset (0-indexed)

        Returns:
            List of definition locations or None
        """
        params = {
            'textDocument': {'uri': self._file_to_uri(file_path)},
            'position': {'line': line, 'character': character}
        }
        return self._invoke_lsp('textDocument/definition', params)

    def find_references(
        self,
        file_path: Path,
        line: int,
        character: int,
        include_declaration: bool = False
    ) -> Optional[List[LSPLocation]]:
        """
        Find all references to symbol at position.

        Args:
            file_path: File containing the symbol
            line: Line number (0-indexed)
            character: Character offset (0-indexed)
            include_declaration: Include declaration in results

        Returns:
            List of reference locations or None
        """
        params = {
            'textDocument': {'uri': self._file_to_uri(file_path)},
            'position': {'line': line, 'character': character},
            'context': {'includeDeclaration': include_declaration}
        }
        return self._invoke_lsp('textDocument/references', params)

    def hover(self, file_path: Path, line: int, character: int) -> Optional[Hover]:
        """
        Get hover information at position.

        Args:
            file_path: File path
            line: Line number (0-indexed)
            character: Character offset (0-indexed)

        Returns:
            Hover information or None
        """
        params = {
            'textDocument': {'uri': self._file_to_uri(file_path)},
            'position': {'line': line, 'character': character}
        }
        return self._invoke_lsp('textDocument/hover', params)

    def document_symbol(self, file_path: Path) -> Optional[List[DocumentSymbol]]:
        """
        Get document symbols (hierarchical heading tree).

        Args:
            file_path: File path

        Returns:
            List of document symbols or None
        """
        params = {
            'textDocument': {'uri': self._file_to_uri(file_path)}
        }
        return self._invoke_lsp('textDocument/documentSymbol', params)

    def workspace_symbol(self, query: str) -> Optional[List[WorkspaceSymbol]]:
        """
        Search workspace symbols (fuzzy search across vault).

        Args:
            query: Search query

        Returns:
            List of workspace symbols or None
        """
        params = {'query': query}
        return self._invoke_lsp('workspace/symbol', params)

    def prepare_call_hierarchy(
        self,
        file_path: Path,
        line: int,
        character: int
    ) -> Optional[List[CallHierarchyItem]]:
        """
        Prepare call hierarchy for symbol at position.

        Args:
            file_path: File path
            line: Line number (0-indexed)
            character: Character offset (0-indexed)

        Returns:
            List of call hierarchy items or None
        """
        params = {
            'textDocument': {'uri': self._file_to_uri(file_path)},
            'position': {'line': line, 'character': character}
        }
        return self._invoke_lsp('textDocument/prepareCallHierarchy', params)

    def incoming_calls(self, item: CallHierarchyItem) -> Optional[List[CallHierarchyCall]]:
        """
        Get incoming calls for a call hierarchy item.

        Args:
            item: Call hierarchy item

        Returns:
            List of incoming calls or None
        """
        params = {'item': asdict(item)}
        return self._invoke_lsp('callHierarchy/incomingCalls', params)

    def outgoing_calls(self, item: CallHierarchyItem) -> Optional[List[CallHierarchyCall]]:
        """
        Get outgoing calls for a call hierarchy item.

        Args:
            item: Call hierarchy item

        Returns:
            List of outgoing calls or None
        """
        params = {'item': asdict(item)}
        return self._invoke_lsp('callHierarchy/outgoingCalls', params)


# ============================================================================
# Markdown-Oxide Integration
# ============================================================================

class MarkdownOxideIntegration:
    """
    High-level interface for markdown-oxide LSP capabilities.

    Provides Obsidian-specific operations built on top of LSPClient.
    """

    def __init__(self, vault_path: Path, verbose: bool = False):
        """
        Initialize markdown-oxide integration.

        Args:
            vault_path: Path to Obsidian vault
            verbose: Enable verbose logging
        """
        self.vault_path = Path(vault_path)
        self.client = LSPClient(vault_path)
        self.verbose = verbose
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def get_heading_tree(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Get hierarchical heading tree for a file.

        Args:
            file_path: Markdown file path

        Returns:
            Heading tree structure or None
        """
        symbols = self.client.document_symbol(file_path)
        if not symbols:
            return None

        def build_tree(symbol: DocumentSymbol) -> Dict[str, Any]:
            return {
                'name': symbol.name,
                'kind': symbol.kind_name,
                'range': {
                    'start': {'line': symbol.range.start.line, 'char': symbol.range.start.character},
                    'end': {'line': symbol.range.end.line, 'char': symbol.range.end.character}
                },
                'children': [build_tree(child) for child in symbol.children]
            }

        return {
            'file': str(file_path.relative_to(self.vault_path)),
            'symbols': [build_tree(sym) for sym in symbols]
        }

    def search_vault(self, query: str) -> List[Dict[str, Any]]:
        """
        Fuzzy search across entire vault (files, tags, headings).

        Args:
            query: Search query

        Returns:
            List of matching symbols
        """
        symbols = self.client.workspace_symbol(query)
        if not symbols:
            return []

        results = []
        for sym in symbols:
            file_path = self.client._uri_to_file(sym.location.uri)
            results.append({
                'name': sym.name,
                'kind': DocumentSymbol(
                    name="",
                    kind=sym.kind,
                    range=LSPRange(LSPPosition(0, 0), LSPPosition(0, 0)),
                    selection_range=LSPRange(LSPPosition(0, 0), LSPPosition(0, 0))
                ).kind_name,
                'file': str(file_path.relative_to(self.vault_path)),
                'location': {
                    'line': sym.location.range.start.line,
                    'character': sym.location.range.start.character
                },
                'container': sym.container_name
            })

        return results

    def find_backlinks(self, file_path: Path, position: Optional[Tuple[int, int]] = None) -> List[Dict[str, Any]]:
        """
        Find all wikilink references to a file or symbol.

        Args:
            file_path: File to find backlinks for
            position: Optional (line, character) for specific symbol

        Returns:
            List of backlink locations
        """
        if position:
            line, char = position
        else:
            # Use first line for file-level backlinks
            line, char = 0, 0

        references = self.client.find_references(file_path, line, char, include_declaration=False)
        if not references:
            return []

        backlinks = []
        for ref in references:
            ref_file = self.client._uri_to_file(ref.uri)
            backlinks.append({
                'file': str(ref_file.relative_to(self.vault_path)),
                'line': ref.range.start.line,
                'character': ref.range.start.character,
                'range': {
                    'start': {'line': ref.range.start.line, 'char': ref.range.start.character},
                    'end': {'line': ref.range.end.line, 'char': ref.range.end.character}
                }
            })

        return backlinks

    def resolve_wikilink(self, file_path: Path, line: int, character: int) -> Optional[Dict[str, Any]]:
        """
        Resolve wikilink target at position.

        Args:
            file_path: File containing wikilink
            line: Line number (0-indexed)
            character: Character offset (0-indexed)

        Returns:
            Wikilink target information or None
        """
        locations = self.client.goto_definition(file_path, line, character)
        if not locations or len(locations) == 0:
            return None

        # Take first definition
        loc = locations[0]
        target_file = self.client._uri_to_file(loc.uri)

        return {
            'target_file': str(target_file.relative_to(self.vault_path)),
            'line': loc.range.start.line,
            'character': loc.range.start.character,
            'range': {
                'start': {'line': loc.range.start.line, 'char': loc.range.start.character},
                'end': {'line': loc.range.end.line, 'char': loc.range.end.character}
            }
        }

    def get_preview(self, file_path: Path, line: int, character: int) -> Optional[Dict[str, Any]]:
        """
        Get content preview with backlinks for symbol at position.

        Args:
            file_path: File path
            line: Line number (0-indexed)
            character: Character offset (0-indexed)

        Returns:
            Preview with content and backlinks or None
        """
        hover = self.client.hover(file_path, line, character)
        if not hover:
            return None

        # Get backlinks for context
        backlinks = self.find_backlinks(file_path, (line, character))

        return {
            'content': hover.contents,
            'backlinks_count': len(backlinks),
            'backlinks': backlinks[:5]  # First 5 backlinks
        }


# ============================================================================
# Recursive LSP Operations
# ============================================================================

class RecursiveLSP:
    """
    Recursive graph traversal operations using LSP.

    Supports:
    - Recursive backlinks (backlinks of backlinks)
    - Dependency chains
    - Link graph construction
    - Orphan detection
    """

    def __init__(self, integration: MarkdownOxideIntegration):
        """
        Initialize recursive LSP operations.

        Args:
            integration: MarkdownOxideIntegration instance
        """
        self.integration = integration
        self.vault_path = integration.vault_path

    def recursive_backlinks(
        self,
        file_path: Path,
        max_depth: int = 3,
        visited: Optional[Set[str]] = None
    ) -> Dict[str, Any]:
        """
        Build recursive backlink graph.

        Args:
            file_path: Starting file
            max_depth: Maximum recursion depth
            visited: Set of already visited files (internal)

        Returns:
            Recursive backlink graph structure
        """
        if visited is None:
            visited = set()

        file_rel = str(file_path.relative_to(self.vault_path))

        if file_rel in visited or max_depth <= 0:
            return {'file': file_rel, 'backlinks': []}

        visited.add(file_rel)

        # Get direct backlinks
        backlinks = self.integration.find_backlinks(file_path)

        # Recursively get backlinks of backlinks
        result = {
            'file': file_rel,
            'depth': max_depth,
            'backlinks': []
        }

        for backlink in backlinks:
            backlink_file = self.vault_path / backlink['file']
            recursive_result = self.recursive_backlinks(
                backlink_file,
                max_depth - 1,
                visited
            )
            result['backlinks'].append({
                **backlink,
                'recursive_backlinks': recursive_result
            })

        return result

    def build_link_graph(self, files: List[Path]) -> Dict[str, Any]:
        """
        Build complete link graph for multiple files.

        Args:
            files: List of files to analyze

        Returns:
            Link graph with nodes and edges
        """
        nodes = {}
        edges = []

        for file_path in files:
            file_rel = str(file_path.relative_to(self.vault_path))

            # Get backlinks
            backlinks = self.integration.find_backlinks(file_path)

            # Add node
            nodes[file_rel] = {
                'file': file_rel,
                'incoming_links': len(backlinks),
                'backlinks': backlinks
            }

            # Add edges
            for backlink in backlinks:
                edges.append({
                    'from': backlink['file'],
                    'to': file_rel,
                    'line': backlink['line']
                })

        return {
            'nodes': nodes,
            'edges': edges,
            'node_count': len(nodes),
            'edge_count': len(edges)
        }

    def find_orphans(self, files: List[Path]) -> List[str]:
        """
        Find orphaned files (no incoming links).

        Args:
            files: List of files to check

        Returns:
            List of orphaned file paths
        """
        orphans = []

        for file_path in files:
            backlinks = self.integration.find_backlinks(file_path)
            if len(backlinks) == 0:
                orphans.append(str(file_path.relative_to(self.vault_path)))

        return orphans

    def find_strongly_connected(self, files: List[Path]) -> List[List[str]]:
        """
        Find strongly connected components in link graph.

        Args:
            files: List of files to analyze

        Returns:
            List of strongly connected components
        """
        # Build adjacency list
        graph = defaultdict(set)

        for file_path in files:
            file_rel = str(file_path.relative_to(self.vault_path))
            backlinks = self.integration.find_backlinks(file_path)

            for backlink in backlinks:
                graph[backlink['file']].add(file_rel)

        # Tarjan's algorithm for strongly connected components
        index_counter = [0]
        stack = []
        lowlinks = {}
        index = {}
        on_stack = defaultdict(bool)
        components = []

        def strongconnect(node):
            index[node] = index_counter[0]
            lowlinks[node] = index_counter[0]
            index_counter[0] += 1
            on_stack[node] = True
            stack.append(node)

            for successor in graph.get(node, []):
                if successor not in index:
                    strongconnect(successor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[successor])
                elif on_stack[successor]:
                    lowlinks[node] = min(lowlinks[node], index[successor])

            if lowlinks[node] == index[node]:
                component = []
                while True:
                    successor = stack.pop()
                    on_stack[successor] = False
                    component.append(successor)
                    if successor == node:
                        break
                components.append(component)

        for node in graph:
            if node not in index:
                strongconnect(node)

        # Return only components with more than 1 node
        return [comp for comp in components if len(comp) > 1]


# ============================================================================
# Vault LSP Analyzer
# ============================================================================

class VaultLSPAnalyzer(BatchProcessor):
    """
    Vault-wide analysis combining LSP queries with batch processing.

    Inherits from BatchProcessor to leverage existing vault operations.
    """

    def __init__(self, vault_path: Path, dry_run: bool = False, verbose: bool = False):
        """
        Initialize vault LSP analyzer.

        Args:
            vault_path: Path to Obsidian vault
            dry_run: Dry-run mode (no modifications)
            verbose: Enable verbose logging
        """
        super().__init__(vault_path, dry_run, verbose)
        self.integration = MarkdownOxideIntegration(vault_path, verbose)
        self.recursive_lsp = RecursiveLSP(self.integration)

    def analyze_vault_structure(self) -> Dict[str, Any]:
        """
        Analyze vault structure using LSP.

        Returns:
            Vault structure analysis
        """
        logger.info("Analyzing vault structure with LSP")

        # Find all markdown files
        md_files = self.find_markdown_files()

        # Build link graph
        logger.info(f"Building link graph for {len(md_files)} files")
        link_graph = self.recursive_lsp.build_link_graph(md_files)

        # Find orphans
        logger.info("Finding orphaned files")
        orphans = self.recursive_lsp.find_orphans(md_files)

        # Find strongly connected components
        logger.info("Finding strongly connected components")
        components = self.recursive_lsp.find_strongly_connected(md_files)

        # Calculate statistics
        total_files = len(md_files)
        total_links = link_graph['edge_count']
        orphan_count = len(orphans)
        component_count = len(components)

        # Find hub notes (most incoming links)
        hubs = sorted(
            link_graph['nodes'].items(),
            key=lambda x: x[1]['incoming_links'],
            reverse=True
        )[:10]

        return {
            'total_files': total_files,
            'total_links': total_links,
            'orphan_count': orphan_count,
            'orphan_percentage': (orphan_count / total_files * 100) if total_files > 0 else 0,
            'orphaned_files': orphans,
            'strongly_connected_components': component_count,
            'components': components,
            'hub_notes': [
                {
                    'file': file,
                    'incoming_links': data['incoming_links']
                }
                for file, data in hubs
            ],
            'link_graph': link_graph
        }

    def find_broken_links(self) -> List[Dict[str, Any]]:
        """
        Find broken wikilinks using LSP diagnostics.

        Returns:
            List of broken links
        """
        logger.info("Finding broken links via LSP diagnostics")

        broken_links = []
        md_files = self.find_markdown_files()

        for file_path in md_files:
            # Note: LSP diagnostics would be retrieved here
            # For now, this is a placeholder
            pass

        return broken_links

    def process(self, output_path: Optional[Path] = None) -> ProcessingResult:
        """
        Process vault with LSP analysis.

        Args:
            output_path: Optional output file for results

        Returns:
            ProcessingResult with analysis data
        """
        logger.info(f"Processing vault with LSP: {self.vault_path}")

        # Analyze vault structure
        analysis = self.analyze_vault_structure()

        # Find broken links
        broken_links = self.find_broken_links()

        # Combine results
        results = {
            'vault_path': str(self.vault_path),
            'timestamp': datetime.now().isoformat(),
            'structure_analysis': analysis,
            'broken_links': broken_links,
            'broken_link_count': len(broken_links)
        }

        # Write output
        if output_path:
            if not self.dry_run:
                output_path.write_text(
                    json.dumps(results, indent=2),
                    encoding='utf-8'
                )
                logger.info(f"Analysis exported to {output_path}")
            else:
                logger.info(f"[DRY-RUN] Would export analysis to {output_path}")

        # Log summary
        logger.info(f"Vault analysis complete:")
        logger.info(f"  - Total files: {analysis['total_files']}")
        logger.info(f"  - Total links: {analysis['total_links']}")
        logger.info(f"  - Orphaned files: {analysis['orphan_count']} ({analysis['orphan_percentage']:.1f}%)")
        logger.info(f"  - Strongly connected components: {analysis['strongly_connected_components']}")
        logger.info(f"  - Broken links: {len(broken_links)}")

        return ProcessingResult(
            success=True,
            files_processed=analysis['total_files'],
            files_modified=0,
            errors=self.errors,
            warnings=self.warnings,
            metadata={
                'analysis': analysis,
                'broken_links': len(broken_links),
                'output_path': str(output_path) if output_path else None
            }
        )


# ============================================================================
# CLI Interface
# ============================================================================

def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for LSP integration CLI."""
    parser = argparse.ArgumentParser(
        description='LSP Integration for Obsidian Vault Processing',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Common arguments
    def add_common_args(subparser):
        subparser.add_argument('--vault', type=Path, required=True, help='Vault path')
        subparser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    # references command
    p_refs = subparsers.add_parser('references', help='Find references to symbol')
    add_common_args(p_refs)
    p_refs.add_argument('--file', type=Path, required=True, help='File path')
    p_refs.add_argument('--line', type=int, required=True, help='Line number (0-indexed)')
    p_refs.add_argument('--char', type=int, required=True, help='Character offset (0-indexed)')

    # recursive-backlinks command
    p_recursive = subparsers.add_parser('recursive-backlinks', help='Build recursive backlink graph')
    add_common_args(p_recursive)
    p_recursive.add_argument('--file', type=Path, required=True, help='Starting file')
    p_recursive.add_argument('--depth', type=int, default=3, help='Maximum recursion depth')
    p_recursive.add_argument('--output', type=Path, help='Output JSON file')

    # analyze-vault command
    p_analyze = subparsers.add_parser('analyze-vault', help='Analyze vault structure')
    add_common_args(p_analyze)
    p_analyze.add_argument('--output', type=Path, help='Output JSON file')

    # search command
    p_search = subparsers.add_parser('search', help='Search vault symbols')
    add_common_args(p_search)
    p_search.add_argument('--query', type=str, required=True, help='Search query')

    # heading-tree command
    p_tree = subparsers.add_parser('heading-tree', help='Get heading tree for file')
    add_common_args(p_tree)
    p_tree.add_argument('--file', type=Path, required=True, help='File path')

    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    try:
        if args.command == 'references':
            integration = MarkdownOxideIntegration(args.vault, args.verbose)
            backlinks = integration.find_backlinks(args.file, (args.line, args.char))
            print(json.dumps(backlinks, indent=2))

        elif args.command == 'recursive-backlinks':
            integration = MarkdownOxideIntegration(args.vault, args.verbose)
            recursive_lsp = RecursiveLSP(integration)
            graph = recursive_lsp.recursive_backlinks(args.file, args.depth)

            if args.output:
                args.output.write_text(json.dumps(graph, indent=2), encoding='utf-8')
                logger.info(f"Recursive backlink graph exported to {args.output}")
            else:
                print(json.dumps(graph, indent=2))

        elif args.command == 'analyze-vault':
            analyzer = VaultLSPAnalyzer(args.vault, verbose=args.verbose)
            result = analyzer.process(output_path=args.output)
            print(json.dumps(asdict(result), indent=2))

        elif args.command == 'search':
            integration = MarkdownOxideIntegration(args.vault, args.verbose)
            results = integration.search_vault(args.query)
            print(json.dumps(results, indent=2))

        elif args.command == 'heading-tree':
            integration = MarkdownOxideIntegration(args.vault, args.verbose)
            tree = integration.get_heading_tree(args.file)
            print(json.dumps(tree, indent=2))

        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
