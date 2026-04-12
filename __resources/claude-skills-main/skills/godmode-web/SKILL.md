---
name: godmode-web
description: Make HTTP requests, scrape web pages, download files, and send webhooks via GODMODE MCP. Tools — http_request, web_scrape, download_file, webhook_send.
allowed-tools: Read, Bash
---

# Godmode HTTP & Web

Web tools via GODMODE MCP.

## Tools

| Tool | Args | Description |
|------|------|-------------|
| `http_request` | `url`, `method`, `headers?`, `body?`, `follow_redirects?` | HTTP GET/POST/PUT/DELETE/PATCH |
| `web_scrape` | `url`, `extract?` (text/html/links/images/tables) | Scrape web page content |
| `download_file` | `url`, `output_path` | Download file from URL |
| `webhook_send` | `url`, `payload`, `headers?` | Send webhook (Slack, Discord, Zapier) |
