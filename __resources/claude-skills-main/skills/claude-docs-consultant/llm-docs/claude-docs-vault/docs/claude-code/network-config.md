---
created: 2025-11-05
modified: 2025-11-05
title: "Enterprise network configuration"
url: https://docs.claude.com/en/docs/claude-code/network-config
category: docs
subcategory: claude-code
description: "Configure Claude Code for enterprise environments with proxy servers, custom Certificate Authorities (CA), and mutual Transport Layer Security (mTLS) authentication."
tags:
  - docs
  - claude-code
related:
  - '[[amazon-bedrock]]'
  - '[[analytics]]'
  - '[[checkpointing]]'
  - '[[claude-code-on-the-web]]'
  - '[[cli-reference]]'
---

# Enterprise network configuration

Configure Claude Code for enterprise environments with proxy servers, custom Certificate Authorities (CA), and mutual Transport Layer Security (mTLS) authentication.

Claude Code supports various enterprise network and security configurations through environment variables. This includes routing traffic through corporate proxy servers, trusting custom Certificate Authorities (CA), and authenticating with mutual Transport Layer Security (mTLS) certificates for enhanced security.

> [!note]
> All environment variables shown on this page can also be configured in [[settings|`settings.json`]].

## Proxy configuration

### Environment variables

Claude Code respects standard proxy environment variables:

```bash  theme={null}

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/network-config)
