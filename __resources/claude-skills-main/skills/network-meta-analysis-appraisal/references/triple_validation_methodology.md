# Triple-Validation Methodology

## Overview

The triple-validation approach employs two independent appraisers conducting concurrent evaluations, followed by meta-review concordance analysis. This methodology reduces bias and increases reliability of appraisal ratings.

## Appraiser Roles

### Appraiser #1: Critical Reviewer
- **Stance**: Skeptical, conservative
- **Evidence threshold**: High (0.75)
- **Bias**: Prefers more stringent ratings
- **Focus**: Identifying gaps and methodological concerns

### Appraiser #2: Methodologist
- **Stance**: Technical rigor emphasis
- **Evidence threshold**: Moderate (0.70)
- **Bias**: Focuses on statistical and methodological precision
- **Focus**: Assessing technical implementation quality

## Concordance Analysis

### Agreement Levels

**Perfect Agreement**:
- Both appraisers assign identical ratings
- Confidence: Very high
- Action: Accept rating without further review

**Minor Discordance**:
- Adjacent ratings (✓ vs ⚠, or ⚠ vs ✗)
- Confidence: High
- Action: Apply resolution strategy

**Major Discordance**:
- Opposite ratings (✓ vs ✗)
- Confidence: Low
- Action: Flag for manual review and provide evidence from both

**Uncertain**:
- One or both appraisers unable to assess
- Confidence: Unable to determine
- Action: Mark as N/A with explanation

### Resolution Strategies

**Evidence-Weighted** (default):
- Select rating with stronger evidence support
- Compare evidence quality scores
- Prefer rating backed by explicit PDF citations

**Conservative**:
- Always select more conservative (worse) rating
- Use when quality standards must be strict
- Appropriate for high-stakes decisions

**Optimistic**:
- Select less conservative (better) rating
- Use when encouraging marginal compliance
- Appropriate for formative assessments

## Confidence Scoring

Each evidence match receives a confidence score:

```
High (≥0.75): Clear, unambiguous evidence found
Moderate (0.55-0.74): Evidence present but requires interpretation
Low (0.35-0.54): Weak or indirect evidence
Unable (<0.35): No relevant evidence located
```

## Quality Control

**Minimum Standards**:
- Overall agreement rate ≥ 65%
- No more than 10% major discordance
- Evidence confidence ≥ moderate for ≥50% of items

**Flags for Review**:
- Major discordance on critical items
- Low evidence confidence on key methodological items
- Systematic disagreement on specific sections
