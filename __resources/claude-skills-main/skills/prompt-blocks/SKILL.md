---
name: "prompt-blocks"
description: "Use when building or improving system prompts for any LLM agent — provides copy-paste-ready prompt blocks for tool persistence, verification, completeness, research, citation discipline, verbosity control, and other agentic behaviors. Model-agnostic: works with Claude, OpenAI, Ollama, and any instruction-following LLM."
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - WebFetch
  - WebSearch
---

# Prompt Blocks

A library of battle-tested, model-agnostic prompt blocks for agentic LLM workflows. Each block is a self-contained XML-tagged instruction set you can drop into any system prompt.

Derived from OpenAI's GPT-5.4 prompting upgrade guide (Apache 2.0) and generalized for cross-model use.

## When to use

- Building or tuning system prompts for agents, assistants, or multi-agent systems
- Diagnosing regressions in completeness, persistence, citation quality, or verbosity after a model swap
- Adding guardrails to tool-heavy, research-heavy, or long-running workflows

## Usage principles

1. **Start lean.** Don't add all blocks. Add only what an observed regression or requirement demands.
2. **One or two blocks first.** Test before layering more. Remove blocks that aren't earning their keep.
3. **Combine by workflow type.** See the profiles section for recommended combos.
4. **These are additive.** Drop them into an existing system prompt — they don't replace your core instructions.

## Block catalog

### Tool use and persistence

#### `tool_persistence_rules`

Problem: Model stops calling tools too early, sacrificing completeness for efficiency.

```text
<tool_persistence_rules>
- Use tools whenever they materially improve correctness, completeness, or grounding.
- Do not stop early just to save tool calls.
- Keep calling tools until:
  (1) the task is complete, and
  (2) verification passes.
- If a tool returns empty or partial results, retry with a different strategy.
</tool_persistence_rules>
```

#### `dependency_checks`

Problem: Model skips prerequisite lookups and jumps to the final action.

```text
<dependency_checks>
- Before taking an action, check whether prerequisite discovery, lookup, or memory retrieval is required.
- Do not skip prerequisite steps just because the intended final action seems obvious.
- If a later step depends on the output of an earlier one, resolve that dependency first.
</dependency_checks>
```

#### `parallel_tool_calling`

Problem: Independent lookups run sequentially, wasting wall-clock time.

```text
<parallel_tool_calling>
- When multiple retrieval or lookup steps are independent, prefer parallel tool calls to reduce wall-clock time.
- Do not parallelize steps with prerequisite dependencies or where one result determines the next action.
- After parallel retrieval, pause to synthesize before making more calls.
- Prefer selective parallelism: parallelize independent evidence gathering, not speculative or redundant tool use.
</parallel_tool_calling>
```

#### `terminal_tool_hygiene`

Problem: Coding/terminal agents misuse shell commands or skip verification.

```text
<terminal_tool_hygiene>
- Only run shell commands through the terminal tool.
- Never try to "run" tool names as shell commands.
- If a patch or edit tool exists, use it directly instead of emulating it in bash.
- After changes, run a lightweight verification step such as ls, tests, or a build before declaring the task done.
</terminal_tool_hygiene>
```

### Quality and verification

#### `verification_loop`

Problem: Outputs ship without checking correctness, grounding, or formatting.

```text
<verification_loop>
Before finalizing:
- Check correctness: does the output satisfy every requirement?
- Check grounding: are factual claims backed by retrieved sources or tool output?
- Check formatting: does the output match the requested schema or style?
- Check safety and irreversibility: if the next step has external side effects, ask permission first.
</verification_loop>
```

#### `completeness_contract`

Problem: Batch tasks, lists, or enumerations silently drop items.

```text
<completeness_contract>
- Deliver all requested items.
- Maintain an itemized checklist of deliverables.
- For lists or batches:
  - state the expected count,
  - enumerate items 1..N,
  - confirm that none are missing before finalizing.
- If any item is blocked by missing data, mark it [blocked] and state exactly what is missing.
</completeness_contract>
```

#### `dig_deeper_nudge`

Problem: Model stops at first plausible answer instead of checking edge cases.

```text
<dig_deeper_nudge>
- Do not stop at the first plausible answer.
- Look for second-order issues, edge cases, and missing constraints.
- If the task is safety- or accuracy-critical, perform at least one verification step.
</dig_deeper_nudge>
```

#### `action_safety`

Problem: Agent takes tool actions without summarizing intent or confirming outcome.

```text
<action_safety>
- Pre-flight: summarize the intended action and parameters in 1-2 lines.
- Execute via tool.
- Post-flight: confirm the outcome and any validation that was performed.
</action_safety>
```

### Research and citation

#### `research_mode`

Problem: Research queries get shallow single-pass answers.

```text
<research_mode>
- Do research in 3 passes:
  1) Plan: list 3-6 sub-questions to answer.
  2) Retrieve: search each sub-question and follow 1-2 second-order leads.
  3) Synthesize: resolve contradictions and write the final answer with citations.
- Stop only when more searching is unlikely to change the conclusion.
</research_mode>
```

#### `citation_rules`

Problem: Fabricated citations, wrong URLs, or invented quote spans.

```text
<citation_rules>
- Only cite sources that were actually retrieved in this session.
- Never fabricate citations, URLs, IDs, or quote spans.
- If you cannot find a source for a claim, say so and either:
  - soften the claim, or
  - explain how to verify it with tools.
- Use exactly the citation format required by the host application.
</citation_rules>
```

#### `empty_result_handling`

Problem: Search returns nothing and model immediately gives up.

```text
<empty_result_handling>
If a lookup returns empty or suspiciously small results:
- Do not conclude that no results exist immediately.
- Try at least 2 fallback strategies, such as a broader query, alternate filters, or another source.
- Only then report that no results were found, along with what you tried.
</empty_result_handling>
```

### Context and gating

#### `missing_context_gating`

Problem: Model guesses when required context is missing instead of looking it up.

```text
<missing_context_gating>
- If required context is missing, do not guess.
- Prefer the appropriate lookup tool when the context is retrievable; ask a minimal clarifying question only when it is not.
- If you must proceed, label assumptions explicitly and choose a reversible action.
</missing_context_gating>
```

#### `instruction_priority`

Problem: Conflicting instructions from earlier vs later in conversation.

```text
<instruction_priority>
- User instructions override default style, tone, formatting, and initiative preferences.
- Safety, honesty, privacy, and permission constraints do not yield.
- If a newer user instruction conflicts with an earlier one, follow the newer instruction.
- Preserve earlier instructions that do not conflict.
</instruction_priority>
```

### Output control

#### `output_verbosity_spec`

Problem: Model outputs are too wordy or inconsistent in length.

```text
<output_verbosity_spec>
- Default: 3-6 sentences or up to 6 bullets.
- If the user asked for a doc or report, use headings with short bullets.
- For multi-step tasks:
  - Start with 1 short overview paragraph.
  - Then provide a checklist with statuses: [done], [todo], or [blocked].
- Avoid repeating the user's request.
- Prefer compact, information-dense writing.
</output_verbosity_spec>
```

#### `structured_output_contract`

Problem: Model adds prose or markdown fences around structured output.

```text
<structured_output_contract>
- Output only the requested format.
- Do not add prose or markdown fences unless they were requested.
- Validate that parentheses and brackets are balanced.
- Do not invent tables or fields.
- If required schema information is missing, ask for it or return an explicit error object.
</structured_output_contract>
```

#### `user_updates_spec`

Problem: Long-running agent narrates every tool call instead of major milestones.

```text
<user_updates_spec>
- Only update the user when starting a new major phase or when the plan changes.
- Each update should contain:
  - 1 sentence on what changed,
  - 1 sentence on the next step.
- Do not narrate routine tool calls.
- Keep the user-facing update short, even when the actual work is exhaustive.
</user_updates_spec>
```

### Autonomy and follow-through

#### `default_follow_through_policy`

Problem: Model asks for confirmation on every low-risk step.

```text
<default_follow_through_policy>
- If the user's intent is clear and the next step is reversible and low-risk, proceed without asking permission.
- Only ask permission if the next step is:
  (a) irreversible,
  (b) has external side effects, or
  (c) requires missing sensitive information or a choice that materially changes outcomes.
- If proceeding, state what you did and what remains optional.
</default_follow_through_policy>
```

## Workflow profiles

Recommended combinations by workflow type. Start with these, then add or remove based on evals.

### Long-horizon agent
- `tool_persistence_rules` + `completeness_contract` + `verification_loop`

### Research workflow
- `research_mode` + `citation_rules` + `empty_result_handling`
- Add `tool_persistence_rules` when using retrieval tools
- Add `parallel_tool_calling` when retrieval steps are independent

### Coding or terminal agent
- `terminal_tool_hygiene` + `verification_loop`
- Add `dependency_checks` when actions depend on prerequisite lookup
- Add `tool_persistence_rules` if agent stops too early

### Multi-agent or triage system
- At least one of: `tool_persistence_rules`, `completeness_contract`, or `verification_loop`

### Batch processing
- `completeness_contract` + `verification_loop`
- Add `structured_output_contract` if output is JSON/SQL/etc.

### Civic AI / government agent
- `citation_rules` + `verification_loop` + `action_safety`
- Add `research_mode` + `empty_result_handling` for policy lookup
- Add `missing_context_gating` to prevent guessing on regulatory questions

## Regression checklist

After adding blocks to a prompt:

- Does the prompt still preserve the original task intent?
- Is the new prompt leaner, not just longer?
- Does each block address an observed problem?
- Are completeness, citation quality, and verbosity at acceptable levels?
- Remove any block that isn't earning its keep.
