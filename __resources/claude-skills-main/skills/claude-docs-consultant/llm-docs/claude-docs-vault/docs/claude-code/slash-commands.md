---
created: 2025-11-05
modified: 2025-11-05
title: "Slash commands"
url: https://docs.claude.com/en/docs/claude-code/slash-commands
category: docs
subcategory: claude-code
description: "Control Claude's behavior during an interactive session with slash commands."
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

# Slash commands

Control Claude's behavior during an interactive session with slash commands.

## Built-in slash commands

| Command                   | Purpose                                                                                                                                      |
| :------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------- |
| `/add-dir`                | Add additional working directories                                                                                                           |
| `/agents`                 | Manage custom AI subagents for specialized tasks                                                                                             |
| `/bug`                    | Report bugs (sends conversation to Anthropic)                                                                                                |
| `/clear`                  | Clear conversation history                                                                                                                   |
| `/compact [instructions]` | Compact conversation with optional focus instructions                                                                                        |
| `/config`                 | Open the Settings interface (Config tab)                                                                                                     |
| `/cost`                   | Show token usage statistics (see [[costs#using-the-cost-command|cost tracking guide]] for subscription-specific details) |
| `/doctor`                 | Checks the health of your Claude Code installation                                                                                           |
| `/help`                   | Get usage help                                                                                                                               |
| `/init`                   | Initialize project with CLAUDE.md guide                                                                                                      |
| `/login`                  | Switch Anthropic accounts                                                                                                                    |
| `/logout`                 | Sign out from your Anthropic account                                                                                                         |
| `/mcp`                    | Manage MCP server connections and OAuth authentication                                                                                       |
| `/memory`                 | Edit CLAUDE.md memory files                                                                                                                  |
| `/model`                  | Select or change the AI model                                                                                                                |
| `/permissions`            | View or update [permissions](https://docs.claude.com/en/docs/claude-code/iam#configuring-permissions)                                                               |
| `/pr_comments`            | View pull request comments                                                                                                                   |
| `/review`                 | Request code review                                                                                                                          |
| `/sandbox`                | Enable sandboxed bash tool with filesystem and network isolation for safer, more autonomous execution                                        |
| `/rewind`                 | Rewind the conversation and/or code                                                                                                          |
| `/status`                 | Open the Settings interface (Status tab) showing version, model, account, and connectivity                                                   |
| `/terminal-setup`         | Install Shift+Enter key binding for newlines (iTerm2 and VSCode only)                                                                        |
| `/usage`                  | Show plan usage limits and rate limit status (subscription plans only)                                                                       |
| `/vim`                    | Enter vim mode for alternating insert and command modes                                                                                      |

## Custom slash commands

Custom slash commands allow you to define frequently-used prompts as Markdown files that Claude Code can execute. Commands are organized by scope (project-specific or personal) and support namespacing through directory structures.

### Syntax

```
/<command-name> [arguments]
```

#### Parameters

| Parameter        | Description                                                       |
| :--------------- | :---------------------------------------------------------------- |
| `<command-name>` | Name derived from the Markdown filename (without `.md` extension) |
| `[arguments]`    | Optional arguments passed to the command                          |

### Command types

#### Project commands

Commands stored in your repository and shared with your team. When listed in `/help`, these commands show "(project)" after their description.

**Location**: `.claude/commands/`

In the following example, we create the `/optimize` command:

```bash  theme={null}

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/slash-commands)
