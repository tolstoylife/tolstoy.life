## Core Capabilities

### 1. Few-Shot Learning

Teach the model by showing examples instead of explaining rules. Include 2-5 input-output pairs that demonstrate the desired behavior. Use when you need consistent formatting, specific reasoning patterns, or handling of edge cases. More examples improve accuracy but consume tokens—balance based on task complexity.

**Example:**

```markdown
Extract key information from support tickets:

Input: "My login doesn't work and I keep getting error 403"
Output: {"issue": "authentication", "error_code": "403", "priority": "high"}

Input: "Feature request: add dark mode to settings"
Output: {"issue": "feature_request", "error_code": null, "priority": "low"}

Now process: "Can't upload files larger than 10MB, getting timeout"
```

### 2. Chain-of-Thought Prompting

Request step-by-step reasoning before the final answer. Add "Let's think step by step" (zero-shot) or include example reasoning traces (few-shot). Use for complex problems requiring multi-step logic, mathematical reasoning, or when you need to verify the model's thought process. Improves accuracy on analytical tasks by 30-50%.

**Example:**

```markdown
Analyze this bug report and determine root cause.

Think step by step:
1. What is the expected behavior?
2. What is the actual behavior?
3. What changed recently that could cause this?
4. What components are involved?
5. What is the most likely root cause?

Bug: "Users can't save drafts after the cache update deployed yesterday"
```

### 3. Prompt Optimization

Systematically improve prompts through testing and refinement. Start simple, measure performance (accuracy, consistency, token usage), then iterate. Test on diverse inputs including edge cases. Use A/B testing to compare variations. Critical for production prompts where consistency and cost matter.

**Example:**

```markdown
Version 1 (Simple): "Summarize this article"
→ Result: Inconsistent length, misses key points

Version 2 (Add constraints): "Summarize in 3 bullet points"
→ Result: Better structure, but still misses nuance

Version 3 (Add reasoning): "Identify the 3 main findings, then summarize each"
→ Result: Consistent, accurate, captures key information
```

### 4. Template Systems

Build reusable prompt structures with variables, conditional sections, and modular components. Use for multi-turn conversations, role-based interactions, or when the same pattern applies to different inputs. Reduces duplication and ensures consistency across similar tasks.

**Example:**

```python
# Reusable code review template
template = """
Review this {language} code for {focus_area}.

Code:
{code_block}

Provide feedback on:
{checklist}
"""

# Usage
prompt = template.format(
    language="Python",
    focus_area="security vulnerabilities",
    code_block=user_code,
    checklist="1. SQL injection\n2. XSS risks\n3. Authentication"
)
```

### 5. System Prompt Design

Set global behavior and constraints that persist across the conversation. Define the model's role, expertise level, output format, and safety guidelines. Use system prompts for stable instructions that shouldn't change turn-to-turn, freeing up user message tokens for variable content.

**Example:**

```markdown
System: You are a senior backend engineer specializing in API design.

Rules:
- Always consider scalability and performance
- Suggest RESTful patterns by default
- Flag security concerns immediately
- Provide code examples in Python
- Use early return pattern

Format responses as:
1. Analysis
2. Recommendation
3. Code example
4. Trade-offs
```

## Key Patterns

### Progressive Disclosure

Start with simple prompts, add complexity only when needed:

1. **Level 1**: Direct instruction
   - "Summarize this article"

2. **Level 2**: Add constraints
   - "Summarize this article in 3 bullet points, focusing on key findings"

3. **Level 3**: Add reasoning
   - "Read this article, identify the main findings, then summarize in 3 bullet points"

4. **Level 4**: Add examples
   - Include 2-3 example summaries with input-output pairs

### Instruction Hierarchy

```
[System Context] → [Task Instruction] → [Examples] → [Input Data] → [Output Format]
```

### Error Recovery

Build prompts that gracefully handle failures:

- Include fallback instructions
- Request confidence scores
- Ask for alternative interpretations when uncertain
- Specify how to indicate missing information

## Best Practices

1. **Be Specific**: Vague prompts produce inconsistent results
2. **Show, Don't Tell**: Examples are more effective than descriptions
3. **Test Extensively**: Evaluate on diverse, representative inputs
4. **Iterate Rapidly**: Small changes can have large impacts
5. **Monitor Performance**: Track metrics in production
6. **Version Control**: Treat prompts as code with proper versioning
7. **Document Intent**: Explain why prompts are structured as they are

## Common Pitfalls

- **Over-engineering**: Starting with complex prompts before trying simple ones
- **Example pollution**: Using examples that don't match the target task
- **Context overflow**: Exceeding token limits with excessive examples
- **Ambiguous instructions**: Leaving room for multiple interpretations
- **Ignoring edge cases**: Not testing on unusual or boundary inputs

## Integration Patterns

### With RAG Systems

```python
# Combine retrieved context with prompt engineering
prompt = f"""Given the following context:
{retrieved_context}

{few_shot_examples}

Question: {user_question}

Provide a detailed answer based solely on the context above. If the context doesn't contain enough information, explicitly state what's missing."""
```

### With Validation

```python
# Add self-verification step
prompt = f"""{main_task_prompt}

After generating your response, verify it meets these criteria:
1. Answers the question directly
2. Uses only information from provided context
3. Cites specific sources
4. Acknowledges any uncertainty

If verification fails, revise your response."""
```

## Performance Optimization

### Token Efficiency

- Remove redundant words and phrases
- Use abbreviations consistently after first definition
- Consolidate similar instructions
- Move stable content to system prompts

### Latency Reduction

- Minimize prompt length without sacrificing quality
- Use streaming for long-form outputs
- Cache common prompt prefixes
- Batch similar requests when possible

### 6. Self-Consistency (Multiple Reasoning Paths)

Generate multiple classification/reasoning paths and aggregate by majority vote. Reduces single-path errors by 10-20% on classification tasks. Use when a single prompt gives inconsistent results across similar inputs.

**Pattern:**

```python
import asyncio
from collections import Counter

async def classify_with_self_consistency(message: str, classify_fn, num_paths: int = 3) -> dict:
    """Run N diverse classification paths and return majority vote."""
    # Generate diverse paths with different prompting strategies
    strategies = [
        f"Classify this message directly: {message}",
        f"Think step by step about the intent, then classify: {message}",
        f"Consider what domain this belongs to, then determine intent: {message}",
    ]

    results = await asyncio.gather(*[
        classify_fn(strategies[i % len(strategies)])
        for i in range(num_paths)
    ])

    # Majority vote
    votes = Counter(r["intent"] for r in results if "intent" in r)
    winner, count = votes.most_common(1)[0]

    return {
        "intent": winner,
        "confidence": count / num_paths,
        "agreement": count,
        "total_paths": num_paths,
        "all_votes": dict(votes),
    }
```

**When to use:**
- Classification accuracy below 80%
- Ambiguous inputs that could map to multiple categories
- High-stakes routing where misclassification is costly

**When NOT to use:**
- Latency-sensitive paths (3x API calls)
- Simple, unambiguous inputs
- Token-budget-constrained contexts

### 7. Negative Prompting

Specify what to exclude from outputs to constrain generation. Combines exclusion lists, constraint functions, and iterative refinement.

**Pattern:**

```python
# Exclusion-based prompt
negative_prompt = """Classify the user's intent.

Do NOT classify as:
- "general_question" if the message contains domain-specific terms
- "coding_task" if the user is asking ABOUT code, not asking to WRITE code
- "research_task" if the user wants a direct answer, not a research report

Excluded behaviors:
- Do not hedge with multiple intents when one is clearly dominant
- Do not default to general_question when confidence is low — pick the best match

Message: {message}
Intent:"""

# Programmatic constraint validation
def validate_output(output: str, constraints: dict) -> dict:
    """Validate output against negative constraints."""
    results = {}
    for name, check_fn in constraints.items():
        results[name] = check_fn(output)
    return results

constraints = {
    "no_excluded_words": lambda x: all(w not in x.lower() for w in ["maybe", "perhaps", "unclear"]),
    "single_intent": lambda x: x.count(",") == 0,
    "not_empty": lambda x: len(x.strip()) > 0,
}
```

**Key insight:** Negative prompts are most effective when they target *specific known failure modes*, not generic quality. Audit your classification errors first, then write negative constraints for the top 5 failure patterns.

### 8. Evaluation Framework

Systematic prompt evaluation using relevance scoring, consistency scoring, and A/B comparison. Essential for production prompts.

**Pattern:**

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def relevance_score(response: str, expected: str) -> float:
    """Semantic similarity between response and expected content."""
    embeddings = model.encode([response, expected])
    return float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])

def consistency_score(responses: list[str]) -> float:
    """How consistent are N responses to the same prompt."""
    if len(responses) < 2:
        return 1.0
    similarities = []
    for i in range(len(responses)):
        for j in range(i + 1, len(responses)):
            similarities.append(relevance_score(responses[i], responses[j]))
    return float(np.mean(similarities))

def evaluate_prompt(prompt_fn, test_cases: list[dict]) -> dict:
    """Evaluate a prompt function against labeled test cases.

    test_cases: [{"input": "...", "label": "expected_output"}, ...]
    """
    correct = 0
    results = []
    for case in test_cases:
        prediction = prompt_fn(case["input"]).strip()
        is_correct = prediction.lower() == case["label"].lower()
        correct += int(is_correct)
        results.append({"input": case["input"], "predicted": prediction,
                        "expected": case["label"], "correct": is_correct})
    return {"accuracy": correct / len(test_cases), "results": results}

def compare_prompts(prompt_fns: dict, test_cases: list[dict]) -> dict:
    """A/B test multiple prompt variants on the same test cases."""
    return {name: evaluate_prompt(fn, test_cases) for name, fn in prompt_fns.items()}
```

**Production checklist:**
1. Define 20+ labeled test cases covering all categories
2. Include 5+ edge cases (ambiguous, multi-intent, adversarial)
3. Run `evaluate_prompt` on current prompt → baseline accuracy
4. Modify prompt → re-run → compare
5. Track accuracy over time as categories or data change

---

# Agent Prompting Best Practices

Based on Anthropic's official best practices for agent prompting.

