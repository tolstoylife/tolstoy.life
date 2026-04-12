# Integration Patterns for Compound Learning

> How compound-learning composes with other skills in the λο.τ ecosystem.

## Core Composition Algebra

```haskell
-- Basic operators
(∘) :: (β → γ) → (α → β) → (α → γ)      -- Sequential: do then do
(⊗) :: (α → β) → (α → γ) → (α → (β,γ))  -- Parallel: do simultaneously
fix :: (α → α) → α                        -- Recursive: repeat until done
(|) :: (α → β) → (α → Bool) → (α → Maybe β)  -- Conditional: if then do

-- Compound learning as composition
compound_loop = compound ∘ assess ∘ execute ∘ plan

-- With knowledge threading
λ(ο,Κ).τ = emit ∘ validate ∘ (compound ⊗ update_Κ) ∘ assess ∘ execute ∘ plan(Κ)
```

## Skill Integration Map

```
                              ┌─────────────────────────────────────────────┐
                              │           compound-learning                  │
                              │  Plan → Execute → Assess → Compound          │
                              └─────────────────────────────────────────────┘
                                      │           │          │
           ┌──────────────────────────┼───────────┼──────────┼───────────────┐
           │                          │           │          │               │
           ▼                          ▼           ▼          ▼               ▼
    ┌──────────────┐           ┌──────────┐ ┌─────────┐ ┌─────────┐   ┌──────────┐
    │    reason    │           │  think   │ │critique │ │  graph  │   │  memory  │
    │ parse→branch │           │ box ⊗    │ │ multi-  │ │ η≥4     │   │ persist  │
    │ →reduce→emit │           │ models   │ │ lens    │ │ validate│   │ recall   │
    └──────────────┘           └──────────┘ └─────────┘ └─────────┘   └──────────┘
           │                          │           │          │               │
           │                          │           │          │               │
           ▼                          ▼           ▼          ▼               ▼
    ┌──────────────┐           ┌──────────┐ ┌─────────┐ ┌─────────┐   ┌──────────┐
    │hierarchical- │           │infranodus│ │  abduct │ │ ontolog │   │   skill  │
    │  reasoning   │           │ gaps,    │ │ refactor│ │ λο.τ    │   │ -updater │
    │   S→T→O      │           │ questions│ │ schema  │ │ formal  │   │ improve  │
    └──────────────┘           └──────────┘ └─────────┘ └─────────┘   └──────────┘
```

## Phase-Specific Integrations

### PLAN Phase

```haskell
-- Plan phase composition
plan :: (Query, Knowledge) → Plan
plan(q, Κ) = synthesize ∘ (
    context_analyze ⊗ 
    domain_research ⊗ 
    history_recall(Κ) ⊗ 
    gap_detect
)

-- With skill integrations
plan_with_skills = 
    hierarchical_reasoning.S_T_O ∘     -- Structure the plan
    reason.decompose ∘                  -- Break into parts
    (
        think.mental_models ⊗           -- Apply relevant models
        infranodus.gaps ⊗               -- Detect knowledge gaps
        memory.recall(Κ)                -- Retrieve past learnings
    )
```

**Skill compositions:**

| Skill | Function | Integration Point |
|-------|----------|-------------------|
| `reason` | Decompose problem | context-analyzer |
| `hierarchical-reasoning` | S→T→O structure | plan synthesis |
| `think` | Mental models | domain research |
| `infranodus` | Gap detection | gap-analyzer |
| `memory` | Knowledge recall | history-analyzer |

**Example: Plan with InfraNodus gap detection**

```python
def plan_with_gaps(task_description: str, Κ: KnowledgeBase) -> Plan:
    # Parallel research
    context = context_analyzer.run(task_description)
    domain = domain_researcher.run(context.domain)
    history = history_analyzer.search(Κ, context.signature)
    
    # InfraNodus gap analysis
    combined_context = f"{context.summary}\n{domain.best_practices}"
    gaps = infranodus.generateContentGaps(combined_context)
    questions = infranodus.generateResearchQuestions(
        combined_context, 
        useSeveralGaps=True
    )
    
    # Hierarchical synthesis
    return hierarchical_reasoning.synthesize(
        strategic=define_goals(context, gaps),
        tactical=design_approach(domain, history),
        operational=specify_steps(questions)
    )
```

### EXECUTE Phase

```haskell
-- Execute phase composition
execute :: Plan → (Outputs, ExecutionLog)
execute = track ∘ run_steps ∘ validate_prereqs

-- With skill integrations
execute_with_skills =
    reason.emit ∘              -- Produce outputs
    reason.ground ∘            -- Ground in reality
    agency.act                 -- Take actions
```

**Skill compositions:**

| Skill | Function | Integration Point |
|-------|----------|-------------------|
| `reason` | Ground execution | task-executor |
| `agency` | OODA loop | progress-tracker |

### ASSESS Phase

```haskell
-- Assess phase composition
assess :: (Outputs, Plan) → AssessmentReport
assess = synthesize ∘ (
    quality_review ⊗
    pattern_detect ⊗
    gap_identify ⊗
    risk_analyze
)

-- With skill integrations
assess_with_skills =
    critique.synthesize ∘      -- Combine perspectives
    (
        critique.STRUCTURAL ⊗   -- Structure quality
        critique.EVIDENTIAL ⊗   -- Evidence strength
        critique.PRAGMATIC ⊗    -- Practical value
        critique.ADVERSARIAL    -- Attack testing
    )
```

**Skill compositions:**

| Skill | Function | Integration Point |
|-------|----------|-------------------|
| `critique` | Multi-lens evaluation | quality-reviewer |
| `abduct` | Pattern detection | pattern-detector |
| `graph` | Topology analysis | coverage validation |

**Example: Assess with multi-lens critique**

```python
def assess_with_critique(outputs, plan) -> AssessmentReport:
    # Parallel critique lenses
    structural = critique.evaluate(
        outputs, 
        lens="STRUCTURAL",
        question="Does structure serve purpose?"
    )
    evidential = critique.evaluate(
        outputs,
        lens="EVIDENTIAL", 
        question="Is quality justified by evidence?"
    )
    pragmatic = critique.evaluate(
        outputs,
        lens="PRAGMATIC",
        question="Will this improve real outcomes?"
    )
    adversarial = critique.evaluate(
        outputs,
        lens="ADVERSARIAL",
        question="How could this fail?"
    )
    
    # Synthesis
    return critique.synthesize([
        structural, evidential, pragmatic, adversarial
    ])
```

### COMPOUND Phase

```haskell
-- Compound phase composition
compound :: (Solution, Assessment) → (Documentation, Knowledge')
compound = write ∘ classify ∘ (
    extract_solution ⊗
    design_prevention ⊗
    find_related
)

-- With skill integrations
compound_with_skills =
    obsidian_markdown.format ∘      -- Proper formatting
    graph.validate_topology(η≥4) ∘  -- Ensure connectivity
    (
        abduct.extract_schema ⊗      -- Extract patterns
        memory.integrate ⊗           -- Update memory
        skill_updater.observe         -- Feed meta-improvement
    )
```

**Skill compositions:**

| Skill | Function | Integration Point |
|-------|----------|-------------------|
| `graph` | Topology validation | category-classifier |
| `abduct` | Schema extraction | solution-extractor |
| `memory` | Κ integration | documentation-writer |
| `obsidian-markdown` | Formatting | documentation-writer |
| `skill-updater` | Meta-improvement | post-compound |

**Example: Compound with topology validation**

```python
def compound_with_topology(solution, assessment, Κ) -> tuple:
    # Extract and classify
    extracted = solution_extractor.run(solution)
    prevention = prevention_strategist.run(solution, assessment)
    category = category_classifier.run(extracted, Κ.categories)
    
    # Graph topology check before integration
    G_before = graph.build(Κ.documents)
    η_before = graph.calculate_η(G_before)
    
    # Create documentation
    doc = documentation_writer.assemble(
        extracted, prevention, category
    )
    
    # Validate topology after integration
    Κ_new = Κ.add(doc)
    G_after = graph.build(Κ_new.documents)
    η_after = graph.calculate_η(G_after)
    
    # Ensure topology not degraded
    assert η_after >= η_before, "Topology degraded"
    assert η_after >= 4.0, f"η={η_after} below threshold"
    
    # Trigger skill-updater observation
    skill_updater.observe(
        skills_used=["compound-learning"],
        outcome="success",
        metrics={"η_before": η_before, "η_after": η_after}
    )
    
    return doc, Κ_new
```

## Cross-Skill Workflows

### Full Compound Cycle with All Skills

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PLAN                                                                         │
│   reason.decompose(query)                                                    │
│   ↓                                                                          │
│   think.apply_model("First Principles") ⊗ infranodus.gaps() ⊗ memory.recall()│
│   ↓                                                                          │
│   hierarchical_reasoning.synthesize(S, T, O)                                 │
│   ↓                                                                          │
│   → Plan                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ EXECUTE                                                                      │
│   agency.observe(plan)                                                       │
│   ↓                                                                          │
│   reason.ground(steps) → execute(step) → agency.reflect(result)             │
│   ↓                                                                          │
│   → Outputs, ExecutionLog                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ ASSESS                                                                       │
│   critique.parallel([STRUCTURAL, EVIDENTIAL, PRAGMATIC, ADVERSARIAL])       │
│   ↓                                                                          │
│   abduct.detect_patterns(outputs)                                            │
│   ↓                                                                          │
│   critique.synthesize() → graph.validate_coverage()                          │
│   ↓                                                                          │
│   → AssessmentReport                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ COMPOUND                                                                     │
│   abduct.extract_schema(solution)                                            │
│   ↓                                                                          │
│   graph.validate_topology(Κ ∪ new_doc)                                       │
│   ↓                                                                          │
│   obsidian_markdown.format(doc) → memory.integrate(Κ)                        │
│   ↓                                                                          │
│   skill_updater.observe(outcome)                                             │
│   ↓                                                                          │
│   → Documentation, Κ'                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Research-Heavy Cycle

```haskell
research_cycle = 
    compound ∘ 
    assess ∘ 
    execute ∘ 
    (
        infranodus.research_questions ∘
        web_search.gather ∘
        think.mental_models("Scientific Method") ∘
        plan
    )
```

### Learning-Focused Cycle

```haskell
learning_cycle =
    compound ∘
    assess ∘
    (
        reason.self_explain ∘
        think.notebook("feynman-sequential") ∘
        execute
    ) ∘
    (
        memory.retrieve_schema ∘
        infranodus.gaps ∘
        plan
    )
```

### Meta-Improvement Cycle

```haskell
-- Compound learning improving itself
meta_cycle =
    skill_updater.update_if_warranted ∘
    skill_optimiser.validate ∘
    compound_learning.full_cycle(domain="Skills")
```

## Tool Integration

### MCP Tool Routing

```yaml
plan_phase:
  - web_search: External research
  - conversation_search: Past learnings
  - google_drive_search: Internal docs
  - infranodus.gaps: Knowledge gaps
  - infranodus.questions: Research questions

execute_phase:
  - bash_tool: Command execution
  - create_file: Output generation
  - str_replace: Iteration

assess_phase:
  - infranodus.compare: Overlap analysis
  - graph.analyze: Topology metrics

compound_phase:
  - create_file: Documentation
  - memory.add: Κ updates
  - infranodus.graph: Cross-reference
```

### Parallel Tool Execution

```python
def plan_with_parallel_tools(context):
    """Execute research tools in parallel."""
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(web_search, f"best practices {context.domain}"): "external",
            executor.submit(conversation_search, context.signature): "history",
            executor.submit(google_drive_search, context.query): "internal",
            executor.submit(infranodus.gaps, context.text): "gaps"
        }
        
        results = {}
        for future in as_completed(futures):
            key = futures[future]
            results[key] = future.result()
    
    return results
```

## Invariant Preservation

### Across All Integrations

```python
class IntegrationInvariants:
    """Invariants that must hold across skill compositions."""
    
    @staticmethod
    def knowledge_monotonic(Κ_before, Κ_after):
        """Knowledge never decreases."""
        return len(Κ_after) >= len(Κ_before)
    
    @staticmethod
    def topology_preserved(G_before, G_after):
        """Graph density never degrades."""
        η_before = edges(G_before) / nodes(G_before)
        η_after = edges(G_after) / nodes(G_after)
        return η_after >= η_before and η_after >= 4.0
    
    @staticmethod
    def skill_compatibility(skills_used):
        """All skills can compose."""
        for s1, s2 in combinations(skills_used, 2):
            if not compatible(s1, s2):
                return False
        return True
    
    @staticmethod
    def convergence_achieved(states):
        """Iteration converged."""
        if len(states) < 2:
            return False
        return similarity(states[-1], states[-2]) > 0.95
```

## Quick Reference

| Integration | Composition | When |
|-------------|-------------|------|
| reason + plan | `reason.decompose ∘ plan` | Problem structuring |
| think + plan | `think.models ⊗ plan` | Apply mental models |
| infranodus + plan | `infranodus.gaps ⊗ plan` | Gap detection |
| critique + assess | `critique.parallel ∘ assess` | Multi-lens review |
| abduct + compound | `abduct.extract ∘ compound` | Pattern extraction |
| graph + compound | `graph.validate ∘ compound` | Topology check |
| memory + all | `memory.recall ⊗ memory.store` | Knowledge threading |
| skill-updater + post | `skill_updater.observe` | Meta-improvement |

---

```
λSkills.τ = emit ∘ (skill₁ ⊗ skill₂ ⊗ ... ⊗ skillₙ) ∘ route
η≥4 preserved across compositions
Knowledge threads through all phases
```
