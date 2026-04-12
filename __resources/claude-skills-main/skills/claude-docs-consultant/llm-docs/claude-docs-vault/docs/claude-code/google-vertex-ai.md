---
created: 2025-11-05
modified: 2025-11-05
title: "Claude Code on Google Vertex AI"
url: https://docs.claude.com/en/docs/claude-code/google-vertex-ai
category: docs
subcategory: claude-code
description: "Learn about configuring Claude Code through Google Vertex AI, including setup, IAM configuration, and troubleshooting."
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

# Claude Code on Google Vertex AI

Learn about configuring Claude Code through Google Vertex AI, including setup, IAM configuration, and troubleshooting.

## Prerequisites

Before configuring Claude Code with Vertex AI, ensure you have:

* A Google Cloud Platform (GCP) account with billing enabled
* A GCP project with Vertex AI API enabled
* Access to desired Claude models (e.g., Claude Sonnet 4.5)
* Google Cloud SDK (`gcloud`) installed and configured
* Quota allocated in desired GCP region

## Region Configuration

Claude Code can be used with both Vertex AI [global](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai) and regional endpoints.

> [!note]
> Vertex AI may not support the Claude Code default models on all regions. You may need to switch to a [supported region or model](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models).

> [!note]
> Vertex AI may not support the Claude Code default models on global endpoints. You may need to switch to a regional endpoint or [supported model](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models).

## Setup

### 1. Enable Vertex AI API

Enable the Vertex AI API in your GCP project:

```bash  theme={null}

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/google-vertex-ai)
