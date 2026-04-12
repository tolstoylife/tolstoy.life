"""
Topologist Agent
================

Σ → Persistent Homology → Persistence Diagram

Computes multi-scale topological features.
Identifies significant structures via persistence.
"""

from __future__ import annotations
from typing import Set, List, Dict, Optional, Tuple
import dspy
from collections import defaultdict

from .types import (
    SimplicialComplex, Simplex, PersistenceDiagram, BirthDeath, Metrics,
    TopologistSignature, AgentState, AgentResult
)


# =============================================================================
# BOUNDARY MATRIX
# =============================================================================

def boundary_matrix(Σ: SimplicialComplex, k: int) -> Dict[Simplex, Dict[Simplex, int]]:
    """
    Compute boundary matrix ∂ₖ: Cₖ → Cₖ₋₁
    
    ∂ₖ[v₀,...,vₖ] = Σᵢ (-1)ⁱ [v₀,...,v̂ᵢ,...,vₖ]
    """
    k_simplices = list(Σ.k_simplices(k))
    k_minus_1_simplices = list(Σ.k_simplices(k - 1)) if k > 0 else []
    
    boundary = {}
    
    for σ in k_simplices:
        boundary[σ] = {}
        for i, v in enumerate(σ.vertices):
            # Face without vertex i
            face_vertices = tuple(v for j, v in enumerate(σ.vertices) if j != i)
            face = Simplex(face_vertices)
            
            if face in Σ.simplices:
                sign = (-1) ** i
                boundary[σ][face] = sign
    
    return boundary


# =============================================================================
# BETTI NUMBERS
# =============================================================================

def compute_betti_numbers(Σ: SimplicialComplex) -> List[int]:
    """
    Compute Betti numbers β₀, β₁, β₂, ...
    
    βₖ = dim(Hₖ) = dim(ker ∂ₖ) - dim(im ∂ₖ₊₁)
    
    Simplified computation for small complexes.
    """
    betti = []
    max_dim = Σ.dimension()
    
    for k in range(max_dim + 1):
        # Simplified: count k-simplices minus boundaries
        k_count = len(Σ.k_simplices(k))
        
        if k == 0:
            # β₀ = connected components (approximate)
            # For complete graph, β₀ = 1
            betti.append(1)
        elif k == 1:
            # β₁ = independent cycles
            # Euler characteristic: χ = V - E + F = β₀ - β₁ + β₂
            v = len(Σ.vertices)
            e = len(Σ.k_simplices(1))
            # For simple graph: β₁ ≈ e - v + 1
            betti.append(max(0, e - v + 1))
        else:
            # Higher dimensions
            betti.append(0)
    
    return betti


# =============================================================================
# PERSISTENCE COMPUTATION
# =============================================================================

def compute_filtration(Σ: SimplicialComplex) -> List[Tuple[float, Simplex]]:
    """
    Compute filtration ordering.
    
    Default: order by dimension, then lexicographically.
    """
    filtration = []
    
    for dim in range(Σ.dimension() + 1):
        simplices = sorted(Σ.k_simplices(dim), key=lambda σ: σ.vertices)
        for σ in simplices:
            scale = float(dim)  # Simple: scale = dimension
            filtration.append((scale, σ))
    
    return filtration


def compute_persistence(Σ: SimplicialComplex) -> PersistenceDiagram:
    """
    Compute persistent homology.
    
    Simplified algorithm tracking feature births and deaths.
    """
    filtration = compute_filtration(Σ)
    points = []
    
    # Track connected components (H₀)
    components = {v: v for v in Σ.vertices}  # Union-find structure
    
    def find(v):
        if components[v] != v:
            components[v] = find(components[v])
        return components[v]
    
    def union(v1, v2, scale):
        r1, r2 = find(v1), find(v2)
        if r1 != r2:
            # Component merges (death of one component)
            components[r2] = r1
            points.append(BirthDeath(birth=0.0, death=scale, dimension=0))
    
    # Process filtration
    for scale, σ in filtration:
        if σ.dimension == 1:
            # Edge: may merge components
            v1, v2 = σ.vertices
            union(v1, v2, scale)
    
    # Surviving components
    unique_roots = len(set(find(v) for v in Σ.vertices))
    for _ in range(unique_roots):
        points.append(BirthDeath(birth=0.0, death=float('inf'), dimension=0))
    
    # H₁: cycles (simplified)
    betti_1 = len(Σ.k_simplices(1)) - len(Σ.vertices) + 1
    for i in range(max(0, betti_1)):
        points.append(BirthDeath(birth=1.0, death=float('inf'), dimension=1))
    
    return PersistenceDiagram(points=points)


# =============================================================================
# METRICS COMPUTATION
# =============================================================================

def compute_metrics(Σ: SimplicialComplex, dgm: PersistenceDiagram) -> Metrics:
    """
    Compute topological metrics.
    """
    vertex_count = len(Σ.vertices)
    simplex_count = len(Σ.simplices)
    dimension = Σ.dimension()
    euler = Σ.euler_characteristic()
    
    # Density = simplices / vertices
    density = simplex_count / max(1, vertex_count)
    
    # Max persistence
    max_pers = dgm.max_persistence() if dgm.points else 0.0
    
    # Betti numbers
    betti = compute_betti_numbers(Σ)
    
    return Metrics(
        vertex_count=vertex_count,
        simplex_count=simplex_count,
        dimension=dimension,
        euler_characteristic=euler,
        density=density,
        max_persistence=max_pers,
        betti_0=betti[0] if betti else 1,
        betti_1=betti[1] if len(betti) > 1 else 0
    )


# =============================================================================
# DSPY MODULE
# =============================================================================

class Topologist(dspy.Module):
    """
    DSPy module for topological analysis.
    
    Pipeline:
        Σ → filtration() → persistence() → diagram + metrics
    """
    
    def __init__(self):
        super().__init__()
        self.predictor = dspy.ChainOfThought(TopologistSignature)
    
    def forward(self, state: AgentState) -> AgentResult:
        """
        Compute persistent homology.
        
        Args:
            state: AgentState containing SimplicialComplex
        
        Returns:
            AgentResult with PersistenceDiagram and Metrics
        """
        if not state.complex:
            state.errors.append("No complex in state")
            return AgentResult(success=False, state=state)
        
        try:
            # Step 1: Compute persistence
            dgm = compute_persistence(state.complex)
            
            # Step 2: Compute metrics
            metrics = compute_metrics(state.complex, dgm)
            
            state.diagram = dgm
            state.metrics = metrics
            
            return AgentResult(
                success=True,
                state=state,
                trace=f"Homology: {metrics.compact()}"
            )
            
        except Exception as e:
            state.errors.append(f"Topology computation failed: {str(e)}")
            return AgentResult(
                success=False,
                state=state,
                trace=f"Error: {str(e)}"
            )


# =============================================================================
# FUNCTIONAL INTERFACE
# =============================================================================

def analyze_topology(Σ: SimplicialComplex) -> Tuple[PersistenceDiagram, Metrics]:
    """
    Functional interface for topological analysis.
    
    Args:
        Σ: Simplicial complex
    
    Returns:
        (PersistenceDiagram, Metrics) tuple
    """
    dgm = compute_persistence(Σ)
    metrics = compute_metrics(Σ, dgm)
    return dgm, metrics
