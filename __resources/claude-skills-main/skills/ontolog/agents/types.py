"""
OntoLog Type System
===================

λ-calculus primitives over simplicial complexes.
All structures are holarchic—simultaneously wholes and parts.

Primitives:
    ο (omicron) : Base variable
    τ (tau)     : Terminal variable
    λ (lambda)  : Operation/abstraction
    Σ (sigma)   : Simplicial complex
    H (eta)     : Holon
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Set, List, Dict, Optional, Tuple, FrozenSet, Callable, Any
from enum import Enum
from abc import ABC, abstractmethod
import dspy


# =============================================================================
# LAMBDA CALCULUS PRIMITIVES
# =============================================================================

@dataclass(frozen=True)
class Base:
    """
    ο (omicron): Base variable.
    Grounded entity. Input to operations. Vertex in simplicial complex.
    
    Identity through structural position, not intrinsic properties.
    """
    id: str
    
    def __repr__(self) -> str:
        return f"ο({self.id})"
    
    def __hash__(self) -> int:
        return hash(self.id)


@dataclass(frozen=True)
class Terminal:
    """
    τ (tau): Terminal variable.
    Target purpose. Output of operations. Attractor in dynamical system.
    """
    id: str
    persistence: float = 1.0  # Topological significance
    
    def __repr__(self) -> str:
        return f"τ({self.id})"
    
    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Operation:
    """
    λ (lambda): Operation/abstraction.
    Transformation. Edge in simplicial complex. Maps bases toward terminals.
    
    Universal form: λο.τ
    """
    id: str
    domain: Set[Base]
    codomain: Set[Base | Terminal]
    path: List[Base] = field(default_factory=list)
    confidence: float = 1.0
    
    def __repr__(self) -> str:
        dom = ",".join(b.id for b in self.domain)
        cod = ",".join(x.id for x in self.codomain)
        return f"λ({dom}→{cod})"
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    @property
    def weight(self) -> float:
        """Combined weight for filtering."""
        return self.confidence


# =============================================================================
# SIMPLICIAL COMPLEX
# =============================================================================

@dataclass(frozen=True)
class Simplex:
    """
    k-simplex: ordered set of k+1 vertices.
    
    0-simplex: vertex (ο)
    1-simplex: edge (λ binary)
    2-simplex: triangle (λ ternary)
    """
    vertices: Tuple[str, ...]  # Ordered tuple of vertex IDs
    
    @property
    def dimension(self) -> int:
        return len(self.vertices) - 1
    
    def faces(self) -> Set[Simplex]:
        """All (k-1)-dimensional faces."""
        if self.dimension == 0:
            return set()
        return {
            Simplex(tuple(v for j, v in enumerate(self.vertices) if j != i))
            for i in range(len(self.vertices))
        }
    
    def __repr__(self) -> str:
        return f"σ[{','.join(self.vertices)}]"


@dataclass
class SimplicialComplex:
    """
    Σ (sigma): Simplicial complex.
    Collection of simplices closed under taking faces.
    """
    vertices: Set[str] = field(default_factory=set)
    simplices: Set[Simplex] = field(default_factory=set)
    
    def add_vertex(self, v: str):
        self.vertices.add(v)
        self.simplices.add(Simplex((v,)))
    
    def add_simplex(self, vertices: Tuple[str, ...]):
        """Add simplex and all its faces (closure property)."""
        σ = Simplex(vertices)
        self.simplices.add(σ)
        for v in vertices:
            self.vertices.add(v)
        # Add all faces recursively
        for face in σ.faces():
            if face not in self.simplices:
                self.add_simplex(face.vertices)
    
    def dimension(self) -> int:
        """Maximum dimension of any simplex."""
        if not self.simplices:
            return -1
        return max(σ.dimension for σ in self.simplices)
    
    def k_simplices(self, k: int) -> Set[Simplex]:
        """All k-dimensional simplices."""
        return {σ for σ in self.simplices if σ.dimension == k}
    
    def euler_characteristic(self) -> int:
        """χ = Σ (-1)^k |Σₖ|"""
        return sum(
            ((-1) ** k) * len(self.k_simplices(k))
            for k in range(self.dimension() + 1)
        )


# =============================================================================
# PERSISTENCE
# =============================================================================

@dataclass
class BirthDeath:
    """Single feature in persistence diagram."""
    birth: float
    death: float
    dimension: int
    
    @property
    def persistence(self) -> float:
        return self.death - self.birth
    
    def __repr__(self) -> str:
        return f"({self.birth:.2f}, {self.death:.2f})_{self.dimension}"


@dataclass
class PersistenceDiagram:
    """
    Multi-scale topological summary.
    """
    points: List[BirthDeath] = field(default_factory=list)
    
    def dimension(self, k: int) -> List[BirthDeath]:
        return [p for p in self.points if p.dimension == k]
    
    def max_persistence(self) -> float:
        if not self.points:
            return 0.0
        return max(p.persistence for p in self.points)
    
    def total_persistence(self) -> float:
        return sum(p.persistence for p in self.points)


# =============================================================================
# HOLON
# =============================================================================

@dataclass
class Holon:
    """
    H: Holarchic structure.
    Simultaneously whole (contains sub-holons) and part (contained in super-holon).
    Self-similar at all scales. Homoiconic: structure encodes semantics.
    """
    id: str
    complex: SimplicialComplex = field(default_factory=SimplicialComplex)
    operations: Set[Operation] = field(default_factory=set)
    terminals: Set[Terminal] = field(default_factory=set)
    sub_holons: Set[Holon] = field(default_factory=set)
    parent: Optional[Holon] = None
    
    # Persistence information
    persistence_diagram: Optional[PersistenceDiagram] = None
    
    def is_atomic(self) -> bool:
        """Has no sub-holons."""
        return len(self.sub_holons) == 0
    
    def depth(self) -> int:
        """Distance to root in holarchy."""
        if self.parent is None:
            return 0
        return 1 + self.parent.depth()
    
    def all_bases(self) -> Set[Base]:
        """All bases in this holon and sub-holons."""
        bases = {Base(id=v) for v in self.complex.vertices}
        for h in self.sub_holons:
            bases.update(h.all_bases())
        return bases
    
    def __repr__(self) -> str:
        return f"H({self.id}|{len(self.sub_holons)} sub)"
    
    def __hash__(self) -> int:
        return hash(self.id)


# =============================================================================
# QUERY
# =============================================================================

class ScopeLevel(Enum):
    LIST = 1
    OUTLINE = 2
    DESCRIBE = 3
    EXPLAIN = 4
    COMPARE = 5
    ANALYSE = 6


@dataclass
class Scope:
    """Traversal constraints."""
    level: ScopeLevel
    depth: int      # Hierarchical depth
    breadth: int    # Parallel paths
    
    @classmethod
    def from_verb(cls, verb: str) -> Scope:
        mapping = {
            'list':     (ScopeLevel.LIST, 1, 1),
            'outline':  (ScopeLevel.OUTLINE, 2, 3),
            'describe': (ScopeLevel.DESCRIBE, 3, 4),
            'explain':  (ScopeLevel.EXPLAIN, 4, 5),
            'compare':  (ScopeLevel.COMPARE, 3, 2),
            'analyse':  (ScopeLevel.ANALYSE, 5, 7),
        }
        level, d, b = mapping.get(verb.lower(), (ScopeLevel.EXPLAIN, 4, 5))
        return cls(level=level, depth=d, breadth=b)


@dataclass
class Query:
    """
    Query over holarchic structure.
    """
    text: str
    scope: Scope
    focal_bases: Set[Base] = field(default_factory=set)
    focal_terminals: Set[Terminal] = field(default_factory=set)


# =============================================================================
# METRICS
# =============================================================================

@dataclass
class Metrics:
    """Topological and structural metrics."""
    vertex_count: int = 0
    simplex_count: int = 0
    dimension: int = 0
    euler_characteristic: int = 0
    density: float = 0.0
    max_persistence: float = 0.0
    betti_0: int = 1  # Connected components
    betti_1: int = 0  # Loops
    
    def is_valid(self) -> bool:
        return (
            self.density >= 4.0 and
            self.betti_0 == 1  # Single component
        )
    
    def compact(self) -> str:
        valid = "✓" if self.is_valid() else "✗"
        return f"[Σ|v{self.vertex_count}|s{self.simplex_count}|η{self.density:.2f}|χ{self.euler_characteristic}|{valid}]"


@dataclass
class ValidationResult:
    """Result of axiom validation."""
    passed: bool
    violations: List[str] = field(default_factory=list)
    metrics: Optional[Metrics] = None


# =============================================================================
# AGENT STATE
# =============================================================================

@dataclass
class AgentState:
    """State passed between agents."""
    query: Optional[Query] = None
    complex: Optional[SimplicialComplex] = None
    operations: Set[Operation] = field(default_factory=set)
    terminals: Set[Terminal] = field(default_factory=set)
    holon: Optional[Holon] = None
    diagram: Optional[PersistenceDiagram] = None
    metrics: Optional[Metrics] = None
    errors: List[str] = field(default_factory=list)


@dataclass
class AgentResult:
    """Result from agent execution."""
    success: bool
    state: AgentState
    trace: str = ""


# =============================================================================
# DSPY SIGNATURES
# =============================================================================

class EncoderSignature(dspy.Signature):
    """Encode query into simplicial complex."""
    query_text: str = dspy.InputField(desc="Natural language query")
    context: str = dspy.InputField(desc="Contextual information")
    
    vertices: list = dspy.OutputField(desc="Extracted vertex IDs")
    simplices: list = dspy.OutputField(desc="Extracted simplex vertex tuples")
    scope_verb: str = dspy.OutputField(desc="Detected scope verb")


class TopologistSignature(dspy.Signature):
    """Compute persistent homology."""
    complex_json: str = dspy.InputField(desc="Simplicial complex as JSON")
    
    persistence_points: list = dspy.OutputField(desc="Birth-death pairs")
    betti_numbers: list = dspy.OutputField(desc="Betti numbers by dimension")


class ResolverSignature(dspy.Signature):
    """Resolve λ-operations."""
    vertices: list = dspy.InputField(desc="Available vertices")
    persistence: list = dspy.InputField(desc="Persistence information")
    
    operations: list = dspy.OutputField(desc="Resolved operations with structure")


class TargeterSignature(dspy.Signature):
    """Identify τ-terminals."""
    vertices: list = dspy.InputField(desc="Available vertices")
    operations: list = dspy.InputField(desc="Available operations")
    
    terminals: list = dspy.OutputField(desc="Identified terminals")


class ValidatorSignature(dspy.Signature):
    """Check Lex axioms."""
    complex_json: str = dspy.InputField(desc="Simplicial complex")
    operations_json: str = dspy.InputField(desc="Operations")
    axioms: list = dspy.InputField(desc="Axioms to check")
    
    passed: bool = dspy.OutputField(desc="Validation passed")
    violations: list = dspy.OutputField(desc="Violation descriptions")


class SynthesizerSignature(dspy.Signature):
    """Generate holon from components."""
    complex_json: str = dspy.InputField(desc="Simplicial complex")
    operations_json: str = dspy.InputField(desc="Operations")
    terminals_json: str = dspy.InputField(desc="Terminals")
    scope: str = dspy.InputField(desc="Output scope")
    
    holon_structure: str = dspy.OutputField(desc="Holon structure")
    formatted_output: str = dspy.OutputField(desc="Formatted result")
