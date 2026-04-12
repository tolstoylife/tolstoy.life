#!/usr/bin/env python3
"""
Compression Verification Tool

Verifies that compressed graphs preserve specified query types by comparing
query results between original and compressed graphs.

The Universal Property Guarantee:
For any quotient Q: C → C/R, if H: C → D is any functor respecting the
equivalence R, then H factors uniquely as H = H' ∘ Q. This means all
structure-preserving queries on the original can be answered on the quotient.

Supported query types:
- reachability: Can node A reach node B?
- pattern: Does subgraph pattern P exist?
- neighborhood: What nodes are within k hops?

Usage:
    python verify_compression.py original.json compressed.json --queries reachability,pattern
"""

import json
import argparse
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple, Any, Optional


def load_graph(filepath: str) -> Tuple[Dict[str, Any], List[Any], Dict[str, int]]:
    """Load graph and return (nodes_dict, edges_list, partition_map)."""
    with open(filepath) as f:
        data = json.load(f)
    
    graph = data.get('graph', data)
    nodes = {n['id']: n for n in graph.get('nodes', [])}
    edges = graph.get('edges', [])
    
    # Extract partition from compression metadata if available
    partition = {}
    if 'compression_metadata' in data:
        partition = data['compression_metadata'].get('partition', {})
    
    # Or reconstruct from node members
    if not partition:
        for node_id, node in nodes.items():
            members = node.get('properties', {}).get('members', [node_id])
            if isinstance(members, list):
                for member in members:
                    partition[member] = node_id
            else:
                partition[node_id] = node_id
    
    return nodes, edges, partition


def build_adjacency(nodes: Dict[str, Any], edges: List[Any]) -> Dict[str, Set[str]]:
    """Build adjacency list."""
    adj = defaultdict(set)
    node_ids = set(nodes.keys())
    
    for edge in edges:
        source = edge['source']
        target = edge['target']
        if source in node_ids and target in node_ids:
            adj[source].add(target)
    
    return adj


def verify_reachability(original_nodes: Dict, original_edges: List,
                        compressed_nodes: Dict, compressed_edges: List,
                        partition: Dict[str, str],
                        sample_size: int = 50) -> Dict[str, Any]:
    """
    Verify reachability query preservation.
    
    For k-bisimulation: If A can reach B in original, then
    representative(A) can reach representative(B) in compressed.
    """
    import random
    random.seed(42)
    
    orig_adj = build_adjacency(original_nodes, original_edges)
    comp_adj = build_adjacency(compressed_nodes, compressed_edges)
    
    # Sample node pairs
    node_list = list(original_nodes.keys())
    if len(node_list) < 2:
        return {'preserved': True, 'tested_pairs': 0, 'details': 'Too few nodes'}
    
    pairs = []
    for _ in range(sample_size):
        a, b = random.sample(node_list, 2)
        pairs.append((a, b))
    
    # BFS reachability check
    def can_reach(adj: Dict[str, Set[str]], source: str, target: str) -> bool:
        if source == target:
            return True
        visited = {source}
        queue = deque([source])
        while queue:
            current = queue.popleft()
            for neighbor in adj[current]:
                if neighbor == target:
                    return True
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return False
    
    preserved = 0
    violated = 0
    violations = []
    
    for a, b in pairs:
        orig_reachable = can_reach(orig_adj, a, b)
        
        # Map to compressed representatives
        a_rep = partition.get(a, a)
        b_rep = partition.get(b, b)
        
        # If both map to same representative, trivially reachable
        if a_rep == b_rep:
            comp_reachable = True
        elif a_rep in compressed_nodes and b_rep in compressed_nodes:
            comp_reachable = can_reach(comp_adj, a_rep, b_rep)
        else:
            comp_reachable = False
        
        # Reachability should be preserved (if original reachable, compressed should be too)
        if orig_reachable and not comp_reachable:
            violated += 1
            violations.append({'source': a, 'target': b, 
                             'original': orig_reachable, 'compressed': comp_reachable})
        else:
            preserved += 1
    
    return {
        'query_type': 'reachability',
        'preserved': violated == 0,
        'preservation_rate': preserved / len(pairs) if pairs else 1.0,
        'tested_pairs': len(pairs),
        'violations': violations[:5] if violations else []
    }


def verify_neighborhood(original_nodes: Dict, original_edges: List,
                        compressed_nodes: Dict, compressed_edges: List,
                        partition: Dict[str, str],
                        k: int = 3,
                        sample_size: int = 20) -> Dict[str, Any]:
    """
    Verify k-hop neighborhood preservation.
    
    For k-bisimulation with depth >= k: neighborhood types should be preserved.
    """
    import random
    random.seed(42)
    
    orig_adj = build_adjacency(original_nodes, original_edges)
    comp_adj = build_adjacency(compressed_nodes, compressed_edges)
    
    def get_k_neighborhood(adj: Dict[str, Set[str]], start: str, k: int) -> Set[str]:
        """Get all nodes within k hops."""
        visited = {start}
        frontier = {start}
        for _ in range(k):
            new_frontier = set()
            for node in frontier:
                for neighbor in adj[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        new_frontier.add(neighbor)
            frontier = new_frontier
        return visited
    
    node_list = list(original_nodes.keys())
    sample = random.sample(node_list, min(sample_size, len(node_list)))
    
    preserved = 0
    size_preserved = 0
    
    for node in sample:
        orig_neighborhood = get_k_neighborhood(orig_adj, node, k)
        
        node_rep = partition.get(node, node)
        if node_rep in compressed_nodes:
            comp_neighborhood = get_k_neighborhood(comp_adj, node_rep, k)
            
            # Map original neighborhood to compressed
            orig_mapped = {partition.get(n, n) for n in orig_neighborhood}
            
            # Check if compressed neighborhood contains mapped original
            if orig_mapped <= comp_neighborhood:
                preserved += 1
            
            # Check size relationship (compressed should be <=)
            if len(comp_neighborhood) <= len(orig_mapped):
                size_preserved += 1
    
    return {
        'query_type': f'{k}-hop neighborhood',
        'preserved': preserved == len(sample),
        'preservation_rate': preserved / len(sample) if sample else 1.0,
        'size_preservation_rate': size_preserved / len(sample) if sample else 1.0,
        'tested_nodes': len(sample),
        'k': k
    }


def verify_pattern_matching(original_nodes: Dict, original_edges: List,
                            compressed_nodes: Dict, compressed_edges: List,
                            partition: Dict[str, str]) -> Dict[str, Any]:
    """
    Verify simple pattern preservation (edge types between node types).
    
    For k-bisimulation: patterns up to size k should be preserved.
    """
    # Collect edge type patterns
    def get_patterns(nodes: Dict, edges: List) -> Set[Tuple[str, str, str]]:
        patterns = set()
        for edge in edges:
            source_type = nodes.get(edge['source'], {}).get('type', 'unknown')
            target_type = nodes.get(edge['target'], {}).get('type', 'unknown')
            edge_type = edge.get('type', 'related')
            patterns.add((source_type, edge_type, target_type))
        return patterns
    
    orig_patterns = get_patterns(original_nodes, original_edges)
    comp_patterns = get_patterns(compressed_nodes, compressed_edges)
    
    # Original patterns should be subset of compressed (modulo type preservation)
    preserved = orig_patterns <= comp_patterns
    
    missing = orig_patterns - comp_patterns
    extra = comp_patterns - orig_patterns
    
    return {
        'query_type': 'pattern_matching',
        'preserved': len(missing) == 0,
        'original_patterns': len(orig_patterns),
        'compressed_patterns': len(comp_patterns),
        'missing_patterns': list(missing)[:5],
        'note': 'Patterns are (source_type, edge_type, target_type) triples'
    }


def main():
    parser = argparse.ArgumentParser(
        description='Verify compression preserves query semantics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Verification based on Universal Property of Categorical Quotients:
  Any functor H respecting the equivalence R factors uniquely through
  the quotient Q: C → C/R. This guarantees structure-preserving queries
  remain answerable on compressed graphs.

Examples:
  python verify_compression.py original.json compressed.json
  python verify_compression.py original.json compressed.json --queries reachability,neighborhood
        """
    )
    
    parser.add_argument('original', help='Original graph JSON')
    parser.add_argument('compressed', help='Compressed graph JSON')
    parser.add_argument('--queries', default='reachability,pattern,neighborhood',
                       help='Query types to verify (comma-separated)')
    parser.add_argument('--k', type=int, default=3, help='Neighborhood depth for neighborhood queries')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Load graphs
    orig_nodes, orig_edges, _ = load_graph(args.original)
    comp_nodes, comp_edges, partition = load_graph(args.compressed)
    
    # If partition not in compressed, try to reconstruct
    if not partition:
        # Assume identity partition for comparison
        partition = {n: n for n in orig_nodes}
    
    results = {
        'original_nodes': len(orig_nodes),
        'original_edges': len(orig_edges),
        'compressed_nodes': len(comp_nodes),
        'compressed_edges': len(comp_edges),
        'compression_ratio': round(1 - len(comp_nodes)/len(orig_nodes), 4) if orig_nodes else 0,
        'verifications': []
    }
    
    query_types = [q.strip() for q in args.queries.split(',')]
    
    for query in query_types:
        if query == 'reachability':
            result = verify_reachability(orig_nodes, orig_edges, comp_nodes, comp_edges, partition)
        elif query == 'pattern':
            result = verify_pattern_matching(orig_nodes, orig_edges, comp_nodes, comp_edges, partition)
        elif query == 'neighborhood':
            result = verify_neighborhood(orig_nodes, orig_edges, comp_nodes, comp_edges, partition, k=args.k)
        else:
            result = {'query_type': query, 'error': 'Unknown query type'}
        
        results['verifications'].append(result)
    
    # Overall verdict
    all_preserved = all(v.get('preserved', False) for v in results['verifications'])
    results['overall_preserved'] = all_preserved
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("\n" + "=" * 60)
        print("COMPRESSION VERIFICATION REPORT")
        print("=" * 60)
        print(f"\nGraph sizes:")
        print(f"  Original:   {results['original_nodes']} nodes, {results['original_edges']} edges")
        print(f"  Compressed: {results['compressed_nodes']} nodes, {results['compressed_edges']} edges")
        print(f"  Compression ratio: {results['compression_ratio']*100:.1f}%")
        
        print(f"\nQuery Verification Results:")
        for v in results['verifications']:
            status = '✓ PRESERVED' if v.get('preserved', False) else '✗ VIOLATED'
            print(f"\n  {v['query_type']}: {status}")
            if 'preservation_rate' in v:
                print(f"    Preservation rate: {v['preservation_rate']*100:.1f}%")
            if v.get('violations'):
                print(f"    Sample violations: {v['violations'][:2]}")
            if v.get('missing_patterns'):
                print(f"    Missing patterns: {v['missing_patterns'][:3]}")
        
        print(f"\n{'='*60}")
        overall = '✓ ALL QUERIES PRESERVED' if all_preserved else '✗ SOME QUERIES VIOLATED'
        print(f"OVERALL: {overall}")
        print("=" * 60)


if __name__ == '__main__':
    main()
