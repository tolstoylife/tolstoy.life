#!/usr/bin/env python3
"""
MEGA v2.0 Core Implementation
────────────────────────────
Maximally Endowed Graph Architecture with operational grounding.

Pareto principle: complexity is earned, not assumed.
Most structures stay at Level 0-2; full MEGA reserved for pathological cases.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import (
    Dict, List, Set, Optional, Tuple, Callable, Any, 
    FrozenSet, TypeVar, Generic
)
from enum import IntEnum, Enum, auto
from abc import ABC, abstractmethod
import math
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MEGA")


# =============================================================================
# CORE TYPES
# =============================================================================

class Level(IntEnum):
    """n-SHG level assignment. Max practical depth is 3."""
    ENTITY = 0      # Atomic concepts
    GROUPING = 1    # Sets of entities
    SCHEMA = 2      # Patterns across groupings
    PARADIGM = 3    # Organizing principles (rarely needed)


@dataclass(frozen=True)
class UncertaintyTuple:
    """Grounded plithogenic attributes: (confidence, coverage, source_quality)."""
    confidence: float      # [0,1] epistemic certainty
    coverage: float        # [0,1] fraction of attribute space
    source_quality: float  # [0,1] reliability of evidence
    
    def __post_init__(self):
        for name in ['confidence', 'coverage', 'source_quality']:
            val = getattr(self, name)
            if not 0 <= val <= 1:
                raise ValueError(f"{name} must be in [0,1], got {val}")
    
    def __and__(self, other: UncertaintyTuple) -> UncertaintyTuple:
        """Conjunction (meet)."""
        return UncertaintyTuple(
            min(self.confidence, other.confidence),
            min(self.coverage, other.coverage),
            min(self.source_quality, other.source_quality)
        )
    
    def __or__(self, other: UncertaintyTuple) -> UncertaintyTuple:
        """Disjunction (join)."""
        return UncertaintyTuple(
            max(self.confidence, other.confidence),
            max(self.coverage, other.coverage),
            max(self.source_quality, other.source_quality)
        )
    
    def contradicts(self, other: UncertaintyTuple, threshold: float = 0.5) -> bool:
        """Check if contradictory (high quality sources disagree)."""
        return (
            abs(self.confidence - other.confidence) > threshold and
            min(self.source_quality, other.source_quality) > 0.6
        )


@dataclass
class Node:
    """MEGA node at any level."""
    id: str
    level: Level = Level.ENTITY
    content: FrozenSet[str] = field(default_factory=frozenset)  # contained node IDs
    attributes: Dict[str, UncertaintyTuple] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id


@dataclass
class Edge:
    """MEGA edge with optional label and weight."""
    source: str
    target: str
    label: str = "related"
    weight: float = 1.0
    attributes: Dict[str, UncertaintyTuple] = field(default_factory=dict)
    
    @property
    def id(self) -> str:
        return f"{self.source}-[{self.label}]->{self.target}"


# =============================================================================
# n-SUPERHYPERGRAPH
# =============================================================================

@dataclass
class nSHG:
    """
    Bounded n-SuperHyperGraph (n ≤ 3).
    
    Core invariants:
      - η = |E|/|V| ≥ 4 (edge density)
      - φ < 0.2 (isolation ratio)
      - Levels well-founded (no orphans at higher levels)
    """
    nodes: Dict[str, Node] = field(default_factory=dict)
    edges: Dict[str, Edge] = field(default_factory=dict)
    correlations: Dict[Tuple[str, str], float] = field(default_factory=dict)
    max_level: Level = Level.ENTITY
    
    # Invariant thresholds
    ETA_THRESHOLD: float = 4.0
    PHI_THRESHOLD: float = 0.2
    CORRELATION_THRESHOLD: float = 0.5
    
    def add_node(self, node: Node) -> None:
        """Add node with level validation."""
        if node.level > Level.PARADIGM:
            raise ValueError(f"Level {node.level} exceeds max (3)")
        
        # Validate containment level consistency
        if node.level > Level.ENTITY and node.content:
            for child_id in node.content:
                if child_id in self.nodes:
                    child = self.nodes[child_id]
                    if child.level >= node.level:
                        raise ValueError(
                            f"Level violation: {node.id}@L{node.level} "
                            f"contains {child_id}@L{child.level}"
                        )
        
        self.nodes[node.id] = node
        self.max_level = max(self.max_level, node.level)
    
    def add_edge(self, edge: Edge) -> None:
        """Add edge with existence validation."""
        if edge.source not in self.nodes:
            raise ValueError(f"Source node {edge.source} not found")
        if edge.target not in self.nodes:
            raise ValueError(f"Target node {edge.target} not found")
        self.edges[edge.id] = edge
    
    def set_correlation(self, node_a: str, node_b: str, value: float) -> None:
        """Set correlation between nodes (symmetric)."""
        if not -1 <= value <= 1:
            raise ValueError(f"Correlation must be in [-1,1], got {value}")
        if abs(value) < self.CORRELATION_THRESHOLD:
            return  # Don't store weak correlations
        key = (min(node_a, node_b), max(node_a, node_b))
        self.correlations[key] = value
    
    @property
    def eta(self) -> float:
        """Edge density η = |E|/|V|."""
        return len(self.edges) / max(len(self.nodes), 1)
    
    @property
    def phi(self) -> float:
        """Isolation ratio φ = |isolated|/|V|."""
        connected = set()
        for edge in self.edges.values():
            connected.add(edge.source)
            connected.add(edge.target)
        isolated = len(self.nodes) - len(connected)
        return isolated / max(len(self.nodes), 1)
    
    def nodes_at_level(self, level: Level) -> List[Node]:
        """Get all nodes at specified level."""
        return [n for n in self.nodes.values() if n.level == level]
    
    def degree(self, node_id: str) -> int:
        """Compute node degree (undirected)."""
        return sum(
            1 for e in self.edges.values()
            if e.source == node_id or e.target == node_id
        )
    
    def neighbors(self, node_id: str) -> Set[str]:
        """Get neighbor node IDs."""
        result = set()
        for e in self.edges.values():
            if e.source == node_id:
                result.add(e.target)
            elif e.target == node_id:
                result.add(e.source)
        return result
    
    def validate(self) -> List[str]:
        """Check all invariants, return violation messages."""
        violations = []
        
        # η check
        if self.eta < self.ETA_THRESHOLD:
            violations.append(f"η={self.eta:.2f} < {self.ETA_THRESHOLD}")
        
        # φ check
        if self.phi > self.PHI_THRESHOLD:
            violations.append(f"φ={self.phi:.2f} > {self.PHI_THRESHOLD}")
        
        # Level grounding check
        for node in self.nodes.values():
            if node.level > Level.ENTITY:
                has_lower_link = any(
                    (e.source == node.id and 
                     self.nodes[e.target].level < node.level) or
                    (e.target == node.id and 
                     self.nodes[e.source].level < node.level)
                    for e in self.edges.values()
                    if e.source in self.nodes and e.target in self.nodes
                )
                if not has_lower_link and not node.content:
                    violations.append(f"Node {node.id}@L{node.level} ungrounded")
        
        return violations
    
    def is_valid(self) -> bool:
        """Quick validity check."""
        return len(self.validate()) == 0


# =============================================================================
# COMPLEXITY ESCALATION
# =============================================================================

class EscalationLevel(IntEnum):
    """Pareto-governed complexity ladder."""
    SIMPLE_GRAPH = 0
    PROPERTY_GRAPH = 1
    HYPERGRAPH = 2
    N_SHG = 3
    FULL_MEGA = 4


def assess_escalation(graph: nSHG) -> Tuple[EscalationLevel, List[str]]:
    """
    Determine appropriate complexity level via Pareto governance.
    
    Returns (recommended_level, reasons).
    """
    reasons = []
    level = EscalationLevel.SIMPLE_GRAPH
    
    # Check η
    if graph.eta < 2:
        reasons.append(f"η={graph.eta:.2f} < 2: needs densification")
        level = max(level, EscalationLevel.PROPERTY_GRAPH)
    
    # Check φ
    if graph.phi > 0.3:
        reasons.append(f"φ={graph.phi:.2f} > 0.3: high isolation")
        level = max(level, EscalationLevel.PROPERTY_GRAPH)
    
    # Check for structured uncertainty
    has_uncertainty = any(
        len(node.attributes) > 0 
        for node in graph.nodes.values()
    )
    if has_uncertainty:
        has_contradictions = any(
            u1.contradicts(u2)
            for node in graph.nodes.values()
            for u1 in node.attributes.values()
            for u2 in node.attributes.values()
            if u1 != u2
        )
        if has_contradictions:
            reasons.append("Has contradicting uncertainty: needs plithogenic")
            level = max(level, EscalationLevel.HYPERGRAPH)
    
    # Check for hypernodes
    has_hypernodes = any(
        node.level > Level.ENTITY 
        for node in graph.nodes.values()
    )
    if has_hypernodes:
        max_depth = max(node.level for node in graph.nodes.values())
        reasons.append(f"Has hypernodes at level {max_depth}")
        level = max(level, EscalationLevel.N_SHG)
    
    # Check for correlations
    has_correlations = len(graph.correlations) > 0
    if has_correlations and level >= EscalationLevel.N_SHG:
        reasons.append("Has correlations: approaching full MEGA")
        level = max(level, EscalationLevel.FULL_MEGA)
    
    return level, reasons


# =============================================================================
# QUERY CONTEXT & DECOHERENCE
# =============================================================================

@dataclass
class QueryContext:
    """Context extracted from query for disambiguation."""
    query_text: str
    domain: Optional[str] = None
    temporal_focus: Optional[str] = None
    scope: Optional[str] = None
    
    @classmethod
    def from_query(cls, query: str) -> QueryContext:
        """Extract context from query string."""
        ctx = cls(query_text=query)
        
        # Domain detection keywords
        domain_keywords = {
            "hemodynamic": ["cardiac", "CO", "SVR", "heart", "flow", "pressure"],
            "respiratory": ["ventilation", "oxygen", "FiO2", "PEEP", "lung"],
            "pharmacology": ["drug", "dose", "pharmacokinetics", "metabolism"],
            "toxicology": ["poison", "overdose", "toxin", "antidote"],
        }
        
        # Domain detection
        query_lower = query.lower()
        for domain, keywords in domain_keywords.items():
            if any(kw.lower() in query_lower for kw in keywords):
                ctx.domain = domain
                break
        
        return ctx
    
    def semantic_similarity(self, text: str) -> float:
        """Simple word overlap similarity."""
        query_words = set(self.query_text.lower().split())
        text_words = set(text.lower().split())
        if not query_words or not text_words:
            return 0.0
        intersection = len(query_words & text_words)
        union = len(query_words | text_words)
        return intersection / union if union > 0 else 0.0


@dataclass
class Interpretation:
    """One possible meaning for a polysemous node."""
    meaning: str
    domain: str
    confidence: float


@dataclass
class PolysemousNode:
    """Node with multiple possible interpretations."""
    id: str
    interpretations: List[Interpretation]
    
    def resolve(self, context: QueryContext) -> str:
        """Resolve to best interpretation for context."""
        if not self.interpretations:
            return self.id
        
        # Prefer domain match
        for interp in self.interpretations:
            if interp.domain == context.domain:
                return interp.meaning
        
        # Fall back to semantic similarity
        best = max(
            self.interpretations,
            key=lambda i: context.semantic_similarity(i.meaning)
        )
        return best.meaning


def decohere(
    graph: nSHG,
    query: str,
    polysemous: Optional[List[PolysemousNode]] = None
) -> nSHG:
    """
    Query-time materialization: resolve ambiguities for specific query.
    
    This is 'decoherence' in operational terms—not quantum mechanics,
    but lazy evaluation becoming eager upon observation (query).
    """
    context = QueryContext.from_query(query)
    polysemous = polysemous or []
    
    # Build resolution map
    resolutions = {}
    for poly in polysemous:
        resolutions[poly.id] = poly.resolve(context)
    
    # Clone graph with resolutions
    resolved = nSHG()
    
    for node in graph.nodes.values():
        new_metadata = dict(node.metadata)
        if node.id in resolutions:
            new_metadata['_resolved_meaning'] = resolutions[node.id]
            new_metadata['_resolution_context'] = context.domain
        
        resolved.add_node(Node(
            id=node.id,
            level=node.level,
            content=node.content,
            attributes=node.attributes,
            metadata=new_metadata
        ))
    
    for edge in graph.edges.values():
        resolved.add_edge(edge)
    
    resolved.correlations = dict(graph.correlations)
    
    return resolved


# =============================================================================
# AUTOPOIETIC REFINEMENT
# =============================================================================

class RefinementAction(Enum):
    BRIDGE_GAPS = "R1"      # Add edges to increase density
    COMPRESS = "R2"         # Merge structurally equivalent nodes
    EXPAND = "R3"           # Create meta-nodes for clusters
    REPAIR = "R4"           # Local restructuring


@dataclass
class Violation:
    """Invariant violation with remediation suggestion."""
    type: str
    metric: str
    value: float
    threshold: float
    severity: str  # CRITICAL, MAJOR, MINOR
    
    def suggested_action(self) -> RefinementAction:
        if self.metric in ("η", "φ"):
            return RefinementAction.BRIDGE_GAPS
        elif self.metric == "redundancy":
            return RefinementAction.COMPRESS
        elif self.metric == "cluster_size":
            return RefinementAction.EXPAND
        return RefinementAction.REPAIR


class AutopoieticEngine:
    """
    Incremental self-refinement engine.
    
    Triggers on invariant violations, applies bounded refinements.
    """
    
    def __init__(self, graph: nSHG, max_refinements: int = 10):
        self.graph = graph
        self.max_refinements = max_refinements
        self.refinement_count = 0
    
    def detect_violations(self) -> List[Violation]:
        """Check invariants, return violations."""
        violations = []
        
        if self.graph.eta < nSHG.ETA_THRESHOLD:
            violations.append(Violation(
                type="TOPOLOGY", metric="η",
                value=self.graph.eta, threshold=nSHG.ETA_THRESHOLD,
                severity="CRITICAL"
            ))
        
        if self.graph.phi > nSHG.PHI_THRESHOLD:
            violations.append(Violation(
                type="TOPOLOGY", metric="φ",
                value=self.graph.phi, threshold=nSHG.PHI_THRESHOLD,
                severity="MAJOR"
            ))
        
        return violations
    
    def apply_bridge_gaps(self) -> bool:
        """R1: Connect low-degree nodes to high-degree nodes."""
        degrees = {nid: self.graph.degree(nid) for nid in self.graph.nodes}
        low_degree = [nid for nid, d in degrees.items() if d < 2]
        high_degree = sorted(
            [nid for nid, d in degrees.items() if d >= 4],
            key=lambda x: degrees[x],
            reverse=True
        )[:5]
        
        if not low_degree or not high_degree:
            return False
        
        bridged = False
        for low in low_degree[:5]:
            for high in high_degree:
                if low != high:
                    try:
                        self.graph.add_edge(Edge(
                            source=low, target=high,
                            label="bridged", weight=0.5
                        ))
                        logger.info(f"Bridged {low} -> {high}")
                        bridged = True
                        break
                    except Exception:
                        continue
        
        return bridged
    
    def apply_compress(self) -> bool:
        """R2: Merge nodes with identical neighborhoods."""
        from collections import defaultdict
        
        neighborhoods = defaultdict(list)
        for nid in self.graph.nodes:
            neighbors = frozenset(self.graph.neighbors(nid))
            neighborhoods[neighbors].append(nid)
        
        merged = False
        for equiv_class in neighborhoods.values():
            if len(equiv_class) > 1:
                keep = equiv_class[0]
                for remove in equiv_class[1:]:
                    self._merge_nodes(keep, remove)
                    merged = True
        
        return merged
    
    def _merge_nodes(self, keep: str, remove: str) -> None:
        """Merge 'remove' into 'keep'."""
        # Update edges
        new_edges = {}
        for eid, edge in self.graph.edges.items():
            new_source = keep if edge.source == remove else edge.source
            new_target = keep if edge.target == remove else edge.target
            if new_source != new_target:
                new_edge = Edge(new_source, new_target, edge.label, edge.weight)
                new_edges[new_edge.id] = new_edge
        
        self.graph.edges = new_edges
        del self.graph.nodes[remove]
        logger.info(f"Merged {remove} into {keep}")
    
    def cycle(self) -> bool:
        """Run one refinement cycle. Returns True if changes made."""
        if self.refinement_count >= self.max_refinements:
            logger.warning("Max refinements reached")
            return False
        
        violations = self.detect_violations()
        if not violations:
            return False
        
        # Sort by severity
        severity_order = {"CRITICAL": 0, "MAJOR": 1, "MINOR": 2}
        violations.sort(key=lambda v: severity_order.get(v.severity, 3))
        
        top = violations[0]
        action = top.suggested_action()
        
        success = False
        if action == RefinementAction.BRIDGE_GAPS:
            success = self.apply_bridge_gaps()
        elif action == RefinementAction.COMPRESS:
            success = self.apply_compress()
        
        if success:
            self.refinement_count += 1
        
        return success
    
    def converge(self, max_cycles: int = 10) -> nSHG:
        """Run cycles until convergence."""
        for i in range(max_cycles):
            if not self.cycle():
                logger.info(f"Converged after {i+1} cycles")
                break
        return self.graph


# =============================================================================
# MAIN WORKFLOW: λΩ.τ
# =============================================================================

@dataclass
class MEGAHolon:
    """Output structure: a validated, resolved MEGA subgraph."""
    graph: nSHG
    level: EscalationLevel
    query: str
    resolution_context: Optional[QueryContext] = None
    strategic_summary: Optional[str] = None
    tactical_approach: Optional[str] = None
    operational_steps: Optional[List[str]] = None


def mega_process(
    query: str,
    initial_nodes: List[Node],
    initial_edges: List[Edge],
    polysemous: Optional[List[PolysemousNode]] = None,
    max_refinements: int = 10
) -> MEGAHolon:
    """
    Main MEGA workflow: λΩ.τ
    
    Query → Validated Holon
    
    Implements Pareto-governed complexity escalation:
    start simple, add complexity only when invariants fail.
    """
    
    # Φ1: BUILD initial graph
    graph = nSHG()
    for node in initial_nodes:
        graph.add_node(node)
    for edge in initial_edges:
        graph.add_edge(edge)
    
    logger.info(f"Initial graph: |V|={len(graph.nodes)}, |E|={len(graph.edges)}")
    
    # Φ2: ASSESS complexity level needed
    level, reasons = assess_escalation(graph)
    logger.info(f"Escalation level: {level.name}")
    for reason in reasons:
        logger.info(f"  - {reason}")
    
    # Φ3: VALIDATE initial state
    violations = graph.validate()
    
    # Φ4: REFINE if needed
    if violations:
        logger.info(f"Violations found: {violations}")
        engine = AutopoieticEngine(graph, max_refinements)
        graph = engine.converge()
        
        # Re-validate
        violations = graph.validate()
        if violations:
            logger.warning(f"Residual violations: {violations}")
    
    # Φ5: DECOHERE for query
    resolved = decohere(graph, query, polysemous)
    context = QueryContext.from_query(query)
    
    # Φ6: SYNTHESIZE holon
    holon = MEGAHolon(
        graph=resolved,
        level=level,
        query=query,
        resolution_context=context
    )
    
    logger.info(f"Output: level={level.name}, η={resolved.eta:.2f}, φ={resolved.phi:.2f}")
    
    return holon


# =============================================================================
# EXAMPLE / TEST
# =============================================================================

def example_usage():
    """Demonstrate MEGA workflow."""
    
    # Create sample nodes (cardiac output domain)
    nodes = [
        Node("CO", Level.ENTITY, attributes={
            "definition": UncertaintyTuple(0.95, 0.9, 0.9)
        }),
        Node("HR", Level.ENTITY),
        Node("SV", Level.ENTITY),
        Node("SVR", Level.ENTITY),
        Node("MAP", Level.ENTITY),
        Node("CVP", Level.ENTITY),
        Node("thermodilution", Level.ENTITY),
        Node("Fick", Level.ENTITY),
        Node("Stewart-Hamilton", Level.ENTITY),
        Node("CO_measurement", Level.GROUPING, 
             content=frozenset(["thermodilution", "Fick"])),
    ]
    
    # Create sample edges
    edges = [
        Edge("HR", "CO", "determines"),
        Edge("SV", "CO", "determines"),
        Edge("CO", "MAP", "contributes_to"),
        Edge("SVR", "MAP", "contributes_to"),
        Edge("thermodilution", "Stewart-Hamilton", "uses"),
        Edge("Fick", "CO", "measures"),
        Edge("thermodilution", "CO", "measures"),
        Edge("CO_measurement", "CO", "contains"),
        Edge("CO_measurement", "thermodilution", "contains"),
        Edge("CO_measurement", "Fick", "contains"),
    ]
    
    # Define polysemous nodes
    polysemous = [
        PolysemousNode("CO", [
            Interpretation("cardiac output", "hemodynamic", 0.9),
            Interpretation("carbon monoxide", "toxicology", 0.9),
        ])
    ]
    
    # Run MEGA process
    holon = mega_process(
        query="How is cardiac output measured using thermodilution?",
        initial_nodes=nodes,
        initial_edges=edges,
        polysemous=polysemous
    )
    
    print(f"\nResult:")
    print(f"  Level: {holon.level.name}")
    print(f"  Nodes: {len(holon.graph.nodes)}")
    print(f"  Edges: {len(holon.graph.edges)}")
    print(f"  η: {holon.graph.eta:.2f}")
    print(f"  φ: {holon.graph.phi:.2f}")
    print(f"  Valid: {holon.graph.is_valid()}")
    
    # Check resolution
    co_node = holon.graph.nodes.get("CO")
    if co_node and "_resolved_meaning" in co_node.metadata:
        print(f"  CO resolved to: {co_node.metadata['_resolved_meaning']}")


if __name__ == "__main__":
    example_usage()
