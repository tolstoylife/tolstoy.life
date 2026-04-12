---
name: oauth-flow-builder
description: Implement OAuth 2.0 and OIDC authentication flows. Covers authorization code, PKCE, client credentials, and token refresh with proper security practices.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - WebFetch
  - WebSearch
---

# OAuth Flow Builder

Implement OAuth 2.0 authentication flows correctly.

## When to Use

- Adding "Sign in with Google/GitHub/etc." to an app
- Building API authentication with OAuth2
- Implementing machine-to-machine auth (client credentials)
- Debugging OAuth redirect loops or token issues

## Flows

| Flow | Use Case | Security Level |
|------|----------|---------------|
| Authorization Code + PKCE | SPAs, mobile apps | High |
| Authorization Code | Server-side web apps | High |
| Client Credentials | Service-to-service | High (no user) |
| Device Code | CLI tools, TVs | Medium |

## Workflow

1. **Choose flow** — Based on client type and security requirements
2. **Register app** — Get client_id, set redirect URIs
3. **Implement** — Auth URL → redirect → token exchange → refresh
4. **Store tokens** — Secure storage (httpOnly cookies, keychain, NOT localStorage)
5. **Handle refresh** — Silent refresh before expiry, handle revocation

## Security Checklist

- Always use PKCE for public clients (SPAs, mobile)
- Validate state parameter to prevent CSRF
- Use httpOnly, secure, sameSite cookies for web
- Never expose client_secret in frontend code
- Validate ID token claims (iss, aud, exp, nonce)
