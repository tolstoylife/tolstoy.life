---
name: inference-chain
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: src/.*\.(ts|js|py)$
  - field: new_text
    operator: regex_match
    pattern: (TODO|FIXME|BUG|HACK).*\?$
---

**Abductive Inference Incomplete**

Detected uncertainty marker (ending with ?). Complete the inference chain.

**Abductive reasoning requires:**

```
Observation (O) -> Hypothesis (H) -> Prediction (P) -> Test (T)
```

**Convert uncertainty to testable hypothesis:**

**Instead of:**
```python
# TODO: Why does this fail sometimes?
```

**Use:**
```python
# O: Intermittent failure under load
# H: Race condition in shared state access
# P: Adding mutex should eliminate failures
# T: Load test with mutex -> verify no failures
# TODO(race-fix,required): Implement mutex per hypothesis
```

**Compound benefit:**
Each resolved hypothesis becomes reusable pattern in K.

**Quick template:**
```python
# O: [observation]
# H: [best explanation]
# P: [testable prediction]
# T: [verification method]
# TODO(id): [action based on hypothesis]
```
