---
name: godmode-crypto
description: Cryptographic and encoding operations via GODMODE MCP — hash generation (MD5/SHA), base64 encode/decode, UUID generation, and JWT token decoding. Tools — hash, base64_encode, base64_decode, uuid_generate, jwt_decode.
allowed-tools: Read, Bash
---

# Godmode Crypto & Encoding

Crypto tools via GODMODE MCP.

## Tools

| Tool | Args | Description |
|------|------|-------------|
| `hash` | `input` (text or file path), `algorithm` (md5/sha1/sha256/sha512) | Generate hash |
| `base64_encode` | `input` (text or file path) | Base64 encode |
| `base64_decode` | `input`, `output_file?` | Base64 decode |
| `uuid_generate` | `version?` (1/4), `count?` | Generate UUIDs |
| `jwt_decode` | `token` | Decode JWT without verification |
