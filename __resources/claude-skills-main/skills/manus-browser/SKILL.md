---
name: manus-browser
description: Browser automation agent using Playwright and Selenium via the Manus platform. Web scraping, form filling, screenshot capture, and headless browsing with MCP integration.
allowed-tools: Read, Bash, Grep, Glob
---

# Manus Browser Agent

Browser automation via `~/manus-chatbot/agents/implementations/browser_agent.py`.

## Capabilities

- **Playwright** headless browser automation
- **Selenium** WebDriver support
- Web page navigation and interaction
- Form filling and submission
- Screenshot capture
- Element inspection and data extraction
- Cookie and session management
- JavaScript execution in page context

## MCP Servers

| Server | File | Purpose |
|--------|------|---------|
| `manus_mcp_server.py` | Manus browser MCP | Exposes browser automation via MCP protocol |
| `antigravity_mcp_server.py` | VS Code MCP | IDE browser integration |

## Also via Godmode

```
godmode.web_scrape(url="...", extract="text|html|links|images|tables")
```

## API Access

```bash
curl -X POST http://localhost:8000/api/v1/chat/message \
  -d '{"message": "Go to example.com and extract the main heading", "agent": "browser"}'
```
