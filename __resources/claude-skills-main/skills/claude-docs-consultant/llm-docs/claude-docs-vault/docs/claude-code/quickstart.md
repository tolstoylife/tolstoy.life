---
created: 2025-11-05
modified: 2025-11-05
title: "Quickstart"
url: https://docs.claude.com/en/docs/claude-code/quickstart
category: docs
subcategory: claude-code
description: "Welcome to Claude Code!"
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

# Quickstart

Welcome to Claude Code!

This quickstart guide will have you using AI-powered coding assistance in just a few minutes. By the end, you'll understand how to use Claude Code for common development tasks.

## Before you begin

Make sure you have:

* A terminal or command prompt open
* A code project to work with
* A [Claude.ai](https://claude.ai) (recommended) or [Claude Console](https://console.anthropic.com/) account

## Step 1: Install Claude Code

To install Claude Code, use one of the following methods:



**Native Install (Recommended)**

**Homebrew (macOS, Linux):**

    ```sh  theme={null}
    brew install --cask claude-code
    ```

    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```


  
**NPM**

If you have [Node.js 18 or newer installed](https://nodejs.org/en/download/):

    ```sh  theme={null}
    npm install -g @anthropic-ai/claude-code
    ```



## Step 2: Log in to your account

Claude Code requires an account to use. When you start an interactive session with the `claude` command, you'll need to log in:

```bash  theme={null}
claude

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/quickstart)
