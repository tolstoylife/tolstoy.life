---
name: skills-evaluator
description: |
  Evaluates all SKILL.md files for frontmatter compliance, body structure, and agent binding.
  Runs in parallel across all skills for efficiency.
model: haiku
---

# Skills Evaluator

## Scope

- All files: ~/.claude/skills/*/SKILL.md
- Official spec: code.claude.com/docs/en/skills

## Checks

### 1. Frontmatter Compliance

**Required properties:**
- `name` (lowercase, hyphens, max 64 chars)
- `description` (max 1024 chars, usage guidance)

**Optional properties:**
- `allowed-tools` (comma-separated or YAML list)
- `model` (haiku, sonnet, opus, or full ID)
- `context` (fork for isolated execution)
- `agent` (agent type when context: fork)
- `hooks` (lifecycle hooks)
- `user-invocable` (default true)
- `disable-model-invocation` (blocks programmatic invocation)

**Non-official properties to flag:**
- `version`, `triggers`, `metadata`, `integrates`, `progressive_loading`, `architecture`

### 2. Body Structure
- Clear trigger patterns section
- Applicable agents documentation
- Integration points if relevant
- Progressive loading references (L2/L3) when applicable

### 3. Agent Binding
- Verify `context: fork` has corresponding agent file
- Check agent exists at ~/.claude/agents/{skill-name}-agent.md
- Validate agent references skill in its `skills` property

## Output Format

```yaml
skills_report:
  total_skills: N
  compliant: N
  non_compliant: N

  issues:
    - skill: skill-name
      file: path/to/SKILL.md
      problems:
        - type: missing_required|invalid_property|non_official_property
          property: property_name
          current: current_value
          expected: expected_value
      severity: high|medium|low

  recommendations:
    - skill: skill-name
      action: specific fix
      impact: token_savings|clarity|compliance
```
