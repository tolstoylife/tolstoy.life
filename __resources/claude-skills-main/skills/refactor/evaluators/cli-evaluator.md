---
name: cli-evaluator
description: |
  Evaluates CLI tools for installation, version compatibility, and integration health.
  Checks research, pex, ck, pieces, screenapp, notability, and other CLI binaries.
model: haiku
---

# CLI Evaluator

## Scope

- CLI tools:
  - research: ~/.local/bin/research
  - pex: ~/.local/bin/pex
  - ck: ~/.cargo/bin/ck
  - pieces: /opt/homebrew/bin/pieces
  - screenapp: ~/Projects/screenapp-cli/bin/screenapp.ts
  - notability: /Users/mikhail/miniconda3/bin/notability
  - gemini: /opt/homebrew/bin/gemini
  - codex: ~/.local/bin/codex
  - amp: ~/.amp/bin/amp

## Checks

### 1. Installation
- Verify binary exists and is executable
- Check for correct installation path
- Validate dependencies are met

### 2. Version Compatibility
- Check current version vs expected
- Identify outdated tools
- Flag deprecated versions

### 3. Integration Health
- Test basic invocation
- Verify configuration files exist
- Check for integration with CLAUDE.md rules

### 4. Usage Patterns
- Identify unused CLI tools
- Check for missing tools referenced in rules
- Validate trigger patterns in context extraction

## Output Format

```yaml
cli_report:
  total_tools: N
  installed: N
  missing: N
  outdated: N

  tools:
    - name: tool_name
      path: /path/to/binary
      status: installed|missing|broken
      version: X.Y.Z
      expected_version: X.Y.Z
      health: healthy|degraded|broken
      issues: [list of problems]

  integration:
    configured_in_rules: [list of tools in CLAUDE.md]
    missing_from_rules: [installed but not referenced]
    referenced_but_missing: [in rules but not installed]

  recommendations:
    - tool: tool_name
      action: install|update|remove|configure
      priority: high|medium|low
      impact: functionality|performance
```
