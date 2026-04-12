# Citation Formats

## Footnote Standard

All citations use Obsidian-compatible footnote syntax with full bibliographic detail.

### Format Template

```markdown
[^n]: Author(s). *Title*. Edition. Publisher; page. "Verbatim quote if applicable."
```

### Examples by Source Type

#### Textbook (Single Author)
```markdown
[^1]: West JB. *Respiratory Physiology: The Essentials*. 11th ed. Wolters Kluwer; p.204. "Whether flow will be laminar or turbulent depends to a large extent on the Reynolds number."
```

#### Textbook (Multiple Authors)
```markdown
[^2]: Pappano AJ, Wier WG. *Cardiovascular Physiology*. 11th ed. Elsevier; p.123. "For NR = 2000, the flow is usually laminar; for NR > 3000, the flow is turbulent."
```

#### Textbook (et al.)
```markdown
[^3]: Middleton B et al. *Physics in Anaesthesia*. Scion Publishing; p.115. "The Reynolds number is a dimensionless quantity."
```

#### Manual/Reference
```markdown
[^4]: Oh TE. *Oh's Intensive Care Manual*. 8th ed. Elsevier; p.505.
```

#### Multi-Author Reference
```markdown
[^5]: Miller RD et al. *Miller's Anesthesia*. 10th ed. Elsevier; p.329.
```

## Citation Placement Rules

### Inline Citation
For single claims:
```markdown
Reynolds number is dimensionless[^1].
```

### Multiple Citations
For consensus claims:
```markdown
The critical threshold is generally accepted as Re < 2000[^1][^2][^3].
```

### Citation with Contrast
For acknowledged variations:
```markdown
Most sources cite Re < 2000[^1][^2], though stricter thresholds exist[^3].
```

## Deontic Obligations

| Rule | Symbol | Meaning |
|:-----|:-------|:--------|
| **O(cite)** | Obligatory | All claims must have citations |
| **O(page)** | Obligatory | Page numbers required |
| **P(quote)** | Permitted | Direct quotes allowed for definitions |
| **P(multi)** | Permitted | Multiple citations for consensus |
| **F(uncited)** | Forbidden | Uncited claims prohibited |
| **F(generic)** | Forbidden | "From textbook" without specifics |

## Source Quality Weights

| Source Type | Weight | Usage |
|:------------|:-------|:------|
| Examiner reports | 0.95 | Primary for expected answers |
| Core textbooks | 0.85 | Primary for content |
| Review articles | 0.80 | For synthesis and overview |
| Primary research | 0.75 | For specific findings |
| Web sources | 0.50 | Triangulation only |

## Special Cases

### Paraphrased Content
No quotation marks, still requires citation:
```markdown
High velocity, density, and diameter all increase the Reynolds number[^1].
```

### Verbatim Definition
Use quotation marks:
```markdown
Reynolds number is defined as "the ratio of inertial forces to viscous forces"[^1].
```

### Numerical Values
Always cite with page:
```markdown
Critical threshold: Re < 2000 for laminar flow[^1].
```

### Contradicting Sources
Cite both with explicit contrast:
```markdown
While most sources cite Re < 2000[^1][^2], Kam & Power suggest Re < 1000 for definite laminar flow[^3].
```

## Validation Checklist

```
[ ] Every factual claim has at least one citation
[ ] All citations include page numbers
[ ] Verbatim quotes are in quotation marks
[ ] Multiple sources cited for key consensus claims
[ ] Contradictions explicitly cite both sources
[ ] Source quality weights inform synthesis priority
[ ] No generic citations ("textbooks say...")
```
