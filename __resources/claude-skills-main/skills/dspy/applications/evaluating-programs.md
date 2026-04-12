# Evaluating Programs

Evaluation is the compass for optimization. You cannot improve what you cannot measure.

## `dspy.Evaluate`

The standard tool for running evaluation metrics over a dataset.

```python
from dspy.evaluate import Evaluate

evaluator = Evaluate(
    devset=devset,
    metric=my_metric,
    num_threads=4,
    display_progress=True,
    display_table=True
)

score = evaluator(my_program)
```

## Defining Metrics

A metric is a function that takes `(example, prediction, trace)` and returns a number (score) or boolean.

### 1. Exact Match (Boolean)
```python
def exact_match(example, pred, trace=None):
    return example.answer == pred.answer
```

### 2. Semantic Match (using LLM)
Useful for long-form answers where exact wording varies.

```python
class Assess(dspy.Signature):
    """Assess if the prediction matches the reference answer."""
    reference = dspy.InputField()
    prediction = dspy.InputField()
    matches: bool = dspy.OutputField()

def semantic_metric(example, pred, trace=None):
    return dspy.Predict(Assess)(
        reference=example.answer,
        prediction=pred.answer
    ).matches
```

### 3. Multi-faceted Metric
Combining multiple signals.

```python
def mixed_metric(example, pred, trace=None):
    exact = example.answer == pred.answer
    length_ok = len(pred.answer) < 100
    return (exact * 0.8) + (length_ok * 0.2)
```

## Built-in Metrics

DSPy provides common metrics:
- `dspy.evaluate.answer_exact_match`
- `dspy.evaluate.SemanticF1` (LLM-based F1)

## Best Practices

- **Hold-out Set**: Never optimize on your dev/test set.
- **Speed**: Simple string-match metrics are fast. LLM-based metrics are slow but more accurate for open-ended tasks.
- **Trace Analysis**: The `trace` argument allows you to inspect intermediate steps (e.g., "did retrieval find the right document?") and score based on process, not just outcome.
