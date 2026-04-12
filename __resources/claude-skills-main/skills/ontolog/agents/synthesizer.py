"""
Synthesizer Agent
=================

(Σ, Set[λ], Set[τ], Persistence) → Holon

Generates holarchic structure from components.
Produces formatted output based on scope.
"""

from __future__ import annotations
from typing import Set, List, Dict, Optional
import dspy
from abc import ABC, abstractmethod

from .types import (
    Base, Terminal, Operation, SimplicialComplex, PersistenceDiagram,
    Holon, Query, Scope, ScopeLevel,
    SynthesizerSignature, AgentState, AgentResult
)


# =============================================================================
# HOLON CONSTRUCTION
# =============================================================================

def build_holon(
    id: str,
    Σ: SimplicialComplex,
    operations: Set[Operation],
    terminals: Set[Terminal],
    dgm: PersistenceDiagram = None
) -> Holon:
    """
    Construct holon from components.
    
    λ-calculus interpretation:
        ο = vertices (bases)
        λ = operations  
        τ = terminals
    """
    H = Holon(
        id=id,
        complex=Σ,
        operations=operations,
        terminals=terminals,
        persistence_diagram=dgm
    )
    
    return H


def decompose_holon(
    H: Holon,
    min_size: int = 3
) -> Set[Holon]:
    """
    Decompose holon into sub-holons.
    
    Uses community detection on operation graph.
    """
    sub_holons = set()
    
    # Simple decomposition: each terminal defines a sub-holon
    for τ in H.terminals:
        # Find operations leading to this terminal
        relevant_ops = {
            λ for λ in H.operations
            if any(x.id == τ.id for x in λ.codomain)
        }
        
        if len(relevant_ops) >= min_size:
            # Create sub-complex
            vertices = set()
            for λ in relevant_ops:
                vertices.update(b.id for b in λ.domain)
                vertices.update(x.id for x in λ.codomain)
            
            sub_Σ = SimplicialComplex()
            for v in vertices:
                sub_Σ.add_vertex(v)
            
            sub_H = Holon(
                id=f"{H.id}::{τ.id}",
                complex=sub_Σ,
                operations=relevant_ops,
                terminals={τ},
                parent=H
            )
            sub_holons.add(sub_H)
    
    H.sub_holons = sub_holons
    return sub_holons


# =============================================================================
# FORMATTERS
# =============================================================================

class Formatter(ABC):
    """Abstract formatter for holon output."""
    
    @abstractmethod
    def format(self, H: Holon, query: Query = None) -> str:
        pass


class TripartiteFormatter(Formatter):
    """
    Hierarchical outline format.
    
    ο (bases) → λ (operations) → τ (terminals)
    """
    
    def format(self, H: Holon, query: Query = None) -> str:
        lines = []
        
        # Header
        lines.append(f"# {H.id}")
        lines.append("")
        
        # Terminals (τ)
        lines.append("## Terminals (τ)")
        for τ in sorted(H.terminals, key=lambda x: x.persistence, reverse=True):
            lines.append(f"- **{τ.id}** [pers={τ.persistence:.2f}]")
        lines.append("")
        
        # Operations (λ)
        lines.append("## Operations (λ)")
        for λ in sorted(H.operations, key=lambda x: x.confidence, reverse=True):
            dom = ", ".join(b.id for b in λ.domain)
            cod = ", ".join(x.id for x in λ.codomain)
            lines.append(f"- {dom} → {cod} [conf={λ.confidence:.2f}]")
        lines.append("")
        
        # Bases (ο)
        lines.append("## Bases (ο)")
        for v in sorted(H.complex.vertices):
            lines.append(f"- {v}")
        
        # Sub-holons
        if H.sub_holons:
            lines.append("")
            lines.append("## Sub-holons")
            for h in H.sub_holons:
                lines.append(f"- {h.id}")
        
        return "\n".join(lines)


class ProseFormatter(Formatter):
    """
    Prose format for verbal delivery.
    
    Natural language synthesis.
    """
    
    def format(self, H: Holon, query: Query = None) -> str:
        parts = []
        
        # Terminal summary
        terminals = sorted(H.terminals, key=lambda x: x.persistence, reverse=True)
        if terminals:
            τ_names = ", ".join(τ.id for τ in terminals[:3])
            parts.append(f"The analysis targets {τ_names}.")
        
        # Operation summary
        op_count = len(H.operations)
        parts.append(f"There are {op_count} transformations connecting the components.")
        
        # Base summary
        base_count = len(H.complex.vertices)
        parts.append(f"The structure contains {base_count} base entities.")
        
        # Topology summary
        if H.persistence_diagram:
            max_pers = H.persistence_diagram.max_persistence()
            parts.append(f"Maximum topological persistence: {max_pers:.2f}.")
        
        return " ".join(parts)


class CompactFormatter(Formatter):
    """
    Compact single-line format.
    
    [H|ο{n}|λ{m}|τ{k}|pers{p}]
    """
    
    def format(self, H: Holon, query: Query = None) -> str:
        n = len(H.complex.vertices)
        m = len(H.operations)
        k = len(H.terminals)
        p = H.persistence_diagram.max_persistence() if H.persistence_diagram else 0.0
        
        return f"[{H.id}|ο{n}|λ{m}|τ{k}|pers{p:.2f}]"


def get_formatter(scope: ScopeLevel) -> Formatter:
    """Select formatter based on scope."""
    if scope in {ScopeLevel.LIST, ScopeLevel.OUTLINE}:
        return TripartiteFormatter()
    elif scope == ScopeLevel.DESCRIBE:
        return ProseFormatter()
    else:
        return TripartiteFormatter()


# =============================================================================
# DSPY MODULE
# =============================================================================

class Synthesizer(dspy.Module):
    """
    DSPy module for holon synthesis.
    
    Pipeline:
        (Σ, λ, τ, dgm) → build_holon() → decompose() → format() → output
    """
    
    def __init__(self, decompose: bool = True):
        super().__init__()
        self.decompose = decompose
        self.predictor = dspy.ChainOfThought(SynthesizerSignature)
    
    def forward(self, state: AgentState) -> AgentResult:
        """
        Synthesize holon from components.
        
        Args:
            state: AgentState with all components
        
        Returns:
            AgentResult with holon and formatted output
        """
        if not state.complex:
            state.errors.append("No complex in state")
            return AgentResult(success=False, state=state)
        
        try:
            # Generate holon ID from query
            holon_id = "H"
            if state.query:
                # Use first few words of query
                words = state.query.text.split()[:3]
                holon_id = "_".join(w for w in words if w.isalnum())
            
            # Step 1: Build holon
            H = build_holon(
                id=holon_id,
                Σ=state.complex,
                operations=state.operations,
                terminals=state.terminals,
                dgm=state.diagram
            )
            
            # Step 2: Decompose (optional)
            if self.decompose and len(state.terminals) > 1:
                decompose_holon(H)
            
            # Step 3: Format output
            scope = state.query.scope.level if state.query else ScopeLevel.EXPLAIN
            formatter = get_formatter(scope)
            output = formatter.format(H, state.query)
            
            state.holon = H
            
            return AgentResult(
                success=True,
                state=state,
                trace=f"Synthesized: {CompactFormatter().format(H)}"
            )
            
        except Exception as e:
            state.errors.append(f"Synthesis failed: {str(e)}")
            return AgentResult(
                success=False,
                state=state,
                trace=f"Error: {str(e)}"
            )


# =============================================================================
# FUNCTIONAL INTERFACE
# =============================================================================

def synthesize(
    Σ: SimplicialComplex,
    operations: Set[Operation],
    terminals: Set[Terminal],
    dgm: PersistenceDiagram = None,
    query: Query = None
) -> Tuple[Holon, str]:
    """
    Functional interface for holon synthesis.
    
    Args:
        Σ: Simplicial complex
        operations: Set of λ-operations
        terminals: Set of τ-terminals
        dgm: Persistence diagram
        query: Original query
    
    Returns:
        (Holon, formatted_output) tuple
    """
    from typing import Tuple
    
    holon_id = "H"
    if query:
        words = query.text.split()[:3]
        holon_id = "_".join(w for w in words if w.isalnum())
    
    H = build_holon(holon_id, Σ, operations, terminals, dgm)
    
    if len(terminals) > 1:
        decompose_holon(H)
    
    scope = query.scope.level if query else ScopeLevel.EXPLAIN
    formatter = get_formatter(scope)
    output = formatter.format(H, query)
    
    return H, output
