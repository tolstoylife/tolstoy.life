#!/usr/bin/env python3
"""
Validate node ratios between RPP levels.

Targets:
- L1:L2 ratio = 2-3:1 (atomic to composite)
- L1:L3 ratio = 6-9:1 (atomic to detail)
- Pareto coverage: 20%/80%, 4%/64%, 0.8%/51%

Usage:
    python validate_ratios.py --input rpp_graph.json
"""

import json
import argparse


def load_graph(filepath: str) -> dict:
    """Load RPP graph from JSON."""
    with open(filepath, 'r') as f:
        return json.load(f)


def validate_ratios(graph_data: dict) -> dict:
    """
    Validate all node ratios.
    
    Returns dict with validation results.
    """
    counts = {
        'l0': len(graph_data['levels'].get('l0', {}).get('nodes', [])),
        'l1': len(graph_data['levels'].get('l1', {}).get('nodes', [])),
        'l2': len(graph_data['levels'].get('l2', {}).get('nodes', [])),
        'l3': len(graph_data['levels'].get('l3', {}).get('nodes', []))
    }
    
    results = {
        'counts': counts,
        'ratios': {},
        'pareto_percentages': {},
        'violations': [],
        'valid': True
    }
    
    # Skip if L3 is empty
    if counts['l3'] == 0:
        results['violations'].append("L3 is empty - cannot validate")
        results['valid'] = False
        return results
    
    # L2:L1 ratio (target 2-3:1)
    if counts['l1'] > 0:
        ratio = counts['l2'] / counts['l1']
        results['ratios']['l2_l1'] = ratio
        if not (2.0 <= ratio <= 3.0):
            results['violations'].append(f"L2:L1 ratio {ratio:.2f} outside [2, 3]")
    
    # L3:L1 ratio (target 6-9:1)
    if counts['l1'] > 0:
        ratio = counts['l3'] / counts['l1']
        results['ratios']['l3_l1'] = ratio
        if not (6.0 <= ratio <= 9.0):
            results['violations'].append(f"L3:L1 ratio {ratio:.2f} outside [6, 9]")
    
    # L2 as percentage of L3 (target ~20%)
    pct = counts['l2'] / counts['l3']
    results['pareto_percentages']['l2_of_l3'] = pct
    if not (0.15 <= pct <= 0.25):
        results['violations'].append(f"L2 = {pct:.1%} of L3, target 15-25%")
    
    # L1 as percentage of L3 (target ~4%)
    pct = counts['l1'] / counts['l3']
    results['pareto_percentages']['l1_of_l3'] = pct
    if not (0.02 <= pct <= 0.06):
        results['violations'].append(f"L1 = {pct:.1%} of L3, target 2-6%")
    
    # L0 as percentage of L3 (target ~0.8%)
    pct = counts['l0'] / counts['l3']
    results['pareto_percentages']['l0_of_l3'] = pct
    if not (0.005 <= pct <= 0.02):
        results['violations'].append(f"L0 = {pct:.2%} of L3, target 0.5-2%")
    
    # Children per node constraint (2-3)
    for parent_level, child_level in [('l0', 'l1'), ('l1', 'l2'), ('l2', 'l3')]:
        parent_count = counts[parent_level]
        child_count = counts[child_level]
        
        if parent_count > 0:
            avg_children = child_count / parent_count
            results['ratios'][f'{child_level}_per_{parent_level}'] = avg_children
            
            # Allow some flexibility (1.5 to 4)
            if not (1.5 <= avg_children <= 4.0):
                results['violations'].append(
                    f"Avg {avg_children:.1f} children per {parent_level} node, target ~2-3"
                )
    
    results['valid'] = len(results['violations']) == 0
    
    return results


def print_report(results: dict):
    """Print validation report."""
    print("\nNode Ratio Validation Report")
    print("=" * 50)
    
    # Counts
    print("\nNode Counts:")
    for level, count in results['counts'].items():
        print(f"  {level.upper()}: {count}")
    
    # Ratios
    print("\nLevel Ratios:")
    for ratio_name, value in results['ratios'].items():
        print(f"  {ratio_name}: {value:.2f}")
    
    # Pareto percentages
    print("\nPareto Percentages:")
    for pct_name, value in results['pareto_percentages'].items():
        print(f"  {pct_name}: {value:.2%}")
    
    # Violations
    print("\nViolations:")
    if results['violations']:
        for v in results['violations']:
            print(f"  ✗ {v}")
    else:
        print("  ✓ No violations")
    
    print("\n" + "=" * 50)
    status = "PASS" if results['valid'] else "FAIL"
    print(f"Overall: {status}")


def main():
    parser = argparse.ArgumentParser(description="Validate RPP node ratios")
    parser.add_argument("--input", required=True, help="Input RPP graph JSON")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    graph_data = load_graph(args.input)
    results = validate_ratios(graph_data)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_report(results)


if __name__ == "__main__":
    main()
