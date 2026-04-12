---
name: ssl-cert-manager
description: Manage SSL/TLS certificates. Generate self-signed certs for development, debug certificate chain issues, check expiration dates, and configure HTTPS for common web servers.
---

# SSL/TLS Certificate Manager

Manage certificates for development and production.

## When to Use

- Need self-signed certs for local HTTPS development
- Certificate errors in browser or API calls
- Checking certificate expiration across services
- Configuring HTTPS on nginx, Apache, or Node.js
- Debugging certificate chain issues

## Workflow

1. **Diagnose** — Check current cert status (openssl s_client, curl -vI)
2. **Generate** — Self-signed certs with proper SANs for development
3. **Configure** — Set up HTTPS in web server or application
4. **Verify chain** — Ensure intermediate certs are properly bundled
5. **Monitor** — Check expiration dates, set up renewal reminders

## Common Tasks

- Generate dev CA + signed cert (trusted locally via Keychain/certutil)
- Create CSR for production certificate
- Convert between formats (PEM, DER, PKCS12, PFX)
- Debug "certificate not trusted" errors
- Configure HSTS, OCSP stapling
