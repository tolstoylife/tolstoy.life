# DSPy Optimization Guide

Complete guide to optimizing DSPy modules with GEPA and built-in optimizers.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Optimizer Selection](#optimizer-selection)
3. [Data Preparation](#data-preparation)
4. [Metric Definition](#metric-definition)
5. [GEPA Workflow](#gepa-workflow)
6. [Compilation Process](#compilation-process)
7. [Evaluation](#evaluation)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 5-Minute Optimization

```python
import dspy
from dspy.evaluate import Evaluate

# 1. Configure LM
lm = dspy.OpenAI(model="gpt-3.5-turbo")
dspy.settings.configure(lm=lm)

# 2. Define module
class QA(dspy.Module):
    def __init__(self):
        self.qa = dspy.ChainOfThought("question -> answer")

    def forward(self, question):
        return self.qa(question=question)

# 3. Prepare data (minimum 10 examples)
trainset = [
    dspy.Example(question="What is DSPy?", answer="...").with_inputs("question"),
    # Add 9+ more examples
]

# 4. Define metric
def accuracy(example, prediction, trace=None):
    return example.answer.lower() in prediction.answer.lower()

# 5. Optimize
optimizer = dspy.BootstrapFewShot(metric=accuracy)
optimized = optimizer.compile(QA(), trainset=trainset)

# 6. Evaluate
evaluator = Evaluate(devset=devset, metric=accuracy)
score = evaluator(optimized)
print(f"Score: {score:.2%}")

# 7. Save
optimized.save('optimized_qa.json')
```

**Expected Results**:
- Time: 1-2 minutes
- Improvement: +15-25%
- Data needed: 10-50 examples

---

## Optimizer Selection

### Decision Tree

```
Start
  │
  ├─ Data size < 50?
  │  └─ Use BootstrapFewShot (⚡⚡⚡ fast)
  │
  ├─ Data size 50-100?
  │  ├─ Need speed? → BootstrapFewShotWithRandomSearch
  │  └─ Need quality? → COPRO
  │
  ├─ Data size 100-200?
  │  ├─ Single-stage task? → COPRO
  │  └─ Multi-stage pipeline? → MIPRO
  │
  └─ Data size 200+?
     └─ Use MIPROv2 (⭐⭐⭐⭐⭐ best quality)
```

### Optimizer Comparison

| Optimizer | Data Needed | Speed | Quality | Use Case |
|-----------|-------------|-------|---------|----------|
| **BootstrapFewShot** | 10-50 | ⚡⚡⚡ | ⭐⭐⭐ | Quick prototyping |
| **BootstrapFewShotWithRandomSearch** | 50+ | ⚡⚡ | ⭐⭐⭐⭐ | Hyperparameter tuning |
| **COPRO** | 50+ | ⚡⚡ | ⭐⭐⭐⭐ | Prompt optimization |
| **MIPRO** | 100+ | ⚡ | ⭐⭐⭐⭐⭐ | Multi-stage pipelines |
| **MIPROv2** | 200+ | ⚡ | ⭐⭐⭐⭐⭐ | Best quality |
| **KNNFewShot** | 100+ | ⚡⚡ | ⭐⭐⭐⭐ | Variable examples |
| **Ensemble** | 100+ | ⚡ | ⭐⭐⭐⭐ | Robustness |

### Configuration Examples

#### BootstrapFewShot - Quick Start
```python
optimizer = dspy.BootstrapFewShot(
    metric=accuracy,
    max_bootstrapped_demos=4,  # Generated examples
    max_labeled_demos=8,       # Labeled examples
)
```

**Best for**: Initial prototyping, classification, simple QA

**Parameters**:
- `max_bootstrapped_demos`: Examples generated from training data (4-8)
- `max_labeled_demos`: Manually labeled examples to include (8-16)
- `teacher_model`: Model for bootstrapping (defaults to configured LM)

#### MIPRO - Production Quality
```python
optimizer = dspy.MIPRO(
    metric=f1_score,
    prompt_model=dspy.OpenAI("gpt-4"),      # Strong model for optimization
    task_model=dspy.OpenAI("gpt-3.5-turbo"), # Production model
    num_trials=20,                            # Optimization trials
    minibatch_size=50,                        # Batch size
    requires_permission_to_run=False          # Auto-run
)
```

**Best for**: Multi-stage pipelines, complex reasoning, production deployment

**Parameters**:
- `prompt_model`: Stronger model for finding good prompts (GPT-4)
- `task_model`: Model that will run in production (GPT-3.5)
- `num_trials`: Number of optimization trials (10-30)
- `minibatch_size`: Size of evaluation batches (25-100)

#### COPRO - Prompt Engineering
```python
optimizer = dspy.COPRO(
    metric=rouge_l,
    breadth=10,           # Number of prompt candidates per generation
    depth=3,              # Number of refinement iterations
    init_temperature=1.4   # Temperature for prompt generation
)
```

**Best for**: Single-stage tasks, text generation, when prompt is critical

**Parameters**:
- `breadth`: Prompt candidates per iteration (5-15)
- `depth`: Refinement iterations (3-5)
- `init_temperature`: Creativity for prompt generation (1.0-1.5)

#### KNNFewShot - Dynamic Examples
```python
optimizer = dspy.KNNFewShot(
    k=5,                  # Examples per prediction
    trainset=trainset,    # Training examples
    vectorizer="sentence-transformers/all-MiniLM-L6-v2"
)
```

**Best for**: Variable task distributions, RAG systems, contextual examples

**Parameters**:
- `k`: Number of similar examples to retrieve (3-7)
- `trainset`: Pool of examples to select from
- `vectorizer`: Embedding model for similarity

---

## Data Preparation

### Minimum Requirements

| Task Type | Min Examples | Recommended | Optimal |
|-----------|-------------|-------------|---------|
| Classification | 10 | 50 | 200+ |
| QA | 20 | 100 | 300+ |
| Generation | 30 | 150 | 500+ |
| Multi-hop | 50 | 200 | 1000+ |

### Data Format

```python
# Basic example
example = dspy.Example(
    question="What is the capital of France?",
    answer="Paris"
).with_inputs("question")

# Multi-input example
example = dspy.Example(
    context="France is a country in Europe...",
    question="What is the capital?",
    answer="Paris"
).with_inputs("context", "question")

# With metadata
example = dspy.Example(
    question="...",
    answer="...",
    metadata={"difficulty": "easy", "category": "geography"}
).with_inputs("question")
```

### Train/Dev/Test Splits

```python
# Option 1: Manual split
train_size = int(0.8 * len(dataset))
dev_size = int(0.1 * len(dataset))

trainset = dataset[:train_size]
devset = dataset[train_size:train_size+dev_size]
testset = dataset[train_size+dev_size:]

# Option 2: Random split
import random
random.shuffle(dataset)
trainset = dataset[:80]
devset = dataset[80:90]
testset = dataset[90:]

# Option 3: Stratified split (for classification)
from sklearn.model_selection import train_test_split

train, temp = train_test_split(dataset, test_size=0.2, stratify=labels)
dev, test = train_test_split(temp, test_size=0.5, stratify=temp_labels)
```

### Data Quality Checklist

- [ ] **Diverse**: Covers various input distributions
- [ ] **Representative**: Includes edge cases and common patterns
- [ ] **Consistent**: Labels follow same format
- [ ] **Clean**: No noise, errors, or duplicates
- [ ] **Balanced**: Even distribution across classes (if applicable)
- [ ] **Sufficient**: Meets minimum requirements for optimizer

### Loading Data

```python
# From JSON
import json

with open('data/train.json', 'r') as f:
    data = json.load(f)
    trainset = [
        dspy.Example(**item).with_inputs("question")
        for item in data
    ]

# From CSV
import pandas as pd

df = pd.read_csv('data/train.csv')
trainset = [
    dspy.Example(
        question=row['question'],
        answer=row['answer']
    ).with_inputs("question")
    for _, row in df.iterrows()
]

# From Hugging Face
from datasets import load_dataset

dataset = load_dataset("hotpot_qa", "distractor")
trainset = [
    dspy.Example(
        question=item['question'],
        answer=item['answer']
    ).with_inputs("question")
    for item in dataset['train']
]
```

---

## Metric Definition

### Built-in Metrics

#### Accuracy (Classification)
```python
def accuracy(example, prediction, trace=None):
    """Perfect for classification tasks."""
    return example.answer.lower() == prediction.answer.lower()
```

**Use for**: Classification, simple QA, exact matching

#### F1 Score (Multi-label)
```python
def f1_score(example, prediction, trace=None):
    """For multi-label classification."""
    pred_set = set(prediction.labels)
    gold_set = set(example.labels)

    if not pred_set or not gold_set:
        return 0.0

    precision = len(pred_set & gold_set) / len(pred_set)
    recall = len(pred_set & gold_set) / len(gold_set)

    if precision + recall == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)
```

**Use for**: Multi-label classification, tagging, entity extraction

#### ROUGE-L (Text Generation)
```python
from rouge import Rouge
rouge = Rouge()

def rouge_l(example, prediction, trace=None):
    """For text generation quality."""
    try:
        scores = rouge.get_scores(prediction.answer, example.answer)
        return scores[0]['rouge-l']['f']
    except:
        return 0.0
```

**Use for**: Summarization, generation, long-form QA

#### BLEU (Translation)
```python
from nltk.translate.bleu_score import sentence_bleu

def bleu(example, prediction, trace=None):
    """For translation quality."""
    reference = [example.answer.split()]
    candidate = prediction.answer.split()
    return sentence_bleu(reference, candidate)
```

**Use for**: Translation, paraphrasing

#### Exact Match (Strict)
```python
def exact_match(example, prediction, trace=None):
    """Strict string matching."""
    return prediction.answer.strip() == example.answer.strip()
```

**Use for**: Fact retrieval, short answers, numeric outputs

### Custom Metrics

#### Semantic Similarity
```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(example, prediction, trace=None):
    """Embedding-based similarity."""
    emb1 = model.encode(example.answer)
    emb2 = model.encode(prediction.answer)
    return cosine_similarity([emb1], [emb2])[0][0]
```

**Use for**: Semantic equivalence, paraphrasing, flexible matching

#### Multi-criteria Metric
```python
def composite_metric(example, prediction, trace=None):
    """Combine multiple metrics."""
    acc = accuracy(example, prediction)
    rouge = rouge_l(example, prediction)

    # Weighted average
    return 0.6 * acc + 0.4 * rouge
```

**Use for**: Balancing multiple objectives

#### LLM-as-Judge
```python
judge_lm = dspy.OpenAI(model="gpt-4")

def llm_judge(example, prediction, trace=None):
    """Use LLM to evaluate quality."""
    prompt = f"""
    Evaluate the quality of this answer:

    Question: {example.question}
    Gold Answer: {example.answer}
    Predicted Answer: {prediction.answer}

    Return score 0-1:
    """

    result = judge_lm(prompt)
    return float(result.strip())
```

**Use for**: Nuanced evaluation, open-ended tasks

---

## GEPA Workflow

### What is GEPA?

**Genetic-Evolutionary Prompt Architecture** - Automatic prompt optimization through evolutionary algorithms.

**Key Concepts**:
- **Population**: Set of prompt variants
- **Fitness**: Performance on training data
- **Selection**: Keep best-performing prompts
- **Crossover**: Combine prompts
- **Mutation**: Introduce variations

### Basic GEPA Usage

```python
from dspy.gepa import GEPA

# 1. Configure GEPA
gepa = GEPA(
    metric=accuracy,
    population_size=10,    # Number of prompt variants
    generations=20,        # Evolution iterations
    mutation_rate=0.3,     # Variation frequency
    crossover_rate=0.7     # Combination frequency
)

# 2. Optimize
result = gepa.optimize(
    seed_prompt="question -> answer",
    training_examples=trainset[:50],
    budget=100  # Max LLM calls
)

# 3. Use optimized prompt
print(f"Best prompt: {result.best_prompt}")
print(f"Score: {result.best_score:.2%}")
```

### GEPA Configuration Guide

#### Exploration Phase (Finding Good Prompts)
```python
gepa = GEPA(
    population_size=15,    # Larger population
    generations=30,        # More generations
    mutation_rate=0.5,     # High mutation
    crossover_rate=0.6     # Moderate crossover
)
```

**Use when**: Starting fresh, unclear about good prompts

#### Exploitation Phase (Refining Prompts)
```python
gepa = GEPA(
    population_size=8,     # Smaller population
    generations=15,        # Fewer generations
    mutation_rate=0.2,     # Low mutation
    crossover_rate=0.8     # High crossover
)
```

**Use when**: Have good seed prompt, need refinement

#### Balanced Approach (Recommended)
```python
gepa = GEPA(
    population_size=10,
    generations=20,
    mutation_rate=0.3,
    crossover_rate=0.7,
    budget=100            # Cost control
)
```

### GEPA Evolution Tracking

```python
result = gepa.optimize(
    seed_prompt="question -> answer",
    training_examples=trainset,
    budget=100,
    verbose=True  # Show progress
)

# Track evolution
print("Evolution history:")
for gen, (prompt, score) in enumerate(result.evolution_history):
    print(f"Gen {gen}: {score:.2%} - {prompt}")

# Analyze improvement
initial_score = result.evolution_history[0][1]
final_score = result.best_score
improvement = (final_score - initial_score) / initial_score
print(f"Improvement: {improvement:.1%}")
```

### Combining GEPA with Optimizers

```python
# Step 1: Use GEPA to find good prompt
gepa = GEPA(metric=accuracy, budget=100)
gepa_result = gepa.optimize(
    seed_prompt="question -> answer",
    training_examples=trainset[:50]
)

# Step 2: Create module with optimized prompt
class OptimizedQA(dspy.Module):
    def __init__(self):
        self.qa = dspy.ChainOfThought(gepa_result.best_prompt)

    def forward(self, question):
        return self.qa(question=question)

# Step 3: Further optimize with MIPRO
optimizer = dspy.MIPRO(metric=accuracy)
final_optimized = optimizer.compile(
    OptimizedQA(),
    trainset=trainset
)
```

**Expected improvement**: +50-70% over baseline

---

## Compilation Process

### Basic Compilation

```python
# Define module
module = QA()

# Configure optimizer
optimizer = dspy.BootstrapFewShot(metric=accuracy)

# Compile
optimized = optimizer.compile(module, trainset=trainset)
```

### Advanced Compilation

#### With Validation Set
```python
optimized = optimizer.compile(
    module,
    trainset=train_split,
    valset=dev_split,  # Early stopping
    max_bootstrapped_demos=8,
    max_labeled_demos=16
)
```

#### With Multiple Trials
```python
optimizer = dspy.BootstrapFewShotWithRandomSearch(
    metric=accuracy,
    num_candidate_programs=10,  # Try 10 configurations
    num_threads=4                # Parallel evaluation
)

optimized = optimizer.compile(module, trainset=trainset)
```

#### Progress Tracking
```python
from tqdm import tqdm

class ProgressOptimizer(dspy.BootstrapFewShot):
    def compile(self, *args, **kwargs):
        with tqdm(total=len(self.trainset)) as pbar:
            def callback(example):
                pbar.update(1)

            return super().compile(*args, **kwargs, callback=callback)
```

---

## Evaluation

### Comprehensive Evaluation

```python
from dspy.evaluate import Evaluate

evaluator = Evaluate(
    devset=devset,
    metric=accuracy,
    num_threads=4,           # Parallel evaluation
    display_progress=True,    # Show progress bar
    display_table=True        # Show results table
)

score = evaluator(optimized)
print(f"Dev score: {score:.2%}")
```

### Multi-Metric Evaluation

```python
from dspy.evaluate import evaluate_all_metrics

results = evaluate_all_metrics(
    module=optimized,
    devset=devset,
    metrics={
        'accuracy': accuracy,
        'f1': f1_score,
        'rouge_l': rouge_l,
        'bleu': bleu
    }
)

for metric_name, score in results.items():
    print(f"{metric_name}: {score:.2%}")
```

### A/B Testing

```python
# Baseline
baseline_score = evaluator(module)

# Optimized
optimized_score = evaluator(optimized)

# Compare
improvement = (optimized_score - baseline_score) / baseline_score
print(f"Baseline: {baseline_score:.2%}")
print(f"Optimized: {optimized_score:.2%}")
print(f"Improvement: {improvement:+.1%}")

# Statistical significance
from scipy.stats import ttest_rel

baseline_preds = [module(ex.question) for ex in devset]
optimized_preds = [optimized(ex.question) for ex in devset]

baseline_scores = [accuracy(ex, pred) for ex, pred in zip(devset, baseline_preds)]
optimized_scores = [accuracy(ex, pred) for ex, pred in zip(devset, optimized_preds)]

t_stat, p_value = ttest_rel(baseline_scores, optimized_scores)
print(f"p-value: {p_value:.4f}")
print("Statistically significant!" if p_value < 0.05 else "Not significant")
```

---

## Troubleshooting

### Low Improvement

**Symptoms**: Score increase < 10%

**Causes & Solutions**:

1. **Insufficient training data**
   - Solution: Add more examples (aim for 50-200)
   - Check: `len(trainset)` should be >= 50

2. **Poor metric function**
   - Solution: Ensure metric aligns with task goals
   - Test: `metric(example, prediction)` returns 0-1

3. **Wrong optimizer**
   - Solution: Try MIPRO or COPRO for better quality
   - Benchmark: Compare multiple optimizers

4. **Baseline already good**
   - Solution: May be near ceiling, focus on edge cases
   - Check: Evaluate baseline on hard examples

### Slow Optimization

**Symptoms**: Compilation takes > 30 minutes

**Causes & Solutions**:

1. **Too many trials**
   - Solution: Reduce `num_trials` to 10-20
   - Trade-off: Quality vs speed

2. **Large training set**
   - Solution: Use subset for iteration, then full set
   - Example: `trainset[:50]` for prototyping

3. **Expensive metric**
   - Solution: Cache predictions, optimize metric code
   - Profile: Time metric function calls

4. **Sequential evaluation**
   - Solution: Enable `num_threads=4`
   - Speedup: 2-4x with parallelism

### Overfitting

**Symptoms**: High train score, low dev score

**Causes & Solutions**:

1. **Too many demonstrations**
   - Solution: Reduce `max_bootstrapped_demos`
   - Recommended: 4-8 demos

2. **Small dev set**
   - Solution: Increase dev set size (20+ examples)
   - Split: 80% train, 10% dev, 10% test

3. **Memorization**
   - Solution: Use different optimizer (KNNFewShot)
   - Add: Regularization or diversity

### Unstable Results

**Symptoms**: Different scores across runs

**Causes & Solutions**:

1. **Random seed**
   - Solution: Set seed for reproducibility
   ```python
   import random
   random.seed(42)
   ```

2. **Small dataset**
   - Solution: Increase data size
   - Use: Cross-validation

3. **Stochastic optimizer**
   - Solution: Run multiple times, average results
   - Report: Mean ± std deviation

---

## Best Practices Summary

### Do's
✓ Start with 50+ training examples
✓ Use validation set for early stopping
✓ Try multiple optimizers
✓ Track optimization history
✓ A/B test against baseline
✓ Use parallel evaluation
✓ Save optimized programs
✓ Monitor production metrics

### Don'ts
✗ Skip baseline evaluation
✗ Optimize on test set
✗ Ignore data quality
✗ Use weak metrics
✗ Overfit to training data
✗ Forget to version control
✗ Deploy without testing
✗ Ignore statistical significance

---

**Next Steps**: After optimization, use `/validate` to verify correctness and `/export` to deploy to production.
