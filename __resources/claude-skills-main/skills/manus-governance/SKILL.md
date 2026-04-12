---
name: manus-governance
description: PII redaction, safety gates, NIST 800-53 audit logging, prompt scoring (9-dimension rubric), and model registry with versioned rollback. Use for compliance, content safety, and prompt quality management in the Manus platform.
allowed-tools: Read, Bash, Grep, Glob
---

# Manus Governance & Compliance

Compliance, safety, and quality tools in `~/manus-chatbot/governance/`.

## Modules

| Module | What It Does |
|--------|-------------|
| `pii_redaction.py` | Detect and redact SSN, CC, email, phone, addresses |
| `safety_gates.py` | Pre-deployment safety evaluation gates |
| `audit_logger.py` | NIST 800-53/FISMA compliant audit trail (20+ event types) |
| `prompt_scoring.py` | 9-dimension scoring: accuracy 30%, safety 25%, clarity, etc. Publish threshold 8.0 |
| `prompt_testing.py` | 3-test methodology: golden path, realistic, edge/adversarial |
| `model_registry.py` | Version control for models and prompts with rollback |
| `llm_executor.py` | Multi-provider prompt execution (OpenAI, Anthropic, Ollama, Azure) |
| `output_schemas.py` | Structured output: action items, triage, meeting summary, draft, review |
| `platform_rules.py` | Platform-specific constraints (M365 Copilot vs GPT) |
| `sharepoint_schema.py` | SharePoint content type mapping (17 fields) |

## CLI

```bash
cd ~/manus-chatbot
python -m governance.prompt_cli list          # List all prompts
python -m governance.prompt_cli show <name>   # Show prompt details
python -m governance.prompt_cli test <name>   # Run 3-test suite
python -m governance.prompt_cli score <name>  # Score against 9D rubric
python -m governance.prompt_cli promote <name> # Promote to production
```

## Scoring Dimensions

| Dimension | Weight | Measures |
|-----------|--------|----------|
| Accuracy | 30% | Factual correctness |
| Safety | 25% | Harmful content prevention |
| Clarity | 10% | Readability |
| Relevance | 10% | On-topic |
| Completeness | 10% | Covers all aspects |
| Tone | 5% | Appropriate register |
| Bias | 5% | Fairness |
| Format | 3% | Structure compliance |
| Citations | 2% | Source attribution |
