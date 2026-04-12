---
created: 2025-11-05
modified: 2025-11-05
title: "Prompt engineering overview"
url: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview
category: docs
subcategory: build-with-claude
tags:
  - docs
  - build-with-claude
  - prompt
related:
  - '[[batch-processing]]'
  - '[[citations]]'
  - '[[context-editing]]'
  - '[[context-windows]]'
  - '[[embeddings]]'
---

# Prompt engineering overview

> [!note]
> While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [[extended-thinking-tips|here]].

## Before prompt engineering

This guide assumes that you have:

1. A clear definition of the success criteria for your use case
2. Some ways to empirically test against those criteria
3. A first draft prompt you want to improve

If not, we highly suggest you spend time establishing that first. Check out [[define-success|Define your success criteria]] and [[develop-tests|Create strong empirical evaluations]] for tips and guidance.

> [!info] Prompt generator
> Don't have a first draft prompt? Try the prompt generator in the Claude Console!

***

## When to prompt engineer

This guide focuses on success criteria that are controllable through prompt engineering.
Not every success criteria or failing eval is best solved by prompt engineering. For example, latency and cost can be sometimes more easily improved by selecting a different model.

> [!info]- Prompting vs. finetuning
> Prompt engineering is far faster than other methods of model behavior control, such as finetuning, and can often yield leaps in performance in far less time. Here are some reasons to consider prompt engineering over finetuning:<br />
>
>   * **Resource efficiency**: Fine-tuning requires high-end GPUs and large memory, while prompt engineering only needs text input, making it much more resource-friendly.
>   * **Cost-effectiveness**: For cloud-based AI services, fine-tuning incurs significant costs. Prompt engineering uses the base model, which is typically cheaper.
>   * **Maintaining model updates**: When providers update models, fine-tuned versions might need retraining. Prompts usually work across versions without changes.
>   * **Time-saving**: Fine-tuning can take hours or even days. In contrast, prompt engineering provides nearly instantaneous results, allowing for quick problem-solving.
>   * **Minimal data needs**: Fine-tuning needs substantial task-specific, labeled data, which can be scarce or expensive. Prompt engineering works with few-shot or even zero-shot learning.
>   * **Flexibility & rapid iteration**: Quickly try various approaches, tweak prompts, and see immediate results. This rapid experimentation is difficult with fine-tuning.
>   * **Domain adaptation**: Easily adapt models to new domains by providing domain-specific context in prompts, without retraining.
>   * **Comprehension improvements**: Prompt engineering is far more effective than finetuning at helping models better understand and utilize external content such as retrieved documents
>   * **Preserves general knowledge**: Fine-tuning risks catastrophic forgetting, where the model loses general knowledge. Prompt engineering maintains the model's broad capabilities.
>   * **Transparency**: Prompts are human-readable, showing exactly what information the model receives. This transparency aids in understanding and debugging.

***

## How to prompt engineer

The prompt engineering pages in this section have been organized from most broadly effective techniques to more specialized techniques. When troubleshooting performance, we suggest you try these techniques in order, although the actual impact of each technique will depend on your use case.

1. [[prompt-generator|Prompt generator]]
2. [[be-clear-and-direct|Be clear and direct]]
3. [[multishot-prompting|Use examples (multishot)]]
4. [[chain-of-thought|Let Claude think (chain of thought)]]
5. [[use-xml-tags|Use XML tags]]
6. [[system-prompts|Give Claude a role (system prompts)]]
7. [[prefill-claudes-response|Prefill Claude's response]]
8. [[chain-prompts|Chain complex prompts]]
9. [[long-context-tips|Long context tips]]

***

## Prompt engineering tutorial

If you're an interactive learner, you can dive into our interactive tutorials instead!


> [!info] GitHub prompting tutorial
> An example-filled tutorial that covers the prompt engineering concepts found in our docs.

  > [!info] Google Sheets prompting tutorial
> A lighter weight version of our prompt engineering tutorial via an interactive spreadsheet.


---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)
