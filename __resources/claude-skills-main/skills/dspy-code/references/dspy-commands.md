# DSPy-Code Commands Reference

Complete reference for all dspy-code slash commands and their usage.

---

## `/init <project_name>`

**Purpose**: Initialize new DSPy project with recommended structure

**Syntax**:
```
/init <project_name> [--template <template>] [--lm <model>] [--retrieval]
```

**Arguments**:
- `project_name` (required) - Name of project directory to create
- `--template <name>` (optional) - Template to use (qa, rag, multi-hop, agent)
- `--lm <model>` (optional) - Language model (gpt-3.5-turbo, gpt-4, claude-3-opus, etc.)
- `--retrieval` (flag) - Include retrieval setup (ColBERTv2, vector DB)

**Created Structure**:
```
project_name/
├── modules/          # DSPy modules
│   └── __init__.py
├── data/            # Training/dev/test datasets
│   ├── train.json
│   ├── dev.json
│   └── test.json
├── metrics/         # Custom metrics
│   └── __init__.py
├── optimized/       # Saved optimized programs
├── tests/           # Unit tests
│   └── test_modules.py
├── config.py        # Configuration
├── requirements.txt # Dependencies
└── README.md        # Project documentation
```

**Examples**:
```bash
# Basic initialization
/init my-qa-bot

# With template
/init customer-support --template rag --lm gpt-4

# With retrieval
/init research-assistant --template multi-hop --retrieval

# Complete setup
/init production-app --template agent --lm gpt-4 --retrieval
```

**Generated Files**:

`config.py`:
```python
import dspy
import os

# Language Model Configuration
LM_MODEL = os.getenv("LM_MODEL", "gpt-3.5-turbo")
LM_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure DSPy
lm = dspy.OpenAI(model=LM_MODEL, api_key=LM_API_KEY)
dspy.settings.configure(lm=lm)

# Retrieval Configuration (if --retrieval flag used)
RETRIEVAL_URL = os.getenv("RETRIEVAL_URL", "http://localhost:2017")
rm = dspy.ColBERTv2(url=RETRIEVAL_URL)
dspy.settings.configure(rm=rm)
```

`requirements.txt`:
```
dspy-ai>=2.4.0
openai>=1.0.0
anthropic>=0.18.0  # if claude
sentence-transformers>=2.2.0  # if --retrieval
```

---

## `/connect`

**Purpose**: Connect to existing DSPy workspace and index codebase

**Syntax**:
```
/connect [<workspace_path>] [--reindex] [--verbose]
```

**Arguments**:
- `workspace_path` (optional) - Path to workspace (defaults to current directory)
- `--reindex` (flag) - Force reindexing of codebase
- `--verbose` (flag) - Show detailed indexing progress

**Actions Performed**:
1. Scan workspace for DSPy files (*.py)
2. Index modules, signatures, metrics
3. Load configuration from config.py
4. Resume or create session
5. Display workspace summary

**Output**:
```
Connected to workspace: /path/to/project
Session ID: session_abc123

Discovered:
  - 5 modules (QAModule, RAGPipeline, ...)
  - 8 signatures
  - 3 metrics (accuracy, f1_score, rouge_l)
  - 2 optimizers configured
  - 150 training examples

Configuration:
  - LM: gpt-3.5-turbo
  - Retrieval: ColBERTv2 (http://localhost:2017)
  - Cache: enabled
```

**Index Structure**:
```typescript
{
    workspace: "/path/to/project",
    indexed_at: "2024-01-15T10:30:00Z",
    modules: [
        {
            path: "modules/qa.py",
            name: "QAModule",
            signature: "question -> answer",
            type: "ChainOfThought"
        },
        // ...
    ],
    signatures: [
        {
            path: "modules/qa.py",
            definition: "question -> answer"
        },
        // ...
    ],
    metrics: [
        {
            path: "metrics/accuracy.py",
            name: "accuracy",
            type: "accuracy"
        },
        // ...
    ]
}
```

**Examples**:
```bash
# Connect to current directory
/connect

# Connect to specific workspace
/connect /path/to/dspy-project

# Force reindex
/connect --reindex

# Verbose output
/connect --verbose
```

---

## `/demo <template>`

**Purpose**: Generate demo code from production-ready templates

**Syntax**:
```
/demo <template> [--with-optimization] [--with-tests] [--output <path>]
```

**Arguments**:
- `template` (required) - Template name (see list below)
- `--with-optimization` (flag) - Include optimization example
- `--with-tests` (flag) - Include unit tests
- `--output <path>` (optional) - Custom output path

**Available Templates**:

1. **simple-qa** - Basic question answering
   - Predictor: ChainOfThought
   - Use case: Simple QA, classification
   - Complexity: ⭐

2. **rag** - Retrieval-augmented generation
   - Components: Retrieve + ChainOfThought
   - Use case: Knowledge-grounded QA
   - Complexity: ⭐⭐

3. **multi-hop** - Multi-step reasoning
   - Components: Multiple retrieval + generation steps
   - Use case: Complex reasoning, research
   - Complexity: ⭐⭐⭐

4. **typed-output** - Structured data extraction
   - Predictor: TypedPredictor with Pydantic
   - Use case: Data extraction, API integration
   - Complexity: ⭐⭐

5. **classification** - Multi-class classification
   - Predictor: ChainOfThought with labels
   - Use case: Sentiment analysis, categorization
   - Complexity: ⭐

6. **agent** - ReAct agent with tools
   - Predictor: ReAct
   - Use case: Autonomous agents, tool use
   - Complexity: ⭐⭐⭐⭐

7. **ensemble** - Multiple predictor voting
   - Components: Multiple predictors + majority
   - Use case: High accuracy, robustness
   - Complexity: ⭐⭐

8. **self-refining** - Iterative refinement
   - Components: Generate + Critique + Refine
   - Use case: Quality-critical outputs
   - Complexity: ⭐⭐⭐

9. **hinted-qa** - Guided reasoning with hints
   - Predictor: ChainOfThoughtWithHint
   - Use case: Educational, exam questions
   - Complexity: ⭐⭐

10. **program-of-thought** - Code generation for math
    - Predictor: ProgramOfThought
    - Use case: Mathematical reasoning
    - Complexity: ⭐⭐⭐

11. **chatbot** - Multi-turn conversation
    - Components: ChainOfThought + history
    - Use case: Chat, customer support
    - Complexity: ⭐⭐

12. **data-pipeline** - ETL workflow
    - Components: Extract + Transform + Validate
    - Use case: Data processing
    - Complexity: ⭐⭐⭐

**Examples**:
```bash
# Basic demo
/demo simple-qa

# With optimization example
/demo rag --with-optimization

# With tests
/demo multi-hop --with-tests

# Custom output
/demo agent --output agents/custom_agent.py

# Complete example
/demo rag --with-optimization --with-tests --output examples/rag_complete.py
```

**Output Format**:
```python
"""
Template: RAG Pipeline
Generated: 2024-01-15T10:30:00Z
Use case: Knowledge-grounded question answering
"""

import dspy

# Module Definition
class RAGPipeline(dspy.Module):
    # ... implementation ...

# Example Usage
if __name__ == "__main__":
    # ... usage example ...

# Optimization Example (if --with-optimization)
if __name__ == "__main__":
    # ... optimization workflow ...

# Unit Tests (if --with-tests)
import unittest

class TestRAGPipeline(unittest.TestCase):
    # ... tests ...
```

---

## `/optimize <module>`

**Purpose**: Run complete optimization workflow on DSPy module

**Syntax**:
```
/optimize <module> [--optimizer <type>] [--budget <N>] [--metric <name>] [--no-save] [--use-gepa]
```

**Arguments**:
- `module` (required) - Path to module file or class name
- `--optimizer <type>` (optional) - Force optimizer (bootstrap, mipro, copro, etc.)
- `--budget <N>` (optional) - Max optimization budget (LLM calls)
- `--metric <name>` (optional) - Use specific metric (accuracy, f1, etc.)
- `--no-save` (flag) - Don't save optimized program
- `--use-gepa` (flag) - Enable GEPA optimization

**Interactive Workflow**:

**Step 1: Load Module**
```
Loading module: modules/qa.py
Module: QAModule
Signature: question -> answer
Predictor: ChainOfThought
```

**Step 2: Training Data**
```
Training data:
  [1] Load from data/train.json
  [2] Use existing trainset variable
  [3] Enter data manually
  [4] Load from CSV/JSON file

Select option: 1
Loaded 100 examples from data/train.json
```

**Step 3: Metric Function**
```
Metric function:
  [1] accuracy (classification)
  [2] f1_score (multi-label)
  [3] rouge_l (text generation)
  [4] exact_match (strict)
  [5] Custom metric

Select option: 1
Using metric: accuracy
```

**Step 4: Optimizer Selection**
```
Recommended optimizer based on data size (100 examples): MIPRO

Available optimizers:
  [1] BootstrapFewShot (⚡⚡⚡ fast, ⭐⭐⭐ quality)
  [2] MIPRO (⚡ slow, ⭐⭐⭐⭐⭐ quality)
  [3] COPRO (⚡⚡ medium, ⭐⭐⭐⭐ quality)
  [4] KNNFewShot (⚡⚡ medium, ⭐⭐⭐⭐ quality)

Select optimizer [2]:
```

**Step 5: Compilation**
```
Compiling module with MIPRO...
Teacher model: gpt-4
Student model: gpt-3.5-turbo
Num trials: 20
Minibatch size: 50

Progress: [████████████████████] 20/20 trials
Best score: 0.87 (trial 15)
```

**Step 6: Evaluation**
```
Evaluating on dev set (20 examples)...
Dev score: 0.85

Baseline (unoptimized): 0.62
Optimized: 0.85
Improvement: +23%
```

**Step 7: Save**
```
Save optimized program? [Y/n]: Y
Saved to: optimized/qa_optimized_2024-01-15.json
```

**Examples**:
```bash
# Basic optimization
/optimize modules/qa.py

# Force optimizer
/optimize modules/rag.py --optimizer mipro

# With budget limit
/optimize modules/agent.py --budget 50

# Custom metric
/optimize modules/classifier.py --metric f1_score

# No save
/optimize modules/test.py --no-save

# GEPA optimization
/optimize modules/qa.py --use-gepa --budget 100

# Complete
/optimize modules/rag.py --optimizer mipro --metric accuracy --budget 100
```

---

## `/validate <file>`

**Purpose**: Validate DSPy code for correctness and best practices

**Syntax**:
```
/validate <file> [--strict] [--autofix]
```

**Arguments**:
- `file` (required) - Path to Python file or directory
- `--strict` (flag) - Treat warnings as errors
- `--autofix` (flag) - Automatically fix simple issues

**Validation Checks**:

**1. Import Statements**
- ✓ DSPy import present
- ✗ Direct LLM API imports (openai, anthropic)
- ⚠ Missing type hints

**2. Signature Format**
- ✓ Valid format: "input1, input2 -> output1, output2"
- ✗ Missing arrow (->)
- ✗ Invalid syntax

**3. Module Structure**
- ✓ Inherits from dspy.Module
- ✓ Has `__init__` method
- ✓ Has `forward` method
- ✓ Calls `super().__init__()`
- ⚠ Missing return type annotation

**4. Metric Functions**
- ✓ Correct signature: (example, prediction, trace=None)
- ✗ Missing trace parameter
- ⚠ No return type hint

**5. Anti-Patterns**
- ✗ Hardcoded prompts
- ✗ Direct LLM calls
- ✗ Monolithic functions (>100 lines)
- ⚠ String .format() instead of f-strings

**Output Format**:
```
=== DSPy Code Validation ===
Target: modules/qa.py

Checking Import Statements
✓ DSPy import found
⚠ WARNING: Direct OpenAI import found
💡 SUGGESTION: Replace with dspy.OpenAI(model=...)

Checking Signature Format
✓ Valid signature format: "question -> answer"

Checking Module Structure
✓ Module QAModule has __init__ method
✓ Module QAModule has forward method
✓ Module QAModule calls super().__init__()
💡 SUGGESTION: Add return type: def forward(...) -> dspy.Prediction

Checking Metric Functions
✓ Metric function accuracy has correct signature

=== Validation Summary ===
Errors:      0
Warnings:    1
Suggestions: 2

Validation PASSED
```

**Examples**:
```bash
# Validate single file
/validate modules/qa.py

# Validate directory
/validate modules/

# Strict mode
/validate modules/qa.py --strict

# Auto-fix
/validate modules/qa.py --autofix
```

---

## `/export <format>`

**Purpose**: Export module to target format

**Syntax**:
```
/export <format> [<module>] [--include-examples] [--include-tests] [--minify] [--output <path>]
```

**Arguments**:
- `format` (required) - Target format (python, json, yaml, markdown)
- `module` (optional) - Module to export (defaults to current)
- `--include-examples` (flag) - Include usage examples
- `--include-tests` (flag) - Include test code
- `--minify` (flag) - Remove comments and whitespace
- `--output <path>` (optional) - Custom output path

**Export Formats**:

**1. Python** - Executable Python code
```python
"""
Exported from DSPy module: QAModule
Generated: 2024-01-15T10:30:00Z
"""

import dspy

class QAModule(dspy.Module):
    # ... implementation ...

# Usage Example (if --include-examples)
if __name__ == "__main__":
    # ... example ...

# Unit Tests (if --include-tests)
import unittest
# ... tests ...
```

**2. JSON** - Structured configuration
```json
{
  "module": {
    "name": "QAModule",
    "type": "ChainOfThought",
    "signature": "question -> answer",
    "predictors": [...],
    "optimized": true,
    "optimizer": "MIPRO",
    "dev_score": 0.85
  },
  "examples": [...],
  "tests": [...]
}
```

**3. YAML** - Human-readable config
```yaml
module:
  name: QAModule
  type: ChainOfThought
  signature: "question -> answer"
  predictors:
    - qa: ChainOfThought
  optimized: true
  optimizer: MIPRO
  dev_score: 0.85

examples:
  - question: "What is DSPy?"
    answer: "..."
```

**4. Markdown** - Documentation
```markdown
# QAModule

**Type**: ChainOfThought
**Signature**: `question -> answer`
**Optimized**: Yes (MIPRO)
**Dev Score**: 0.85

## Usage

\`\`\`python
qa = QAModule()
result = qa(question="...")
\`\`\`

## Examples
...

## Tests
...
```

**Examples**:
```bash
# Export to Python
/export python modules/qa.py

# Export to JSON with examples
/export json --include-examples

# Export to YAML with tests
/export yaml modules/rag.py --include-tests

# Export to Markdown documentation
/export markdown --include-examples --include-tests

# Minified JSON
/export json --minify --output dist/qa.min.json

# Complete export
/export python modules/qa.py --include-examples --include-tests --output export/qa_complete.py
```

---

## Command Cheat Sheet

```bash
# Project Setup
/init my-project --template rag --lm gpt-4
/connect

# Development
/demo rag --with-optimization
/validate modules/qa.py
/validate modules/ --strict

# Optimization
/optimize modules/qa.py
/optimize modules/rag.py --optimizer mipro --budget 100
/optimize modules/agent.py --use-gepa

# Export
/export python modules/qa.py --include-examples
/export json --minify
/export markdown --include-examples --include-tests
```

---

## Best Practices

### 1. Always validate before optimizing
```bash
/validate modules/qa.py
/optimize modules/qa.py
```

### 2. Use appropriate optimizer for data size
```bash
# Small (10-50 examples)
/optimize modules/qa.py --optimizer bootstrap

# Medium (50-200 examples)
/optimize modules/qa.py --optimizer mipro

# Large (200+ examples)
/optimize modules/qa.py --optimizer miprov2
```

### 3. Export optimized programs
```bash
/optimize modules/qa.py
/export json --include-examples --output production/qa.json
```

### 4. Generate demos for learning
```bash
/demo rag --with-optimization --with-tests
```

### 5. Use strict validation in CI/CD
```bash
/validate modules/ --strict
```

---

**Last Updated**: 2025-12-02
