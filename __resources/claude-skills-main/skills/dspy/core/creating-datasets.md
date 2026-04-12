# Creating Datasets

Data is the fuel for DSPy optimizers. Instead of manual prompt tuning, you curate examples that define good behavior.

## The `dspy.Example` Class

The core data structure is `dspy.Example`. It holds input and output fields.

```python
import dspy

# Create an example
ex = dspy.Example(
    question="What is the capital of France?",
    answer="Paris",
    context="France is a country in Europe..."
)
```

### Specifying Inputs

Crucially, you must tell DSPy which fields are **inputs** for your task. The rest are assumed to be labels/metadata.

```python
# Mark 'question' as the input
train_ex = ex.with_inputs("question")

# Mark 'question' and 'context' as inputs
rag_ex = ex.with_inputs("question", "context")
```

## Creating Training Sets

A training set is just a list of `dspy.Example` objects.

```python
trainset = [
    dspy.Example(question="2+2", answer="4").with_inputs("question"),
    dspy.Example(question="3+3", answer="6").with_inputs("question"),
    dspy.Example(question="5*5", answer="25").with_inputs("question"),
]
```

## Creating Validation/Dev Sets

It's best practice to keep a separate set for evaluation.

```python
devset = [
    dspy.Example(question="10-2", answer="8").with_inputs("question"),
    dspy.Example(question="100/10", answer="10").with_inputs("question"),
]
```

## Data quantity guidelines

| Optimizer | Required Examples |
|-----------|-------------------|
| `BootstrapFewShot` | 10-50 |
| `MIPROv2` | 50-200+ |
| `BootstrapFinetune` | 100-500+ |
| `KNNFewShot` | 10+ (used as reference bank) |

## Bootstrapping Data (Synthetic Data)

If you don't have enough data, you can use a strong model (like GPT-4) to generate examples for a weaker model.

1. Create a handful of perfect examples.
2. Use them to prompt a strong model to generate more.
3. Validate/filter the generated examples.
4. Use the filtered set to train your DSPy program.
