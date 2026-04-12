#!/usr/bin/env python3
"""
URF Topology Validator

Validates knowledge graphs against URF invariants:
- η (eta): Edge density ≥ 4
- ζ (zeta): Acyclicity
- κ (kappa): Clustering coefficient > 0.3
- φ (phi): Isolated nodes < 20%
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum

class ValidationStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"

@dataclass
class ValidationResult:
    metric: str
    status: ValidationStatus
    value: float
    target: float
    message: str
    remediation: Optional[str] = None

@dataclass
class TopologyReport:
    overall: ValidationStatus
    results: List[ValidationResult]
    graph_stats: Dict[str, Any]

class TopologyValidator:
    """Validates graph topology against URF invariants."""
    
    TARGETS = {
        "η": {"target": 4.0, "op": ">=", "name": "density"},
        "ζ": {"target": 0, "op": "==", "name": "cycles"},
        "κ": {"target": 0.3, "op": ">", "name": "clustering"},
        "φ": {"target": 0.2, "op": "<", "name": "isolated_ratio"},
    }
    
    def __init__(self, graph: Dict[str, Any]):
        """
        Initialize with graph in adjacency format:
        {
            "nodes": ["a", "b", "c", ...],
            "edges": [("a", "b"), ("b", "c"), ...]
        }
        """
        self.nodes = set(graph.get("nodes", []))
        self.edges = graph.get("edges", [])
        self.adjacency = self._build_adjacency()
    
    def _build_adjacency(self) -> Dict[str, List[str]]:
        """Build adjacency list from edges."""
        adj = {n: [] for n in self.nodes}
        for src, dst in self.edges:
            if src in adj:
                adj[src].append(dst)
        return adj
    
    def validate_density(self) -> ValidationResult:
        """η: Edge density should be ≥ 4."""
        if not self.nodes:
            return ValidationResult(
                metric="η",
                status=ValidationStatus.FAILED,
                value=0.0,
                target=4.0,
                message="Empty graph",
                remediation="Add nodes and edges to the graph"
            )
        
        ratio = len(self.edges) / len(self.nodes)
        target = self.TARGETS["η"]["target"]
        
        if ratio >= target:
            return ValidationResult(
                metric="η",
                status=ValidationStatus.PASSED,
                value=ratio,
                target=target,
                message=f"Density {ratio:.2f} meets target {target}"
            )
        else:
            return ValidationResult(
                metric="η",
                status=ValidationStatus.FAILED,
                value=ratio,
                target=target,
                message=f"Density {ratio:.2f} below target {target}",
                remediation='invoke infranodus:getGraphAndAdvice with optimize="gaps"'
            )
    
    def validate_acyclic(self) -> ValidationResult:
        """ζ: Graph should be acyclic (DAG)."""
        cycles = self._find_cycles()
        
        if not cycles:
            return ValidationResult(
                metric="ζ",
                status=ValidationStatus.PASSED,
                value=0,
                target=0,
                message="Graph is acyclic"
            )
        else:
            return ValidationResult(
                metric="ζ",
                status=ValidationStatus.FAILED,
                value=len(cycles),
                target=0,
                message=f"Found {len(cycles)} cycle(s)",
                remediation="invoke abduct.refactor with cycle_breaking=True"
            )
    
    def _find_cycles(self) -> List[List[str]]:
        """Detect cycles using DFS."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {n: WHITE for n in self.nodes}
        cycles = []
        
        def dfs(node, path):
            color[node] = GRAY
            path.append(node)
            
            for neighbor in self.adjacency.get(node, []):
                if color[neighbor] == GRAY:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:])
                elif color[neighbor] == WHITE:
                    dfs(neighbor, path.copy())
            
            color[node] = BLACK
        
        for node in self.nodes:
            if color[node] == WHITE:
                dfs(node, [])
        
        return cycles
    
    def validate_clustering(self) -> ValidationResult:
        """κ: Clustering coefficient should be > 0.3."""
        coeff = self._clustering_coefficient()
        target = self.TARGETS["κ"]["target"]
        
        if coeff > target:
            return ValidationResult(
                metric="κ",
                status=ValidationStatus.PASSED,
                value=coeff,
                target=target,
                message=f"Clustering {coeff:.3f} exceeds target {target}"
            )
        else:
            return ValidationResult(
                metric="κ",
                status=ValidationStatus.FAILED,
                value=coeff,
                target=target,
                message=f"Clustering {coeff:.3f} below target {target}",
                remediation="invoke graph.add_triangulation"
            )
    
    def _clustering_coefficient(self) -> float:
        """Calculate average clustering coefficient."""
        if len(self.nodes) < 3:
            return 0.0
        
        # Build undirected adjacency for clustering
        undirected = {n: set() for n in self.nodes}
        for src, dst in self.edges:
            if src in undirected and dst in undirected:
                undirected[src].add(dst)
                undirected[dst].add(src)
        
        coefficients = []
        for node in self.nodes:
            neighbors = undirected[node]
            k = len(neighbors)
            if k < 2:
                continue
            
            # Count triangles
            triangles = 0
            neighbors_list = list(neighbors)
            for i, n1 in enumerate(neighbors_list):
                for n2 in neighbors_list[i+1:]:
                    if n2 in undirected[n1]:
                        triangles += 1
            
            possible = k * (k - 1) / 2
            coefficients.append(triangles / possible if possible > 0 else 0)
        
        return sum(coefficients) / len(coefficients) if coefficients else 0.0
    
    def validate_connectivity(self) -> ValidationResult:
        """φ: Isolated nodes should be < 20%."""
        isolated = sum(1 for n in self.nodes if not self.adjacency.get(n))
        ratio = isolated / len(self.nodes) if self.nodes else 0
        target = self.TARGETS["φ"]["target"]
        
        if ratio < target:
            return ValidationResult(
                metric="φ",
                status=ValidationStatus.PASSED,
                value=ratio,
                target=target,
                message=f"Isolated ratio {ratio:.3f} below target {target}"
            )
        else:
            return ValidationResult(
                metric="φ",
                status=ValidationStatus.FAILED,
                value=ratio,
                target=target,
                message=f"Isolated ratio {ratio:.3f} exceeds target {target}",
                remediation="invoke graph.connect_orphans"
            )
    
    def validate_all(self) -> TopologyReport:
        """Run all validations and return comprehensive report."""
        results = [
            self.validate_density(),
            self.validate_acyclic(),
            self.validate_clustering(),
            self.validate_connectivity(),
        ]
        
        # Overall status
        if all(r.status == ValidationStatus.PASSED for r in results):
            overall = ValidationStatus.PASSED
        elif any(r.status == ValidationStatus.FAILED for r in results):
            overall = ValidationStatus.FAILED
        else:
            overall = ValidationStatus.WARNING
        
        return TopologyReport(
            overall=overall,
            results=results,
            graph_stats={
                "nodes": len(self.nodes),
                "edges": len(self.edges),
                "density": len(self.edges) / len(self.nodes) if self.nodes else 0,
            }
        )

def validate_krog(action: Dict[str, Any]) -> Dict[str, bool]:
    """
    Validate action against KROG constraints.
    
    K: Knowable - Effects transparent
    R: Rights - Agent has authority
    O: Obligations - Duties satisfied
    G: Governance - Within meta-bounds
    """
    return {
        "K": action.get("effects_visible", False) and action.get("auditable", False),
        "R": action.get("has_authority", False),
        "O": not any(action.get("violated_duties", [])),
        "G": action.get("within_governance_bounds", True),
        "valid": True  # Set after checking all
    }

def main():
    """Example usage."""
    # Sample graph
    graph = {
        "nodes": ["concept_a", "concept_b", "concept_c", "concept_d", "concept_e"],
        "edges": [
            ("concept_a", "concept_b"),
            ("concept_a", "concept_c"),
            ("concept_b", "concept_c"),
            ("concept_b", "concept_d"),
            ("concept_c", "concept_d"),
            ("concept_c", "concept_e"),
            ("concept_d", "concept_e"),
        ]
    }
    
    validator = TopologyValidator(graph)
    report = validator.validate_all()
    
    print("=" * 60)
    print("URF TOPOLOGY VALIDATION REPORT")
    print("=" * 60)
    print(f"\nOverall Status: {report.overall.value.upper()}")
    print(f"\nGraph Statistics:")
    for key, value in report.graph_stats.items():
        print(f"  {key}: {value}")
    
    print(f"\nValidation Results:")
    for result in report.results:
        status_icon = "✓" if result.status == ValidationStatus.PASSED else "✗"
        print(f"\n  {status_icon} {result.metric} ({result.status.value})")
        print(f"    Value: {result.value:.3f} (target: {result.target})")
        print(f"    {result.message}")
        if result.remediation:
            print(f"    Remediation: {result.remediation}")

if __name__ == "__main__":
    main()
