# Worktree Operations Reference (L2)

Progressive loading: This content loads when worktree/branch management is needed.

## Worktree Lifecycle

### Creation
```bash
~/.claude/skills/git-orchestrator/scripts/worktree-manager.sh create <name>
```

Creates isolated environment at `~/.claude-worktrees/<name>` with dedicated branch `worktree/<name>`.

**Use Cases**:
- Testing new router architecture
- Experimental skill modifications
- Parallel configuration development
- A/B testing different setups

### Management
```bash
# List all worktrees
worktree-manager.sh list

# Switch to worktree (exports path)
worktree-manager.sh switch <name>

# Remove specific worktree
worktree-manager.sh remove <name>

# Cleanup stale worktrees (>7 days)
worktree-manager.sh cleanup
```

## Branch Strategies

### Feature Branches
```
worktree/feature-name → develop → main
```

### Experiment Branches
```
worktree/experiment-name → (merge or discard)
```

### Session Branches
```
session/YYYYMMDD-HHMMSS → main (auto-merge)
```

## Integration with bd/bv

```bash
# Track worktree creation
bd add "Worktree: <name>" --tags experiment

# Analyze branch graph
bv --robot metrics ~/.claude

# Find parallel development
bv graph --format mermaid
```

## Best Practices

1. **Naming**: Use descriptive names (e.g., `test-grounding-router`, `experiment-meta-dispatcher`)
2. **Cleanup**: Run cleanup weekly to remove stale worktrees
3. **Merging**: Test in worktree before merging to main
4. **Isolation**: Each worktree has independent working directory but shares git history

## Worktree Safety

- **Shared .git**: All worktrees share same repository database
- **Independent working trees**: Changes isolated until merge
- **Branch protection**: Can't checkout same branch in multiple worktrees
- **Atomic operations**: Git ensures consistency across worktrees
