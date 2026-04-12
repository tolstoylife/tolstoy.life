---
name: cors-troubleshooter
description: Diagnose and fix CORS (Cross-Origin Resource Sharing) issues. Explains preflight requests, configures proper headers, and handles credentials, wildcards, and complex CORS scenarios.
---

# CORS Troubleshooter

Fix Cross-Origin Resource Sharing errors.

## When to Use

- Browser console shows "blocked by CORS policy"
- Preflight OPTIONS requests failing
- Credentials (cookies) not being sent cross-origin
- Need to configure CORS on a new API

## Common Errors and Fixes

- **"No 'Access-Control-Allow-Origin'"** — Server not sending CORS headers
- **"not in allowed list"** — Origin mismatch (check protocol, port, subdomain)
- **"Preflight response not OK"** — OPTIONS handler missing or returning wrong status
- **"Credentials flag is true but Allow-Origin is *"** — Can't use wildcard with credentials
- **"Method not allowed"** — Missing Access-Control-Allow-Methods header

## Workflow

1. **Read the error** — Browser error message tells you exactly what's wrong
2. **Check request** — Is it simple or does it trigger preflight?
3. **Inspect response** — What CORS headers is the server returning?
4. **Fix server** — Add proper CORS middleware/headers
5. **Verify** — Test with actual browser request (not curl — curl ignores CORS)

## Key Rules

- CORS is enforced by browsers only, not by servers or curl
- Preflight triggered by: custom headers, non-simple methods, non-simple content-types
- Credentials require explicit origin (no wildcard) + Allow-Credentials: true
