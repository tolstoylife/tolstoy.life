# Instruction Optimization in DSPy

Beyond just selecting examples (few-shot learning), DSPy can optimize the *instructions* (prompts) themselves. This is essentially "Automated Prompt Engineering" but done systematically using data.

## Key Optimizers

### 1. `MIPROv2` (State-of-the-Art)
**MIPROv2 (Most Important Prompt Optimization v2)** is the recommended default for most rigorous tasks. It jointly optimizes both the instructions and the few-shot demonstrations.

**When to Use:**
- You have **200+ labeled examples**.
- You can afford longer optimization runs (~40+ trials).
- You need the highest possible performance.

**How it Works:**
1. **Bootstrap**: Generates candidate demonstrations.
2. **Propose**: Uses a powerful LM (Proposer) to generate varied instruction candidates based on data.
3. **Search**: Uses Bayesian Optimization to find the best combination of instruction + demos.

**Code Example:**
```python
from dspy.teleprompt import MIPROv2

optimizer = MIPROv2(
    metric=my_metric,
    auto="medium",  # Presets: "light" (10 trials), "medium" (40 trials), "heavy" (100+ trials)
)

compiled_program = optimizer.compile(
    student_module,
    trainset=trainset,
    valset=valset, # Highly recommended for MIPRO
    minibatch=True # Updates on small batches for efficiency
)
```

### 2. `COPRO` (Coordinate Prompt Optimization)
A simpler instruction optimizer that refines instructions iteratively.

**When to Use:**
- You have fewer examples (50-100).
- You want to see the instruction evolution step-by-step.
- You don't want to change the few-shot examples (pure instruction tuning).

**How it Works:**
- Generates N variations of the current instruction.
- Evaluates them on a subset of data.
- Keeps the best and iterates.

```python
from dspy.teleprompt import COPRO

optimizer = COPRO(
    metric=my_metric,
    breadth=10, # Candidates per step
    depth=3     # Refinement steps
)
```

### 3. `GEPA` (Genetic-Evolutionary Prompt Architecture)
A newer, reflective optimizer that uses evolutionary algorithms and rich textual feedback.

**When to Use:**
- **Agentic systems** with tool use.
- You have a metric that can provide **textual feedback** (why it failed), not just a score.
- Complex multi-step reasoning where standard optimization struggles.

**Code Example:**
```python
# Metric must return (score, feedback_string)
def feedback_metric(example, pred, trace=None):
    if correct: return 1.0, "Good job"
    return 0.0, f"Failed: Expected {example.ans}, got {pred.ans}"

optimizer = dspy.GEPA(
    metric=feedback_metric,
    reflection_lm=dspy.LM("openai/gpt-4o"), # Needs strong reflection model
    auto="medium"
)
```

## Best Practices

1. **Data Quantity**: MIPROv2 thrives on data. If you have <50 examples, stick to `BootstrapFewShot`. If >200, use `MIPROv2`.
2. **Auto Presets**: Use `auto="medium"` as a starting point. It balances cost and performance.
3. **Evaluation**: Always evaluate on a held-out test set. Optimization can overfit to the training set.
4. **Mini-Batching**: For large datasets, use `minibatch=True` in compile to speed up evaluation during optimization.
5. **Instruction-Only Mode**: You can force MIPROv2 to only optimize instructions (and keep demos fixed or empty) by setting `max_bootstrapped_demos=0`.

## Comparison Table

| Feature | BootstrapFewShot | COPRO | MIPROv2 | GEPA |
|---------|------------------|-------|---------|------|
| **Optimizes** | Demos only | Instructions only | Instructions + Demos | Instructions + Tool Descs |
| **Data Needed** | Low (10+) | Medium (50+) | High (200+) | Medium (50+) |
| **Cost** | Low | Medium | High | High |
| **Feedback** | Score only | Score only | Score only | Score + Text |
| **Best For** | Baselines | Readable Prompts | Max Performance | Agents/Complex Logic |
