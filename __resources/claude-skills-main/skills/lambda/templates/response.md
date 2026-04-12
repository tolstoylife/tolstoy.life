# Response Templates

Output patterns by routing level.

## R0: Direct

```
[Direct answer in 1-2 sentences, ≤50 tokens]
```

**Example:**
> MAC (minimum alveolar concentration) is the alveolar concentration of an inhaled anaesthetic at 1 atm that prevents movement in 50% of subjects in response to a surgical stimulus.

## R1: Single Paragraph

```
[Topic sentence answering the question]

[2-3 supporting sentences with mechanism or context]

[Concluding sentence with clinical relevance or implication]
```

**Example:**
> Propofol produces hypotension primarily through reduction of systemic vascular resistance. The drug inhibits sympathetic nervous system activity and directly relaxes vascular smooth muscle, leading to venodilation and arterial vasodilation. Cardiac output is usually maintained or only slightly reduced in healthy patients, making the blood pressure drop predominantly a vascular phenomenon. This effect is dose-dependent and more pronounced in hypovolaemic or elderly patients.

## R2: Mechanistic

```
[TELEOLOGY: 1-2 sentences on why this matters]

[MECHANISM: Explicit causal chain]
A → B → C → D → clinical effect

[TRANSLATION: What this means practically]

[CONFIDENCE: ~X% based on Y; limitation: Z]
```

**Example:**
> Understanding propofol's cardiovascular effects is essential for safe induction, particularly in patients with limited reserve.

> Propofol → GABA-A receptor potentiation → reduced central sympathetic outflow → decreased noradrenaline release → arterial and venous smooth muscle relaxation → ↓SVR (primary) + ↓venous return → ↓MAP. Simultaneously, propofol → direct myocardial depression → ↓contractility (usually mild). The combined effect: SVR reduction dominates, with HR typically unchanged or reflexly increased.

> Clinically, this manifests as 15-40% MAP reduction post-induction. Mitigation: slow injection, co-induction with opioid or midazolam, adequate preload, vasopressor availability.

> ~85% confidence based on extensive clinical data; limitation: individual variability in autonomic response.

## R3: Comprehensive

```
## Purpose
[Why this matters - 2-3 sentences contextualizing the question]

## Mechanism

### Strategic (Why)
[High-level physiological/pharmacological rationale]

### Tactical (How)
[Specific pathways and processes]

### Operational (What)
[Molecular/cellular details]

## Evidence
[Key studies, guidelines, consensus - with citations if available]

## Application
[Clinical implications, practical considerations]

## Limitations
[Uncertainties, gaps, contraindications to this reasoning]

---
Confidence: ~X% | Validated: [η=Y.Z, KROG: ✓]
```

**Example skeleton for "Compare sevoflurane and desflurane in aortic stenosis":**

```
## Purpose
Choosing between volatile agents in aortic stenosis requires understanding their differential effects on SVR, contractility, and heart rate in a circulation dependent on maintaining afterload and avoiding tachycardia.

## Mechanism

### Strategic
AS patients require: stable HR (adequate diastolic filling), maintained SVR (coronary perfusion pressure), preserved contractility. Both volatiles depress these parameters—the question is magnitude and controllability.

### Tactical
Sevoflurane: gradual onset, minimal airway irritation, moderate SVR reduction, slight HR increase.
Desflurane: rapid equilibration but dose-dependent sympathetic activation → tachycardia + hypertension at >1 MAC, then hypotension. The sympathetic surge is the critical hazard.

### Operational
[Molecular mechanisms of myocardial depression, vascular effects, MAC-awake curves]

## Evidence
[Guidelines, studies comparing agents in cardiac surgery]

## Application
Sevoflurane preferred: smoother haemodynamics, lower sympathetic activation. Desflurane: acceptable if titrated carefully, avoid rapid increases. Both require invasive monitoring.

## Limitations
Individual response varies; evidence largely from non-AS populations; newer agents not considered.

---
Confidence: ~75% | η=4.2, KROG: ✓
```

## Structure Decision Tree

```
Query received
    │
    ├─ Force R0? ("define", "what is") → R0 template
    │
    ├─ Complexity <4? → R1 template
    │
    ├─ Complexity <8? → R2 template
    │
    └─ Complexity ≥8? → R3 template
```

## Validation Checklist

Before emitting:

- [ ] Matches routing level constraints
- [ ] Teleology before mechanism
- [ ] Explicit causation (→) where applicable
- [ ] Confidence stated
- [ ] No forbidden patterns (bullets at R0-R2, excess bold)
- [ ] Word count appropriate
