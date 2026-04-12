#!/usr/bin/env python3
"""
OntoLog Validator
=================

Validate holonic structures against Lex axioms.

Usage:
    python validate.py structure.ol [--strict]
    python validate.py --text "query text"

Checks:
    - Acyclicity: No cycles in λ-graph
    - Groundedness: All vertices participate in operations
    - Connectivity: Single connected component
    - Density: Sufficient simplex-to-vertex ratio
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Set, List, Dict, Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents import (
    SimplicialComplex, Operation, Base,
    Validator, Axiom, AxiomType,
    validate, Metrics
)
from agents.topologist import compute_metrics, compute_persistence


def parse_ontology_file(filepath: Path) -> tuple:
    """
    Parse .ol ontology file.
    
    Format:
        # Comments
        vertex A
        vertex B
        vertex C
        edge A B
        edge B C
        terminal C
    
    Returns:
        (SimplicialComplex, Set[Operation])
    """
    Σ = SimplicialComplex()
    operations = set()
    terminals = set()
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            cmd = parts[0].lower()
            
            if cmd == 'vertex' and len(parts) >= 2:
                Σ.add_vertex(parts[1])
            
            elif cmd == 'edge' and len(parts) >= 3:
                v1, v2 = parts[1], parts[2]
                Σ.add_vertex(v1)
                Σ.add_vertex(v2)
                Σ.add_simplex((v1, v2))
                
                # Create operation
                conf = float(parts[3]) if len(parts) > 3 else 1.0
                λ = Operation(
                    id=f"λ_{v1}_{v2}",
                    domain={Base(id=v1)},
                    codomain={Base(id=v2)},
                    path=[Base(id=v1), Base(id=v2)],
                    confidence=conf
                )
                operations.add(λ)
            
            elif cmd == 'simplex' and len(parts) >= 2:
                vertices = tuple(parts[1:])
                Σ.add_simplex(vertices)
            
            elif cmd == 'terminal' and len(parts) >= 2:
                terminals.add(parts[1])
    
    return Σ, operations, terminals


def validate_structure(
    Σ: SimplicialComplex,
    operations: Set[Operation],
    strict: bool = False
) -> Dict:
    """
    Validate structure against axioms.
    
    Returns dict with validation results.
    """
    # Select axioms based on strictness
    axioms = [
        Axiom(AxiomType.ACYCLICITY, "No cycles", required=True),
        Axiom(AxiomType.CONNECTIVITY, "Connected", required=True),
        Axiom(AxiomType.GROUNDEDNESS, "Grounded", required=strict),
        Axiom(AxiomType.DENSITY, "Dense", required=strict),
    ]
    
    # Run validation
    result = validate(Σ, operations, axioms)
    
    # Compute metrics
    dgm = compute_persistence(Σ)
    metrics = compute_metrics(Σ, dgm)
    
    return {
        "passed": result.passed,
        "violations": result.violations,
        "metrics": {
            "vertices": metrics.vertex_count,
            "simplices": metrics.simplex_count,
            "dimension": metrics.dimension,
            "euler": metrics.euler_characteristic,
            "density": metrics.density,
            "betti_0": metrics.betti_0,
            "betti_1": metrics.betti_1,
            "max_persistence": metrics.max_persistence,
        },
        "compact": metrics.compact()
    }


def format_result(result: Dict, verbose: bool = False) -> str:
    """Format validation result for output."""
    lines = []
    
    # Status
    status = "✓ VALID" if result["passed"] else "✗ INVALID"
    lines.append(status)
    
    # Compact metrics
    lines.append(result["compact"])
    
    # Violations
    if result["violations"]:
        lines.append("")
        lines.append("Violations:")
        for v in result["violations"]:
            lines.append(f"  - {v}")
    
    # Verbose metrics
    if verbose:
        lines.append("")
        lines.append("Metrics:")
        for k, v in result["metrics"].items():
            lines.append(f"  {k}: {v}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Validate OntoLog structures against Lex axioms"
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        help="Path to .ol ontology file"
    )
    parser.add_argument(
        "--text",
        type=str,
        help="Query text to validate"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict validation (groundedness, density required)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    if args.file:
        # Parse file
        Σ, operations, terminals = parse_ontology_file(args.file)
    elif args.text:
        # Encode from text
        from agents import encode
        query, Σ = encode(args.text)
        from agents import resolve_operations
        operations = resolve_operations(Σ)
    else:
        parser.print_help()
        sys.exit(1)
    
    # Validate
    result = validate_structure(Σ, operations, args.strict)
    
    # Output
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_result(result, args.verbose))
    
    # Exit code
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
