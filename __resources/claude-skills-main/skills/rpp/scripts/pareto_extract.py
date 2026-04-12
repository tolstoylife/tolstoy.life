#!/usr/bin/env python3
"""
Pareto extraction algorithm for RPP level construction.

Implements the core Pareto principle: extract nodes that provide
maximum coverage with minimum count (80% coverage from 20% nodes).

Usage:
    python pareto_extract.py --input graph.json --target-coverage 0.8 --max-ratio 0.2
"""

import json
import argparse
from dataclasses import dataclass
from typing import Optional


@dataclass
class ExtractionResult:
    """Result of Pareto extraction."""
    selected_nodes: list
    coverage: float
    node_ratio: float
    valid: bool
    message: str


def compute_importance(nodes: list, edges: list) -> dict:
    """
    Compute node importance scores.
    
    Combines:
    - Degree centrality
    - Semantic weight
    - Information density
    """
    # Build adjacency
    adjacency = {n['id']: [] for n in nodes}
    for e in edges:
        if e['source'] in adjacency:
            adjacency[e['source']].append(e['target'])
        if e['target'] in adjacency:
            adjacency[e['target']].append(e['source'])
    
    scores = {}
    for node in nodes:
        node_id = node['id']
        
        # Degree centrality
        degree = len(adjacency.get(node_id, []))
        max_degree = len(nodes) - 1
        degree_centrality = degree / max_degree if max_degree > 0 else 0
        
        # Semantic weight (from node data or default)
        semantic_weight = node.get('semantic_weight', 1.0 / len(nodes))
        
        # Combined score
        scores[node_id] = 0.5 * degree_centrality + 0.5 * semantic_weight
    
    return scores


def marginal_coverage(
    node: dict,
    already_covered: set,
    all_nodes: list
) -> float:
    """
    Compute marginal coverage contribution of adding a node.
    
    Uses submodular function to prevent redundancy.
    """
    # Nodes this node would cover
    would_cover = {node['id']}
    
    # Add grounded nodes if present
    if 'grounded_nodes' in node:
        would_cover.update(node['grounded_nodes'])
    
    # Marginal = new coverage not already covered
    new_coverage = would_cover - already_covered
    
    return len(new_coverage) / len(all_nodes) if all_nodes else 0.0


def pareto_extract(
    nodes: list,
    edges: list,
    target_coverage: float = 0.8,
    max_ratio: float = 0.2
) -> ExtractionResult:
    """
    Extract Pareto-optimal subset of nodes.
    
    Args:
        nodes: List of node dicts with 'id' and optionally 'semantic_weight'
        edges: List of edge dicts with 'source' and 'target'
        target_coverage: Target coverage threshold (default 0.8)
        max_ratio: Maximum ratio of nodes to select (default 0.2)
    
    Returns:
        ExtractionResult with selected nodes and metrics
    """
    if not nodes:
        return ExtractionResult(
            selected_nodes=[],
            coverage=0.0,
            node_ratio=0.0,
            valid=False,
            message="No nodes to extract from"
        )
    
    # Compute importance scores
    importance = compute_importance(nodes, edges)
    
    # Sort by importance
    sorted_nodes = sorted(
        nodes,
        key=lambda n: importance.get(n['id'], 0),
        reverse=True
    )
    
    # Greedy selection
    selected = []
    covered = set()
    cumulative_coverage = 0.0
    max_nodes = max(1, int(len(nodes) * max_ratio))
    
    for node in sorted_nodes:
        if len(selected) >= max_nodes:
            break
        
        # Compute marginal contribution
        contribution = marginal_coverage(node, covered, nodes)
        
        if contribution > 0:
            selected.append(node)
            covered.add(node['id'])
            if 'grounded_nodes' in node:
                covered.update(node['grounded_nodes'])
            cumulative_coverage += contribution
        
        if cumulative_coverage >= target_coverage:
            break
    
    # Compute final metrics
    node_ratio = len(selected) / len(nodes)
    
    return ExtractionResult(
        selected_nodes=selected,
        coverage=cumulative_coverage,
        node_ratio=node_ratio,
        valid=(cumulative_coverage >= target_coverage * 0.9 and node_ratio <= max_ratio * 1.1),
        message=f"Selected {len(selected)} nodes ({node_ratio:.1%}) with {cumulative_coverage:.1%} coverage"
    )


def diverse_pareto_extract(
    nodes: list,
    edges: list,
    target_coverage: float = 0.8,
    max_ratio: float = 0.2,
    diversity_weight: float = 0.3
) -> ExtractionResult:
    """
    Pareto extraction with diversity constraint.
    
    Penalizes selecting nodes too similar to already-selected.
    """
    if not nodes:
        return ExtractionResult(
            selected_nodes=[],
            coverage=0.0,
            node_ratio=0.0,
            valid=False,
            message="No nodes to extract from"
        )
    
    # Compute importance
    importance = compute_importance(nodes, edges)
    
    # Build node content map for similarity
    content_map = {n['id']: n.get('content', '') for n in nodes}
    
    def similarity(n1_id: str, n2_id: str) -> float:
        """Simple word overlap similarity."""
        words1 = set(content_map.get(n1_id, '').lower().split())
        words2 = set(content_map.get(n2_id, '').lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        return len(words1 & words2) / len(words1 | words2)
    
    selected = []
    covered = set()
    cumulative_coverage = 0.0
    max_nodes = max(1, int(len(nodes) * max_ratio))
    
    for _ in range(max_nodes):
        best_node = None
        best_score = -1
        
        for node in nodes:
            if node['id'] in covered:
                continue
            
            # Importance score
            imp = importance.get(node['id'], 0)
            
            # Diversity score (minimum distance to selected)
            if selected:
                div = min(
                    1 - similarity(node['id'], s['id'])
                    for s in selected
                )
            else:
                div = 1.0
            
            # Combined score
            score = (1 - diversity_weight) * imp + diversity_weight * div
            
            if score > best_score:
                best_score = score
                best_node = node
        
        if best_node is None:
            break
        
        selected.append(best_node)
        covered.add(best_node['id'])
        if 'grounded_nodes' in best_node:
            covered.update(best_node['grounded_nodes'])
        
        cumulative_coverage = len(covered) / len(nodes)
        
        if cumulative_coverage >= target_coverage:
            break
    
    node_ratio = len(selected) / len(nodes)
    
    return ExtractionResult(
        selected_nodes=selected,
        coverage=cumulative_coverage,
        node_ratio=node_ratio,
        valid=(cumulative_coverage >= target_coverage * 0.9 and node_ratio <= max_ratio * 1.1),
        message=f"Selected {len(selected)} diverse nodes ({node_ratio:.1%}) with {cumulative_coverage:.1%} coverage"
    )


def chain_pareto(
    source_nodes: list,
    source_edges: list,
    levels: int = 3
) -> list:
    """
    Apply chained Pareto extraction to create multiple levels.
    
    L3 → L2 (20%/80%) → L1 (4%/64%) → L0 (0.8%/51%)
    """
    results = []
    current_nodes = source_nodes
    current_edges = source_edges
    
    for level in range(levels):
        result = pareto_extract(
            current_nodes,
            current_edges,
            target_coverage=0.8,
            max_ratio=0.2
        )
        
        results.append({
            'level': levels - level,  # L3, L2, L1, L0
            'nodes': result.selected_nodes,
            'coverage': result.coverage,
            'ratio': result.node_ratio
        })
        
        # Next iteration uses selected as input
        current_nodes = result.selected_nodes
        # Rebuild edges for selected nodes
        selected_ids = {n['id'] for n in current_nodes}
        current_edges = [
            e for e in current_edges
            if e['source'] in selected_ids and e['target'] in selected_ids
        ]
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Pareto extraction for RPP")
    parser.add_argument("--input", required=True, help="Input graph JSON (single level)")
    parser.add_argument("--target-coverage", type=float, default=0.8, help="Target coverage")
    parser.add_argument("--max-ratio", type=float, default=0.2, help="Max node ratio")
    parser.add_argument("--diverse", action="store_true", help="Use diverse extraction")
    parser.add_argument("--diversity-weight", type=float, default=0.3, help="Diversity weight")
    parser.add_argument("--output", help="Output JSON file")
    
    args = parser.parse_args()
    
    # Load input
    with open(args.input, 'r') as f:
        data = json.load(f)
    
    # Handle different input formats
    if 'nodes' in data:
        nodes = data['nodes']
        edges = data.get('edges', [])
    elif 'levels' in data:
        # Use L3 as source
        nodes = data['levels']['l3'].get('nodes', [])
        edges = data['levels']['l3'].get('edges', [])
    else:
        print("Error: Input must have 'nodes' or 'levels' key")
        return
    
    # Extract
    if args.diverse:
        result = diverse_pareto_extract(
            nodes, edges,
            target_coverage=args.target_coverage,
            max_ratio=args.max_ratio,
            diversity_weight=args.diversity_weight
        )
    else:
        result = pareto_extract(
            nodes, edges,
            target_coverage=args.target_coverage,
            max_ratio=args.max_ratio
        )
    
    # Output
    output = {
        'selected_count': len(result.selected_nodes),
        'total_count': len(nodes),
        'node_ratio': result.node_ratio,
        'coverage': result.coverage,
        'valid': result.valid,
        'message': result.message,
        'selected_nodes': [n['id'] for n in result.selected_nodes]
    }
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"Output saved to {args.output}")
    else:
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
