---
created: 2025-11-05
modified: 2025-11-05
title: "Hooks reference"
url: https://docs.claude.com/en/docs/claude-code/hooks
category: docs
subcategory: claude-code
description: "This page provides reference documentation for implementing hooks in Claude Code."
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

# Hooks reference

This page provides reference documentation for implementing hooks in Claude Code.

> [!tip]
> For a quickstart guide with examples, see [[hooks-guide|Get started with Claude Code hooks]].

## Configuration

Claude Code hooks are configured in your [[settings|settings files]]:

* `~/.claude/settings.json` - User settings
* `.claude/settings.json` - Project settings
* `.claude/settings.local.json` - Local project settings (not committed)
* Enterprise managed policy settings

### Structure

Hooks are organized by matchers, where each matcher can have multiple hooks:

```json  theme={null}
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

* **matcher**: Pattern to match tool names, case-sensitive (only applicable for
  `PreToolUse` and `PostToolUse`)
  * Simple strings match exactly: `Write` matches only the Write tool
  * Supports regex: `Edit|Write` or `Notebook.*`
  * Use `*` to match all tools. You can also use empty string (`""`) or leave
    `matcher` blank.
* **hooks**: Array of hooks to execute when the pattern matches
  * `type`: Hook execution type - `"command"` for bash commands or `"prompt"` for LLM-based evaluation
  * `command`: (For `type: "command"`) The bash command to execute (can use `$CLAUDE_PROJECT_DIR` environment variable)
  * `prompt`: (For `type: "prompt"`) The prompt to send to the LLM for evaluation
  * `timeout`: (Optional) How long a hook should run, in seconds, before canceling that specific hook

For events like `UserPromptSubmit`, `Notification`, `Stop`, and `SubagentStop`
that don't use matchers, you can omit the matcher field:

```json  theme={null}
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/prompt-validator.py"
          }
        ]
      }
    ]
  }
}
```

### Project-Specific Hook Scripts

You can use the environment variable `CLAUDE_PROJECT_DIR` (only available when
Claude Code spawns the hook command) to reference scripts stored in your project,
ensuring they work regardless of Claude's current directory:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
          }
        ]
      }
    ]
  }
}
```

### Plugin hooks

[[plugins|Plugins]] can provide hooks that integrate seamlessly with your user and project hooks. Plugin hooks are automatically merged with your configuration when plugins are enabled.

**How plugin hooks work**:

* Plugin hooks are defined in the plugin's `hooks/hooks.json` file or in a file given by a custom path to the `hooks` field.
* When a plugin is enabled, its hooks are merged with user and project hooks
* Multiple hooks from different sources can respond to the same event
* Plugin hooks use the `${CLAUDE_PLUGIN_ROOT}` environment variable to reference plugin files

**Example plugin hook configuration**:

```json  theme={null}
{
  "description": "Automatic code formatting",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

> [!note]
> Plugin hooks use the same format as regular hooks with an optional `description` field to explain the hook's purpose.

> [!note]
> Plugin hooks run alongside your custom hooks. If multiple hooks match an event, they all execute in parallel.

**Environment variables for plugins**:

* `${CLAUDE_PLUGIN_ROOT}`: Absolute path to the plugin directory
* `${CLAUDE_PROJECT_DIR}`: Project root directory (same as for project hooks)
* All standard environment variables are available

See the [[plugins-reference#hooks|plugin components reference]] for details on creating plugin hooks.

## Prompt-Based Hooks

In addition to bash command hooks (`type: "command"`), Claude Code supports prompt-based hooks (`type: "prompt"`) that use an LLM to evaluate whether to allow or block an action. Prompt-based hooks are currently only supported for `Stop` and `SubagentStop` hooks, where they enable intelligent, context-aware decisions.

### How prompt-based hooks work

Instead of executing a bash command, prompt-based hooks:

1. Send the hook input and your prompt to a fast LLM (Haiku)
2. The LLM responds with structured JSON containing a decision
3. Claude Code processes the decision automatically

### Configuration

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
          }
        ]
      }
    ]
  }
}
```

**Fields:**

* `type`: Must be `"prompt"`
* `prompt`: The prompt text to send to the LLM
  * Use `$ARGUMENTS` as a placeholder for the hook input JSON
  * If `$ARGUMENTS` is not present, input JSON is appended to the prompt
* `timeout`: (Optional) Timeout in seconds (default: 30 seconds)

### Response schema

The LLM must respond with JSON containing:

```json  theme={null}
{
  "decision": "approve" | "block",
  "reason": "Explanation for the decision",
  "continue": false,  // Optional: stops Claude entirely
  "stopReason": "Message shown to user",  // Optional: custom stop message
  "systemMessage": "Warning or context"  // Optional: shown to user
}
```

**Response fields:**

* `decision`: `"approve"` allows the action, `"block"` prevents it
* `reason`: Explanation shown to Claude when decision is `"block"`
* `continue`: (Optional) If `false`, stops Claude's execution entirely
* `stopReason`: (Optional) Message shown when `continue` is false
* `systemMessage`: (Optional) Additional message shown to the user

### Supported hook events

Prompt-based hooks work with any hook event, but are most useful for:

* **Stop**: Intelligently decide if Claude should continue working
* **SubagentStop**: Evaluate if a subagent has completed its task
* **UserPromptSubmit**: Validate user prompts with LLM assistance
* **PreToolUse**: Make context-aware permission decisions

### Example: Intelligent Stop hook

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"decision\": \"approve\" or \"block\", \"reason\": \"your explanation\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Example: SubagentStop with custom logic

```json  theme={null}
{
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if this subagent should stop. Input: $ARGUMENTS\n\nCheck if:\n- The subagent completed its assigned task\n- Any errors occurred that need fixing\n- Additional context gathering is needed\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}"
          }
        ]
      }
    ]
  }
}
```

### Comparison with bash command hooks

| Feature               | Bash Command Hooks      | Prompt-Based Hooks             |
| --------------------- | ----------------------- | ------------------------------ |
| **Execution**         | Runs bash script        | Queries LLM                    |
| **Decision logic**    | You implement in code   | LLM evaluates context          |
| **Setup complexity**  | Requires script file    | Just configure prompt          |
| **Context awareness** | Limited to script logic | Natural language understanding |
| **Performance**       | Fast (local execution)  | Slower (API call)              |
| **Use case**          | Deterministic rules     | Context-aware decisions        |

### Best practices

* **Be specific in prompts**: Clearly state what you want the LLM to evaluate
* **Include decision criteria**: List the factors the LLM should consider
* **Test your prompts**: Verify the LLM makes correct decisions for your use cases
* **Set appropriate timeouts**: Default is 30 seconds, adjust if needed
* **Use for complex decisions**: Bash hooks are better for simple, deterministic rules

See the [[plugins-reference#hooks|plugin components reference]] for details on creating plugin hooks.

## Hook Events

### PreToolUse

Runs after Claude creates tool parameters and before processing the tool call.

**Common matchers:**

* `Task` - Subagent tasks (see [[sub-agents|subagents documentation]])
* `Bash` - Shell commands
* `Glob` - File pattern matching
* `Grep` - Content search
* `Read` - File reading
* `Edit` - File editing
* `Write` - File writing
* `WebFetch`, `WebSearch` - Web operations

### PostToolUse

Runs immediately after a tool completes successfully.

Recognizes the same matcher values as PreToolUse.

### Notification

Runs when Claude Code sends notifications. Notifications are sent when:

1. Claude needs your permission to use a tool. Example: "Claude needs your
   permission to use Bash"
2. The prompt input has been idle for at least 60 seconds. "Claude is waiting
   for your input"

### UserPromptSubmit

Runs when the user submits a prompt, before Claude processes it. This allows you
to add additional context based on the prompt/conversation, validate prompts, or
block certain types of prompts.

### Stop

Runs when the main Claude Code agent has finished responding. Does not run if
the stoppage occurred due to a user interrupt.

### SubagentStop

Runs when a Claude Code subagent (Task tool call) has finished responding.

### PreCompact

Runs before Claude Code is about to run a compact operation.

**Matchers:**

* `manual` - Invoked from `/compact`
* `auto` - Invoked from auto-compact (due to full context window)

### SessionStart

Runs when Claude Code starts a new session or resumes an existing session (which
currently does start a new session under the hood). Useful for loading in
development context like existing issues or recent changes to your codebase, installing dependencies, or setting up environment variables.

**Matchers:**

* `startup` - Invoked from startup
* `resume` - Invoked from `--resume`, `--continue`, or `/resume`
* `clear` - Invoked from `/clear`
* `compact` - Invoked from auto or manual compact.

#### Persisting environment variables

SessionStart hooks have access to the `CLAUDE_ENV_FILE` environment variable, which provides a file path where you can persist environment variables for subsequent bash commands.

**Example: Setting individual environment variables**

```bash  theme={null}
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export API_KEY=your-api-key' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

**Example: Persisting all environment changes from the hook**

When your setup modifies the environment (e.g., `nvm use`), capture and persist all changes by diffing the environment:

```bash  theme={null}
#!/bin/bash

ENV_BEFORE=$(export -p | sort)

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/hooks)
