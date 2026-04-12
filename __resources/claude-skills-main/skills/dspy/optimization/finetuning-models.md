# Fine-Tuning Models with DSPy

DSPy allows you to "compile" your program into model weights (fine-tuning) instead of just prompt context. This is handled by `BootstrapFinetune`.

## Workflow

1. **Prompt-based Optimization First**: Use `BootstrapFewShot` with a large teacher model (e.g., GPT-4) to get a high-performing program.
2. **Generate Training Data**: DSPy runs your optimized program on your training set to generate "traces" (intermediate steps + final outputs).
3. **Fine-tune Smaller Model**: These traces are used to fine-tune a smaller, efficient model (e.g., Llama-3-8B, T5).

## Usage

```python
from dspy.teleprompt import BootstrapFinetune

# 1. Define your module
teacher = MyComplexModule()

# 2. Configure a strong teacher
dspy.configure(lm=dspy.LM("openai/gpt-4o"))

# 3. Compile for fine-tuning
optimizer = BootstrapFinetune(metric=my_metric)

# This doesn't return a module immediately; it prepares fine-tuning data
finetune_data = optimizer.compile(
    teacher,
    trainset=trainset,
    target='t5-large', # or any local model path
    bsize=12           # batch size
)

# 4. Run the fine-tuning (usually handled via script or API)
# dspy.finetune(...)
```

## Benefits

- **Cost**: Smaller models are cheaper to run.
- **Latency**: Smaller models are faster.
- **Privacy**: You can run fine-tuned models locally.
- **Performance**: A fine-tuned small model can often match a large prompt-engineered model for specific tasks.

## When to Use

- You have a stable, successful DSPy program.
- You have moderate to large amounts of data (100s or 1000s of examples).
- You need to reduce inference cost or latency for production.
