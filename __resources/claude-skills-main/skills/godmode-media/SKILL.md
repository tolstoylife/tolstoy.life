---
name: godmode-media
description: Media processing via GODMODE MCP — PDF text extraction, OCR from images, Whisper audio transcription, YouTube download, and image resize/convert. Tools — pdf_to_text, image_to_text, audio_transcribe, youtube_download, image_resize, image_convert.
allowed-tools: Read, Bash
---

# Godmode Media Processing

Media tools via GODMODE MCP.

## Tools

| Tool | Args | Description |
|------|------|-------------|
| `pdf_to_text` | `file`, `pages?` | Extract text from PDF (requires poppler) |
| `image_to_text` | `file`, `language?` | OCR from image (requires tesseract) |
| `audio_transcribe` | `file`, `model?` (tiny/base/small/medium/large) | Whisper transcription |
| `youtube_download` | `url`, `output_path?`, `format?` (video/audio) | YouTube download (requires yt-dlp) |
| `image_resize` | `file`, `width?`, `height?`, `output?` | Resize image (macOS sips) |
| `image_convert` | `file`, `format` (png/jpeg/gif/bmp/tiff), `output?` | Convert image format |
