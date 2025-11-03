#!/bin/sh
# Uninstallation script for Paprwall (POSIX-compliant)
# Usage: curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/uninstall.sh | sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
INSTALL_DIR="$HOME/.paprwall"
CONFIG_DIR="$HOME/.config/paprwall"
DATA_DIR="$HOME/.local/share/paprwall"
SERVICE_FILE="$HOME/.config/systemd/user/paprwall.service"

printf "${BLUE}╔════════════════════════════════════════╗${NC}\n"
printf "${BLUE}║   Paprwall Uninstallation Script      ║${NC}\n"
printf "${BLUE}╚════════════════════════════════════════╝${NC}\n"
printf "\n"

# Check if installed
if [ ! -d "$INSTALL_DIR" ] && ! pip3 show paprwall >/dev/null 2>&1; then
    printf "${YELLOW}⚠${NC} Paprwall is not installed\n"
    exit 0
fi

printf "${YELLOW}⚠${NC} This will remove Paprwall and all its data\n"
printf "\n"
printf "The following will be removed:\n"
[ -d "$INSTALL_DIR" ] && printf "  • %s\n" "$INSTALL_DIR"
[ -d "$CONFIG_DIR" ] && printf "  • %s\n" "$CONFIG_DIR"
[ -d "$DATA_DIR" ] && printf "  • %s\n" "$DATA_DIR"
[ -f "$SERVICE_FILE" ] && printf "  • %s\n" "$SERVICE_FILE"
pip3 show paprwall >/dev/null 2>&1 && printf "  • Python package (paprwall)\n"
printf "\n"

printf "Continue? (y/N): "
read -r REPLY
case "$REPLY" in
    [Yy]*)
        ;;
    *)
        printf "${BLUE}ℹ${NC} Uninstallation cancelled\n"
        exit 0
        ;;
esac

printf "\n"
printf "${BLUE}ℹ${NC} Uninstalling Paprwall...\n"
printf "\n"

# Stop service if running
if systemctl --user is-active paprwall >/dev/null 2>&1; then
    printf "${BLUE}ℹ${NC} Stopping service...\n"
    systemctl --user stop paprwall
    printf "${GREEN}✓${NC} Service stopped\n"
fi

# Disable service if enabled
if systemctl --user is-enabled paprwall >/dev/null 2>&1; then
    printf "${BLUE}ℹ${NC} Disabling service...\n"
    systemctl --user disable paprwall
    printf "${GREEN}✓${NC} Service disabled\n"
fi

# Remove service file
if [ -f "$SERVICE_FILE" ]; then
    rm -f "$SERVICE_FILE"
    systemctl --user daemon-reload 2>/dev/null || true
    printf "${GREEN}✓${NC} Service file removed\n"
fi

# Uninstall Python package
if pip3 show paprwall >/dev/null 2>&1; then
    printf "${BLUE}ℹ${NC} Uninstalling Python package...\n"
    pip3 uninstall -y paprwall >/dev/null 2>&1
    printf "${GREEN}✓${NC} Package uninstalled\n"
fi

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    printf "${GREEN}✓${NC} Installation directory removed\n"
fi

# Remove config directory
if [ -d "$CONFIG_DIR" ]; then
    rm -rf "$CONFIG_DIR"
    printf "${GREEN}✓${NC} Configuration directory removed\n"
fi

# Remove data directory
if [ -d "$DATA_DIR" ]; then
    rm -rf "$DATA_DIR"
    printf "${GREEN}✓${NC} Data directory removed\n"
fi

# Remove command links if they exist
if [ -f "$HOME/.local/bin/paprwall" ]; then
    rm -f "$HOME/.local/bin/paprwall"
    printf "${GREEN}✓${NC} Removed paprwall command\n"
fi

if [ -f "$HOME/.local/bin/paprwall-gui" ]; then
    rm -f "$HOME/.local/bin/paprwall-gui"
    printf "${GREEN}✓${NC} Removed paprwall-gui command\n"
fi

printf "\n"
printf "${GREEN}╔════════════════════════════════════════╗${NC}\n"
printf "${GREEN}║   Uninstallation Complete! ✨         ║${NC}\n"
printf "${GREEN}╚════════════════════════════════════════╝${NC}\n"
printf "\n"
printf "${BLUE}ℹ${NC} Paprwall has been removed from your system\n"
printf "\n"
printf "To reinstall:\n"
printf "  curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | sh\n"
printf "\n"
printf "Thank you for using Paprwall! 👋\n"
printf "\n"
