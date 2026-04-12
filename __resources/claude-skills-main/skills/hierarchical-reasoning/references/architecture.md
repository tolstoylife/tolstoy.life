# Hierarchical Reasoning Architecture

## Fundamental Principles

### Teleological Foundation: Why Hierarchy?

The hierarchical reasoning architecture solves a fundamental limitation of flat, single-pass processing: **the inability to simultaneously maintain abstract strategic coherence while executing detailed tactical operations**.

Human cognition operates across multiple timescales:
- **Strategic** (slow, 10-100s): Goal formation, problem framing, metacognition
- **Tactical** (medium, 1-10s): Method selection, approach design, planning
- **Operational** (fast, 100ms-1s): Execution, calculation, retrieval

This architecture mirrors that structure, enabling:
1. **Deep reasoning in single pass** - No autoregressive iteration needed
2. **Bidirectional refinement** - Bottom-up and top-down information flow
3. **Adaptive computation** - Convergence detection for efficiency
4. **Uncertainty awareness** - Explicit tracking of confidence at each level

### Irreducible Primitives

The system builds from four foundational elements:

1. **State Persistence**: Reasoning states (z_S, z_T, z_O) maintain context across iterations
2. **Temporal Hierarchy**: Nested cycles create multi-timescale processing
3. **Bidirectional Flow**: Information propagates both up and down the hierarchy
4. **Convergence Detection**: Adaptive halting based on state stability and confidence

## Architectural Components

### Three-Level Hierarchy

```
STRATEGIC (z_S)
    ↓ guides ↑ informs
TACTICAL (z_T)
    ↓ guides ↑ informs
OPERATIONAL (z_O)
```

**Strategic Level** (High-level module):
- **Purpose**: Abstract problem formulation, goal setting, metacognitive monitoring
- **Characteristics**: Slow updates, high abstraction, holistic perspective
- **Outputs**: Problem frames, success criteria, strategic constraints

**Tactical Level** (Mid-level module):
- **Purpose**: Method selection, approach design, algorithm choice
- **Characteristics**: Medium update frequency, moderate abstraction
- **Outputs**: Reasoning strategies, decomposition plans, verification methods

**Operational Level** (Low-level module):
- **Purpose**: Detailed computation, concrete reasoning, execution
- **Characteristics**: Fast updates, low abstraction, specific computations
- **Outputs**: Intermediate results, calculations, evidence gathering

### Information Flow Patterns

#### Top-Down Guidance

Strategic insights constrain and guide lower levels:
```python
tactical_input = strategic_state + problem_context
operational_input = tactical_state + strategic_state
```

#### Bottom-Up Refinement

Operational findings refine higher-level understanding:
```python
strategic_update = f(tactical_convergence, operational_evidence)
tactical_update = f(operational_results, strategic_goals)
```

### Convergence Mechanisms

#### State Convergence Score

Measures stability of reasoning state:
```
convergence(t) = 0.7 × similarity(state(t), state(t-1)) + 0.3 × confidence(t)
```

Where:
- `similarity`: Semantic similarity between consecutive states
- `confidence`: Model's self-assessed confidence in current state

#### Multi-Level Convergence Check

System converges when:
1. All levels exceed threshold (e.g., > 0.95), OR
2. Weighted average converges:
   ```
   weighted_conv = 0.5×strategic + 0.3×tactical + 0.2×operational
   ```

Weights reflect relative importance of strategic coherence.

## Implementation Patterns

### Initialization

States initialize with:
- Empty content (no preconceptions)
- Low confidence (0.0)
- High uncertainty (1.0)
- Zero convergence score

### Iterative Refinement Loop

```
for strategic_cycle in range(max_strategic):
    strategic_state = strategic_reasoning(problem, tactical_state)
    
    for tactical_cycle in range(max_tactical):
        tactical_state = tactical_reasoning(strategic_state, operational_state)
        
        for operational_cycle in range(max_operational):
            operational_state = operational_reasoning(strategic_state, tactical_state)
            
            if converged_across_all_levels():
                break
```

### Adaptive Computation Time (ACT)

The system can implement ACT through:
1. **Convergence-based halting**: Stop when states stabilize
2. **Q-learning halting**: Learn when to stop (future enhancement)
3. **Max-step constraint**: Prevent infinite loops

### Uncertainty Quantification

Each state tracks:
- **Confidence**: How certain the reasoning is
- **Uncertainty**: Epistemic uncertainty about conclusions
- **Convergence score**: How stable the state has become

These enable:
- Selective trust in conclusions
- Identification of areas needing more reasoning
- Graceful degradation under ambiguity

## Improvements Over Base HRM

### 1. Explicit Convergence Detection

Original HRM uses fixed iteration counts. This implementation:
- Monitors state stability across iterations
- Adaptively halts when converged
- Reports convergence diagnostics

### 2. Three-Level Hierarchy

Extends two-level (high/low) to three levels (strategic/tactical/operational):
- Better separation of concerns
- Clearer abstraction boundaries
- More aligned with cognitive science

### 3. Uncertainty Awareness

Tracks both confidence and uncertainty:
- Confidence: How certain we are about current conclusions
- Uncertainty: Recognition of unknowns and ambiguities
- Enables meta-reasoning about reasoning quality

### 4. General-Purpose Design

Not tied to specific task types (puzzles, etc.):
- Accepts arbitrary problems
- Flexible context handling
- Extensible to any reasoning domain

### 5. Rich Diagnostic Trace

Records complete reasoning trajectory:
- State evolution at each level
- Convergence progression
- Enables analysis and debugging

## Usage Patterns

### Basic Usage

```python
reasoner = HierarchicalReasoner(
    max_strategic_cycles=3,
    max_tactical_cycles=5,
    max_operational_cycles=7,
    convergence_threshold=0.95
)

result = reasoner.reason(
    problem="How can we optimize supply chain efficiency?",
    context={"domain": "logistics", "constraints": ["cost", "time"]}
)
```

### Interpreting Results

```python
# Check convergence
if result.converged:
    print(f"Converged after {result.total_iterations} iterations")
    print(f"Reason: {result.convergence_reason}")

# Examine final states
print(f"Strategic confidence: {result.strategic_state.confidence}")
print(f"Tactical convergence: {result.tactical_state.convergence_score}")
print(f"Operational uncertainty: {result.operational_state.uncertainty}")

# Review synthesis
print(result.final_synthesis)
```

### Trace Analysis

```python
# Examine reasoning trajectory
for entry in result.trace:
    print(f"Cycle {entry['cycle']} - {entry['level']}")
    print(f"  Confidence: {entry['state']['confidence']:.2f}")
    print(f"  Convergence: {entry['state']['convergence_score']:.2f}")
```

## Theoretical Foundations

### Cognitive Architecture Alignment

Inspired by:
- **ACT-R**: Production system with declarative/procedural distinction
- **SOAR**: Multiple problem spaces with chunking
- **Global Workspace Theory**: Hierarchical processing with selective attention

### Computational Efficiency

Advantages over alternatives:
- **vs. Chain-of-Thought**: More structured, convergence-aware
- **vs. Tree-of-Thought**: Single forward pass, no search overhead
- **vs. Flat transformers**: Explicit abstraction hierarchy

### Scaling Properties

- **Time complexity**: O(S × T × O) where S, T, O are cycle counts
- **Space complexity**: O(state_size) - constant memory per level
- **Convergence time**: Typically O(log(problem_complexity)) with good initialization

## Future Enhancements

### 1. Neural Implementation

Replace placeholder reasoning with actual neural modules:
- Transformer blocks with rotary embeddings
- Cross-attention between levels
- Learned halting via Q-learning

### 2. Meta-Learning

Adapt hyperparameters based on problem type:
- Learn optimal cycle counts per domain
- Adjust convergence thresholds
- Optimize level abstractions

### 3. Parallel Reasoning

Explore multiple hypotheses simultaneously:
- Beam search at strategic level
- Multiple tactical approaches
- Ensemble operational execution

### 4. Memory Integration

Add persistent knowledge base:
- Retrieve relevant past reasoning
- Build episodic memory
- Transfer learning across problems

### 5. Tool Integration

Enable operational level to use tools:
- Calculators for math
- Code execution for algorithms
- Web search for facts
