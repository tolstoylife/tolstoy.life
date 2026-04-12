---
created: 2025-11-05
modified: 2025-11-05
title: "Improve a prompt"
url: https://docs.claude.com/en/api/prompt-tools-improve
category: api
description: "Create a new-and-improved prompt guided by feedback"
tags:
  - api
  - tool
  - prompt
related:
  - '[[get-api-key]]'
  - '[[list-api-keys]]'
  - '[[update-api-key]]'
  - '[[get-claude-code-usage-report]]'
  - '[[create-invite]]'
---

# Improve a prompt

post /v1/experimental/improve_prompt
Create a new-and-improved prompt guided by feedback

> [!tip]
> The prompt tools APIs are in a closed research preview. [Request to join the closed research preview](https://forms.gle/LajXBafpsf1SuJHp7).

## Before you begin

The prompt tools are a set of APIs to generate and improve prompts. Unlike our other APIs, this is an experimental API: you'll need to request access, and it doesn't have the same level of commitment to long-term support as other APIs.

These APIs are similar to what's available in the [Anthropic Workbench](https://console.anthropic.com/workbench), and are intended for use by other prompt engineering platforms and playgrounds.

## Getting started with the prompt improver

To use the prompt generation API, you'll need to:

1. Have joined the closed research preview for the prompt tools APIs
2. Use the API directly, rather than the SDK
3. Add the beta header `prompt-tools-2025-04-02`

> [!tip]
> This API is not available in the SDK

## Improve a prompt

---

**Source:** [Official Documentation](https://docs.claude.com/en/api/prompt-tools-improve)
