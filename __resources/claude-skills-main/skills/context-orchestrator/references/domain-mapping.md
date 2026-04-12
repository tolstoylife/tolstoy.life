# Domain to CLI Mapping

## Primary Mappings

| Domain | Keywords | Primary CLI | Secondary | Confidence |
|--------|----------|-------------|-----------|------------|
| **Personal/Life** | lifelog, pendant, meeting, daily, yesterday, conversation, told me, discussed | limitless | pieces | High |
| **Technical Docs** | documentation, how to, tutorial, guide, implementation | research | pieces | High |
| **Code History** | my code, I wrote, previous solution, saved, snippet, LTM | pieces | limitless | High |
| **Verification** | fact-check, verify, confirm, is it true, accurate | research | - | High |
| **Medical/PEX** | pex, medical, clinical, prescription, treatment, grounding | research | limitless | High |
| **Academic** | research, paper, study, citation, journal | research | - | Medium |
| **API/SDK** | api, sdk, method, function, endpoint | research | pieces | Medium |
| **Calendar/Errands** | appointment, schedule, calendar, reminder, to-do | limitless | - | High |
| **Projects** | project, working on, task, implementation | pieces | limitless | Medium |

## Cross-Domain Patterns

### Combined Queries (→ Parallel Mode)

| Pattern | Example | CLIs |
|---------|---------|------|
| Personal + Technical | "How did we decide to implement auth?" | limitless + research |
| Code + Discussion | "What approach did I use and why?" | pieces + limitless |
| All Sources | "/context" or comprehensive query | all three |

### Temporal Indicators

| Timeframe | Preferred CLI | Command Pattern |
|-----------|---------------|-----------------|
| Today | limitless | `workflow daily $(date)` |
| Yesterday | limitless | `workflow daily $(date -v-1d)` |
| Last week | limitless | `workflow recent --hours 168` |
| This month | pieces | `ask --ltm` (better for code history) |
| Older history | pieces | `ask --ltm` (3+ months coverage) |

## Confidence Thresholds

```yaml
high_confidence: 0.8+
  action: Invoke immediately

medium_confidence: 0.5-0.8
  action: Invoke with lower priority

low_confidence: <0.5
  action: Skip unless explicit command
```

## Fallback Rules

```yaml
limitless_unavailable:
  fallback: pieces (for code discussions)
  note: Personal context lost, focus on work history

research_unavailable:
  fallback: pieces (for cached docs in snippets)
  note: Online context lost, use local knowledge

pieces_unavailable:
  fallback: limitless (for code discussions)
  note: LTM lost, rely on conversation memory
```
