#!/usr/bin/env bash
# Download and install Obsidian .deb package.
source "$(dirname "$0")/lib.sh"

OBSIDIAN_VERSION="${OBSIDIAN_VERSION:-1.12.7}"
DEB_FILE="/tmp/obsidian_${OBSIDIAN_VERSION}.deb"
URL="https://github.com/obsidianmd/obsidian-releases/releases/download/v${OBSIDIAN_VERSION}/obsidian_${OBSIDIAN_VERSION}_amd64.deb"

log_info "=== Installing Obsidian v${OBSIDIAN_VERSION} ==="

# Check if already installed
if check_dpkg obsidian; then
    INSTALLED_VER=$(dpkg -l obsidian 2>/dev/null | grep obsidian | awk '{print $3}')
    log_info "Obsidian ${INSTALLED_VER} already installed"
    exit 0
fi

# Download
if [ -f "$DEB_FILE" ]; then
    log_info "Using cached download at $DEB_FILE"
else
    log_info "Downloading Obsidian v${OBSIDIAN_VERSION}..."
    wget -q --show-progress -O "$DEB_FILE" "$URL"
    if [ $? -ne 0 ]; then
        log_error "Download failed from $URL"
        exit 1
    fi
fi

# Install
log_info "Installing Obsidian..."
if ! confirm_action "This requires sudo to install the .deb package. Continue?"; then
    log_warn "Skipped Obsidian installation"
    exit 0
fi

sudo dpkg -i "$DEB_FILE"
if [ $? -ne 0 ]; then
    log_info "Fixing missing dependencies..."
    sudo apt-get install -f -y
fi

# Verify
if check_dpkg obsidian; then
    log_info "=== Obsidian installed successfully ==="
else
    log_error "Obsidian installation failed"
    exit 1
fi
