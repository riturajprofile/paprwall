#!/usr/bin/env bash
# 
# Paprwall Installer
# Installs paprwall wallpaper manager for Linux
#
set -euo pipefail

INSTALL_DIR="$HOME/.paprwall"
VENV_DIR="$INSTALL_DIR/.venv"
BIN_DIR="$HOME/.local/bin"
REPO_URL="https://github.com/riturajprofile/paprwall"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

echo_success() {
    echo -e "${GREEN}✓${NC} $1"
}

echo_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo_error() {
    echo -e "${RED}✗${NC} $1"
}

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║     Paprwall Wallpaper Manager Setup     ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo_error "Python 3 is not installed!"
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo_info "Found Python $PYTHON_VERSION"

# Check Python version (require 3.8+)
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo_error "Python 3.8 or higher is required (found $PYTHON_VERSION)"
    exit 1
fi

# Detect package manager
detect_pm() {
  if command -v apt-get >/dev/null 2>&1; then echo apt; return; fi
  if command -v dnf >/dev/null 2>&1; then echo dnf; return; fi
  if command -v yum >/dev/null 2>&1; then echo yum; return; fi
  if command -v pacman >/dev/null 2>&1; then echo pacman; return; fi
  if command -v zypper >/dev/null 2>&1; then echo zypper; return; fi
  echo none
}

PM="$(detect_pm)"
echo_info "Package manager: $PM"

# Check and install system dependencies
echo_info "Checking system dependencies..."

install_system_deps() {
    case "$PM" in
        apt)
            echo_info "Installing dependencies via apt..."
            sudo apt-get update -qq
            sudo apt-get install -y python3-venv python3-tk git curl 2>/dev/null || true
            ;;
        dnf|yum)
            echo_info "Installing dependencies via $PM..."
            sudo "$PM" install -y python3-venv python3-tkinter git curl 2>/dev/null || true
            ;;
        pacman)
            echo_info "Installing dependencies via pacman..."
            sudo pacman -Sy --noconfirm python tk git curl 2>/dev/null || true
            ;;
        zypper)
            echo_info "Installing dependencies via zypper..."
            sudo zypper install -y python3-venv python3-tk git curl 2>/dev/null || true
            ;;
        none)
            echo_warning "Could not detect package manager"
            echo_warning "Please ensure python3-venv, python3-tk, git, and curl are installed"
            read -p "Continue anyway? (y/N) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
            ;;
    esac
}

# Only install if not already present
if ! python3 -c "import venv" 2>/dev/null; then
    install_system_deps
else
    echo_success "System dependencies OK"
fi

# Create installation directory
echo_info "Creating installation directory..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Clean up old installation if exists
if [ -d "$VENV_DIR" ]; then
    echo_warning "Existing installation found. Removing..."
    rm -rf "$VENV_DIR"
fi

# Create virtual environment
echo_info "Creating virtual environment..."
python3 -m venv "$VENV_DIR"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo_info "Upgrading pip..."
python -m pip install --upgrade pip -q

# Install paprwall
echo_info "Installing paprwall..."

# Check if we're in a git repository
if [ -d .git ] && [ -f setup.py ]; then
    echo_info "Installing from local repository..."
    pip install -e . -q
else
    echo_info "Installing from GitHub..."
    pip install "git+${REPO_URL}.git" -q
fi

echo_success "Paprwall installed successfully!"

# Create wrapper scripts
echo_info "Creating command wrappers..."

cat > "$BIN_DIR/paprwall" << 'WRAPPER_EOF'
#!/bin/bash
source "$HOME/.paprwall/.venv/bin/activate"
exec python -m paprwall.cli "$@"
WRAPPER_EOF

cat > "$BIN_DIR/wallpaper-manager" << 'WRAPPER_EOF'
#!/bin/bash
source "$HOME/.paprwall/.venv/bin/activate"
exec python -m paprwall.wallpaper_cli "$@"
WRAPPER_EOF

cat > "$BIN_DIR/wallpaper-gui" << 'WRAPPER_EOF'
#!/bin/bash
source "$HOME/.paprwall/.venv/bin/activate"
exec python -m paprwall.gui.wallpaper_manager_gui "$@"
WRAPPER_EOF

chmod +x "$BIN_DIR/paprwall"
chmod +x "$BIN_DIR/wallpaper-manager"
chmod +x "$BIN_DIR/wallpaper-gui"

echo_success "Command wrappers created"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo_warning "~/.local/bin is not in your PATH"
    echo ""
    echo "Add this to your shell configuration (~/.bashrc or ~/.zshrc):"
    echo ""
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

# Setup systemd service for auto-start
echo_info "Setting up auto-start service..."
"$VENV_DIR/bin/python" -m paprwall.service.autostart --enable 2>/dev/null || {
    echo_warning "Could not enable auto-start service"
    echo "You can enable it later with: paprwall --enable-service"
}

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║    Installation Complete! 🎉              ║"
echo "╚═══════════════════════════════════════════╝"
echo ""
echo_success "Paprwall has been installed to: $INSTALL_DIR"
echo ""
echo "📝 Quick Start:"
echo ""
echo "  1. Set up API keys (optional, but recommended):"
echo "     - Pixabay:  https://pixabay.com/api/docs/"
echo "     - Unsplash: https://unsplash.com/developers"
echo "     - Pexels:   https://www.pexels.com/api/"
echo ""
echo "     Add keys to: ~/.config/paprwall/api_keys.json"
echo ""
echo "  2. Try these commands:"
echo "     paprwall --fetch              # Download & set new wallpapers"
echo "     paprwall --next               # Navigate to next wallpaper"
echo "     paprwall --set-theme nature   # Set theme to nature"
echo "     wallpaper-gui                 # Launch GUI (requires tkinter)"
echo ""
echo "  3. For more help:"
echo "     paprwall --help"
echo ""
echo "🔗 Documentation: https://github.com/riturajprofile/paprwall"
echo ""
