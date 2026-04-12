"""
Encoder Agent
=============

Query → Simplicial Complex Σ

Transforms natural language into topological structure.
Extracts vertices (ο-bases) and simplices (multi-way relations).
"""

from __future__ import annotations
from typing import Set, List, Dict, Optional, Tuple
import re
import dspy

from .types import (
    Base, Terminal, Operation, Simplex, SimplicialComplex,
    Query, Scope, ScopeLevel,
    EncoderSignature, AgentState, AgentResult
)


# =============================================================================
# SCOPE DETECTION
# =============================================================================

SCOPE_PATTERNS: Dict[str, List[str]] = {
    'list':     ['list', 'enumerate', 'name', 'state'],
    'outline':  ['outline', 'summarise', 'summarize', 'overview'],
    'describe': ['describe', 'characterise', 'characterize'],
    'explain':  ['explain', 'mechanism', 'how', 'why'],
    'compare':  ['compare', 'contrast', 'versus', 'vs'],
    'analyse':  ['analyse', 'analyze', 'examine', 'evaluate'],
}


def detect_scope(text: str) -> Scope:
    """Detect scope from query text."""
    text_lower = text.lower()
    
    for verb, patterns in SCOPE_PATTERNS.items():
        if any(p in text_lower for p in patterns):
            return Scope.from_verb(verb)
    
    return Scope.from_verb('explain')


# =============================================================================
# VERTEX EXTRACTION
# =============================================================================

def extract_vertices(text: str, known_vertices: Set[str] = None) -> Set[str]:
    """
    Extract vertex identifiers from text.
    
    Strategy:
    1. Match known vertices
    2. Extract capitalized terms
    3. Extract quoted terms
    """
    vertices = set()
    known = known_vertices or set()
    
    # Match known vertices
    for v in known:
        if v.lower() in text.lower():
            vertices.add(v)
    
    # Extract capitalized terms (potential entities)
    caps = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    vertices.update(caps)
    
    # Extract quoted terms
    quoted = re.findall(r'"([^"]+)"', text)
    vertices.update(quoted)
    
    # Extract terms in backticks
    backticked = re.findall(r'`([^`]+)`', text)
    vertices.update(backticked)
    
    return vertices


# =============================================================================
# SIMPLEX CONSTRUCTION
# =============================================================================

def build_simplicial_complex(
    vertices: Set[str],
    relations: List[Tuple[str, ...]] = None
) -> SimplicialComplex:
    """
    Build simplicial complex from vertices and relations.
    
    Each vertex becomes a 0-simplex.
    Each pair becomes a 1-simplex (edge).
    Higher-order relations become k-simplices.
    """
    Σ = SimplicialComplex()
    
    # Add all vertices as 0-simplices
    for v in vertices:
        Σ.add_vertex(v)
    
    # Add specified relations as simplices
    if relations:
        for rel in relations:
            if all(v in vertices for v in rel):
                Σ.add_simplex(rel)
    
    # Default: add edges between all pairs (complete graph)
    # Filter by co-occurrence in text later
    vertex_list = list(vertices)
    for i, v1 in enumerate(vertex_list):
        for v2 in vertex_list[i+1:]:
            Σ.add_simplex((v1, v2))
    
    return Σ


# =============================================================================
# DSPY MODULE
# =============================================================================

class Encoder(dspy.Module):
    """
    DSPy module for query encoding.
    
    Pipeline:
        Query → detect_scope() → extract_vertices() → build_complex() → Σ
    """
    
    def __init__(self, known_vertices: Set[str] = None):
        super().__init__()
        self.known_vertices = known_vertices or set()
        self.predictor = dspy.ChainOfThought(EncoderSignature)
    
    def forward(
        self,
        query_text: str,
        context: str = ""
    ) -> AgentResult:
        """
        Encode query into simplicial complex.
        
        Args:
            query_text: Natural language query
            context: Additional context
        
        Returns:
            AgentResult with complex in state
        """
        state = AgentState()
        
        try:
            # Step 1: Detect scope
            scope = detect_scope(query_text)
            
            # Step 2: Extract vertices
            vertices = extract_vertices(query_text, self.known_vertices)
            
            # Step 3: Build simplicial complex
            Σ = build_simplicial_complex(vertices)
            
            # Step 4: Construct query
            query = Query(
                text=query_text,
                scope=scope,
                focal_bases={Base(id=v) for v in vertices}
            )
            
            state.query = query
            state.complex = Σ
            
            return AgentResult(
                success=True,
                state=state,
                trace=f"Encoded: {len(vertices)} vertices, {len(Σ.simplices)} simplices, scope={scope.level.name}"
            )
            
        except Exception as e:
            state.errors.append(f"Encoding failed: {str(e)}")
            return AgentResult(
                success=False,
                state=state,
                trace=f"Error: {str(e)}"
            )
    
    def with_vertices(self, vertices: Set[str]) -> Encoder:
        """Set known vertices for matching."""
        self.known_vertices = vertices
        return self


# =============================================================================
# FUNCTIONAL INTERFACE
# =============================================================================

def encode(
    query_text: str,
    known_vertices: Set[str] = None,
    context: str = ""
) -> Tuple[Query, SimplicialComplex]:
    """
    Functional interface for encoding.
    
    Args:
        query_text: Natural language query
        known_vertices: Known vertex identifiers
        context: Additional context
    
    Returns:
        (Query, SimplicialComplex) tuple
    """
    encoder = Encoder(known_vertices)
    result = encoder.forward(query_text, context)
    
    if not result.success:
        raise ValueError(f"Encoding failed: {result.state.errors}")
    
    return result.state.query, result.state.complex
