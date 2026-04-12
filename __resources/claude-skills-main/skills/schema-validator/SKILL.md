---
name: schema-validator
description: Validate data against schemas. Generate JSON Schema, Zod, Pydantic, or TypeScript validators from examples. Catch data quality issues before they reach your database.
---

# Schema Validator

Generate and apply data validation schemas.

## When to Use

- Need to validate API request/response bodies
- Generating TypeScript types from JSON examples
- Creating Pydantic models from API documentation
- Validating config files or data imports

## Supported Formats

| Format | Language | Use Case |
|--------|----------|----------|
| JSON Schema | Any | API specs, config validation |
| Zod | TypeScript | Runtime validation + type inference |
| Pydantic | Python | FastAPI models, data validation |
| TypeScript | TypeScript | Compile-time type checking |
| io-ts | TypeScript | Runtime codec validation |

## Workflow

1. **Input** — JSON examples, API docs, or natural language description
2. **Infer schema** — Detect types, optionality, patterns, constraints
3. **Generate validator** — In the requested format
4. **Add constraints** — min/max, patterns, enums, custom rules
5. **Test** — Generate test cases for valid and invalid data
