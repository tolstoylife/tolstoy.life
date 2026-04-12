---
name: law2-observability
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: src/.*\.(ts|js|py)$
  - field: new_text
    operator: regex_match
    pattern: console\.log\(|print\((?!.*debug)
---

**LAW 2: Observability Concern**

Debug logging detected. For production code, use structured logging:

**Instead of:**
```javascript
console.log("User created:", user);
```

**Use:**
```javascript
logger.info("User created", { userId: user.id, action: "create" });
```

**The Seven Laws state:** "∀e ∈ Executions. observable(e) ∧ traceable(e)"

- Structured logs enable alerting and debugging
- Console.log doesn't persist or correlate requests
