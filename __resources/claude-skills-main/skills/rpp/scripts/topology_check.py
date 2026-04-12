#!/usr/bin/env python3
"""
Topology validation for RPP graphs.

Validates:
- Edge density (η ≥ 4.0)
- Clustering coefficient (κ > 0.3)
- Isolation ratio (φ < 0.2)
- Small-world coefficient (σ > 1.0)
- Node ratios between levels

Usage:
    python topology_check.py --input rpp_graph.json
"""

import json
import math
import argparse
from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResult:
    """Result of a single validation check."""
    metric: str
    value: float
    target: tuple
    valid: bool
    message: str


@dataclass 
class TopologyReport:
    """Complete topology validation report."""
    results: list
    overall_valid: bool
    
    def add(self, result: ValidationResult):
        self.results.append(result)
    
    def print_report(self):
        print("\nTopology Validation Report")
        print("=" * 50)
        
        for r in self.results:
            status = "✓" if r.valid else "✗"
            print(f"{status} {r.metric}: {r.value:.3f} (target: {r.target})")
            if not r.valid:
                print(f"    {r.message}")
        
        print("=" * 50)
        status = "PASS" if self.overall_valid else "FAIL"
        print(f"Overall: {status}")


def load_rpp_graph(filepath: str) -> dict:
    """Load RPP graph from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def compute_eta(graph_data: dict) -> float:
    """
    Compute edge density (η).
    
    η = |E| / |V|
    Target: η ≥ 4.0
    """
    total_nodes = 0
    total_edges = 0
    
    for level_name in ['l0', 'l1', 'l2', 'l3']:
        level = graph_data['levels'].get(level_name, {})
        total_nodes += len(level.get('nodes', []))
        total_edges += len(level.get('edges', []))
    
    if total_nodes == 0:
        return 0.0
    
    return total_edges / total_nodes


def compute_clustering(graph_data: dict) -> float:
    """
    Compute average clustering coefficient (κ).
    
    Target: κ > 0.3
    """
    # Build adjacency for unified graph
    adjacency = {}
    all_nodes = set()
    
    for level_name in ['l0', 'l1', 'l2', 'l3']:
        level = graph_data['levels'].get(level_name, {})
        
        for node in level.get('nodes', []):
            node_id = node['id']
            all_nodes.add(node_id)
            if node_id not in adjacency:
                adjacency[node_id] = set()
        
        for edge in level.get('edges', []):
            src, tgt = edge['source'], edge['target']
            if src not in adjacency:
                adjacency[src] = set()
            if tgt not in adjacency:
                adjacency[tgt] = set()
            adjacency[src].add(tgt)
            adjacency[tgt].add(src)
    
    if not all_nodes:
        return 0.0
    
    # Compute local clustering for each node
    coefficients = []
    
    for node in all_nodes:
        neighbors = list(adjacency.get(node, set()))
        k = len(neighbors)
        
        if k < 2:
            coefficients.append(0.0)
            continue
        
        # Count edges between neighbors
        actual_edges = 0
        for i, n1 in enumerate(neighbors):
            for n2 in neighbors[i+1:]:
                if n2 in adjacency.get(n1, set()):
                    actual_edges += 1
        
        possible_edges = k * (k - 1) / 2
        coefficients.append(actual_edges / possible_edges if possible_edges > 0 else 0.0)
    
    return sum(coefficients) / len(coefficients) if coefficients else 0.0


def compute_isolation(graph_data: dict) -> float:
    """
    Compute isolation ratio (φ).
    
    φ = orphan_nodes / total_nodes
    Target: φ < 0.2
    """
    # Build degree map
    degrees = {}
    
    for level_name in ['l0', 'l1', 'l2', 'l3']:
        level = graph_data['levels'].get(level_name, {})
        
        for node in level.get('nodes', []):
            node_id = node['id']
            degrees[node_id] = 0
        
        for edge in level.get('edges', []):
            degrees[edge['source']] = degrees.get(edge['source'], 0) + 1
            degrees[edge['target']] = degrees.get(edge['target'], 0) + 1
    
    if not degrees:
        return 1.0
    
    isolated = sum(1 for d in degrees.values() if d == 0)
    return isolated / len(degrees)


def compute_small_world(graph_data: dict, eta: float, clustering: float) -> float:
    """
    Compute small-world coefficient (σ).
    
    σ = (C/C_random) / (L/L_random)
    
    For sparse graphs, approximated as σ ≈ C * n / k
    Target: σ > 1.0
    """
    total_nodes = sum(
        len(graph_data['levels'].get(l, {}).get('nodes', []))
        for l in ['l0', 'l1', 'l2', 'l3']
    )
    
    if total_nodes < 2 or eta == 0:
        return 0.0
    
    # Approximate: σ ≈ C / (k/n) where k is average degree
    # k ≈ 2 * η (since each edge contributes to 2 degrees)
    k = 2 * eta
    c_random = k / total_nodes
    
    if c_random == 0:
        return 0.0
    
    return clustering / c_random


def validate_node_ratios(graph_data: dict) -> list:
    """
    Validate node ratios between levels.
    
    Targets:
    - L1:L2 = 2-3:1
    - L1:L3 = 6-9:1
    """
    results = []
    
    counts = {
        'l0': len(graph_data['levels'].get('l0', {}).get('nodes', [])),
        'l1': len(graph_data['levels'].get('l1', {}).get('nodes', [])),
        'l2': len(graph_data['levels'].get('l2', {}).get('nodes', [])),
        'l3': len(graph_data['levels'].get('l3', {}).get('nodes', []))
    }
    
    # L2:L1 ratio (should be 2-3)
    if counts['l1'] > 0:
        ratio_l2_l1 = counts['l2'] / counts['l1']
        results.append(ValidationResult(
            metric='L2:L1 ratio',
            value=ratio_l2_l1,
            target=(2.0, 3.0),
            valid=2.0 <= ratio_l2_l1 <= 3.0,
            message=f"L2:L1 = {ratio_l2_l1:.2f}, target 2-3:1"
        ))
    
    # L3:L1 ratio (should be 6-9)
    if counts['l1'] > 0:
        ratio_l3_l1 = counts['l3'] / counts['l1']
        results.append(ValidationResult(
            metric='L3:L1 ratio',
            value=ratio_l3_l1,
            target=(6.0, 9.0),
            valid=6.0 <= ratio_l3_l1 <= 9.0,
            message=f"L3:L1 = {ratio_l3_l1:.2f}, target 6-9:1"
        ))
    
    return results


def validate_pareto_coverage(graph_data: dict) -> list:
    """
    Validate Pareto coverage at each level.
    
    Targets:
    - L2: 20% nodes → 80% coverage of L3
    - L1: 4% of L3 → 64% coverage
    - L0: 0.8% of L3 → 51% coverage
    """
    results = []
    
    counts = {
        'l0': len(graph_data['levels'].get('l0', {}).get('nodes', [])),
        'l1': len(graph_data['levels'].get('l1', {}).get('nodes', [])),
        'l2': len(graph_data['levels'].get('l2', {}).get('nodes', [])),
        'l3': len(graph_data['levels'].get('l3', {}).get('nodes', []))
    }
    
    if counts['l3'] > 0:
        # L2 percentage of L3
        l2_pct = counts['l2'] / counts['l3']
        results.append(ValidationResult(
            metric='L2 as % of L3',
            value=l2_pct,
            target=(0.15, 0.25),
            valid=0.15 <= l2_pct <= 0.25,
            message=f"L2 = {l2_pct:.1%} of L3, target ~20%"
        ))
        
        # L1 percentage of L3
        l1_pct = counts['l1'] / counts['l3']
        results.append(ValidationResult(
            metric='L1 as % of L3',
            value=l1_pct,
            target=(0.02, 0.06),
            valid=0.02 <= l1_pct <= 0.06,
            message=f"L1 = {l1_pct:.1%} of L3, target ~4%"
        ))
        
        # L0 percentage of L3
        l0_pct = counts['l0'] / counts['l3']
        results.append(ValidationResult(
            metric='L0 as % of L3',
            value=l0_pct,
            target=(0.005, 0.02),
            valid=0.005 <= l0_pct <= 0.02,
            message=f"L0 = {l0_pct:.2%} of L3, target ~0.8%"
        ))
    
    return results


def validate_topology(graph_data: dict) -> TopologyReport:
    """
    Run complete topology validation.
    """
    report = TopologyReport(results=[], overall_valid=True)
    
    # Core metrics
    eta = compute_eta(graph_data)
    report.add(ValidationResult(
        metric='η (edge density)',
        value=eta,
        target=(4.0, float('inf')),
        valid=eta >= 4.0,
        message=f"η = {eta:.2f}, target ≥ 4.0"
    ))
    
    clustering = compute_clustering(graph_data)
    report.add(ValidationResult(
        metric='κ (clustering)',
        value=clustering,
        target=(0.3, 1.0),
        valid=clustering > 0.3,
        message=f"κ = {clustering:.2f}, target > 0.3"
    ))
    
    isolation = compute_isolation(graph_data)
    report.add(ValidationResult(
        metric='φ (isolation)',
        value=isolation,
        target=(0.0, 0.2),
        valid=isolation < 0.2,
        message=f"φ = {isolation:.2f}, target < 0.2"
    ))
    
    sigma = compute_small_world(graph_data, eta, clustering)
    report.add(ValidationResult(
        metric='σ (small-world)',
        value=sigma,
        target=(1.0, float('inf')),
        valid=sigma > 1.0,
        message=f"σ = {sigma:.2f}, target > 1.0"
    ))
    
    # Node ratios
    for result in validate_node_ratios(graph_data):
        report.add(result)
    
    # Pareto coverage
    for result in validate_pareto_coverage(graph_data):
        report.add(result)
    
    # Compute overall validity
    report.overall_valid = all(r.valid for r in report.results)
    
    return report


def main():
    parser = argparse.ArgumentParser(description="Validate RPP graph topology")
    parser.add_argument("--input", required=True, help="Input RPP graph JSON file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Load graph
    graph_data = load_rpp_graph(args.input)
    
    # Validate
    report = validate_topology(graph_data)
    
    if args.json:
        output = {
            "valid": report.overall_valid,
            "results": [
                {
                    "metric": r.metric,
                    "value": r.value,
                    "target": r.target,
                    "valid": r.valid,
                    "message": r.message
                }
                for r in report.results
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        report.print_report()


if __name__ == "__main__":
    main()
