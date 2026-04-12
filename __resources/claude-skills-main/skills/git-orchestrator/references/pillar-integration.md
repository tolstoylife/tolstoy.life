# Pillar Integration Reference (L3)

Progressive loading: This content loads when cross-pillar coordination is needed.

## Eight-Pillar Integration Matrix

### 1. Claude-Mem Integration

**Hook**: SessionStart
**Action**: Initialize memory context, record session start
**Git Integration**: Commit messages include claude-mem search results for context

```bash
# SessionStart flow
session-start.sh → claude-mem search → session-state.json
```

### 2. Ralph Loop Integration

**Hook**: Notification (via ralph-activity-log.sh)
**Action**: Activity logging throughout autonomous iterations
**Git Integration**: Each Ralph iteration can create checkpoint commits

```bash
# Ralph iteration checkpoint
git commit -m "ralph-iteration-$N: <progress-summary>"
```

### 3. Refactor Agent Integration

**Hook**: PostToolUse (after optimization changes)
**Action**: Auto-commit refactor changes with optimization metrics
**Git Integration**: Dedicated refactor/* branches with detailed metrics

```bash
# Refactor commit format
git commit -m "refactor(${component}): ${optimization}

Metrics:
  - Line reduction: ${reduction}%
  - Latency improvement: ${latency_ms}ms

${detailed_changes}"
```

### 4. Code Skill Integration

**Hook**: PreToolUse (preflight validation)
**Action**: Validate changes before git operations
**Git Integration**: OHPT protocol (Observation-Hypothesis-Prediction-Test) in commit workflow

```bash
# Preflight check before commit
if ! validate_changes; then
  echo "Validation failed, aborting commit"
  exit 1
fi
```

### 5. Learn Skill Integration

**Hook**: Stop (crystallization trigger)
**Action**: Crystallize learnings into knowledge commits
**Git Integration**: Knowledge commits preserve compound engineering K' = K ∪ new_learning

```bash
# Learning commit
git commit -m "learn(${domain}): ${learning_title}

Crystallized from session:
${symptom} → ${root_cause} → ${solution}

Vertices: ${shared_concepts}
Confidence: ${epistemic_weight}"
```

### 6. Ultrawork Agent Integration

**Hook**: Background execution coordination
**Action**: Parallel worktree operations for multi-agent orchestration
**Git Integration**: Each agent can have dedicated worktree for isolation

```bash
# Spawn parallel agents in worktrees
for agent in agent1 agent2 agent3; do
  worktree-manager.sh create "ultrawork-$agent"
done
```

### 7. bv/bd Integration

**Hook**: Continuous (all git operations)
**Action**: DAG issue tracking, graph analysis, metrics
**Git Integration**: Issues tracked in .beads/beads.jsonl, auto-synced with commits

```bash
# bd operations
bd add "Configuration change: ${file}" --tags config
bd link ${parent_issue} ${child_issue}
bd close ${issue_id} --reason "committed"

# bv analysis
bv --robot metrics ~/.claude
bv critical-path --json
```

### 8. Hookify Integration

**Hook**: PreToolUse/PostToolUse validation
**Action**: Runtime validation and enforcement
**Git Integration**: Pre-commit hooks validate changes before git operations

```bash
# Hookify validation in commit flow
hookify validate --all || exit 1
git commit -m "..."
```

## Cross-Pillar Workflows

### Compound Engineering Workflow
```
Plan(K) → Execute → Assess → Compound(K→K') → Git Commit
```

### Refactor Workflow
```
24hr Trigger → Evaluate → Optimize → Git Commit → Push
```

### Learning Workflow
```
Session → Experience → Crystallize → Git Commit → K' Update
```

## Invariant Preservation

All git operations preserve:
- **K-Monotonicity**: len(K') ≥ len(K) - git never loses history
- **Vertex-Sharing**: Cross-references maintained via git log
- **Topology**: η ≥ 4 via structured commit messages
- **Homoiconicity**: Git-orchestrator versions itself
