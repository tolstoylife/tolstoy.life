# Assertions & Validation

DSPy Assertions allow you to impose constraints on LM outputs and automatically recover from failures.

## `dspy.Assert` vs `dspy.Suggest`

- **Assert**: Hard constraint. If failed, it triggers a retry loop. If retries run out, it raises an error (unless handled).
- **Suggest**: Soft constraint. If failed, it triggers a retry loop. If retries run out, it logs the failure but continues with the best attempt.

## Usage

```python
import dspy

class SafeQA(dspy.Module):
    def __init__(self):
        self.generate = dspy.Predict("question -> answer")

    def forward(self, question):
        pred = self.generate(question=question)

        # Constraint: Answer must be short
        dspy.Suggest(
            len(pred.answer) < 100,
            "Please keep the answer under 100 characters."
        )

        # Constraint: Must not contain PII
        dspy.Assert(
            "email" not in pred.answer,
            "Do not include email addresses."
        )

        return pred
```

## Backtracking

To enable the retry logic, you must wrap your module execution with `dspy.assert_transform_module`.

```python
from dspy.primitives.assertions import assert_transform_module, backtrack_handler

# Transform the module to handle assertions
safe_qa = assert_transform_module(SafeQA(), backtrack_handler)

# Now running it will automatically retry with feedback if constraints fail
result = safe_qa(question="Give me a long answer with an email.")
```

## How it works
When an assertion fails, DSPy captures the failure message and re-prompts the model:
*"The previous output failed validation: [Message]. Please try again..."*

This "self-correction" loop significantly improves reliability without complex manual loops.
