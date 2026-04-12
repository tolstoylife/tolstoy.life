# Abductive Learning Reference

Inference to the best explanation for systematic debugging and knowledge building.

## Core Principle

**Abduction**: Given observation O, find hypothesis H that best explains O.

```haskell
abduct :: Observation -> [Hypothesis] -> Hypothesis
abduct o hs = argmax (\h -> likelihood(o | h) * prior(h)) hs

-- Select hypothesis that maximizes explanatory power
-- Weighted by prior plausibility (parsimony)
```

## The OHPT Protocol

| Phase | Question | Output | Tool |
|-------|----------|--------|------|
| **O**bservation | What was observed? | Symptom | Logs, errors, behavior |
| **H**ypothesis | What explains O? | Candidate causes | Domain knowledge |
| **P**rediction | If H true, what else? | Testable claims | Deduction |
| **T**est | Does P hold? | Evidence | Experiments, code review |

## Abductive Debugging

### Phase 1: Observation (O)

Gather all relevant observations:

```python
def gather_observations(symptom: str) -> Observation:
    return Observation(
        symptom=symptom,
        error_messages=collect_errors(),
        logs=collect_relevant_logs(),
        state=capture_system_state(),
        context=gather_execution_context(),
        reproducibility=assess_reproducibility()
    )
```

**Quality checklist:**
- [ ] Error message captured exactly
- [ ] Stack trace included
- [ ] Reproducibility assessed (always/sometimes/once)
- [ ] Environment documented
- [ ] Recent changes noted

### Phase 2: Hypothesis Generation (H)

Generate candidate explanations ranked by parsimony:

```python
def generate_hypotheses(obs: Observation) -> List[Hypothesis]:
    candidates = []

    # Common cause patterns
    candidates.extend(check_common_causes(obs))

    # Domain-specific patterns
    candidates.extend(check_domain_patterns(obs))

    # Analogical reasoning from K
    candidates.extend(find_similar_past_issues(obs, K))

    # Rank by parsimony (simpler = more likely)
    return sorted(candidates, key=lambda h: h.complexity)
```

**Hypothesis quality:**
| Criterion | Good | Bad |
|-----------|------|-----|
| Specificity | "Race condition in auth mutex" | "Something wrong with auth" |
| Testability | Implies observable predictions | Unfalsifiable |
| Parsimony | Minimal assumptions | Requires many coincidences |
| Mechanism | Explains HOW | Only describes WHAT |

### Phase 3: Prediction (P)

Derive testable predictions from each hypothesis:

```python
def derive_predictions(hypothesis: Hypothesis) -> List[Prediction]:
    """
    If H is true, what else MUST be true?
    These become our test cases.
    """
    predictions = []

    # Necessary conditions
    predictions.extend(hypothesis.necessary_conditions())

    # Observable consequences
    predictions.extend(hypothesis.observable_effects())

    # Distinguishing tests (separates this H from alternatives)
    predictions.extend(hypothesis.distinguishing_features())

    return predictions
```

**Example:**
```
H: "Auth fails due to race condition in token refresh"

Predictions:
P1: Failure rate increases under concurrent load
P2: Adding mutex around refresh eliminates failures
P3: Failure logs show interleaved token operations
P4: Single-threaded execution never fails
```

### Phase 4: Test (T)

Systematically test predictions:

```python
def test_hypothesis(hypothesis: Hypothesis, predictions: List[Prediction]) -> Result:
    results = []

    for prediction in predictions:
        # Design test
        test = design_test(prediction)

        # Execute test
        outcome = execute_test(test)

        # Record evidence
        results.append(Evidence(
            prediction=prediction,
            outcome=outcome,
            supports_hypothesis=outcome.matches(prediction)
        ))

    # Evaluate overall support
    support_ratio = sum(1 for r in results if r.supports_hypothesis) / len(results)

    return Result(
        hypothesis=hypothesis,
        confirmed=support_ratio > 0.8,
        evidence=results,
        confidence=calculate_confidence(results)
    )
```

## Integration with Compound Learning

### From Resolution to Knowledge

When OHPT succeeds, crystallize the learning:

```yaml
date: 2026-01-14
trigger: "Bug report: intermittent auth failures"

# OHPT chain
observation: "Auth fails ~5% of requests under load"
hypothesis: "Race condition in token refresh"
prediction: "Mutex should eliminate failures"
test: "Load test with mutex: 0% failures"

# Resolution
root_cause: "Non-atomic read-modify-write in token refresh"
solution: "Added mutex around token refresh operation"
why_works: "Mutex ensures atomicity, prevents race"
prevention: "Use atomic operations for shared state"

# Integration
vertices:
  - "[[concurrency]]"
  - "[[race-conditions]]"
  - "[[authentication]]"
related:
  - "[[mutex-patterns]]"
  - "[[token-refresh]]"

confidence: 0.90
evidence_strength: "strong"
```

### Compound Growth

```
      ┌──────────────────────────────────────────┐
      │                                          │
      ▼                                          │
   Symptom ──► OHPT ──► Resolution ──► Crystallize
                                          │
                                          ▼
                                    K ∪ new_learning
                                          │
                                          ▼
                                   K' (enriched)
                                          │
      ┌───────────────────────────────────┘
      │
      ▼
   Future OHPT uses K' for hypothesis generation
```

## Abductive Patterns

### Pattern: Differential Diagnosis

When multiple hypotheses seem plausible:

```python
def differential_diagnosis(obs: Observation, hypotheses: List[Hypothesis]) -> Hypothesis:
    """
    Find tests that distinguish between hypotheses.
    """
    while len(hypotheses) > 1:
        # Find most discriminating test
        test = find_discriminating_test(hypotheses)

        # Execute test
        result = execute_test(test)

        # Eliminate hypotheses inconsistent with result
        hypotheses = [h for h in hypotheses if consistent(h, result)]

    return hypotheses[0] if hypotheses else None
```

### Pattern: Analogical Transfer

Use past solutions for similar problems:

```python
def analogical_hypothesis(obs: Observation, K: Knowledge) -> List[Hypothesis]:
    """
    Find similar past issues and transfer solutions.
    """
    # Find similar observations in K
    similar = find_similar_observations(obs, K)

    # Extract hypotheses that worked
    candidates = []
    for past in similar:
        if past.resolution.successful:
            # Adapt hypothesis to current context
            adapted = adapt_hypothesis(past.hypothesis, obs)
            adapted.prior_boost = past.resolution.confidence
            candidates.append(adapted)

    return candidates
```

### Pattern: Bisection

For regression debugging:

```python
def bisection_debug(obs: Observation, history: List[Commit]) -> Commit:
    """
    Binary search through history to find introducing commit.
    """
    # H: Bug introduced in some commit
    # P: All commits before introduction work; all after fail

    left, right = 0, len(history) - 1

    while left < right:
        mid = (left + right) // 2
        if test_commit(history[mid]).works:
            left = mid + 1
        else:
            right = mid

    return history[left]  # First failing commit
```

## Anti-Patterns

| Anti-Pattern | Problem | Correction |
|--------------|---------|------------|
| Jumping to fix | Skips hypothesis validation | Complete OHPT before fixing |
| Confirmation bias | Only tests supporting evidence | Test predictions that would REFUTE H |
| Anchoring | First hypothesis dominates | Generate multiple candidates |
| Availability bias | Recent causes over-weighted | Consider full hypothesis space |
| Tautological testing | Test only verifies implementation | Test verifies REQUIREMENTS |

## Hookify Enforcement

| Hook | Trigger | Enforcement |
|------|---------|-------------|
| `abductive-hypothesis` | Test with fix/solve keywords | Require OHPT documentation |
| `inference-chain` | TODO ending with ? | Complete the reasoning chain |
| `pattern-crystallization` | Commit with fix message | Prompt learning extraction |

## Quick Reference

### OHPT Template

```python
"""
O: [What was observed - be specific]
H: [Best explanation - testable, parsimonious]
P: [If H true, then... - observable consequences]
T: [Test result - confirms/refutes H]
"""
```

### Debugging Checklist

- [ ] O: Observation fully captured
- [ ] H: Multiple hypotheses considered
- [ ] H: Ranked by parsimony
- [ ] P: Predictions are testable
- [ ] P: Predictions would distinguish H from alternatives
- [ ] T: Tests executed systematically
- [ ] T: Results recorded
- [ ] Resolution crystallized to K
