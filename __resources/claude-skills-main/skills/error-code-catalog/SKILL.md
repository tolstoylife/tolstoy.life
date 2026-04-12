---
name: error-code-catalog
description: Design structured error codes and error handling for APIs. Create error catalogs with codes, messages, HTTP status mappings, and client-friendly error responses.
---

# Error Code Catalog

Design structured error handling for APIs and applications.

## When to Use

- Designing error responses for a new API
- Standardizing error handling across microservices
- Creating developer-friendly error messages
- Mapping internal errors to HTTP status codes

## Workflow

1. **Define categories** — Auth, validation, business logic, system, external
2. **Assign codes** — Namespaced codes (AUTH_001, VAL_002) or numeric ranges
3. **Write messages** — Developer message (technical) + user message (friendly)
4. **Map to HTTP** — Each error code maps to one HTTP status
5. **Document** — Generate error catalog documentation

## Error Response Structure

```json
{
  "error": {
    "code": "VAL_003",
    "message": "Email address is invalid",
    "details": [{"field": "email", "reason": "must be a valid email"}],
    "request_id": "req_abc123"
  }
}
```

## Best Practices

- Include request_id for support correlation
- Separate developer messages from user-facing messages
- Never expose stack traces or internal details in production
- Use consistent structure across all endpoints
