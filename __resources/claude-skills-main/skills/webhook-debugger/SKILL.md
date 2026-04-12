---
name: webhook-debugger
description: Debug and test webhooks. Inspect payloads, verify signatures, simulate deliveries, handle retries, and troubleshoot common webhook integration issues.
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

# Webhook Debugger

Debug, test, and verify webhook integrations.

## When to Use

- Webhook events aren't arriving or processing correctly
- Need to verify webhook signature validation
- Testing webhook handlers locally (with ngrok/cloudflared)
- Setting up new webhook integrations
- Debugging payload format mismatches

## Workflow

1. **Inspect** — Log incoming webhook payload, headers, and method
2. **Verify signature** — Check HMAC/RSA signature against secret
3. **Test locally** — Set up tunnel (ngrok, cloudflared) for local development
4. **Simulate** — Send test webhook payloads to your endpoint
5. **Handle failures** — Implement idempotency, retry logic, dead letter queue

## Signature Verification Patterns

- **HMAC-SHA256** — Stripe, GitHub, Shopify
- **RSA** — Twilio, DocuSign
- **Timestamp + HMAC** — Slack, Svix
- Always verify before processing; reject invalid signatures with 401
