# MEGA v2.0 Endowments Reference
## Operationally Grounded Component Specifications

<overview>
Each endowment is defined with:
- **Mathematical specification**: Precise formal definition
- **Operational semantics**: What it means computationally
- **Implementation pattern**: How to realize in code
- **Validation criterion**: How to verify correctness
- **Failure mode**: What breaks and how to detect
</overview>

---

## 1. n-SUPERHYPERGRAPH (n-SHG)

<specification>
```
FORMAL DEFINITION
─────────────────
n-SHG = (V_n, E_n, ι, λ) where:

V_n = ∪_{k=0}^{n} V_k    Vertices across n+1 levels
V_0 ⊂ BaseSet            Ground level: atomic entities
V_{k+1} ⊆ P(V_k)         Level k+1: subsets of level k
  subject to: |v| > 1 for v ∈ V_{k+1}  (no trivial singletons)

E_n ⊆ V_n × V_n × Labels  Edges with labels
  subject to: ∃ cross-level edges  (levels connected)

ι : V_n → {0..n}         Level assignment function
λ : E_n → Labels         Edge labeling function

OPERATIONAL BOUNDS
──────────────────
n_max = 3                 Practical depth limit
|V_k| ≤ |V_{k-1}|^{1.5}  Subquadratic growth per level
|E_n| ≥ 4|V_n|           Density invariant
```
</specification>

<implementation>
```python
from dataclasses import dataclass, field
from typing import Set, Dict, Optional, FrozenSet
from enum import IntEnum

class Level(IntEnum):
    ENTITY = 0      # Atomic concepts
    GROUPING = 1    # Sets of entities (meta-entities)
    SCHEMA = 2      # Patterns across groupings
    PARADIGM = 3    # Organizing principles (rarely used)

@dataclass(frozen=True)
class Node:
    id: str
    level: Level
    content: Optional[FrozenSet[str]] = None  # IDs of contained nodes
    attributes: Dict[str, float] = field(default_factory=dict)
    
    def __hash__(self):
        return hash(self.id)

@dataclass
class Edge:
    source: str
    target: str
    label: str
    weight: float = 1.0
    
@dataclass
class nSHG:
    nodes: Dict[str, Node] = field(default_factory=dict)
    edges: Dict[str, Edge] = field(default_factory=dict)
    max_level: Level = Level.ENTITY
    
    def add_node(self, node: Node) -> None:
        if node.level > Level.PARADIGM:
            raise ValueError(f"Level {node.level} exceeds max (3)")
        
        # Validate level grounding
        if node.level > Level.ENTITY and node.content:
            for child_id in node.content:
                child = self.nodes.get(child_id)
                if child and child.level >= node.level:
                    raise ValueError(f"Level violation: {node.id} contains {child_id}")
        
        self.nodes[node.id] = node
        self.max_level = max(self.max_level, node.level)
    
    def add_edge(self, edge: Edge) -> None:
        if edge.source not in self.nodes or edge.target not in self.nodes:
            raise ValueError(f"Edge references missing node")
        self.edges[f"{edge.source}->{edge.target}"] = edge
    
    @property
    def eta(self) -> float:
        """Edge density η = |E|/|V|"""
        return len(self.edges) / max(len(self.nodes), 1)
    
    def nodes_at_level(self, level: Level) -> list[Node]:
        return [n for n in self.nodes.values() if n.level == level]
    
    def validate(self) -> list[str]:
        """Return list of validation violations."""
        violations = []
        
        # Check η ≥ 4
        if self.eta < 4:
            violations.append(f"η={self.eta:.2f} < 4")
        
        # Check level grounding
        for node in self.nodes.values():
            if node.level > Level.ENTITY:
                has_grounding = any(
                    e.target == node.id 
                    for e in self.edges.values()
                    if self.nodes[e.source].level < node.level
                )
                if not has_grounding:
                    violations.append(f"Node {node.id} at L{node.level} ungrounded")
        
        # Check growth bounds
        for level in range(1, self.max_level + 1):
            count_k = len(self.nodes_at_level(Level(level)))
            count_k1 = len(self.nodes_at_level(Level(level - 1)))
            if count_k > count_k1 ** 1.5:
                violations.append(f"Level {level} exceeds growth bound")
        
        return violations
```
</implementation>

<validation>
```python
def validate_n_shg(shg: nSHG) -> ValidationResult:
    violations = shg.validate()
    
    return ValidationResult(
        valid=len(violations) == 0,
        violations=violations,
        remediation=[
            "For η < 4: Use infranodus.getGraphAndAdvice(optimize='gaps')",
            "For ungrounded: Add cross-level containment edges",
            "For growth violation: Merge redundant nodes at high levels"
        ] if violations else []
    )
```
</validation>

---

## 2. PLITHOGENIC ATTRIBUTES (Grounded)

<specification>
```
FORMAL DEFINITION
─────────────────
Π : (Element × Attribute) → UncertaintyTuple

UncertaintyTuple = (confidence, coverage, source_quality)
  confidence ∈ [0, 1]     Epistemic certainty
  coverage ∈ [0, 1]       Fraction of attribute space addressed
  source_quality ∈ [0, 1] Reliability of evidence source

COMPOSITION (meet/join)
───────────────────────
Π₁ ∧ Π₂ = (min(c₁,c₂), min(v₁,v₂), min(q₁,q₂))  conjunction
Π₁ ∨ Π₂ = (max(c₁,c₂), max(v₁,v₂), max(q₁,q₂))  disjunction
¬Π = (1-c, v, q)                                   negation

CONTRADICTION DETECTION
───────────────────────
contradict(Π₁, Π₂) ⟺ same_subject ∧ |c₁ - c₂| > 0.5 ∧ min(q₁,q₂) > 0.6
```
</specification>

<grounding_heuristics>
```python
# Source quality calibration (based on typical reliability)
SOURCE_QUALITY = {
    # Medical/scientific
    "cochrane_review": 0.95,
    "meta_analysis": 0.92,
    "rct": 0.88,
    "cohort_study": 0.80,
    "case_series": 0.65,
    "expert_opinion": 0.55,
    
    # Educational
    "examiner_report": 0.95,  # CICM/ANZCA
    "textbook": 0.85,
    "review_article": 0.80,
    "lecture_notes": 0.70,
    
    # General
    "peer_reviewed": 0.85,
    "reputable_news": 0.70,
    "web_search": 0.50,
    "llm_inference": 0.40,
    "speculation": 0.20,
}

# Confidence calibration
def calibrate_confidence(
    source_type: str,
    consensus_level: float,  # 0-1, how many sources agree
    recency_years: float     # how old is the evidence
) -> float:
    """
    Compute calibrated confidence.
    """
    base = SOURCE_QUALITY.get(source_type, 0.5)
    
    # Consensus multiplier: 0.8-1.2
    consensus_mult = 0.8 + 0.4 * consensus_level
    
    # Recency decay: exp(-0.1 * years) for fast-changing fields
    recency_mult = math.exp(-0.1 * recency_years)
    
    # Combine with ceiling
    return min(base * consensus_mult * recency_mult, 0.99)
```
</grounding_heuristics>

<implementation>
```python
@dataclass
class PlithoAttribute:
    name: str
    confidence: float  # [0, 1]
    coverage: float    # [0, 1]  
    source_quality: float  # [0, 1]
    sources: list[str] = field(default_factory=list)
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        for val, name in [(self.confidence, 'confidence'), 
                          (self.coverage, 'coverage'),
                          (self.source_quality, 'source_quality')]:
            if not 0 <= val <= 1:
                raise ValueError(f"{name} must be in [0, 1], got {val}")
    
    def __and__(self, other: 'PlithoAttribute') -> 'PlithoAttribute':
        """Conjunction: meet operation."""
        return PlithoAttribute(
            name=f"({self.name} ∧ {other.name})",
            confidence=min(self.confidence, other.confidence),
            coverage=min(self.coverage, other.coverage),
            source_quality=min(self.source_quality, other.source_quality),
            sources=self.sources + other.sources
        )
    
    def __or__(self, other: 'PlithoAttribute') -> 'PlithoAttribute':
        """Disjunction: join operation."""
        return PlithoAttribute(
            name=f"({self.name} ∨ {other.name})",
            confidence=max(self.confidence, other.confidence),
            coverage=max(self.coverage, other.coverage),
            source_quality=max(self.source_quality, other.source_quality),
            sources=self.sources + other.sources
        )
    
    def __invert__(self) -> 'PlithoAttribute':
        """Negation."""
        return PlithoAttribute(
            name=f"¬{self.name}",
            confidence=1 - self.confidence,
            coverage=self.coverage,
            source_quality=self.source_quality,
            sources=self.sources
        )
    
    def contradicts(self, other: 'PlithoAttribute') -> bool:
        """Check if two attributes contradict."""
        return (
            abs(self.confidence - other.confidence) > 0.5 and
            min(self.source_quality, other.source_quality) > 0.6
        )
    
    def resolve_with(self, other: 'PlithoAttribute') -> 'PlithoAttribute':
        """Resolve contradiction, preferring higher quality source."""
        if self.source_quality > other.source_quality:
            return self
        elif other.source_quality > self.source_quality:
            return other
        else:
            # Equal quality: average with reduced confidence
            return PlithoAttribute(
                name=f"resolved({self.name}, {other.name})",
                confidence=(self.confidence + other.confidence) / 2 * 0.7,
                coverage=max(self.coverage, other.coverage),
                source_quality=min(self.source_quality, other.source_quality),
                sources=self.sources + other.sources
            )
```
</implementation>

---

## 3. CORRELATION MATRIX (Operational Entanglement)

<specification>
```
FORMAL DEFINITION
─────────────────
Ψ : V × V → [-1, 1]

Ψ(i, j) = correlation between update histories of i and j
  Ψ = +1: Perfect positive correlation (always co-update)
  Ψ = 0:  Independent
  Ψ = -1: Perfect negative correlation (inverse updates)

STORAGE
───────
Sparse representation: only |Ψ(i,j)| > threshold stored
Default threshold: 0.5

PROPAGATION RULE
────────────────
When node i updated:
  For each j where |Ψ(i,j)| > 0.7:
    flag_for_review(j, change_type=sign(Ψ(i,j)))
```
</specification>

<implementation>
```python
from scipy.sparse import lil_matrix
import numpy as np

@dataclass
class CorrelationMatrix:
    size: int
    threshold: float = 0.5
    propagation_threshold: float = 0.7
    _matrix: lil_matrix = field(init=False)
    _id_to_index: Dict[str, int] = field(default_factory=dict)
    _index_to_id: Dict[int, str] = field(default_factory=dict)
    
    def __post_init__(self):
        self._matrix = lil_matrix((self.size, self.size))
    
    def register_node(self, node_id: str) -> int:
        if node_id not in self._id_to_index:
            idx = len(self._id_to_index)
            self._id_to_index[node_id] = idx
            self._index_to_id[idx] = node_id
        return self._id_to_index[node_id]
    
    def set_correlation(self, id_a: str, id_b: str, value: float) -> None:
        if not -1 <= value <= 1:
            raise ValueError(f"Correlation must be in [-1, 1], got {value}")
        
        if abs(value) < self.threshold:
            return  # Don't store weak correlations
        
        i = self.register_node(id_a)
        j = self.register_node(id_b)
        
        # Symmetric
        self._matrix[i, j] = value
        self._matrix[j, i] = value
    
    def get_correlation(self, id_a: str, id_b: str) -> float:
        i = self._id_to_index.get(id_a)
        j = self._id_to_index.get(id_b)
        if i is None or j is None:
            return 0.0
        return self._matrix[i, j]
    
    def propagation_targets(self, node_id: str) -> list[tuple[str, float]]:
        """Get nodes that should be flagged when node_id is updated."""
        i = self._id_to_index.get(node_id)
        if i is None:
            return []
        
        targets = []
        row = self._matrix.getrow(i).toarray()[0]
        for j, val in enumerate(row):
            if abs(val) > self.propagation_threshold:
                targets.append((self._index_to_id[j], val))
        
        return targets
    
    def update_from_history(
        self, 
        update_log: list[tuple[str, datetime]]
    ) -> None:
        """Learn correlations from update co-occurrence."""
        from collections import defaultdict
        
        # Group updates by time window (e.g., 1 hour)
        windows = defaultdict(set)
        for node_id, timestamp in update_log:
            window_key = timestamp.replace(minute=0, second=0)
            windows[window_key].add(node_id)
        
        # Count co-occurrences
        cooccur = defaultdict(int)
        occur = defaultdict(int)
        
        for window, nodes in windows.items():
            for node in nodes:
                occur[node] += 1
                for other in nodes:
                    if node != other:
                        cooccur[(min(node, other), max(node, other))] += 1
        
        # Compute correlations (simplified Jaccard)
        for (a, b), count in cooccur.items():
            jaccard = count / (occur[a] + occur[b] - count)
            if jaccard > self.threshold:
                self.set_correlation(a, b, jaccard)
```
</implementation>

---

## 4. QUERY-TIME MATERIALIZATION (Operational Decoherence)

<specification>
```
FORMAL DEFINITION
─────────────────
Γ : (Ω_lazy, Query) → Ω_resolved

Ω_lazy: Graph with unresolved ambiguities
  - Polysemous nodes (multiple interpretations)
  - Conditional edges (active only in certain contexts)
  - Underspecified attributes

Query: Context-providing request
  - Domain markers
  - Disambiguation cues
  - Scope constraints

Ω_resolved: Fully materialized graph for this query

OPERATIONS
──────────
resolve_polysemy(node, context) → interpretation
activate_conditionals(edges, context) → active_subset
specialize_attributes(attributes, context) → specific_values
```
</specification>

<implementation>
```python
from dataclasses import dataclass
from typing import Optional, Callable
from enum import Enum

class ResolutionStrategy(Enum):
    SEMANTIC_SIMILARITY = "semantic"
    CONTEXT_FREQUENCY = "frequency"
    EXPLICIT_MARKER = "marker"
    DOMAIN_DEFAULT = "domain"

@dataclass
class Interpretation:
    meaning: str
    domain: str
    confidence: float
    
@dataclass
class PolysemousNode:
    id: str
    interpretations: list[Interpretation]
    
    def resolve(self, context: 'QueryContext') -> str:
        """Resolve to best interpretation for context."""
        if not self.interpretations:
            return self.id
        
        # Strategy 1: Explicit domain marker
        for interp in self.interpretations:
            if interp.domain == context.domain:
                return interp.meaning
        
        # Strategy 2: Semantic similarity
        best = max(
            self.interpretations,
            key=lambda i: context.semantic_similarity(i.meaning)
        )
        return best.meaning

@dataclass
class ConditionalEdge:
    source: str
    target: str
    condition: Callable[['QueryContext'], bool]
    label: str
    
    def is_active(self, context: 'QueryContext') -> bool:
        return self.condition(context)

@dataclass  
class QueryContext:
    query_text: str
    domain: Optional[str] = None
    scope: Optional[str] = None
    temporal_focus: Optional[str] = None
    
    def semantic_similarity(self, text: str) -> float:
        """Compute semantic similarity to query. Stub for actual embedding."""
        # In practice: use sentence embeddings
        words_query = set(self.query_text.lower().split())
        words_text = set(text.lower().split())
        if not words_query or not words_text:
            return 0.0
        return len(words_query & words_text) / len(words_query | words_text)
    
    @classmethod
    def from_query(cls, query: str) -> 'QueryContext':
        """Extract context from query string."""
        context = cls(query_text=query)
        
        # Domain detection (simple keyword matching)
        domains = {
            "hemodynamic": ["cardiac", "CO", "SVR", "heart", "flow"],
            "respiratory": ["ventilation", "oxygen", "FiO2", "PEEP"],
            "toxicology": ["poison", "overdose", "toxin"],
            "pharmacology": ["drug", "dose", "pharmacokinetics"],
        }
        for domain, keywords in domains.items():
            if any(kw.lower() in query.lower() for kw in keywords):
                context.domain = domain
                break
        
        return context

def decohere(
    shg: nSHG, 
    query: str,
    polysemous_nodes: list[PolysemousNode],
    conditional_edges: list[ConditionalEdge]
) -> nSHG:
    """
    Materialize lazy graph for specific query.
    """
    context = QueryContext.from_query(query)
    
    # Create resolved copy
    resolved = nSHG()
    
    # Resolve polysemous nodes
    resolved_meanings = {}
    for poly in polysemous_nodes:
        resolved_meanings[poly.id] = poly.resolve(context)
    
    # Copy nodes with resolved meanings
    for node_id, node in shg.nodes.items():
        if node_id in resolved_meanings:
            new_node = Node(
                id=node_id,
                level=node.level,
                content=node.content,
                attributes={**node.attributes, 
                           '_resolved_meaning': resolved_meanings[node_id]}
            )
        else:
            new_node = node
        resolved.add_node(new_node)
    
    # Filter edges based on conditions
    for edge_id, edge in shg.edges.items():
        # Check if this edge has a condition
        conditional = next(
            (ce for ce in conditional_edges 
             if ce.source == edge.source and ce.target == edge.target),
            None
        )
        
        if conditional is None or conditional.is_active(context):
            resolved.add_edge(edge)
    
    return resolved
```
</implementation>

---

## 5. AUTOPOIETIC REFINEMENT

<specification>
```
FORMAL DEFINITION
─────────────────
Δ : (Ω, Environment, Violations) → Ω'

Refinement triggers:
  T1: η < 4 after insertion
  T2: Modularity increase > 0.05 (new cluster detected)
  T3: φ increases (orphan creation)
  T4: Contradiction detected

Refinement actions:
  R1: Bridge gaps (via infranodus integration)
  R2: Compress redundancy (bisimulation quotient)
  R3: Expand abstraction (meta-node creation)
  R4: Repair violations (local restructuring)

BOUNDS
──────
max_refinements_per_trigger = 10
max_growth_per_cycle = 1.2x
convergence_threshold = 0.02 (relative change)
```
</specification>

<implementation>
```python
from enum import Enum
from typing import Optional
import logging

class RefinementAction(Enum):
    BRIDGE_GAPS = "R1"
    COMPRESS = "R2"
    EXPAND = "R3"
    REPAIR = "R4"

@dataclass
class Violation:
    type: str
    metric: str
    value: float
    threshold: float
    severity: str  # CRITICAL, MAJOR, MINOR
    
    def suggested_action(self) -> RefinementAction:
        if self.metric == "η" and self.value < self.threshold:
            return RefinementAction.BRIDGE_GAPS
        elif self.metric == "φ" and self.value > self.threshold:
            return RefinementAction.BRIDGE_GAPS
        elif self.metric == "redundancy":
            return RefinementAction.COMPRESS
        elif self.metric == "cluster_size":
            return RefinementAction.EXPAND
        else:
            return RefinementAction.REPAIR

class AutopoieticEngine:
    def __init__(self, shg: nSHG, max_refinements: int = 10):
        self.shg = shg
        self.max_refinements = max_refinements
        self.refinement_count = 0
        self.logger = logging.getLogger("autopoiesis")
    
    def detect_violations(self) -> list[Violation]:
        """Check all invariants and return violations."""
        violations = []
        
        # η check
        eta = self.shg.eta
        if eta < 4:
            violations.append(Violation(
                type="TOPOLOGY", metric="η",
                value=eta, threshold=4.0,
                severity="CRITICAL"
            ))
        
        # φ check
        isolated = sum(1 for n in self.shg.nodes.values() 
                      if not any(e.source == n.id or e.target == n.id 
                                for e in self.shg.edges.values()))
        phi = isolated / max(len(self.shg.nodes), 1)
        if phi > 0.2:
            violations.append(Violation(
                type="TOPOLOGY", metric="φ",
                value=phi, threshold=0.2,
                severity="MAJOR"
            ))
        
        return violations
    
    def apply_refinement(self, action: RefinementAction, violation: Violation) -> bool:
        """Apply single refinement action. Returns True if successful."""
        self.logger.info(f"Applying {action.value} for {violation.metric}")
        
        if action == RefinementAction.BRIDGE_GAPS:
            return self._bridge_gaps()
        elif action == RefinementAction.COMPRESS:
            return self._compress_redundancy()
        elif action == RefinementAction.EXPAND:
            return self._expand_abstraction()
        elif action == RefinementAction.REPAIR:
            return self._repair_violation(violation)
        
        return False
    
    def _bridge_gaps(self) -> bool:
        """R1: Add edges to increase density and reduce isolation."""
        # Find isolated or low-degree nodes
        degrees = {}
        for node_id in self.shg.nodes:
            degrees[node_id] = sum(
                1 for e in self.shg.edges.values()
                if e.source == node_id or e.target == node_id
            )
        
        low_degree = [nid for nid, d in degrees.items() if d < 2]
        if not low_degree:
            return False
        
        # Connect low-degree nodes to semantically similar high-degree nodes
        high_degree = sorted(
            [nid for nid, d in degrees.items() if d >= 4],
            key=lambda x: degrees[x],
            reverse=True
        )[:5]
        
        for low in low_degree[:5]:  # Limit per cycle
            if high_degree:
                target = high_degree[0]  # Simplified: should use semantic similarity
                self.shg.add_edge(Edge(
                    source=low, target=target,
                    label="bridged", weight=0.5
                ))
                self.logger.info(f"Bridged {low} -> {target}")
        
        return True
    
    def _compress_redundancy(self) -> bool:
        """R2: Merge structurally equivalent nodes."""
        # Simplified bisimulation: merge nodes with identical neighborhoods
        from collections import defaultdict
        
        neighborhoods = defaultdict(list)
        for node_id in self.shg.nodes:
            neighbors = frozenset(
                e.target if e.source == node_id else e.source
                for e in self.shg.edges.values()
                if e.source == node_id or e.target == node_id
            )
            neighborhoods[neighbors].append(node_id)
        
        merged = False
        for equiv_class in neighborhoods.values():
            if len(equiv_class) > 1:
                # Merge into first node
                keep = equiv_class[0]
                for remove in equiv_class[1:]:
                    self._merge_nodes(keep, remove)
                    merged = True
        
        return merged
    
    def _merge_nodes(self, keep: str, remove: str) -> None:
        """Merge 'remove' into 'keep'."""
        # Redirect edges
        edges_to_update = []
        for eid, edge in list(self.shg.edges.items()):
            if edge.source == remove or edge.target == remove:
                new_source = keep if edge.source == remove else edge.source
                new_target = keep if edge.target == remove else edge.target
                if new_source != new_target:  # Avoid self-loops
                    edges_to_update.append((eid, Edge(
                        source=new_source, target=new_target,
                        label=edge.label, weight=edge.weight
                    )))
                del self.shg.edges[eid]
        
        for eid, edge in edges_to_update:
            self.shg.edges[eid] = edge
        
        # Remove node
        del self.shg.nodes[remove]
        self.logger.info(f"Merged {remove} into {keep}")
    
    def _expand_abstraction(self) -> bool:
        """R3: Create meta-node for dense cluster."""
        # Find clusters (simplified: just look at high-degree nodes)
        # In practice: use community detection
        return False  # Placeholder
    
    def _repair_violation(self, violation: Violation) -> bool:
        """R4: Generic repair based on violation type."""
        self.logger.warning(f"Generic repair for {violation.type}:{violation.metric}")
        return False  # Placeholder for specific repairs
    
    def cycle(self) -> bool:
        """
        Run one autopoietic cycle.
        Returns True if changes were made.
        """
        if self.refinement_count >= self.max_refinements:
            self.logger.warning("Max refinements reached")
            return False
        
        violations = self.detect_violations()
        if not violations:
            self.logger.info("No violations, graph is stable")
            return False
        
        # Sort by severity
        severity_order = {"CRITICAL": 0, "MAJOR": 1, "MINOR": 2}
        violations.sort(key=lambda v: severity_order.get(v.severity, 3))
        
        # Apply refinement for most severe
        top_violation = violations[0]
        action = top_violation.suggested_action()
        
        success = self.apply_refinement(action, top_violation)
        if success:
            self.refinement_count += 1
        
        return success
    
    def converge(self, max_cycles: int = 10) -> nSHG:
        """Run refinement cycles until convergence."""
        for i in range(max_cycles):
            changed = self.cycle()
            if not changed:
                self.logger.info(f"Converged after {i+1} cycles")
                break
        
        return self.shg
```
</implementation>

---

## 6. SUMMARY: ENDOWMENT ACTIVATION

<activation_table>
```
ENDOWMENT          ACTIVATED WHEN               COST    TYPICAL USE
─────────────────────────────────────────────────────────────────────
n-SHG (n=1)        η < 3                        O(n)    Always
n-SHG (n=2)        Groupings needed             O(n²)   70% of cases
n-SHG (n=3)        Schemas required             O(n³)   15% of cases
Plithogenic        Structured uncertainty       O(1)    When multi-source
Correlation        Co-update patterns exist     O(n²)   For maintenance
Decoherence        Polysemy present            O(k)    At query time
Autopoiesis        Invariant violation         O(n)    Periodic refresh
─────────────────────────────────────────────────────────────────────
Full MEGA (Ω)      All triggers active         O(n³)   <5% of cases
```
</activation_table>
