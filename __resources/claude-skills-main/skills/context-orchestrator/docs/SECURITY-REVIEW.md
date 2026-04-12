# Security Review: Context Orchestrator

**Review Date**: 2026-01-05
**Reviewer**: Red Team Analysis
**Severity Scale**: Critical | High | Medium | Low | Info

---

## Executive Summary

The Context Orchestrator implementation has been subjected to red team security review. Several issues were identified ranging from potential command injection to data exposure concerns. Mitigations are provided for each finding.

---

## Findings

### 1. Command Injection in Intent Detector

**Severity**: HIGH
**Location**: `hooks/context-intent-detector.ts` lines 106-114, 167-179

**Issue**: User input from prompts is embedded directly into suggested CLI commands without proper escaping. A malicious prompt containing shell metacharacters could lead to command injection if these commands are executed without sanitization.

**Example Attack Vector**:
```
User prompt: /context `rm -rf ~`; cat /etc/passwd
Resulting command: limitless workflow search "`rm -rf ~`; cat /etc/passwd" --format json
```

**Mitigation**:
```typescript
function escapeShellArg(arg: string): string {
  // Escape single quotes and wrap in single quotes
  return "'" + arg.replace(/'/g, "'\\''") + "'";
}

// Use:
signal.suggested_commands.limitless = `limitless workflow search ${escapeShellArg(query)} --format json`;
```

**Status**: FIXED (2026-01-05) - Added `escapeShellArg()` and `sanitizeQuery()` functions

---

### 2. Path Traversal in Cache Manager

**Severity**: MEDIUM
**Location**: `scripts/cache-manager.py` line 71

**Issue**: The `generate_key` function uses query content directly in cache key generation. While currently only used for lookup, if cache keys were ever used in file paths, path traversal could occur.

**Example Attack Vector**:
```python
query = "../../../etc/passwd"
# Could potentially escape cache directory
```

**Current Mitigation**: Hash-based key generation already mitigates this by converting to hex digest.

**Status**: ACCEPTABLE (current implementation safe)

---

### 3. Resource Exhaustion - Cache Size

**Severity**: LOW
**Location**: `scripts/cache-manager.py` lines 27-28

**Issue**: `MAX_CACHE_SIZE_MB = 5` is defined but not enforced. Large result payloads could exceed this limit.

**Mitigation**: Add size check before caching:
```python
def set_cache(source: str, query: str, result: Any):
    result_size = len(json.dumps(result))
    if result_size > MAX_CACHE_SIZE_MB * 1024 * 1024:
        return {"error": "Result too large to cache"}
    # ... rest of function
```

**Status**: ENHANCEMENT RECOMMENDED

---

### 4. Sensitive Data Exposure in History

**Severity**: MEDIUM
**Location**: `scripts/history.py`

**Issue**: The history log stores full extraction results which may contain sensitive data (personal conversations, credentials in code, medical information). No encryption or access control is implemented.

**Example Risk**:
- Limitless extractions may contain private conversations
- Pieces extractions may contain API keys or credentials from code
- History persists for 90 days by default

**Mitigation**:
1. Add content redaction for known sensitive patterns
2. Consider encryption at rest
3. Reduce retention period for sensitive sources
4. Add explicit user consent before logging

```python
SENSITIVE_PATTERNS = [
    r'(?i)(api[_-]?key|secret|password|token)\s*[=:]\s*\S+',
    r'(?i)(bearer|authorization)\s*:\s*\S+',
]

def redact_sensitive(content: str) -> str:
    for pattern in SENSITIVE_PATTERNS:
        content = re.sub(pattern, '[REDACTED]', content)
    return content
```

**Status**: ENHANCEMENT RECOMMENDED

---

### 5. Unvalidated JSON Input in Hooks

**Severity**: LOW
**Location**: `hooks/context-intent-detector.ts` lines 224-229

**Issue**: The hook accepts both JSON and plain text input. Malformed JSON could potentially cause issues, though current implementation handles gracefully.

**Current Mitigation**: Try-catch with fallback already implemented.

**Status**: ACCEPTABLE

---

### 6. TTL Clock Skew Vulnerability

**Severity**: INFO
**Location**: `scripts/cache-manager.py` line 81

**Issue**: TTL calculation uses local system time. Clock manipulation could bypass cache TTL.

**Impact**: Minimal - only affects caching behavior, not security.

**Status**: ACCEPTABLE (low impact)

---

### 7. No Rate Limiting

**Severity**: LOW
**Location**: System-wide

**Issue**: No rate limiting on CLI invocations. Rapid repeated queries could cause resource exhaustion or API rate limit issues on research CLI.

**Mitigation**: Add rate limiter:
```python
from functools import lru_cache
from time import time

RATE_LIMITS = {
    "limitless": 10,  # 10 per minute
    "research": 5,    # 5 per minute (API limits)
    "pieces": 20,     # 20 per minute
}

class RateLimiter:
    def __init__(self):
        self.calls = {}

    def check(self, source: str) -> bool:
        now = time()
        window = 60  # 1 minute window

        if source not in self.calls:
            self.calls[source] = []

        # Clean old calls
        self.calls[source] = [t for t in self.calls[source] if now - t < window]

        if len(self.calls[source]) >= RATE_LIMITS.get(source, 10):
            return False

        self.calls[source].append(now)
        return True
```

**Status**: ENHANCEMENT RECOMMENDED

---

### 8. Subprocess Timeout Not Enforced

**Severity**: MEDIUM
**Location**: General architecture (subagent invocation)

**Issue**: While timeouts are documented (10s/15s/8s per CLI), actual enforcement depends on Claude's timeout handling. Hung CLI processes could block indefinitely.

**Mitigation**: Add explicit timeout wrapper:
```bash
# In hook scripts
timeout 10s limitless lifelogs search "$query" || echo '{"error": "timeout"}'
```

**Status**: ENHANCEMENT RECOMMENDED

---

### 9. Log Injection

**Severity**: LOW
**Location**: `scripts/metrics.py`

**Issue**: User-controlled data is written to log files. While JSONL format mitigates most issues, specially crafted input could create misleading log entries.

**Mitigation**: Sanitize log data:
```python
def sanitize_for_log(data: str) -> str:
    # Remove control characters
    return re.sub(r'[\x00-\x1f\x7f-\x9f]', '', data)
```

**Status**: LOW PRIORITY

---

### 10. Missing Input Validation on CLI Args

**Severity**: MEDIUM
**Location**: `scripts/cache-manager.py`, `scripts/history.py`, `scripts/metrics.py` (main functions)

**Issue**: CLI arguments are passed directly to functions without validation. While these are internal scripts, improper usage could cause unexpected behavior.

**Example**:
```bash
python3 cache-manager.py set "" "" ""  # Empty values
python3 history.py search --limit -1    # Negative limit
```

**Mitigation**: Add input validation:
```python
def validate_source(source: str) -> bool:
    return source in ["limitless", "research", "pieces"]

def validate_limit(limit: int) -> int:
    return max(1, min(limit, 1000))
```

**Status**: ENHANCEMENT RECOMMENDED

---

## Summary

| Severity | Count | Status |
|----------|-------|--------|
| Critical | 0 | - |
| High | 1 | FIXED |
| Medium | 3 | Documented for next iteration |
| Low | 4 | Optional improvements |
| Info | 1 | No action required |

---

## Recommendations

### Immediate Actions (High Priority)
1. ~~**Fix command injection** in intent detector by implementing proper shell escaping~~ ✅ COMPLETED

### Short-term Actions (Medium Priority)
2. Add sensitive data redaction to history logging
3. Implement subprocess timeout enforcement
4. Add input validation to CLI scripts

### Long-term Actions (Low Priority)
5. Add rate limiting
6. Implement encryption at rest for sensitive caches
7. Add log sanitization
8. Consider adding audit logging for security events

### Bugs Fixed During Review
- Fixed typo: `scores.saved` → `scores.pieces` in pattern scoring

---

## Appendix: Attack Scenarios Tested

1. **Command Injection via Prompt**: Tested with shell metacharacters - identified vulnerability
2. **Path Traversal**: Tested cache key generation - safe due to hashing
3. **Resource Exhaustion**: Tested large payloads - identified missing size limits
4. **Race Conditions**: Tested concurrent cache access - acceptable behavior
5. **Data Leakage**: Reviewed history storage - identified sensitive data risk
6. **Privilege Escalation**: Not applicable (runs as user)
7. **Denial of Service**: Tested rapid requests - identified missing rate limits
