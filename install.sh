#!/bin/bash
# One-line installation script for Paprwall
# Usage: curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | bash

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
REPO_URL="https://github.com/riturajprofile/paprwall.git"
INSTALL_DIR="$HOME/.paprwall"
TEMP_DIR="/tmp/paprwall-install-$$"

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Paprwall Installation Script v1.0   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}✗${NC} This script only works on Linux systems"
    exit 1
fi
echo -e "${GREEN}✓${NC} Running on Linux"

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗${NC} Python 3 is not installed"
    echo ""
    echo "Install Python:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✓${NC} Found Python $PYTHON_VERSION"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}✗${NC} Git is not installed"
    echo ""
    echo "Install Git:"
    echo "  Ubuntu/Debian: sudo apt install git"
    echo "  Fedora: sudo dnf install git"
    echo "  Arch: sudo pacman -S git"
    exit 1
fi
echo -e "${GREEN}✓${NC} Found Git"

# Check for GTK dependencies
if ! python3 -c "import gi" 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC} PyGObject (GTK) not found - GUI will not work"
    echo ""
    echo "To install GTK support:"
    echo "  Ubuntu/Debian: sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0"
    echo "  Fedora: sudo dnf install python3-gobject gtk3"
    echo "  Arch: sudo pacman -S python-gobject gtk3"
    echo ""
    read -p "Continue without GUI? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} GTK dependencies found"
fi

echo ""
echo -e "${BLUE}ℹ${NC} Installing Paprwall..."
echo ""

# Remove old installation if exists
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}⚠${NC} Found existing installation"
    read -p "Remove and reinstall? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$INSTALL_DIR"
        echo -e "${GREEN}✓${NC} Removed old installation"
    else
        echo -e "${RED}✗${NC} Installation cancelled"
        exit 1
    fi
fi

# Create temporary directory
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# Clone repository
echo -e "${BLUE}ℹ${NC} Cloning repository..."
if git clone --depth 1 "$REPO_URL" "$TEMP_DIR" 2>&1 | grep -v "Cloning into"; then
    :
fi
echo -e "${GREEN}✓${NC} Repository cloned"

# Move to install directory
mkdir -p "$INSTALL_DIR"
cp -r "$TEMP_DIR"/* "$INSTALL_DIR/"
cp -r "$TEMP_DIR"/.env.example "$INSTALL_DIR/" 2>/dev/null || true
cp -r "$TEMP_DIR"/.gitignore "$INSTALL_DIR/" 2>/dev/null || true
echo -e "${GREEN}✓${NC} Files copied to $INSTALL_DIR"

# Clean up
rm -rf "$TEMP_DIR"

# Install package
cd "$INSTALL_DIR"
echo -e "${BLUE}ℹ${NC} Installing Python package..."
if pip3 install -e . --user > /tmp/paprwall-install.log 2>&1; then
    echo -e "${GREEN}✓${NC} Package installed"
else
    echo -e "${RED}✗${NC} Failed to install package"
    cat /tmp/paprwall-install.log
    exit 1
fi

# Verify installation
if command -v paprwall &> /dev/null; then
    echo -e "${GREEN}✓${NC} Command 'paprwall' is available"
else
    echo -e "${YELLOW}⚠${NC} Command 'paprwall' not found in PATH"
    echo ""
    echo "Add to PATH by adding this to ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Then run: source ~/.bashrc"
fi

# Setup .env file
if [ -f ".env.example" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓${NC} Created .env configuration file"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Installation Complete! 🎉           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "📁 Installation: $INSTALL_DIR"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Get FREE API keys:"
echo "   • Pixabay: https://pixabay.com/api/docs/"
echo "   • Pexels: https://www.pexels.com/api/"
echo ""
echo "2. Add API keys:"
echo "   nano $INSTALL_DIR/.env"
echo ""
echo "3. Use Paprwall:"
echo "   paprwall --themes          # List themes"
echo "   paprwall --set-theme ocean # Set theme"
echo "   paprwall --fetch           # Get wallpapers"
echo "   paprwall-gui               # Launch GUI"
echo ""
echo "�� Attribution Secret: riturajprofile@162"
echo "   (Enter in GUI to remove desktop overlay)"
echo ""
echo "📖 Docs: $INSTALL_DIR/README.md"
echo "🆘 Help: https://github.com/riturajprofile/paprwall/issues"
echo ""

# Check service
if systemctl --user is-enabled paprwall &>/dev/null; then
    echo -e "${GREEN}✓${NC} Auto-start service enabled"
    echo "   Start: systemctl --user start paprwall"
fi

echo ""
echo -e "${BLUE}ℹ${NC} To uninstall: curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/uninstall.sh | bash"
echo ""
