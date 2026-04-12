# Viva Example: Pharmacology

> Demonstrates λ(ο,K).τ at R2 complexity with η∈[3.0,4.0] for viva format, including progressive disclosure and follow-up anticipation.

## Opening Question

**"Tell me about the mechanism of action of propofol."**

## λ Processing

### Parse (ρ)
```yaml
intent: explain mechanism
domain: pharmacology (anaesthetics)
components: [mechanism, receptor, effect]
constraints:
  format: viva
  style: progressive disclosure
  anticipate: follow-ups likely
keywords: ["propofol", "mechanism", "action"]
```

### Route (Π)
- Complexity score: 5.0 (domains=1×2, depth=3×3=9, stakes=2×1.5=3, novelty=0)
- **Route → R2** (4 ≤ score < 8)
- Constraints: η≥3.0, mechanistic, anticipate follow-ups

### Execute (Ψ) — Progressive Disclosure

**Opening Response (30 seconds):**

Propofol is a GABA-A receptor positive allosteric modulator. It binds to the β-subunit of the pentameric GABA-A receptor, potentiating chloride conductance and hyperpolarising neurons. This produces dose-dependent CNS depression: sedation, hypnosis, and at higher concentrations, burst suppression. The onset is rapid due to high lipid solubility enabling swift blood-brain barrier penetration, while redistribution terminates the effect.

### Validate (Round 1)

```
η = 15/5 = 3.0 ✓
Nodes: propofol, GABA-A, β-subunit, Cl⁻ conductance, CNS depression
Edges: 15 (mechanism chain + properties)
```

---

## Anticipated Follow-ups

### Follow-up 1: "What about the cardiovascular effects?"

**Response:**

Propofol causes hypotension through multiple mechanisms. It reduces sympathetic tone centrally, decreases systemic vascular resistance via direct smooth muscle relaxation, and has negative inotropic effects. The baroreceptor reflex is blunted, preventing compensatory tachycardia. These effects are exaggerated in hypovolaemia, elderly patients, and those with impaired cardiac function.

```yaml
route: R1 (focused question)
η: 12/4 = 3.0 ✓
anticipate_next: "How would you manage this?"
```

### Follow-up 2: "How does its metabolism compare to thiopentone?"

**Response:**

Propofol is metabolised primarily by hepatic conjugation (glucuronidation and sulphation), with extrahepatic metabolism contributing significantly—clearance exceeds hepatic blood flow, suggesting pulmonary and renal contributions. The context-sensitive half-time remains short even after prolonged infusion due to rapid distribution and metabolism.

In contrast, thiopentone undergoes hepatic oxidation with a long elimination half-life (11 hours). Accumulation occurs with repeated dosing or infusion, causing prolonged sedation. This makes propofol preferable for TIVA and sedation in intensive care.

```yaml
route: R2 (comparative, higher complexity)
η: 20/6 = 3.3 ✓
structure: contrast (propofol vs thiopentone)
```

### Follow-up 3: "What is propofol infusion syndrome?"

**Response:**

Propofol infusion syndrome is a rare but potentially fatal complication of prolonged, high-dose infusion (>4mg/kg/hr for >48 hours). It manifests as metabolic acidosis, rhabdomyolysis, hyperkalaemia, cardiac failure, and lipaemia. The mechanism involves impaired mitochondrial fatty acid oxidation and disruption of the electron transport chain. Risk factors include critical illness, catecholamine infusion, and carbohydrate depletion. Prevention requires limiting dose and duration; treatment is supportive with immediate cessation of propofol.

```yaml
route: R2 (syndrome = multiple components)
η: 18/6 = 3.0 ✓
pattern: syndrome description (mechanism → manifestation → management)
```

---

## Full Viva Graph

```
Nodes (V=12):
  propofol, GABA-A, β-subunit, Cl⁻, CNS depression,
  CVS effects, metabolism, context-sensitive half-time,
  thiopentone, PRIS, mitochondria, fatty acid oxidation

Edges (E=42):
  [mechanism chain: 8]
  [CVS pathway: 6]
  [metabolism pathway: 8]
  [comparison edges: 6]
  [PRIS pathway: 8]
  [cross-references: 6]

η = 42/12 = 3.5 ✓ (target: 3.0-4.0)
```

## KROG Validation

| Check | Status | Evidence |
|-------|--------|----------|
| K (Knowable) | ✓ | Each response builds logically |
| R (Rights) | ✓ | Pharmacology within expertise |
| O (Obligations) | ✓ | Accurate, complete for level |
| G (Governance) | ✓ | Educational, no harm |

## Style (Φ)

- **Teleology first**: Start with "what it does" before "how"
- **Progressive disclosure**: Core concept → details → complications
- **Mechanistic**: Clear A→B→C causation chains
- **Anticipatory**: Each response sets up natural follow-up

## Compound (Κ)

```yaml
trigger: "viva pharmacology example completed"
insight: "Viva requires layered knowledge—opening is iceberg tip"
vertices:
  - "[[Propofol]]"
  - "[[GABA Receptor]]"
  - "[[Context-Sensitive Half-Time]]"
  - "[[Propofol Infusion Syndrome]]"
prevention: "Always prepare 2-3 follow-up depths for viva topics"
pattern: "opening (30s) → mechanism (1min) → complications (1min) → comparisons"
```

## Viva Success Criteria

| Criterion | Achieved |
|-----------|----------|
| Structured opening | ✓ Mechanism-first |
| Progressive depth | ✓ 3 follow-up levels |
| Anticipation | ✓ Natural question flow |
| η maintained | ✓ 3.0-3.5 throughout |
| Time-appropriate | ✓ ~30s per response |

---

```
λ(ο,K).τ    R2    η=3.5    KROG✓    Φ=progressive    viva-ready
```
