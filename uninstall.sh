#!/bin/sh
# Paprwall Uninstallation Script
# Simple, clean, POSIX-compliant uninstaller
# Usage: curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/uninstall.sh | sh

set -e

# Configuration
INSTALL_DIR="$HOME/.paprwall"
CONFIG_DIR="$HOME/.config/paprwall"
DATA_DIR="$HOME/.local/share/paprwall"
BIN_DIR="$HOME/.local/bin"
SERVICE_FILE="$HOME/.config/systemd/user/paprwall.service"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    printf "\n${BLUE}========================================${NC}\n"
    printf "${BLUE}  Paprwall Uninstaller${NC}\n"
    printf "${BLUE}========================================${NC}\n\n"
}

print_success() {
    printf "${GREEN}✓${NC} %s\n" "$1"
}

print_error() {
    printf "${RED}✗${NC} %s\n" "$1"
}

print_warning() {
    printf "${YELLOW}⚠${NC} %s\n" "$1"
}

print_info() {
    printf "${BLUE}ℹ${NC} %s\n" "$1"
}

print_header

# Check if installed
FOUND_INSTALLATION=0

if [ -d "$INSTALL_DIR" ]; then
    FOUND_INSTALLATION=1
fi

if [ -f "$BIN_DIR/paprwall" ] || [ -f "$BIN_DIR/paprwall-gui" ]; then
    FOUND_INSTALLATION=1
fi

if [ $FOUND_INSTALLATION -eq 0 ]; then
    print_warning "Paprwall does not appear to be installed"
    printf "\nNothing to uninstall.\n\n"
    exit 0
fi

# Show what will be removed
print_warning "This will completely remove Paprwall from your system"
printf "\n"
printf "The following will be removed:\n"

if [ -d "$INSTALL_DIR" ]; then
    printf "  • ${YELLOW}%s${NC}\n" "$INSTALL_DIR"
fi

if [ -d "$CONFIG_DIR" ]; then
    printf "  • ${YELLOW}%s${NC}\n" "$CONFIG_DIR"
fi

if [ -d "$DATA_DIR" ]; then
    printf "  • ${YELLOW}%s${NC} (downloaded wallpapers)\n" "$DATA_DIR"
fi

if [ -f "$BIN_DIR/paprwall" ]; then
    printf "  • ${YELLOW}%s${NC}\n" "$BIN_DIR/paprwall"
fi

if [ -f "$BIN_DIR/paprwall-gui" ]; then
    printf "  • ${YELLOW}%s${NC}\n" "$BIN_DIR/paprwall-gui"
fi

if [ -f "$SERVICE_FILE" ]; then
    printf "  • ${YELLOW}%s${NC}\n" "$SERVICE_FILE"
fi

printf "\n"

# Ask for confirmation (only in interactive mode)
if [ -t 0 ]; then
    printf "Continue with uninstallation? (y/N): "
    read -r REPLY
    case "$REPLY" in
        [Yy]*)
            ;;
        *)
            print_info "Uninstallation cancelled"
            exit 0
            ;;
    esac
    printf "\n"
fi

# Start uninstallation
print_info "Uninstalling Paprwall..."
printf "\n"

# Stop and disable systemd service
if command -v systemctl >/dev/null 2>&1; then
    if systemctl --user is-active paprwall >/dev/null 2>&1; then
        print_info "Stopping service..."
        systemctl --user stop paprwall 2>/dev/null || true
        print_success "Service stopped"
    fi

    if systemctl --user is-enabled paprwall >/dev/null 2>&1; then
        print_info "Disabling service..."
        systemctl --user disable paprwall 2>/dev/null || true
        print_success "Service disabled"
    fi

    if [ -f "$SERVICE_FILE" ]; then
        rm -f "$SERVICE_FILE"
        systemctl --user daemon-reload 2>/dev/null || true
        print_success "Service file removed"
    fi
fi

# Remove virtualenv and installation
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    print_success "Removed installation directory"
fi

# Remove config
if [ -d "$CONFIG_DIR" ]; then
    rm -rf "$CONFIG_DIR"
    print_success "Removed configuration directory"
fi

# Remove data (downloaded wallpapers)
if [ -d "$DATA_DIR" ]; then
    rm -rf "$DATA_DIR"
    print_success "Removed data directory (wallpapers)"
fi

# Remove command wrappers
if [ -f "$BIN_DIR/paprwall" ]; then
    rm -f "$BIN_DIR/paprwall"
    print_success "Removed paprwall command"
fi

if [ -f "$BIN_DIR/paprwall-gui" ]; then
    rm -f "$BIN_DIR/paprwall-gui"
    print_success "Removed paprwall-gui command"
fi

# Remove PATH modifications from shell configs
print_info "Checking shell configurations..."

for config_file in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
    if [ -f "$config_file" ]; then
        # Check if our PATH modification exists
        if grep -q "Added by Paprwall installer" "$config_file" 2>/dev/null; then
            # Create temp file without Paprwall lines
            grep -v "Added by Paprwall installer" "$config_file" > "$config_file.tmp" 2>/dev/null || true
            grep -v 'export PATH="$HOME/.local/bin:$PATH"' "$config_file.tmp" > "$config_file.tmp2" 2>/dev/null || true
            mv "$config_file.tmp2" "$config_file"
            rm -f "$config_file.tmp"
            print_success "Cleaned $(basename $config_file)"
        fi
    fi
done

# Completion message
printf "\n"
printf "${GREEN}========================================${NC}\n"
printf "${GREEN}  Uninstallation Complete! ✨${NC}\n"
printf "${GREEN}========================================${NC}\n"
printf "\n"

print_success "Paprwall has been removed from your system"
printf "\n"

printf "To reinstall:\n"
printf "  ${BLUE}curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | bash${NC}\n"
printf "\n"

printf "Thank you for using Paprwall! 👋\n"
printf "\n"
