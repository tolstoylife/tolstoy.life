#!/usr/bin/env python3
"""
LSP Backlink Analysis Example

Demonstrates comprehensive backlink analysis using LSP integration:
- Recursive backlink graphs
- Hub note identification
- Orphan detection
- Link density analysis
- Strongly connected components

Usage:
    python lsp_backlink_analysis.py --vault ~/Documents/Obsidian --output report.json
"""

import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from lsp_integration import (
    MarkdownOxideIntegration,
    RecursiveLSP,
    VaultLSPAnalyzer
)


def analyze_backlinks(vault_path: Path, output_path: Path = None, max_depth: int = 3):
    """
    Perform comprehensive backlink analysis.

    Args:
        vault_path: Path to Obsidian vault
        output_path: Optional output file for results
        max_depth: Maximum recursion depth for backlink graphs
    """
    print(f"Analyzing backlinks for vault: {vault_path}")

    # Initialize LSP integration
    integration = MarkdownOxideIntegration(vault_path, verbose=True)
    recursive_lsp = RecursiveLSP(integration)
    analyzer = VaultLSPAnalyzer(vault_path, verbose=True)

    # Find all markdown files
    md_files = list(vault_path.glob("**/*.md"))
    print(f"Found {len(md_files)} markdown files")

    # Build complete link graph
    print("\nBuilding link graph...")
    link_graph = recursive_lsp.build_link_graph(md_files)

    # Find hub notes (most incoming links)
    print("\nIdentifying hub notes...")
    hub_notes = sorted(
        link_graph['nodes'].items(),
        key=lambda x: x[1]['incoming_links'],
        reverse=True
    )[:20]

    # Find orphaned notes
    print("\nFinding orphaned notes...")
    orphans = recursive_lsp.find_orphans(md_files)

    # Find strongly connected components
    print("\nFinding strongly connected components (circular references)...")
    components = recursive_lsp.find_strongly_connected(md_files)

    # Calculate link density per directory
    print("\nCalculating link density by directory...")
    dir_stats = defaultdict(lambda: {'files': 0, 'links': 0})

    for file_path in md_files:
        dir_path = file_path.parent.relative_to(vault_path)
        dir_name = str(dir_path) if dir_path != Path('.') else 'root'

        dir_stats[dir_name]['files'] += 1

        file_rel = str(file_path.relative_to(vault_path))
        if file_rel in link_graph['nodes']:
            dir_stats[dir_name]['links'] += link_graph['nodes'][file_rel]['incoming_links']

    # Calculate density
    for dir_name, stats in dir_stats.items():
        if stats['files'] > 0:
            stats['density'] = stats['links'] / stats['files']
        else:
            stats['density'] = 0

    # Build recursive backlink graphs for hub notes
    print("\nBuilding recursive backlink graphs for top 5 hubs...")
    recursive_graphs = []

    for i, (file_rel, node_data) in enumerate(hub_notes[:5]):
        print(f"  [{i+1}/5] Analyzing {file_rel}...")
        file_path = vault_path / file_rel

        graph = recursive_lsp.recursive_backlinks(file_path, max_depth=max_depth)
        recursive_graphs.append({
            'file': file_rel,
            'incoming_links': node_data['incoming_links'],
            'recursive_graph': graph
        })

    # Compile results
    results = {
        'vault_path': str(vault_path),
        'total_files': len(md_files),
        'total_links': link_graph['edge_count'],
        'average_links_per_file': link_graph['edge_count'] / len(md_files) if len(md_files) > 0 else 0,

        'hub_notes': [
            {
                'file': file,
                'incoming_links': data['incoming_links'],
                'backlinks': data['backlinks'][:3]  # First 3 for brevity
            }
            for file, data in hub_notes
        ],

        'orphaned_notes': {
            'count': len(orphans),
            'percentage': (len(orphans) / len(md_files) * 100) if len(md_files) > 0 else 0,
            'files': orphans
        },

        'strongly_connected_components': {
            'count': len(components),
            'components': [
                {
                    'size': len(component),
                    'notes': component
                }
                for component in components
            ]
        },

        'directory_statistics': {
            dir_name: {
                'files': stats['files'],
                'total_incoming_links': stats['links'],
                'link_density': round(stats['density'], 2)
            }
            for dir_name, stats in sorted(
                dir_stats.items(),
                key=lambda x: x[1]['density'],
                reverse=True
            )
        },

        'recursive_backlink_graphs': recursive_graphs,

        'link_graph': link_graph
    }

    # Print summary
    print("\n" + "="*60)
    print("BACKLINK ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total files: {results['total_files']}")
    print(f"Total links: {results['total_links']}")
    print(f"Average links per file: {results['average_links_per_file']:.2f}")
    print(f"\nOrphaned notes: {results['orphaned_notes']['count']} ({results['orphaned_notes']['percentage']:.1f}%)")
    print(f"Strongly connected components: {results['strongly_connected_components']['count']}")

    print("\nTop 10 Hub Notes:")
    for i, hub in enumerate(results['hub_notes'][:10], 1):
        print(f"  {i}. {hub['file']} ({hub['incoming_links']} links)")

    print("\nTop 5 Directories by Link Density:")
    for i, (dir_name, stats) in enumerate(
        sorted(
            results['directory_statistics'].items(),
            key=lambda x: x[1]['link_density'],
            reverse=True
        )[:5],
        1
    ):
        print(f"  {i}. {dir_name}: {stats['link_density']:.2f} links/file ({stats['files']} files)")

    if results['strongly_connected_components']['count'] > 0:
        print("\nStrongly Connected Components (Circular References):")
        for i, component in enumerate(results['strongly_connected_components']['components'], 1):
            print(f"  {i}. Size {component['size']}: {', '.join(component['notes'][:3])}...")

    # Write output
    if output_path:
        output_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
        print(f"\nFull analysis written to: {output_path}")

    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Comprehensive backlink analysis using LSP integration'
    )
    parser.add_argument('--vault', type=Path, required=True,
                        help='Path to Obsidian vault')
    parser.add_argument('--output', type=Path,
                        help='Output JSON file for results')
    parser.add_argument('--depth', type=int, default=3,
                        help='Maximum recursion depth for backlink graphs (default: 3)')

    args = parser.parse_args()

    try:
        results = analyze_backlinks(
            vault_path=args.vault,
            output_path=args.output,
            max_depth=args.depth
        )

        print("\n✓ Analysis complete!")
        return 0

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
