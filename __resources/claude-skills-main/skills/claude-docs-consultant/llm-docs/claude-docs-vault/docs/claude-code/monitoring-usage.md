---
created: 2025-11-05
modified: 2025-11-05
title: "Monitoring"
url: https://docs.claude.com/en/docs/claude-code/monitoring-usage
category: docs
subcategory: claude-code
description: "Learn how to enable and configure OpenTelemetry for Claude Code."
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

# Monitoring

Learn how to enable and configure OpenTelemetry for Claude Code.

Claude Code supports OpenTelemetry (OTel) metrics and events for monitoring and observability.

All metrics are time series data exported via OpenTelemetry's standard metrics protocol, and events are exported via OpenTelemetry's logs/events protocol. It is the user's responsibility to ensure their metrics and logs backends are properly configured and that the aggregation granularity meets their monitoring requirements.

> [!note]
> OpenTelemetry support is currently in beta and details are subject to change.

## Quick Start

Configure OpenTelemetry using environment variables:

```bash  theme={null}

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/monitoring-usage)
