#!/usr/bin/env bash
# Install project dependencies using uv with Python 3.11 venv.
# Also sets up notebooklm-py and verifies Obsidian CLI.
#
# Usage: ./scripts/install-deps.sh [--yes]
source "$(dirname "$0")/lib.sh"

log_info "=== Installing dependencies ==="

VENV_DIR="${PROJECT_ROOT}/.venv"

# 1. Check uv
if ! check_command uv; then
    log_error "uv is required. Install: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 2. Create venv if needed
if [ ! -d "$VENV_DIR" ]; then
    log_info "Creating Python 3.11 venv via uv..."
    uv venv --python 3.11 "$VENV_DIR"
else
    log_info "Venv exists at $VENV_DIR"
fi

# 3. Install Python packages
log_info "Installing Python packages from requirements.txt..."
uv pip install -r "${PROJECT_ROOT}/requirements.txt"

# 4. Install Playwright chromium for notebooklm-py browser auth
log_info "Installing Playwright chromium (for notebooklm-py auth)..."
"${VENV_DIR}/bin/playwright" install chromium 2>/dev/null || log_warn "Playwright chromium install skipped"

# 5. Verify
log_info "Verifying installations..."
"${VENV_DIR}/bin/python" -c "import yaml; print(f'  PyYAML {yaml.__version__}')" 2>/dev/null && log_info "PyYAML OK"
"${VENV_DIR}/bin/python" -c "import youtube_transcript_api; print('  youtube-transcript-api OK')" 2>/dev/null
"${VENV_DIR}/bin/notebooklm" --version 2>/dev/null && log_info "notebooklm-py OK" || log_warn "notebooklm-py not working"

# 6. Check Obsidian CLI
if check_command obsidian; then
    log_info "Obsidian CLI found (requires running app for full functionality)"
else
    log_warn "Obsidian CLI not found — install Obsidian 1.12.7+ and enable CLI in Settings > General"
fi

# 7. Integration check
log_info "Integration status:"
"${VENV_DIR}/bin/python" -m tools.pipeline integrations

log_info "=== Dependencies installed ==="
log_info "Use: .venv/bin/python -m tools.pipeline <command>"
log_info "  Or: source .venv/bin/activate && python -m tools.pipeline <command>"
