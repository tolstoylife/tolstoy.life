---
name: godmode-macos
description: macOS-native automation via GODMODE MCP — AppleScript, notifications, clipboard, screenshots, Keychain secrets, Spotlight search, window management, and text-to-speech. 12 macOS tools.
allowed-tools: Read, Bash
---

# Godmode macOS Native

macOS automation via GODMODE MCP.

## Tools

| Tool | Args | Description |
|------|------|-------------|
| `applescript` | `code` | Execute AppleScript |
| `open_app` | `name` or `path`, `background?` | Open application or file |
| `notification` | `title`, `message`, `subtitle?`, `sound?` | Show macOS notification |
| `clipboard_get` | — | Get clipboard contents |
| `clipboard_set` | `content` | Set clipboard contents |
| `screenshot` | `type?` (fullscreen/region/window), `path?` | Take screenshot |
| `keychain_get` | `service`, `account` | Get Keychain password |
| `keychain_set` | `service`, `account`, `password` | Set Keychain password |
| `spotlight_search` | `query`, `kind?` (app/document/folder/image/pdf) | Spotlight search |
| `window_list` | — | List all open windows |
| `window_focus` | `app?`, `title?` | Focus/activate a window |
| `say` | `text`, `voice?`, `rate?` | Text-to-speech |
