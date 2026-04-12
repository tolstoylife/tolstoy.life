# MAKER Technical Reference

## Mathematical Foundations

### Error Propagation in Multi-Step Tasks

For a task with n sequential steps, each with accuracy p:
```
P(success) = p^n
```

**Example degradation:**
| Steps | p=0.95 | p=0.90 | p=0.85 |
|-------|--------|--------|--------|
| 1     | 95.0%  | 90.0%  | 85.0%  |
| 3     | 85.7%  | 72.9%  | 61.4%  |
| 5     | 77.4%  | 59.0%  | 44.4%  |
| 10    | 59.9%  | 34.9%  | 19.7%  |

This exponential decay motivates MAKER's decomposition and voting approach.

### Consensus Voting Mathematics

For m agents with individual accuracy p, the probability of correct consensus with margin k is computed via binomial distribution:

```
P(correct) = Σ C(m,i) × p^i × (1-p)^(m-i)
             for i from ceil((m+k)/2) to m
```

Where C(m,i) is the binomial coefficient "m choose i".

**Derived reliability by configuration:**

| m  | k | p=0.85 | p=0.90 | p=0.95 |
|----|---|--------|--------|--------|
| 3  | 1 | 92.7%  | 97.2%  | 99.3%  |
| 5  | 2 | 97.1%  | 99.1%  | 99.9%  |
| 7  | 3 | 98.9%  | 99.8%  | 99.98% |
| 11 | 5 | 99.7%  | 99.96% | 99.998%|

### Cost Analysis

**Expected cost per subtask:**
```
E[cost] = E[agents_executed] × cost_per_call
```

With early termination, E[agents_executed] ≈ 0.6×m for high-agreement tasks.

**Total pipeline cost:**
```
Total = Σ E[cost_i] for i in subtasks
      = n × 0.6 × m × cost_per_call
```

**Cost-accuracy Pareto frontier:**

The optimal configuration lies on the Pareto frontier where no improvement in accuracy is possible without increasing cost, and vice versa.

## DAG Construction Patterns

### Pattern 1: Sequential Extraction

For multi-hop QA and entity-attribute-value chains:

```
[Extract Entity] → [Lookup Attribute] → [Transform Value]
```

DAG depth = n (number of hops)
DAG width = 1 (fully sequential)

### Pattern 2: Parallel Extraction

For document analysis with independent components:

```
         ┌─ [Extract Dates]    ─┐
[Parse] ─┼─ [Extract Entities] ─┼─ [Merge Results]
         └─ [Extract Numbers]  ─┘
```

DAG depth = 3
DAG width = 3

### Pattern 3: Hierarchical Verification

For claims requiring multi-source validation:

```
              ┌─ [Source A] ─┐
[Claim] ─┬────┼─ [Source B] ─┼─── [Cross-Validate]
         │    └─ [Source C] ─┘
         └──────────────────────── [Confidence Score]
```

### Pattern 4: Iterative Refinement

For tasks requiring progressive improvement:

```
[Draft] → [Critique] → [Revise] → [Validate] → [Final]
```

With optional loops: if Validate fails, return to Revise.

## Red-Flag Implementation Details

### Length Threshold Calibration

Empirical studies show correlation between output length and error:

```
P(error | length > L_max) ≈ 3-5 × P(error | length ≤ L_max)
```

**Recommended thresholds by task type:**
| Task Type        | L_max (tokens) |
|------------------|----------------|
| Single extraction| 20             |
| Short answer     | 50             |
| Explanation      | 200            |
| Analysis         | 500            |
| Generation       | 1000           |

### Format Validation Schemas

**Strict extraction schema:**
```json
{
  "type": "object",
  "properties": {
    "value": {"type": "string", "minLength": 1},
    "source": {"type": "string"}
  },
  "required": ["value"],
  "additionalProperties": false
}
```

**Flexible answer schema:**
```json
{
  "type": "object",
  "properties": {
    "answer": {"type": "string"},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "reasoning": {"type": "string"}
  },
  "required": ["answer"]
}
```

### Custom Red-Flag Extensions

For domain-specific validation, implement additional checks:

**Numerical range check:**
```python
def check_range_flag(output, min_val, max_val):
    try:
        value = float(output)
        if not (min_val <= value <= max_val):
            return RedFlag(
                flag_type="out_of_range",
                reason=f"Value {value} outside [{min_val}, {max_val}]",
                severity=0.9
            )
    except ValueError:
        pass
    return None
```

**Citation verification:**
```python
def check_citation_flag(output, known_sources):
    cited = extract_citations(output)
    unknown = cited - known_sources
    if unknown:
        return RedFlag(
            flag_type="unknown_citation",
            reason=f"Unknown sources: {unknown}",
            severity=0.7
        )
    return None
```

## Equivalence Class Algorithms

### Semantic Similarity Method

For natural language outputs requiring semantic comparison:

```python
def semantic_equivalence(output1, output2, threshold=0.85):
    emb1 = encode(output1)  # Sentence embedding
    emb2 = encode(output2)
    similarity = cosine_similarity(emb1, emb2)
    return similarity >= threshold
```

**Recommended thresholds:**
| Task Type       | Threshold |
|-----------------|-----------|
| Factual QA      | 0.90      |
| Summarization   | 0.80      |
| Translation     | 0.75      |
| Paraphrase      | 0.85      |

### Structured Comparison Method

For JSON/structured outputs:

```python
def structured_equivalence(output1, output2):
    try:
        obj1 = json.loads(output1)
        obj2 = json.loads(output2)
        # Recursive field comparison with type coercion
        return deep_equal(obj1, obj2)
    except:
        return string_normalized_equal(output1, output2)
```

## Advanced Configuration

### Adaptive Agent Allocation

Dynamically adjust m based on observed disagreement:

```
Initial: m = m_base
After round 1: 
  If disagreement > threshold:
    m = m + Δm
  Repeat until consensus or m = m_max
```

**Disagreement metric:**
```
disagreement = 1 - (max_votes / total_votes)
```

### Tiered Model Strategy

Use cheaper models for less critical subtasks:

```
Criticality high   → GPT-4 / Claude Opus
Criticality medium → GPT-3.5 / Claude Sonnet  
Criticality low    → Claude Haiku / Gemini Flash
```

**Cost savings:** 50-80% with minimal reliability impact

### Cross-Model Ensembles

Reduce correlated errors by diversifying model families:

```
Agents 1-2: Claude models
Agents 3-4: GPT models
Agents 5+:  Gemini/Llama models
```

**Error correlation reduction:**
```
P(all wrong) = Π ε_i << ε^m when errors independent
```

## Integration Patterns

### With API-Based Execution

```python
async def execute_maker_subtask(subtask, inputs, config):
    # Generate m prompts
    prompts = [
        await maker_generate_prompt(subtask, inputs, i)
        for i in range(config.m)
    ]
    
    # Parallel API calls
    outputs = await asyncio.gather(*[
        call_llm_api(p) for p in prompts
    ])
    
    # Red-flag validation
    validated = []
    for i, output in enumerate(outputs):
        flags, valid = apply_red_flags(output, subtask.max_tokens)
        validated.append(AgentOutput(
            agent_id=f"agent_{i}",
            output=output,
            is_valid=valid,
            red_flags=flags
        ))
    
    # Consensus voting
    result = first_to_ahead_by_k_vote(validated, config.k)
    return result
```

### With Batch Processing

For large-scale tasks, batch subtasks by dependency level:

```python
async def execute_maker_pipeline(dag, config):
    results = {}
    
    # Group by dependency level
    levels = group_by_level(dag)
    
    for level in levels:
        # All subtasks at same level can run in parallel
        level_results = await asyncio.gather(*[
            execute_maker_subtask(
                subtask=dag.subtasks[sid],
                inputs=gather_inputs(sid, results, dag),
                config=config
            )
            for sid in level
        ])
        
        # Store results
        for sid, result in zip(level, level_results):
            results[sid] = result
    
    return compose_results(results, dag)
```

## Monitoring and Observability

### Key Metrics

Track these metrics for MAKER pipeline health:

**Reliability metrics:**
- Consensus rate by subtask type
- Red-flag trigger rate by type
- Multi-round retry rate
- Final accuracy (if ground truth available)

**Cost metrics:**
- Average agents per subtask
- Early termination rate
- Cost per successful task

**Latency metrics:**
- P50/P95/P99 subtask latency
- DAG critical path latency
- Total pipeline latency

### Alerting Thresholds

| Metric                    | Warning | Critical |
|---------------------------|---------|----------|
| Consensus rate            | < 0.90  | < 0.80   |
| Red-flag rate             | > 0.30  | > 0.50   |
| Early termination rate    | < 0.50  | < 0.30   |
| Average agents/subtask    | > 0.8×m | > 0.95×m |

## Troubleshooting

### High Red-Flag Rate

**Symptoms:** >30% of outputs being filtered

**Causes:**
1. Length threshold too strict
2. Schema too restrictive
3. Prompt ambiguity causing verbose responses

**Solutions:**
1. Calibrate thresholds against valid output samples
2. Relax "additionalProperties: false" in schema
3. Add explicit constraints to prompt: "Be concise", "Maximum 50 words"

### Low Consensus Rate

**Symptoms:** Frequent disagreement, no clear winner

**Causes:**
1. Task too ambiguous
2. Multiple valid interpretations
3. Prompt underspecification

**Solutions:**
1. Further decompose the subtask
2. Add examples to prompt
3. Use semantic equivalence instead of exact matching

### High Cost

**Symptoms:** Cost multiplier approaching m×

**Causes:**
1. Early termination not triggering
2. High disagreement requiring full m execution
3. Too many retry rounds

**Solutions:**
1. Verify early_terminate=True in voting
2. Reduce task ambiguity
3. Consider lower criticality configuration
