# Typed Outputs

For robust systems, you often need more than string outputs. `dspy.TypedPredictor` integrates Pydantic to enforce structured schemas.

## Usage

```python
import dspy
from pydantic import BaseModel, Field

# 1. Define Output Schema
class UserProfile(BaseModel):
    name: str
    age: int = Field(ge=0, le=120)
    interests: list[str]
    is_active: bool

# 2. Define Signature
class ExtractUser(dspy.Signature):
    """Extract user details from bio."""
    bio: str = dspy.InputField()
    profile: UserProfile = dspy.OutputField()

# 3. Use TypedPredictor
predictor = dspy.TypedPredictor(ExtractUser)

# 4. Run
result = predictor(bio="Alice is a 25 year old coder who loves hiking.")
user = result.profile  # This is a UserProfile instance

print(user.name)      # "Alice"
print(user.interests) # ["coding", "hiking"]
```

## Benefits

1. **Type Safety**: Returns actual Python objects, not dicts or JSON strings.
2. **Validation**: Pydantic validates fields (e.g., age range). If validation fails, DSPy (via `TypedPredictor`) automatically feeds the error back to the LM to correct it.
3. **Schema Injection**: The Pydantic schema is automatically converted to JSON schema and injected into the prompt, helping the model understand the required format.

## Comparison with `Predict`

- `dspy.Predict`: Good for free-form text.
- `dspy.TypedPredictor`: Essential for API integrations, databases, and downstream code consumption.
