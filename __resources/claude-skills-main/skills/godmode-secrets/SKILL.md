---
name: godmode-secrets
description: Multi-cloud secret management via GODMODE MCP — HashiCorp Vault (KV v2), AWS Secrets Manager, and Azure Key Vault with versioning and rotation workflows. Tools — vault_read, vault_write, vault_list, aws_secret_get, azure_keyvault_get, secret_rotate.
allowed-tools: Read, Bash
---

# Godmode Secret Management

Multi-cloud secrets via GODMODE MCP.

## Tools

| Tool | Args | Description |
|------|------|-------------|
| `vault_read` | `path`, `version?` | Read from HashiCorp Vault KV |
| `vault_write` | `path`, `data`, `cas?` | Write to Vault (check-and-set) |
| `vault_list` | `path`, `recursive?` | List Vault secrets |
| `aws_secret_get` | `secret_id`, `version_id?`, `version_stage?` | AWS Secrets Manager |
| `azure_keyvault_get` | `vault_url`, `secret_name`, `version?` | Azure Key Vault |
| `secret_rotate` | `provider` (vault/aws/azure), `path`, `strategy?` (immediate/staged) | Trigger rotation |
