## Decision Matrix: Which Technique to Use

```
                           Need Examples?
                          /              \
                        No                Yes
                        |                  |
                Zero-shot CoT          Few-shot CoT
                        |                  |
                Need higher accuracy?  Need computation?
                /                \           |
              Yes               No          PAL
               |                |
    Self-Consistency    Done with CoT
               |
        Still not enough?
        /              \
      Yes              No
       |                |
  Problem decomposable?  Done
  /                    \
Yes                    No
 |                      |
Least-to-Most     Need exploration?
                  /              \
                Yes              No
                 |                |
          Tree of Thoughts   Need external info?
                             /              \
                           Yes              No
                            |                |
                          ReAct         Need iteration?
                                        /           \
                                      Yes           No
                                       |             |
                                   Reflexion      Use CoT
```

---

## Best Practices

### 1. Start Simple
Begin with Zero-shot CoT ("Let's think step by step"), then progress to more complex techniques if needed.

### 2. Match Technique to Task
- **Math/Logic**: CoT, PAL, Self-Consistency
- **Multi-hop QA**: ReAct, Least-to-Most
- **Creative/Puzzles**: Tree of Thoughts
- **Iterative Tasks**: Reflexion

### 3. Combine Techniques
Techniques are often complementary:
- ReAct + Self-Consistency for robust factual answers
- ToT + PAL for complex computational exploration
- Least-to-Most + Reflexion for hard multi-step problems

### 4. Prompt Engineering Tips
- Use clear step markers ("Step 1:", "First,", etc.)
- Include diverse exemplars covering edge cases
- Format consistently across examples
- Add verification steps ("Let me verify...")

---

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Using CoT for simple lookups | Adds unnecessary tokens and latency | Reserve for multi-step reasoning |
| Too few samples in Self-Consistency | Majority voting needs adequate samples | Use 5-10 samples minimum |
| Generic "think step by step" without checking output | Model may produce irrelevant reasoning | Validate reasoning quality, not just presence |
| Mixing techniques without understanding trade-offs | Computational cost without benefit | Understand when each technique adds value |
| Using PAL without code interpreter | Code generation is useless without execution | Ensure execution environment available |
| Not testing exemplar quality in few-shot CoT | Poor exemplars lead to poor reasoning | Validate exemplars solve problems correctly |
| Applying Tree of Thoughts to linear problems | Massive overhead for no benefit | Use ToT only when exploration needed |


---

## References

1. Wei, J. et al. (2022). "Chain of Thought Prompting Elicits Reasoning in Large Language Models." [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)

2. Kojima, T. et al. (2022). "Large Language Models are Zero-Shot Reasoners." [arXiv:2205.11916](https://arxiv.org/abs/2205.11916)

3. Wang, X. et al. (2022). "Self-Consistency Improves Chain of Thought Reasoning in Language Models." [arXiv:2203.11171](https://arxiv.org/abs/2203.11171)

4. Yao, S. et al. (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." [arXiv:2305.10601](https://arxiv.org/abs/2305.10601)

5. Zhou, D. et al. (2022). "Least-to-Most Prompting Enables Complex Reasoning in Large Language Models." [arXiv:2205.10625](https://arxiv.org/abs/2205.10625)

6. Yao, S. et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)

7. Gao, L. et al. (2022). "PAL: Program-aided Language Models." [arXiv:2211.10435](https://arxiv.org/abs/2211.10435)

8. Zhang, Z. et al. (2022). "Automatic Chain of Thought Prompting in Large Language Models." [arXiv:2210.03493](https://arxiv.org/abs/2210.03493)

9. Shinn, N. et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning." [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)
