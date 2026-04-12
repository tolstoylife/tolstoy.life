# Routing Examples

Classification decisions demonstrating pipeline selection.

## R0 Examples

### Query: "What is MAC?"

**Force trigger**: "What is" → R0

**Score**: N/A (forced)

**Response**:
> MAC (minimum alveolar concentration) is the alveolar concentration of an inhaled anaesthetic at 1 atm that prevents movement in 50% of subjects in response to a surgical stimulus.

**Validation**: 18 words ✓, no formatting ✓

---

### Query: "Define cardiac output"

**Force trigger**: "Define" → R0

**Response**:
> Cardiac output is the volume of blood pumped by the heart per unit time, calculated as stroke volume × heart rate, typically 4-8 L/min in adults.

---

## R1 Examples

### Query: "How does age affect MAC?"

**Score**:
```
domains = 1 (pharmacology)        × 2 = 2
depth = 1 (single mechanism)      × 3 = 3
stakes = 0 (conceptual)           × 1.5 = 0
novelty = 0 (well-established)    × 2 = 0
Total = 5 → would be R2, but single-factor question → R1
```

**Response**:
> MAC decreases approximately 6% per decade after age 40, reflecting reduced neuronal density and altered receptor sensitivity. Neonates have lower MAC than infants, with MAC peaking at around 6 months of age. The age-MAC relationship follows a predictable pattern: MAC at age X ≈ MAC40 × (1 - 0.006 × (X - 40)) for adults. This has direct clinical implications for dosing volatile agents in elderly patients.

---

### Query: "SAQ: List factors that affect MAC"

**Force trigger**: "SAQ" → R1 with exam constraints

**Response**:
> MAC is influenced by physiological, pharmacological, and pathological factors. Physiologically, age reduces MAC (6% per decade after 40), while pregnancy and hyperthermia also decrease it. Pharmacologically, opioids, benzodiazepines, α2-agonists, and other CNS depressants reduce MAC synergistically. Acute alcohol intoxication decreases MAC, while chronic use increases it. Pathologically, hypoxia (PaO2 <40 mmHg), severe hypotension, and metabolic acidosis reduce MAC. Factors that do not significantly affect MAC include duration of anaesthesia, gender, and thyroid status. Notably, MAC-awake is approximately 0.3-0.4 MAC, relevant for emergence. Understanding these factors enables rational dose adjustment.

**Word count**: 107 | **η**: ~2.4

---

## R2 Examples

### Query: "Explain the mechanism of propofol hypotension"

**Score**:
```
domains = 2 (pharmacology + physiology)  × 2 = 4
depth = 2 (mechanistic pathway)          × 3 = 6
stakes = 1 (clinical relevance)          × 1.5 = 1.5
novelty = 0 (established)                × 2 = 0
Total = 11.5 → R2
```

**Response** (R2 mechanistic template):

> Understanding propofol's cardiovascular effects is essential for safe induction, particularly in haemodynamically vulnerable patients.

> Propofol → GABA-A receptor potentiation (central) → reduced sympathetic outflow → ↓noradrenaline at vascular smooth muscle → arterial and venous relaxation → ↓SVR (dominant, 15-40% reduction) + ↓venous return. Simultaneously: propofol → direct myocardial calcium channel effects → ↓contractility (mild in healthy patients). Combined result: hypotension predominantly from afterload reduction, with relatively preserved cardiac output.

> Clinically: expect 15-40% MAP drop, HR typically unchanged or slight reflex increase. High-risk groups: hypovolaemic, elderly, AS, reduced EF. Mitigation: slow injection (20-40s), preload optimisation, co-induction with opioid, vasopressor availability.

> ~85% confidence based on extensive clinical literature; individual variability exists.

---

### Query: "Compare the cardiovascular effects of sevoflurane and isoflurane"

**Score**:
```
domains = 2 (two agents)         × 2 = 4
depth = 2 (mechanism comparison) × 3 = 6
stakes = 1 (clinical choice)     × 1.5 = 1.5
novelty = 0 (established)        × 2 = 0
Total = 11.5 → R2
```

**Response**:

> Comparing volatile agents' cardiovascular profiles guides selection in patients with cardiac disease.

> Both agents reduce SVR and MAP dose-dependently. Isoflurane → more pronounced tachycardia (coronary steal concern, largely theoretical) + greater SVR reduction. Sevoflurane → more cardiac depression + less tachycardia + more stable SVR. Mechanism: isoflurane preferentially dilates resistance vessels; sevoflurane has greater direct myocardial effect via calcium handling.

> Clinically: sevoflurane preferred in coronary disease (no steal risk, stable HR), isoflurane acceptable with rate control. Both preserve response to catecholamines. At equi-MAC doses, sevoflurane produces ~5-10% less HR increase than isoflurane.

> ~80% confidence; limitation: clinical significance of differences is modest in most patients.

---

## R3 Examples

### Query: "Provide a comprehensive analysis of volatile anaesthetic choice in aortic stenosis"

**Score**:
```
domains = 3 (agents + pathophysiology + clinical) × 2 = 6
depth = 3 (systems integration)                    × 3 = 9
stakes = 2 (critical patient population)           × 1.5 = 3
novelty = 1 (nuanced decision)                     × 2 = 2
Total = 20 → R3
```

**Force triggers**: "comprehensive" → R3

**Response**: Full R3 template with Purpose → Mechanism (S→T→O) → Evidence → Application → Limitations

[See templates/response.md for R3 structure]

---

### Query: "Verify the current evidence for sugammadex in malignant hyperthermia"

**Force trigger**: "verify" + "current evidence" → R3

This requires web search for current literature, full KROG validation, comprehensive synthesis.

---

## Decision Matrix

| Pattern | Route | Rationale |
|---------|-------|-----------|
| "Define X" | R0 | Force trigger |
| "What is X?" | R0 | Force trigger |
| "List factors for X" | R1 | Enumeration |
| "SAQ: X" | R1 | Exam constraint |
| "Explain mechanism of X" | R2 | Causal depth |
| "Compare X and Y" | R2 | Multi-domain |
| "Comprehensive analysis" | R3 | Force trigger |
| "Current evidence for X" | R3 | Force trigger |
| "Verify X" | R3 | Force trigger |

## Escalation Example

**Initial**: Query classified R1
**During execution**: Validation fails (η < 2.0)
**Action**: Escalate to R2, add graph skill
**Result**: η achieved, emit

## De-escalation Example

**Initial**: Query classified R2
**Context**: User said "quick answer"
**Action**: De-escalate to R1
**Constraint**: Drop explicit η validation, use implicit
