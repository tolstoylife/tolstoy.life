# Subagent Orchestration Reference

Detailed specifications for recursive multi-agent reasoning within NLR, aligned with Anthropic's orchestrator-worker pattern.

**Related:** [RESEARCH-ORCHESTRATION.md](RESEARCH-ORCHESTRATION.md) for effort scaling and lead researcher patterns.

## Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUBAGENT ORCHESTRATOR                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   AGENT REGISTRY                         │    │
│  │  mapper | skeptic | placeholder | quantifier | hypothesizer │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────────────┐    │
│  │                 QUESTION GENERATOR                       │    │
│  │  agent.generate_questions(scaffold) → graph_question[]   │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────────────┐    │
│  │                  ANSWER PROCESSOR                        │    │
│  │  process_answers(results) → graph_answer                │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────────────┐    │
│  │                RECURSIVE COORDINATOR                     │    │
│  │  spawn_subagent() | terminate() | coordinate()          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Agent Specifications

### 1. Mapper Agent

**Role:** Extract entities, relationships, gaps from input.

**Integration with think skill:**
```python
# Use thoughtbox for systematic mapping
thoughtbox({
    thought: """
    MAPPING PHASE
    Entities found: [...]
    Relationships implied: [...]
    Gaps identified: [...]
    """,
    thoughtNumber: current,
    totalThoughts: estimate,
    nextThoughtNeeded: True
})
```

**Questions Template:**
```json
{
    "agent_id": "mapper_agent",
    "questions": [
        "What are the primary entities and concepts in {QUERY}?",
        "What relationships are implied between {ENTITY_A} and {ENTITY_B}?",
        "What critical gaps exist in the relationship between {DOMAIN_X}?"
    ],
    "expected_signals": ["discover_gap", "confirm", "differentiate"]
}
```

**Output Contract:**
```typescript
interface MapperOutput {
    entities: Array<{
        label: string;
        why_relevant: string;
        confidence: number;  // 0-1
        evidence: Array<{result_id: string; note: string}>;
    }>;
    relationships: Array<{
        source: string;
        target: string;
        type: RelationType;
        strength: number;
        provisional: boolean;
    }>;
    gaps: Array<{
        description: string;
        suggested_placeholder: string;
    }>;
}
```

### 2. Skeptic Agent

**Role:** Challenge assumptions, surface uncertainty.

**Integration with think skill:**
```python
# Use mental model for systematic skepticism
mental_models({
    operation: "get_model",
    args: { model: "assumption-surfacing" }
})

# Apply to current scaffold
thoughtbox({
    thought: """
    SKEPTIC ANALYSIS
    Assumptions challenged: [...]
    Low-confidence elements: [...]
    Noise budget status: {current}/{required}
    """,
    thoughtNumber: current,
    isRevision: True,  # Revising previous mapper conclusions
    revisesThought: mapper_thought_number
})
```

**Questions Template:**
```json
{
    "agent_id": "skeptic_agent",
    "questions": [
        "What assumptions underlie the claim that {CLAIM}?",
        "What evidence would disconfirm the relationship {SOURCE}->{TARGET}?",
        "Which elements have confidence > 0.8 that should be challenged?",
        "Is noise budget (25%) satisfied with current low-confidence elements?"
    ],
    "expected_signals": ["disconfirm", "refine_placeholder_confidence", "select_for_noise_budget"]
}
```

### 3. Placeholder Generator

**Role:** Create provisional elements for gaps.

**Placeholder Schema:**
```typescript
interface Placeholder {
    id: string;  // Format: "placeholder_{domain}_{index}"
    label: string;  // Descriptive but uncertain
    description: string;  // Why this placeholder exists
    type: "placeholder";
    confidence: number;  // Always ≤ 0.5
    constraints: string[];  // What would make this concrete
    gap_reference: string;  // Link to identified gap
}
```

**Generation Pattern:**
```python
def generate_placeholder(gap: Gap) -> Placeholder:
    return {
        "id": f"placeholder_{gap.domain}_{uuid4()[:8]}",
        "label": f"[PROVISIONAL] {infer_likely_form(gap)}",
        "description": f"Placeholder for: {gap.description}",
        "type": "placeholder",
        "confidence": 0.3,  # Default low confidence
        "constraints": [
            f"Would be confirmed by: {gap.confirmation_criteria}",
            f"Would be disconfirmed by: {gap.disconfirmation_criteria}"
        ],
        "gap_reference": gap.id
    }
```

### 4. Uncertainty Quantifier

**Role:** Assign confidence/strength values systematically.

**Quantification Framework:**
```python
def quantify_confidence(element, evidence) -> float:
    """
    Factors:
    - Source quality (peer-reviewed: +0.2, blog: -0.1)
    - Recency (within 1yr: +0.1, >5yr: -0.1)
    - Corroboration (multiple sources: +0.2)
    - Internal consistency (+0.1 if no contradictions)
    """
    base = 0.5
    
    if has_peer_reviewed_source(evidence):
        base += 0.2
    if is_recent(evidence):
        base += 0.1
    if has_multiple_sources(evidence):
        base += 0.2
    if is_internally_consistent(element):
        base += 0.1
    
    return min(1.0, max(0.0, base))

def quantify_strength(edge, evidence) -> float:
    """
    Edge strength considers:
    - Causal evidence (+0.3)
    - Correlational only (+0.1)
    - Theoretical justification (+0.15)
    - Counter-evidence (-0.2)
    """
    base = 0.4
    
    if has_causal_evidence(evidence):
        base += 0.3
    elif has_correlation(evidence):
        base += 0.1
    
    if has_theoretical_basis(evidence):
        base += 0.15
    
    if has_counter_evidence(evidence):
        base -= 0.2
    
    return min(1.0, max(0.0, base))
```

### 5. Hypothesizer Agent

**Role:** Generate structural hypotheses for graph.

**Integration with think skill:**
```python
# Use branching for alternative hypotheses
thoughtbox({
    thought: "Hypothesis A: Linear causal chain {X}→{Y}→{Z}",
    thoughtNumber: current,
    totalThoughts: estimate,
    nextThoughtNeeded: True
})

# Branch for alternative
thoughtbox({
    thought: "Hypothesis B: Bidirectional influence {X}⟷{Y}⟷{Z}",
    thoughtNumber: current,
    branchFromThought: previous_thought,
    branchId: "hypothesis_b"
})
```

**Hypothesis Template:**
```typescript
interface StructuralHypothesis {
    name: string;
    rationale: string;
    structure: {
        pattern: "linear" | "hub_spoke" | "network" | "hierarchical";
        central_nodes: string[];
        key_relationships: Array<{source: string; target: string; type: string}>;
    };
    placeholders: Array<{
        label: string;
        reason: string;
        position: "central" | "peripheral" | "bridge";
    }>;
    testable_predictions: string[];
}
```

## Recursive Loop Implementation

### Spawn Pattern

```typescript
interface SubagentSpawnConfig {
    agent_type: AgentType;
    context: {
        scaffold: NoisyGraphScaffold;
        iteration: number;
        focus_area?: string[];  // Specific nodes/edges to focus on
    };
    integration: {
        think_skill: boolean;  // Use thoughtbox for reasoning
        agent_skill: boolean;  // Emit events via agent-core
    };
}

async function spawnSubagent(config: SubagentSpawnConfig): Promise<SubagentInstance> {
    // 1. Initialize agent with context
    const agent = createAgent(config.agent_type, config.context);
    
    // 2. If think_skill integration, start thoughtbox
    if (config.integration.think_skill) {
        await thoughtbox({
            thought: `[${config.agent_type}] Starting analysis...`,
            thoughtNumber: 1,
            totalThoughts: estimate_thoughts(config.agent_type),
            nextThoughtNeeded: true
        });
    }
    
    // 3. If agent_skill integration, emit spawn event
    if (config.integration.agent_skill) {
        await eventBus.publish({
            type: 'nlr.subagent.spawned',
            source: 'non-linear-reasoning',
            payload: { agent_id: agent.id, agent_type: config.agent_type }
        });
    }
    
    return agent;
}
```

### Recursive Coordination

```python
async def coordinate_recursive_loop(scaffold: NoisyGraphScaffold):
    """
    Main recursive loop coordinating all subagents.
    
    Pattern: THINK → ACT → OBSERVE → BUILD → SELF-CORRECT → RECURSE
    """
    iteration = scaffold.meta.iteration
    
    while not should_stop(scaffold, iteration):
        # THINK: Generate questions via all active agents
        all_questions = []
        for agent in scaffold.agents:
            # Think skill integration: use thoughtbox
            await thoughtbox({
                thought: f"[{agent.id}] Generating questions for iteration {iteration}",
                thoughtNumber: iteration * 2 - 1,
                totalThoughts: scaffold.meta.iteration_limit * 2,
                nextThoughtNeeded: True
            })
            
            questions = await agent.generate_questions(scaffold)
            all_questions.extend(questions)
            
            # Agent skill integration: emit event
            await event_bus.publish({
                type: 'nlr.subagent.question_generated',
                payload: {'agent_id': agent.id, 'count': len(questions)}
            })
        
        scaffold.graph_question = all_questions
        
        # ACT: Execute MCP tools for evidence
        results = await gather_evidence(scaffold.graph_question)
        
        # OBSERVE: Process results into answers
        scaffold.graph_answer = process_evidence_to_answers(results, scaffold)
        
        # BUILD: Update graph with new nodes/edges
        update_graph_from_answers(scaffold)
        
        # SELF-CORRECT: Run checklist
        run_self_correction(scaffold)
        
        # Emit iteration complete event
        await event_bus.publish({
            type: 'nlr.reasoning.iteration_complete',
            payload: {
                'iteration': iteration,
                'nodes': len(scaffold.graph.nodes),
                'edges': len(scaffold.graph.edges)
            }
        })
        
        iteration += 1
        scaffold.meta.iteration = iteration
    
    # Final convergence event
    await event_bus.publish({
        type: 'nlr.reasoning.converged',
        payload: {'total_iterations': iteration}
    })
    
    return scaffold
```

### Inter-Agent Communication

Agents communicate via the event bus and shared scaffold:

```typescript
// Agent A discovers a gap
await eventBus.publish({
    type: 'nlr.graph.gap_discovered',
    source: 'mapper_agent',
    payload: {
        gap_description: 'Missing mediator between X and Y',
        suggested_placeholder: 'mediator_xy',
        confidence: 0.3
    }
});

// Placeholder generator subscribes and responds
eventBus.subscribe('nlr.graph.gap_discovered', async (event) => {
    const placeholder = generatePlaceholder(event.payload);
    scaffold.graph.nodes.push(placeholder);
    
    await eventBus.publish({
        type: 'nlr.graph.node_added',
        source: 'placeholder_generator',
        payload: { node: placeholder }
    });
});
```

## Noise Budget Management

Agents collectively maintain the noise budget:

```python
def check_noise_budget(scaffold):
    """Ensure ≥ noise_budget fraction of elements are low-confidence."""
    total_nodes = len(scaffold.graph.nodes)
    total_edges = len(scaffold.graph.edges)
    
    low_conf_nodes = sum(1 for n in scaffold.graph.nodes if n.confidence <= 0.5)
    low_conf_edges = sum(1 for e in scaffold.graph.edges if e.strength <= 0.5)
    
    node_ratio = low_conf_nodes / total_nodes if total_nodes > 0 else 0
    edge_ratio = low_conf_edges / total_edges if total_edges > 0 else 0
    
    overall_ratio = (node_ratio + edge_ratio) / 2
    
    return {
        'satisfied': overall_ratio >= scaffold.meta.noise_budget,
        'current': overall_ratio,
        'target': scaffold.meta.noise_budget,
        'deficit': max(0, scaffold.meta.noise_budget - overall_ratio)
    }

# If not satisfied, skeptic_agent generates questions to add uncertainty
if not check_noise_budget(scaffold)['satisfied']:
    await eventBus.publish({
        type: 'nlr.noise_budget.deficit',
        source: 'noise_monitor',
        payload: check_noise_budget(scaffold)
    })
```

## Agent Lifecycle

```
SPAWN → ACTIVE → [PAUSE] → [RESUME] → TERMINATE

States:
- SPAWN: Agent created with context
- ACTIVE: Generating questions and processing answers
- PAUSE: Waiting for evidence or other agents
- RESUME: Continue after pause
- TERMINATE: Complete or error
```

Each agent tracks its state:

```typescript
interface AgentState {
    id: string;
    status: 'spawn' | 'active' | 'pause' | 'terminate';
    questions_generated: number;
    answers_processed: number;
    last_activity: Date;
    error?: string;
}
```
