---
created: 2025-11-05
modified: 2025-11-05
title: "Claude Code overview"
url: https://docs.claude.com/en/docs/claude-code/overview
category: docs
subcategory: claude-code
description: "Learn about Claude Code, Anthropic's agentic coding tool that lives in your terminal and helps you turn ideas into code faster than ever before."
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

# Claude Code overview

Learn about Claude Code, Anthropic's agentic coding tool that lives in your terminal and helps you turn ideas into code faster than ever before.

## Get started in 30 seconds

Prerequisites:

* A [Claude.ai](https://claude.ai) (recommended) or [Claude Console](https://console.anthropic.com/) account

**Install Claude Code:**



**macOS/Linux**

```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```


  
**Homebrew**

```bash  theme={null}
    brew install --cask claude-code
    ```


  
**Windows**

```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```


  
**NPM**

```bash  theme={null}
    npm install -g @anthropic-ai/claude-code
    ```

    Requires [Node.js 18+](https://nodejs.org/en/download/)



**Start using Claude Code:**

```bash  theme={null}
cd your-project
claude
```

You'll be prompted to log in on first use. That's it! [[quickstart|Continue with Quickstart (5 mins) →]]

> [!tip]
> See [[setup|advanced setup]] for installation options or [[troubleshooting|troubleshooting]] if you hit issues.

> [!note]
> **New VS Code Extension (Beta)**: Prefer a graphical interface? Our new [[vs-code|VS Code extension]] provides an easy-to-use native IDE experience without requiring terminal familiarity. Simply install from the marketplace and start coding with Claude directly in your sidebar.

## What Claude Code does for you

* **Build features from descriptions**: Tell Claude what you want to build in plain English. It will make a plan, write the code, and ensure it works.
* **Debug and fix issues**: Describe a bug or paste an error message. Claude Code will analyze your codebase, identify the problem, and implement a fix.
* **Navigate any codebase**: Ask anything about your team's codebase, and get a thoughtful answer back. Claude Code maintains awareness of your entire project structure, can find up-to-date information from the web, and with [[mcp|MCP]] can pull from external datasources like Google Drive, Figma, and Slack.
* **Automate tedious tasks**: Fix fiddly lint issues, resolve merge conflicts, and write release notes. Do all this in a single command from your developer machines, or automatically in CI.

## Why developers love Claude Code

* **Works in your terminal**: Not another chat window. Not another IDE. Claude Code meets you where you already work, with the tools you already love.
* **Takes action**: Claude Code can directly edit files, run commands, and create commits. Need more? [[mcp|MCP]] lets Claude read your design docs in Google Drive, update your tickets in Jira, or use *your* custom developer tooling.
* **Unix philosophy**: Claude Code is composable and scriptable. `tail -f app.log | claude -p "Slack me if you see any anomalies appear in this log stream"` *works*. Your CI can run `claude -p "If there are new text strings, translate them into French and raise a PR for @lang-fr-team to review"`.
* **Enterprise-ready**: Use the Claude API, or host on AWS or GCP. Enterprise-grade [[security|security]], [[data-usage|privacy]], and [compliance](https://trust.anthropic.com/) is built-in.

## Next steps


> [!info] Quickstart
> See Claude Code in action with practical examples

  > [!info] Common workflows
> Step-by-step guides for common workflows

  > [!info] Troubleshooting
> Solutions for common issues with Claude Code

  > [!info] IDE setup
> Add Claude Code to your IDE


## Additional resources


> [!info] Build with the Agent SDK
> Create custom AI agents with the Claude Agent SDK

  > [!info] Host on AWS or GCP
> Configure Claude Code with Amazon Bedrock or Google Vertex AI

  > [!info] Settings
> Customize Claude Code for your workflow

  > [!info] Commands
> Learn about CLI commands and controls

  > [!info] Reference implementation
> Clone our development container reference implementation

  > [!info] Security
> Discover Claude Code's safeguards and best practices for safe usage

  > [!info] Privacy and data usage
> Understand how Claude Code handles your data


---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/overview)
