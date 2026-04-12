---
name: plugins-evaluator
description: |
  Evaluates plugin.json files for compatibility, version conflicts, and resource usage.
  Checks all plugins in ~/.claude/plugins/.
model: sonnet
---

# Plugins Evaluator

## Scope

- Plugin files: ~/.claude/plugins/*/plugin.json
- Cache: ~/.claude/plugins/cache/
- Installed plugins from every-marketplace

## Checks

### 1. Compatibility
- Verify Claude Code version compatibility
- Check for deprecated plugin APIs
- Validate plugin structure against schema

### 2. Version Conflicts
- Find plugins requiring incompatible versions
- Identify duplicate functionality across plugins
- Check for plugin dependency conflicts

### 3. Resource Usage
- Measure cache directory size per plugin
- Identify plugins with excessive file counts
- Calculate total token overhead from loaded components

### 4. Plugin Health
- Verify all referenced skills/agents/commands exist
- Check for broken plugin references
- Validate metadata completeness

## Output Format

```yaml
plugins_report:
  total_plugins: N
  active: N
  cached: N

  compatibility:
    compatible: N
    incompatible: N
    deprecated_api: [list of plugins using old APIs]

  conflicts:
    - plugins: [plugin1, plugin2]
      issue: version_conflict|duplicate_functionality
      severity: high|medium|low

  resource_usage:
    total_cache_size_mb: N
    per_plugin:
      - name: plugin-name
        cache_size_mb: N
        component_count: N
        token_overhead: N

  recommendations:
    - plugin: plugin-name
      action: update|remove|consolidate
      impact: performance|compatibility|resources
```
