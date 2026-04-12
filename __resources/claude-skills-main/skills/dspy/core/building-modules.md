# Building Modules

Modules are the building blocks of DSPy programs. They wrap Signatures with execution logic, parameter management, and optimization capabilities.

## Core Modules

### 1. dspy.Predict
The fundamental unit. It takes a Signature and executes it directly.

```python
# Inline
predictor = dspy.Predict("question -> answer")

# Class-based
class QA(dspy.Signature):
    question = dspy.InputField()
    answer = dspy.OutputField()

predictor = dspy.Predict(QA)
result = predictor(question="Hello")
```

**Use when:** You need a simple, direct response without reasoning.

### 2. dspy.ChainOfThought
Adds a "reasoning" step before the output. This significantly improves performance on complex tasks.

```python
cot = dspy.ChainOfThought("question -> answer")
result = cot(question="What is 15% of 80?")

print(result.rationale) # "Let's think step by step..."
print(result.answer)    # "12"
```

**Use when:** The task requires logic, math, or multi-step deduction.

### 3. dspy.ReAct
An agent loop that can use tools. It iterates through Thought -> Action -> Observation cycles.

```python
def search(query): ...
def calculate(expr): ...

react = dspy.ReAct("question -> answer", tools=[search, calculate])
result = react(question="Population of France / 2?")
```

**Use when:** You need to retrieve external information or perform actions.

### 4. dspy.ProgramOfThought
Generates and executes Python code to solve problems (especially math/logic).

```python
pot = dspy.ProgramOfThought("question -> answer")
result = pot(question="If train A leaves at...")
```

**Use when:** The problem requires precise calculation or algorithmic logic.

## Composition

You can build complex systems by composing modules within a custom `dspy.Module`.

### Sequential Pipeline

```python
class Pipeline(dspy.Module):
    def __init__(self):
        super().__init__()
        self.stage1 = dspy.Predict("input -> intermediate")
        self.stage2 = dspy.ChainOfThought("intermediate -> output")

    def forward(self, input):
        intermediate = self.stage1(input=input).intermediate
        output = self.stage2(intermediate=intermediate).output
        return dspy.Prediction(output=output)
```

### RAG Pattern

```python
class RAG(dspy.Module):
    def __init__(self, k=3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=k)
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)
```

## Batch Processing

All modules support `batch` for efficient processing of multiple inputs.

```python
questions = ["Q1", "Q2", "Q3"]
results = predictor.batch([{"question": q} for q in questions])
```

## Saving and Loading

Modules (including their learned parameters from optimization) can be saved to JSON.

```python
# Save
module.save("my_module.json")

# Load
loaded_module = MyModule()
loaded_module.load("my_module.json")
```
