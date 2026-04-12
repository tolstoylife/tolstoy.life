#!/usr/bin/env python3
"""
Non-Linear Reasoning Orchestrator v2.0

Implements Anthropic's orchestrator-worker pattern with:
- Effort scaling based on query complexity
- Parallel subagent execution with isolated contexts
- State persistence and checkpoint recovery
- NoisyGraph integration for uncertainty-aware reasoning

Usage:
    python orchestrator.py "<query>" [--mode full|compact|semantic|research] [--effort auto|simple|moderate|complex]

Based on Anthropic's multi-agent research system architecture (June 2025).
"""

import json
import asyncio
import hashlib
import os
from typing import Dict, List, Optional, Any, Set, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum, auto
from pathlib import Path
from uuid import uuid4

# ============================================================================
# Configuration
# ============================================================================

CHECKPOINT_DIR = Path("/home/claude/nlr_checkpoints")

DEFAULT_CONFIG = {
    "effort_levels": {
        "simple": {"subagents": 1, "max_tool_calls": 10, "iterations": 3, "checkpoint_interval": 3},
        "moderate": {"subagents": 3, "max_tool_calls": 30, "iterations": 5, "checkpoint_interval": 2},
        "complex": {"subagents": 7, "max_tool_calls": 100, "iterations": 9, "checkpoint_interval": 2}
    },
    "noise_budget": 0.25,
    "topology_target": 4.0,
    "max_nodes": 60,
    "max_edges": 240,
    "convergence_threshold": 0.95
}

# Domain detection keywords
DOMAIN_KEYWORDS = {
    'medical': ['diagnosis', 'treatment', 'symptom', 'disease', 'medication', 'clinical', 
                'patient', 'therapeutic', 'pathophysiology', 'pharmacology', 'ICU', 'anaesthesia',
                'cardiac', 'respiratory', 'hemodynamic'],
    'legal': ['law', 'regulation', 'compliance', 'statute', 'legal', 'court', 'contract'],
    'technical': ['algorithm', 'implementation', 'architecture', 'system', 'code', 'API'],
    'scientific': ['research', 'study', 'experiment', 'hypothesis', 'evidence', 'mechanism'],
    'financial': ['investment', 'market', 'financial', 'trading', 'portfolio', 'risk']
}

REASONING_INDICATORS = {
    'compare': 3, 'contrast': 3, 'analyze': 4, 'synthesize': 5,
    'evaluate': 4, 'mechanism': 4, 'pathway': 4, 'causation': 5,
    'why': 3, 'how does': 3
}

HIGH_STAKES_DOMAINS = {'medical', 'legal'}

# ============================================================================
# Enums
# ============================================================================

class Mode(Enum):
    FULL = "full"
    COMPACT = "compact"
    SEMANTIC = "semantic"
    RESEARCH = "research"

class EffortLevel(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    
    @classmethod
    def from_score(cls, score: float) -> 'EffortLevel':
        if score < 4:
            return cls.SIMPLE
        elif score < 8:
            return cls.MODERATE
        else:
            return cls.COMPLEX

class NodeType(Enum):
    ENTITY = "entity"
    CONCEPT = "concept"
    PROCESS = "process"
    DATASET = "dataset"
    CLAIM = "claim"
    PLACEHOLDER = "placeholder"

class EdgeType(Enum):
    CAUSES = "causes"
    CORRELATES_WITH = "correlates_with"
    IS_A = "is_a"
    PART_OF = "part_of"
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    SIMILAR_TO = "similar_to"

class Status(Enum):
    NEW = "new"
    UPDATED = "updated"
    UNCHANGED = "unchanged"
    REMOVED = "removed"

class ResearchState(Enum):
    INIT = auto()
    STRATEGY = auto()
    SPAWN_SUBAGENTS = auto()
    EXECUTE_PARALLEL = auto()
    INTEGRATE_RESULTS = auto()
    SELF_CORRECT = auto()
    CHECKPOINT = auto()
    SYNTHESIZE = auto()
    COMPLETE = auto()
    ERROR = auto()

class ExpectedSignal(Enum):
    CONFIRM = "confirm"
    DISCONFIRM = "disconfirm"
    DIFFERENTIATE = "differentiate"
    DISCOVER_GAP = "discover_gap"
    REFINE_CONFIDENCE = "refine_placeholder_confidence"
    NOISE_BUDGET = "select_for_noise_budget"

# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class Evidence:
    result_id: str
    note: str
    source_type: str = "unknown"
    confidence: float = 0.5

@dataclass
class Node:
    id: str
    label: str
    description: str
    type: NodeType
    confidence: float
    status: Status = Status.NEW
    constraints: List[str] = field(default_factory=list)
    evidence: List[Evidence] = field(default_factory=list)

@dataclass
class Edge:
    id: str
    source: str
    target: str
    type: EdgeType
    description: str
    strength: float
    status: Status = Status.NEW
    evidence: List[Evidence] = field(default_factory=list)

@dataclass
class EffortConfig:
    level: EffortLevel
    subagents: int
    max_tool_calls: int
    max_iterations: int
    checkpoint_interval: int

@dataclass
class SubagentConfig:
    id: str
    type: str
    priority: int
    required: bool
    tool_access: List[str]

@dataclass
class TaskAssignment:
    task_id: str
    subagent_id: str
    description: str
    output_schema: Dict[str, Any]
    tool_guidance: str
    boundaries: str
    completion_criteria: str
    allowed_tools: List[str]

@dataclass
class SubagentResult:
    task_id: str
    subagent_id: str
    output: Dict[str, Any]
    tool_calls_made: int
    confidence: float
    error: Optional[str] = None

@dataclass
class GraphQuestion:
    agent_id: str
    question: str
    why_this_question: str
    expected_signal: ExpectedSignal
    targets: Dict[str, List[str]]

@dataclass
class Meta:
    mode: str
    topic: str
    timestamp_utc: str
    iteration: int
    iteration_limit: int
    noise_budget: float
    effort_level: str
    assumptions: List[str] = field(default_factory=list)
    caveats: List[str] = field(default_factory=list)
    research_plan: Dict[str, Any] = field(default_factory=dict)
    next_actions: List[str] = field(default_factory=list)
    last_checkpoint: Optional[str] = None

@dataclass
class Core:
    entities_and_concepts: List[Dict[str, Any]]
    implied_relationships_and_gaps: List[Dict[str, Any]]
    hypotheses_for_structure: List[Dict[str, Any]]

@dataclass
class Graph:
    nodes: List[Node]
    edges: List[Edge]

@dataclass
class SelfCorrection:
    checklist: List[str]
    issues_found: List[str]
    actions: List[Dict[str, str]]

@dataclass
class NoisyGraphScaffold:
    meta: Meta
    core: Core
    graph: Graph
    agents: List[SubagentConfig]
    graph_question: List[GraphQuestion]
    graph_answer: Optional[Dict[str, Any]]
    self_correction: SelfCorrection

@dataclass
class SynthesisResult:
    synthesis: str
    confidence: float
    graph: Graph
    uncertainties: List[str]
    recommendations: List[str]
    trace: Dict[str, Any]

# ============================================================================
# Subagent Registry
# ============================================================================

SUBAGENT_REGISTRY = {
    'mapper': SubagentConfig(
        id='mapper_agent', type='mapper', priority=1, required=True,
        tool_access=['infranodus:getGraphAndStatements', 'infranodus:getGraphAndAdvice']
    ),
    'skeptic': SubagentConfig(
        id='skeptic_agent', type='skeptic', priority=2, required=True,
        tool_access=['Scholar Gateway:semanticSearch']
    ),
    'searcher_web': SubagentConfig(
        id='web_searcher', type='searcher', priority=3, required=False,
        tool_access=['exa:web_search_exa', 'web_fetch']
    ),
    'searcher_academic': SubagentConfig(
        id='academic_searcher', type='searcher', priority=3, required=False,
        tool_access=['Scholar Gateway:semanticSearch']
    ),
    'placeholder_generator': SubagentConfig(
        id='placeholder_agent', type='placeholder_generator', priority=4, required=False,
        tool_access=[]
    ),
    'uncertainty_quantifier': SubagentConfig(
        id='uncertainty_agent', type='uncertainty_quantifier', priority=4, required=False,
        tool_access=[]
    ),
    'hypothesizer': SubagentConfig(
        id='hypothesizer_agent', type='hypothesizer', priority=5, required=False,
        tool_access=['infranodus:getGraphAndAdvice']
    ),
    'verifier': SubagentConfig(
        id='verifier_agent', type='verifier', priority=2, required=False,
        tool_access=['Scholar Gateway:semanticSearch', 'exa:web_search_exa']
    )
}

SELF_CORRECTION_CHECKLIST = [
    "Duplicate labels merged or made distinct?",
    "Any edge without both endpoints?",
    "Any claim without at least one possible falsifier?",
    "Noise budget respected (≥25% low-confidence elements)?",
    "Contradictions explicitly represented (contradicts edges)?",
    "Evidence provenance preserved (result_ids linked)?",
    "Topology target met (|E|/|N| ≥ 4)?"
]

# ============================================================================
# Effort Classification
# ============================================================================

def detect_domains(query: str) -> Set[str]:
    """Detect domains present in query."""
    query_lower = query.lower()
    detected = set()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            detected.add(domain)
    return detected

def requires_current_information(query: str) -> bool:
    """Check if query requires up-to-date information."""
    indicators = ['latest', 'current', '2024', '2025', 'recent', 'now', 'today', 'new']
    return any(ind in query.lower() for ind in indicators)

def classify_effort(query: str, context: dict = None) -> EffortConfig:
    """Classify query complexity and return effort configuration."""
    score = 0.0
    
    # Domain complexity
    domains = detect_domains(query)
    score += len(domains) * 2
    
    # Reasoning indicators
    query_lower = query.lower()
    for indicator, points in REASONING_INDICATORS.items():
        if indicator in query_lower:
            score += points
    
    # Stakes multiplier
    if domains & HIGH_STAKES_DOMAINS:
        score *= 1.5
    
    # Novelty requirement
    if requires_current_information(query):
        score += 2
    
    effort_level = EffortLevel.from_score(score)
    config = DEFAULT_CONFIG["effort_levels"][effort_level.value]
    
    return EffortConfig(
        level=effort_level,
        subagents=config["subagents"],
        max_tool_calls=config["max_tool_calls"],
        max_iterations=config["iterations"],
        checkpoint_interval=config["checkpoint_interval"]
    )

def allocate_subagents(effort_config: EffortConfig, domains: Set[str]) -> List[SubagentConfig]:
    """Allocate subagents based on effort level and domains."""
    allocated = [cfg for cfg in SUBAGENT_REGISTRY.values() if cfg.required]
    optional = sorted(
        [cfg for cfg in SUBAGENT_REGISTRY.values() if not cfg.required],
        key=lambda x: x.priority
    )
    
    remaining_slots = effort_config.subagents - len(allocated)
    
    # Domain-specific allocation
    if 'medical' in domains or 'scientific' in domains:
        for cfg in optional[:]:
            if cfg.type in ('searcher', 'verifier') and 'Scholar Gateway' in str(cfg.tool_access):
                allocated.append(cfg)
                optional.remove(cfg)
                remaining_slots -= 1
                if remaining_slots <= 0:
                    break
    
    for cfg in optional[:remaining_slots]:
        allocated.append(cfg)
    
    return allocated

# ============================================================================
# Scaffold Operations
# ============================================================================

def create_scaffold(topic: str, mode: Mode, effort_config: EffortConfig) -> NoisyGraphScaffold:
    """Initialize a new NoisyGraphScaffold with effort-scaled configuration."""
    domains = detect_domains(topic)
    agents = allocate_subagents(effort_config, domains)
    
    return NoisyGraphScaffold(
        meta=Meta(
            mode=mode.value,
            topic=topic,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            iteration=0,
            iteration_limit=effort_config.max_iterations,
            noise_budget=DEFAULT_CONFIG["noise_budget"],
            effort_level=effort_config.level.value,
            assumptions=[],
            caveats=["This scaffold is provisional and requires validation"]
        ),
        core=Core(
            entities_and_concepts=[],
            implied_relationships_and_gaps=[],
            hypotheses_for_structure=[]
        ),
        graph=Graph(nodes=[], edges=[]),
        agents=agents,
        graph_question=[],
        graph_answer=None,
        self_correction=SelfCorrection(
            checklist=SELF_CORRECTION_CHECKLIST.copy(),
            issues_found=[],
            actions=[]
        )
    )

def generate_node_id(label: str) -> str:
    """Generate stable node ID from label."""
    return f"n_{hashlib.md5(label.lower().encode()).hexdigest()[:8]}"

def generate_edge_id(source: str, target: str, edge_type: EdgeType) -> str:
    """Generate stable edge ID."""
    return f"e_{source}_{edge_type.value}_{target}"

def add_node(scaffold: NoisyGraphScaffold, label: str, description: str,
             node_type: NodeType, confidence: float, evidence: List[Evidence] = None) -> Node:
    """Add node to scaffold."""
    node = Node(
        id=generate_node_id(label),
        label=label,
        description=description,
        type=node_type,
        confidence=confidence,
        status=Status.NEW,
        evidence=evidence or []
    )
    scaffold.graph.nodes.append(node)
    return node

def add_edge(scaffold: NoisyGraphScaffold, source_id: str, target_id: str,
             edge_type: EdgeType, description: str, strength: float,
             evidence: List[Evidence] = None) -> Edge:
    """Add edge to scaffold."""
    edge = Edge(
        id=generate_edge_id(source_id, target_id, edge_type),
        source=source_id,
        target=target_id,
        type=edge_type,
        description=description,
        strength=strength,
        status=Status.NEW,
        evidence=evidence or []
    )
    scaffold.graph.edges.append(edge)
    return edge

# ============================================================================
# Validation
# ============================================================================

def check_noise_budget(scaffold: NoisyGraphScaffold) -> Dict[str, Any]:
    """Check if noise budget is satisfied."""
    nodes, edges = scaffold.graph.nodes, scaffold.graph.edges
    target = scaffold.meta.noise_budget
    
    total = len(nodes) + len(edges)
    if total == 0:
        return {"satisfied": True, "current": 0, "target": target, "deficit": 0}
    
    low_conf = sum(1 for n in nodes if n.confidence <= 0.5)
    low_strength = sum(1 for e in edges if e.strength <= 0.5)
    current = (low_conf + low_strength) / total
    
    return {
        "satisfied": current >= target,
        "current": current,
        "target": target,
        "deficit": max(0, target - current)
    }

def check_topology(scaffold: NoisyGraphScaffold) -> Dict[str, Any]:
    """Check if topology target is met."""
    target = DEFAULT_CONFIG["topology_target"]
    node_count = len(scaffold.graph.nodes)
    edge_count = len(scaffold.graph.edges)
    
    if node_count == 0:
        return {"met": False, "ratio": 0, "target": target}
    
    ratio = edge_count / node_count
    return {"met": ratio >= target, "ratio": ratio, "target": target}

def check_edge_integrity(scaffold: NoisyGraphScaffold) -> Dict[str, Any]:
    """Check for dangling edges."""
    node_ids = {n.id for n in scaffold.graph.nodes}
    dangling = []
    
    for edge in scaffold.graph.edges:
        if edge.source not in node_ids:
            dangling.append({"edge_id": edge.id, "missing": edge.source})
        if edge.target not in node_ids:
            dangling.append({"edge_id": edge.id, "missing": edge.target})
    
    return {"valid": len(dangling) == 0, "dangling_edges": dangling}

def run_self_correction(scaffold: NoisyGraphScaffold) -> None:
    """Run self-correction checklist."""
    scaffold.self_correction.issues_found = []
    scaffold.self_correction.actions = []
    
    # Check duplicates
    labels = [n.label for n in scaffold.graph.nodes]
    duplicates = [l for l in labels if labels.count(l) > 1]
    if duplicates:
        scaffold.self_correction.issues_found.append(f"Duplicate labels: {list(set(duplicates))}")
    
    # Check edge integrity
    integrity = check_edge_integrity(scaffold)
    if not integrity["valid"]:
        for d in integrity["dangling_edges"]:
            scaffold.self_correction.issues_found.append(f"Dangling edge: {d['edge_id']}")
    
    # Check noise budget
    noise = check_noise_budget(scaffold)
    if not noise["satisfied"]:
        scaffold.self_correction.issues_found.append(
            f"Noise budget not met: {noise['current']:.2%} < {noise['target']:.2%}"
        )
    
    # Check topology
    topology = check_topology(scaffold)
    if not topology["met"]:
        scaffold.self_correction.issues_found.append(
            f"Topology target not met: {topology['ratio']:.2f} < {topology['target']:.2f}"
        )

def should_stop(scaffold: NoisyGraphScaffold) -> bool:
    """Check stopping conditions."""
    if scaffold.meta.iteration >= scaffold.meta.iteration_limit:
        return True
    
    has_changes = any(
        n.status in (Status.NEW, Status.UPDATED) for n in scaffold.graph.nodes
    ) or any(
        e.status in (Status.NEW, Status.UPDATED) for e in scaffold.graph.edges
    )
    
    noise_satisfied = check_noise_budget(scaffold)["satisfied"]
    return not has_changes or (noise_satisfied and scaffold.meta.iteration > 0)

# ============================================================================
# Checkpoint Operations
# ============================================================================

def ensure_checkpoint_dir():
    """Ensure checkpoint directory exists."""
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

def generate_checkpoint_id(scaffold: NoisyGraphScaffold) -> str:
    """Generate unique checkpoint ID."""
    topic_hash = hashlib.md5(scaffold.meta.topic.encode()).hexdigest()[:8]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"nlr_{topic_hash}_{scaffold.meta.iteration}_{timestamp}"

def save_checkpoint(scaffold: NoisyGraphScaffold) -> str:
    """Save checkpoint to filesystem."""
    ensure_checkpoint_dir()
    checkpoint_id = generate_checkpoint_id(scaffold)
    
    checkpoint_data = {
        "id": checkpoint_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "topic": scaffold.meta.topic,
        "iteration": scaffold.meta.iteration,
        "effort_level": scaffold.meta.effort_level,
        "graph_summary": {
            "nodes": len(scaffold.graph.nodes),
            "edges": len(scaffold.graph.edges),
            "topology": len(scaffold.graph.edges) / max(1, len(scaffold.graph.nodes))
        },
        "issues": scaffold.self_correction.issues_found,
        "next_actions": scaffold.meta.next_actions
    }
    
    path = CHECKPOINT_DIR / f"{checkpoint_id}.json"
    path.write_text(json.dumps(checkpoint_data, indent=2))
    
    scaffold.meta.last_checkpoint = checkpoint_id
    return checkpoint_id

def list_checkpoints(topic: str = None) -> List[Dict[str, Any]]:
    """List available checkpoints."""
    ensure_checkpoint_dir()
    checkpoints = []
    
    for path in CHECKPOINT_DIR.glob("nlr_*.json"):
        data = json.loads(path.read_text())
        if topic is None or topic.lower() in data.get('topic', '').lower():
            checkpoints.append(data)
    
    return sorted(checkpoints, key=lambda x: x['timestamp'], reverse=True)

# ============================================================================
# Output Formatting
# ============================================================================

def compact_marker(scaffold: NoisyGraphScaffold) -> str:
    """Generate compact mode progress marker."""
    noise = check_noise_budget(scaffold)
    topology = check_topology(scaffold)
    
    return (
        f"[NLR:i{scaffold.meta.iteration}/{scaffold.meta.iteration_limit}|"
        f"n{len(scaffold.graph.nodes)}|"
        f"e{len(scaffold.graph.edges)}|"
        f"r{topology['ratio']:.1f}|"
        f"c{1 - noise['deficit']:.2f}]"
    )

def scaffold_to_dict(scaffold: NoisyGraphScaffold) -> Dict[str, Any]:
    """Convert scaffold to JSON-serializable dict."""
    return {
        "meta": {
            "mode": scaffold.meta.mode,
            "topic": scaffold.meta.topic,
            "timestamp_utc": scaffold.meta.timestamp_utc,
            "iteration": scaffold.meta.iteration,
            "iteration_limit": scaffold.meta.iteration_limit,
            "noise_budget": scaffold.meta.noise_budget,
            "effort_level": scaffold.meta.effort_level,
            "assumptions": scaffold.meta.assumptions,
            "caveats": scaffold.meta.caveats
        },
        "graph": {
            "nodes": [
                {
                    "id": n.id, "label": n.label, "description": n.description,
                    "type": n.type.value, "confidence": n.confidence,
                    "status": n.status.value
                }
                for n in scaffold.graph.nodes
            ],
            "edges": [
                {
                    "id": e.id, "source": e.source, "target": e.target,
                    "type": e.type.value, "description": e.description,
                    "strength": e.strength, "status": e.status.value
                }
                for e in scaffold.graph.edges
            ]
        },
        "agents": [{"id": a.id, "type": a.type, "priority": a.priority} for a in scaffold.agents],
        "self_correction": {
            "checklist": scaffold.self_correction.checklist,
            "issues_found": scaffold.self_correction.issues_found,
            "actions": scaffold.self_correction.actions
        },
        "validation": {
            "noise_budget": check_noise_budget(scaffold),
            "topology": check_topology(scaffold),
            "edge_integrity": check_edge_integrity(scaffold)
        }
    }

def scaffold_to_json(scaffold: NoisyGraphScaffold, indent: int = 2) -> str:
    """Convert scaffold to JSON string."""
    return json.dumps(scaffold_to_dict(scaffold), indent=indent)

# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Non-Linear Reasoning Orchestrator v2.0"
    )
    parser.add_argument("query", help="The query to reason about")
    parser.add_argument("--mode", choices=["full", "compact", "semantic", "research"], default="full")
    parser.add_argument("--effort", choices=["auto", "simple", "moderate", "complex"], default="auto")
    parser.add_argument("--list-checkpoints", action="store_true", help="List available checkpoints")
    
    args = parser.parse_args()
    
    if args.list_checkpoints:
        checkpoints = list_checkpoints(args.query if args.query != "list" else None)
        print(json.dumps(checkpoints, indent=2))
        return
    
    # Classify effort
    if args.effort == "auto":
        effort_config = classify_effort(args.query)
    else:
        config = DEFAULT_CONFIG["effort_levels"][args.effort]
        effort_config = EffortConfig(
            level=EffortLevel(args.effort),
            subagents=config["subagents"],
            max_tool_calls=config["max_tool_calls"],
            max_iterations=config["iterations"],
            checkpoint_interval=config["checkpoint_interval"]
        )
    
    # Create scaffold
    mode = Mode(args.mode)
    scaffold = create_scaffold(args.query, mode, effort_config)
    
    # Output
    if mode == Mode.COMPACT:
        print(compact_marker(scaffold))
    else:
        print(scaffold_to_json(scaffold))
    
    # Save initial checkpoint
    checkpoint_id = save_checkpoint(scaffold)
    print(f"\nCheckpoint saved: {checkpoint_id}", file=__import__('sys').stderr)

if __name__ == "__main__":
    main()
