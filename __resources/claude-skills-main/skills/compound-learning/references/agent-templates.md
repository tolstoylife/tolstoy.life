# Agent Templates for Compound Learning

> Templates for implementing phase-specific agents in the compound loop.

## Agent Structure

Each agent follows a consistent structure:

```yaml
agent:
  name: string
  phase: PLAN | EXECUTE | ASSESS | COMPOUND
  role: string  # What this agent does
  inputs: [string]  # What it receives
  outputs: [string]  # What it produces
  tools: [string]  # MCP tools it uses
  skills: [string]  # Skills it references
  parallelizable: boolean  # Can run alongside others
```

## PLAN Phase Agents

### Context Analyzer

```yaml
name: context-analyzer
phase: PLAN
role: Extract problem structure, constraints, and goals from current context
parallelizable: true

inputs:
  - task_description: "User's request/problem statement"
  - conversation_history: "Prior context"
  - attached_files: "Any uploaded documents"

outputs:
  - problem_statement: "Clarified, structured problem"
  - constraints: "Hard requirements, boundaries"
  - goals: "Success criteria"
  - unknowns: "Information gaps"

procedure:
  1. Parse task description for explicit requirements
  2. Extract implicit constraints from context
  3. Identify success criteria (how we know we're done)
  4. Flag ambiguities requiring clarification
  5. Produce structured context object

tools:
  - conversation_search: Recall related past discussions
  - google_drive_search: Find relevant internal docs

skills:
  - reason: For decomposition
  - hierarchical-reasoning: S→T→O structure
```

### Domain Researcher

```yaml
name: domain-researcher
phase: PLAN
role: Gather domain standards, best practices, current state of art
parallelizable: true

inputs:
  - problem_domain: "Area of work"
  - specific_topics: "Key concepts to research"
  - depth: MINIMAL | MORE | COMPREHENSIVE

outputs:
  - best_practices: "Recommended approaches"
  - common_pitfalls: "Things to avoid"
  - resources: "Relevant documentation, examples"
  - current_standards: "State of the art"

procedure:
  1. Identify authoritative sources for domain
  2. Search for best practices, patterns
  3. Find common failure modes, antipatterns
  4. Gather concrete examples of good work
  5. Synthesize into actionable guidance

tools:
  - web_search: External research
  - context7: Framework documentation
  - infranodus: Gap detection

skills:
  - think: Mental models for domain
```

### History Analyzer

```yaml
name: history-analyzer
phase: PLAN
role: Find relevant past solutions and patterns from knowledge base
parallelizable: true

inputs:
  - problem_signature: "Key characteristics"
  - domain: "Area of work"
  - knowledge_base_path: "docs/solutions/**/*.md"

outputs:
  - related_solutions: "Past problems similar to this"
  - applicable_patterns: "Reusable approaches"
  - warnings: "Past mistakes to avoid"
  - cross_references: "Connected knowledge"

procedure:
  1. Generate search queries from problem signature
  2. Search knowledge base for matching frontmatter
  3. Rank by relevance (problem_type, component, symptoms)
  4. Extract applicable patterns and warnings
  5. Build cross-reference map

tools:
  - conversation_search: Past discussions
  - bash_tool: grep/search knowledge base files

skills:
  - memory: Recall relevant context
  - graph: Navigate knowledge topology
```

### Gap Analyzer

```yaml
name: gap-analyzer
phase: PLAN
role: Identify unknowns, risks, and dependencies
parallelizable: true

inputs:
  - context_analysis: "From context-analyzer"
  - domain_research: "From domain-researcher"
  - history_analysis: "From history-analyzer"

outputs:
  - knowledge_gaps: "What we don't know"
  - risks: "What could go wrong"
  - dependencies: "What we need before/during execution"
  - questions: "Clarifications needed"

procedure:
  1. Compare requirements against known solutions
  2. Identify areas without coverage
  3. Assess risk of each unknown
  4. Map dependencies (blocking vs. parallel)
  5. Generate prioritized question list

tools:
  - infranodus: generateContentGaps, generateResearchQuestions

skills:
  - critique: Multi-lens gap analysis
  - hierarchical-reasoning: Risk stratification
```

## EXECUTE Phase Agents

### Task Executor

```yaml
name: task-executor
phase: EXECUTE
role: Implement plan while tracking decisions and obstacles
parallelizable: false  # Sequential execution

inputs:
  - plan: "Structured plan from PLAN phase"
  - context: "Current state"
  - tools_available: "Execution capabilities"

outputs:
  - deliverables: "Task outputs"
  - execution_log: "Decisions, blockers, deviations"
  - time_actual: "Actual duration"

procedure:
  1. Parse plan into executable steps
  2. For each step:
     a. Execute action
     b. Log decisions made
     c. Note any blockers encountered
     d. Track deviations from plan
  3. Verify step completion before next
  4. Produce deliverables and metadata

tools:
  - bash_tool: Command execution
  - create_file: Output generation
  - str_replace: Iterative refinement

decision_log_schema:
  - timestamp: ISO-8601
  - step: "Which plan step"
  - decision: "What was decided"
  - rationale: "Why"
  - alternatives_considered: [string]
```

### Progress Tracker

```yaml
name: progress-tracker
phase: EXECUTE
role: Monitor execution, flag issues, suggest adjustments
parallelizable: true  # Runs alongside executor

inputs:
  - plan: "Expected steps and timeline"
  - execution_stream: "Live execution state"

outputs:
  - status_updates: "Progress reports"
  - deviation_alerts: "Plan vs. actual discrepancies"
  - adjustment_suggestions: "Course corrections"

procedure:
  1. Compare expected vs. actual progress
  2. Calculate completion percentage
  3. Identify steps taking longer than expected
  4. Flag blockers requiring intervention
  5. Suggest plan adjustments if needed

alert_thresholds:
  - step_overrun: 1.5x estimated time
  - blocker_duration: 10 minutes stuck
  - deviation_significance: Major requirement change
```

## ASSESS Phase Agents

### Quality Reviewer

```yaml
name: quality-reviewer
phase: ASSESS
role: Evaluate output against requirements
parallelizable: true

inputs:
  - deliverables: "Task outputs"
  - requirements: "From plan"
  - acceptance_criteria: "Success definition"

outputs:
  - quality_score: 0.0-1.0
  - requirements_met: [boolean per requirement]
  - defects: [description of issues]
  - strengths: [what worked well]

procedure:
  1. Map deliverables to requirements
  2. Verify each acceptance criterion
  3. Identify defects (unmet requirements)
  4. Note unexpected strengths
  5. Calculate overall quality score

quality_dimensions:
  - correctness: "Does it work?"
  - completeness: "Is it done?"
  - robustness: "Does it handle edge cases?"
  - maintainability: "Can it be sustained?"
```

### Pattern Detector

```yaml
name: pattern-detector
phase: ASSESS
role: Identify reusable patterns from execution
parallelizable: true

inputs:
  - execution_log: "Decisions, approaches taken"
  - deliverables: "What was produced"
  - similar_past_work: "Related knowledge base entries"

outputs:
  - patterns_detected: [Pattern objects]
  - abstraction_candidates: "Patterns worth codifying"
  - novelty_assessment: "Is this new knowledge?"

procedure:
  1. Analyze execution log for recurring decisions
  2. Compare approaches to past work
  3. Identify techniques that worked well
  4. Assess abstraction potential (frequency × impact)
  5. Flag novel patterns for compound phase

pattern_schema:
  name: string
  description: string
  context: "When to use"
  approach: "How to apply"
  frequency: int  # Times observed
  success_rate: float
  abstractable: boolean
```

### Gap Identifier

```yaml
name: gap-identifier
phase: ASSESS
role: Find missing cases, edge conditions, coverage gaps
parallelizable: true

inputs:
  - deliverables: "What was produced"
  - requirements: "What was specified"
  - domain_knowledge: "Standard expectations"

outputs:
  - coverage_gaps: [string]
  - edge_cases_missed: [string]
  - implicit_assumptions: [string]
  - suggested_additions: [string]

procedure:
  1. Enumerate possible cases in domain
  2. Check which cases are covered
  3. Identify edge cases not handled
  4. Surface implicit assumptions
  5. Prioritize gaps by risk

tools:
  - infranodus: generateContentGaps

skills:
  - critique: ADVERSARIAL lens
```

### Risk Analyzer

```yaml
name: risk-analyzer
phase: ASSESS
role: Evaluate safety, security, reliability
parallelizable: true

inputs:
  - deliverables: "Outputs to analyze"
  - domain: "Area (determines risk categories)"
  - context: "How it will be used"

outputs:
  - risks_identified: [Risk objects]
  - severity_assessment: "Overall risk level"
  - mitigations_suggested: [string]

procedure:
  1. Apply domain-specific risk checklist
  2. Assess each risk dimension
  3. Prioritize by severity × likelihood
  4. Generate mitigation strategies
  5. Flag showstoppers

risk_dimensions_by_domain:
  Coding: [security, performance, reliability, maintainability]
  Learning: [misconception, decay, transfer_failure]
  Writing: [misinterpretation, offense, factual_error]
  Research: [bias, invalid_inference, ethics]
```

## COMPOUND Phase Agents

### Solution Extractor

```yaml
name: solution-extractor
phase: COMPOUND
role: Identify and articulate the working solution
parallelizable: true

inputs:
  - execution_log: "What was done"
  - deliverables: "What was produced"
  - problem_statement: "What was solved"

outputs:
  - solution_summary: "Concise description"
  - solution_steps: "How to replicate"
  - code_examples: "Concrete implementations"
  - key_insights: "Why it worked"

procedure:
  1. Identify the core solution approach
  2. Extract replicable steps
  3. Isolate key code/content examples
  4. Articulate why this worked
  5. Format for documentation

output_format: |
  ## Solution
  
  {solution_summary}
  
  ### Steps
  {numbered_steps}
  
  ### Key Code/Example
  ```{language}
  {example}
  ```
  
  ### Why This Works
  {explanation}
```

### Prevention Strategist

```yaml
name: prevention-strategist
phase: COMPOUND
role: Develop strategies to prevent recurrence
parallelizable: true

inputs:
  - problem_statement: "What went wrong"
  - root_cause: "Why it happened"
  - solution: "How it was fixed"

outputs:
  - prevention_strategies: [string]
  - early_warning_signs: "How to catch early"
  - test_cases: "Verification approaches"
  - best_practices: "Ongoing guidance"

procedure:
  1. Analyze root cause chain
  2. Identify intervention points
  3. Design prevention measures
  4. Create early detection criteria
  5. Generate test cases

output_format: |
  ## Prevention
  
  ### How to Avoid
  {prevention_strategies}
  
  ### Early Warning Signs
  {early_warning_signs}
  
  ### Test Cases
  {test_cases}
```

### Category Classifier

```yaml
name: category-classifier
phase: COMPOUND
role: Determine optimal storage location and metadata
parallelizable: true

inputs:
  - problem_analysis: "What was the problem"
  - domain: "Area of work"
  - existing_categories: "Current docs/solutions/ structure"

outputs:
  - category: "Folder path"
  - filename: "Document name"
  - tags: [string]
  - related_docs: [paths to cross-reference]

procedure:
  1. Match problem to domain schema
  2. Select most specific applicable category
  3. Generate descriptive filename
  4. Assign searchable tags
  5. Identify related existing docs

naming_convention: |
  {domain}/{problem_type}/{component}-{brief-description}.md
  
  Examples:
  coding/performance/api-n-plus-one-query.md
  learning/retention/renal-tubular-function.md
  writing/structure/persuasive-essay-thesis.md
```

### Documentation Writer

```yaml
name: documentation-writer
phase: COMPOUND
role: Assemble complete documentation with frontmatter
parallelizable: false  # Depends on other compound agents

inputs:
  - frontmatter_skeleton: "From context-extractor"
  - solution_content: "From solution-extractor"
  - prevention_content: "From prevention-strategist"
  - category_info: "From category-classifier"
  - related_docs: "From related-finder"

outputs:
  - complete_document: "Full markdown with frontmatter"
  - file_path: "Where to save"

procedure:
  1. Validate all inputs present
  2. Assemble YAML frontmatter
  3. Construct document sections
  4. Add cross-references
  5. Validate against schema
  6. Write to file system

document_structure: |
  ---
  {yaml_frontmatter}
  ---
  
  # {title}
  
  ## Problem
  {problem_description}
  
  ## Investigation
  {investigation_steps}
  
  ## Solution
  {solution_content}
  
  ## Prevention
  {prevention_content}
  
  ## Related
  {cross_references}

tools:
  - create_file: Write documentation
  
skills:
  - obsidian-markdown: Proper formatting
```

## Parallelization Matrix

```
PLAN Phase:
┌───────────────────┐ ┌──────────────────┐ ┌─────────────────┐ ┌──────────────┐
│ context-analyzer  │ │ domain-researcher│ │ history-analyzer│ │ gap-analyzer │
└─────────┬─────────┘ └────────┬─────────┘ └────────┬────────┘ └──────┬───────┘
          └──────────────────┬─┴───────────────────┬┘                 │
                             ▼                     ▼                   │
                        plan-synthesizer ◀────────────────────────────┘

EXECUTE Phase:
┌───────────────────┐ ┌───────────────────┐
│  task-executor    │ │  progress-tracker │
│   (sequential)    │ │    (parallel)     │
└───────────────────┘ └───────────────────┘

ASSESS Phase:
┌────────────────┐ ┌──────────────────┐ ┌───────────────┐ ┌───────────────┐
│quality-reviewer│ │ pattern-detector │ │ gap-identifier│ │ risk-analyzer │
└───────┬────────┘ └────────┬─────────┘ └───────┬───────┘ └───────┬───────┘
        └──────────────────┬┴──────────────────┬┘                 │
                           ▼                   ▼                   │
                      assess-synthesizer ◀────────────────────────┘

COMPOUND Phase:
┌──────────────────┐ ┌─────────────────────┐ ┌───────────────────┐
│solution-extractor│ │prevention-strategist│ │category-classifier│
└────────┬─────────┘ └──────────┬──────────┘ └─────────┬─────────┘
         └──────────────────────┴──────────────────────┘
                                ▼
                      documentation-writer (waits for above)
```

## Implementation Notes

### Spawning Parallel Agents

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_parallel_agents(agents: list, inputs: dict) -> dict:
    """Run parallelizable agents concurrently."""
    results = {}
    
    with ThreadPoolExecutor(max_workers=len(agents)) as executor:
        futures = {
            executor.submit(agent.run, inputs): agent.name 
            for agent in agents 
            if agent.parallelizable
        }
        
        for future in as_completed(futures):
            agent_name = futures[future]
            results[agent_name] = future.result()
    
    # Run sequential agents after
    for agent in agents:
        if not agent.parallelizable:
            results[agent.name] = agent.run({**inputs, **results})
    
    return results
```

### Agent Communication

Agents communicate through structured outputs that become inputs for downstream agents:

```python
@dataclass
class AgentOutput:
    agent_name: str
    timestamp: datetime
    outputs: dict
    confidence: float
    metadata: dict
```
