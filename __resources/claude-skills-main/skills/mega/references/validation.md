# MEGA v2.0 Validation Reference
## Operationally Grounded Constraint Enforcement

<overview>
Validation in MEGA v2.0 follows the Pareto principle: check essential invariants first, escalate complexity only when simple checks fail. The framework combines topology invariants (mandatory), KROG governance (for operations), and structural constraints (level-specific).
</overview>

---

## 1. TOPOLOGY INVARIANTS (MANDATORY)

<primary_invariants>
```
ESSENTIAL CHECKS — Run on every operation
─────────────────────────────────────────

η = |E|/|V| ≥ 4.0          Edge density
  WHY: Below 4, graph lacks sufficient connectivity for 
       small-world properties and meaningful traversal.
  REMEDIATION: R1 (bridge_gaps) via infranodus integration

φ = |isolated|/|V| < 0.2   Isolation ratio
  WHY: Orphan nodes fragment knowledge, prevent integration.
  REMEDIATION: R1 (bridge_gaps) or prune isolated nodes

κ > 0.3                     Clustering coefficient (recommended)
  WHY: Indicates meaningful local structure, not random graph.
  REMEDIATION: R3 (expand abstraction) to create bridging meta-nodes

ζ = 0                       Acyclicity (DAG mode only)
  WHY: Required for causal reasoning, topological sort.
  REMEDIATION: R4 (repair) to break cycles via edge removal
```
</primary_invariants>

<implementation>
```python
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class Severity(Enum):
    CRITICAL = 0  # Must fix before any operation
    MAJOR = 1     # Should fix, operations may fail
    MINOR = 2     # Recommended fix, degrades quality
    INFO = 3      # Advisory only

@dataclass
class Violation:
    type: str           # TOPOLOGY, STRUCTURAL, GOVERNANCE
    metric: str         # η, φ, κ, etc.
    value: float        # Current value
    threshold: float    # Required value
    severity: Severity
    message: str
    remediation: str    # Suggested fix
    
    def __str__(self):
        return f"[{self.severity.name}] {self.type}:{self.metric}={self.value:.2f} (threshold: {self.threshold})"

def validate_topology(graph) -> List[Violation]:
    """
    Check essential topology invariants.
    Returns list of violations, empty if valid.
    """
    violations = []
    
    # η: Edge density
    eta = len(graph.edges) / max(len(graph.nodes), 1)
    if eta < 4.0:
        violations.append(Violation(
            type="TOPOLOGY",
            metric="η",
            value=eta,
            threshold=4.0,
            severity=Severity.CRITICAL,
            message=f"Edge density {eta:.2f} below minimum 4.0",
            remediation="Apply R1: bridge_gaps() or infranodus.getGraphAndAdvice(optimize='gaps')"
        ))
    
    # φ: Isolation ratio
    connected = set()
    for edge in graph.edges.values():
        connected.add(edge.source)
        connected.add(edge.target)
    isolated = len(graph.nodes) - len(connected)
    phi = isolated / max(len(graph.nodes), 1)
    
    if phi > 0.2:
        violations.append(Violation(
            type="TOPOLOGY",
            metric="φ",
            value=phi,
            threshold=0.2,
            severity=Severity.MAJOR,
            message=f"Isolation ratio {phi:.2f} exceeds maximum 0.2 ({isolated} orphan nodes)",
            remediation="Apply R1: connect orphans to semantically similar nodes"
        ))
    
    # κ: Clustering coefficient (simplified)
    if len(graph.nodes) >= 3:
        triangles = 0
        triples = 0
        for node_id in graph.nodes:
            neighbors = graph.neighbors(node_id)
            n = len(neighbors)
            if n >= 2:
                triples += n * (n - 1) / 2
                # Count actual triangles
                for i, n1 in enumerate(neighbors):
                    for n2 in list(neighbors)[i+1:]:
                        if graph.has_edge(n1, n2):
                            triangles += 1
        
        kappa = (3 * triangles / triples) if triples > 0 else 0
        
        if kappa < 0.3:
            violations.append(Violation(
                type="TOPOLOGY",
                metric="κ",
                value=kappa,
                threshold=0.3,
                severity=Severity.MINOR,
                message=f"Clustering coefficient {kappa:.2f} below recommended 0.3",
                remediation="Apply R3: create bridging meta-nodes for clusters"
            ))
    
    return violations
```
</implementation>

---

## 2. STRUCTURAL INVARIANTS (LEVEL-SPECIFIC)

<level_constraints>
```
n-SHG STRUCTURAL CONSTRAINTS
────────────────────────────

WELL-FOUNDEDNESS
  ∀v ∈ V: level(v) = 0 ∨ ∃u ∈ V: level(u) < level(v) ∧ connected(u, v)
  
  Every non-ground node must have grounding at lower level.
  WHY: Prevents "floating" abstractions disconnected from reality.

GROWTH BOUNDS  
  |V_k| ≤ |V_{k-1}|^{1.5}  for k ∈ {1, 2, 3}
  
  Higher levels grow subquadratically.
  WHY: Prevents combinatorial explosion, ensures tractability.

CONTAINMENT CONSISTENCY
  ∀v ∈ V_{k+1}, ∀u ∈ contents(v): level(u) = k
  
  Meta-nodes contain only nodes from immediately lower level.
  WHY: Clean hierarchy, no skip-level containment.

BOUNDED DEPTH
  max(level(v)) ≤ 3 for all v ∈ V
  
  WHY: n > 3 rarely justified; signals over-abstraction.
  REMEDIATION: Split domain rather than adding levels.
```
</level_constraints>

<implementation>
```python
def validate_structure(graph) -> List[Violation]:
    """
    Check n-SHG structural invariants.
    """
    violations = []
    
    # Well-foundedness check
    for node in graph.nodes.values():
        if node.level > 0:
            has_grounding = False
            
            # Check edges
            for edge in graph.edges.values():
                if edge.target == node.id:
                    source = graph.nodes.get(edge.source)
                    if source and source.level < node.level:
                        has_grounding = True
                        break
                if edge.source == node.id:
                    target = graph.nodes.get(edge.target)
                    if target and target.level < node.level:
                        has_grounding = True
                        break
            
            # Check containment
            if not has_grounding and node.content:
                for child_id in node.content:
                    if child_id in graph.nodes:
                        has_grounding = True
                        break
            
            if not has_grounding:
                violations.append(Violation(
                    type="STRUCTURAL",
                    metric="well_founded",
                    value=node.level,
                    threshold=0,
                    severity=Severity.MAJOR,
                    message=f"Node {node.id}@L{node.level} has no grounding at lower level",
                    remediation="Add cross-level edge or containment, or demote to L0"
                ))
    
    # Growth bound check
    level_counts = {}
    for node in graph.nodes.values():
        level_counts[node.level] = level_counts.get(node.level, 0) + 1
    
    for k in range(1, 4):
        if k in level_counts and (k-1) in level_counts:
            max_allowed = level_counts[k-1] ** 1.5
            if level_counts[k] > max_allowed:
                violations.append(Violation(
                    type="STRUCTURAL",
                    metric="growth_bound",
                    value=level_counts[k],
                    threshold=max_allowed,
                    severity=Severity.MINOR,
                    message=f"Level {k} has {level_counts[k]} nodes, exceeds bound {max_allowed:.0f}",
                    remediation="Merge redundant nodes at level {k} via R2: compress"
                ))
    
    # Bounded depth check
    max_level = max((n.level for n in graph.nodes.values()), default=0)
    if max_level > 3:
        violations.append(Violation(
            type="STRUCTURAL",
            metric="max_depth",
            value=max_level,
            threshold=3,
            severity=Severity.CRITICAL,
            message=f"Graph depth {max_level} exceeds maximum 3",
            remediation="Split domain into separate graphs; do not exceed n=3"
        ))
    
    return violations
```
</implementation>

---

## 3. UNCERTAINTY INVARIANTS

<plithogenic_constraints>
```
GROUNDED UNCERTAINTY BOUNDS
───────────────────────────

RANGE BOUNDS
  ∀x,a: Π(x,a) = (c, v, q) ∈ [0,1]³
  
  All uncertainty components in unit interval.

COMPOSITION CONSISTENCY
  (Π₁ ∧ Π₂).confidence ≤ min(Π₁.confidence, Π₂.confidence)
  (Π₁ ∨ Π₂).confidence ≥ max(Π₁.confidence, Π₂.confidence)
  
  Meet/join operations respect lattice structure.

SOURCE QUALITY COHERENCE
  high_quality_source ⟹ confidence ≤ source_quality + 0.1
  
  Cannot be more confident than source reliability allows.
```
</plithogenic_constraints>

<implementation>
```python
def validate_uncertainty(graph) -> List[Violation]:
    """
    Check plithogenic attribute bounds.
    """
    violations = []
    
    for node in graph.nodes.values():
        for attr_name, attr in node.attributes.items():
            # Range bounds
            for component in ['confidence', 'coverage', 'source_quality']:
                value = getattr(attr, component)
                if not 0 <= value <= 1:
                    violations.append(Violation(
                        type="UNCERTAINTY",
                        metric=f"{component}_bound",
                        value=value,
                        threshold=1.0,
                        severity=Severity.CRITICAL,
                        message=f"Node {node.id}.{attr_name}.{component}={value} outside [0,1]",
                        remediation="Clamp value to [0, 1]"
                    ))
            
            # Source quality coherence
            if attr.confidence > attr.source_quality + 0.1:
                violations.append(Violation(
                    type="UNCERTAINTY",
                    metric="source_coherence",
                    value=attr.confidence,
                    threshold=attr.source_quality + 0.1,
                    severity=Severity.MINOR,
                    message=f"Node {node.id}.{attr_name}: confidence {attr.confidence:.2f} exceeds source quality {attr.source_quality:.2f}",
                    remediation="Reduce confidence to match source reliability"
                ))
    
    return violations
```
</implementation>

---

## 4. KROG GOVERNANCE (FOR OPERATIONS)

<krog_framework>
```
KROG VALIDITY THEOREM
─────────────────────
Valid(λ) ⟺ K(λ) ∧ R(λ) ∧ O(λ) ∧ G(λ)

K (Knowable):     Effects visible, auditable, traceable
R (Rights):       Agent has Hohfeldian position for operation
O (Obligations):  No duties violated by operation
G (Governance):   Within meta-bounds of system

WHEN TO CHECK KROG
──────────────────
KROG validation applies to OPERATIONS, not structures.
Use for:
  - Autopoietic refinements (R1-R4)
  - External integrations (InfraNodus, Obsidian)
  - User-facing queries that modify state
  
Skip for:
  - Read-only queries
  - Internal topology checks
  - Decoherence (query-time materialization)
```
</krog_framework>

<implementation>
```python
from dataclasses import dataclass
from typing import Set
from enum import Enum

class HohfeldPosition(Enum):
    CLAIM = "claim"           # Right to X → other has duty
    PRIVILEGE = "privilege"   # May X → other has no-right
    POWER = "power"           # Can change X → other liable
    IMMUNITY = "immunity"     # Cannot be changed → other disabled

class OperationType(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    GOVERN = "govern"

# Position requirements by operation type
POSITION_REQUIREMENTS = {
    OperationType.READ: {HohfeldPosition.PRIVILEGE},
    OperationType.WRITE: {HohfeldPosition.POWER},
    OperationType.DELETE: {HohfeldPosition.POWER, HohfeldPosition.CLAIM},
    OperationType.GOVERN: {HohfeldPosition.IMMUNITY},
}

@dataclass
class Agent:
    id: str
    positions: Set[HohfeldPosition]

@dataclass  
class Operation:
    type: OperationType
    agent: Agent
    target: str
    rationale: str
    logged: bool = True

def validate_krog(operation: Operation) -> List[Violation]:
    """
    Validate operation against KROG constraints.
    """
    violations = []
    
    # K: Knowable
    if not operation.logged:
        violations.append(Violation(
            type="GOVERNANCE",
            metric="K_knowable",
            value=0,
            threshold=1,
            severity=Severity.MAJOR,
            message=f"Operation {operation.type.value} not logged",
            remediation="Enable logging for all state-changing operations"
        ))
    
    if not operation.rationale:
        violations.append(Violation(
            type="GOVERNANCE",
            metric="K_traceable",
            value=0,
            threshold=1,
            severity=Severity.MINOR,
            message=f"Operation {operation.type.value} lacks rationale",
            remediation="Provide rationale for audit trail"
        ))
    
    # R: Rights
    required = POSITION_REQUIREMENTS.get(operation.type, set())
    missing = required - operation.agent.positions
    
    if missing:
        violations.append(Violation(
            type="GOVERNANCE",
            metric="R_rights",
            value=len(operation.agent.positions),
            threshold=len(required),
            severity=Severity.CRITICAL,
            message=f"Agent {operation.agent.id} lacks positions {missing} for {operation.type.value}",
            remediation="Grant required positions or use different operation type"
        ))
    
    # O: Obligations — context-dependent, simplified here
    # G: Governance — bounds checking done in topology validation
    
    return violations
```
</implementation>

---

## 5. VALIDATION WORKFLOW

<complete_validation>
```python
@dataclass
class ValidationResult:
    valid: bool
    violations: List[Violation]
    summary: str
    
    @classmethod
    def from_violations(cls, violations: List[Violation]) -> 'ValidationResult':
        critical = [v for v in violations if v.severity == Severity.CRITICAL]
        major = [v for v in violations if v.severity == Severity.MAJOR]
        minor = [v for v in violations if v.severity == Severity.MINOR]
        
        valid = len(critical) == 0
        
        summary = f"Validation: {'PASS' if valid else 'FAIL'}\n"
        summary += f"  Critical: {len(critical)}\n"
        summary += f"  Major: {len(major)}\n"
        summary += f"  Minor: {len(minor)}\n"
        
        if not valid:
            summary += "\nBlocking issues:\n"
            for v in critical:
                summary += f"  - {v}\n"
        
        return cls(valid=valid, violations=violations, summary=summary)

def validate_mega(graph, operation: Optional[Operation] = None) -> ValidationResult:
    """
    Complete MEGA validation.
    
    Args:
        graph: nSHG structure to validate
        operation: Optional operation to KROG-validate
        
    Returns:
        ValidationResult with all violations and summary
    """
    all_violations = []
    
    # 1. Topology (mandatory, always run)
    all_violations.extend(validate_topology(graph))
    
    # 2. Structure (mandatory for n > 0)
    if graph.max_level > 0:
        all_violations.extend(validate_structure(graph))
    
    # 3. Uncertainty (if attributes present)
    has_attrs = any(n.attributes for n in graph.nodes.values())
    if has_attrs:
        all_violations.extend(validate_uncertainty(graph))
    
    # 4. KROG (only for operations)
    if operation:
        all_violations.extend(validate_krog(operation))
    
    return ValidationResult.from_violations(all_violations)
```
</complete_validation>

---

## 6. REMEDIATION REFERENCE

<remediation_table>
```
VIOLATION → REMEDIATION MAPPING
───────────────────────────────

TOPOLOGY
  η < 4.0        → R1: bridge_gaps()
                   infranodus.getGraphAndAdvice(optimize='gaps')
                   
  φ > 0.2        → R1: connect_orphans()
                   Find semantically similar nodes, add edges
                   
  κ < 0.3        → R3: expand_abstraction()
                   Create meta-nodes bridging clusters

STRUCTURAL
  ungrounded     → Add cross-level edge OR demote node to L0
  growth_bound   → R2: compress() merge redundant nodes
  max_depth > 3  → Split into separate domain graphs

UNCERTAINTY
  bound_violation → Clamp to [0, 1]
  source_coherence → Reduce confidence to match source

GOVERNANCE
  K_violation    → Enable logging, add rationale
  R_violation    → Grant positions or change operation type
  O_violation    → Fulfill duty or request exemption
  G_violation    → Operate within system bounds
```
</remediation_table>

---

## 7. QUICK REFERENCE

```
MEGA v2.0 VALIDATION
════════════════════

MANDATORY INVARIANTS
  η ≥ 4.0         Edge density
  φ < 0.2         Isolation ratio
  n ≤ 3           Max depth

SEVERITY LEVELS
  CRITICAL        Must fix, blocks operations
  MAJOR           Should fix, operations may fail
  MINOR           Recommended, degrades quality
  INFO            Advisory only

VALIDATION ORDER
  1. Topology     Always
  2. Structure    If n > 0
  3. Uncertainty  If attributes exist
  4. KROG         If operation provided

REMEDIATION ACTIONS
  R1: bridge_gaps     Add edges (η, φ violations)
  R2: compress        Merge nodes (growth violations)
  R3: expand          Create meta-nodes (κ violations)
  R4: repair          Local fixes (structural violations)
```
