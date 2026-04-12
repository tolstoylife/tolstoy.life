# State Persistence Reference

Patterns for checkpointing, state management, and context overflow recovery in recursive NLR workflows.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          STATE PERSISTENCE LAYER                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      CHECKPOINT MANAGER                              │   │
│   │  • Save interval: Every N iterations                                │   │
│   │  • Compression: Minimal context extraction                          │   │
│   │  • Storage: Filesystem (/home/claude/nlr_checkpoints/)              │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│              ┌─────────────────────┼─────────────────────┐                  │
│              │                     │                     │                  │
│              ▼                     ▼                     ▼                  │
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐          │
│   │   FULL STATE    │   │  SUMMARY STATE  │   │  RECOVERY PLAN  │          │
│   │   (detailed)    │   │  (condensed)    │   │  (actionable)   │          │
│   └─────────────────┘   └─────────────────┘   └─────────────────┘          │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      RECOVERY ENGINE                                 │   │
│   │  • Load checkpoint on context overflow                              │   │
│   │  • Resume with fresh subagent contexts                              │   │
│   │  • Preserve accumulated findings                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Checkpoint Schema

### Full Checkpoint (Every N Iterations)

```python
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import json
import hashlib

@dataclass
class CheckpointMetadata:
    checkpoint_id: str
    topic: str
    timestamp_utc: str
    iteration: int
    total_iterations: int
    effort_level: str
    version: str = "2.0"

@dataclass
class GraphSummary:
    node_count: int
    edge_count: int
    topology_ratio: float
    noise_ratio: float
    high_confidence_count: int
    low_confidence_count: int
    placeholder_count: int

@dataclass
class ResearchProgress:
    sub_questions_total: int
    sub_questions_answered: int
    gaps_identified: int
    gaps_resolved: int
    subagents_completed: int
    subagents_failed: int

@dataclass
class KeyFinding:
    claim: str
    confidence: float
    evidence_count: int
    source_types: List[str]
    node_id: str

@dataclass
class OpenGap:
    description: str
    severity: str  # high, medium, low
    between: List[str]
    suggested_search: str
    attempts: int

@dataclass
class FullCheckpoint:
    metadata: CheckpointMetadata
    graph_summary: GraphSummary
    research_progress: ResearchProgress
    key_findings: List[KeyFinding]
    open_gaps: List[OpenGap]
    research_plan: Dict[str, Any]
    next_actions: List[str]
    
    # Condensed graph (for recovery)
    condensed_nodes: List[Dict]  # Only high-value nodes
    condensed_edges: List[Dict]  # Only strong edges
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'FullCheckpoint':
        data = json.loads(json_str)
        return cls(
            metadata=CheckpointMetadata(**data['metadata']),
            graph_summary=GraphSummary(**data['graph_summary']),
            research_progress=ResearchProgress(**data['research_progress']),
            key_findings=[KeyFinding(**f) for f in data['key_findings']],
            open_gaps=[OpenGap(**g) for g in data['open_gaps']],
            research_plan=data['research_plan'],
            next_actions=data['next_actions'],
            condensed_nodes=data['condensed_nodes'],
            condensed_edges=data['condensed_edges']
        )
```

### Condensed Context Extraction

```python
def extract_condensed_context(scaffold: NoisyGraphScaffold) -> Dict[str, Any]:
    """Extract minimal context for subagent injection or recovery."""
    
    # High-value nodes: hubs, high confidence, or central to query
    high_value_nodes = [
        {
            'id': n.id,
            'label': n.label,
            'type': n.type.value,
            'confidence': n.confidence
        }
        for n in scaffold.graph.nodes
        if n.confidence > 0.7 or is_hub(n, scaffold) or is_central(n, scaffold)
    ][:20]  # Limit to 20 nodes
    
    # Strong edges: high strength, connects high-value nodes
    high_value_node_ids = {n['id'] for n in high_value_nodes}
    strong_edges = [
        {
            'source': e.source,
            'target': e.target,
            'type': e.type.value,
            'strength': e.strength
        }
        for e in scaffold.graph.edges
        if e.strength > 0.6 and e.source in high_value_node_ids and e.target in high_value_node_ids
    ][:40]  # Limit to 40 edges
    
    # Key findings summary
    key_findings = extract_key_findings(scaffold)[:10]
    
    # Open gaps
    open_gaps = [
        g for g in scaffold.core.implied_relationships_and_gaps
        if not g.get('resolved', False)
    ][:5]
    
    return {
        'topic': scaffold.meta.topic,
        'iteration': scaffold.meta.iteration,
        'nodes_summary': high_value_nodes,
        'edges_summary': strong_edges,
        'key_findings': key_findings,
        'open_gaps': open_gaps,
        'noise_budget_status': check_noise_budget(scaffold),
        'topology_status': check_topology(scaffold)
    }

def is_hub(node: Node, scaffold: NoisyGraphScaffold) -> bool:
    """Check if node is a hub (high degree centrality)."""
    degree = sum(1 for e in scaffold.graph.edges 
                 if e.source == node.id or e.target == node.id)
    avg_degree = len(scaffold.graph.edges) * 2 / max(1, len(scaffold.graph.nodes))
    return degree > avg_degree * 1.5

def is_central(node: Node, scaffold: NoisyGraphScaffold) -> bool:
    """Check if node is central to the query topic."""
    topic_terms = scaffold.meta.topic.lower().split()
    return any(term in node.label.lower() for term in topic_terms)
```

## Checkpoint Operations

### Save Checkpoint

```python
import os
from pathlib import Path

CHECKPOINT_DIR = Path("/home/claude/nlr_checkpoints")

def ensure_checkpoint_dir():
    """Ensure checkpoint directory exists."""
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

def generate_checkpoint_id(scaffold: NoisyGraphScaffold) -> str:
    """Generate unique checkpoint ID."""
    topic_hash = hashlib.md5(scaffold.meta.topic.encode()).hexdigest()[:8]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"nlr_{topic_hash}_{scaffold.meta.iteration}_{timestamp}"

def save_checkpoint(scaffold: NoisyGraphScaffold) -> str:
    """Save full checkpoint to filesystem."""
    ensure_checkpoint_dir()
    
    checkpoint_id = generate_checkpoint_id(scaffold)
    
    # Extract key findings
    key_findings = [
        KeyFinding(
            claim=n.label,
            confidence=n.confidence,
            evidence_count=len(n.evidence),
            source_types=list(set(e.result_id.split('_')[0] for e in n.evidence)),
            node_id=n.id
        )
        for n in scaffold.graph.nodes
        if n.confidence > 0.7 and n.type.value == 'claim'
    ][:15]
    
    # Extract open gaps
    open_gaps = [
        OpenGap(
            description=g['gap'],
            severity='medium',  # Default
            between=g.get('between', []),
            suggested_search=g.get('suggested_search', ''),
            attempts=g.get('attempts', 0)
        )
        for g in scaffold.core.implied_relationships_and_gaps
        if not g.get('resolved', False)
    ][:10]
    
    # Build checkpoint
    checkpoint = FullCheckpoint(
        metadata=CheckpointMetadata(
            checkpoint_id=checkpoint_id,
            topic=scaffold.meta.topic,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            iteration=scaffold.meta.iteration,
            total_iterations=scaffold.meta.iteration_limit,
            effort_level=scaffold.meta.get('effort_level', 'moderate')
        ),
        graph_summary=GraphSummary(
            node_count=len(scaffold.graph.nodes),
            edge_count=len(scaffold.graph.edges),
            topology_ratio=len(scaffold.graph.edges) / max(1, len(scaffold.graph.nodes)),
            noise_ratio=calculate_noise_ratio(scaffold),
            high_confidence_count=sum(1 for n in scaffold.graph.nodes if n.confidence > 0.7),
            low_confidence_count=sum(1 for n in scaffold.graph.nodes if n.confidence <= 0.5),
            placeholder_count=sum(1 for n in scaffold.graph.nodes if n.type.value == 'placeholder')
        ),
        research_progress=ResearchProgress(
            sub_questions_total=len(scaffold.meta.get('sub_questions', [])),
            sub_questions_answered=len([q for q in scaffold.meta.get('sub_questions', []) if q.get('answered')]),
            gaps_identified=len(scaffold.core.implied_relationships_and_gaps),
            gaps_resolved=len([g for g in scaffold.core.implied_relationships_and_gaps if g.get('resolved')]),
            subagents_completed=scaffold.meta.get('subagents_completed', 0),
            subagents_failed=scaffold.meta.get('subagents_failed', 0)
        ),
        key_findings=key_findings,
        open_gaps=open_gaps,
        research_plan=scaffold.meta.get('research_plan', {}),
        next_actions=scaffold.meta.get('next_actions', []),
        condensed_nodes=extract_condensed_context(scaffold)['nodes_summary'],
        condensed_edges=extract_condensed_context(scaffold)['edges_summary']
    )
    
    # Save to file
    checkpoint_path = CHECKPOINT_DIR / f"{checkpoint_id}.json"
    checkpoint_path.write_text(checkpoint.to_json())
    
    # Also save full scaffold for complete recovery
    full_path = CHECKPOINT_DIR / f"{checkpoint_id}_full.json"
    full_path.write_text(scaffold_to_json(scaffold))
    
    return checkpoint_id

def calculate_noise_ratio(scaffold: NoisyGraphScaffold) -> float:
    """Calculate current noise ratio."""
    total = len(scaffold.graph.nodes) + len(scaffold.graph.edges)
    if total == 0:
        return 0.0
    
    low_conf = sum(1 for n in scaffold.graph.nodes if n.confidence <= 0.5)
    low_strength = sum(1 for e in scaffold.graph.edges if e.strength <= 0.5)
    
    return (low_conf + low_strength) / total
```

### Load Checkpoint

```python
def list_checkpoints(topic: str = None) -> List[Dict[str, Any]]:
    """List available checkpoints, optionally filtered by topic."""
    ensure_checkpoint_dir()
    
    checkpoints = []
    for path in CHECKPOINT_DIR.glob("nlr_*.json"):
        if "_full" in path.name:
            continue  # Skip full backups
        
        checkpoint = FullCheckpoint.from_json(path.read_text())
        
        if topic is None or topic.lower() in checkpoint.metadata.topic.lower():
            checkpoints.append({
                'id': checkpoint.metadata.checkpoint_id,
                'topic': checkpoint.metadata.topic,
                'timestamp': checkpoint.metadata.timestamp_utc,
                'iteration': checkpoint.metadata.iteration,
                'progress': f"{checkpoint.research_progress.sub_questions_answered}/{checkpoint.research_progress.sub_questions_total}"
            })
    
    return sorted(checkpoints, key=lambda x: x['timestamp'], reverse=True)

def load_checkpoint(checkpoint_id: str) -> FullCheckpoint:
    """Load checkpoint by ID."""
    path = CHECKPOINT_DIR / f"{checkpoint_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_id}")
    
    return FullCheckpoint.from_json(path.read_text())

def load_full_scaffold(checkpoint_id: str) -> NoisyGraphScaffold:
    """Load full scaffold backup for complete recovery."""
    path = CHECKPOINT_DIR / f"{checkpoint_id}_full.json"
    if not path.exists():
        raise FileNotFoundError(f"Full scaffold not found: {checkpoint_id}")
    
    return scaffold_from_json(path.read_text())

def load_latest_checkpoint(topic: str) -> FullCheckpoint:
    """Load most recent checkpoint for a topic."""
    checkpoints = list_checkpoints(topic)
    if not checkpoints:
        raise FileNotFoundError(f"No checkpoints found for topic: {topic}")
    
    return load_checkpoint(checkpoints[0]['id'])
```

### Recovery from Checkpoint

```python
async def recover_from_checkpoint(
    checkpoint: FullCheckpoint,
    scaffold: NoisyGraphScaffold = None
) -> NoisyGraphScaffold:
    """Recover research state from checkpoint."""
    
    # Try to load full scaffold first
    try:
        full_scaffold = load_full_scaffold(checkpoint.metadata.checkpoint_id)
        return full_scaffold
    except FileNotFoundError:
        pass
    
    # Reconstruct from condensed checkpoint
    if scaffold is None:
        scaffold = create_scaffold(checkpoint.metadata.topic)
    
    # Restore metadata
    scaffold.meta.iteration = checkpoint.metadata.iteration
    scaffold.meta.topic = checkpoint.metadata.topic
    scaffold.meta['effort_level'] = checkpoint.metadata.effort_level
    scaffold.meta['research_plan'] = checkpoint.research_plan
    scaffold.meta['next_actions'] = checkpoint.next_actions
    
    # Restore condensed nodes
    for node_data in checkpoint.condensed_nodes:
        node = Node(
            id=node_data['id'],
            label=node_data['label'],
            description=f"Recovered from checkpoint {checkpoint.metadata.checkpoint_id}",
            type=NodeType(node_data['type']),
            confidence=node_data['confidence'],
            status=Status.UNCHANGED
        )
        scaffold.graph.nodes.append(node)
    
    # Restore condensed edges
    for edge_data in checkpoint.condensed_edges:
        edge = Edge(
            id=f"{edge_data['source']}_{edge_data['type']}_{edge_data['target']}",
            source=edge_data['source'],
            target=edge_data['target'],
            type=EdgeType(edge_data['type']),
            description=f"Recovered from checkpoint",
            strength=edge_data['strength'],
            status=Status.UNCHANGED
        )
        scaffold.graph.edges.append(edge)
    
    # Restore open gaps
    scaffold.core.implied_relationships_and_gaps = [
        {
            'gap': gap.description,
            'between': gap.between,
            'suggested_search': gap.suggested_search,
            'attempts': gap.attempts,
            'resolved': False
        }
        for gap in checkpoint.open_gaps
    ]
    
    # Log recovery
    scaffold.self_correction.issues_found.append(
        f"Recovered from checkpoint {checkpoint.metadata.checkpoint_id} at iteration {checkpoint.metadata.iteration}"
    )
    
    return scaffold
```

## StateFlow Pattern

Model task-solving as finite state machine:

```python
from enum import Enum, auto
from typing import Callable, Dict

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

@dataclass
class StateTransition:
    from_state: ResearchState
    to_state: ResearchState
    condition: Callable[[NoisyGraphScaffold], bool]
    action: Callable[[NoisyGraphScaffold], None]

class ResearchStateMachine:
    def __init__(self, scaffold: NoisyGraphScaffold):
        self.scaffold = scaffold
        self.state = ResearchState.INIT
        self.state_history = []
        self.iteration_count = 0
        self.max_iterations = scaffold.meta.iteration_limit
        
    def define_transitions(self) -> List[StateTransition]:
        return [
            StateTransition(
                ResearchState.INIT,
                ResearchState.STRATEGY,
                condition=lambda s: True,
                action=self.log_transition
            ),
            StateTransition(
                ResearchState.STRATEGY,
                ResearchState.SPAWN_SUBAGENTS,
                condition=lambda s: s.meta.get('research_plan') is not None,
                action=self.log_transition
            ),
            StateTransition(
                ResearchState.SPAWN_SUBAGENTS,
                ResearchState.EXECUTE_PARALLEL,
                condition=lambda s: len(s.agents) > 0,
                action=self.log_transition
            ),
            StateTransition(
                ResearchState.EXECUTE_PARALLEL,
                ResearchState.INTEGRATE_RESULTS,
                condition=lambda s: True,  # Always after execution
                action=self.log_transition
            ),
            StateTransition(
                ResearchState.INTEGRATE_RESULTS,
                ResearchState.SELF_CORRECT,
                condition=lambda s: True,
                action=self.log_transition
            ),
            StateTransition(
                ResearchState.SELF_CORRECT,
                ResearchState.CHECKPOINT,
                condition=lambda s: self.should_checkpoint(),
                action=self.do_checkpoint
            ),
            StateTransition(
                ResearchState.SELF_CORRECT,
                ResearchState.SPAWN_SUBAGENTS,
                condition=lambda s: not self.should_stop() and not self.should_checkpoint(),
                action=self.increment_iteration
            ),
            StateTransition(
                ResearchState.CHECKPOINT,
                ResearchState.SPAWN_SUBAGENTS,
                condition=lambda s: not self.should_stop(),
                action=self.increment_iteration
            ),
            StateTransition(
                ResearchState.CHECKPOINT,
                ResearchState.SYNTHESIZE,
                condition=lambda s: self.should_stop(),
                action=self.log_transition
            ),
            StateTransition(
                ResearchState.SELF_CORRECT,
                ResearchState.SYNTHESIZE,
                condition=lambda s: self.should_stop(),
                action=self.log_transition
            ),
            StateTransition(
                ResearchState.SYNTHESIZE,
                ResearchState.COMPLETE,
                condition=lambda s: True,
                action=self.log_transition
            ),
            # Error recovery
            StateTransition(
                ResearchState.ERROR,
                ResearchState.CHECKPOINT,
                condition=lambda s: self.can_recover(),
                action=self.attempt_recovery
            )
        ]
    
    def should_checkpoint(self) -> bool:
        """Check if checkpoint is due."""
        checkpoint_interval = self.scaffold.meta.get('checkpoint_interval', 2)
        return self.iteration_count > 0 and self.iteration_count % checkpoint_interval == 0
    
    def should_stop(self) -> bool:
        """Check stopping conditions."""
        return (
            self.iteration_count >= self.max_iterations or
            check_convergence(self.scaffold) or
            no_material_changes(self.scaffold)
        )
    
    def can_recover(self) -> bool:
        """Check if recovery is possible."""
        checkpoints = list_checkpoints(self.scaffold.meta.topic)
        return len(checkpoints) > 0
    
    def log_transition(self, scaffold: NoisyGraphScaffold) -> None:
        """Log state transition."""
        self.state_history.append({
            'from': self.state.name,
            'iteration': self.iteration_count,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
    
    def increment_iteration(self, scaffold: NoisyGraphScaffold) -> None:
        """Increment iteration counter."""
        self.iteration_count += 1
        scaffold.meta.iteration = self.iteration_count
    
    def do_checkpoint(self, scaffold: NoisyGraphScaffold) -> None:
        """Execute checkpoint."""
        checkpoint_id = save_checkpoint(scaffold)
        scaffold.meta['last_checkpoint'] = checkpoint_id
    
    async def attempt_recovery(self, scaffold: NoisyGraphScaffold) -> None:
        """Attempt recovery from last checkpoint."""
        checkpoint = load_latest_checkpoint(scaffold.meta.topic)
        self.scaffold = await recover_from_checkpoint(checkpoint, scaffold)
        self.state = ResearchState.SPAWN_SUBAGENTS
    
    async def run(self) -> NoisyGraphScaffold:
        """Execute state machine."""
        transitions = self.define_transitions()
        
        while self.state != ResearchState.COMPLETE:
            # Find applicable transition
            applicable = [
                t for t in transitions
                if t.from_state == self.state and t.condition(self.scaffold)
            ]
            
            if not applicable:
                self.state = ResearchState.ERROR
                if not self.can_recover():
                    raise RuntimeError(f"No valid transition from state {self.state}")
                continue
            
            # Execute transition
            transition = applicable[0]
            transition.action(self.scaffold)
            self.state = transition.to_state
            
            # Execute state-specific logic
            await self.execute_state_logic()
        
        return self.scaffold
    
    async def execute_state_logic(self) -> None:
        """Execute logic for current state."""
        state_handlers = {
            ResearchState.STRATEGY: self.handle_strategy,
            ResearchState.SPAWN_SUBAGENTS: self.handle_spawn,
            ResearchState.EXECUTE_PARALLEL: self.handle_execute,
            ResearchState.INTEGRATE_RESULTS: self.handle_integrate,
            ResearchState.SELF_CORRECT: self.handle_self_correct,
            ResearchState.SYNTHESIZE: self.handle_synthesize
        }
        
        handler = state_handlers.get(self.state)
        if handler:
            await handler()
```

## Context Overflow Handling

```python
async def execute_with_overflow_protection(
    scaffold: NoisyGraphScaffold,
    state_machine: ResearchStateMachine
) -> SynthesisResult:
    """Execute research with automatic context overflow recovery."""
    
    max_recovery_attempts = 3
    recovery_attempts = 0
    
    while recovery_attempts < max_recovery_attempts:
        try:
            result_scaffold = await state_machine.run()
            return synthesize_findings(result_scaffold)
            
        except ContextOverflowError as e:
            recovery_attempts += 1
            
            # Save emergency checkpoint
            checkpoint_id = save_checkpoint(scaffold)
            
            # Log overflow
            scaffold.self_correction.issues_found.append(
                f"Context overflow at iteration {scaffold.meta.iteration}. "
                f"Checkpoint: {checkpoint_id}. Recovery attempt: {recovery_attempts}"
            )
            
            # Load checkpoint and create fresh state machine
            checkpoint = load_checkpoint(checkpoint_id)
            scaffold = await recover_from_checkpoint(checkpoint)
            
            # Summarize completed work to reduce context
            scaffold = compress_scaffold_context(scaffold)
            
            # Create new state machine
            state_machine = ResearchStateMachine(scaffold)
            state_machine.state = ResearchState.SPAWN_SUBAGENTS
            state_machine.iteration_count = checkpoint.metadata.iteration
    
    # Max recovery attempts exceeded - force synthesis with current state
    return synthesize_with_partial_data(scaffold)

def compress_scaffold_context(scaffold: NoisyGraphScaffold) -> NoisyGraphScaffold:
    """Compress scaffold to reduce context size."""
    
    # Keep only high-value nodes
    high_value_nodes = [
        n for n in scaffold.graph.nodes
        if n.confidence > 0.6 or n.type.value == 'placeholder'
    ][:30]
    
    # Keep only strong edges between retained nodes
    retained_ids = {n.id for n in high_value_nodes}
    strong_edges = [
        e for e in scaffold.graph.edges
        if e.strength > 0.5 and e.source in retained_ids and e.target in retained_ids
    ][:60]
    
    scaffold.graph.nodes = high_value_nodes
    scaffold.graph.edges = strong_edges
    
    # Summarize completed sub-questions
    if scaffold.meta.get('sub_questions'):
        answered = [q for q in scaffold.meta['sub_questions'] if q.get('answered')]
        scaffold.meta['completed_summary'] = summarize_answered_questions(answered)
        scaffold.meta['sub_questions'] = [q for q in scaffold.meta['sub_questions'] if not q.get('answered')]
    
    return scaffold
```

## Integration with Think Skill

```python
async def checkpoint_with_reasoning(
    scaffold: NoisyGraphScaffold,
    checkpoint_id: str
) -> None:
    """Checkpoint with reasoning trace via thoughtbox."""
    
    await thoughtbox({
        'thought': f"""
        CHECKPOINT: {checkpoint_id}
        
        State Summary:
        - Iteration: {scaffold.meta.iteration}/{scaffold.meta.iteration_limit}
        - Nodes: {len(scaffold.graph.nodes)}
        - Edges: {len(scaffold.graph.edges)}
        - Topology: {len(scaffold.graph.edges)/max(1,len(scaffold.graph.nodes)):.2f}
        - Noise: {calculate_noise_ratio(scaffold):.2%}
        
        Key Findings (top 5):
        {format_top_findings(scaffold, 5)}
        
        Open Gaps (top 3):
        {format_top_gaps(scaffold, 3)}
        
        Next Actions:
        {scaffold.meta.get('next_actions', ['Continue research'])}
        
        Recovery Strategy:
        If context overflow occurs, load checkpoint {checkpoint_id} and:
        1. Resume from iteration {scaffold.meta.iteration}
        2. Focus on open gaps
        3. Spawn fresh subagents with condensed context
        """,
        'thoughtNumber': scaffold.meta.iteration,
        'totalThoughts': scaffold.meta.iteration_limit,
        'nextThoughtNeeded': True
    })
```

## Cleanup Operations

```python
def cleanup_old_checkpoints(topic: str, keep_last: int = 3) -> int:
    """Remove old checkpoints, keeping most recent N."""
    checkpoints = list_checkpoints(topic)
    
    if len(checkpoints) <= keep_last:
        return 0
    
    to_remove = checkpoints[keep_last:]
    removed = 0
    
    for checkpoint in to_remove:
        try:
            path = CHECKPOINT_DIR / f"{checkpoint['id']}.json"
            full_path = CHECKPOINT_DIR / f"{checkpoint['id']}_full.json"
            
            if path.exists():
                path.unlink()
                removed += 1
            if full_path.exists():
                full_path.unlink()
        except Exception:
            pass
    
    return removed

def cleanup_all_checkpoints() -> int:
    """Remove all checkpoints."""
    ensure_checkpoint_dir()
    removed = 0
    
    for path in CHECKPOINT_DIR.glob("nlr_*.json"):
        try:
            path.unlink()
            removed += 1
        except Exception:
            pass
    
    return removed
```
