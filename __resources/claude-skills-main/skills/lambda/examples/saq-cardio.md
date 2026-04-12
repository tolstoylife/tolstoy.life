# SAQ Example: Cardiovascular Physiology

> Demonstrates λ(ο,K).τ at R1 complexity with η∈[2.0,2.5] for SAQ constraints.

## Question

**"Describe the factors that determine myocardial oxygen supply and demand."** (10 marks)

## λ Processing

### Parse (ρ)
```yaml
intent: explain physiological determinants
domain: cardiovascular physiology
components: [supply, demand]
constraints:
  format: SAQ
  words: ~200
  marks: 10
keywords: ["myocardial", "oxygen", "supply", "demand"]
```

### Route (Π)
- Complexity score: 3.5 (domains=1×2, depth=2×3=6, stakes=1×1.5, novelty=0)
- **Route → R1** (score < 4)
- Constraints: 1-2¶, implicit η, prose primacy

### Execute (Ψ)

**Response:**

Myocardial oxygen supply depends primarily on coronary blood flow and arterial oxygen content. Coronary flow occurs predominantly during diastole, driven by the pressure gradient between the aortic root and right atrium, and is regulated by metabolic vasodilators (adenosine, K⁺, H⁺) that match perfusion to demand. Oxygen content depends on haemoglobin concentration and saturation, with extraction already near-maximal (~70%) at rest—limiting the reserve for increased extraction.

Myocardial oxygen demand is determined by heart rate, contractility, and wall tension. Wall tension, by Laplace's law, increases with ventricular pressure and radius while decreasing with wall thickness. The rate-pressure product (HR × systolic BP) provides a clinical index of demand. Any imbalance—whether from reduced supply (coronary stenosis, hypoxaemia) or increased demand (tachycardia, hypertension)—precipitates ischaemia.

### Validate (Γ+χ)

**Topology (η):**
```
Nodes (V=8): supply, demand, coronary flow, O₂ content, wall tension,
             heart rate, contractility, rate-pressure product
Edges (E=18): supply→coronary flow, supply→O₂ content,
              coronary flow→diastole, coronary flow→pressure gradient,
              coronary flow→metabolic regulation, O₂ content→Hb,
              O₂ content→saturation, demand→HR, demand→contractility,
              demand→wall tension, wall tension→Laplace,
              wall tension→pressure, wall tension→radius,
              wall tension→thickness, rate-pressure product→HR,
              rate-pressure product→SBP, imbalance→ischaemia,
              supply↔demand (balance)

η = 18/8 = 2.25 ✓ (target: 2.0-2.5)
```

**KROG:**
- [x] K: Reasoning transparent (cause→effect chains)
- [x] R: Within physiological expertise
- [x] O: Complete (both supply and demand addressed)
- [x] G: Safe, educational, proportional

**Style (Φ):**
- [x] Prose primacy (no bullet points)
- [x] Mechanistic (A→B→C causation)
- [x] Teleological hints ("matching perfusion to demand")

### Emit

Word count: 178 ✓
Paragraphs: 2 ✓
Format: Prose only ✓

## Compound (Κ)

```yaml
trigger: "SAQ cardiovascular example completed"
insight: "Supply/demand dichotomy provides natural 2-paragraph structure"
vertices:
  - "[[Coronary Blood Flow]]"
  - "[[Myocardial Oxygen Consumption]]"
  - "[[Laplace's Law]]"
  - "[[Rate-Pressure Product]]"
prevention: "Always address both sides of physiological balance questions"
```

## Connected Concepts

| Concept | Relationship |
|---------|--------------|
| [[Coronary Blood Flow]] | concept_direct |
| [[Fick Principle]] | concept_prerequisite |
| [[Laplace's Law]] | concept_mechanism |
| [[Oxygen-Haemoglobin Dissociation]] | concept_indirect |

## Mark Scheme Alignment

| Component | Marks | Coverage |
|-----------|-------|----------|
| Supply factors | 5 | Coronary flow, O₂ content, diastolic timing, metabolic regulation |
| Demand factors | 5 | HR, contractility, wall tension, Laplace, RPP |

---

```
λ(ο,K).τ    R1    η=2.25    KROG✓    Φ=prose    ~180 words
```
