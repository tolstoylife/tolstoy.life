# Lens Specifications Reference

Complete templates for the five evaluative lenses.

## Lens Overview

| Lens | Code | Domain | Core Question |
|------|------|--------|---------------|
| STRUCTURAL | S | Logic & Architecture | Is the reasoning valid? |
| EVIDENTIAL | E | Evidence & Epistemology | What justifies belief? |
| SCOPE | O | Boundaries & Generality | Where does this apply? |
| ADVERSARIAL | A | Opposition & Alternatives | What's the best counter? |
| PRAGMATIC | P | Application & Consequence | Does this work? |

## STRUCTURAL Lens (S)

**Objective**: Evaluate logical architecture, coherence, and inferential validity.

**Attack Vectors**:
```yaml
structural_attacks:
  - type: non_sequitur
    pattern: "Conclusion does not follow from premises"
    detection: Gap between stated premises and claimed conclusion
    
  - type: circular_reasoning
    pattern: "Conclusion presupposed in premises"
    detection: Claim A depends on B depends on A
    
  - type: false_dichotomy
    pattern: "Excluded middle options"
    detection: "Either X or Y" when Z exists
    
  - type: equivocation
    pattern: "Term used with multiple meanings"
    detection: Key term shifts definition mid-argument
    
  - type: composition_division
    pattern: "Part-whole fallacy"
    detection: Properties of parts ≠ properties of whole
    
  - type: affirming_consequent
    pattern: "If P then Q; Q; therefore P"
    detection: Reversed conditional logic
    
  - type: denying_antecedent
    pattern: "If P then Q; not P; therefore not Q"
    detection: Invalid negation of conditional
```

**Output Schema**:
```yaml
structural_evaluation:
  logical_gaps:
    - location: C{id} → C{id}
      type: "{attack_type}"
      severity: fatal|major|minor
      explanation: "{Why this is a gap}"
      
  dependency_issues:
    - claim: C{id}
      problem: "{Missing support | Circular | Unstated premise}"
      fix_suggestion: "{How to repair}"
      
  coherence_analysis:
    consistent: true|false
    contradictions: ["{C{id} conflicts with C{id}}"]
    redundancies: ["{C{id} duplicates C{id}}"]
    
  coherence_score: 0.0-1.0
```

**Cross-Evaluation Contribution**:
- Can identify logical flaws in other lenses' reasoning
- Validates whether attacks from other lenses are well-formed
- Detects when ADVERSARIAL lens attacks strawmen vs. actual claims

## EVIDENTIAL Lens (E)

**Objective**: Assess evidence quality, epistemic justification, and falsifiability.

**Attack Vectors**:
```yaml
evidential_attacks:
  - type: insufficient_evidence
    pattern: "Claim exceeds evidential support"
    detection: High confidence with weak/absent citation
    
  - type: cherry_picking
    pattern: "Selective evidence presentation"
    detection: Counter-evidence exists but unaddressed
    
  - type: unfalsifiable
    pattern: "No possible disconfirming evidence"
    detection: Claim structured to be immune to refutation
    
  - type: correlation_causation
    pattern: "Causal claim from correlational data"
    detection: "X correlates with Y" → "X causes Y"
    
  - type: anecdotal_generalization
    pattern: "N=1 to universal"
    detection: Single case extrapolated broadly
    
  - type: appeal_to_authority
    pattern: "Expert said X, therefore X"
    detection: Authority cited outside domain expertise
    
  - type: outdated_evidence
    pattern: "Evidence no longer current"
    detection: Field has advanced past cited work
```

**Output Schema**:
```yaml
evidential_evaluation:
  unsupported_claims:
    - claim: C{id}
      confidence_claimed: 0.0-1.0
      evidence_supports: 0.0-1.0
      gap: "{What's missing}"
      
  falsification_tests:
    - claim: C{id}
      test: "{Observable that would disprove}"
      feasibility: easy|moderate|hard|impossible
      
  evidence_quality:
    - claim: C{id}
      sources: ["{Listed sources}"]
      quality: peer_reviewed|preprint|anecdotal|none
      recency: current|dated|obsolete
      
  evidence_score: 0.0-1.0
```

**Cross-Evaluation Contribution**:
- Validates evidence cited by other lenses
- Checks if ADVERSARIAL counter-evidence is legitimate
- Assesses whether PRAGMATIC consequences have empirical support

## SCOPE Lens (O)

**Objective**: Test boundaries, edge cases, and domain of applicability.

**Attack Vectors**:
```yaml
scope_attacks:
  - type: overgeneralization
    pattern: "Specific case → universal claim"
    detection: "All X" when only "Some X" demonstrated
    
  - type: false_universal
    pattern: "No exceptions acknowledged"
    detection: Edge case defeats universal
    
  - type: excluded_middle
    pattern: "Binary when spectrum exists"
    detection: Ignores intermediate cases
    
  - type: boundary_violation
    pattern: "Applied outside valid domain"
    detection: Claim X valid in context A, applied in context B
    
  - type: context_dependence
    pattern: "Unstated contextual requirements"
    detection: Claim requires conditions not specified
    
  - type: base_rate_neglect
    pattern: "Ignores prior probability"
    detection: Conditional without base rate
    
  - type: survivorship_bias
    pattern: "Only successful cases visible"
    detection: Failed cases systematically excluded
```

**Output Schema**:
```yaml
scope_evaluation:
  edge_cases:
    - case: "{Specific scenario}"
      claim_affected: C{id}
      failure_mode: "{How claim fails here}"
      severity: fatal|major|minor
      
  scope_violations:
    - claim: C{id}
      stated_scope: "{What claim says}"
      actual_scope: "{What evidence supports}"
      overreach: "{The gap}"
      
  boundary_conditions:
    - claim: C{id}
      valid_when: ["{Conditions for validity}"]
      invalid_when: ["{Conditions for invalidity}"]
      unstated_assumptions: ["{Hidden requirements}"]
      
  generality_score: 0.0-1.0
```

**Cross-Evaluation Contribution**:
- Tests whether other lenses' attacks apply generally or only in edge cases
- Validates ADVERSARIAL counter-position isn't itself overgeneralized
- Checks PRAGMATIC concerns for context-specificity

## ADVERSARIAL Lens (A)

**Objective**: Construct strongest possible counter-position and alternative explanations.

**Attack Vectors**:
```yaml
adversarial_attacks:
  - type: steel_man_opposition
    pattern: "Best version of opposing view"
    construction: Build strongest counter-argument
    
  - type: alternative_explanation
    pattern: "Different cause for same effect"
    construction: Competing hypothesis equally plausible
    
  - type: reductio_ad_absurdum
    pattern: "Follow to absurd conclusion"
    construction: If thesis true, then absurdity follows
    
  - type: precedent_contradiction
    pattern: "Conflicts with established case"
    construction: Accepted instance defeats thesis
    
  - type: expert_dissent
    pattern: "Qualified opposition exists"
    construction: Domain experts disagree
    
  - type: historical_failure
    pattern: "Similar thesis failed before"
    construction: Past attempt with same logic failed
```

**Output Schema**:
```yaml
adversarial_evaluation:
  counter_thesis:
    statement: "{Complete opposing position}"
    strength: weak|moderate|strong|compelling
    
  counter_evidence:
    - point: "{Specific counter-point}"
      source: "{Citation or construction}"
      targets: [C{ids}]
      
  alternative_explanations:
    - for_claim: C{id}
      alternative: "{Different explanation}"
      plausibility: 0.0-1.0
      
  steel_man:
    position: "{Strongest form of opposition}"
    key_arguments: ["{Main points}"]
    concessions_required: ["{What thesis must grant}"]
    
  counter_strength: 0.0-1.0
```

**Cross-Evaluation Contribution**:
- Tests whether other lenses attacked actual claims vs. strawmen
- Provides counter-arguments to other lenses' conclusions
- Validates that rejected attacks were genuinely weak

## PRAGMATIC Lens (P)

**Objective**: Evaluate real-world applicability, implementation, and consequences.

**Attack Vectors**:
```yaml
pragmatic_attacks:
  - type: implementation_barrier
    pattern: "Cannot be executed as stated"
    detection: Resource, technical, or social obstacle
    
  - type: unintended_consequence
    pattern: "Second-order effects harmful"
    detection: If X, then Y follows, and Y is bad
    
  - type: resource_constraint
    pattern: "Requires unavailable resources"
    detection: Time, money, expertise, or attention gap
    
  - type: scaling_failure
    pattern: "Works small, fails large"
    detection: N=10 success ≠ N=10000 success
    
  - type: incentive_misalignment
    pattern: "Actors won't behave as required"
    detection: Assumes behavior contrary to incentives
    
  - type: goodhart_vulnerability
    pattern: "Measure becomes target, ceases to measure"
    detection: Metric optimization defeats purpose
    
  - type: reversibility_problem
    pattern: "Cannot undo if wrong"
    detection: Irreversible commitment with uncertainty
```

**Output Schema**:
```yaml
pragmatic_evaluation:
  implementation_issues:
    - barrier: "{Specific obstacle}"
      severity: blocking|significant|minor
      workaround: "{Possible mitigation}"
      
  consequences:
    - condition: "If {thesis applied}"
      effect: "{What happens}"
      valence: positive|negative|mixed
      likelihood: 0.0-1.0
      
  resource_requirements:
    - resource: "{What's needed}"
      availability: available|scarce|unavailable
      criticality: required|helpful|optional
      
  scaling_analysis:
    works_at: "{Scale where valid}"
    fails_at: "{Scale where breaks}"
    transition: "{What changes}"
    
  feasibility_score: 0.0-1.0
```

**Cross-Evaluation Contribution**:
- Reality-checks theoretical attacks from other lenses
- Validates whether STRUCTURAL repairs are implementable
- Tests if ADVERSARIAL counter-position is itself practical

## Lens Interaction Patterns

**Complementary Pairs**:
- S + E: Logic requires evidence; evidence requires logical interpretation
- O + A: Scope limits meet counter-examples
- P + S: Practical constraints reveal structural assumptions

**Tension Pairs**:
- A vs E: Adversarial may construct hypotheticals; Evidential demands real evidence
- O vs P: Scope may be theoretically valid but practically irrelevant
- S vs P: Logically valid may be practically impossible

**Calibration Signals**:
- If S and E both attack same claim → high confidence in attack
- If A attacks but P endorses → theoretical vs practical tension
- If O finds edge case that P confirms → actionable scope limitation
