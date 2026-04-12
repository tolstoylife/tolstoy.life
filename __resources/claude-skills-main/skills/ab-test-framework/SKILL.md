---
name: ab-test-framework
description: Design A/B testing infrastructure. Handles experiment assignment, statistical significance calculation, and result analysis. Covers sample size estimation and common pitfalls.
---

# A/B Test Framework

Design and analyze A/B tests with statistical rigor.

## When to Use

- Need to test two versions of a feature
- Determining sample size before running an experiment
- Analyzing A/B test results for statistical significance
- Setting up experiment infrastructure

## Workflow

1. **Define hypothesis** — What metric will improve and by how much?
2. **Calculate sample size** — Based on baseline rate, MDE, power, significance
3. **Design assignment** — Consistent hashing by user ID for stable buckets
4. **Instrument** — Track variant assignment and conversion events
5. **Analyze** — Chi-squared or t-test, check for significance
6. **Decide** — Ship winner, iterate, or declare inconclusive

## Common Pitfalls

- Peeking at results too early (inflates false positives)
- Not accounting for multiple comparisons
- Sample ratio mismatch (unequal bucket sizes)
- Novelty effects or day-of-week bias
- Testing too many variants at once
