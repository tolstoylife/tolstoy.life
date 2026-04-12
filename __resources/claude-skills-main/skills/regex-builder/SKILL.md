---
name: regex-builder
description: Build, explain, test, and debug regular expressions. Translates natural language descriptions into regex patterns with test cases. Supports Python, JavaScript, Go, and PCRE flavors.
---

# Regex Builder

Translates natural language intent into correct, tested regular expressions.

## When to Use

- User needs a regex for validation (email, phone, URL, etc.)
- User has a regex that doesn't work and needs debugging
- User wants to understand what an existing regex does
- Need to convert regex between flavors (Python ↔ JS ↔ Go)

## Workflow

1. **Clarify intent** — What should match? What should NOT match? Get example strings.
2. **Choose flavor** — Detect from project context or ask (Python `re`, JS, Go `regexp`, PCRE)
3. **Build pattern** — Write the regex with named groups where helpful
4. **Explain it** — Break down each component in plain English
5. **Test it** — Generate test cases covering: valid matches, near-misses, edge cases, empty input
6. **Optimize** — Avoid catastrophic backtracking, use atomic groups or possessive quantifiers where supported

## Flavor Differences to Track

- **Go:** No lookahead/lookbehind, no backreferences (RE2 engine)
- **JavaScript:** No atomic groups, limited lookbehind in older engines
- **Python:** Full PCRE-like support via `re` module
- Always note flavor limitations when the requested pattern can't be expressed
