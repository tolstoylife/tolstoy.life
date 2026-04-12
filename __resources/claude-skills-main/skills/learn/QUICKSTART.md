# Learn Skill Quickstart

Get productive with the learn skill in 5 minutes.

## What is Learn?

Learn is a **recursive self-improving holon** that compounds knowledge through structured reflection. It implements:

```
λ(ο,Κ,Σ).τ' — Knowledge compounds, schema evolves.
```

Every interaction makes future interactions easier.

## When to Use

| Trigger | Use Case |
|---------|----------|
| `/learn` | Explicit learning mode |
| `/compound` | Extract learnings from session |
| `/improve` | Enhance existing knowledge |
| "lessons learned" | Post-mortem reflection |
| "best practices" | Pattern extraction |

## Quick Pipeline

```
Query → PARSE → ROUTE → EXECUTE → ASSESS → COMPOUND → Response
                                      ↓
                              Knowledge grows (Κ→Κ')
```

## Core Invariants

| Invariant | Rule | Why |
|-----------|------|-----|
| **Κ-monotonicity** | Knowledge never decreases | Compound interest |
| **η ≥ 4** | Maintain edge density | Rich connections |
| **Vertex-sharing** | Integrate via shared concepts | No orphan knowledge |

## 5-Minute Workflow

### 1. Parse Your Goal

What are you trying to learn or improve?

```yaml
goal: "Understand cardiac output regulation"
domain: physiology
current_knowledge: [Fick principle, preload, afterload]
```

### 2. Route to Complexity

The skill auto-routes based on complexity:

| Score | Route | Response Style |
|-------|-------|----------------|
| < 2 | R0 | Brief definition |
| < 4 | R1 | 1-2 paragraphs |
| < 8 | R2 | Mechanistic explanation |
| ≥ 8 | R3 | Comprehensive with KROG |

### 3. Execute with Context

The skill pulls from your knowledge base (Κ):

```
"Given what you know about Fick principle..."
```

### 4. Compound the Learning

After resolution, extract:

```yaml
trigger: "what initiated learning"
insight: "key takeaway"
vertices: ["[[shared concept 1]]", "[[shared concept 2]]"]
prevention: "how to avoid future confusion"
```

## Domains

| Domain | Focus | η Target |
|--------|-------|----------|
| `learning` | Knowledge acquisition | 4.0 |
| `coding` | Software patterns | 4.5 |
| `research` | Academic investigation | 5.0 |
| `writing` | Content creation | 3.5 |
| `meta` | Self-improvement | 5.5 |

## Common Patterns

### Pattern 1: Post-Task Reflection

After completing any significant task:

```
/compound

What worked:
- [observation 1]
- [observation 2]

What didn't:
- [problem 1]

For next time:
- [prevention strategy]
```

### Pattern 2: Concept Integration

When learning something new:

```
/learn [new concept]

Connect to existing knowledge:
- Related to: [[existing concept 1]]
- Builds on: [[prerequisite]]
- Contrasts with: [[alternative approach]]
```

### Pattern 3: Skill Improvement

When a skill needs refinement:

```
/improve [skill area]

Current state:
- [assessment]

Target state:
- [goal]

Gap analysis:
- [what's missing]
```

## Integration with Lambda

Learn extends the core λ transformation:

```haskell
-- Lambda (basic)
λο.τ = emit ∘ validate ∘ execute ∘ route ∘ parse

-- Learn (with compounding)
λ(ο,Κ,Σ).τ' = let τ = (emit ∘ validate ∘ execute(Κ) ∘ route ∘ parse) ο
                   Κ' = Κ ∪ compound(assess(τ))
               in (τ, Κ')
```

## File Navigation

| Need | File |
|------|------|
| Full skill definition | [SKILL.md](SKILL.md) |
| Complete index | [INDEX.md](INDEX.md) |
| Schema reference | [schema.yaml](schema.yaml) |
| Phase details | [phases/](phases/) |
| Domain guides | [domains/](domains/) |
| Concept explanations | [concepts/](concepts/) |

## Quick Reference

```
┌────────────────────────────────────────────────┐
│ λ(ο,Κ,Σ).τ'                                    │
│                                                │
│ Parse → Route → Execute → Assess → Compound    │
│                                                │
│ Invariants:                                    │
│   • Κ grows monotonically                      │
│   • η ≥ 4 preserved                            │
│   • Vertex-sharing enforced                    │
│                                                │
│ Triggers: /learn /compound /improve /reflect   │
└────────────────────────────────────────────────┘
```

---

**Next Steps:**
1. Try `/learn` with a topic you're studying
2. After a work session, use `/compound` to extract learnings
3. Review [concepts/compound-interest.md](concepts/compound-interest.md) for the theory

The more you use it, the smarter it gets. That's the point.
