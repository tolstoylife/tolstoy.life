"""
Targeter Agent
==============

Σ + Set[λ] → Set[τ]

Identifies τ-terminals from structure.
Terminals are attractors reachable via operations.
"""

from __future__ import annotations
from typing import Set, List, Dict, Optional
import dspy

from .types import (
    Base, Terminal, Operation, SimplicialComplex,
    TargeterSignature, AgentState, AgentResult
)


# =============================================================================
# TERMINAL IDENTIFICATION
# =============================================================================

def identify_terminals(
    Σ: SimplicialComplex,
    operations: Set[Operation]
) -> Set[Terminal]:
    """
    Identify τ-terminals from structure.
    
    Terminals are:
    1. Vertices with only incoming operations (sinks)
    2. Vertices with high in-degree
    3. Vertices that appear in many operation codomains
    """
    terminals = set()
    
    # Count in-degree and out-degree
    in_degree: Dict[str, int] = {v: 0 for v in Σ.vertices}
    out_degree: Dict[str, int] = {v: 0 for v in Σ.vertices}
    
    for λ in operations:
        for b in λ.domain:
            if b.id in out_degree:
                out_degree[b.id] += 1
        for x in λ.codomain:
            if x.id in in_degree:
                in_degree[x.id] += 1
    
    # Identify sinks (only incoming, no outgoing)
    for v in Σ.vertices:
        if in_degree[v] > 0 and out_degree[v] == 0:
            terminals.add(Terminal(
                id=v,
                persistence=1.0  # Sinks are definite terminals
            ))
    
    # Identify high in-degree vertices (attractors)
    if Σ.vertices:
        max_in = max(in_degree.values())
        threshold = max_in * 0.5
        
        for v in Σ.vertices:
            if in_degree[v] >= threshold and v not in {t.id for t in terminals}:
                # Persistence proportional to in-degree ratio
                pers = in_degree[v] / max(1, max_in)
                terminals.add(Terminal(id=v, persistence=pers))
    
    return terminals


def compute_reachability(
    operations: Set[Operation],
    terminals: Set[Terminal]
) -> Dict[str, Set[str]]:
    """
    Compute which bases can reach which terminals.
    
    Returns:
        Map from terminal ID to set of reachable-from base IDs
    """
    reachability: Dict[str, Set[str]] = {t.id: set() for t in terminals}
    
    # Build reverse adjacency (from codomain to domain)
    reverse_adj: Dict[str, Set[str]] = {}
    for λ in operations:
        for x in λ.codomain:
            if x.id not in reverse_adj:
                reverse_adj[x.id] = set()
            for b in λ.domain:
                reverse_adj[x.id].add(b.id)
    
    # BFS from each terminal backward
    for τ in terminals:
        visited = {τ.id}
        queue = [τ.id]
        
        while queue:
            current = queue.pop(0)
            for predecessor in reverse_adj.get(current, []):
                if predecessor not in visited:
                    visited.add(predecessor)
                    queue.append(predecessor)
                    reachability[τ.id].add(predecessor)
    
    return reachability


# =============================================================================
# DSPY MODULE
# =============================================================================

class Targeter(dspy.Module):
    """
    DSPy module for τ-terminal identification.
    
    Pipeline:
        (Σ, Set[λ]) → identify_terminals() → compute_reachability() → Set[τ]
    """
    
    def __init__(self):
        super().__init__()
        self.predictor = dspy.ChainOfThought(TargeterSignature)
    
    def forward(self, state: AgentState) -> AgentResult:
        """
        Identify τ-terminals.
        
        Args:
            state: AgentState containing complex and operations
        
        Returns:
            AgentResult with terminals in state
        """
        if not state.complex:
            state.errors.append("No complex in state")
            return AgentResult(success=False, state=state)
        
        try:
            # Step 1: Identify terminals
            terminals = identify_terminals(state.complex, state.operations)
            
            # Step 2: Compute reachability
            reachability = compute_reachability(state.operations, terminals)
            
            # Step 3: Filter to reachable from query focal bases
            if state.query and state.query.focal_bases:
                focal_ids = {b.id for b in state.query.focal_bases}
                filtered = set()
                for τ in terminals:
                    if reachability.get(τ.id, set()) & focal_ids:
                        filtered.add(τ)
                    elif τ.id in focal_ids:
                        filtered.add(τ)
                terminals = filtered if filtered else terminals
            
            state.terminals = terminals
            
            return AgentResult(
                success=True,
                state=state,
                trace=f"Targeted: {len(terminals)} τ-terminals"
            )
            
        except Exception as e:
            state.errors.append(f"Targeting failed: {str(e)}")
            return AgentResult(
                success=False,
                state=state,
                trace=f"Error: {str(e)}"
            )


# =============================================================================
# FUNCTIONAL INTERFACE
# =============================================================================

def target_terminals(
    Σ: SimplicialComplex,
    operations: Set[Operation],
    focal_bases: Set[Base] = None
) -> Set[Terminal]:
    """
    Functional interface for terminal identification.
    
    Args:
        Σ: Simplicial complex
        operations: Set of λ-operations
        focal_bases: Query focal bases (optional)
    
    Returns:
        Set of identified terminals
    """
    terminals = identify_terminals(Σ, operations)
    
    if focal_bases:
        reachability = compute_reachability(operations, terminals)
        focal_ids = {b.id for b in focal_bases}
        
        filtered = {
            τ for τ in terminals
            if reachability.get(τ.id, set()) & focal_ids or τ.id in focal_ids
        }
        return filtered if filtered else terminals
    
    return terminals
