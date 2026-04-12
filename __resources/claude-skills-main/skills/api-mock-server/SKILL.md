---
name: api-mock-server
description: Generate mock API servers for development and testing. Creates realistic mock endpoints from OpenAPI specs, example responses, or existing API calls with configurable latency and error simulation.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - WebFetch
  - WebSearch
---

# API Mock Server

Generate mock API servers for development and testing.

## When to Use

- Frontend needs to develop against an API that doesn't exist yet
- Integration tests need deterministic API responses
- Need to simulate error conditions (timeouts, 500s, rate limits)
- Prototyping API designs before implementation

## Workflow

1. **Define endpoints** — From OpenAPI spec, example curl commands, or description
2. **Generate responses** — Realistic mock data with proper types and relationships
3. **Create server** — Standalone mock server (Express, FastAPI, or json-server)
4. **Add behaviors** — Latency simulation, error injection, stateful responses
5. **Record/replay** — Capture real API responses for replay in tests

## Output Formats

- **json-server** — Zero-code REST API from a JSON file
- **Express/Node** — Full control with middleware
- **FastAPI/Python** — Typed endpoints with auto-docs
- **MSW (Mock Service Worker)** — Browser/Node request interception
