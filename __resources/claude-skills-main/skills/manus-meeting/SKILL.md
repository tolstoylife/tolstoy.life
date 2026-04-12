---
name: manus-meeting
description: Meeting recording with OpenAI Whisper transcription, speaker diarization, audio enhancement, and Google Drive upload for NotebookLM integration. Auto-capture and enhanced transcription pipelines.
allowed-tools: Read, Bash, Grep, Glob
---

# Manus Meeting Transcription

Audio transcription and meeting intelligence in `~/manus-chatbot/`.

## Modules

| Module | Purpose |
|--------|---------|
| `audio_transcription.py` | OpenAI Whisper speech-to-text |
| `audio_enhancer.py` | Audio preprocessing for WhisperX accuracy |
| `meeting_transcriber.py` | Meeting recording with speaker diarization |
| `meeting_transcriber_enhanced.py` | Enhanced meeting transcription pipeline |
| `auto_meeting_recorder.py` | Automated meeting capture |
| `google_drive_uploader.py` | Upload transcripts to Google Drive for NotebookLM |

## Workflow

1. **Record** — Auto-capture or manual recording
2. **Enhance** — Audio preprocessing (noise reduction, normalization)
3. **Transcribe** — Whisper STT with timestamp alignment
4. **Diarize** — Speaker identification and labeling
5. **Upload** — Push to Google Drive for NotebookLM analysis

## Usage

```python
from meeting_transcriber_enhanced import EnhancedMeetingTranscriber
transcriber = EnhancedMeetingTranscriber()
result = transcriber.transcribe("meeting.wav", diarize=True)
```

## Also Available via Godmode MCP

```
godmode.audio_transcribe(file="meeting.wav", model="base")
```
