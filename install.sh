#!/bin/bash
# Installation script for riturajprofile-wallpaper

set -e

echo "=================================="
echo "riturajprofile-wallpaper Installer"
echo "=================================="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Error: This application only works on Linux"
    exit 1
fi

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    REQUIRED_VERSION="3.8"
    
    if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
        echo "✓ Python $PYTHON_VERSION found"
    else
        echo "❌ Error: Python 3.8 or higher required (found $PYTHON_VERSION)"
        exit 1
    fi
else
    echo "❌ Error: Python 3 not found"
    exit 1
fi

# Detect package manager and install dependencies
echo ""
echo "Installing system dependencies..."

if command -v apt-get &> /dev/null; then
    echo "Detected Debian/Ubuntu system"
    sudo apt-get update
    sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 python3-pip
elif command -v dnf &> /dev/null; then
    echo "Detected Fedora system"
    sudo dnf install -y python3-gobject gtk3 python3-pip
elif command -v pacman &> /dev/null; then
    echo "Detected Arch Linux system"
    sudo pacman -S --noconfirm python-gobject gtk3 python-pip
else
    echo "⚠️  Warning: Could not detect package manager"
    echo "Please manually install: python3-gi, gtk3, python3-pip"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install the package
echo ""
echo "Installing riturajprofile-wallpaper..."

if [ -f "pyproject.toml" ]; then
    # Installing from source
    echo "Installing from source..."
    pip3 install --user .
else
    # Installing from PyPI
    echo "Installing from PyPI..."
    pip3 install --user riturajprofile-wallpaper
fi

# Ensure ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "⚠️  Adding ~/.local/bin to PATH"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo "Please run: source ~/.bashrc"
fi

echo ""
echo "✓ Installation complete!"
echo ""
echo "Quick Start:"
echo "  1. Launch GUI:   riturajprofile-wallpaper-gui"
echo "  2. Fetch images: riturajprofile-wallpaper --fetch"
echo "  3. Show help:    riturajprofile-wallpaper --help"
echo ""
echo "Optional: Install systemd service for auto-rotation"
echo "  mkdir -p ~/.config/systemd/user"
echo "  cp systemd/riturajprofile-wallpaper.service ~/.config/systemd/user/"
echo "  systemctl --user enable riturajprofile-wallpaper"
echo "  systemctl --user start riturajprofile-wallpaper"
echo ""
echo "For more information, see README.md"
echo "=================================="
