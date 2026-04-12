# Ensemble Strategies

Ensembling combines multiple modules or predictions to improve accuracy and robustness.

## `dspy.majority`

The simplest form of ensembling is majority voting.

```python
from dspy.primitives import majority

# Run prediction 5 times
preds = [module(question) for _ in range(5)]

# Get the consensus answer
final_answer = majority([p.answer for p in preds])
```

## `Ensemble` Module

You can explicitly optimize multiple variants of a program and ensemble them.

```python
class Ensemble(dspy.Module):
    def __init__(self, modules):
        self.modules = modules

    def forward(self, *args, **kwargs):
        results = [m(*args, **kwargs) for m in self.modules]
        # Custom logic to combine results
        # e.g., majority vote, or weighted average by confidence
        return dspy.Prediction(answer=majority([r.answer for r in results]))

# Create 3 optimized versions
opt1 = BootstrapFewShot(...).compile(mod, trainset)
opt2 = MIPROv2(...).compile(mod, trainset)
opt3 = COPRO(...).compile(mod, trainset)

# Combine them
ensemble_prog = Ensemble([opt1, opt2, opt3])
```

## `MultiChainComparison`

This built-in module generates multiple reasoning chains and then asks the model to compare them and select the best one.

```python
# M=5 means generate 5 chains
comparer = dspy.MultiChainComparison("question -> answer", M=5)

result = comparer(question="Complex ambiguous question...")
```

This is particularly effective for:
- Math/Logic problems where verification is easier than generation.
- Ambiguous queries where exploring multiple interpretations helps.
