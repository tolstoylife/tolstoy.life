# Organized Search

Search the indexed Organized folder (Manatee County AI Program materials) via ChromaDB RAG.

## When to use

Use when the user asks about:
- AI governance documents, NIST AI RMF, vendor assessments (SVAQ)
- Presentation materials, demo runbooks, prompt playbook
- EPE goals, performance review content
- Microfiche/records management processing
- Any content from `~/Desktop/Organized/`

## How to search

Run the organized_manager.py CLI:

```bash
python3 ~/scripts/organized_manager.py search "YOUR QUERY" -n 5
```

### Examples

```bash
# Find SVAQ vendor assessment details
python3 ~/scripts/organized_manager.py search "SVAQ vendor assessment framework"

# Find demo runbook timing
python3 ~/scripts/organized_manager.py search "demo timing field notes"

# Find NIST risk framework content
python3 ~/scripts/organized_manager.py search "NIST AI risk management"

# Find EPE goal ROI numbers
python3 ~/scripts/organized_manager.py search "Copilot license ROI savings"
```

## Other commands

```bash
# Show what's indexed
python3 ~/scripts/organized_manager.py status

# Reindex everything
python3 ~/scripts/organized_manager.py reindex

# Ingest new files only
python3 ~/scripts/organized_manager.py ingest
```

## Folder structure

```
~/Desktop/Organized/
├── Governance/          8 files — NIST, Georgia, Maryland, GovAI, readiness
├── Presentation/       10 files — deck, runbooks, cheat sheet, QR code
├── Prompt-Engineering/  3 files — strategies, playbook content
├── Performance/         2 files — EPE goals (regenerate: epe), mid-year draft
├── Data/                4 files — inventories, SR list, pipeline diagram
├── Records-Management/  2 files — microfiche processing report + package
├── Reference/           2 files — Anthropic context engineering, audio analysis
├── Screenshots/         2 files + debug/ subfolder
└── Resources/           watcher.log
```

## Automation

- **Auto-indexer**: `com.organized.watcher` launchd agent polls every 30s
- **EPE generator**: Edit `~/scripts/epe_goals.yaml` → run `epe`
- **Header generator**: Run `forms-header`
- **ChromaDB**: `~/.ml-toolkit-mcp/chroma/` collection `organized` (508+ chunks)
