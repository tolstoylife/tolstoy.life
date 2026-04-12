---
name: jwt-debugger
description: Debug and inspect JWT tokens. Decode headers and payloads, verify signatures, check expiration, and troubleshoot common JWT authentication issues without exposing secrets.
---

# JWT Debugger

Inspect, decode, and troubleshoot JWT tokens.

## When to Use

- Authentication failing and you suspect a JWT issue
- Need to inspect token claims (expiry, roles, issuer)
- Debugging token refresh flows
- Verifying JWT signature configuration

## Workflow

1. **Decode** — Split token into header.payload.signature, base64 decode
2. **Inspect header** — Check algorithm (RS256, HS256), key ID
3. **Inspect payload** — Check exp, iat, iss, aud, sub, custom claims
4. **Check expiry** — Is the token expired? Clock skew issues?
5. **Verify** — Match issuer, audience, and algorithm with server config

## Common Issues

- **"jwt expired"** — Token past exp time, need refresh
- **"invalid signature"** — Wrong secret/key, algorithm mismatch
- **"jwt malformed"** — Encoding issue, extra whitespace, truncated
- **"audience invalid"** — aud claim doesn't match expected value
- **Clock skew** — Server times out of sync, add leeway

## Safety

- NEVER log or display the full token in production
- Decode payload for inspection only — don't trust without verification
- Always verify signature server-side before trusting claims
