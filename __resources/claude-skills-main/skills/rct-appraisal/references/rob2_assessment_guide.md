# Cochrane Risk of Bias 2.0 (RoB 2) Assessment Guide

## Overview

The Cochrane Risk of Bias tool (RoB 2.0) is the current standard for assessing bias in randomized controlled trials. It uses a domain-based evaluation structure with signaling questions that lead to risk of bias judgments.

**Purpose**: Systematic assessment of internal validity threats
**Domains**: 5 bias domains with ~30 signaling questions
**Judgments**: Low risk / Some concerns / High risk
**Scope**: Individual outcomes in individual trials

## RoB 2.0 Structure

### Assessment Levels

**Low risk of bias**: Trial appears free of bias in this domain
**Some concerns**: Potential for bias exists but insufficient evidence to determine high risk
**High risk**: Substantial risk of bias that seriously weakens confidence in results

### Domain-Based Assessment

Each domain includes:
1. Signaling questions (answered Yes/Probably yes/Probably no/No/No information)
2. Risk of bias judgment for the domain
3. Support for judgment with evidence from trial report

## Domain 1: Bias Arising from the Randomization Process

### Purpose
Assess whether allocation sequence was random and whether allocation concealment prevented prediction of assignment.

### Signaling Questions

**1.1** Was the allocation sequence random?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Computer-generated sequence, random number table, coin toss |
| Probably yes | States "randomized" with reputable methodology description |
| Probably no | Unclear method or quasi-random (alternation, date of birth) |
| No | Non-random assignment (physician choice, patient preference) |
| No information | States "randomized" without method description |

**1.2** Was the allocation sequence concealed until participants were enrolled and assigned to interventions?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Central randomization, sequentially numbered sealed opaque envelopes, pharmacy-controlled |
| Probably yes | States "allocation concealment" with reasonable method |
| Probably no | Unclear concealment or unsealed envelopes |
| No | Open random allocation schedule, unsealed/transparent envelopes |
| No information | No mention of concealment method |

**1.3** Did baseline differences between intervention groups suggest a problem with the randomization process?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Substantial baseline imbalances in prognostic factors suggesting selection bias |
| Probably yes | Some imbalances that are unlikely due to chance |
| Probably no | Minor imbalances consistent with chance |
| No | No important baseline differences or differences consistent with chance |
| No information | Baseline characteristics not reported |

### Risk of Bias Judgment for Domain 1

**Low risk**: All of:
- Random sequence generation (1.1 = Yes/Probably yes)
- Allocation concealment (1.2 = Yes/Probably yes)
- No baseline imbalances suggesting selection bias (1.3 = No/Probably no)

**Some concerns**: Any of:
- 1.1 = No information
- 1.2 = No information
- 1.3 = No information/Probably yes

**High risk**: Any of:
- 1.1 = No/Probably no (non-random sequence)
- 1.2 = No/Probably no (no concealment)
- 1.3 = Yes (baseline imbalances suggesting selection bias)

### Common Issues
- Authors state "randomized" without describing method (→ Some concerns)
- Alternation or date-based assignment is NOT random (→ High risk)
- Baseline imbalances in small trials may be due to chance (careful assessment needed)

## Domain 2: Bias Due to Deviations from Intended Interventions

### Purpose
Assess whether implementation deviations arose because of the trial context and whether analysis was appropriate to estimate the effect of assignment to intervention.

### Effect of Interest Selection

Choose ONE:
- **Effect of assignment to intervention (intention-to-treat effect)**: Effect of being assigned to intervention, regardless of adherence
- **Effect of adhering to intervention (per-protocol effect)**: Effect of receiving intervention as planned

*Most RCT appraisals assess intention-to-treat effect.*

### Signaling Questions (Intention-to-Treat Effect)

**2.1** Were participants aware of their assigned intervention during the trial?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Open-label, unblinded, or participants could identify intervention |
| Probably yes | Blinding described but likely broken |
| Probably no | Blinding described with reasonable methods |
| No | Double-blind with identical placebo/sham |
| No information | Blinding status not described |

**2.2** Were carers and people delivering the interventions aware of participants' assigned intervention during the trial?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Open-label or intervention obvious to providers |
| Probably yes | Blinding described but likely broken |
| Probably no | Blinding of providers described |
| No | Double-blind with provider blinding confirmed |
| No information | Blinding status not described |

**2.3** If Y/PY/NI to 2.1 or 2.2: Were there deviations from the intended intervention that arose because of the trial context?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Protocol violations, crossovers, co-interventions due to knowledge of assignment |
| Probably yes | Some deviations likely influenced by unblinding |
| Probably no | Deviations reported but unlikely related to trial context |
| No | No deviations or deviations unrelated to trial context |
| No information | Adherence not reported |

**2.4** If Y/PY to 2.3: Were these deviations likely to have affected the outcome?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Substantial crossover, differential co-interventions, selective withdrawal |
| Probably yes | Deviations plausibly affected outcomes |
| Probably no | Minor deviations unlikely to affect outcomes |
| No | Deviations clearly would not affect outcomes |
| No information | Impact cannot be determined |

**2.5** If Y/PY/NI to 2.4: Were these deviations from intended intervention balanced between groups?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Similar rates of deviations in both groups |
| Probably yes | Deviations appear balanced |
| Probably no | Unbalanced deviations (more in one group) |
| No | Clearly unbalanced deviations |
| No information | Cannot determine balance |

**2.6** Was an appropriate analysis used to estimate the effect of assignment to intervention?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Intention-to-treat analysis clearly stated and implemented |
| Probably yes | States ITT but some exclusions justified |
| Probably no | Modified ITT or per-protocol without justification |
| No | Per-protocol analysis without ITT sensitivity analysis |
| No information | Analysis approach not clearly described |

**2.7** If N/PN/NI to 2.6: Was there potential for a substantial impact (on the result) of the failure to analyse participants in the group to which they were randomized?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Many participants excluded from analysis, likely differential by group |
| Probably yes | Some excluded participants, potential for bias |
| Probably no | Few exclusions, unlikely to affect results |
| No | No exclusions or exclusions clearly would not affect results |
| No information | Cannot determine impact |

### Risk of Bias Judgment for Domain 2 (Intention-to-Treat Effect)

**Low risk**: All of:
- No/probably no deviations (2.3)
- OR deviations present but would not affect outcome (2.4 = No/Probably no)
- ITT analysis used (2.6 = Yes/Probably yes)

**Some concerns**: Any of:
- 2.3 = No information
- 2.4 = No information
- 2.5 = No information
- 2.6 = Probably yes with minor issues

**High risk**: Any of:
- Deviations likely affected outcome + unbalanced (2.4 = Yes/Probably yes AND 2.5 = No/Probably no)
- Inappropriate analysis with substantial impact (2.6 = No/Probably no AND 2.7 = Yes/Probably yes)

### Common Issues
- Many trials use "modified ITT" - assess what was modified and why
- Unblinded behavioral interventions often have context-driven deviations
- Per-protocol analyses are appropriate for some questions but should be pre-specified

## Domain 3: Bias Due to Missing Outcome Data

### Purpose
Assess whether missing data could have substantially affected observed effect estimate.

### Signaling Questions

**3.1** Were data for this outcome available for all, or nearly all, participants randomized?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | >95% outcome data available |
| Probably yes | 90-95% outcome data available |
| Probably no | 80-89% outcome data available |
| No | <80% outcome data available |
| No information | Outcome data completeness not reported |

**3.2** If N/PN/NI to 3.1: Is there evidence that the result was not biased by missing outcome data?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Sensitivity analyses show results robust to missing data |
| Probably yes | Missingness balanced and unlikely to bias results |
| Probably no | Missingness unbalanced or reasons suggest bias |
| No | Clear evidence of bias from missing data |
| No information | Cannot assess impact of missingness |

**3.3** If N/PN to 3.2: Could missingness in the outcome depend on its true value?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Differential missingness by group with reasons related to outcomes (e.g., adverse events) |
| Probably yes | Missingness patterns suggest outcome-related dropout |
| Probably no | Missingness appears unrelated to outcomes |
| No | Reasons for missingness clearly unrelated to outcome |
| No information | Reasons for missingness not reported |

**3.4** If Y/PY/NI to 3.3: Is it likely that missingness in the outcome depended on its true value?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Strong evidence of outcome-related missingness (e.g., "withdrew due to lack of efficacy") |
| Probably yes | Missingness plausibly related to outcomes |
| Probably no | Missingness unlikely related to outcomes despite uncertainty |
| No | Missingness clearly not related to outcomes |
| No information | Cannot determine |

### Risk of Bias Judgment for Domain 3

**Low risk**: Either:
- Outcome data available for nearly all participants (3.1 = Yes/Probably yes)
- OR evidence that result not biased by missing data (3.2 = Yes/Probably yes)

**Some concerns**: Any of:
- 3.1 = Probably no AND 3.2 = No information
- 3.3 = No information
- 3.4 = No information

**High risk**: Any of:
- Substantial missing data + likely biased (3.1 = No AND 3.2 = No/Probably no)
- Missingness likely depends on true outcome value (3.4 = Yes/Probably yes)

### Common Issues
- Last observation carried forward (LOCF) is NOT appropriate handling of missing data
- "Completer analysis" excludes those with missing data - assess reasons
- Differential dropout between groups is RED FLAG
- Reasons for missingness are critical: "lost to follow-up" ≠ "withdrew due to adverse event"

## Domain 4: Bias in Measurement of the Outcome

### Purpose
Assess whether outcome measurement was influenced by knowledge of intervention assignment.

### Signaling Questions

**4.1** Was the method of measuring the outcome inappropriate?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Measurement method fundamentally flawed |
| Probably yes | Method has known biases |
| Probably no | Standard validated method used |
| No | Gold standard objective measurement |
| No information | Measurement method not described |

**4.2** Could measurement or ascertainment of the outcome have differed between intervention groups?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Different measurement methods or timing by group |
| Probably yes | Potential for differential measurement |
| Probably no | Same methods and timing for all groups |
| No | Clearly identical measurement procedures |
| No information | Measurement procedures not fully described |

**4.3** Were outcome assessors aware of the intervention received by study participants?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Open-label or assessors explicitly unblinded |
| Probably yes | Blinding likely broken during assessment |
| Probably no | Blinding of assessors described |
| No | Double-blind with assessor blinding confirmed |
| No information | Assessor blinding status not reported |

**4.4** If Y/PY/NI to 4.3: Could assessment of the outcome have been influenced by knowledge of intervention received?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Subjective outcome + unblinded assessor (e.g., pain, quality of life) |
| Probably yes | Potential for bias in assessment |
| Probably no | Objective outcome or minimal subjectivity |
| No | Outcome measurement cannot be influenced (e.g., mortality, biomarker) |
| No information | Cannot assess objectivity of outcome |

**4.5** If Y/PY/NI to 4.4: Is it likely that assessment of the outcome was influenced by knowledge of intervention received?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Clear potential and motivation for biased assessment |
| Probably yes | Likely some influence of unblinding |
| Probably no | Influence unlikely despite unblinding |
| No | No influence possible |
| No information | Cannot determine |

### Risk of Bias Judgment for Domain 4

**Low risk**: All of:
- Appropriate measurement method (4.1 = No/Probably no)
- No differential measurement (4.2 = No/Probably no)
- Assessors blinded OR outcome not influenced by knowledge (4.3 = No/Probably no OR 4.4 = No/Probably no)

**Some concerns**: Any of:
- 4.1 = No information
- 4.3 = No information
- 4.4 = No information
- 4.5 = No information

**High risk**: Any of:
- Inappropriate measurement method (4.1 = Yes/Probably yes)
- Unblinded assessment of subjective outcome (4.3 = Yes/Probably yes AND 4.4 = Yes/Probably yes)
- Assessment likely influenced by knowledge (4.5 = Yes/Probably yes)

### Common Issues
- Objective outcomes (mortality, lab values) are robust to lack of blinding
- Subjective outcomes (pain, function, quality of life) REQUIRE blinded assessment
- Patient-reported outcomes in unblinded trials are HIGH RISK
- Adjudication committees can mitigate bias if blinded

## Domain 5: Bias in Selection of the Reported Result

### Purpose
Assess whether result was selected from multiple measurements or analyses based on findings.

### Signaling Questions

**5.1** Were the data that produced this result analysed in accordance with a pre-specified analysis plan that was finalized before unblinded outcome data were available for analysis?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Published protocol or registration with detailed analysis plan + adherence confirmed |
| Probably yes | Protocol exists and appears followed |
| Probably no | Protocol exists but deviations noted |
| No | No protocol or substantial undeclared deviations |
| No information | No protocol or registration accessible |

**5.2** Is the numerical result being assessed likely to have been selected, on the basis of the results, from multiple eligible outcome measurements within the outcome domain?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Different scale/time point reported than registered |
| Probably yes | Multiple measurements available, selective reporting likely |
| Probably no | Single measurement reported, aligns with protocol |
| No | Clearly pre-specified single measurement |
| No information | Cannot determine if selection occurred |

**5.3** Is the numerical result being assessed likely to have been selected, on the basis of the results, from multiple eligible analyses of the data?

| Answer | Evidence Examples |
|--------|------------------|
| Yes | Different analysis method than registered (e.g., unadjusted vs adjusted) |
| Probably yes | Multiple analysis options, selective reporting likely |
| Probably no | Single analysis consistent with protocol |
| No | Clearly pre-specified analysis |
| No information | Cannot determine if selection occurred |

### Risk of Bias Judgment for Domain 5

**Low risk**: All of:
- Pre-specified analysis plan finalized before data access (5.1 = Yes/Probably yes)
- No selection of measurement (5.2 = No/Probably no)
- No selection of analysis (5.3 = No/Probably no)

**Some concerns**: Any of:
- 5.1 = No information
- 5.2 = No information
- 5.3 = No information

**High risk**: Any of:
- No pre-specified plan (5.1 = No)
- Selective reporting of measurements (5.2 = Yes/Probably yes)
- Selective reporting of analyses (5.3 = Yes/Probably yes)

### Common Issues
- Trial registration is REQUIRED but insufficient - analysis plan details often missing
- "We registered primary outcome" does not prevent selective reporting of analyses
- Post-hoc subgroup analyses are hypothesis-generating, not confirmatory
- Switching from non-significant to significant outcome is HIGH RISK

## Overall Risk of Bias

### Overall Judgment Algorithm

**Low risk of bias**: Low risk in ALL domains

**Some concerns**: Some concerns in AT LEAST ONE domain (but no high risk)

**High risk of bias**: High risk in AT LEAST ONE domain OR some concerns in MULTIPLE domains

### Critical Appraisal Summary

Document overall risk of bias with:
1. Domain-specific judgments (use traffic light plot: green/yellow/red)
2. Evidence supporting each judgment
3. Overall risk of bias judgment
4. Impact on confidence in results

### Presentation Format

```
Domain 1 (Randomization): LOW RISK
- Computer-generated sequence with central allocation
- No baseline imbalances

Domain 2 (Deviations): SOME CONCERNS
- Open-label design with knowledge of assignment
- ITT analysis used but potential for context-driven deviations

Domain 3 (Missing data): LOW RISK
- 98% outcome data completeness
- Minimal missing data unlikely to bias results

Domain 4 (Outcome measurement): HIGH RISK
- Patient-reported outcome in unblinded trial
- Subjective outcome susceptible to knowledge of assignment

Domain 5 (Selective reporting): SOME CONCERNS
- Trial registered but analysis plan not detailed
- Cannot verify pre-specification of analyses

OVERALL: HIGH RISK (due to Domain 4)
```

## References

1. Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. *BMJ* 2019;366:l4898.

2. Cochrane Handbook for Systematic Reviews of Interventions, Version 6.3. Chapter 8: Assessing risk of bias in a randomized trial. Available at: https://training.cochrane.org/handbook

3. RoB 2.0 detailed guidance and Excel tool: https://www.riskofbias.info/welcome/rob-2-0-tool
