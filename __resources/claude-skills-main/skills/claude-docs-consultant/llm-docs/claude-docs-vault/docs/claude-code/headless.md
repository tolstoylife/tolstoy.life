---
created: 2025-11-05
modified: 2025-11-05
title: "Headless mode"
url: https://docs.claude.com/en/docs/claude-code/headless
category: docs
subcategory: claude-code
description: "Run Claude Code programmatically without interactive UI"
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

# Headless mode

Run Claude Code programmatically without interactive UI

## Overview

The headless mode allows you to run Claude Code programmatically from command line scripts and automation tools without any interactive UI.

## Basic usage

The primary command-line interface to Claude Code is the `claude` command. Use the `--print` (or `-p`) flag to run in non-interactive mode and print the final result:

```bash  theme={null}
claude -p "Stage my changes and write a set of commits for them" \
  --allowedTools "Bash,Read" \
  --permission-mode acceptEdits
```

## Configuration Options

Headless mode leverages all the CLI options available in Claude Code. Here are the key ones for automation and scripting:

| Flag                       | Description                                                                                            | Example                                                                                                                   |
| :------------------------- | :----------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `--print`, `-p`            | Run in non-interactive mode                                                                            | `claude -p "query"`                                                                                                       |
| `--output-format`          | Specify output format (`text`, `json`, `stream-json`)                                                  | `claude -p --output-format json`                                                                                          |
| `--resume`, `-r`           | Resume a conversation by session ID                                                                    | `claude --resume abc123`                                                                                                  |
| `--continue`, `-c`         | Continue the most recent conversation                                                                  | `claude --continue`                                                                                                       |
| `--verbose`                | Enable verbose logging                                                                                 | `claude --verbose`                                                                                                        |
| `--append-system-prompt`   | Append to system prompt (only with `--print`)                                                          | `claude --append-system-prompt "Custom instruction"`                                                                      |
| `--allowedTools`           | Space-separated list of allowed tools, or <br /><br /> string of comma-separated list of allowed tools | `claude --allowedTools mcp__slack mcp__filesystem`<br /><br />`claude --allowedTools "Bash(npm install),mcp__filesystem"` |
| `--disallowedTools`        | Space-separated list of denied tools, or <br /><br /> string of comma-separated list of denied tools   | `claude --disallowedTools mcp__splunk mcp__github`<br /><br />`claude --disallowedTools "Bash(git commit),mcp__github"`   |
| `--mcp-config`             | Load MCP servers from a JSON file                                                                      | `claude --mcp-config servers.json`                                                                                        |
| `--permission-prompt-tool` | MCP tool for handling permission prompts (only with `--print`)                                         | `claude --permission-prompt-tool mcp__auth__prompt`                                                                       |

For a complete list of CLI options and features, see the [[cli-reference|CLI reference]] documentation.

## Multi-turn conversations

For multi-turn conversations, you can resume conversations or continue from the most recent session:

```bash  theme={null}

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/headless)
