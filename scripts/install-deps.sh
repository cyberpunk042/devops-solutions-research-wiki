#!/usr/bin/env bash
# Install Python and system dependencies.
source "$(dirname "$0")/lib.sh"

log_info "=== Installing dependencies ==="

# System deps
if check_command wget; then
    log_info "wget already available"
else
    log_info "Installing wget..."
    sudo apt-get update && sudo apt-get install -y wget
fi

if check_command python3; then
    log_info "python3 already available"
else
    log_error "python3 not found — please install Python 3.8+"
    exit 1
fi

if check_command pip3; then
    log_info "pip3 already available"
else
    log_info "Installing pip3..."
    sudo apt-get update && sudo apt-get install -y python3-pip
fi

# Python deps
log_info "Installing Python dependencies from requirements.txt..."
pip3 install -r "${PROJECT_ROOT}/requirements.txt"

# Verify
python3 -c "import yaml; print('PyYAML', yaml.__version__)" && log_info "PyYAML OK" || log_error "PyYAML import failed"

log_info "=== Dependencies installed ==="
