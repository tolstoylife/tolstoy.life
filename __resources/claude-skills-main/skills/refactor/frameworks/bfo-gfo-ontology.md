# BFO/GFO Ontology Integration

## Principle

**BFO** (Basic Formal Ontology) and **GFO** (General Formal Ontology) are top-level ontologies that provide complementary perspectives for modeling systems:

- **BFO**: Entity-focused ontology for scientific domains - classifies **what things ARE** (continuants and occurrents)
- **GFO**: System-focused ontology for conceptual modeling - classifies **what things DO** (functions and processes)

**Core Principle**: Use multi-perspective recursive integrative inference to bridge the tension between entity-view (BFO) and function-view (GFO), preserving both viewpoints without reduction.

**Integration Goal**: Model Claude Code architecture with precision by recognizing that components like skills and agents are simultaneously:
1. **Entities** (BFO) - persistent, versioned, identifiable objects
2. **Functional Systems** (GFO) - capability providers with defined purposes

## BFO Taxonomy (Code Entities)

### Continuants (Entities that persist through time)

**Independent Continuants:**
```yaml
skill:
  definition: "Self-contained capability module"
  properties: [name, description, allowed-tools, model, context]
  persistence: "Exists across sessions, modified through versions"

agent:
  definition: "Autonomous execution context"
  properties: [name, description, tools, model, permissionMode, skills, hooks]
  persistence: "Instantiated per delegation, configuration persists"

command:
  definition: "User-invocable slash command"
  properties: [description, allowed-tools, model, argument-hint]
  persistence: "Defined statically, invoked dynamically"

hook:
  definition: "Lifecycle event handler"
  properties: [event, matcher, type, command]
  persistence: "Registered at startup, triggered per event"
```

**Dependent Continuants:**
```yaml
frontmatter:
  definition: "YAML metadata block"
  depends_on: skill | agent | command
  qualities: [official_compliance, token_count, complexity]

body:
  definition: "Markdown content after frontmatter"
  depends_on: skill | agent
  qualities: [readability, token_count, documentation_quality]

reference:
  definition: "Link to another component"
  depends_on: skill | agent
  types: [@import, skill_name, agent_name, file_path]
```

### Occurrents (Processes that occur in time)

**Processes:**
```yaml
execution:
  definition: "Skill or agent actively running"
  phases: [initialization, routing, processing, completion]
  duration: milliseconds to minutes

validation:
  definition: "Component compliance checking"
  phases: [scan, analyze, report]
  participants: [evaluator_agent, target_component]

optimization:
  definition: "Architecture improvement process"
  phases: [evaluate, propose, reconcile, implement, verify]
  participants: [refactor_agent, target_components]
```

**Temporal Regions:**
```yaml
session:
  definition: "Single user interaction with Claude Code"
  boundaries: [SessionStart, SessionEnd]
  contains: [user_prompts, tool_invocations, agent_delegations]

iteration:
  definition: "Ralph Loop cycle"
  boundaries: [task_start, done_promise | max_iterations]
  contains: [test_loops, fix_plans, done_signals]

epoch:
  definition: "Significant architecture state"
  boundaries: [major_refactor, version_release]
  contains: [multiple_sessions, cumulative_changes]
```

## GFO Taxonomy (Systems and Relations)

### Systems

**Structural Systems:**
```yaml
architecture:
  definition: "Overall organization of ~/.claude"
  components: [skills, agents, commands, hooks, rules]
  structure: "Hierarchical directory tree"

hierarchy:
  definition: "Parent-child relationships"
  examples:
    - "meta-router → delegate-router → specific agents"
    - "refactor-agent → evaluator subagents"
    - "learn skill → shared compound operations"

graph:
  definition: "Network of dependencies"
  nodes: [skills, agents, files]
  edges: [depends_on, references, imports]
  metrics: [PageRank, Betweenness, HITS]
```

**Functional Systems:**
```yaml
router:
  definition: "Component selection mechanism"
  function: "Map user intent → appropriate skill/agent"
  examples: [meta-router, delegate-router, tools-router]

orchestrator:
  definition: "Multi-component coordination"
  function: "Manage complex workflows across agents"
  examples: [refactor-agent, git-orchestrator, ultrawork-agent]

evaluator:
  definition: "Compliance and quality assessment"
  function: "Scan, analyze, report, recommend"
  examples: [10 refactor evaluators, component-architect]
```

### Relations

**Parthood:**
```yaml
skill_contains_frontmatter:
  type: has_proper_part
  example: "refactor/SKILL.md contains YAML frontmatter"

skill_contains_body:
  type: has_proper_part
  example: "refactor/SKILL.md contains markdown documentation"

agent_contains_hooks:
  type: has_proper_part
  example: "refactor-agent.md contains PreToolUse and PostToolUse hooks"
```

**Dependency:**
```yaml
agent_requires_skill:
  type: depends_on
  example: "refactor-agent requires component-architect, learn, code skills"

skill_requires_tool:
  type: depends_on
  example: "refactor skill requires Task, Read, Write, Edit tools"

hook_requires_script:
  type: depends_on
  example: "SessionStart hook requires session-start.sh script"
```

**Causation:**
```yaml
hook_triggers_action:
  type: causes
  example: "PostToolUse(Write) → track-change.sh → pending-changes.jsonl updated"

agent_invokes_tool:
  type: causes
  example: "refactor-agent → Task tool → evaluator subagent spawned"

optimization_improves_metric:
  type: causes
  example: "meta-dispatcher pattern → 70% latency reduction"
```

## Tension Bridging (Multi-Perspective Integration)

### Problem: BFO vs GFO Conflicting Views

**BFO**: "A skill is an independent continuant (entity)"
**GFO**: "A skill is a functional system (capability provider)"

**Resolution: Multi-Perspective Recursive Integrative Inference**

```yaml
skill_unified_view:
  bfo_perspective:
    category: independent_continuant
    persistence: across_sessions
    qualities: [name, description, token_count]

  gfo_perspective:
    category: functional_system
    function: capability_provision
    structure: [frontmatter, body, references]

  integrated_view:
    definition: "A skill is both an entity (BFO) and a functional system (GFO)"
    ontological_commitment: "Entity-function duality"
    practical_implication:
      - "Entity view: Version control, file management"
      - "Function view: Routing, delegation, execution"
```

### Method: Recursive Integration

```python
def integrate_perspectives(component, bfo_view, gfo_view):
    """
    Multi-perspective recursive integrative inference.
    Preserves both viewpoints without reduction.
    """
    return {
        'bfo': bfo_view,  # Entity-focused
        'gfo': gfo_view,  # System-focused
        'unified': {
            'entity_properties': bfo_view.properties,
            'functional_properties': gfo_view.function,
            'interaction_patterns': analyze_causation(component),
            'lifecycle': combine_temporal_regions(bfo_view, gfo_view)
        }
    }
```

## Practical Applications

### 1. Component Classification

```yaml
# Use BFO to classify what something IS
component_bfo_type:
  - skill → independent_continuant
  - agent → independent_continuant
  - execution → process
  - session → temporal_region

# Use GFO to classify what something DOES
component_gfo_type:
  - meta-router → router (functional_system)
  - refactor-agent → orchestrator (functional_system)
  - claude-md-evaluator → evaluator (functional_system)
```

### 2. Dependency Analysis

```yaml
# Use GFO relations to trace dependencies
dependency_graph:
  - refactor-agent depends_on component-architect skill
  - component-architect skill depends_on Read, Edit, Bash tools
  - Bash tool depends_on system shell

# Use BFO parthood to analyze composition
composition_tree:
  - refactor-agent has_proper_part hooks
  - hooks has_proper_part PreToolUse matcher
  - PreToolUse matcher has_proper_part refactor-validation.sh reference
```

### 3. Invariant Validation

```yaml
# BFO-based invariants
continuant_persistence:
  rule: "Independent continuants must have unique identifiers"
  validation: "Check all skills/agents have unique names"

# GFO-based invariants
system_function:
  rule: "Functional systems must have defined purpose"
  validation: "Check all routers/orchestrators have clear function"

# Integrated invariants
entity_function_duality:
  rule: "Every persistent entity provides function, every function requires entity"
  validation: "Skills (entities) provide capabilities (functions), both must exist"
```

## Application

### Refactor Agent Usage

The BFO/GFO framework guides refactor agent evaluations:

**1. Entity Classification (BFO)**:
```python
# Classify components by ontological type
def classify_component(file_path):
    if file_path.suffix == '.md' and 'skills' in file_path.parts:
        return 'independent_continuant'  # Skill entity
    elif 'hooks' in file_path.parts:
        return 'dependent_continuant'    # Hook depends on script
    # ...
```

**2. Functional Analysis (GFO)**:
```python
# Classify components by functional role
def analyze_function(component):
    if component.name.endswith('-router'):
        return 'router'  # Intent → component mapping
    elif component.name.endswith('-agent'):
        return 'orchestrator' if has_subagents(component) else 'executor'
    # ...
```

**3. Dependency Validation**:
```yaml
# Use GFO relations to validate dependencies
validation_rules:
  - agent_requires_skill: Check all agent.skills exist
  - skill_requires_tool: Check all skill.allowed-tools available
  - hook_requires_script: Check all hook.command paths valid
```

**4. Invariant Enforcement**:
```yaml
# BFO invariant: Entity uniqueness
entity_uniqueness:
  check: "All independent continuants have unique identifiers"
  violation: "Two skills with name 'refactor' found"

# GFO invariant: Functional coherence
functional_coherence:
  check: "Routers must have clear routing logic"
  violation: "meta-router lacks intent classification"

# Integrated invariant: Entity-function duality
entity_function_duality:
  check: "Every entity provides function, every function requires entity"
  example: "Skill 'refactor' (entity) provides architecture optimization (function)"
```

### Architecture Optimization

Use ontological typing to guide optimization decisions:

**BFO Perspective** (What to keep/archive):
- **Independent Continuants**: Version control, archive if unused >90 days
- **Dependent Continuants**: Remove if parent entity archived
- **Processes**: Profile performance, optimize bottlenecks
- **Temporal Regions**: Session lifecycle, iteration tracking

**GFO Perspective** (How to improve):
- **Routers**: Optimize intent classification accuracy
- **Orchestrators**: Reduce coordination overhead via graph analysis
- **Evaluators**: Parallelize independent evaluations

**Integrated Approach**:
```yaml
optimization_strategy:
  bfo_analysis:
    - Identify unused independent continuants → candidates for archival
    - Track process durations → identify slow occurrents

  gfo_analysis:
    - Measure router accuracy → improve classification logic
    - Analyze orchestrator complexity → simplify coordination

  integrated_decision:
    - Archive entity (BFO) if function (GFO) is redundant
    - Preserve entity if unique function exists
    - Optimize process if function is critical but slow
```

## References

- **BFO**: Smith et al., "The OBO Foundry: coordinated evolution of ontologies"
- **GFO**: Herre et al., "General Formal Ontology (GFO)"
- **Multi-Perspective Integration**: Guarino, "Formal Ontology in Information Systems"
- **Tension Bridging**: Our novel contribution - recursive integrative inference
