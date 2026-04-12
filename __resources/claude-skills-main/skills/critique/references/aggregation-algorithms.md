# Aggregation Algorithms Reference

Consensus extraction, conflict resolution, and recursive compression procedures for Φ3.

## Aggregation Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AGGREGATION PIPELINE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Matrix Analysis ──► Categorization ──► Resolution ──► Compression         │
│        │                   │                │               │               │
│        ▼                   ▼                ▼               ▼               │
│   ┌─────────┐        ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│   │ Compute │        │ Consensus│    │ Weighted │    │ Pass 1:  │          │
│   │ endorse-│───────►│ Contested│───►│ voting   │───►│ Core     │          │
│   │ ment    │        │ Unique   │    │ Argument │    │          │          │
│   │ rates   │        │ Rejected │    │ quality  │    │ Pass 2:  │          │
│   └─────────┘        └──────────┘    └──────────┘    │ Cond.    │          │
│                                                      │          │          │
│                                                      │ Pass 3:  │          │
│                                                      │ Enhance  │          │
│                                                      │          │          │
│                                                      │ Pass 4:  │          │
│                                                      │ Validate │          │
│                                                      └──────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Step 1: Categorization

### 1.1 Compute Endorsement Rates

```python
def compute_endorsement_rates(matrix: EvalMatrix) -> dict[str, float]:
    """
    For each attack, compute what fraction of non-source lenses endorse it.
    """
    rates = {}
    
    for attack in matrix.all_attacks:
        source = attack.source_lens
        other_lenses = [l for l in matrix.lenses if l != source]
        
        endorsements = 0
        for lens in other_lenses:
            cross_eval = matrix.get_cross_eval(lens, source)
            if cross_eval.endorses(attack):
                endorsements += 1
        
        rates[attack.id] = endorsements / len(other_lenses)
    
    return rates
```

### 1.2 Categorize Attacks

```python
@dataclass
class CategorizedAttacks:
    consensus: list[Attack]      # ≥80% endorsement
    contested: list[Attack]      # 40-80% endorsement
    unique: list[Attack]         # Single source, not rejected
    rejected: list[Attack]       # <40% endorsement

def categorize_attacks(
    matrix: EvalMatrix,
    rates: dict[str, float]
) -> CategorizedAttacks:
    
    consensus = []
    contested = []
    unique = []
    rejected = []
    
    for attack in matrix.all_attacks:
        rate = rates[attack.id]
        
        if rate >= 0.80:
            consensus.append(attack)
        elif rate >= 0.40:
            contested.append(attack)
        elif rate < 0.40:
            # Check if unique insight (single source, not actively rejected)
            active_rejections = matrix.active_rejection_count(attack)
            if matrix.source_count(attack) == 1 and active_rejections == 0:
                unique.append(attack)
            else:
                rejected.append(attack)
    
    return CategorizedAttacks(consensus, contested, unique, rejected)
```

## Step 2: Resolution

### 2.1 Consensus Resolution (Automatic)

```python
def resolve_consensus(
    thesis: Thesis,
    consensus_attacks: list[Attack]
) -> list[Modification]:
    """
    Consensus attacks require mandatory response.
    No deliberation needed—just determine response type.
    """
    modifications = []
    
    for attack in consensus_attacks:
        target_claim = thesis.get_claim(attack.target)
        
        if attack.severity == "fatal":
            # Fatal consensus attack → claim must be withdrawn or fundamentally revised
            modifications.append(Modification(
                claim=target_claim,
                action="WITHDRAW" if not repairable(target_claim, attack) else "MAJOR_REVISE",
                source="consensus",
                rationale=f"Endorsed by {attack.endorsement_rate:.0%} of lenses",
                attacks_addressed=[attack.id]
            ))
        else:
            # Non-fatal consensus → revision or qualification
            modifications.append(Modification(
                claim=target_claim,
                action="REVISE" if attack.severity == "major" else "QUALIFY",
                source="consensus",
                rationale=f"Endorsed by {attack.endorsement_rate:.0%} of lenses",
                attacks_addressed=[attack.id]
            ))
    
    return modifications
```

### 2.2 Contested Resolution (Deliberative)

```python
def resolve_contested(
    thesis: Thesis,
    contested_attacks: list[Attack],
    matrix: EvalMatrix
) -> list[Modification]:
    """
    Contested attacks require deliberative resolution.
    Use multiple resolution strategies and synthesize.
    """
    modifications = []
    
    for attack in contested_attacks:
        # Strategy 1: Weighted voting
        vote_result = resolve_by_weighted_vote(attack, matrix)
        
        # Strategy 2: Argument quality
        quality_result = resolve_by_argument_quality(attack, matrix)
        
        # Strategy 3: Domain authority
        domain_result = resolve_by_domain_authority(attack, matrix)
        
        # Synthesize strategies
        if all_agree([vote_result, quality_result, domain_result]):
            decision = vote_result.decision
            confidence = "high"
        elif majority_agree([vote_result, quality_result, domain_result]):
            decision = majority_decision([vote_result, quality_result, domain_result])
            confidence = "medium"
        else:
            decision = "CONDITIONAL"
            confidence = "low"
        
        # Generate modification
        if decision == "ADOPT":
            modifications.append(Modification(
                claim=thesis.get_claim(attack.target),
                action="REVISE",
                source="contested_resolved",
                rationale=synthesize_rationale(attack, matrix),
                confidence=confidence,
                attacks_addressed=[attack.id]
            ))
        elif decision == "CONDITIONAL":
            modifications.append(Modification(
                claim=thesis.get_claim(attack.target),
                action="CONDITIONAL_REVISE",
                source="contested_conditional",
                condition=synthesize_condition(attack, matrix),
                rationale=f"Supporters: {attack.supporters}, Opposers: {attack.opposers}",
                confidence=confidence,
                attacks_addressed=[attack.id]
            ))
        # REJECT → no modification, but record decision
    
    return modifications
```

### 2.3 Unique Insight Integration

```python
def integrate_unique_insights(
    thesis: Thesis,
    unique_attacks: list[Attack],
    matrix: EvalMatrix
) -> list[Enhancement]:
    """
    Unique insights add value without consensus.
    Integrate as enhancements, not mandatory changes.
    """
    enhancements = []
    
    for attack in unique_attacks:
        # Unique insights typically reveal edge cases, nuances, or specialized concerns
        enhancement = Enhancement(
            claim=thesis.get_claim(attack.target),
            type="NUANCE" if attack.severity in ["minor", "cosmetic"] else "CAVEAT",
            content=synthesize_enhancement(attack),
            source_lens=attack.source_lens,
            rationale=f"Specialized insight from {attack.source_lens} lens, not rejected by others"
        )
        enhancements.append(enhancement)
    
    return enhancements
```

## Step 3: Recursive Compression

### 3.1 Four-Pass Compression

```python
def recursive_compress(
    thesis: Thesis,
    categorized: CategorizedAttacks,
    matrix: EvalMatrix,
    max_passes: int = 4
) -> Synthesis:
    """
    Compress through iterative passes until coherent.
    """
    
    # Pass 1: Apply consensus modifications (mandatory)
    consensus_mods = resolve_consensus(thesis, categorized.consensus)
    stage_1 = apply_modifications(thesis, consensus_mods)
    
    # Pass 2: Apply contested resolutions (conditional)
    contested_mods = resolve_contested(stage_1, categorized.contested, matrix)
    stage_2 = apply_modifications(stage_1, contested_mods)
    
    # Pass 3: Integrate unique insights (enhancement)
    unique_enhancements = integrate_unique_insights(stage_2, categorized.unique, matrix)
    stage_3 = apply_enhancements(stage_2, unique_enhancements)
    
    # Pass 4: Validate coherence
    if not validate_coherence(stage_3):
        # Coherence violation—need recursive re-compression
        if max_passes > 1:
            # Identify incoherent elements
            incoherent = find_incoherent_elements(stage_3)
            
            # Remove or reconcile incoherent elements
            reconciled = reconcile_incoherence(stage_3, incoherent)
            
            # Recursive call with tighter constraints
            return recursive_compress(
                reconciled,
                reanalyze_remaining(categorized, reconciled),
                matrix,
                max_passes - 1
            )
        else:
            # Max passes exhausted—flag incoherence
            return Synthesis(
                result=stage_3,
                coherent=False,
                incoherence_notes=describe_incoherence(stage_3)
            )
    
    return Synthesis(
        result=stage_3,
        coherent=True,
        modifications=consensus_mods + contested_mods,
        enhancements=unique_enhancements,
        rejected=categorized.rejected
    )
```

### 3.2 Coherence Validation

```python
def validate_coherence(synthesis: ThesisState) -> bool:
    """
    Check synthesis for internal coherence.
    """
    # 1. No contradictions between claims
    if has_contradictions(synthesis.claims):
        return False
    
    # 2. Dependency graph still valid (DAG)
    if has_cycles(synthesis.claim_graph):
        return False
    
    # 3. Modified claims consistent with retained claims
    if modifications_conflict_with_retained(synthesis):
        return False
    
    # 4. Conditional modifications don't contradict each other
    if conditional_conflicts(synthesis.conditional_modifications):
        return False
    
    # 5. Topology still meets minimum thresholds
    if synthesis.topology.density < 1.5:  # Allow some degradation
        return False
    
    return True
```

### 3.3 Incoherence Reconciliation

```python
def reconcile_incoherence(
    synthesis: ThesisState,
    incoherent: list[IncoherenceIssue]
) -> ThesisState:
    """
    Resolve incoherence by removing or modifying conflicting elements.
    """
    reconciled = synthesis.copy()
    
    for issue in incoherent:
        if issue.type == "contradiction":
            # Choose claim with higher support
            winner = choose_by_support(issue.claim_a, issue.claim_b, synthesis)
            loser = issue.claim_b if winner == issue.claim_a else issue.claim_a
            reconciled = remove_claim(reconciled, loser)
            
        elif issue.type == "cycle":
            # Break cycle at weakest edge
            weakest_edge = find_weakest_edge(issue.cycle, synthesis)
            reconciled = remove_edge(reconciled, weakest_edge)
            
        elif issue.type == "modification_conflict":
            # Prioritize consensus over contested over unique
            winner = choose_by_source_priority(issue.mod_a, issue.mod_b)
            loser = issue.mod_b if winner == issue.mod_a else issue.mod_a
            reconciled = revert_modification(reconciled, loser)
    
    return reconciled
```

## Output Schema

```yaml
aggregation_result:
  # Pass 1 outputs
  consensus_modifications:
    - claim: C{id}
      action: WITHDRAW|MAJOR_REVISE|REVISE|QUALIFY
      rationale: "{Endorsement rate and reasoning}"
      attacks_addressed: [ATK_ids]
      
  # Pass 2 outputs
  contested_resolutions:
    - claim: C{id}
      action: REVISE|CONDITIONAL_REVISE|NO_CHANGE
      condition: "{If conditional}"
      confidence: high|medium|low
      supporters: [lens_ids]
      opposers: [lens_ids]
      rationale: "{Resolution reasoning}"
      
  # Pass 3 outputs
  unique_enhancements:
    - claim: C{id}
      type: NUANCE|CAVEAT|EDGE_CASE
      content: "{Enhancement content}"
      source_lens: S|E|O|A|P
      
  # Pass 4 outputs
  coherence_status:
    coherent: true|false
    passes_required: 1-4
    reconciliations: ["{What was reconciled}"]
    
  # Rejected (recorded but not applied)
  rejected_attacks:
    - attack_id: ATK_{id}
      rejection_rate: 0.0-0.4
      reason: "{Why rejected}"
      
  # Final synthesis
  synthesized_thesis:
    response: "{Refined response}"
    claim_graph: {updated graph}
    confidence:
      initial: 0.0-1.0
      final: 0.0-1.0
      delta: +/- 0.0-1.0
```

## Convergence Computation

```python
def compute_final_convergence(
    original_thesis: Thesis,
    synthesis: Synthesis,
    matrix: EvalMatrix
) -> ConvergenceMetrics:
    """
    Compute convergence between original thesis and final synthesis.
    """
    
    # Semantic similarity
    semantic = cosine_similarity(
        embed(original_thesis.response),
        embed(synthesis.response)
    )
    
    # Structural similarity
    structural = jaccard_similarity(
        original_thesis.claim_graph.edges,
        synthesis.claim_graph.edges
    )
    
    # Confidence stability
    conf_delta = abs(synthesis.confidence.final - original_thesis.confidence)
    conf_stability = 1.0 - min(conf_delta, 1.0)
    
    # Consensus integration (how much consensus was incorporated)
    consensus_rate = len(synthesis.consensus_modifications) / max(1, len(matrix.consensus_attacks))
    
    # Weighted convergence
    convergence = (
        0.30 * semantic +
        0.25 * structural +
        0.25 * conf_stability +
        0.20 * consensus_rate
    )
    
    return ConvergenceMetrics(
        semantic=semantic,
        structural=structural,
        confidence_stability=conf_stability,
        consensus_integration=consensus_rate,
        overall=convergence
    )
```

## Complexity Scaling

| Complexity | Lenses | Matrix Size | Compression Passes | Target Convergence |
|------------|--------|-------------|--------------------|--------------------|
| Simple | 3 | 9 cells | 2 | 0.90 |
| Moderate | 5 | 25 cells | 3 | 0.95 |
| Complex | 5 | 25 cells | 4 | 0.98 |

## Edge Cases

### Too Few Attacks
If total attacks < 3, expand lens set or lower threshold for unique insights.

### No Consensus
If no attacks reach 80% endorsement, lower threshold to 70% for that iteration.

### All Rejected
If >80% attacks rejected, thesis likely robust—output with high confidence, noting low attack success rate.

### Incoherence Loop
If coherence validation fails after max passes, output with `coherent: false` flag and describe remaining issues.
