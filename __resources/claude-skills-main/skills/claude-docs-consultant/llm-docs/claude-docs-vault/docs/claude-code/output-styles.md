---
created: 2025-11-05
modified: 2025-11-05
title: "Output styles"
url: https://docs.claude.com/en/docs/claude-code/output-styles
category: docs
subcategory: claude-code
description: "Adapt Claude Code for uses beyond software engineering"
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

# Output styles

Adapt Claude Code for uses beyond software engineering

Output styles allow you to use Claude Code as any type of agent while keeping
its core capabilities, such as running local scripts, reading/writing files, and
tracking TODOs.

## Built-in output styles

Claude Code's **Default** output style is the existing system prompt, designed
to help you complete software engineering tasks efficiently.

There are two additional built-in output styles focused on teaching you the
codebase and how Claude operates:

* **Explanatory**: Provides educational "Insights" in between helping you
  complete software engineering tasks. Helps you understand implementation
  choices and codebase patterns.

* **Learning**: Collaborative, learn-by-doing mode where Claude will not only
  share "Insights" while coding, but also ask you to contribute small, strategic
  pieces of code yourself. Claude Code will add `TODO(human)` markers in your
  code for you to implement.

## How output styles work

Output styles directly modify Claude Code's system prompt.

* Non-default output styles exclude instructions specific to code generation and
  efficient output normally built into Claude Code (such as responding concisely
  and verifying code with tests).
* Instead, these output styles have their own custom instructions added to the
  system prompt.

## Change your output style

You can either:

* Run `/output-style` to access the menu and select your output style (this can
  also be accessed from the `/config` menu)

* Run `/output-style [style]`, such as `/output-style explanatory`, to directly
  switch to a style

These changes apply to the [[settings|local project level]]
and are saved in `.claude/settings.local.json`.

## Create a custom output style

To set up a new output style with Claude's help, run
`/output-style:new I want an output style that ...`

By default, output styles created through `/output-style:new` are saved as
markdown files at the user level in `~/.claude/output-styles` and can be used
across projects. They have the following structure:

```markdown  theme={null}
---
name: My Custom Style
description:
  A brief description of what this style does, to be displayed to the user
---

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/output-styles)
