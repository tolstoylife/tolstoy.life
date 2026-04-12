# GRADE Framework for RCT Evidence Certainty Assessment

## Overview

GRADE (Grading of Recommendations, Assessment, Development and Evaluations) provides a systematic approach to rating confidence in effect estimates. For RCTs, evidence starts at HIGH certainty and can be downgraded or (rarely) upgraded based on specific criteria.

**Purpose**: Rate confidence in effect estimates from RCTs
**Starting Level**: HIGH (randomized trials)
**Criteria**: 5 downgrading + 3 upgrading factors
**Final Ratings**: High / Moderate / Low / Very Low

## GRADE Certainty Levels

### High Certainty (⊕⊕⊕⊕)
**Definition**: Very confident that the true effect lies close to the estimate of effect

**Interpretation**: Further research is very unlikely to change our confidence in the estimate of effect

**Use in decision-making**: Strong recommendation possible

### Moderate Certainty (⊕⊕⊕⊙)
**Definition**: Moderately confident in the effect estimate; true effect is likely close to estimate but possibility it is substantially different

**Interpretation**: Further research is likely to have an important impact on confidence in estimate and may change the estimate

**Use in decision-making**: Conditional recommendation typical

### Low Certainty (⊕⊕⊙⊙)
**Definition**: Limited confidence in effect estimate; true effect may be substantially different from estimate

**Interpretation**: Further research is very likely to have important impact on confidence in estimate and likely to change the estimate

**Use in decision-making**: Conditional recommendation or no recommendation

### Very Low Certainty (⊕⊙⊙⊙)
**Definition**: Very little confidence in effect estimate; true effect is likely substantially different from estimate

**Interpretation**: Any estimate of effect is very uncertain

**Use in decision-making**: No recommendation or recommendation only in research context

## Starting Point for RCTs

**Randomized Controlled Trials**: Start at HIGH certainty (⊕⊕⊕⊕)

**Rationale**: Randomization minimizes confounding and selection bias, making RCTs the most reliable study design for treatment effects

**Exception**: Poorly designed or executed RCTs may start lower if fundamental flaws present

## Downgrading Criteria

Apply each criterion sequentially. Each can reduce certainty by 1 or 2 levels.

### 1. Risk of Bias

**Definition**: Limitations in study design or execution that may bias results

**Assessment**: Based on RoB 2.0 domains (randomization, deviations, missing data, outcome measurement, selective reporting)

#### Downgrade by 1 level (-1) if:
- **Serious risk of bias** in one or more RoB 2.0 domains
- Some concerns in multiple domains
- HIGH risk in non-critical domains only

**Evidence examples:**
- Lack of allocation concealment
- Unblinded assessment of subjective outcomes
- High dropout rate (>20%) without sensitivity analysis
- Some outcome switching detected

#### Downgrade by 2 levels (-2) if:
- **Very serious risk of bias** across multiple domains
- HIGH risk in critical domains (randomization, selective reporting)
- Fatal flaws that severely compromise validity

**Evidence examples:**
- No allocation concealment + baseline imbalances
- High dropout (>40%) with differential attrition
- Clear selective outcome reporting
- Unblinded assessment of highly subjective outcomes + other serious concerns

#### Do NOT downgrade if:
- LOW risk of bias in all RoB 2.0 domains
- Minor concerns unlikely to affect results
- Sensitivity analyses show results robust to concerns

### 2. Inconsistency

**Definition**: Unexplained heterogeneity or variability in results

**Note**: For single RCT appraisal, assess internal consistency of results (subgroups, sensitivity analyses)

#### Downgrade by 1 level (-1) if:
- **Serious inconsistency** in subgroup results without clear explanation
- Sensitivity analyses show substantially different results
- Internal contradictions in findings

**Evidence examples:**
- Large differences in effect size between subgroups without interaction test
- Per-protocol vs ITT analyses show opposite effects
- Different outcomes tell conflicting story

#### Downgrade by 2 levels (-2) if:
- **Very serious inconsistency** with fundamental uncertainty about true effect
- Multiple analyses show contradictory results
- Effect varies widely across populations/outcomes

#### Do NOT downgrade if:
- Single primary analysis with consistent findings
- Subgroup differences are pre-specified and plausible
- Sensitivity analyses confirm main findings

**Note**: Inconsistency is more relevant when assessing multiple RCTs in meta-analysis

### 3. Indirectness

**Definition**: Evidence differs from the research question in PICO (Population, Intervention, Comparison, Outcome)

#### Downgrade by 1 level (-1) if:
- **Serious indirectness** in one or more PICO elements

**Evidence examples:**

**Population indirectness:**
- Trial enrolled younger/healthier patients than typical practice population
- Narrow inclusion criteria limit applicability
- Single ethnicity/region when broader application intended

**Intervention indirectness:**
- Different dose, duration, or formulation than clinical interest
- Intervention bundled with other components
- Delivery by research specialists vs routine practice

**Comparator indirectness:**
- Placebo comparison when active comparator more relevant
- Suboptimal comparator dose
- Comparison to outdated standard of care

**Outcome indirectness:**
- Surrogate outcome instead of patient-important outcome
- Short-term outcome when long-term effect is question
- Composite outcome mixing important and unimportant components

#### Downgrade by 2 levels (-2) if:
- **Very serious indirectness** in multiple PICO elements
- Substantial uncertainty about applicability to question of interest

**Evidence examples:**
- Animal models for human question
- Healthy volunteers for disease population
- Surrogate outcome with uncertain relationship to clinical outcome

#### Do NOT downgrade if:
- Trial population, intervention, comparator, outcome directly address question
- Any differences are minor and unlikely to affect applicability

### 4. Imprecision

**Definition**: Wide confidence intervals or small sample size leading to uncertainty about effect

#### Downgrade by 1 level (-1) if:
- **Serious imprecision** with confidence interval including both benefit and harm
- Optimal information size (OIS) not met
- Small sample size with wide confidence intervals

**Evidence examples:**
- 95% CI crosses 1.0 (no effect) for ratio measures
- 95% CI crosses 0 for difference measures
- 95% CI includes both clinically important benefit and clinically important harm
- Total events <300 (for dichotomous outcomes)
- Total participants <400 (for continuous outcomes)

**Calculation example:**
- RR = 0.75 (95% CI 0.50 to 1.12)
- CI crosses 1.0 → Imprecision present
- CI includes both meaningful benefit (0.50) and potential harm (1.12) → Downgrade by 1

#### Downgrade by 2 levels (-2) if:
- **Very serious imprecision** with very wide confidence intervals
- Very small sample size
- Very few events

**Evidence examples:**
- 95% CI spans from large benefit to large harm
- Total events <100
- Total participants <100
- Confidence interval so wide that it provides no useful information

#### Do NOT downgrade if:
- Confidence interval narrow and excludes clinically unimportant effects
- Adequate sample size achieved
- Optimal information size reached

**Optimal Information Size (OIS) Rules:**
- OIS NOT met if trial has <70% of participants from adequate sample size calculation
- OIS met if CI excludes minimal clinically important difference (MCID)

### 5. Publication Bias

**Definition**: Selective publication of trials or outcomes based on findings

**Note**: Difficult to assess for single RCT; more relevant for meta-analysis

#### Downgrade by 1 level (-1) if:
- **Serious concern** for selective outcome reporting within trial
- Trial not registered or registered retrospectively
- Published outcomes differ from registered outcomes
- Negative results downplayed or buried in results

**Evidence examples:**
- No trial registration found
- Trial registered after enrollment started
- Registered primary outcome not reported or changed
- Positive secondary outcomes emphasized over negative primary outcome
- Selective reporting of favorable subgroups

#### Do NOT downgrade if:
- Trial pre-registered with analysis plan
- All registered outcomes reported
- No evidence of selective reporting

**For meta-analysis context** (not single RCT):
- Asymmetric funnel plot
- Small study effects detected
- Industry sponsorship with positive results (known association with publication bias)

## Upgrading Criteria (Rare for Single RCT)

Upgrading is RARE for single RCTs and typically only considered when observational studies are primary evidence. However, may apply in exceptional circumstances.

### 1. Large Magnitude of Effect

**Upgrade by 1 level (+1) if:**
- **Large effect** with RR >2 or <0.5 in absence of plausible confounders

**Evidence examples:**
- RR = 5.0 (95% CI 3.2 to 7.8)
- NNT = 3 with narrow confidence interval
- Effect size d >0.8 with clinical significance

**Upgrade by 2 levels (+2) if:**
- **Very large effect** with RR >5 or <0.2

**Evidence examples:**
- RR = 10 (95% CI 6 to 16)
- NNT = 2 with life-saving or disability-preventing outcome

**Do NOT upgrade if:**
- Effect estimates are imprecise (wide CI)
- Risk of bias is substantial
- Surrogate outcome rather than patient-important outcome

### 2. Dose-Response Gradient

**Upgrade by 1 level (+1) if:**
- Evidence of dose-response relationship strengthens confidence in causality

**Evidence examples:**
- Higher dose shows greater effect
- Longer duration shows greater effect
- Trend analysis shows clear gradient
- Dose-response observed within RCT through dose-ranging design

**Do NOT upgrade if:**
- Dose-response data are weak or inconsistent
- Confounding could explain gradient
- Small sample sizes at different doses

### 3. Plausible Residual Confounding

**Upgrade by 1 level (+1) if:**
- Plausible confounders would reduce observed effect (strengthening inference)

**Note**: Almost never applies to RCTs since randomization controls confounding

**Possible example:**
- RCT shows benefit despite factors biasing toward null
- Selection of high-risk patients would bias toward null but benefit still seen

**Do NOT upgrade:**
- Standard practice for RCTs - randomization already controls confounding

## GRADE Assessment Process

### Step-by-Step Approach

**Step 1**: Start at HIGH certainty (⊕⊕⊕⊕) for RCT evidence

**Step 2**: Apply downgrading criteria sequentially:
1. Risk of bias (from RoB 2.0 assessment)
2. Inconsistency (if multiple analyses/subgroups)
3. Indirectness (compare PICO to clinical question)
4. Imprecision (assess CI width and sample size)
5. Publication bias (check registration, outcome switching)

**Step 3**: Consider upgrading criteria (rare for single RCT):
1. Large magnitude of effect
2. Dose-response gradient
3. Plausible residual confounding reducing effect

**Step 4**: Calculate final certainty level:
- Start: HIGH (⊕⊕⊕⊕ = 4 points)
- Subtract downgrading points (-1 or -2 per criterion)
- Add upgrading points (+1 or +2 per criterion)
- Final score: 4 = High, 3 = Moderate, 2 = Low, 1 = Very Low

**Step 5**: Document rationale:
- Specify which criteria applied
- Provide evidence for each decision
- Explain magnitude of downgrading/upgrading

### Example Assessment

**RCT**: Novel antihypertensive vs placebo for blood pressure reduction

**Starting level**: HIGH (⊕⊕⊕⊕)

**Downgrading:**
1. Risk of bias: -1 (unblinded outcome assessment of subjective symptoms)
2. Inconsistency: 0 (consistent findings across analyses)
3. Indirectness: -1 (short-term BP surrogate, not CV events)
4. Imprecision: 0 (narrow CI, adequate sample size)
5. Publication bias: 0 (pre-registered, all outcomes reported)

**Upgrading:**
- None applicable

**Final certainty**: 4 - 2 = 2 = **LOW** (⊕⊕⊙⊙)

**Rationale**: "We downgraded by one level for risk of bias due to unblinded assessment of subjective symptom outcomes, and by one level for indirectness because the trial measured blood pressure as a surrogate rather than patient-important cardiovascular outcomes."

## GRADE Summary of Findings Table

Present GRADE assessment in structured format:

| Outcome | Effect Estimate (95% CI) | № Participants (studies) | Certainty | Comments |
|---------|-------------------------|------------------------|-----------|-----------|
| Mortality at 1 year | RR 0.75 (0.62 to 0.91) | 500 (1 RCT) | ⊕⊕⊕⊙ MODERATE | Downgraded for imprecision |
| Quality of life | MD 12 points higher (6 to 18) | 500 (1 RCT) | ⊕⊕⊙⊙ LOW | Downgraded for risk of bias and indirectness |

## Common Pitfalls

1. **Over-reliance on p-values**: GRADE focuses on effect size and confidence intervals, not p-values
2. **Automatic downgrading**: Not every RCT limitation warrants downgrading - assess impact
3. **Ignoring indirectness**: Surrogate outcomes are indirect even in well-conducted RCTs
4. **Double-counting**: Don't downgrade for same issue in multiple categories
5. **Upgrading RCTs**: Rarely appropriate - high starting point makes upgrading uncommon
6. **Imprecision misjudgment**: Don't conflate non-significance with imprecision

## References

1. Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. *BMJ* 2008;336:924-6.

2. Guyatt GH, Oxman AD, Kunz R, et al. GRADE guidelines: 1. Introduction—GRADE evidence profiles and summary of findings tables. *J Clin Epidemiol* 2011;64:383-94.

3. Guyatt GH, Oxman AD, Vist G, et al. GRADE guidelines: 4. Rating the quality of evidence—study limitations (risk of bias). *J Clin Epidemiol* 2011;64:407-15.

4. Guyatt GH, Oxman AD, Kunz R, et al. GRADE guidelines: 8. Rating the quality of evidence—indirectness. *J Clin Epidemiol* 2011;64:1303-10.

5. Guyatt GH, Oxman AD, Kunz R, et al. GRADE guidelines: 6. Rating the quality of evidence—imprecision. *J Clin Epidemiol* 2011;64:1283-93.

6. GRADE Handbook: https://gdt.gradepro.org/app/handbook/handbook.html
