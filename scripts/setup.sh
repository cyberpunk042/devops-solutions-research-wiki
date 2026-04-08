#!/usr/bin/env bash
# Master setup script — orchestrates all sub-scripts.
source "$(dirname "$0")/lib.sh"

usage() {
    cat << 'USAGE'
Usage: ./scripts/setup.sh [OPTIONS]

Options:
  --all           Run everything
  --deps          Install Python + system dependencies
  --obsidian      Install Obsidian + configure vault + generate wikilinks
  --exports       Configure sister project export directories
  --notebooklm    Install notebooklm-py + create stub skill
  --yes           Skip confirmation prompts
  -h, --help      Show this help

With no flags: interactive mode.
USAGE
}

# Parse flags
RUN_DEPS=false
RUN_OBSIDIAN=false
RUN_EXPORTS=false
RUN_NOTEBOOKLM=false
INTERACTIVE=true

while [[ $# -gt 0 ]]; do
    case "$1" in
        --all)
            RUN_DEPS=true; RUN_OBSIDIAN=true; RUN_EXPORTS=true; RUN_NOTEBOOKLM=true
            INTERACTIVE=false; shift ;;
        --deps)
            RUN_DEPS=true; INTERACTIVE=false; shift ;;
        --obsidian)
            RUN_OBSIDIAN=true; INTERACTIVE=false; shift ;;
        --exports)
            RUN_EXPORTS=true; INTERACTIVE=false; shift ;;
        --notebooklm)
            RUN_NOTEBOOKLM=true; INTERACTIVE=false; shift ;;
        --yes)
            export YES_FLAG=true; shift ;;
        -h|--help)
            usage; exit 0 ;;
        *)
            log_error "Unknown option: $1"; usage; exit 1 ;;
    esac
done

# Interactive mode
if [ "$INTERACTIVE" = "true" ]; then
    log_info "=== Research Wiki Setup ==="
    echo ""
    confirm_action "Install Python/system dependencies?" && RUN_DEPS=true
    confirm_action "Install and configure Obsidian?" && RUN_OBSIDIAN=true
    confirm_action "Configure sister project exports?" && RUN_EXPORTS=true
    confirm_action "Set up NotebookLM integration?" && RUN_NOTEBOOKLM=true
    echo ""
fi

SCRIPTS_DIR="$(dirname "$0")"

# Execute in order
if [ "$RUN_DEPS" = "true" ]; then
    bash "${SCRIPTS_DIR}/install-deps.sh"
    echo ""
fi

if [ "$RUN_OBSIDIAN" = "true" ]; then
    bash "${SCRIPTS_DIR}/install-obsidian.sh"
    echo ""
    bash "${SCRIPTS_DIR}/configure-obsidian.sh"
    echo ""
fi

if [ "$RUN_EXPORTS" = "true" ]; then
    bash "${SCRIPTS_DIR}/configure-exports.sh"
    echo ""
fi

if [ "$RUN_NOTEBOOKLM" = "true" ]; then
    bash "${SCRIPTS_DIR}/setup-notebooklm.sh"
    echo ""
fi

log_info "=== Setup complete ==="
