# notebooklm-py — Official Documentation

Source: https://github.com/teng-lin/notebooklm-py
Fetched: 2026-04-08

## Overview

Unofficial Python API and agentic skill for Google NotebookLM. Full programmatic access to NotebookLM's features — including capabilities the web UI doesn't expose — via Python, CLI, and AI agents like Claude Code, Codex, and OpenClaw.

## Requirements

- Python 3.10+
- Tested on macOS, Linux, Windows
- Browser required for initial authentication

## Installation

```bash
pip install notebooklm-py
pip install "notebooklm-py[browser]"
playwright install chromium
```

## Authentication

- `notebooklm login` — Opens browser for Google OAuth
- `notebooklm login --browser msedge` — Edge for SSO orgs
- `notebooklm auth check --test` — Diagnose auth issues
- Credentials stored at ~/.notebooklm/profiles/default/storage_state.json
- Environment variable: NOTEBOOKLM_AUTH_JSON for CI/CD

## CLI Commands

### Session & Auth
- notebooklm login, status, auth check [--test]
- notebooklm profile create <name>, profile switch <name>

### Notebooks
- notebooklm list, create "<title>", use <id>, delete <id>, rename <id> "<title>"
- notebooklm metadata --json

### Sources
- notebooklm source add <url|path|text>
- notebooklm source list, source wait <id> [--timeout], source delete <id>, source fulltext <id>
- notebooklm source add-research "<query>" — web research with auto-import

### Chat
- notebooklm ask "<question>" [--json] [-s <source_id>] [--save-as-note]

### Generation
- notebooklm generate audio [--wait] (4 formats, 3 lengths, 50+ languages)
- notebooklm generate video [--style <style>] [--wait] (3 formats, 9 styles)
- notebooklm generate cinematic-video "<instructions>" [--wait]
- notebooklm generate quiz [--difficulty <level>] [--wait]
- notebooklm generate flashcards [--quantity <n>] [--wait]
- notebooklm generate slide-deck [--wait]
- notebooklm generate infographic [--orientation <o>] [--wait]
- notebooklm generate mind-map [--wait]
- notebooklm generate data-table "<description>" [--wait]
- notebooklm generate report [--wait]

### Downloads
- notebooklm download audio ./file.mp3
- notebooklm download video ./file.mp4
- notebooklm download cinematic-video ./file.mp4
- notebooklm download quiz ./file [--format json|markdown|html]
- notebooklm download flashcards ./file [--format json|markdown|html]
- notebooklm download slide-deck ./file.pdf (or .pptx)
- notebooklm download infographic ./file.png
- notebooklm download mind-map ./file.json
- notebooklm download data-table ./file.csv
- notebooklm download report ./file.pdf

### Sharing
- notebooklm share status

### Utilities
- notebooklm language list (50+ languages)
- notebooklm agent show codex|claude
- notebooklm skill install, skill status

### Global Flags
- -n/--notebook <id>, -p/--profile <name>, --storage <path>, --retry, --wait

## Python API

### Client
- NotebookLMClient — main async client
- NotebookLMClient.from_storage() — init from local credentials

### Namespaces
- client.notebooks — create, list, get, rename, delete
- client.sources — add_url, add_text, add_file, list, delete
- client.chat — ask, get_history
- client.artifacts — generate_*, download_*, wait_for_completion
- client.research — start_fast_research, start_deep_research, poll_status
- client.notes — create, list, delete
- client.sharing — manage permissions and links

## Features Beyond Web UI

- Batch artifact downloads
- Structured quiz/flashcard export (JSON, Markdown, HTML)
- Mind map JSON extraction
- Data table CSV export
- Slide deck PPTX format
- Individual slide revision with natural language
- Report template customization
- Save chat to notebook notes
- Programmatic sharing
- Web research with auto-import

## Agent Integration

- `notebooklm skill install` — installs to ~/.claude/skills/notebooklm and ~/.agents/skills/notebooklm
- `npx skills add teng-lin/notebooklm-py` — via open skills ecosystem
- Works with Claude Code, Codex, OpenClaw

## Stats (as of 2026-04)

- 9.5k GitHub stars, 1.2k forks, 655 commits
- MIT licensed
- v0.3.4 latest (March 2026)
