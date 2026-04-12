# Cross-Evaluation Protocol Reference

Matrix construction, analysis patterns, and inter-lens evaluation procedures.

## Matrix Structure

For N lenses, the evaluation matrix has N² cells:
- N diagonal cells: Each lens's evaluation of thesis (Φ2a)
- N²-N off-diagonal cells: Each lens evaluating each other lens's critique (Φ2b)

**5-Lens Matrix (25 cells)**:

```
           ┌─────────────────────────────────────────────────────┐
           │              EVALUATED LENS                         │
           │    S        E        O        A        P            │
    ┌──────┼─────────────────────────────────────────────────────┤
    │  S   │  S→T     S→E      S→O      S→A      S→P            │
E   │  E   │  E→S     E→T      E→O      E→A      E→P            │
V   │  O   │  O→S     O→E      O→T      O→A      O→P            │
A   │  A   │  A→S     A→E      A→O      A→T      A→P            │
L   │  P   │  P→S     P→E      P→O      P→A      P→T            │
    └──────┴─────────────────────────────────────────────────────┘
    
    T = Thesis (diagonal)
    X→Y = Lens X evaluates Lens Y's critique
```

## Phase 2a: Initial Evaluation Protocol

Each lens independently evaluates thesis. **No cross-lens communication yet.**

```python
def execute_initial_evaluations(thesis: Thesis, lenses: list[str]) -> dict[str, LensEval]:
    """
    Parallel execution of all lens evaluations.
    Each lens sees only the thesis, not other lenses' work.
    """
    evaluations = {}
    
    for lens in lenses:
        template = LENS_TEMPLATES[lens]
        
        evaluation = evaluate_with_lens(
            thesis=thesis,
            objective=template["objective"],
            attack_vectors=template["attack_vectors"],
            output_schema=template["output"]
        )
        
        evaluations[lens] = evaluation
    
    return evaluations
```

**Output per lens**:
```yaml
initial_evaluation:
  lens: S|E|O|A|P
  attacks:
    - id: ATK_{lens}_{n}
      target: C{id}
      type: "{attack_vector}"
      content: "{Specific critique}"
      severity: fatal|major|minor|cosmetic
      confidence_impact: -0.0 to -1.0
  summary_score: 0.0-1.0
  top_vulnerabilities: [ATK_ids ranked by severity]
```

## Phase 2b: Cross-Evaluation Protocol

Each lens evaluates each other lens's critique. **Now sees other lenses' work.**

### Cross-Evaluation Questions

When Lens X evaluates Lens Y's critique:

1. **Validity Check**: Did Y identify real weaknesses?
   - Is the attacked claim actually vulnerable in that way?
   - Is the attack type appropriate for the claim?
   - Is the severity rating calibrated?

2. **Completeness Check**: Did Y miss anything X would catch?
   - From X's perspective, what did Y overlook?
   - Are there related attacks Y should have included?

3. **Quality Check**: Is Y's critique well-formed?
   - Does Y's attack have clear targets and rationale?
   - Is Y attacking the actual claim or a strawman?
   - Does Y's attack contain its own logical flaws?

4. **Calibration Check**: Is Y's severity rating accurate?
   - Is "fatal" really fatal, or recoverable?
   - Is "minor" actually minor, or underestimated?

### Cross-Evaluation Schema

```yaml
cross_evaluation:
  evaluator: S|E|O|A|P
  evaluated: S|E|O|A|P
  
  attack_verdicts:
    - attack_id: ATK_{evaluated}_{n}
      verdict: endorse|partial|reject
      rationale: "{Why this verdict}"
      calibration: over|accurate|under
      
  agreements:
    - attack_id: ATK_{evaluated}_{n}
      endorsement: "{Why valid from evaluator's perspective}"
      strength_modifier: +0.0 to +0.3  # Boost if cross-endorsed
      
  disagreements:
    - attack_id: ATK_{evaluated}_{n}
      objection: "{Why flawed from evaluator's perspective}"
      objection_type: strawman|overreach|miscalibrated|invalid
      
  gaps_identified:
    - description: "{What evaluated lens missed}"
      why_matters: "{Impact of the gap}"
      suggested_attack: "{What should have been included}"
      
  meta_assessment:
    overall_quality: poor|fair|good|excellent
    blind_spots: ["{Systematic issues in evaluated lens}"]
    strengths: ["{What evaluated lens did well}"]
```

### Execution Order

```python
def execute_cross_evaluations(
    initial_evals: dict[str, LensEval],
    lenses: list[str]
) -> dict[tuple[str,str], CrossEval]:
    """
    Each lens evaluates each other lens's initial evaluation.
    Can be parallelized within each evaluating lens.
    """
    cross_evals = {}
    
    for evaluator in lenses:
        for evaluated in lenses:
            if evaluator == evaluated:
                continue  # Skip self-evaluation
            
            cross_eval = evaluate_lens_critique(
                evaluator_lens=evaluator,
                evaluated_critique=initial_evals[evaluated],
                evaluator_template=LENS_TEMPLATES[evaluator]
            )
            
            cross_evals[(evaluator, evaluated)] = cross_eval
    
    return cross_evals
```

## Matrix Analysis Patterns

### Pattern 1: Consensus Detection

```python
def find_consensus_attacks(matrix: EvalMatrix, threshold: float = 0.8) -> list[Attack]:
    """
    Attacks endorsed by ≥threshold of lenses (including cross-eval).
    """
    consensus = []
    
    for attack in matrix.all_attacks:
        # Direct endorsements from other lenses
        endorsement_count = sum(
            1 for lens in matrix.lenses
            if lens != attack.source and matrix.endorses(lens, attack)
        )
        
        # Total possible endorsements
        possible = len(matrix.lenses) - 1
        
        if endorsement_count / possible >= threshold:
            consensus.append(attack)
    
    return consensus
```

### Pattern 2: Contested Detection

```python
def find_contested_attacks(
    matrix: EvalMatrix,
    lower: float = 0.4,
    upper: float = 0.8
) -> list[Attack]:
    """
    Attacks with genuine disagreement (neither consensus nor rejected).
    """
    contested = []
    
    for attack in matrix.all_attacks:
        endorsement_rate = matrix.endorsement_rate(attack)
        
        if lower <= endorsement_rate < upper:
            contested.append(ContestedAttack(
                attack=attack,
                supporters=[l for l in matrix.lenses if matrix.endorses(l, attack)],
                opposers=[l for l in matrix.lenses if matrix.rejects(l, attack)],
                abstainers=[l for l in matrix.lenses if matrix.abstains(l, attack)]
            ))
    
    return contested
```

### Pattern 3: Unique Insight Detection

```python
def find_unique_insights(matrix: EvalMatrix) -> list[Attack]:
    """
    Attacks from single lens that survive cross-evaluation.
    These are valuable specialized insights other lenses missed.
    """
    unique = []
    
    for attack in matrix.all_attacks:
        # Only from one lens
        if matrix.source_count(attack) > 1:
            continue
        
        # But not rejected by cross-eval
        rejection_count = sum(
            1 for lens in matrix.lenses
            if lens != attack.source and matrix.rejects(lens, attack)
        )
        
        if rejection_count == 0:
            unique.append(attack)
    
    return unique
```

### Pattern 4: Credibility Scoring

```python
def compute_lens_credibility(lens: str, matrix: EvalMatrix) -> float:
    """
    How much weight to give a lens based on cross-eval performance.
    
    Factors:
    - How often were this lens's attacks endorsed by others?
    - How often did this lens's cross-evals align with consensus?
    - Were this lens's severity ratings accurate?
    """
    
    # Attack endorsement rate
    own_attacks = matrix.attacks_from(lens)
    endorsed = sum(1 for a in own_attacks if matrix.is_consensus(a))
    attack_score = endorsed / len(own_attacks) if own_attacks else 0.5
    
    # Cross-eval alignment
    own_cross_evals = matrix.cross_evals_from(lens)
    aligned = sum(1 for ce in own_cross_evals if matrix.aligns_with_consensus(ce))
    alignment_score = aligned / len(own_cross_evals) if own_cross_evals else 0.5
    
    # Calibration accuracy
    calibration_score = matrix.calibration_accuracy(lens)
    
    return 0.4 * attack_score + 0.3 * alignment_score + 0.3 * calibration_score
```

## Conflict Resolution Procedures

### Procedure 1: Weighted Voting

```python
def resolve_by_weighted_vote(
    contested: ContestedAttack,
    matrix: EvalMatrix
) -> Resolution:
    """
    Weight each lens's vote by credibility score.
    """
    support_weight = sum(
        matrix.credibility(lens) for lens in contested.supporters
    )
    oppose_weight = sum(
        matrix.credibility(lens) for lens in contested.opposers
    )
    
    if support_weight > oppose_weight * 1.5:
        return Resolution("ADOPT", contested.attack)
    elif oppose_weight > support_weight * 1.5:
        return Resolution("REJECT", contested.attack)
    else:
        return Resolution("CONDITIONAL", contested.attack, 
                        condition=synthesize_condition(contested))
```

### Procedure 2: Argument Quality

```python
def resolve_by_argument_quality(
    contested: ContestedAttack,
    matrix: EvalMatrix
) -> Resolution:
    """
    Compare the quality of supporting vs opposing arguments.
    """
    support_args = [
        matrix.get_rationale(lens, contested.attack)
        for lens in contested.supporters
    ]
    oppose_args = [
        matrix.get_objection(lens, contested.attack)
        for lens in contested.opposers
    ]
    
    # Evaluate argument quality (could use LLM or heuristics)
    support_quality = evaluate_argument_quality(support_args)
    oppose_quality = evaluate_argument_quality(oppose_args)
    
    if support_quality > oppose_quality:
        return Resolution("ADOPT", contested.attack)
    elif oppose_quality > support_quality:
        return Resolution("REJECT", contested.attack)
    else:
        return Resolution("CONDITIONAL", contested.attack)
```

### Procedure 3: Domain Priority

```python
def resolve_by_domain_priority(
    contested: ContestedAttack,
    matrix: EvalMatrix
) -> Resolution:
    """
    Give priority to lenses most relevant to attack type.
    """
    attack_type = contested.attack.type
    
    # Map attack types to most authoritative lenses
    authority_map = {
        "logical": ["S"],           # STRUCTURAL authoritative on logic
        "evidential": ["E"],        # EVIDENTIAL authoritative on evidence
        "scope": ["O"],             # SCOPE authoritative on boundaries
        "counter": ["A"],           # ADVERSARIAL authoritative on opposition
        "practical": ["P"]          # PRAGMATIC authoritative on implementation
    }
    
    authoritative_lenses = authority_map.get(attack_type, [])
    
    # Check what authoritative lenses say
    auth_support = any(l in contested.supporters for l in authoritative_lenses)
    auth_oppose = any(l in contested.opposers for l in authoritative_lenses)
    
    if auth_support and not auth_oppose:
        return Resolution("ADOPT", contested.attack)
    elif auth_oppose and not auth_support:
        return Resolution("REJECT", contested.attack)
    else:
        # Fall back to weighted voting
        return resolve_by_weighted_vote(contested, matrix)
```

## Matrix Visualization

```
EVALUATION MATRIX SUMMARY
═══════════════════════════════════════════════════════════════

THESIS ATTACKS (Diagonal):
  S: 4 attacks (2 fatal, 1 major, 1 minor)
  E: 3 attacks (1 fatal, 2 major)
  O: 5 attacks (0 fatal, 3 major, 2 minor)
  A: 2 attacks (1 fatal, 1 major)
  P: 3 attacks (1 fatal, 1 major, 1 minor)

CROSS-EVAL SUMMARY:
  Total cells: 20 (5×4)
  Average endorsement rate: 0.72
  High agreement pairs: S↔E (0.89), O↔P (0.85)
  Low agreement pairs: A↔S (0.51), E↔A (0.48)

ATTACK STATUS:
  Consensus (≥80%): 7 attacks
  Contested (40-80%): 5 attacks
  Unique insights: 3 attacks
  Rejected (<40%): 2 attacks

LENS CREDIBILITY:
  S: 0.84  E: 0.79  O: 0.76  A: 0.68  P: 0.81

═══════════════════════════════════════════════════════════════
```

## Output Aggregation

```yaml
matrix_analysis:
  consensus_attacks:
    - attack_id: ATK_S_1
      endorsement_rate: 0.95
      endorsing_lenses: [S, E, O, P]
      action: MANDATORY_ADDRESS
      
  contested_attacks:
    - attack_id: ATK_A_2
      endorsement_rate: 0.55
      supporters: [A, O]
      opposers: [S, E]
      resolution: CONDITIONAL
      condition: "Valid if interpreting claim literally"
      
  unique_insights:
    - attack_id: ATK_O_4
      source: O
      cross_eval_status: not_rejected
      value: "Edge case reveals important limitation"
      
  rejected_attacks:
    - attack_id: ATK_A_1
      rejection_rate: 0.85
      reason: "Strawman - attacks claim thesis didn't make"
      
  lens_credibility:
    S: 0.84
    E: 0.79
    O: 0.76
    A: 0.68
    P: 0.81
```
