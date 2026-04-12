---
created: 2025-11-05
modified: 2025-11-05
title: "Claude Code on the web"
url: https://docs.claude.com/en/docs/claude-code/claude-code-on-the-web
category: docs
subcategory: claude-code
description: "Run Claude Code tasks asynchronously on secure cloud infrastructure"
tags:
  - docs
  - claude-code
related:
  - '[[amazon-bedrock]]'
  - '[[analytics]]'
  - '[[checkpointing]]'
  - '[[cli-reference]]'
  - '[[common-workflows]]'
---

# Claude Code on the web

Run Claude Code tasks asynchronously on secure cloud infrastructure

> [!note]
> Claude Code on the web is currently in research preview.

## What is Claude Code on the web?

Claude Code on the web lets developers kick off Claude Code from the Claude app. This is perfect for:

* **Answering questions**: Ask about code architecture and how features are implemented
* **Bugfixes and routine tasks**: Well-defined tasks that don't require frequent steering
* **Parallel work**: Tackle multiple bug fixes in parallel
* **Repositories not on your local machine**: Work on code you don't have checked out locally
* **Backend changes**: Where Claude Code can write tests and then write code to pass those tests

Claude Code is also available on the Claude iOS app. This is perfect for:

* **On the go**: Kick off tasks while commuting or away from laptop
* **Monitoring**: Watch the trajectory and steer the agent's work

Developers can also move Claude Code sessions from the Claude app to their terminal to continue tasks locally.

## Who can use Claude Code on the web?

Claude Code on the web is available in research preview to:

* **Pro users**
* **Max users**

Coming soon to Team and Enterprise premium seat users.

## Getting started

1. Visit [claude.ai/code](https://claude.ai/code)
2. Connect your GitHub account
3. Install the Claude GitHub app in your repositories
4. Select your default environment
5. Submit your coding task
6. Review changes and create a pull request in GitHub

## How it works

When you start a task on Claude Code on the web:

1. **Repository cloning**: Your repository is cloned to an Anthropic-managed virtual machine
2. **Environment setup**: Claude prepares a secure cloud environment with your code
3. **Network configuration**: Internet access is configured based on your settings
4. **Task execution**: Claude analyzes code, makes changes, runs tests, and checks its work
5. **Completion**: You're notified when finished and can create a PR with the changes
6. **Results**: Changes are pushed to a branch, ready for pull request creation

## Moving tasks between web and terminal

### From web to terminal

After starting a task on the web:

1. Click the "Open in CLI" button
2. Paste and run the command in your terminal in a checkout of the repo
3. Any existing local changes will be stashed, and the remote session will be loaded
4. Continue working locally

## Cloud environment

### Default image

We build and maintain a universal image with common toolchains and language ecosystems pre-installed. This image includes:

* Popular programming languages and runtimes
* Common build tools and package managers
* Testing frameworks and linters

#### Checking available tools

To see what's pre-installed in your environment, ask Claude Code to run:

```bash  theme={null}
check-tools
```

This command displays:

* Programming languages and their versions
* Available package managers
* Installed development tools

#### Language-specific setups

The universal image includes pre-configured environments for:

* **Python**: Python 3.x with pip, poetry, and common scientific libraries
* **Node.js**: Latest LTS versions with npm, yarn, and pnpm
* **Java**: OpenJDK with Maven and Gradle
* **Go**: Latest stable version with module support
* **Rust**: Rust toolchain with cargo
* **C++**: GCC and Clang compilers

### Environment configuration

When you start a session in Claude Code on the web, here's what happens under the hood:

1. **Environment preparation**: We clone your repository and run any configured Claude hooks for initialization. The repo will be cloned with the default branch on your GitHub repo. If you would like to check out a specific branch, you can specify that in the prompt.

2. **Network configuration**: We configure internet access for the agent. Internet access is limited by default, but you can configure the environment to have no internet or full internet access based on your needs.

3. **Claude Code execution**: Claude Code runs to complete your task, writing code, running tests, and checking its work. You can guide and steer Claude throughout the session via the web interface. Claude respects context you've defined in your `CLAUDE.md`.

4. **Outcome**: When Claude completes its work, it will push the branch to remote. You will be able to create a PR for the branch.

> [!note]
> Claude operates entirely through the terminal and CLI tools available in the environment. It uses the pre-installed tools in the universal image and any additional tools you install through hooks or dependency management.

**To add a new environment:** Select the current environment to open the environment selector, and then select "Add environment". This will open a dialog where you can specify the environment name, network access level, and any environment variables you want to set.

**To update an existing environment:** Select the current environment, to the right of the environment name, and select the settings button. This will open a dialog where you can update the environment name, network access, and environment variables.

> [!note]
> Environment variables must be specified as key-value pairs, in [`.env` format](https://www.dotenv.org/). For example:
>
>   ```
>   API_KEY=your_api_key
>   DEBUG=true
>   ```

### Dependency management

Configure automatic dependency installation using [[hooks#sessionstart|SessionStart hooks]]. This can be configured in your repository's `.claude/settings.json` file:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

Create the corresponding script at `scripts/install_pkgs.sh`:

```bash  theme={null}
#!/bin/bash
npm install
pip install -r requirements.txt
exit 0
```

Make it executable: `chmod +x scripts/install_pkgs.sh`

#### Local vs remote execution

By default, all hooks execute both locally and in remote (web) environments. To run a hook only in one environment, check the `CLAUDE_CODE_REMOTE` environment variable in your hook script.

```bash  theme={null}
#!/bin/bash

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/claude-code-on-the-web)
