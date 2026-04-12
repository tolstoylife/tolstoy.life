---
name: manus-user-profiles
description: Role-based user personalization (developer, job_seeker, general) with behavioral intent tracking, proactive suggestions, and async SQLite storage. Adapts agent responses based on user history and preferences.
allowed-tools: Read, Bash, Grep, Glob
---

# Manus User Profiles & Intent Tracking

Personalization system in `~/manus-chatbot/agents/`.

## Modules

| Module | Purpose |
|--------|---------|
| `user_profiles.py` | Role-based personalization (developer, job_seeker, general) |
| `user_intent_tracker.py` | Behavioral learning, intent sequences, proactive suggestions |
| `storage.py` | Async SQLite storage for profiles and preferences |

## User Roles

| Role | Adaptations |
|------|------------|
| `developer` | Technical responses, code-first, CLI examples |
| `job_seeker` | Career focus, resume tips, job market data |
| `general` | Balanced, conversational, accessible language |

## Intent Tracking

Tracks user intent sequences over time to:
- Predict next likely request
- Offer proactive suggestions
- Adapt response depth and format
- Build behavioral profiles for better routing
