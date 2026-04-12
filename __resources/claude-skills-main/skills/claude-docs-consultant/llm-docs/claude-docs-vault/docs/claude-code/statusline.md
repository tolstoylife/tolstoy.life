---
created: 2025-11-05
modified: 2025-11-05
title: "Status line configuration"
url: https://docs.claude.com/en/docs/claude-code/statusline
category: docs
subcategory: claude-code
description: "Create a custom status line for Claude Code to display contextual information"
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

# Status line configuration

Create a custom status line for Claude Code to display contextual information

Make Claude Code your own with a custom status line that displays at the bottom of the Claude Code interface, similar to how terminal prompts (PS1) work in shells like Oh-my-zsh.

## Create a custom status line

You can either:

* Run `/statusline` to ask Claude Code to help you set up a custom status line. By default, it will try to reproduce your terminal's prompt, but you can provide additional instructions about the behavior you want to Claude Code, such as `/statusline show the model name in orange`

* Directly add a `statusLine` command to your `.claude/settings.json`:

```json  theme={null}
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0 // Optional: set to 0 to let status line go to edge
  }
}
```

## How it Works

* The status line is updated when the conversation messages update
* Updates run at most every 300ms
* The first line of stdout from your command becomes the status line text
* ANSI color codes are supported for styling your status line
* Claude Code passes contextual information about the current session (model, directories, etc.) as JSON to your script via stdin

## JSON Input Structure

Your status line command receives structured data via stdin in JSON format:

```json  theme={null}
{
  "hook_event_name": "Status",
  "session_id": "abc123...",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/current/working/directory",
  "model": {
    "id": "claude-opus-4-1",
    "display_name": "Opus"
  },
  "workspace": {
    "current_dir": "/current/working/directory",
    "project_dir": "/original/project/directory"
  },
  "version": "1.0.80",
  "output_style": {
    "name": "default"
  },
  "cost": {
    "total_cost_usd": 0.01234,
    "total_duration_ms": 45000,
    "total_api_duration_ms": 2300,
    "total_lines_added": 156,
    "total_lines_removed": 23
  }
}
```

## Example Scripts

### Simple Status Line

```bash  theme={null}
#!/bin/bash

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/statusline)
