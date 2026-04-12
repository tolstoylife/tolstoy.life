---
created: 2025-11-05
modified: 2025-11-05
title: "Reducing latency"
url: https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-latency
category: docs
subcategory: test-and-evaluate
tags:
  - docs
  - test-and-evaluate
related:
  - '[[define-success]]'
  - '[[develop-tests]]'
  - '[[eval-tool]]'
  - '[[handle-streaming-refusals]]'
  - '[[increase-consistency]]'
---

# Reducing latency

Latency refers to the time it takes for the model to process a prompt and and generate an output. Latency can be influenced by various factors, such as the size of the model, the complexity of the prompt, and the underlying infrastructure supporting the model and point of interaction.

> [!note]
> It's always better to first engineer a prompt that works well without model or prompt constraints, and then try latency reduction strategies afterward. Trying to reduce latency prematurely might prevent you from discovering what top performance looks like.

***

## How to measure latency

When discussing latency, you may come across several terms and measurements:

* **Baseline latency**: This is the time taken by the model to process the prompt and generate the response, without considering the input and output tokens per second. It provides a general idea of the model's speed.
* **Time to first token (TTFT)**: This metric measures the time it takes for the model to generate the first token of the response, from when the prompt was sent. It's particularly relevant when you're using streaming (more on that later) and want to provide a responsive experience to your users.

For a more in-depth understanding of these terms, check out our [[glossary|glossary]].

***

## How to reduce latency

### 1. Choose the right model

One of the most straightforward ways to reduce latency is to select the appropriate model for your use case. Anthropic offers a [[overview|range of models]] with different capabilities and performance characteristics. Consider your specific requirements and choose the model that best fits your needs in terms of speed and output quality.

For speed-critical applications, **Claude Haiku 4.5** offers the fastest response times while maintaining high intelligence:

```python  theme={null}
import anthropic

client = anthropic.Anthropic()

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-latency)
