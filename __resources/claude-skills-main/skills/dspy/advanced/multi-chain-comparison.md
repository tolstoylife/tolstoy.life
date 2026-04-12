# Multi-Chain Comparison

`dspy.MultiChainComparison` is a specialized module for comparing multiple reasoning paths. It is useful for tasks where generating the answer is hard, but verifying/comparing answers is easier.

## How it works

1. It generates `M` different completions (using temperature sampling).
2. It presents all `M` completions to the model.
3. It asks the model to pick the best one and explain why.

## Usage

```python
import dspy

# Define a simple signature
class Solve(dspy.Signature):
    question = dspy.InputField()
    answer = dspy.OutputField()

# Create comparison module
# M=3 means "generate 3 options, then pick the best"
comparer = dspy.MultiChainComparison(Solve, M=3)

# Run
result = comparer(question="What is the most nuanced interpretation of...?")

print(result.answer)
print(result.rationale) # Explanation of why this answer was chosen over others
```

## When to use

- **Ambiguous Tasks**: Where there isn't one clearly correct factual string.
- **Reasoning**: To avoid getting stuck in a single bad train of thought.
- **Self-Correction**: It acts as a built-in "critic" step.

It is more expensive (M+1 calls) but often yields higher quality results than a single `ChainOfThought`.
