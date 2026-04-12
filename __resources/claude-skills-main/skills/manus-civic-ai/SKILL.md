---
name: manus-civic-ai
description: Government AI policy guidance using NIST AI RMF, county-level best practices, and 13+ policy documents. Use for civic AI governance, responsible AI deployment in government, and policy compliance questions.
allowed-tools: Read, Bash, Grep, Glob
---

# Manus Civic AI Policy Agent

Government AI policy guidance via `~/manus-chatbot/agents/civic_ai_policy_agent.py`.

## Capabilities

- **NIST AI Risk Management Framework** guidance
- **County-level AI best practices** and governance frameworks
- **13+ policy documents** on government AI deployment
- **Responsible AI** principles for public sector
- AI ethics, transparency, and accountability guidance
- Data governance for government datasets

## Policy Documents Location

`~/Desktop/Government AI/` — Full corpus of government AI policy documents.

## API Access

```bash
# Route to civic AI agent
curl -X POST http://localhost:8000/api/v1/chat/message \
  -d '{"message": "What does NIST RMF say about AI transparency?", "agent": "civic_ai_policy"}'
```

## Use Cases

- Draft AI governance policies for local government
- Evaluate AI systems against NIST RMF
- Review AI procurement requirements
- Assess bias and fairness in government AI
- Create AI ethics guidelines for public agencies
