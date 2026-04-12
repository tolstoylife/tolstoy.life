# Domain Schemas for Compound Learning

> Configure compound-learning for specific domains by instantiating these schemas.

## Schema Structure

Each domain requires:
1. **Problem types**: Classification of issues/challenges
2. **Root causes**: Why problems occur
3. **Resolution types**: Categories of solutions
4. **Components**: What can be worked on
5. **Symptom vocabulary**: Observable indicators

## Core Domains

### Coding

```yaml
domain: Coding
problem_types:
  - build_error: "Compilation/bundling fails"
  - test_failure: "Tests don't pass"
  - runtime_error: "Crashes during execution"
  - performance_issue: "Unacceptable speed/resource use"
  - database_issue: "Data access/integrity problems"
  - security_issue: "Vulnerability detected"
  - ui_bug: "Visual/interaction defect"
  - integration_issue: "Components don't work together"
  - logic_error: "Wrong behavior, no crash"
  - developer_experience: "Friction in development process"

root_causes:
  - missing_dependency: "Required package not installed"
  - wrong_api: "API misused or changed"
  - config_error: "Configuration incorrect"
  - logic_error: "Algorithm/flow wrong"
  - race_condition: "Timing-dependent bug"
  - memory_leak: "Resources not freed"
  - missing_validation: "Input not checked"
  - scope_issue: "Variable/context scope wrong"
  - async_timing: "Promise/callback sequencing"
  - thread_violation: "Concurrency bug"

resolution_types:
  - code_fix: "Change application code"
  - migration: "Database schema change"
  - config_change: "Update configuration"
  - dependency_update: "Update/add package"
  - refactor: "Restructure without behavior change"
  - documentation_update: "Clarify usage"
  - environment_setup: "Fix dev/prod environment"
  - tooling_addition: "Add development tool"

components:
  - controller|model|view|service|job|database|frontend|backend
  - api|auth|payments|email|queue|cache|search|storage

symptom_patterns:
  - "Error: {message}"
  - "{metric} degraded by {percent}%"
  - "Test {name} fails with {assertion}"
  - "{feature} not working when {condition}"
```

### Learning

```yaml
domain: Learning
problem_types:
  - comprehension_gap: "Don't understand concept"
  - retention_failure: "Can't recall learned material"
  - application_difficulty: "Can't apply to new problems"
  - integration_challenge: "Can't connect to existing knowledge"
  - misconception: "Hold incorrect mental model"
  - knowledge_decay: "Previously known, now forgotten"
  - transfer_failure: "Can't apply across contexts"
  - metacognitive_blind_spot: "Don't know what I don't know"

root_causes:
  - missing_prerequisite: "Foundational knowledge absent"
  - weak_encoding: "Initial learning too shallow"
  - no_practice: "Insufficient retrieval practice"
  - isolated_concept: "Not connected to schema"
  - interference: "Similar concepts confused"
  - overload: "Too much at once"
  - passive_consumption: "No active engagement"
  - no_feedback: "Can't verify understanding"

resolution_types:
  - spaced_repetition: "Distributed practice over time"
  - elaboration: "Generate explanations, examples"
  - interleaving: "Mix problem types"
  - schema_integration: "Connect to existing knowledge"
  - worked_example: "Study solved problems"
  - self_explanation: "Explain steps to self"
  - retrieval_practice: "Test without looking"
  - dual_coding: "Combine verbal and visual"
  - feynman_technique: "Teach to learn"

components:
  - concept|principle|procedure|fact|schema|model|framework
  - physiology|pharmacology|anatomy|pathology|clinical

symptom_patterns:
  - "Can't explain {concept} simply"
  - "Confuse {concept_a} with {concept_b}"
  - "Know definition but can't apply"
  - "Forget within {timeframe}"
  - "Can't connect {concept} to {related}"
```

### Writing

```yaml
domain: Writing
problem_types:
  - clarity_issue: "Meaning unclear to reader"
  - structure_problem: "Organization doesn't serve purpose"
  - voice_inconsistency: "Tone/style varies inappropriately"
  - argument_weakness: "Reasoning unconvincing"
  - engagement_failure: "Reader loses interest"
  - technical_error: "Grammar/mechanics wrong"
  - audience_mismatch: "Wrong level/style for reader"
  - redundancy: "Unnecessary repetition"

root_causes:
  - unclear_thesis: "Core message not defined"
  - missing_outline: "No structural plan"
  - weak_evidence: "Claims unsupported"
  - passive_construction: "Indirect expression"
  - jargon_overload: "Inaccessible language"
  - burying_lede: "Key point not prominent"
  - scope_drift: "Strayed from purpose"
  - insufficient_revision: "Didn't iterate"

resolution_types:
  - restructure: "Reorganize sections/flow"
  - reframe: "Change angle/thesis"
  - add_evidence: "Support claims"
  - simplify: "Reduce complexity"
  - add_examples: "Concrete illustrations"
  - cut_redundancy: "Remove repetition"
  - strengthen_transitions: "Improve flow"
  - revise_voice: "Adjust tone/style"

components:
  - thesis|introduction|body|conclusion|paragraph|sentence
  - argument|evidence|example|transition|hook|call_to_action

symptom_patterns:
  - "Reader confused at {point}"
  - "{section} feels disconnected"
  - "Argument for {claim} unconvincing"
  - "Loses energy at {point}"
  - "Too {adjective} for audience"
```

### Research

```yaml
domain: Research
problem_types:
  - hypothesis_failure: "Prediction not supported"
  - method_flaw: "Design doesn't test hypothesis"
  - data_issue: "Data quality/quantity insufficient"
  - interpretation_error: "Conclusions don't follow"
  - replication_problem: "Can't reproduce results"
  - scope_creep: "Project expanded beyond plan"
  - literature_gap: "Missed relevant work"
  - ethics_concern: "Protocol questionable"

root_causes:
  - confounding_variable: "Uncontrolled factor"
  - sampling_bias: "Non-representative sample"
  - measurement_error: "Instrument unreliable"
  - p_hacking: "Multiple comparisons without correction"
  - cherry_picking: "Selective reporting"
  - underpowered: "Sample too small"
  - hindsight_bias: "Post-hoc hypothesis"
  - confirmation_bias: "Saw what expected"

resolution_types:
  - redesign_study: "Fix experimental design"
  - add_controls: "Control confounds"
  - increase_sample: "More participants/observations"
  - preregister: "Commit to analysis before data"
  - replicate: "Repeat to verify"
  - constrain_scope: "Narrow research question"
  - systematic_review: "Comprehensive literature search"
  - peer_feedback: "External validation"

components:
  - hypothesis|method|sample|measurement|analysis|interpretation
  - literature_review|experiment|survey|observation|interview

symptom_patterns:
  - "Effect size {size} but p = {p}"
  - "Results differ from {prior_study}"
  - "{variable} not controlled"
  - "N = {n} insufficient for {effect}"
  - "Conclusion exceeds evidence"
```

### Problem-Solving

```yaml
domain: ProblemSolving
problem_types:
  - stuck: "No progress despite effort"
  - wrong_approach: "Method doesn't fit problem"
  - missed_constraint: "Violated requirement"
  - suboptimal_solution: "Works but not well"
  - overcomplicated: "Unnecessary complexity"
  - fragile_solution: "Breaks easily"
  - unclear_problem: "Requirements ambiguous"
  - resource_exceeded: "Time/cost overrun"

root_causes:
  - fixation: "Stuck on one approach"
  - premature_commitment: "Decided too early"
  - incomplete_analysis: "Didn't understand problem"
  - missing_abstraction: "Didn't see pattern"
  - optimization_obsession: "Premature optimization"
  - complexity_creep: "Added unnecessary features"
  - constraint_amnesia: "Forgot requirements"
  - tool_mismatch: "Wrong tool for job"

resolution_types:
  - reframe_problem: "Different perspective"
  - decompose: "Break into subproblems"
  - analogize: "Apply pattern from elsewhere"
  - simplify: "Reduce to essence"
  - prototype: "Quick test of approach"
  - constraint_relax: "Question requirements"
  - step_back: "Review from higher level"
  - external_input: "Get fresh perspective"

components:
  - definition|constraints|approach|implementation|verification
  - goal|subgoal|operator|state|heuristic

symptom_patterns:
  - "Tried {n} approaches, none work"
  - "Solution violates {constraint}"
  - "Works for {case_a} not {case_b}"
  - "Took {actual} vs {expected} time"
  - "Requires {resource} we don't have"
```

## Extending to New Domains

To add a new domain:

```python
def create_domain_schema(domain_name: str) -> DomainSchema:
    """
    Generate schema through structured analysis.
    """
    return DomainSchema(
        name=domain_name,
        
        # What can go wrong?
        problem_types=extract_problem_categories(domain_name),
        
        # Why do things go wrong?
        root_causes=extract_causal_patterns(domain_name),
        
        # How do we fix things?
        resolution_types=extract_solution_categories(domain_name),
        
        # What do we work on?
        components=extract_domain_objects(domain_name),
        
        # How do we know something's wrong?
        symptom_patterns=extract_observable_indicators(domain_name)
    )
```

### Schema Validation

```python
def validate_domain_schema(schema: DomainSchema) -> ValidationResult:
    checks = [
        len(schema.problem_types) >= 5,
        len(schema.root_causes) >= 5,
        len(schema.resolution_types) >= 5,
        all_causes_map_to_resolutions(schema),
        symptom_patterns_are_observable(schema),
    ]
    return ValidationResult(passed=all(checks))
```

## Cross-Domain Mappings

Some patterns transfer across domains:

| Generic | Coding | Learning | Writing | Research |
|---------|--------|----------|---------|----------|
| Unclear requirements | missing spec | missing prerequisite | unclear thesis | vague hypothesis |
| Wrong approach | wrong algorithm | passive consumption | wrong structure | flawed method |
| Insufficient iteration | no refactoring | no practice | no revision | no replication |
| Complexity excess | over-engineering | cognitive overload | verbose prose | scope creep |
| Missing feedback | no tests | no retrieval practice | no reader review | no peer review |

These mappings enable **transfer learning** in compound knowledge:
- Pattern in one domain may apply to another
- Cross-domain analogies can spark solutions
