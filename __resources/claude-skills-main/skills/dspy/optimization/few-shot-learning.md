# Few-Shot Learning in DSPy

Few-shot learning provides a model with examples of (Input, Output) pairs to guide its behavior. DSPy automates the selection, bootstrapping, and formatting of these examples, replacing manual "prompt engineering" with systematic optimization.

## Key Optimizers

### 1. `BootstrapFewShot` (Standard)
The most common optimizer. It "bootstraps" (generates) reasoning traces for your examples using a teacher model.

**When to Use:**
- You have **10-50 labeled examples**.
- You want the model to use Chain of Thought (reasoning).
- You want a reliable baseline improvement.

**How it Works:**
1. **Teacher Generation**: Runs your program on training inputs using a teacher model.
2. **Filtering**: Keeps only traces that result in correct answers (validated by your metric).
3. **Compilation**: Adds these successful input-output traces as few-shot demonstrations.

### 2. `BootstrapFewShotWithRandomSearch` (Advanced)
A more powerful version that tries random combinations of demonstrations to find the optimal set.

**When to Use:**
- You have **50+ examples**.
- Standard bootstrapping plateaus.
- You have extra compute budget (runs multiple trials).

### 3. `LabeledFewShot` (Simple)
Simply randomly selects examples from your training set without generating reasoning traces.

**When to Use:**
- You have very few examples (<10).
- Debugging pipeline mechanics.
- Bootstrapping is too expensive or failing.

### 4. `KNNFewShot` (Dynamic)
Selects examples at inference time based on similarity to the input query (k-Nearest Neighbors).

**When to Use:**
- Large, diverse datasets where "one size fits all" prompts fail.
- Classification tasks with many classes.

## Workflow: Using BootstrapFewShot

### Phase 1: Setup
```python
import dspy
from dspy.teleprompt import BootstrapFewShot

# Configure LMs
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))
```

### Phase 2: Define Program & Metric
```python
class QA(dspy.Module):
    def __init__(self):
        self.generate = dspy.ChainOfThought("question -> answer")

    def forward(self, question):
        return self.generate(question=question)

def validate_answer(example, pred, trace=None):
    return example.answer.lower() in pred.answer.lower()
```

### Phase 3: Compile
```python
optimizer = BootstrapFewShot(
    metric=validate_answer,
    max_bootstrapped_demos=4,  # Examples with generated reasoning
    max_labeled_demos=4,       # Examples without reasoning
    teacher_settings={'lm': dspy.LM("openai/gpt-4o")} # Stronger teacher
)

compiled_qa = optimizer.compile(QA(), trainset=trainset)
```

### Phase 4: Save & Load
```python
compiled_qa.save("qa_optimized.json")
# Later:
# qa = QA()
# qa.load("qa_optimized.json")
```

## Best Practices

1. **Teacher Selection**: Use a larger model (GPT-4, Opus) as the teacher to bootstrap a smaller student (GPT-4o-mini, Haiku).
   ```python
   teacher_settings={'lm': dspy.LM("anthropic/claude-3-5-sonnet-20240620")}
   ```
2. **Metric Robustness**: Your metric defines "success". If your metric is weak (e.g., exact string match on long text), bootstrapping will fail. Use semantic similarity or LLM-based metrics for complex tasks.
3. **Data Quality**: 10 clean, diverse examples are better than 100 noisy ones.
4. **Iterative Refinement**: Start with `BootstrapFewShot`. If performance isn't sufficient, try `BootstrapFewShotWithRandomSearch` or move to instruction optimization (`MIPROv2`).
