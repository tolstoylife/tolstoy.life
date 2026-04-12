# Designing Signatures

Signatures are the declarative specifications of input/output behavior in DSPy. They replace manual prompt engineering by defining *what* the model should do, not *how* it should do it.

## When to Use

- Defining new DSPy modules
- Need structured/validated outputs
- Complex input/output relationships
- Multi-field responses

## Types of Signatures

### 1. Inline Signatures (String-based)
Best for simple, quick prototypes.

```python
import dspy

# Format: "input_field_1, input_field_2 -> output_field_1, output_field_2"
qa = dspy.Predict("question -> answer")
classifier = dspy.Predict("sentence -> sentiment: bool")
rag = dspy.ChainOfThought("context: list[str], question: str -> answer: str")
```

### 2. Class-based Signatures
Best for production, complex types, and detailed descriptions.

```python
import dspy
from typing import Literal

class EmotionClassifier(dspy.Signature):
    """Classify the emotion expressed in the text."""

    text: str = dspy.InputField(desc="The text to analyze")
    emotion: Literal['joy', 'sadness', 'anger', 'fear', 'surprise'] = dspy.OutputField()
    confidence: float = dspy.OutputField(desc="Confidence score 0-1")
```

## Field Configuration

### InputField
Inputs are the data you provide to the module.

```python
query = dspy.InputField(desc="The search query")
context = dspy.InputField(desc="Background information", format=lambda x: "\n".join(x))
```

### OutputField
Outputs are what the model generates.

```python
answer = dspy.OutputField(desc="Comprehensive answer")
reasoning = dspy.OutputField(desc="Step-by-step logic", prefix="Let's think about this:")
```

## Type Hints Reference

DSPy supports standard Python type hints to constrain generation and guide the model.

```python
from typing import Literal, Optional, List
from pydantic import BaseModel

# Basic types
field: str = dspy.InputField()
field: int = dspy.OutputField()
field: float = dspy.OutputField()
field: bool = dspy.OutputField()

# Collections
field: list[str] = dspy.InputField()
field: List[int] = dspy.OutputField()

# Optional
field: Optional[str] = dspy.OutputField()

# Constrained (Categorical)
field: Literal['a', 'b', 'c'] = dspy.OutputField()

# Pydantic models (Structured)
class Person(BaseModel):
    name: str
    age: int

field: Person = dspy.OutputField()
```

## Production Examples

### Summarization

```python
class Summarize(dspy.Signature):
    """Summarize the document into key points."""

    document: str = dspy.InputField(desc="Full document text")
    max_points: int = dspy.InputField(desc="Maximum bullet points", default=5)

    summary: list[str] = dspy.OutputField(desc="Key points as bullet list")
    word_count: int = dspy.OutputField(desc="Total words in summary")
```

### RAG with Confidence

```python
class GroundedAnswer(dspy.Signature):
    """Answer questions using retrieved context with confidence."""

    context: list[str] = dspy.InputField(desc="Retrieved passages")
    question: str = dspy.InputField()

    answer: str = dspy.OutputField(desc="Factual answer from context")
    confidence: Literal['high', 'medium', 'low'] = dspy.OutputField(
        desc="Confidence based on context support"
    )
    source_passage: int = dspy.OutputField(
        desc="Index of most relevant passage (0-based)"
    )
```

## Best Practices

1. **Descriptive Docstrings**: The class docstring is treated as the high-level task instruction. Make it clear and actionable.
2. **Field Descriptions**: Use `desc` to guide the model on specific fields.
3. **Constrain Outputs**: Use `Literal` for categorical outputs to enforce valid values.
4. **Structured Data**: Use Pydantic models with `dspy.TypedPredictor` for complex objects.
