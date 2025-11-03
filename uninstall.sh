#!/bin/bash
# Uninstallation script for Paprwall
# Usage: curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/uninstall.sh | bash

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

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Paprwall Uninstallation Script      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if installed
if [ ! -d "$INSTALL_DIR" ] && ! pip3 show paprwall &>/dev/null; then
    echo -e "${YELLOW}⚠${NC} Paprwall is not installed"
    exit 0
fi

echo -e "${YELLOW}⚠${NC} This will remove Paprwall and all its data"
echo ""
echo "The following will be removed:"
[ -d "$INSTALL_DIR" ] && echo "  • $INSTALL_DIR"
[ -d "$CONFIG_DIR" ] && echo "  • $CONFIG_DIR"
[ -d "$DATA_DIR" ] && echo "  • $DATA_DIR"
[ -f "$SERVICE_FILE" ] && echo "  • $SERVICE_FILE"
pip3 show paprwall &>/dev/null && echo "  • Python package (paprwall)"
echo ""

read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}ℹ${NC} Uninstallation cancelled"
    exit 0
fi

echo ""
echo -e "${BLUE}ℹ${NC} Uninstalling Paprwall..."
echo ""

# Stop service if running
if systemctl --user is-active paprwall &>/dev/null; then
    echo -e "${BLUE}ℹ${NC} Stopping service..."
    systemctl --user stop paprwall
    echo -e "${GREEN}✓${NC} Service stopped"
fi

# Disable service if enabled
if systemctl --user is-enabled paprwall &>/dev/null; then
    echo -e "${BLUE}ℹ${NC} Disabling service..."
    systemctl --user disable paprwall
    echo -e "${GREEN}✓${NC} Service disabled"
fi

# Remove service file
if [ -f "$SERVICE_FILE" ]; then
    rm -f "$SERVICE_FILE"
    systemctl --user daemon-reload 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Service file removed"
fi

# Uninstall Python package
if pip3 show paprwall &>/dev/null; then
    echo -e "${BLUE}ℹ${NC} Uninstalling Python package..."
    pip3 uninstall -y paprwall > /dev/null 2>&1
    echo -e "${GREEN}✓${NC} Package uninstalled"
fi

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo -e "${GREEN}✓${NC} Installation directory removed"
fi

# Remove config directory
if [ -d "$CONFIG_DIR" ]; then
    rm -rf "$CONFIG_DIR"
    echo -e "${GREEN}✓${NC} Configuration directory removed"
fi

# Remove data directory
if [ -d "$DATA_DIR" ]; then
    rm -rf "$DATA_DIR"
    echo -e "${GREEN}✓${NC} Data directory removed"
fi

# Remove command links if they exist
if [ -f "$HOME/.local/bin/paprwall" ]; then
    rm -f "$HOME/.local/bin/paprwall"
    echo -e "${GREEN}✓${NC} Removed paprwall command"
fi

if [ -f "$HOME/.local/bin/paprwall-gui" ]; then
    rm -f "$HOME/.local/bin/paprwall-gui"
    echo -e "${GREEN}✓${NC} Removed paprwall-gui command"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Uninstallation Complete! ✨         ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}ℹ${NC} Paprwall has been removed from your system"
echo ""
echo "To reinstall:"
echo "  curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | bash"
echo ""
echo "Thank you for using Paprwall! 👋"
echo ""
