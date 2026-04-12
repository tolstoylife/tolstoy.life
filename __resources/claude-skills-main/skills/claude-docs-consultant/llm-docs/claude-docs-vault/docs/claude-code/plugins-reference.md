---
created: 2025-11-05
modified: 2025-11-05
title: "Plugins reference"
url: https://docs.claude.com/en/docs/claude-code/plugins-reference
category: docs
subcategory: claude-code
description: "Complete technical reference for Claude Code plugin system, including schemas, CLI commands, and component specifications."
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

# Plugins reference

Complete technical reference for Claude Code plugin system, including schemas, CLI commands, and component specifications.

> [!tip]
> For hands-on tutorials and practical usage, see [[plugins|Plugins]]. For plugin management across teams and communities, see [[plugin-marketplaces|Plugin marketplaces]].

This reference provides complete technical specifications for the Claude Code plugin system, including component schemas, CLI commands, and development tools.

## Plugin components reference

This section documents the five types of components that plugins can provide.

### Commands

Plugins add custom slash commands that integrate seamlessly with Claude Code's command system.

**Location**: `commands/` directory in plugin root

**File format**: Markdown files with frontmatter

For complete details on plugin command structure, invocation patterns, and features, see [[slash-commands#plugin-commands|Plugin commands]].

### Agents

Plugins can provide specialized subagents for specific tasks that Claude can invoke automatically when appropriate.

**Location**: `agents/` directory in plugin root

**File format**: Markdown files describing agent capabilities

**Agent structure**:

```markdown  theme={null}
---
description: What this agent specializes in
capabilities: ["task1", "task2", "task3"]
---

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/plugins-reference)
