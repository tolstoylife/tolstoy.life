"""
Resolver Agent
==============

Σ + Persistence → Set[λ]

Resolves λ-operations from simplicial structure.
Filters by persistence for significance.
"""

from __future__ import annotations
from typing import Set, List, Dict, Optional, Tuple
import dspy

from .types import (
    Base, Operation, SimplicialComplex, Simplex, PersistenceDiagram, Scope,
    ResolverSignature, AgentState, AgentResult
)


# =============================================================================
# OPERATION EXTRACTION
# =============================================================================

def extract_operations(
    Σ: SimplicialComplex,
    dgm: PersistenceDiagram = None
) -> Set[Operation]:
    """
    Extract λ-operations from simplicial complex.
    
    Each 1-simplex (edge) becomes a binary operation.
    Higher simplices become n-ary operations.
    """
    operations = set()
    
    # 1-simplices → binary operations
    for σ in Σ.k_simplices(1):
        v1, v2 = σ.vertices
        λ = Operation(
            id=f"λ_{v1}_{v2}",
            domain={Base(id=v1)},
            codomain={Base(id=v2)},
            path=[Base(id=v1), Base(id=v2)],
            confidence=1.0
        )
        operations.add(λ)
    
    # 2-simplices → ternary operations (paths)
    for σ in Σ.k_simplices(2):
        v1, v2, v3 = σ.vertices
        λ = Operation(
            id=f"λ_{v1}_{v2}_{v3}",
            domain={Base(id=v1)},
            codomain={Base(id=v3)},
            path=[Base(id=v1), Base(id=v2), Base(id=v3)],
            confidence=0.9  # Slightly lower for longer paths
        )
        operations.add(λ)
    
    return operations


def filter_by_persistence(
    operations: Set[Operation],
    dgm: PersistenceDiagram,
    threshold: float = 0.1
) -> Set[Operation]:
    """
    Filter operations by topological significance.
    
    Operations involving persistent features are retained.
    """
    if not dgm or not dgm.points:
        return operations
    
    # Get maximum persistence for normalization
    max_pers = dgm.max_persistence()
    if max_pers == 0 or max_pers == float('inf'):
        return operations
    
    # Filter: keep operations with above-threshold persistence
    # (Simplified: keep all for now, weight by persistence later)
    return operations


def filter_by_scope(
    operations: Set[Operation],
    scope: Scope
) -> Set[Operation]:
    """
    Filter operations by scope constraints.
    
    - depth: maximum path length
    - breadth: maximum operations per source
    """
    # Filter by depth (path length)
    depth_filtered = {
        λ for λ in operations
        if len(λ.path) <= scope.depth + 1
    }
    
    # Filter by breadth (top N per source)
    by_domain: Dict[str, List[Operation]] = {}
    for λ in depth_filtered:
        key = ",".join(b.id for b in λ.domain)
        if key not in by_domain:
            by_domain[key] = []
        by_domain[key].append(λ)
    
    breadth_filtered = set()
    for domain_key, ops in by_domain.items():
        sorted_ops = sorted(ops, key=lambda x: x.confidence, reverse=True)
        breadth_filtered.update(sorted_ops[:scope.breadth])
    
    return breadth_filtered


# =============================================================================
# DSPY MODULE
# =============================================================================

class Resolver(dspy.Module):
    """
    DSPy module for λ-operation resolution.
    
    Pipeline:
        Σ → extract_operations() → filter_by_persistence() → filter_by_scope() → Set[λ]
    """
    
    def __init__(self):
        super().__init__()
        self.predictor = dspy.ChainOfThought(ResolverSignature)
    
    def forward(
        self,
        state: AgentState,
        persistence_threshold: float = 0.1
    ) -> AgentResult:
        """
        Resolve λ-operations from simplicial complex.
        
        Args:
            state: AgentState containing complex and diagram
            persistence_threshold: Minimum persistence for retention
        
        Returns:
            AgentResult with operations in state
        """
        if not state.complex:
            state.errors.append("No complex in state")
            return AgentResult(success=False, state=state)
        
        try:
            # Step 1: Extract operations
            operations = extract_operations(state.complex, state.diagram)
            
            # Step 2: Filter by persistence
            operations = filter_by_persistence(
                operations, state.diagram, persistence_threshold
            )
            
            # Step 3: Filter by scope
            if state.query:
                operations = filter_by_scope(operations, state.query.scope)
            
            state.operations = operations
            
            return AgentResult(
                success=True,
                state=state,
                trace=f"Resolved: {len(operations)} λ-operations"
            )
            
        except Exception as e:
            state.errors.append(f"Resolution failed: {str(e)}")
            return AgentResult(
                success=False,
                state=state,
                trace=f"Error: {str(e)}"
            )


# =============================================================================
# FUNCTIONAL INTERFACE
# =============================================================================

def resolve_operations(
    Σ: SimplicialComplex,
    dgm: PersistenceDiagram = None,
    scope: Scope = None
) -> Set[Operation]:
    """
    Functional interface for operation resolution.
    
    Args:
        Σ: Simplicial complex
        dgm: Persistence diagram (optional)
        scope: Scope constraints (optional)
    
    Returns:
        Set of resolved operations
    """
    operations = extract_operations(Σ, dgm)
    
    if dgm:
        operations = filter_by_persistence(operations, dgm)
    
    if scope:
        operations = filter_by_scope(operations, scope)
    
    return operations
