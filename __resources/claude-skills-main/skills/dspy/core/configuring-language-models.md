# Configuring Language Models

DSPy requires configuring a Language Model (LM) to execute prompts. You can configure a global default LM or use context managers for specific blocks of code.

## Global Configuration

The most common way to set up DSPy is to configure a global default LM at the start of your script.

```python
import dspy

# Initialize the LM
lm = dspy.Claude(
    model="claude-sonnet-4-5-20250929",
    api_key="your-api-key",  # Optional if set in env vars
    max_tokens=1000,
    temperature=0.7
)

# Set as default
dspy.settings.configure(lm=lm)
```

## Supported Providers

### Anthropic Claude

```python
lm = dspy.Claude(
    model="claude-sonnet-4-5-20250929",
    api_key="sk-...",
    base_url="http://localhost:8318", # Optional proxy
    max_tokens=1000
)
```

### OpenAI GPT

```python
lm = dspy.OpenAI(
    model="gpt-5.2-codex",
    api_key="sk-...",
    max_tokens=1000
)
```

### Google Gemini

```python
lm = dspy.Gemini(
    model="gemini-3-flash-preview",
    api_key="...",
    max_tokens=1000
)
```

### Local Models (Ollama)

```python
lm = dspy.OllamaLocal(
    model="qwen3-4B",
    base_url="http://localhost:11434"
)
```

## Using Multiple Models

You can use different models for different parts of your pipeline. For example, use a cheaper model for simple retrieval tasks and a stronger model for complex reasoning.

```python
# Initialize models
cheap_lm = dspy.OpenAI(model="gpt-4o-mini")
strong_lm = dspy.Claude(model="claude-3-5-sonnet-20241022")

# Set global default
dspy.settings.configure(lm=strong_lm)

# Use context manager for specific operations
with dspy.settings.context(lm=cheap_lm):
    # This block uses the cheap model
    retriever_result = dspy.Retrieve(k=5)("query")

# Outside the block, it reverts to the global default (strong_lm)
response = dspy.Predict("question -> answer")(question="query")
```

## Debugging Configuration

To see what's happening under the hood, you can inspect the history of calls.

```python
# Enable tracing history
dspy.settings.configure(lm=lm, trace=[])

# Run your program
# ...

# Inspect the last call
lm.inspect_history(n=1)
```
