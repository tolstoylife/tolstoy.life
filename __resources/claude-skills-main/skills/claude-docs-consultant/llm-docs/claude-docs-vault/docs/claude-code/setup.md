---
created: 2025-11-05
modified: 2025-11-05
title: "Set up Claude Code"
url: https://docs.claude.com/en/docs/claude-code/setup
category: docs
subcategory: claude-code
description: "Install, authenticate, and start using Claude Code on your development machine."
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

# Set up Claude Code

Install, authenticate, and start using Claude Code on your development machine.

## System requirements

* **Operating Systems**: macOS 10.15+, Ubuntu 20.04+/Debian 10+, or Windows 10+ (with WSL 1, WSL 2, or Git for Windows)
* **Hardware**: 4GB+ RAM
* **Software**: [Node.js 18+](https://nodejs.org/en/download) (only required for NPM installation)
* **Network**: Internet connection required for authentication and AI processing
* **Shell**: Works best in Bash, Zsh or Fish
* **Location**: [Anthropic supported countries](https://www.anthropic.com/supported-countries)

### Additional dependencies

* **ripgrep**: Usually included with Claude Code. If search functionality fails, see [[troubleshooting#search-and-discovery-issues|search troubleshooting]].

## Standard installation

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



> [!note]
> Some users may be automatically migrated to an improved installation method.

After the installation process completes, navigate to your project and start Claude Code:

```bash  theme={null}
cd your-awesome-project
claude
```

Claude Code offers the following authentication options:

1. **Claude Console**: The default option. Connect through the Claude Console and complete the OAuth process. Requires active billing at [console.anthropic.com](https://console.anthropic.com). A "Claude Code" workspace will be automatically created for usage tracking and cost management. Note that you cannot create API keys for the Claude Code workspace - it is dedicated exclusively for Claude Code usage.
2. **Claude App (with Pro or Max plan)**: Subscribe to Claude's [Pro or Max plan](https://claude.com/pricing) for a unified subscription that includes both Claude Code and the web interface. Get more value at the same price point while managing your account in one place. Log in with your Claude.ai account. During launch, choose the option that matches your subscription type.
3. **Enterprise platforms**: Configure Claude Code to use [[third-party-integrations|Amazon Bedrock or Google Vertex AI]] for enterprise deployments with your existing cloud infrastructure.

> [!note]
> Claude Code securely stores your credentials. See [Credential Management](https://docs.claude.com/en/docs/claude-code/iam#credential-management) for details.

## Windows setup

**Option 1: Claude Code within WSL**

* Both WSL 1 and WSL 2 are supported

**Option 2: Claude Code on native Windows with Git Bash**

* Requires [Git for Windows](https://git-scm.com/downloads/win)
* For portable Git installations, specify the path to your `bash.exe`:
  ```powershell  theme={null}
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Alternative installation methods

Claude Code offers multiple installation methods to suit different environments.

If you encounter any issues during installation, consult the [[troubleshooting#linux-permission-issues|troubleshooting guide]].

> [!tip]
> Run `claude doctor` after installation to check your installation type and version.

### Native installation options

The native installation is the recommended method and offers several benefits:

* One self-contained executable
* No Node.js dependency
* Improved auto-updater stability

If you have an existing installation of Claude Code, use `claude install` to migrate to the native binary installation.

For advanced installation options with the native installer:

**macOS, Linux, WSL:**

```bash  theme={null}

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/setup)
