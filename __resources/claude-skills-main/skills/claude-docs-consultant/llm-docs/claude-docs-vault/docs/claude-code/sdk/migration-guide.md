---
created: 2025-11-05
modified: 2025-11-05
title: "Migrate to Claude Agent SDK"
url: https://docs.claude.com/en/docs/claude-code/sdk/migration-guide
category: docs
subcategory: claude-code
description: "Guide for migrating the Claude Code TypeScript and Python SDKs to the Claude Agent SDK"
tags:
  - docs
  - claude-code
  - sdk
related:
  - '[[amazon-bedrock]]'
  - '[[analytics]]'
  - '[[checkpointing]]'
  - '[[claude-code-on-the-web]]'
  - '[[cli-reference]]'
---

# Migrate to Claude Agent SDK

Guide for migrating the Claude Code TypeScript and Python SDKs to the Claude Agent SDK

## Overview

The Claude Code SDK has been renamed to the **Claude Agent SDK** and its documentation has been reorganized. This change reflects the SDK's broader capabilities for building AI agents beyond just coding tasks.

## What's Changed

| Aspect                     | Old                            | New                              |
| :------------------------- | :----------------------------- | :------------------------------- |
| **Package Name (TS/JS)**   | `@anthropic-ai/claude-code`    | `@anthropic-ai/claude-agent-sdk` |
| **Python Package**         | `claude-code-sdk`              | `claude-agent-sdk`               |
| **Documentation Location** | Claude Code docs → SDK section | API Guide → Agent SDK section    |

> [!note]
> **Documentation Changes:** The Agent SDK documentation has moved from the Claude Code docs to the API Guide under a dedicated [[overview|Agent SDK]] section. The Claude Code docs now focus on the CLI tool and automation features.

## Migration Steps

### For TypeScript/JavaScript Projects

**1. Uninstall the old package:**

```bash  theme={null}
npm uninstall @anthropic-ai/claude-code
```

**2. Install the new package:**

```bash  theme={null}
npm install @anthropic-ai/claude-agent-sdk
```

**3. Update your imports:**

Change all imports from `@anthropic-ai/claude-code` to `@anthropic-ai/claude-agent-sdk`:

```typescript  theme={null}
// Before
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-code";

// After
import {
  query,
  tool,
  createSdkMcpServer,
} from "@anthropic-ai/claude-agent-sdk";
```

**4. Update package.json dependencies:**

If you have the package listed in your `package.json`, update it:

```json  theme={null}
// Before
{
  "dependencies": {
    "@anthropic-ai/claude-code": "^1.0.0"
  }
}

// After
{
  "dependencies": {
    "@anthropic-ai/claude-agent-sdk": "^0.1.0"
  }
}
```

That's it! No other code changes are required.

### For Python Projects

**1. Uninstall the old package:**

```bash  theme={null}
pip uninstall claude-code-sdk
```

**2. Install the new package:**

```bash  theme={null}
pip install claude-agent-sdk
```

**3. Update your imports:**

Change all imports from `claude_code_sdk` to `claude_agent_sdk`:

```python  theme={null}

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/sdk/migration-guide)
