---
name: godmode-text
description: Text processing and compression via GODMODE MCP — regex match/replace, text diff, text transforms (upper/lower/reverse/strip), and archive compress/decompress (zip/tar). Tools — regex_match, regex_replace, text_diff, text_transform, compress, decompress.
allowed-tools: Read, Bash
---

# Godmode Text & Compression

Text and archive tools via GODMODE MCP.

## Text Tools

| Tool | Args | Description |
|------|------|-------------|
| `regex_match` | `text`, `pattern`, `flags?` | Find regex matches |
| `regex_replace` | `text`, `pattern`, `replacement`, `flags?` | Regex replace |
| `text_diff` | `text1` or `file1`, `text2` or `file2` | Show diff |
| `text_transform` | `text`, `operation` (upper/lower/title/capitalize/swapcase/reverse/strip) | Transform text |

## Compression Tools

| Tool | Args | Description |
|------|------|-------------|
| `compress` | `files[]`, `output`, `format?` (zip/tar.gz/tar.bz2/tar.xz) | Create archive |
| `decompress` | `file`, `output_dir?` | Extract archive |
