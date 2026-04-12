# Evaluation Methodologies

This reference provides detailed methodologies for evaluating Claude Code agents, including evaluation challenges, rubric design, test set construction, and context engineering evaluation.

## Evaluation Challenges

### Non-Determinism and Multiple Valid Paths

Agents may take completely different valid paths to reach goals. One agent might search three sources while another searches ten. They might use different tools to find the same answer. Traditional evaluations that check for specific steps fail in this context.

**Solution**: The solution is outcomes, not exact execution paths. Judge whether the agent achieves the right result through a reasonable process.

### Context-Dependent Failures

Agent failures often depend on context in subtle ways. An agent might succeed on complex queries but fail on simple ones. It might work well with one tool set but fail with another. Failures may emerge only after extended interaction when context accumulates.

**Solution**: Evaluation must cover a range of complexity levels and test extended interactions, not just isolated queries.

### Composite Quality Dimensions

Agent quality is not a single dimension. It includes factual accuracy, completeness, coherence, tool efficiency, and process quality. An agent might score high on accuracy but low in efficiency, or vice versa.

An agent might score high on accuracy but low in efficiency.

**Solution**: Evaluation rubrics must capture multiple dimensions with appropriate weighting for the use case.

## Evaluation Rubric Design

### Multi-Dimensional Rubric

Effective rubrics cover key dimensions with descriptive levels:

**Instruction Following** (weight: 0.30)

- Excellent (1.0): All instructions followed precisely
- Good (0.8): Minor deviations that don't affect outcome
- Acceptable (0.6): Major instructions followed, minor ones missed
- Poor (0.3): Significant instructions ignored
- Failed (0.0): Fundamentally misunderstood the task

**Output Completeness** (weight: 0.25)

- Excellent: All requested aspects thoroughly covered
- Good: Most aspects covered with minor gaps
- Acceptable: Key aspects covered, some gaps
- Poor: Major aspects missing
- Failed: Fundamental aspects not addressed

**Tool Efficiency** (weight: 0.20)

- Excellent: Optimal tool selection and minimal calls
- Good: Good tool selection with minor inefficiencies
- Acceptable: Appropriate tools with some redundancy
- Poor: Wrong tools or excessive calls
- Failed: Severe tool misuse or extremely excessive calls

**Reasoning Quality** (weight: 0.15)

- Excellent: Clear, logical reasoning throughout
- Good: Generally sound reasoning with minor gaps
- Acceptable: Basic reasoning present
- Poor: Reasoning unclear or flawed
- Failed: No apparent reasoning

**Response Coherence** (weight: 0.10)

- Excellent: Well-structured, easy to follow
- Good: Generally coherent with minor issues
- Acceptable: Understandable but could be clearer
- Poor: Difficult to follow
- Failed: Incoherent

### Scoring Approach

Convert dimension assessments to numeric scores (0.0 to 1.0) with appropriate weighting. Calculate weighted overall scores. Set passing thresholds based on use case requirements (typically 0.7 for general use, 0.85 for critical operations).

## Evaluation Methodologies

### LLM-as-Judge

Using an LLM to evaluate agent outputs scales well and provides consistent judgments. Design evaluation prompts that capture the dimensions of interest. LLM-based evaluation scales to large test sets and provides consistent judgments. The key is designing effective evaluation prompts that capture the dimensions of interest.

Provide clear task description, agent output, ground truth (if available), evaluation scale with level descriptions, and request structured judgment.

**Evaluation Prompt Template**:

```markdown
You are evaluating the output of a Claude Code agent.

## Original Task
{task_description}

## Agent Output
{agent_output}

## Ground Truth (if available)
{expected_output}

## Evaluation Criteria
For each criterion, assess the output and provide:
1. Score (1-5)
2. Specific evidence supporting your score
3. One improvement suggestion

### Criteria
1. Instruction Following: Did the agent follow all instructions?
2. Completeness: Are all requested aspects covered?
3. Tool Efficiency: Were appropriate tools used efficiently?
4. Reasoning Quality: Is the reasoning clear and sound?
5. Response Coherence: Is the output well-structured?

Provide your evaluation as a structured assessment with scores and justifications.
```

**Chain-of-Thought Requirement**: Always require justification before the score. Research shows this improves reliability by 15-25% compared to score-first approaches.

### Human Evaluation

Human evaluation catches what automation misses:

- Hallucinated answers on unusual queries
- Subtle context misunderstandings
- Edge cases that automated evaluation overlooks
- Qualitative issues with tone or approach

For Claude Code development, ask users this:

- Review agent outputs manually for edge cases
- Sample systematically across complexity levels
- Track patterns in failures to inform prompt improvements

### End-State Evaluation

For commands that produce artifacts (files, configurations, code), evaluate the final output rather than the process:

- Does the generated code work?
- Is the configuration valid?
- Does the output meet requirements?

## Test Set Design

**Sample Selection**
Start with small samples during development. Early in agent development, changes have dramatic impacts because there is abundant low-hanging fruit. Small test sets reveal large effects.

Sample from real usage patterns. Add known edge cases. Ensure coverage across complexity levels.

**Complexity Stratification**
Test sets should span complexity levels: simple (single tool call), medium (multiple tool calls), complex (many tool calls, significant ambiguity), and very complex (extended interaction, deep reasoning).

## Context Engineering Evaluation

### Testing Prompt Variations

When iterating on Claude Code prompts, evaluate systematically:

1. **Baseline**: Run current prompt on test cases
2. **Variation**: Run modified prompt on same cases
3. **Compare**: Measure quality scores, token usage, efficiency
4. **Analyze**: Identify which changes improved which dimensions

### Testing Context Strategies

Context engineering choices should be validated through systematic evaluation. Run agents with different context strategies on the same test set. Compare quality scores, token usage, and efficiency metrics.

### Degradation Testing

Test how context degradation affects performance by running agents at different context sizes. Identify performance cliffs where context becomes problematic. Establish safe operating limits.

## Rubric Generation

Well-defined rubrics reduce evaluation variance by 40-60% compared to open-ended scoring.

### Rubric Components

1. **Level descriptions**: Clear boundaries for each score level
2. **Characteristics**: Observable features that define each level
3. **Examples**: Representative outputs for each level (when possible)
4. **Edge cases**: Guidance for ambiguous situations
5. **Scoring guidelines**: General principles for consistent application

### Strictness Calibration

- **Lenient**: Lower bar for passing scores, appropriate for encouraging iteration
- **Balanced**: Fair, typical expectations for production use
- **Strict**: High standards, appropriate for safety-critical or high-stakes evaluation

### Domain Adaptation

Rubrics should use domain-specific terminology:

- A "code readability" rubric mentions variables, functions, and comments.
- Documentation rubrics reference clarity, accuracy, completeness
- Analysis rubrics focus on depth, accuracy, actionability

## Practical Guidance

### Evaluation Pipeline Design

Production evaluation systems require multiple layers:

```
┌─────────────────────────────────────────────────┐
│                 Evaluation Pipeline              │
├─────────────────────────────────────────────────┤
│                                                   │
│  Input: Response + Prompt + Context               │
│           │                                       │
│           ▼                                       │
│  ┌─────────────────────┐                         │
│  │   Criteria Loader   │ ◄── Rubrics, weights    │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  ┌─────────────────────┐                         │
│  │   Primary Scorer    │ ◄── Direct or Pairwise  │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  ┌─────────────────────┐                         │
│  │   Bias Mitigation   │ ◄── Position swap, etc. │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  ┌─────────────────────┐                         │
│  │ Confidence Scoring  │ ◄── Calibration         │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  Output: Scores + Justifications + Confidence     │
│                                                   │
└─────────────────────────────────────────────────┘
```

### Avoiding Evaluation Pitfalls

**Anti-pattern: Scoring without justification**

- Problem: Scores lack grounding, difficult to debug or improve
- Solution: Always require evidence-based justification before score

**Anti-pattern: Single-pass pairwise comparison**

- Problem: Position bias corrupts results
- Solution: Always swap positions and check consistency

**Anti-pattern: Overloaded criteria**

- Problem: Criteria measuring multiple things are unreliable
- Solution: One criterion = one measurable aspect

**Anti-pattern: Missing edge case guidance**

- Problem: Evaluators handle ambiguous cases inconsistently
- Solution: Include edge cases in rubrics with explicit guidance

**Anti-pattern: Ignoring confidence calibration**

- Problem: High-confidence wrong judgments are worse than low-confidence
- Solution: Calibrate confidence to position consistency and evidence strength

### Decision Framework: Direct vs. Pairwise

Use this decision tree:

```
Is there an objective ground truth?
├── Yes → Direct Scoring
│   └── Examples: factual accuracy, instruction following, format compliance
│
└── No → Is it a preference or quality judgment?
    ├── Yes → Pairwise Comparison
    │   └── Examples: tone, style, persuasiveness, creativity
    │
    └── No → Consider reference-based evaluation
        └── Examples: summarization (compare to source), translation (compare to reference)
```

### Scaling Evaluation

For high-volume evaluation:

1. **Panel of LLMs (PoLL)**: Use multiple models as judges, aggregate votes
   - Reduces individual model bias
   - More expensive but more reliable for high-stakes decisions

2. **Hierarchical evaluation**: Fast cheap model for screening, expensive model for edge cases
   - Cost-effective for large volumes
   - Requires calibration of screening threshold

3. **Human-in-the-loop**: Automated evaluation for clear cases, human review for low-confidence
   - Best reliability for critical applications
   - Design feedback loop to improve automated evaluation

## Guidelines

1. **Always require justification before scores** - Chain-of-thought prompting improves reliability by 15-25%

2. **Always swap positions in pairwise comparison** - Single-pass comparison is corrupted by position bias

3. **Match scale granularity to rubric specificity** - Don't use 1-10 without detailed level descriptions

4. **Separate objective and subjective criteria** - Use direct scoring for objective, pairwise for subjective

5. **Include confidence scores** - Calibrate to position consistency and evidence strength

6. **Define edge cases explicitly** - Ambiguous situations cause the most evaluation variance

7. **Use domain-specific rubrics** - Generic rubrics produce generic (less useful) evaluations

8. **Validate against human judgments** - Automated evaluation is only valuable if it correlates with human assessment

9. **Monitor for systematic bias** - Track disagreement patterns by criterion and response type

10. **Design for iteration** - Evaluation systems improve with feedback loops

## Example: Evaluating a Claude Code Command

Suppose you've created a `/refactor` command and want to evaluate its quality:

**Test Cases**:

1. Simple: Rename a variable across a single file
2. Medium: Extract a function from existing code
3. Complex: Refactor a class to use a new design pattern
4. Very Complex: Restructure module dependencies

**Evaluation Rubric**:

- Correctness: Does the refactored code work?
- Completeness: Were all instances updated?
- Style: Does it follow project conventions?
- Efficiency: Were unnecessary changes avoided?

**Evaluation Prompt**:

```markdown
Evaluate this refactoring output:

Original Code:
{original}

Refactored Code:
{refactored}

Request:
{user_request}

Score 1-5 on each dimension with evidence:
1. Correctness: Does the code still work correctly?
2. Completeness: Were all relevant instances updated?
3. Style: Does it follow the project's coding patterns?
4. Efficiency: Were only necessary changes made?

Provide scores with specific evidence from the code.
```

**Iteration**:
If evaluation reveals the command often misses instances:

1. Add explicit instruction: "Search the entire codebase for all occurrences"
2. Re-evaluate with same test cases
3. Compare completeness scores
4. Check that correctness didn't regress

## Iterative Improvement Workflow

1. **Identify weakness**: Use evaluation to find where agent struggles
2. **Hypothesize cause**: Is it the prompt? The context? The examples?
3. **Modify prompt**: Make targeted changes based on hypothesis
4. **Re-evaluate**: Run same test cases with modified prompt
5. **Compare**: Did the change improve the target dimension?
6. **Check regression**: Did other dimensions suffer?
7. **Iterate**: Repeat until quality meets threshold
