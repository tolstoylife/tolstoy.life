---
created: 2025-11-05
modified: 2025-11-05
title: "Model configuration"
url: https://docs.claude.com/en/docs/claude-code/model-config
category: docs
subcategory: claude-code
description: "Learn about the Claude Code model configuration, including model aliases like `opusplan`"
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

# Model configuration

Learn about the Claude Code model configuration, including model aliases like `opusplan`

## Available models

For the `model` setting in Claude Code, you can either configure:

* A **model alias**
* A full **[[overview#model-names|model name]]**
* For Bedrock, an ARN

### Model aliases

Model aliases provide a convenient way to select model settings without
remembering exact version numbers:

| Model alias      | Behavior                                                                                                                                         |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **`default`**    | Recommended model setting, depending on your account type                                                                                        |
| **`sonnet`**     | Uses the latest Sonnet model (currently Sonnet 4.5) for daily coding tasks                                                                       |
| **`opus`**       | Uses Opus model (currently Opus 4.1) for specialized complex reasoning tasks                                                                     |
| **`haiku`**      | Uses the fast and efficient Haiku model for simple tasks                                                                                         |
| **`sonnet[1m]`** | Uses Sonnet with a [[context-windows#1m-token-context-window|1 million token context window]] window for long sessions |
| **`opusplan`**   | Special mode that uses `opus` during plan mode, then switches to `sonnet` for execution                                                          |

### Setting your model

You can configure your model in several ways, listed in order of priority:

1. **During session** - Use `/model <alias|name>` to switch models mid-session
2. **At startup** - Launch with `claude --model <alias|name>`
3. **Environment variable** - Set `ANTHROPIC_MODEL=<alias|name>`
4. **Settings** - Configure permanently in your settings file using the `model`
   field.

Example usage:

```bash  theme={null}

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/model-config)
