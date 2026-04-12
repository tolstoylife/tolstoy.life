# The Seven Laws of Executable Documentation

Complete specification of the governance invariants.

## Law 1: E2E Verification

```haskell
∀f ∈ Features. deployed(f) ⟹ e2e_verified(f)
```

**Principle:** Nothing reaches production without runtime verification.

**Implementation:**
```yaml
# E2E must verify actual behavior, not just code correctness
e2e_requirements:
  - spin_up_actual_environment: true
  - hit_real_endpoints: true
  - verify_database_state: true
  - screenshot_ui_changes: true
  - include_edge_cases: true
```

**Why This Matters:**
- AI produces code that *looks* correct but may not *behave* correctly
- Compilation success ≠ functional correctness
- 80%+ of issues found in E2E that passed unit tests

**Verification Methods:**
| Method | Trust | Use When |
|--------|-------|----------|
| Automated E2E suite | 0.90 | Every PR |
| AI-driven exploratory | 0.85 | New features |
| Manual smoke test | 0.80 | Critical paths |
| Screenshot diff | 0.85 | UI changes |
| Database assertions | 0.90 | Data mutations |

---

## Law 2: Observability

```haskell
∀e ∈ Executions. observable(e) ∧ traceable(e)
```

**Principle:** If it ran, we can see what happened.

**Implementation:**
```python
@dataclass
class ObservabilityRequirements:
    structured_logging: bool = True      # JSON, not text
    trace_correlation: bool = True       # Request IDs propagate
    error_context: bool = True           # Stack traces preserved
    ai_log_review: bool = True           # Agent inspects pre-merge
    alerting_defined: bool = True        # Failure conditions explicit

def verify_observable(execution: Execution) -> bool:
    return (
        has_structured_logs(execution) and
        has_trace_id(execution) and
        errors_have_context(execution)
    )
```

**Log Inspection Workflow:**
```
FEATURE → INSTRUMENT → DEPLOY → TEST → INSPECT_LOGS → PROCEED/FIX
                                            ↓
                                    [anomalies found]
                                            ↓
                                    FIX_BEFORE_MERGE
```

---

## Law 3: Script Enforcement

```haskell
∀r ∈ CriticalRules. script_enforced(r)
```

**Principle:** If it's not scripted, it's aspirational.

**Enforcement Hierarchy:**
```
TIER 1: BLOCKING SCRIPTS (Trust: 1.0)
  - Linters (ESLint, Ruff)
  - Type checkers (TypeScript, mypy)
  - Schema validators
  - Custom preflight scripts
  STATUS: Violations block merge

TIER 2: AGENT INSTRUCTIONS (Trust: 0.3)
  - AGENT.md / claude.md
  - System prompts
  STATUS: May follow, will eventually ignore

TIER 3: WRITTEN CONVENTIONS (Trust: 0.1)
  - Style guides
  - Architecture docs
  STATUS: Will drift, will be ignored
```

**Conversion Protocol:**
```python
def enforce_rule(rule: Rule) -> Enforcement:
    """Convert rule to enforceable form."""
    
    if can_lint(rule):
        return LinterRule(rule)  # Tier 1
    
    if can_type_check(rule):
        return TypeConstraint(rule)  # Tier 1
    
    if can_schema_validate(rule):
        return SchemaRule(rule)  # Tier 1
    
    if can_script_check(rule):
        return PreflightCheck(rule)  # Tier 1
    
    # Cannot enforce mechanically
    return AgentInstruction(rule)  # Tier 2 (low trust)
```

---

## Law 4: Human Review

```haskell
∀pr ∈ PRs. merged(pr) ⟹ human_reviewed(pr)
```

**Principle:** AI code still requires human judgment.

**Review Dimensions:**
```yaml
review_checklist:
  requirement_alignment:
    question: "Does code match original intent?"
    ai_weakness: "Optimizes for plausibility, not requirements"
  
  architectural_consistency:
    question: "Does it fit existing patterns?"
    ai_weakness: "May introduce novel but inconsistent patterns"
  
  security_implications:
    question: "Any vulnerabilities introduced?"
    ai_weakness: "May miss subtle security issues"
  
  semantic_correctness:
    question: "Logic errors AI introduced?"
    ai_weakness: "Syntactically correct ≠ semantically correct"
  
  code_as_documentation:
    question: "Do types/names/structure document intent?"
    ai_weakness: "May name things generically"
```

**Review as Documentation Verification:**
```
Reviewer asks: "Does this code accurately document what it should do?"

NOT: "Is the documentation correct?"
BUT: "Is the code (which IS the documentation) correct?"
```

---

## Law 5: Code as Documentation

```haskell
∀d ∈ AuthoritativeDoc. d ⊂ Codebase
```

**Principle:** The code is the only truth.

**Documentation Mapping:**
| Need | Code Form | Tier |
|------|-----------|------|
| API contract | OpenAPI spec (generated) | T3 |
| Data shapes | TypeScript interfaces | T1 |
| Business rules | Validation functions | T5 |
| Access control | Auth middleware | T5 |
| Workflow steps | State machine / enum | T1 |
| Configuration | Typed config objects | T1 |
| Error conditions | Custom error classes | T1 |
| Dependencies | package.json | T5 |
| Database schema | Migrations | T4 |
| Style rules | Linter config | T5 |
| Architecture | Generated diagrams | T3 |

**Anti-Pattern Detection:**
```python
def detect_external_docs(project: Path) -> List[Violation]:
    """Find documentation that will drift."""
    violations = []
    
    external_doc_patterns = [
        "docs/*.md",           # Will drift
        "ARCHITECTURE.md",     # Will drift
        "API_REFERENCE.md",    # Should be generated
        "IMPLEMENTATION.md",   # Should be TODOs
    ]
    
    for pattern in external_doc_patterns:
        for file in project.glob(pattern):
            violations.append(
                Violation(
                    file=file,
                    message="External doc detected—will drift",
                    suggestion="Convert to code-based documentation"
                )
            )
    
    return violations
```

---

## Law 6: Compilation as Validation

```haskell
compiles(d) ∨ validates(d) ⟹ current(d)
```

**Principle:** If it executes successfully, documentation is current.

**Verification Chain:**
```
Types compile    → Type docs current
Schemas validate → Schema docs current
Migrations run   → DB docs current
Specs generate   → API docs current
Linters pass     → Style docs current
TODOs resolved   → Plan docs current
─────────────────────────────────────
ALL PASS         → Documentation IS current
```

**Implementation:**
```python
def documentation_is_current(project: Project) -> bool:
    """Documentation validity = execution success."""
    return all([
        project.types_compile(),       # T1
        project.schemas_validate(),    # T2
        project.specs_generate(),      # T3
        project.migrations_run(),      # T4
        project.linters_pass(),        # T5
        project.required_todos_resolved(),  # T7
    ])
```

---

## Law 7: TODOs as Plans

```haskell
∀plan ∈ Plans. expressed_as_todos(plan) ∧ in_code(plan)
```

**Principle:** Plans live where work happens.

**TODO Lifecycle:**
```
PLANNING:     Write TODOs at implementation locations
DEVELOPMENT:  Implement code, remove TODO when done
VERIFICATION: Grep for remaining TODOs
COMPLETION:   Zero required TODOs = feature complete
```

**Categories:**
```python
# TODO(id): Standard task
# TODO(id,required): Blocks merge
# TODO(id,blocked:dep): Waiting on dependency
# TODO(tech-debt): Known improvement
# TODO(security): Security task (high priority)
# FIXME: Known bug
# HACK: Temporary solution
```

**Why This Works:**
1. TODOs live WHERE THE WORK HAPPENS → Context preserved
2. TODOs are GREP-ABLE → Progress measurable
3. TODOs are SELF-REMOVING → No stale documentation
4. TODOs are VERSION-CONTROLLED → History preserved

**External Plans (Anti-Pattern):**
```
IMPLEMENTATION_PLAN.md:
  - Written before implementation
  - Lives outside code
  - Becomes stale immediately
  - AI may not read it
  - No completion enforcement

RESULT: Plan says one thing, code does another
```

---

## Law Composition

The Seven Laws form a DAG where each enables the next:

```
LAW_5 (Code is Doc) ─────────────────────────────────┐
    │                                                 │
    ├──► LAW_6 (Compile = Current)                   │
    │        │                                        │
    │        └──► LAW_3 (Script Enforced) ──────────┐│
    │                    │                           ││
    │                    └──► LAW_7 (TODOs) ────────┐││
    │                                               │││
LAW_2 (Observable) ──► LAW_1 (E2E Verified) ───────┤││
                                │                   │││
                                └──► LAW_4 (Review) ┘││
                                         │           ││
                                         └───────────┴┴──► DEPLOYED
```

**Invariant:** No law can be satisfied without its dependencies.

---

## Violation Severity

| Violation | Severity | Response |
|-----------|----------|----------|
| E2E not run | CRITICAL | Block deploy |
| No logging | MAJOR | Block merge |
| Rule not scripted | MAJOR | Convert to script |
| No review | CRITICAL | Block merge |
| External docs | MINOR | Convert to code |
| Compiles but wrong | MAJOR | Add E2E test |
| Required TODOs remain | CRITICAL | Block merge |

---

## Verification Script

```python
def verify_seven_laws(project: Project) -> LawsResult:
    """Verify all Seven Laws are satisfied."""
    
    results = {
        "LAW_1": verify_e2e_coverage(project),
        "LAW_2": verify_observability(project),
        "LAW_3": verify_script_enforcement(project),
        "LAW_4": verify_review_required(project),
        "LAW_5": verify_code_is_doc(project),
        "LAW_6": verify_compile_validates(project),
        "LAW_7": verify_todos_as_plans(project),
    }
    
    return LawsResult(
        passed=all(r.passed for r in results.values()),
        violations=[r.violations for r in results.values() if not r.passed],
        results=results
    )
```
