---
created: 2025-11-05
modified: 2025-11-05
title: "LLM gateway configuration"
url: https://docs.claude.com/en/docs/claude-code/llm-gateway
category: docs
subcategory: claude-code
description: "Learn how to configure Claude Code with LLM gateway solutions, including LiteLLM setup, authentication methods, and enterprise features like usage tracking and budget management."
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

# LLM gateway configuration

Learn how to configure Claude Code with LLM gateway solutions, including LiteLLM setup, authentication methods, and enterprise features like usage tracking and budget management.

LLM gateways provide a centralized proxy layer between Claude Code and model providers, offering:

* **Centralized authentication** - Single point for API key management
* **Usage tracking** - Monitor usage across teams and projects
* **Cost controls** - Implement budgets and rate limits
* **Audit logging** - Track all model interactions for compliance
* **Model routing** - Switch between providers without code changes

## LiteLLM configuration

> [!note]
> LiteLLM is a third-party proxy service. Anthropic doesn't endorse, maintain, or audit LiteLLM's security or functionality. This guide is provided for informational purposes and may become outdated. Use at your own discretion.

### Prerequisites

* Claude Code updated to the latest version
* LiteLLM Proxy Server deployed and accessible
* Access to Claude models through your chosen provider

### Basic LiteLLM setup

**Configure Claude Code**:

#### Authentication methods

##### Static API key

Simplest method using a fixed API key:

```bash  theme={null}

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/llm-gateway)
