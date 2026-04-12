---
name: abductive-hypothesis
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: (test_.*|.*\.test\.|.*\.spec\.)(py|ts|js)$
  - field: new_text
    operator: regex_match
    pattern: (describe|it|test)\s*\(\s*['"].*fix|solve|work
---

**Abductive Learning: Hypothesis Verification Required**

Test pattern suggests hypothesis testing (fix/solve/work).

**Abductive reasoning protocol:**

1. **Observation** (O): What behavior was observed?
2. **Hypothesis** (H): What explanation best accounts for O?
3. **Prediction** (P): If H is true, what else should be true?
4. **Test** (T): Does P hold under examination?

**Before committing this test:**

```python
# Document the abductive chain
# O: [describe observed behavior]
# H: [state the hypothesis]
# P: [what this test verifies]
# T: [how test confirms/refutes H]
```

**Anti-pattern detection:**
- Test only verifies implementation (tautological)
- No hypothesis documented
- "Works" without explaining WHY

**Best practice:**
```python
def test_auth_failure_returns_401():
    """
    O: Login with wrong password silently succeeds
    H: Password comparison uses == instead of constant-time compare
    P: Correct implementation returns 401 for wrong password
    T: This test verifies the prediction
    """
    result = authenticate("user", "wrong_password")
    assert result.status_code == 401
```
