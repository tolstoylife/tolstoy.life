"""
Validator Agent
===============

(Σ, Set[λ], Set[τ]) → ValidationResult

Validates structure against Lex axioms.
Ensures topological and logical consistency.
"""

from __future__ import annotations
from typing import Set, List, Dict, Optional, Callable
import dspy
from dataclasses import dataclass
from enum import Enum

from .types import (
    Base, Terminal, Operation, SimplicialComplex, Metrics,
    ValidatorSignature, ValidationResult, AgentState, AgentResult
)


# =============================================================================
# AXIOM TYPES
# =============================================================================

class AxiomType(Enum):
    ACYCLICITY = "acyclicity"
    GROUNDEDNESS = "groundedness"
    CONNECTIVITY = "connectivity"
    DENSITY = "density"
    TRANSITIVITY = "transitivity"


@dataclass
class Axiom:
    """An axiom to validate."""
    type: AxiomType
    name: str
    required: bool = True


# =============================================================================
# AXIOM CHECKS
# =============================================================================

def check_acyclicity(operations: Set[Operation]) -> List[str]:
    """
    Check for cycles in operation graph.
    
    Axiom: ¬∃path. λ*(a, a)
    """
    violations = []
    
    # Build adjacency
    adj: Dict[str, Set[str]] = {}
    for λ in operations:
        for b in λ.domain:
            if b.id not in adj:
                adj[b.id] = set()
            for x in λ.codomain:
                adj[b.id].add(x.id)
    
    # DFS for cycle detection
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in adj}
    
    def dfs(v: str, path: List[str]) -> Optional[List[str]]:
        color[v] = GRAY
        path.append(v)
        
        for neighbor in adj.get(v, []):
            if neighbor not in color:
                color[neighbor] = WHITE
            if color[neighbor] == GRAY:
                # Found cycle
                cycle_start = path.index(neighbor)
                return path[cycle_start:] + [neighbor]
            if color[neighbor] == WHITE:
                result = dfs(neighbor, path)
                if result:
                    return result
        
        path.pop()
        color[v] = BLACK
        return None
    
    for v in adj:
        if color[v] == WHITE:
            cycle = dfs(v, [])
            if cycle:
                violations.append(f"Cycle detected: {' → '.join(cycle)}")
    
    return violations


def check_groundedness(
    Σ: SimplicialComplex,
    operations: Set[Operation]
) -> List[str]:
    """
    Check that all vertices participate in operations.
    
    Axiom: ∀ο. ∃λ. domain(λ) = ο ∨ codomain(λ) = ο
    """
    violations = []
    
    participating = set()
    for λ in operations:
        for b in λ.domain:
            participating.add(b.id)
        for x in λ.codomain:
            participating.add(x.id)
    
    ungrounded = Σ.vertices - participating
    for v in ungrounded:
        violations.append(f"Ungrounded vertex: {v}")
    
    return violations


def check_connectivity(Σ: SimplicialComplex) -> List[str]:
    """
    Check single connected component.
    
    Axiom: β₀(Σ) = 1
    """
    violations = []
    
    if not Σ.vertices:
        return violations
    
    # BFS connectivity check
    visited = set()
    start = next(iter(Σ.vertices))
    queue = [start]
    
    # Build adjacency from 1-simplices
    adj: Dict[str, Set[str]] = {v: set() for v in Σ.vertices}
    for σ in Σ.k_simplices(1):
        v1, v2 = σ.vertices
        adj[v1].add(v2)
        adj[v2].add(v1)
    
    while queue:
        v = queue.pop(0)
        if v not in visited:
            visited.add(v)
            queue.extend(adj[v] - visited)
    
    unvisited = Σ.vertices - visited
    if unvisited:
        violations.append(f"Disconnected components: {len(unvisited)} vertices unreachable")
    
    return violations


def check_density(Σ: SimplicialComplex, threshold: float = 4.0) -> List[str]:
    """
    Check edge density.
    
    Axiom: |simplices|/|vertices| ≥ threshold
    """
    violations = []
    
    if Σ.vertices:
        density = len(Σ.simplices) / len(Σ.vertices)
        if density < threshold:
            violations.append(f"Insufficient density: {density:.2f} < {threshold}")
    
    return violations


# =============================================================================
# DSPY MODULE
# =============================================================================

class Validator(dspy.Module):
    """
    DSPy module for Lex axiom validation.
    
    Pipeline:
        (Σ, λ, τ) → check_axioms() → ValidationResult
    """
    
    DEFAULT_AXIOMS = [
        Axiom(AxiomType.ACYCLICITY, "No cycles in λ-graph", required=True),
        Axiom(AxiomType.GROUNDEDNESS, "All vertices grounded", required=False),
        Axiom(AxiomType.CONNECTIVITY, "Single component", required=True),
        Axiom(AxiomType.DENSITY, "Sufficient density", required=False),
    ]
    
    def __init__(self, axioms: List[Axiom] = None):
        super().__init__()
        self.axioms = axioms or self.DEFAULT_AXIOMS
        self.predictor = dspy.ChainOfThought(ValidatorSignature)
    
    def forward(self, state: AgentState) -> AgentResult:
        """
        Validate against Lex axioms.
        
        Args:
            state: AgentState containing complex, operations, terminals
        
        Returns:
            AgentResult with validation in state
        """
        if not state.complex:
            state.errors.append("No complex in state")
            return AgentResult(success=False, state=state)
        
        try:
            all_violations = []
            critical_violations = []
            
            for axiom in self.axioms:
                violations = []
                
                if axiom.type == AxiomType.ACYCLICITY:
                    violations = check_acyclicity(state.operations)
                elif axiom.type == AxiomType.GROUNDEDNESS:
                    violations = check_groundedness(state.complex, state.operations)
                elif axiom.type == AxiomType.CONNECTIVITY:
                    violations = check_connectivity(state.complex)
                elif axiom.type == AxiomType.DENSITY:
                    violations = check_density(state.complex)
                
                all_violations.extend(violations)
                if axiom.required and violations:
                    critical_violations.extend(violations)
            
            passed = len(critical_violations) == 0
            
            # Update state
            if not state.metrics:
                from .topologist import compute_metrics, compute_persistence
                dgm = compute_persistence(state.complex)
                state.metrics = compute_metrics(state.complex, dgm)
            
            return AgentResult(
                success=True,
                state=state,
                trace=f"Validated: {'PASS' if passed else 'FAIL'}, {len(all_violations)} violations"
            )
            
        except Exception as e:
            state.errors.append(f"Validation failed: {str(e)}")
            return AgentResult(
                success=False,
                state=state,
                trace=f"Error: {str(e)}"
            )


# =============================================================================
# FUNCTIONAL INTERFACE
# =============================================================================

def validate(
    Σ: SimplicialComplex,
    operations: Set[Operation],
    axioms: List[Axiom] = None
) -> ValidationResult:
    """
    Functional interface for validation.
    
    Args:
        Σ: Simplicial complex
        operations: Set of λ-operations
        axioms: Axioms to check (optional)
    
    Returns:
        ValidationResult
    """
    axioms = axioms or Validator.DEFAULT_AXIOMS
    all_violations = []
    
    for axiom in axioms:
        if axiom.type == AxiomType.ACYCLICITY:
            all_violations.extend(check_acyclicity(operations))
        elif axiom.type == AxiomType.GROUNDEDNESS:
            all_violations.extend(check_groundedness(Σ, operations))
        elif axiom.type == AxiomType.CONNECTIVITY:
            all_violations.extend(check_connectivity(Σ))
        elif axiom.type == AxiomType.DENSITY:
            all_violations.extend(check_density(Σ))
    
    # Check if any required axioms failed
    critical = any(
        axiom.required for axiom in axioms
        if (axiom.type == AxiomType.ACYCLICITY and check_acyclicity(operations)) or
           (axiom.type == AxiomType.CONNECTIVITY and check_connectivity(Σ))
    )
    
    return ValidationResult(
        passed=not critical,
        violations=all_violations
    )
