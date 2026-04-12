# Research Orchestration Reference

Detailed implementation of Anthropic's orchestrator-worker pattern for multi-agent research with custom reasoning framework integration.

## Architecture Overview

Based on Anthropic's multi-agent research system (June 2025), this architecture achieves 90.2% better performance than single-agent approaches through parallel subagent execution with isolated contexts.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LEAD RESEARCHER (ORCHESTRATOR)                       │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      STRATEGY DEVELOPMENT                            │   │
│  │  1. Query Analysis → Complexity Classification                       │   │
│  │  2. Domain Identification → Subagent Allocation                      │   │
│  │  3. Research Plan → Save to Memory                                   │   │
│  │  4. Task Distribution → Parallel Execution                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│              ┌─────────────────────┼─────────────────────┐                  │
│              │                     │                     │                  │
│              ▼                     ▼                     ▼                  │
│  ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐         │
│  │   MAPPER AGENT    │ │   SKEPTIC AGENT   │ │  SEARCHER AGENT   │  ...    │
│  │                   │ │                   │ │                   │         │
│  │ • Entity extract  │ │ • Challenge claims│ │ • Web search      │         │
│  │ • Relationship    │ │ • Uncertainty     │ │ • Scholar search  │         │
│  │ • Gap detection   │ │ • Falsifiability  │ │ • Evidence gather │         │
│  └─────────┬─────────┘ └─────────┬─────────┘ └─────────┬─────────┘         │
│            │                     │                     │                    │
│            └─────────────────────┼─────────────────────┘                    │
│                                  ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                       SYNTHESIS & CITATION                           │   │
│  │  • Integrate findings → NoisyGraph                                   │   │
│  │  • Process citations → Attribution                                   │   │
│  │  • Generate synthesis → Confidence-weighted                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Effort Scaling Implementation

### Complexity Classifier

```python
from dataclasses import dataclass
from enum import Enum
from typing import List, Set

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

@dataclass
class EffortConfig:
    level: EffortLevel
    subagents: int
    max_tool_calls: int
    max_iterations: int
    checkpoint_interval: int

EFFORT_CONFIGS = {
    EffortLevel.SIMPLE: EffortConfig(
        level=EffortLevel.SIMPLE,
        subagents=1,
        max_tool_calls=10,
        max_iterations=3,
        checkpoint_interval=3
    ),
    EffortLevel.MODERATE: EffortConfig(
        level=EffortLevel.MODERATE,
        subagents=3,
        max_tool_calls=30,
        max_iterations=5,
        checkpoint_interval=2
    ),
    EffortLevel.COMPLEX: EffortConfig(
        level=EffortLevel.COMPLEX,
        subagents=7,
        max_tool_calls=100,
        max_iterations=9,
        checkpoint_interval=2
    )
}

DOMAIN_KEYWORDS = {
    'medical': ['diagnosis', 'treatment', 'symptom', 'disease', 'medication', 'clinical', 
                'patient', 'therapeutic', 'pathophysiology', 'pharmacology', 'ICU', 'anaesthesia'],
    'legal': ['law', 'regulation', 'compliance', 'statute', 'legal', 'court', 'contract'],
    'technical': ['algorithm', 'implementation', 'architecture', 'system', 'code', 'API'],
    'scientific': ['research', 'study', 'experiment', 'hypothesis', 'evidence', 'mechanism'],
    'financial': ['investment', 'market', 'financial', 'trading', 'portfolio', 'risk']
}

REASONING_INDICATORS = {
    'compare': 3,
    'contrast': 3,
    'analyze': 4,
    'synthesize': 5,
    'evaluate': 4,
    'mechanism': 4,
    'pathway': 4,
    'causation': 5,
    'why': 3,
    'how does': 3
}

HIGH_STAKES_DOMAINS = {'medical', 'legal'}

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
    
    # Domain complexity (each domain adds 2 points)
    domains = detect_domains(query)
    score += len(domains) * 2
    
    # Reasoning indicators
    query_lower = query.lower()
    for indicator, points in REASONING_INDICATORS.items():
        if indicator in query_lower:
            score += points
    
    # Stakes multiplier (1.5x for high-stakes domains)
    if domains & HIGH_STAKES_DOMAINS:
        score *= 1.5
    
    # Novelty requirement
    if requires_current_information(query):
        score += 2
    
    # Context complexity (if provided)
    if context:
        if len(context.get('prior_findings', [])) > 10:
            score += 2
        if context.get('requires_verification', False):
            score += 3
    
    effort_level = EffortLevel.from_score(score)
    return EFFORT_CONFIGS[effort_level]
```

### Subagent Allocation Strategy

```python
from typing import List, Dict, Any

@dataclass
class SubagentConfig:
    id: str
    type: str
    priority: int  # Lower = higher priority
    required: bool  # Always include in allocation
    tool_access: List[str]
    
SUBAGENT_REGISTRY = {
    'mapper': SubagentConfig(
        id='mapper_agent',
        type='mapper',
        priority=1,
        required=True,
        tool_access=['infranodus:getGraphAndStatements', 'infranodus:getGraphAndAdvice']
    ),
    'skeptic': SubagentConfig(
        id='skeptic_agent',
        type='skeptic',
        priority=2,
        required=True,
        tool_access=['Scholar Gateway:semanticSearch']
    ),
    'searcher_web': SubagentConfig(
        id='web_searcher',
        type='searcher',
        priority=3,
        required=False,
        tool_access=['exa:web_search_exa', 'web_fetch']
    ),
    'searcher_academic': SubagentConfig(
        id='academic_searcher',
        type='searcher',
        priority=3,
        required=False,
        tool_access=['Scholar Gateway:semanticSearch']
    ),
    'placeholder_generator': SubagentConfig(
        id='placeholder_agent',
        type='placeholder_generator',
        priority=4,
        required=False,
        tool_access=[]
    ),
    'uncertainty_quantifier': SubagentConfig(
        id='uncertainty_agent',
        type='uncertainty_quantifier',
        priority=4,
        required=False,
        tool_access=[]
    ),
    'hypothesizer': SubagentConfig(
        id='hypothesizer_agent',
        type='hypothesizer',
        priority=5,
        required=False,
        tool_access=['infranodus:getGraphAndAdvice']
    ),
    'verifier': SubagentConfig(
        id='verifier_agent',
        type='verifier',
        priority=2,
        required=False,
        tool_access=['Scholar Gateway:semanticSearch', 'exa:web_search_exa']
    )
}

def allocate_subagents(effort_config: EffortConfig, domains: Set[str]) -> List[SubagentConfig]:
    """Allocate subagents based on effort level and domains."""
    # Always include required agents
    allocated = [cfg for cfg in SUBAGENT_REGISTRY.values() if cfg.required]
    
    # Sort remaining by priority
    optional = sorted(
        [cfg for cfg in SUBAGENT_REGISTRY.values() if not cfg.required],
        key=lambda x: x.priority
    )
    
    # Fill remaining slots by priority
    remaining_slots = effort_config.subagents - len(allocated)
    
    # Domain-specific allocation
    if 'medical' in domains or 'scientific' in domains:
        # Prioritize academic searcher and verifier for medical/scientific
        for cfg in optional:
            if cfg.type in ('searcher', 'verifier') and 'Scholar Gateway' in str(cfg.tool_access):
                allocated.append(cfg)
                optional.remove(cfg)
                remaining_slots -= 1
                if remaining_slots <= 0:
                    break
    
    # Fill with remaining optional agents
    for cfg in optional[:remaining_slots]:
        allocated.append(cfg)
    
    return allocated
```

## Lead Researcher Implementation

### Strategy Development Phase

```python
async def develop_research_strategy(
    query: str,
    context: dict,
    effort_config: EffortConfig
) -> ResearchPlan:
    """Lead researcher develops comprehensive research strategy."""
    
    # Use extended thinking for strategy development
    strategy_thought = await thoughtbox({
        'thought': f"""
        LEAD RESEARCHER: STRATEGY DEVELOPMENT
        
        Query Analysis:
        - Original query: {query}
        - Detected domains: {detect_domains(query)}
        - Effort level: {effort_config.level.value}
        - Allocated subagents: {effort_config.subagents}
        
        Research Plan Development:
        
        1. DECOMPOSITION
        Break query into sub-questions:
        {decompose_query(query)}
        
        2. DOMAIN MAPPING
        Map sub-questions to domains and required expertise:
        {map_to_domains(query)}
        
        3. EVIDENCE REQUIREMENTS
        Identify evidence types needed:
        - Primary sources: {identify_primary_sources(query)}
        - Secondary sources: {identify_secondary_sources(query)}
        - Verification requirements: {identify_verification_needs(query)}
        
        4. UNCERTAINTY TARGETS
        Define uncertainty handling:
        - Expected high-confidence areas: {identify_high_conf_areas(query)}
        - Expected low-confidence areas: {identify_low_conf_areas(query)}
        - Noise budget allocation: {effort_config.level.value} → {0.25 if effort_config.level == EffortLevel.COMPLEX else 0.2}
        
        5. SUBAGENT TASK DISTRIBUTION
        Assign sub-questions to subagents:
        {distribute_tasks(query, effort_config)}
        
        6. CONVERGENCE CRITERIA
        Define when research is complete:
        - Topology target: |E|/|N| ≥ 4.0
        - Noise budget: ≥ 25% low-confidence elements
        - Coverage: All sub-questions addressed
        - Confidence: Overall ≥ 0.7
        """,
        'thoughtNumber': 1,
        'totalThoughts': effort_config.max_iterations,
        'nextThoughtNeeded': True,
        'includeGuide': True
    })
    
    # Parse strategy into structured plan
    plan = parse_research_plan(strategy_thought)
    
    # Save to memory for context overflow recovery
    await save_plan_to_memory(plan)
    
    return plan
```

### Task Distribution Templates

```python
TASK_DISTRIBUTION_TEMPLATES = {
    'entity_extraction': {
        'description': 'Extract all relevant entities and concepts from {domain}',
        'subagent_type': 'mapper',
        'output_schema': {
            'entities': [{'label': str, 'type': str, 'confidence': float, 'evidence': list}],
            'concepts': [{'label': str, 'definition': str, 'confidence': float}]
        },
        'tool_guidance': 'Use infranodus:getGraphAndStatements for initial extraction',
        'boundaries': 'Focus only on {domain}. Do not extract from unrelated domains.',
        'completion_criteria': 'Return when ≥10 entities extracted or search exhausted'
    },
    
    'relationship_mapping': {
        'description': 'Map relationships between entities: {entity_list}',
        'subagent_type': 'mapper',
        'output_schema': {
            'relationships': [{'source': str, 'target': str, 'type': str, 'strength': float, 'evidence': list}]
        },
        'tool_guidance': 'Use infranodus:getGraphAndAdvice with optimize="develop"',
        'boundaries': 'Only map relationships between provided entities',
        'completion_criteria': 'Return when relationship density ≥ 2 per entity'
    },
    
    'gap_detection': {
        'description': 'Identify structural gaps in knowledge graph for {topic}',
        'subagent_type': 'mapper',
        'output_schema': {
            'gaps': [{'description': str, 'between': list, 'severity': str, 'suggested_search': str}]
        },
        'tool_guidance': 'Use infranodus:getGraphAndAdvice with optimize="gaps", gapDepth=2',
        'boundaries': 'Focus on gaps relevant to original query',
        'completion_criteria': 'Return when ≥3 gaps identified or analysis complete'
    },
    
    'evidence_gathering': {
        'description': 'Gather evidence on: {specific_question}',
        'subagent_type': 'searcher',
        'output_schema': {
            'findings': [{'fact': str, 'source': str, 'source_type': str, 'confidence': float, 'citation': str}],
            'gaps_discovered': [str]
        },
        'tool_guidance': 'Priority: Scholar Gateway > exa:web_search_exa. Max 5 searches.',
        'boundaries': 'Only gather evidence directly relevant to {specific_question}',
        'completion_criteria': 'Return when ≥3 credible sources found or search exhausted'
    },
    
    'claim_verification': {
        'description': 'Verify claim: "{claim}" with confidence {current_confidence}',
        'subagent_type': 'verifier',
        'output_schema': {
            'verification_result': {'verified': bool, 'new_confidence': float, 'supporting_evidence': list, 'contradicting_evidence': list}
        },
        'tool_guidance': 'Search for both supporting AND contradicting evidence',
        'boundaries': 'Verify only the specific claim provided',
        'completion_criteria': 'Return when ≥2 independent sources checked'
    },
    
    'assumption_challenge': {
        'description': 'Challenge assumptions underlying: {claims}',
        'subagent_type': 'skeptic',
        'output_schema': {
            'challenged_assumptions': [{'assumption': str, 'concern': str, 'confidence_impact': float}],
            'missing_falsifiers': [{'claim': str, 'suggested_falsifier': str}]
        },
        'tool_guidance': 'Use Scholar Gateway to find contradicting literature',
        'boundaries': 'Challenge only claims with confidence > 0.7',
        'completion_criteria': 'Return when all high-confidence claims examined'
    },
    
    'uncertainty_quantification': {
        'description': 'Quantify uncertainty for: {elements}',
        'subagent_type': 'uncertainty_quantifier',
        'output_schema': {
            'confidence_updates': [{'element_id': str, 'new_confidence': float, 'rationale': str}],
            'noise_budget_status': {'current': float, 'target': float, 'deficit': float}
        },
        'tool_guidance': 'Base confidence on: source quality, recency, corroboration',
        'boundaries': 'Quantify only provided elements',
        'completion_criteria': 'Return when all elements processed'
    },
    
    'hypothesis_generation': {
        'description': 'Generate structural hypotheses for: {topic}',
        'subagent_type': 'hypothesizer',
        'output_schema': {
            'hypotheses': [{'name': str, 'structure': str, 'rationale': str, 'testable_predictions': list, 'placeholders': list}]
        },
        'tool_guidance': 'Use infranodus:getGraphAndAdvice with optimize="imagine"',
        'boundaries': 'Generate 2-3 alternative hypotheses',
        'completion_criteria': 'Return when ≥2 distinct hypotheses generated'
    }
}

def create_task_assignment(
    template_name: str,
    params: dict,
    subagent_config: SubagentConfig
) -> TaskAssignment:
    """Create a task assignment from template."""
    template = TASK_DISTRIBUTION_TEMPLATES[template_name]
    
    return TaskAssignment(
        task_id=f"{template_name}_{uuid4().hex[:8]}",
        subagent_id=subagent_config.id,
        description=template['description'].format(**params),
        output_schema=template['output_schema'],
        tool_guidance=template['tool_guidance'],
        boundaries=template['boundaries'].format(**params),
        completion_criteria=template['completion_criteria'],
        allowed_tools=subagent_config.tool_access
    )
```

## Subagent Execution Engine

### Isolated Context Execution

```python
async def execute_subagent(
    assignment: TaskAssignment,
    scaffold_context: dict
) -> SubagentResult:
    """Execute subagent with isolated context and NoisyGraph integration."""
    
    # Build subagent system prompt
    system_prompt = f"""
    ## Subagent Role: {assignment.subagent_id}
    
    You are a specialized research subagent operating within the NoisyGraph reasoning framework.
    
    ### Task
    {assignment.description}
    
    ### Output Format
    Return ONLY valid JSON matching this schema:
    ```json
    {json.dumps(assignment.output_schema, indent=2)}
    ```
    
    ### Tool Guidance
    {assignment.tool_guidance}
    
    ### Boundaries
    {assignment.boundaries}
    
    ### Completion Criteria
    {assignment.completion_criteria}
    
    ### Uncertainty Requirements
    For ALL findings:
    1. Rate confidence 0.0-1.0 based on:
       - Source quality (peer-reviewed: +0.2, blog: -0.1)
       - Recency (within 1yr: +0.1, >5yr: -0.1)
       - Corroboration (multiple sources: +0.2)
    2. Explicitly note assumptions
    3. Flag low-confidence elements (≤0.5) - these contribute to noise budget
    4. Include evidence provenance (source URLs, DOIs)
    
    ### Current Context
    {json.dumps(scaffold_context, indent=2)}
    """
    
    # Execute with interleaved thinking
    result = await execute_with_extended_thinking(
        system_prompt=system_prompt,
        tools=assignment.allowed_tools,
        max_tool_calls=10
    )
    
    # Parse and validate result
    parsed = parse_subagent_output(result, assignment.output_schema)
    
    return SubagentResult(
        task_id=assignment.task_id,
        subagent_id=assignment.subagent_id,
        output=parsed,
        tool_calls_made=result.tool_call_count,
        confidence=calculate_result_confidence(parsed)
    )
```

### Parallel Execution Coordinator

```python
async def execute_subagents_parallel(
    assignments: List[TaskAssignment],
    scaffold: NoisyGraphScaffold,
    event_bus: EventBus
) -> List[SubagentResult]:
    """Coordinate parallel subagent execution with event tracking."""
    
    # Extract minimal context for subagents (prevent context overflow)
    scaffold_context = extract_minimal_context(scaffold)
    
    # Emit spawn events
    for assignment in assignments:
        await event_bus.publish({
            'type': 'nlr.subagent.spawned',
            'source': 'lead_researcher',
            'payload': {
                'subagent_id': assignment.subagent_id,
                'task_id': assignment.task_id,
                'task_type': assignment.description[:50]
            }
        })
    
    # Execute in parallel with timeout
    try:
        results = await asyncio.wait_for(
            asyncio.gather(*[
                execute_subagent(assignment, scaffold_context)
                for assignment in assignments
            ], return_exceptions=True),
            timeout=120  # 2 minute timeout for all subagents
        )
    except asyncio.TimeoutError:
        # Partial results on timeout
        results = [SubagentResult.timeout() for _ in assignments]
    
    # Process results and emit completion events
    valid_results = []
    for assignment, result in zip(assignments, results):
        if isinstance(result, Exception):
            await event_bus.publish({
                'type': 'nlr.subagent.failed',
                'source': 'lead_researcher',
                'payload': {
                    'subagent_id': assignment.subagent_id,
                    'error': str(result)
                }
            })
        else:
            await event_bus.publish({
                'type': 'nlr.subagent.completed',
                'source': 'lead_researcher',
                'payload': {
                    'subagent_id': assignment.subagent_id,
                    'task_id': assignment.task_id,
                    'confidence': result.confidence
                }
            })
            valid_results.append(result)
    
    return valid_results
```

## CLAUDE.md Integration

For automatic injection of NoisyGraph reasoning framework into all research sessions:

```markdown
# CLAUDE.md - NoisyGraph Reasoning Framework

## Core Principles

When performing complex reasoning or research tasks, apply the NoisyGraph framework:

### 1. Uncertainty First
- Every claim must have explicit confidence (0-1)
- Maintain noise budget: ≥25% elements with confidence ≤0.5
- Represent gaps as placeholder nodes
- Include falsifiability markers for claims

### 2. Graph-Based Reasoning
- Build knowledge as nodes (entities, concepts) and edges (relationships)
- Target topology: |edges|/|nodes| ≥ 4
- Track evidence provenance for all elements
- Use infranodus for structural gap detection

### 3. Multi-Perspective Analysis
- Always spawn skeptic analysis for high-confidence claims
- Generate alternative hypotheses
- Seek contradicting evidence, not just supporting

### 4. Effort Scaling
| Query Complexity | Subagents | Tool Calls | Iterations |
|-----------------|-----------|------------|------------|
| Simple          | 1         | 3-10       | 3          |
| Moderate        | 2-4       | 10-30      | 5          |
| Complex         | 5-10      | 30-100     | 9          |

### 5. Checkpointing
Save state every 2-3 iterations for context overflow recovery.

## Triggers
- `/nlr`, `/reason`, `/think-deep`: Full NoisyGraph workflow
- `/compact`: Abbreviated output
- `/semantic`: Rich graph exploration
- `/research [topic]`: Full orchestrator-worker pattern
```

## Citation Processing

```python
async def process_citations(
    synthesis: str,
    evidence_sources: List[Evidence]
) -> CitedSynthesis:
    """Process citations for proper attribution."""
    
    # Build citation index
    citation_index = {}
    for i, source in enumerate(evidence_sources):
        citation_key = f"[{i+1}]"
        citation_index[citation_key] = {
            'title': source.title,
            'url': source.url,
            'doi': source.doi,
            'authors': source.authors,
            'year': source.year
        }
    
    # Use extended thinking for citation placement
    cited = await thoughtbox({
        'thought': f"""
        CITATION PROCESSING
        
        Original Synthesis:
        {synthesis}
        
        Available Sources:
        {json.dumps(citation_index, indent=2)}
        
        Task: Insert appropriate citation markers [N] after claims that require attribution.
        
        Rules:
        1. Cite after specific facts, statistics, or quotes
        2. Do not cite general knowledge or reasoning
        3. Prefer multiple citations for contested claims
        4. Ensure each citation is actually used
        
        Cited Synthesis:
        [Insert citations appropriately]
        """,
        'thoughtNumber': 1,
        'totalThoughts': 1,
        'nextThoughtNeeded': False
    })
    
    return CitedSynthesis(
        text=cited.content,
        citations=citation_index
    )
```

## Integration with Existing Skills

### Think Skill Integration

```python
# Interleaved thinking pattern for lead researcher
async def lead_researcher_reasoning_loop(
    scaffold: NoisyGraphScaffold,
    iteration: int
) -> None:
    """Lead researcher reasoning with think skill integration."""
    
    # Strategy update with mental model
    model = await mental_models({
        'operation': 'get_model',
        'args': {'model': select_model_for_iteration(iteration)}
    })
    
    # Apply model in thoughtbox
    await thoughtbox({
        'thought': f"""
        ITERATION {iteration}: Applying {model.name}
        
        {model.process}
        
        Current scaffold state:
        - Nodes: {len(scaffold.graph.nodes)}
        - Edges: {len(scaffold.graph.edges)}
        - Open gaps: {count_open_gaps(scaffold)}
        
        Next actions based on {model.name}:
        {apply_model(model, scaffold)}
        """,
        'thoughtNumber': iteration,
        'totalThoughts': scaffold.meta.iteration_limit,
        'nextThoughtNeeded': True
    })
```

### Agent-Core Integration

```typescript
// Event definitions for research orchestration
const researchOrchestratorConfig: SkillEventSystemConfig<'research-orchestrator'> = {
    skillName: 'research-orchestrator',
    displayName: 'RESEARCH-ORCHESTRATOR',
    groups: {
        strategy: defineEventGroup('strategy', {
            plan_created: event('plan_created'),
            effort_scaled: event('effort_scaled'),
            iteration_started: event('iteration_started')
        }),
        subagent: defineEventGroup('subagent', {
            spawned: event('spawned'),
            completed: event('completed'),
            failed: criticalEvent('failed'),
            result_integrated: event('result_integrated')
        }),
        checkpoint: defineEventGroup('checkpoint', {
            saved: event('saved'),
            restored: event('restored')
        }),
        synthesis: defineEventGroup('synthesis', {
            started: event('started'),
            citations_processed: event('citations_processed'),
            completed: event('completed')
        })
    },
    subscriptions: [
        { eventType: 'nlr.reasoning.started', handler: 'handleReasoningStart' },
        { eventType: 'task.research_request', handler: 'handleResearchRequest' }
    ]
};
```

## Performance Metrics

Based on Anthropic's research system benchmarks:

| Metric | Single Agent | Multi-Agent (Orchestrator-Worker) |
|--------|--------------|-----------------------------------|
| Quality Score | 1.0x baseline | 1.9x (90.2% improvement) |
| Token Usage | 1x | ~15x |
| Time | Variable | Predictable (effort-scaled) |
| Failure Rate | Higher | Lower (parallel redundancy) |

Token usage explains 80% of performance variance—multi-agent research is computationally expensive but significantly more capable.

## Limitations

Current limitations based on available APIs:

1. **No direct Research Mode access**: The internal `launch_extended_search_task` is not exposed
2. **No built-in subagent spawning**: Must implement via SDK patterns
3. **No automatic CitationAgent**: Must implement citation processing manually
4. **Context limits**: 200K token limit requires checkpointing for complex research

These limitations are addressed through the patterns documented above.
