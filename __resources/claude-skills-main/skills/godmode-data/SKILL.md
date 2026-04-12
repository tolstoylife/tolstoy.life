---
name: godmode-data
description: Parse and query structured data via GODMODE MCP. JQ-like JSON queries, CSV to JSON, YAML to JSON, XML to JSON conversion. Tools — json_query, csv_parse, yaml_parse, xml_parse.
allowed-tools: Read, Bash
---

# Godmode Data Parsing

Structured data tools via GODMODE MCP.

## Tools

| Tool | Args | Description |
|------|------|-------------|
| `json_query` | `data` or `file`, `query` (dot-path) | JQ-like JSON query |
| `csv_parse` | `file`, `delimiter?`, `has_header?` | CSV to JSON |
| `yaml_parse` | `file` | YAML to JSON |
| `xml_parse` | `file` | XML to JSON |
