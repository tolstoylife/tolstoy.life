# Skill Synthesis Method

This reference describes the synthesis pipeline used to combine multiple skills into a single, higher-order workflow.

## Inputs

- A list of discovered skills (name, description, downloads, updated_at if available)
- The user task or discovery query

## Pipeline Stages

1. Pattern Extraction
   - Extract core capability tokens from each skill (name + description)
   - Normalize to a shared vocabulary
2. Capability Matrix
   - Build a skill -> capabilities map and capability -> skills map
   - Identify complementary clusters and sparse coverage
3. Architectural Reasoning
   - Map skills into roles (discover, decide, design, build, verify, deliver)
   - Favor coverage of all stages over single-stage depth
4. Pareto Optimization
   - Maximize relevance, popularity, recency, diversity
   - Minimize redundancy (semantic similarity)
5. Homoiconic Output
   - Represent the pipeline as a list of stages (data = structure)
   - Each stage embeds a holographic summary of the whole loop

## Output Format

```
Pipeline (Synthesized Skill):
1) discover: [skill-a, skill-b] -> "micro-instruction"
2) decide: [skill-c] -> "micro-instruction"
3) design: [skill-d] -> "micro-instruction"
4) build: [skill-e] -> "micro-instruction"
5) verify: [skill-f] -> "micro-instruction"
6) deliver: [skill-g] -> "micro-instruction"

Meta-instruction: "One-line loop that stitches stages together."
```

## Example Use

```
./scripts/pipeline_synthesis.py results.json --query="improve code quality" --limit-per-role=2
```
