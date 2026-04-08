#!/usr/bin/env bash
# Shared functions for setup scripts.
# Source this at the top of every sub-script:
#   source "$(dirname "$0")/lib.sh"

# Auto-detect project root (parent of scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
WIKI_DIR="${PROJECT_ROOT}/wiki"
CONFIG_DIR="${PROJECT_ROOT}/config"

# Global flag — set by setup.sh --yes
YES_FLAG="${YES_FLAG:-false}"

# --- Logging ---

log_info() {
    echo -e "\033[0;32m[INFO]\033[0m $1"
}

log_warn() {
    echo -e "\033[0;33m[WARN]\033[0m $1"
}

log_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1" >&2
}

# --- Checks ---

check_command() {
    local cmd="$1"
    if command -v "$cmd" &>/dev/null; then
        log_info "$cmd is available"
        return 0
    else
        log_warn "$cmd is not installed"
        return 1
    fi
}

check_dpkg() {
    local pkg="$1"
    if dpkg -l "$pkg" &>/dev/null; then
        log_info "$pkg is installed"
        return 0
    else
        log_warn "$pkg is not installed"
        return 1
    fi
}

check_dir() {
    local dir="$1"
    local label="$2"
    if [ -d "$dir" ]; then
        log_info "$label found at $dir"
        return 0
    else
        log_warn "$label not found at $dir"
        return 1
    fi
}

# --- Interaction ---

confirm_action() {
    local prompt="$1"
    if [ "$YES_FLAG" = "true" ]; then
        return 0
    fi
    read -rp "$prompt [y/N] " response
    case "$response" in
        [yY][eE][sS]|[yY]) return 0 ;;
        *) return 1 ;;
    esac
}
