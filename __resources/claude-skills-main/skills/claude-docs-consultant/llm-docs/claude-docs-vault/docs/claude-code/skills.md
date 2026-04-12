---
created: 2025-11-05
modified: 2025-11-05
title: "Agent Skills"
url: https://docs.claude.com/en/docs/claude-code/skills
category: docs
subcategory: claude-code
description: "Create, manage, and share Skills to extend Claude's capabilities in Claude Code."
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

# Agent Skills

Create, manage, and share Skills to extend Claude's capabilities in Claude Code.

This guide shows you how to create, use, and manage Agent Skills in Claude Code. Skills are modular capabilities that extend Claude's functionality through organized folders containing instructions, scripts, and resources.

## Prerequisites

* Claude Code version 1.0 or later
* Basic familiarity with [[quickstart|Claude Code]]

## What are Agent Skills?

Agent Skills package expertise into discoverable capabilities. Each Skill consists of a `SKILL.md` file with instructions that Claude reads when relevant, plus optional supporting files like scripts and templates.

**How Skills are invoked**: Skills are **model-invoked**—Claude autonomously decides when to use them based on your request and the Skill's description. This is different from slash commands, which are **user-invoked** (you explicitly type `/command` to trigger them).

**Benefits**:

* Extend Claude's capabilities for your specific workflows
* Share expertise across your team via git
* Reduce repetitive prompting
* Compose multiple Skills for complex tasks

Learn more in the [[overview|Agent Skills overview]].

> [!note]
> For a deep dive into the architecture and real-world applications of Agent Skills, read our engineering blog: [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).

## Create a Skill

Skills are stored as directories containing a `SKILL.md` file.

### Personal Skills

Personal Skills are available across all your projects. Store them in `~/.claude/skills/`:

```bash  theme={null}
mkdir -p ~/.claude/skills/my-skill-name
```

**Use personal Skills for**:

* Your individual workflows and preferences
* Experimental Skills you're developing
* Personal productivity tools

### Project Skills

Project Skills are shared with your team. Store them in `.claude/skills/` within your project:

```bash  theme={null}
mkdir -p .claude/skills/my-skill-name
```

**Use project Skills for**:

* Team workflows and conventions
* Project-specific expertise
* Shared utilities and scripts

Project Skills are checked into git and automatically available to team members.

### Plugin Skills

Skills can also come from [[plugins|Claude Code plugins]]. Plugins may bundle Skills that are automatically available when the plugin is installed. These Skills work the same way as personal and project Skills.

## Write SKILL.md

Create a `SKILL.md` file with YAML frontmatter and Markdown content:

```yaml  theme={null}
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/skills)
