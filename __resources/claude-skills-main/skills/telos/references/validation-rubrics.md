# Validation Rubrics for Teleological Claims

## Purpose

Teleological analysis generates claims about biological optimization. These rubrics ensure claims are rigorous, falsifiable, and scientifically valid—not post-hoc rationalization.

## Claim Types and Validation Requirements

### Type 1: Single-Constraint Optimization

**Claim structure**: "System X is optimized for constraint Y"

| Criterion | Required Evidence |
|-----------|-------------------|
| Constraint identification | Explicit physical/chemical/energetic basis |
| Optimality measure | Quantitative metric defining "optimal" |
| Comparison to alternatives | Why observed design beats alternatives |
| Deviation cost | What happens when constraint is violated |

**Scoring**:
- 1 point: Constraint identified but not quantified
- 2 points: Quantified constraint with metric
- 3 points: Comparison to alternatives provided
- 4 points: Deviation cost demonstrated experimentally

### Type 2: Multi-Constraint Optimization

**Claim structure**: "System X resolves conflict between constraints Y and Z"

| Criterion | Required Evidence |
|-----------|-------------------|
| Constraint enumeration | All relevant constraints listed (minimum 3) |
| Conflict identification | How constraints oppose each other |
| Resolution mechanism | How design addresses all constraints |
| Trade-off quantification | Position on Pareto frontier |
| Alternative rejection | Why simpler designs fail |

**Scoring** (per criterion):
- 0: Not addressed
- 1: Mentioned qualitatively
- 2: Analyzed with reasoning
- 3: Quantified with data/equations

**Minimum passing score**: 10/15 with no zeros

### Type 3: Convergent Design

**Claim structure**: "Design X represents convergent solution to universal constraint"

| Criterion | Required Evidence |
|-----------|-------------------|
| Independent origins | Phylogenetically distinct taxa |
| Constraint universality | Same physical/chemical constraints apply |
| Design similarity | Structural/functional homoplasy |
| Alternative exclusion | Other taxa show design failure modes |

**Scoring**:
- Weak (1): 2 taxa, related constraints
- Moderate (2): 3+ taxa, clear constraints
- Strong (3): 5+ taxa across kingdoms, quantified similarity

## Red Flags: Invalid Teleological Reasoning

### 1. Post-Hoc Rationalization
**Pattern**: Observing feature → inventing purpose
**Fix**: Start from constraints, predict features

**Example (bad)**: "The appendix must serve a purpose, so it probably stores bacteria"
**Example (good)**: "Given need for bacterial reservoir + anatomical constraints, appendix location and structure are predicted"

### 2. Unfalsifiable Claims
**Pattern**: Any observation confirms the claim
**Fix**: Specify what would refute the claim

**Unfalsifiable**: "This is optimized for the organism's needs"
**Falsifiable**: "If this were optimized for oxygen transport, we would expect P50 between 25-30 mmHg"

### 3. Single-Constraint Tunnel Vision
**Pattern**: Optimize for one constraint, ignore trade-offs
**Fix**: Enumerate all constraints before analysis

**Tunnel vision**: "Thick bones would be better for strength"
**Multi-constraint**: "Bone thickness trades off against weight, metabolic cost, and growth requirements"

### 4. Ignoring Historical Contingency
**Pattern**: Assuming current design is optimal from first principles
**Fix**: Acknowledge phylogenetic constraints

**Ahistorical**: "Vertebrate eyes are optimally designed"
**Historical**: "Given inherited constraints from ancestral forms, vertebrate eyes optimize within available design space"

### 5. Panglossian Fallacy
**Pattern**: Assuming everything has adaptive purpose
**Fix**: Allow for vestigial, neutral, or maladaptive features

**Panglossian**: "Every anatomical feature must serve a function"
**Realistic**: "Some features are vestigial (wisdom teeth), pleiotropic side effects, or phylogenetic baggage"

## Quantitative Validation Metrics

### Optimization Efficiency

```
η = (Actual performance) / (Theoretical maximum)
```

| Rating | η Value | Interpretation |
|--------|---------|----------------|
| Weak | < 0.5 | Substantial room for improvement |
| Moderate | 0.5-0.8 | Reasonable but not optimal |
| Strong | 0.8-0.95 | Near-optimal performance |
| Exceptional | > 0.95 | At physical limits |

### Pareto Frontier Position

For multi-constraint optimization:

```
Distance from Pareto frontier = √(Σ(xᵢ - xᵢ*)²)
where xᵢ* = Pareto-optimal value for constraint i
```

| Rating | Distance | Interpretation |
|--------|----------|----------------|
| Optimal | 0 | On Pareto frontier |
| Near-optimal | < 0.1 | Close to frontier |
| Suboptimal | 0.1-0.3 | Clear trade-off costs |
| Poor | > 0.3 | Not optimized |

### Predictive Accuracy

```
Accuracy = (Confirmed predictions) / (Total predictions made)
```

| Rating | Accuracy | Interpretation |
|--------|----------|----------------|
| Weak | < 0.5 | Poor predictive power |
| Moderate | 0.5-0.7 | Some predictive value |
| Strong | 0.7-0.9 | Good predictions |
| Exceptional | > 0.9 | High predictive power |

## Comprehensive Validation Checklist

### Before Analysis
- [ ] Primary constraints identified from first principles
- [ ] Constraint conflicts mapped
- [ ] Falsifiable predictions generated
- [ ] Alternative designs considered

### During Analysis
- [ ] All claims tied to specific constraints
- [ ] Quantitative metrics where possible
- [ ] Trade-offs explicitly acknowledged
- [ ] Historical/phylogenetic context considered

### After Analysis
- [ ] Claims falsifiable and testable
- [ ] Predictions align with experimental data
- [ ] Alternative explanations addressed
- [ ] Uncertainty/limitations stated

## Integrating with Examination Preparation

### SAQ Application

When applying teleological reasoning in exam answers:

1. **Lead with mechanism** (examiners expect this)
2. **Add teleological context** as value-add
3. **Quantify where possible** (shows depth)
4. **Predict clinical implications** (integration points)

**Template**:
```
[Mechanism description - standard]
↓
[Constraint context - why this mechanism?]
↓  
[Multi-constraint integration - sophisticated understanding]
↓
[Clinical prediction - application]
```

### Avoiding Examiner Pitfalls

Examiners may challenge teleological claims. Prepare by:
- Acknowledging limitations of teleological reasoning
- Distinguishing heuristic from metaphysical claims
- Having mechanistic backup for all claims
- Showing awareness of historical contingency
