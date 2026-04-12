# DSPy-Code Cheatsheet

Quick reference for common DSPy-Code operations.

---

## Commands

```bash
# Initialize project
/init my-project --template rag --lm gpt-4

# Connect to workspace
/connect

# Generate demo
/demo rag --with-optimization

# Validate code
/validate modules/qa.py --strict

# Optimize module
/optimize modules/qa.py --optimizer mipro

# Export module
/export python --include-examples
```

---

## 10 Predictors

```python
dspy.Predict(signature)                      # Basic
dspy.ChainOfThought(signature)               # CoT reasoning
dspy.ChainOfThoughtWithHint(signature)       # CoT + hints
dspy.ProgramOfThought(signature)             # Code execution
dspy.ReAct(signature)                        # Agent with tools
dspy.MultiChainComparison(signature)         # Compare chains
dspy.Retrieve(k=3)                           # Document retrieval
dspy.TypedPredictor(signature, output_type)  # Type-constrained
dspy.Ensemble([predictor1, predictor2])      # Multiple predictors
dspy.majority(predictions)                   # Majority vote
```

---

## 11 Optimizers

```python
# Fast prototyping (10-50 examples)
dspy.BootstrapFewShot(metric=accuracy)

# Hyperparameter tuning (50+ examples)
dspy.BootstrapFewShotWithRandomSearch(metric=accuracy)

# Prompt optimization (50+ examples)
dspy.COPRO(metric=accuracy, breadth=10, depth=3)

# Multi-stage pipelines (100+ examples)
dspy.MIPRO(
    metric=accuracy,
    prompt_model=dspy.OpenAI("gpt-4"),
    task_model=dspy.OpenAI("gpt-3.5-turbo")
)

# Best quality (200+ examples)
dspy.MIPROv2(metric=accuracy)

# KNN-based selection (100+ examples)
dspy.KNNFewShot(k=5, trainset=trainset)

# Ensemble methods (100+ examples)
dspy.Ensemble(metric=accuracy)
```

---

## 4 Adapters

```python
dspy.ChatAdapter()        # Chat models
dspy.JSONAdapter()        # JSON outputs
dspy.FunctionAdapter()    # Function calling
dspy.ImageAdapter()       # Image inputs
```

---

## Metrics

```python
# Accuracy
def accuracy(example, pred, trace=None):
    return example.answer == pred.answer

# F1 Score
def f1_score(example, pred, trace=None):
    # Multi-label classification
    ...

# ROUGE-L
from rouge import Rouge
rouge = Rouge()
def rouge_l(example, pred, trace=None):
    return rouge.get_scores(pred.answer, example.answer)[0]['rouge-l']['f']

# Exact Match
def exact_match(example, pred, trace=None):
    return pred.answer.strip() == example.answer.strip()
```

---

## Quick Patterns

### Simple QA
```python
class QA(dspy.Module):
    def __init__(self):
        self.qa = dspy.ChainOfThought("question -> answer")

    def forward(self, question):
        return self.qa(question=question)
```

### RAG Pipeline
```python
class RAG(dspy.Module):
    def __init__(self, k=3):
        self.retrieve = dspy.Retrieve(k=k)
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)
```

### Typed Output
```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float

class Extractor(dspy.Module):
    def __init__(self):
        self.extract = dspy.TypedPredictor(
            "text -> product",
            output_type=Product
        )

    def forward(self, text):
        return self.extract(text=text)
```

### Agent
```python
class Agent(dspy.Module):
    def __init__(self, tools):
        self.react = dspy.ReAct("question, tools -> answer")
        self.tools = tools

    def forward(self, question):
        return self.react(question=question, tools=self.tools)
```

---

## Optimization Workflow

```python
# 1. Prepare data
trainset = [
    dspy.Example(question="...", answer="...").with_inputs("question")
]

# 2. Define metric
def metric(example, pred, trace=None):
    return example.answer == pred.answer

# 3. Choose optimizer
optimizer = dspy.BootstrapFewShot(metric=metric)

# 4. Compile
optimized = optimizer.compile(module, trainset=trainset)

# 5. Evaluate
from dspy.evaluate import Evaluate
evaluator = Evaluate(devset=devset, metric=metric)
score = evaluator(optimized)

# 6. Save
optimized.save('optimized.json')
```

---

## GEPA Optimization

```python
from dspy.gepa import GEPA

# Configure
gepa = GEPA(
    metric=accuracy,
    population_size=10,
    generations=20,
    mutation_rate=0.3,
    crossover_rate=0.7
)

# Optimize
result = gepa.optimize(
    seed_prompt="question -> answer",
    training_examples=trainset[:50],
    budget=100
)

# Use result
print(f"Best: {result.best_prompt}")
print(f"Score: {result.best_score:.2%}")
```

---

## Configuration

```python
import dspy

# OpenAI
lm = dspy.OpenAI(model="gpt-3.5-turbo", api_key="...")
dspy.settings.configure(lm=lm)

# Anthropic
lm = dspy.Claude(model="claude-3-opus-20240229", api_key="...")
dspy.settings.configure(lm=lm)

# Cohere
lm = dspy.Cohere(model="command", api_key="...")
dspy.settings.configure(lm=lm)

# Ollama
lm = dspy.Ollama(model="llama2")
dspy.settings.configure(lm=lm)

# With retrieval
rm = dspy.ColBERTv2(url="http://localhost:2017")
dspy.settings.configure(lm=lm, rm=rm)
```

---

## Evaluation

```python
from dspy.evaluate import Evaluate

# Single metric
evaluator = Evaluate(devset=devset, metric=accuracy)
score = evaluator(module)

# Multiple metrics
from dspy.evaluate import evaluate_all_metrics
results = evaluate_all_metrics(
    module=module,
    devset=devset,
    metrics={
        'accuracy': accuracy,
        'f1': f1_score,
        'rouge': rouge_l
    }
)

# A/B testing
baseline_score = evaluator(module)
optimized_score = evaluator(optimized)
improvement = (optimized_score - baseline_score) / baseline_score
```

---

## Saving & Loading

```python
# Save
optimized.save('model.json')

# Load
from dspy import load_program
loaded = load_program('model.json')

# Use
result = loaded(question="...")
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Low improvement | Increase data size, try MIPRO |
| Slow optimization | Reduce trials, enable `num_threads` |
| Overfitting | Reduce demos, increase data |
| Unstable results | Set random seed, increase data |

---

## Optimizer Decision Matrix

| Data Size | Speed Priority | Quality Priority |
|-----------|---------------|------------------|
| 10-50 | BootstrapFewShot | BootstrapFewShot |
| 50-100 | BootstrapFewShotWithRandomSearch | COPRO |
| 100-200 | COPRO | MIPRO |
| 200+ | KNNFewShot | MIPROv2 |

---

## Performance Expectations

| Dataset | Optimizer | Time | Improvement |
|---------|-----------|------|-------------|
| 10 examples | BootstrapFewShot | 30s | +15-25% |
| 50 examples | BootstrapFewShot | 2min | +20-35% |
| 100 examples | MIPRO | 15min | +30-50% |
| 200 examples | MIPROv2 | 30min | +40-60% |
| 500 examples | MIPRO + GEPA | 1hr | +50-70% |

---

## Best Practices

**Do's** ✓
- Start with 50+ examples
- Use validation sets
- Try multiple optimizers
- Track optimization history
- A/B test baselines
- Save optimized programs
- Monitor production

**Don'ts** ✗
- Skip baseline evaluation
- Optimize on test set
- Ignore data quality
- Use weak metrics
- Overfit training data
- Deploy without testing

---

## Resources

- **Docs**: https://dspy-docs.vercel.app
- **GitHub**: https://github.com/stanfordnlp/dspy
- **Examples**: https://github.com/stanfordnlp/dspy/tree/main/examples
- **Codebase**: `/Users/mikhail/Downloads/architect/dspy-code-codebase`

---

## Quick Start

```bash
# 1. Install
pip install dspy-ai

# 2. Initialize project
/init my-app --template qa

# 3. Develop
/demo simple-qa --with-optimization

# 4. Validate
/validate modules/qa.py

# 5. Optimize
/optimize modules/qa.py

# 6. Export
/export python --include-examples

# 7. Deploy
python -m modules.qa
```

---

**Version**: 1.0.0
**Last Updated**: 2025-12-02
