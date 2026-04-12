# GPT-5.4 prompting upgrade guide

Use this guide when prompts written for older models need to be adapted for GPT-5.4 during an upgrade. Start lean: keep the model-string change narrow, preserve the original task intent, and add only the smallest prompt changes needed to recover behavior.

## Default upgrade posture

- Start with `model string only` whenever the old prompt is already short, explicit, and task-bounded.
- Move to `model string + light prompt rewrite` only when regressions appear in completeness, persistence, citation quality, verification, or verbosity.
- Prefer one or two targeted prompt additions over a broad rewrite.
- Treat reasoning effort as a last-mile knob. Start lower, then increase only after prompt-level fixes and evals.
- Before increasing reasoning effort, first add a completeness contract, a verification loop, and tool persistence rules - depending on the usage case.

## Behavioral differences to account for

Current GPT-5.4 upgrade guidance suggests these strengths:

- stronger personality and tone adherence, with less drift over long answers
- better long-horizon and agentic workflow stamina
- stronger spreadsheet, finance, and formatting tasks
- more efficient tool selection and fewer unnecessary calls by default
- stronger structured generation and classification reliability

The main places where prompt guidance still helps are:

- retrieval-heavy workflows that need persistent tool use and explicit completeness
- research and citation discipline
- verification before irreversible or high-impact actions
- terminal and tool workflow hygiene
- defaults and implied follow-through
- verbosity control for compact, information-dense answers

## Prompt rewrite patterns

| Older prompt pattern | Adjustment | Why | Example addition |
| --- | --- | --- | --- |
| Long, repetitive instructions that compensate for weaker instruction following | Remove duplicate scaffolding and keep only the constraints that materially change behavior | Newer models usually need less repeated steering | Replace repeated reminders with one concise rule plus a verification block |
| Fast assistant prompt with no verbosity control | Keep the prompt as-is first; add a verbosity clamp only if outputs become too long | Many upgrades work with just a model-string swap | Add `output_verbosity_spec` only after a verbosity regression |
| Tool-heavy agent prompt that assumes the model will keep searching until complete | Add persistence and verification rules | Model may use fewer tool calls by default for efficiency | Add `tool_persistence_rules` and `verification_loop` |
| Tool-heavy workflow where later actions depend on earlier lookup or retrieval | Add prerequisite and missing-context rules before action steps | Explicit dependency-aware routing when context is still thin | Add `dependency_checks` and `missing_context_gating` |
| Retrieval workflow with several independent lookups | Add selective parallelism guidance | Strong at parallel tool use, but should not parallelize dependent steps | Add `parallel_tool_calling` |
| Batch workflow prompt that often misses items | Add an explicit completeness contract | Item accounting benefits from direct instruction | Add `completeness_contract` |
| Research prompt that needs grounding and citation discipline | Add research, citation, and empty-result recovery blocks | Multi-pass retrieval is stronger when the model is told how to react to weak or empty search results | Add `research_mode`, `citation_rules`, and `empty_result_handling` |
| Coding or terminal prompt with shell misuse or early stop failures | Keep the same tool surface and add terminal hygiene and verification instructions | Tool-using coding workflows usually need better prompt steering, not host rewiring | Add `terminal_tool_hygiene` and `verification_loop` |
| Multi-agent or support-triage workflow with escalation or completeness requirements | Add one lightweight control block for persistence, completeness, or verification | More efficient by default, so multi-step support flows benefit from an explicit completion or verification contract | Add at least one of `tool_persistence_rules`, `completeness_contract`, or `verification_loop` |

## Prompt blocks

Use these selectively. Do not add all of them by default. These blocks are model-agnostic and work with any LLM that follows system instructions.

### `output_verbosity_spec`

Use when the model gets too wordy or the host needs compact, information-dense answers.

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

### `default_follow_through_policy`

Use when the model becomes too conservative or asks for confirmation too often on reversible, low-risk steps.

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

### `instruction_priority`

Use when users often change task shape, format, or tone mid-conversation and an explicit override policy is needed.

```text
<instruction_priority>
- User instructions override default style, tone, formatting, and initiative preferences.
- Safety, honesty, privacy, and permission constraints do not yield.
- If a newer user instruction conflicts with an earlier one, follow the newer instruction.
- Preserve earlier instructions that do not conflict.
</instruction_priority>
```

### `tool_persistence_rules`

Use when the workflow needs multiple retrieval or verification steps and the model starts stopping too early.

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

### `dig_deeper_nudge`

Use when the model is too literal or stops at the first plausible answer, especially for safety- or accuracy-sensitive tasks.

```text
<dig_deeper_nudge>
- Do not stop at the first plausible answer.
- Look for second-order issues, edge cases, and missing constraints.
- If the task is safety- or accuracy-critical, perform at least one verification step.
</dig_deeper_nudge>
```

### `dependency_checks`

Use when later actions depend on prerequisite lookup, memory retrieval, or discovery steps.

```text
<dependency_checks>
- Before taking an action, check whether prerequisite discovery, lookup, or memory retrieval is required.
- Do not skip prerequisite steps just because the intended final action seems obvious.
- If a later step depends on the output of an earlier one, resolve that dependency first.
</dependency_checks>
```

### `parallel_tool_calling`

Use when the workflow has multiple independent retrieval steps and wall-clock time matters.

```text
<parallel_tool_calling>
- When multiple retrieval or lookup steps are independent, prefer parallel tool calls to reduce wall-clock time.
- Do not parallelize steps with prerequisite dependencies or where one result determines the next action.
- After parallel retrieval, pause to synthesize before making more calls.
- Prefer selective parallelism: parallelize independent evidence gathering, not speculative or redundant tool use.
</parallel_tool_calling>
```

### `completeness_contract`

Use when the task involves batches, lists, enumerations, or multiple deliverables and missing items are a common failure mode.

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

### `empty_result_handling`

Use when the workflow performs search, CRM, logs, or retrieval steps where no-results failures are often false negatives.

```text
<empty_result_handling>
If a lookup returns empty or suspiciously small results:
- Do not conclude that no results exist immediately.
- Try at least 2 fallback strategies, such as a broader query, alternate filters, or another source.
- Only then report that no results were found, along with what you tried.
</empty_result_handling>
```

### `verification_loop`

Use when the workflow has downstream impact and accuracy, formatting, or completeness regressions matter.

```text
<verification_loop>
Before finalizing:
- Check correctness: does the output satisfy every requirement?
- Check grounding: are factual claims backed by retrieved sources or tool output?
- Check formatting: does the output match the requested schema or style?
- Check safety and irreversibility: if the next step has external side effects, ask permission first.
</verification_loop>
```

### `missing_context_gating`

Use when required context is sometimes missing early in the workflow and the model should prefer retrieval over guessing.

```text
<missing_context_gating>
- If required context is missing, do not guess.
- Prefer the appropriate lookup tool when the context is retrievable; ask a minimal clarifying question only when it is not.
- If you must proceed, label assumptions explicitly and choose a reversible action.
</missing_context_gating>
```

### `action_safety`

Use when the agent takes actions through tools and the host benefits from a short pre-flight and post-flight execution frame.

```text
<action_safety>
- Pre-flight: summarize the intended action and parameters in 1-2 lines.
- Execute via tool.
- Post-flight: confirm the outcome and any validation that was performed.
</action_safety>
```

### `citation_rules`

Use when the workflow produces cited answers and fabricated citations are costly.

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

### `research_mode`

Use when the workflow is research-heavy and uses web search or retrieval tools.

```text
<research_mode>
- Do research in 3 passes:
  1) Plan: list 3-6 sub-questions to answer.
  2) Retrieve: search each sub-question and follow 1-2 second-order leads.
  3) Synthesize: resolve contradictions and write the final answer with citations.
- Stop only when more searching is unlikely to change the conclusion.
</research_mode>
```

### `structured_output_contract`

Use when the host depends on strict JSON, SQL, or other structured output.

```text
<structured_output_contract>
- Output only the requested format.
- Do not add prose or markdown fences unless they were requested.
- Validate that parentheses and brackets are balanced.
- Do not invent tables or fields.
- If required schema information is missing, ask for it or return an explicit error object.
</structured_output_contract>
```

### `terminal_tool_hygiene`

Use when the prompt belongs to a terminal-based or coding-agent workflow.

```text
<terminal_tool_hygiene>
- Only run shell commands through the terminal tool.
- Never try to "run" tool names as shell commands.
- If a patch or edit tool exists, use it directly instead of emulating it in bash.
- After changes, run a lightweight verification step such as ls, tests, or a build before declaring the task done.
</terminal_tool_hygiene>
```

### `user_updates_spec`

Use when the workflow is long-running and user updates matter.

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

## Example upgrade profiles

### GPT-4o or GPT-4.1 assistant
- Use `gpt-5.4` with `none` reasoning effort
- Add `output_verbosity_spec` only if output becomes too verbose

### Long-horizon agent
- Use `gpt-5.4` with `medium` reasoning effort
- Add `tool_persistence_rules` + `completeness_contract` + `verification_loop`

### Research workflow
- Use `gpt-5.4` with `medium` reasoning effort
- Add `research_mode` + `citation_rules` + `empty_result_handling`
- Add `tool_persistence_rules` when using retrieval tools
- Add `parallel_tool_calling` when retrieval steps are independent

### Coding or terminal workflow
- Use `gpt-5.4`, match current reasoning effort
- Add `terminal_tool_hygiene` + `verification_loop`
- Add `dependency_checks` when actions depend on prerequisite lookup
- Add `tool_persistence_rules` if the agent stops too early

### Multi-agent or support triage
- Prefer `model string + light prompt rewrite`
- Add at least one of `tool_persistence_rules`, `completeness_contract`, or `verification_loop`

## Prompt regression checklist

- Check whether the upgraded prompt still preserves the original task intent.
- Check whether the new prompt is leaner, not just longer.
- Check completeness, citation quality, dependency handling, verification behavior, and verbosity.
- Confirm that each added prompt block addresses an observed regression.
- Remove prompt blocks that are not earning their keep.
