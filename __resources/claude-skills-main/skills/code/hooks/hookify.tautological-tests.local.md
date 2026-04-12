---
name: tautological-tests
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: (test_.*|.*\.test\.|.*\.spec\.)(py|ts|js)$
  - field: new_text
    operator: regex_match
    pattern: assert.*==\s*True|expect\(.*\)\.toBe\(true\)
---

**LAW 3 Caveat: Potential Tautological Test**

Pattern detected: `assert ... == True` or `expect(...).toBe(true)`

**Risk:** Tests that verify implementation matches implementation are tautological:
```python
# BAD: Test just verifies code does what code does
def test_auth():
    assert authenticate("user", "pass") == True  # PASSES but proves nothing
```

**Better:**
```python
# GOOD: Test verifies requirement
def test_auth_with_valid_credentials():
    user = create_user(password="secret123")
    result = authenticate(user.email, "secret123")
    assert result.authenticated == True
    assert result.user_id == user.id
```

**Trust hierarchy:** E2E (0.9) > Review (0.75) > Unit (0.3)
