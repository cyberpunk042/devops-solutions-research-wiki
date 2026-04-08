#!/usr/bin/env bash
# Install notebooklm-py and create stub skill for NotebookLM integration.
source "$(dirname "$0")/lib.sh"

log_info "=== Setting up NotebookLM integration ==="

# Attempt to install notebooklm-py
log_info "Attempting to install notebooklm-py..."
if pip3 install notebooklm-py 2>/dev/null; then
    log_info "notebooklm-py installed successfully"
else
    log_warn "notebooklm-py not available via pip"
    log_warn "Try manual install: pip3 install git+https://github.com/nicktang/notebooklm-py.git"
    log_warn "Or check: https://github.com/nicktang/notebooklm-py"
fi

# Check for existing auth
if [ -f "$HOME/.notebooklm/credentials.json" ]; then
    log_info "NotebookLM credentials found at ~/.notebooklm/credentials.json"
else
    log_warn "NotebookLM not authenticated"
    log_warn "After installing notebooklm-py, run: notebooklm auth"
    log_warn "This will open Chrome for Google account login"
fi

# Create stub skill if not present
SKILL_DIR="${PROJECT_ROOT}/skills/notebooklm"
SKILL_FILE="${SKILL_DIR}/skill.md"

if [ -f "$SKILL_FILE" ]; then
    log_info "NotebookLM skill already exists at $SKILL_FILE"
else
    mkdir -p "$SKILL_DIR"
    cat > "$SKILL_FILE" << 'SKILL'
# NotebookLM Integration — Stub

This skill will connect the research wiki to Google NotebookLM.

## Status: Not yet configured

To set up:
1. Install: `pip3 install notebooklm-py`
2. Authenticate: `notebooklm auth` (opens Chrome for Google login)
3. Replace this stub with the full NotebookLM skill

## Planned Capabilities

- Push wiki pages as NotebookLM sources
- Create notebooks organized by domain
- Query wiki content through NotebookLM's grounded chat
- Generate audio/video summaries of research domains

## Usage (once configured)

```
Hey Claude, push the knowledge-systems domain into a NotebookLM notebook.
Hey Claude, create a NotebookLM notebook from my latest research.
```
SKILL
    log_info "Created stub skill at $SKILL_FILE"
fi

log_info "=== NotebookLM setup complete ==="
