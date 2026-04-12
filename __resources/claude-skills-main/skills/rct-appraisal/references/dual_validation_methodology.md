# Dual-Validation Methodology for RCT Appraisal

## Overview

Dual-validation employs two independent appraisers conducting concurrent evaluations, followed by concordance analysis and resolution of discordances. This methodology enhances reliability and reduces individual bias in quality assessment.

**Note**: This is similar to the triple-validation used in NMA-appraisal but streamlined for RCT assessment (dual appraisers + meta-review for discordances only).

## Appraiser Roles

### Appraiser #1: Critical Reviewer

**Stance**: Skeptical, conservative
**Evidence threshold**: HIGH
**Bias direction**: Favors more stringent ratings
**Focus**: Identifying methodological gaps and concerns

**Rating approach:**
- Requires explicit, unambiguous evidence to rate ✓
- Interprets ambiguous information conservatively
- Applies strict interpretation of criteria
- Quick to identify "some concerns" or "high risk"

**Example behavior:**
- If randomization method described as "computer-generated" without further detail → Some Concerns (not Low Risk)
- If harms reported but no severity grading → ✗ (not ⚠)
- If intervention described but lacks dose/duration detail → ⚠ (not ✓)

### Appraiser #2: Methodologist

**Stance**: Technical rigor emphasis
**Evidence threshold**: MODERATE
**Bias direction**: Focuses on methodological soundness
**Focus**: Assessing technical implementation quality

**Rating approach:**
- Accepts reasonable inferences from context
- Interprets standard methods charitably if described
- Emphasizes statistical and design considerations
- Balances ideal vs pragmatic trial quality

**Example behavior:**
- If randomization method described as "computer-generated" → Low Risk (standard method)
- If harms reported but no severity grading → ⚠ (present but incomplete)
- If intervention described with key elements → ✓ (sufficient for replication)

## Independence Protocol

**CRITICAL**: Appraisers must work independently to prevent anchoring bias

### Before Appraisal
1. Both appraisers receive same materials (RCT PDF, frameworks)
2. Agree on appraisal scope (comprehensive vs focused)
3. Schedule independent work periods (no communication during appraisal)

### During Appraisal
- **NO discussion** of ratings between appraisers
- **NO sharing** of preliminary findings
- Document evidence independently
- Complete all frameworks before comparing

### After Independent Appraisal
- Submit ratings simultaneously to prevent anchoring
- Compare ratings systematically (concordance analysis)
- Discuss discordances with evidence from both appraisers
- Apply resolution strategy to reach consensus

## Concordance Analysis

### Agreement Levels

**Perfect Agreement:**
- Both appraisers assign identical ratings
- Confidence: Very high
- Action: Accept rating without further review
- Example: Both rate CONSORT Item 1a as ✓

**Minor Discordance:**
- Adjacent ratings differ by one level
- Examples: ✓ vs ⚠, or ⚠ vs ✗
- Confidence: Moderate-High
- Action: Apply resolution strategy (usually evidence-weighted)

**Major Discordance:**
- Opposite ratings (✓ vs ✗)
- Confidence: Low
- Action: Mandatory meta-review with justification from both appraisers
- Example: Appraiser #1 rates RoB 2.0 Domain 4 as HIGH RISK; Appraiser #2 rates as LOW RISK

**N/A Discordance:**
- One appraiser rates N/A, other rates ✓/⚠/✗
- Confidence: Variable
- Action: Review criterion applicability; usually defer to substantive rating if justified

### Agreement Metrics

Calculate after all items rated:

**Overall Agreement Rate:**
```
Agreement Rate = (Perfect Agreement Items) / (Total Items)
Target: ≥70%
```

**Cohen's Kappa** (optional):
```
Kappa adjusts for chance agreement
Interpretation: <0.20 (poor), 0.21-0.40 (fair), 0.41-0.60 (moderate),
0.61-0.80 (substantial), >0.80 (almost perfect)
Target: ≥0.60
```

**Discordance Distribution:**
```
Major Discordances: Should be <5% of items
Minor Discordances: Expected 20-30% of items
Perfect Agreement: Target ≥70%
```

## Resolution Strategies

### Evidence-Weighted Resolution (Default)

**Principle**: Select rating with stronger supporting evidence

**Process:**
1. Each appraiser presents evidence for their rating
2. Compare:
   - Specificity of evidence (explicit statement > inference)
   - Location of evidence (methods > discussion)
   - Quality of evidence (trial report > assumptions)
3. Select rating with more compelling evidence
4. Document rationale

**Example:**
```
Item: CONSORT 8a (random sequence generation)
Appraiser #1: ⚠ (states "randomized" but no method described)
Appraiser #2: ✓ (states "computer-generated randomization")

Resolution:
- Appraiser #2 provides specific quote from Methods: "Randomization was
  computer-generated using permuted blocks of 4"
- Evidence: Explicit, specific method described
- Consensus: ✓ (evidence supports adequate reporting)
```

### Conservative Resolution

**Principle**: Select more conservative (worse) rating

**Use when:**
- High-stakes decisions (regulatory, reimbursement)
- Uncertainty about evidence quality
- Risk tolerance favors false negatives over false positives

**Process:**
1. Identify more conservative rating (✗ > ⚠ > ✓)
2. Accept conservative rating as consensus
3. Document conservative approach used

**Example:**
```
Item: RoB 2.0 Domain 2 (Deviations)
Appraiser #1: Some Concerns (unblinded, potential context-driven deviations)
Appraiser #2: Low Risk (ITT analysis mitigates concerns)

Conservative Resolution: Some Concerns
Rationale: When uncertain, err on side of caution for bias risk
```

### Liberal Resolution

**Principle**: Select less conservative (better) rating

**Use when:**
- Formative assessment or educational context
- Benefit of doubt appropriate
- False positives preferable to false negatives

**Process:**
1. Identify less conservative rating (✓ > ⚠ > ✗)
2. Verify minimum evidence threshold met
3. Accept liberal rating as consensus
4. Document liberal approach used

**Note**: Liberal resolution is RARELY appropriate for RCT appraisal; use with caution

### Expert Arbitration (For Unresolved Discordances)

**Use when:**
- Major discordance with equal evidence quality
- Discordance reflects methodological ambiguity
- Standard resolution strategies fail

**Process:**
1. Present case to third expert reviewer (not involved in appraisal)
2. Expert reviews evidence from both appraisers
3. Expert provides independent judgment with rationale
4. Expert decision is final

## Quality Control Checks

### Minimum Standards

**Overall Agreement Rate**: ≥70%
- Below 70% suggests inadequate appraiser training or ambiguous criteria

**Major Discordance Rate**: ≤5%
- Above 5% suggests fundamental disagreement on evidence interpretation

**Evidence Confidence**: ≥60% of items with ≥moderate confidence
- Below 60% suggests inadequate trial reporting or evidence extraction

### Flags for Review

**Systematic Disagreement on Specific Sections:**
- Example: Appraiser #1 consistently rates RoB 2.0 more strictly
- Action: Re-review section with explicit discussion of rating criteria

**Low Evidence Confidence on Critical Items:**
- Example: Cannot confidently rate randomization due to poor reporting
- Action: Flag as limitation in appraisal report

**Major Discordance on Outcome-Determinative Items:**
- Example: Disagree on whether primary outcome is patient-important (affects GRADE indirectness)
- Action: Mandatory expert arbitration

## Documentation Requirements

### For Each Item

**Record:**
1. Rating (✓/⚠/✗/N/A)
2. Confidence level (high/moderate/low/unable)
3. Evidence source (specific location in paper)
4. Evidence quote or summary
5. Rationale for rating

### For Discordances

**Record:**
1. Initial ratings from both appraisers
2. Evidence presented by each appraiser
3. Resolution strategy applied
4. Final consensus rating
5. Rationale for consensus

**Example documentation:**
```
Item: Benefits/Harms H4 (Specific Harms of Interest)

Appraiser #1 Rating: ✗
Confidence: High
Evidence: "No mention of hepatotoxicity monitoring despite known class effect"
Rationale: Expected harm not assessed

Appraiser #2 Rating: ⚠
Confidence: Moderate
Evidence: "Liver function tests performed at baseline and endpoint per Table 2"
Rationale: Some monitoring but not comprehensive

Discordance Type: Minor (adjacent ratings)
Resolution Strategy: Evidence-weighted
Evidence Comparison:
- Appraiser #2 provides specific table reference showing LFT monitoring
- Appraiser #1 correct that no explicit hepatotoxicity assessment mentioned
- LFTs are indirect measure of hepatotoxicity

Consensus: ⚠
Rationale: Some monitoring present via LFTs but not explicitly framed as
hepatotoxicity assessment. Partial compliance.
```

## Appraiser Training

### Before First Appraisal

**Requirements:**
1. Read all 6 framework reference documents
2. Complete practice appraisal on training RCT
3. Compare practice ratings with gold standard
4. Discuss discrepancies and calibrate

**Calibration Process:**
- Both appraisers independently rate training RCT
- Compare with expert-rated gold standard
- Target: ≥80% agreement with gold standard before proceeding

### Ongoing Calibration

- After every 3-5 appraisals, review agreement metrics
- If agreement drops below 70%, re-calibrate
- Discuss systematic disagreements and refine criteria interpretation

## Benefits of Dual-Validation

**Reduces individual bias:**
- Skeptical reviewer catches over-optimistic ratings
- Methodologist prevents overly harsh ratings
- Balance reduces extreme ratings

**Increases reliability:**
- High agreement indicates robust, reproducible assessment
- Discordances identify ambiguous or poorly reported items

**Enhances credibility:**
- Independent appraisals more trustworthy than single reviewer
- Transparent resolution process demonstrates rigor

**Improves learning:**
- Appraisers learn from each other's evidence interpretation
- Calibration discussions enhance framework understanding

## Limitations

**Time-intensive:**
- Requires two appraisers (double time investment)
- Concordance analysis adds overhead

**Not always feasible:**
- Single reviewer may be only option for rapid appraisal
- Can be simplified to single appraiser + self-review after 24 hours

**Agreement ≠ Accuracy:**
- High agreement between appraisers doesn't guarantee correct ratings
- Both could be wrong if trial reporting is ambiguous

## Simplified Alternative: Single Appraiser with Self-Review

If dual appraisal not feasible:

1. **Day 1**: Complete initial appraisal
2. **Day 2+**: Re-review appraisal after 24-48 hours without consulting initial ratings
3. Compare self-ratings and resolve self-discordances
4. Document changed ratings with rationale

**Less rigorous** than dual validation but better than single-pass appraisal

## References

1. Hartling L, Hamm MP, Milne A, et al. Testing the risk of bias tool showed low reliability between individual reviewers. *J Clin Epidemiol* 2013;66(9):973-983.

2. Armijo-Olivo S, Stiles CR, Hagen NA, et al. Assessment of study quality for systematic reviews: a comparison of the Cochrane Collaboration Risk of Bias Tool and the Effective Public Health Practice Project Quality Assessment Tool. *J Eval Clin Pract* 2012;18(1):12-18.

3. Jørgensen L, Paludan-Müller AS, Laursen DR, et al. Evaluation of the Cochrane tool for assessing risk of bias in randomized clinical trials. *Int J Epidemiol* 2016;45(6):1866-1877.
