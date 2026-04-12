# Integrated Workflow: How All 6 Frameworks Work Together

## Overview

This document explains how CONSORT 2025, RoB 2.0, GRADE, TIDieR, Benefits/Harms, and COI frameworks integrate into a comprehensive RCT appraisal system addressing distinct but complementary quality dimensions.

## Framework Integration Map

```
RCT Quality Dimensions:

1. REPORTING TRANSPARENCY → CONSORT 2025
   ↓
2. RISK OF BIAS → RoB 2.0
   ↓
3. EVIDENCE CERTAINTY → GRADE (incorporates RoB 2.0)
   ↓
4. INTERVENTION REPLICABILITY → TIDieR
   ↓
5. BENEFIT-HARM BALANCE → Benefits/Harms Assessment
   ↓
6. TRUSTWORTHINESS → COI Assessment

INTEGRATION: All frameworks feed into comprehensive quality judgment
```

## Sequential Application Logic

### Step 1: CONSORT 2025 → Reporting Assessment
**Purpose**: Establish whether trial is sufficiently reported to assess

**Key Question**: "Can I evaluate this trial's quality?"

**Critical CONSORT Items for Other Frameworks:**
- Item 3a (trial design) → Needed for RoB 2.0 Domain 1
- Items 8-10 (randomization) → Core of RoB 2.0 Domain 1
- Item 11 (blinding) → Core of RoB 2.0 Domains 2, 4
- Item 13 (participant flow) → Needed for RoB 2.0 Domain 3
- Item 5 (interventions) → Assessed in detail by TIDieR
- Item 19 (harms) → Assessed in detail by Benefits/Harms
- Item 25 (funding) → Core of COI assessment

**Decision Point**: If CONSORT compliance <60%, consider stopping - inadequate reporting prevents valid appraisal

### Step 2: RoB 2.0 → Bias Assessment
**Purpose**: Evaluate internal validity threats

**Key Question**: "Are the results believable?"

**RoB 2.0 Feeds into GRADE:**
- Domain 1 (Randomization) concerns → GRADE risk of bias downgrade
- Domain 2 (Deviations) concerns → GRADE risk of bias downgrade
- Domain 3 (Missing data) concerns → GRADE risk of bias + imprecision downgrade
- Domain 4 (Outcome measurement) concerns → GRADE risk of bias downgrade
- Domain 5 (Selective reporting) concerns → GRADE publication bias downgrade

**Mapping Example:**
```
RoB 2.0: Domain 4 = HIGH RISK (unblinded subjective outcome)
    ↓
GRADE: Downgrade -1 for risk of bias → Moderate certainty
```

### Step 3: GRADE → Certainty of Evidence
**Purpose**: Rate confidence in effect estimates

**Key Question**: "How confident are we in these results?"

**GRADE Integrates:**
- RoB 2.0 assessment → Risk of bias criterion
- Statistical precision → Imprecision criterion
- Applicability → Indirectness criterion
- Selective reporting (from RoB 2.0 Domain 5) → Publication bias criterion

**GRADE Outputs:**
- High / Moderate / Low / Very Low certainty
- Directly informs recommendation strength
- Critical for guideline development

### Step 4: TIDieR → Intervention Replicability
**Purpose**: Assess whether intervention can be replicated

**Key Question**: "Can clinicians/researchers implement this intervention?"

**TIDieR Complements CONSORT:**
- CONSORT Item 5 requires intervention description
- TIDieR provides 12-item detailed checklist for Item 5
- Poor TIDieR compliance prevents translation to practice

**Impact on Other Frameworks:**
- Poor TIDieR → Cannot assess what intervention actually was → Reduces confidence in GRADE
- Poor TIDieR → Cannot replicate → Limited clinical utility despite high GRADE

**Special Note**: Apply TIDieR to BOTH intervention AND control groups

### Step 5: Benefits/Harms → Risk-Benefit Balance
**Purpose**: Comprehensively evaluate efficacy AND safety

**Key Question**: "Do benefits outweigh harms for typical patient?"

**Benefits/Harms Integrates:**
- Efficacy (from CONSORT Items 17-18) → Benefits domain
- Harms (from CONSORT Item 19) → Harms domain
- Patient-important outcomes (feeds into GRADE indirectness)
- NNT vs NNH comparison

**Critical Integration:**
- CONSORT assesses IF harms are reported
- Benefits/Harms assesses HOW WELL harms are reported and interpreted
- GRADE considers harms in overall certainty rating

### Step 6: COI → Trustworthiness
**Purpose**: Assess potential for bias from financial/non-financial conflicts

**Key Question**: "Can we trust these results given who paid for and conducted the study?"

**COI Integrates Across Frameworks:**
- Funding transparency (from CONSORT Item 25)
- Selective outcome reporting (connects to RoB 2.0 Domain 5)
- Interpretation bias (affects GRADE confidence)
- Influence on benefit-harm framing

**COI Influences GRADE:**
```
High COI + Borderline positive results → Consider additional risk of bias downgrade
High COI + Negative results → Usually do NOT downgrade (no bias toward null)
```

## Cross-Framework Synergies

### Synergy 1: RoB 2.0 × GRADE
**Integration Point**: RoB 2.0 is PRIMARY input for GRADE risk of bias criterion

**Workflow:**
1. Complete RoB 2.0 assessment (5 domains)
2. Overall RoB 2.0 judgment (Low / Some concerns / High)
3. Translate to GRADE downgrade:
   - Low risk → No downgrade
   - Some concerns → Consider -1
   - High risk → Downgrade -1 or -2

**Example:**
```
RoB 2.0: HIGH RISK (Domain 4: unblinded subjective outcome)
GRADE: Start HIGH → Downgrade -1 for risk of bias → MODERATE
```

### Synergy 2: CONSORT × TIDieR
**Integration Point**: CONSORT Item 5 requires intervention description; TIDieR operationalizes

**Workflow:**
1. Check CONSORT Item 5 compliance (Is intervention described?)
2. Apply TIDieR checklist (HOW WELL is intervention described?)
3. TIDieR provides detailed rating (12 items vs CONSORT's single item)

**Common Finding**: CONSORT Item 5 rated ✓ but TIDieR shows only 5/12 items adequate

### Synergy 3: Benefits/Harms × GRADE
**Integration Point**: Harms assessment informs GRADE precision and risk of bias

**Workflow:**
1. Assess benefits (efficacy) → Feeds into GRADE effect size
2. Assess harms (safety) → Feeds into GRADE risk of bias (if AE reporting inadequate)
3. Calculate NNT and NNH → Feeds into GRADE clinical significance
4. Balance assessment → Informs GRADE indirectness (patient-important outcomes?)

**Example:**
```
Benefits: NNT = 20 for moderate benefit
Harms: NNH = 15 for serious harm
Balance: Unfavorable → GRADE confidence reduced
```

### Synergy 4: COI × RoB 2.0 Domain 5
**Integration Point**: Both assess selective reporting and trustworthiness

**Workflow:**
1. RoB 2.0 Domain 5: Assess outcome switching, selective analyses
2. COI Assessment: Assess who controlled data and had incentive to select favorable results
3. Integration: High COI + Some concerns in Domain 5 = Higher suspicion of bias

**Red Flag Combination:**
- Industry funding
- Sponsor-controlled data
- Outcomes differ from registration
→ HIGH RISK of selective reporting bias

### Synergy 5: All Frameworks → Comprehensive Quality Profile

**Integration**: No single framework captures all quality dimensions

| Framework | Dimension Assessed | Limitation |
|-----------|-------------------|------------|
| CONSORT | Reporting transparency | Does NOT assess validity |
| RoB 2.0 | Internal validity | Does NOT assess clinical significance |
| GRADE | Evidence certainty | Does NOT assess replicability |
| TIDieR | Intervention description | Does NOT assess efficacy/safety |
| Benefits/Harms | Risk-benefit balance | Does NOT assess bias |
| COI | Trustworthiness | Does NOT assess methods quality |

**Comprehensive Profile Requires ALL:**
```
Example Appraisal:
- CONSORT: 23/25 (92%) - Excellent reporting
- RoB 2.0: Some concerns (Domain 2) - Good but not perfect
- GRADE: Moderate certainty - Reasonable confidence
- TIDieR: 10/12 (83%) - Good replicability
- Benefits/Harms: Favorable balance (NNT=8, NNH=100)
- COI: Moderate impact (industry-funded but transparent)

INTEGRATED JUDGMENT: High-quality trial with favorable risk-benefit;
recommend with caveat about open-label design
```

## Framework Selection by Appraisal Purpose

### For Peer Review (Comprehensive)
**Use**: All 6 frameworks
**Rationale**: Complete quality assessment
**Time**: 3-4 hours

### For Systematic Review Inclusion (Bias Focus)
**Use**: RoB 2.0 + GRADE + CONSORT (selective items)
**Rationale**: Assess validity and certainty for synthesis
**Time**: 1-2 hours

### For Guideline Development (Evidence Rating)
**Use**: RoB 2.0 + GRADE + Benefits/Harms
**Rationale**: Rate evidence certainty and inform recommendations
**Time**: 2-3 hours

### For Clinical Decision-Making (Applicability)
**Use**: Benefits/Harms + TIDieR + GRADE
**Rationale**: Assess whether to use intervention in practice
**Time**: 1-2 hours

### For Editorial Writing (Critical Analysis)
**Use**: RoB 2.0 + Benefits/Harms + COI
**Rationale**: Identify biases, balance, and trustworthiness issues
**Time**: 2-3 hours

## Reporting Integrated Appraisal

### Executive Summary Format
```
STUDY: [Citation]
APPRAISAL DATE: [Date]
FRAMEWORKS APPLIED: [List]

REPORTING QUALITY (CONSORT): [Score] - [Excellent/Good/Adequate/Poor]
RISK OF BIAS (RoB 2.0): [Low/Some concerns/High] - [Domain specifics]
EVIDENCE CERTAINTY (GRADE): [High/Moderate/Low/Very Low] - [Rationale]
INTERVENTION REPLICABILITY (TIDieR): [Score] - [Complete/Adequate/Incomplete]
BENEFIT-HARM BALANCE: [Favorable/Uncertain/Unfavorable] - [NNT vs NNH]
CONFLICTS OF INTEREST: [Low/Moderate/High impact] - [Key issues]

OVERALL ASSESSMENT: [2-3 sentence synthesis]
RECOMMENDATION: [For/Against/Conditional/More research needed]
```

### Traffic Light Summary
```
Framework           Green (✓)  Yellow (⚠)  Red (✗)
-------------------------------------------------
CONSORT 2025        23         2          0
RoB 2.0 Domain 1    ✓
RoB 2.0 Domain 2               ⚠
RoB 2.0 Domain 3    ✓
RoB 2.0 Domain 4               ⚠
RoB 2.0 Domain 5    ✓
GRADE                          Moderate
TIDieR              10         2          0
Benefits            ✓
Harms                          ⚠
Balance             ✓
COI                            Moderate
-------------------------------------------------
OVERALL                        Acceptable with caveats
```

## Common Integration Challenges

### Challenge 1: Discordant Findings
**Example**: High CONSORT compliance but High RoB 2.0 risk
**Resolution**: Good reporting does not ensure good methods. Trust RoB 2.0 for validity.

### Challenge 2: GRADE Uncertainty
**Example**: Low RoB 2.0 risk but GRADE downgraded for imprecision
**Resolution**: Low bias ≠ high certainty. Precision matters independently.

### Challenge 3: TIDieR vs GRADE Priority
**Example**: Poor TIDieR but High GRADE certainty
**Resolution**: High certainty in RESULTS, but low certainty in replicability. Both matter.

### Challenge 4: COI Interpretation
**Example**: High COI but seemingly rigorous methods
**Resolution**: Acknowledge COI impact on trust without dismissing methods. Call for replication.

### Challenge 5: Benefit-Harm Inconsistency
**Example**: Statistically significant benefit but unfavorable NNT/NNH ratio
**Resolution**: Statistical significance ≠ clinical significance. Balance matters more than p-value.

## References

1. Page MJ, Higgins JPT, Sterne JAC. Chapter 8: Assessing risk of bias in a randomized trial. *Cochrane Handbook for Systematic Reviews of Interventions* version 6.3, 2022.

2. Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. *BMJ* 2008;336:924-6.

3. Hoffmann TC, Glasziou PP, Boutron I, et al. Better reporting of interventions: template for intervention description and replication (TIDieR) checklist and guide. *BMJ* 2014;348:g1687.

4. Ioannidis JP, Evans SJ, Gøtzsche PC, et al. Better reporting of harms in randomized trials: an extension of the CONSORT statement. *Ann Intern Med* 2004;141(10):781-8.
