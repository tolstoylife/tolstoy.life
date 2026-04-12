---
created: 2025-11-05
modified: 2025-11-05
title: "Enterprise deployment overview"
url: https://docs.claude.com/en/docs/claude-code/third-party-integrations
category: docs
subcategory: claude-code
description: "Learn how Claude Code can integrate with various third-party services and infrastructure to meet enterprise deployment requirements."
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

# Enterprise deployment overview

Learn how Claude Code can integrate with various third-party services and infrastructure to meet enterprise deployment requirements.

This page provides an overview of available deployment options and helps you choose the right configuration for your organization.

## Provider comparison

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Anthropic</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Regions</td>
      <td>Supported [countries](https://www.anthropic.com/supported-countries)</td>
      <td>Multiple AWS [regions](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)</td>
      <td>Multiple GCP [regions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)</td>
    </tr>

    <tr>
      <td>Prompt caching</td>
      <td>Enabled by default</td>
      <td>Enabled by default</td>
      <td>Enabled by default</td>
    </tr>

    <tr>
      <td>Authentication</td>
      <td>API key</td>
      <td>AWS credentials (IAM)</td>
      <td>GCP credentials (OAuth/Service Account)</td>
    </tr>

    <tr>
      <td>Cost tracking</td>
      <td>Dashboard</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
    </tr>

    <tr>
      <td>Enterprise features</td>
      <td>Teams, usage monitoring</td>
      <td>IAM policies, CloudTrail</td>
      <td>IAM roles, Cloud Audit Logs</td>
    </tr>
  </tbody>
</table>

## Cloud providers


> [!info] Amazon Bedrock
> Use Claude models through AWS infrastructure with IAM-based authentication and AWS-native monitoring

  > [!info] Google Vertex AI
> Access Claude models via Google Cloud Platform with enterprise-grade security and compliance


## Corporate infrastructure


> [!info] Enterprise Network
> Configure Claude Code to work with your organization's proxy servers and SSL/TLS requirements

  > [!info] LLM Gateway
> Deploy centralized model access with usage tracking, budgeting, and audit logging


## Configuration overview

Claude Code supports flexible configuration options that allow you to combine different providers and infrastructure:

> [!note]
> Understand the difference between:
>
>   * **Corporate proxy**: An HTTP/HTTPS proxy for routing traffic (set via `HTTPS_PROXY` or `HTTP_PROXY`)
>   * **LLM Gateway**: A service that handles authentication and provides provider-compatible endpoints (set via `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL`, or `ANTHROPIC_VERTEX_BASE_URL`)
>
>   Both configurations can be used in tandem.

### Using Bedrock with corporate proxy

Route Bedrock traffic through a corporate HTTP/HTTPS proxy:

```bash  theme={null}

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/third-party-integrations)
