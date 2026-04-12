# Integrating Haystack

DSPy can be used to optimize prompts within Haystack pipelines.

## Goal
Use DSPy's optimization capabilities to automatically improve prompts in Haystack components.

## Workflow

1. **Build Haystack Pipeline**: Create your standard pipeline.
2. **Wrap in DSPy**: Create a DSPy module that mimics the pipeline's structure (or calls the pipeline components).
3. **Optimize**: Run DSPy optimizer (e.g., `BootstrapFewShot`).
4. **Extract Prompt**: Get the optimized prompt/examples from the compiled DSPy module.
5. **Update Haystack**: Inject the optimized prompt back into the Haystack `PromptBuilder`.

## Example: Optimizing a Haystack Retriever-Generator

```python
# 1. DSPy Module wrapping Haystack components
class HaystackRAG(dspy.Module):
    def __init__(self, haystack_retriever):
        self.retriever = haystack_retriever
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        # Call Haystack retriever
        results = self.retriever.run(query=question)
        context = [d.content for d in results['documents']]

        # Call DSPy generator
        return self.generate(context=context, question=question)

# 2. Optimize
optimizer = BootstrapFewShot(metric=my_metric)
compiled_rag = optimizer.compile(HaystackRAG(my_retriever), trainset)

# 3. Extract Prompt
demos = compiled_rag.generate.demos
# Format 'demos' into a Jinja2 template string for Haystack
```

## Why do this?
Haystack is great for infrastructure (document stores, file conversion, complex routing). DSPy is great for *programmatic prompt optimization*. Combining them gives you robust infrastructure with self-optimizing intelligence.
