#!/usr/bin/env bash
# 
# Paprwall Single-File Installer
# Downloads and installs paprwall wallpaper manager for Linux
#
set -euo pipefail

INSTALL_DIR="$HOME/.paprwall"
BIN_DIR="$HOME/.local/bin"
REPO_URL="https://github.com/riturajprofile/paprwall"
VERSION="v1.1.1"

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
echo "║           Single Binary Install           ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Check if we should download binary or install from source
INSTALL_MODE="binary"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --source)
            INSTALL_MODE="source"
            shift
            ;;
        --version)
            VERSION="$2"
            shift 2
            ;;
        *)
            echo_error "Unknown option: $1"
            echo "Usage: $0 [--source] [--version v1.1.1]"
            exit 1
            ;;
    esac
done

echo_info "Install mode: $INSTALL_MODE"

# Create directories
mkdir -p "$BIN_DIR"
mkdir -p "$INSTALL_DIR"

if [ "$INSTALL_MODE" = "binary" ]; then
    # ==========================================
    # BINARY INSTALLATION (Recommended)
    # ==========================================
    
    echo_info "Downloading pre-built binaries from GitHub..."
    
    # Detect architecture
    ARCH=$(uname -m)
    case "$ARCH" in
        x86_64)
            CLI_BINARY="paprwall-linux-amd64"
            GUI_BINARY="paprwall-gui-linux-amd64"
            ;;
        aarch64|arm64)
            CLI_BINARY="paprwall-linux-arm64"
            GUI_BINARY="paprwall-gui-linux-arm64"
            ;;
        *)
            echo_error "Unsupported architecture: $ARCH"
            echo "Falling back to source installation..."
            INSTALL_MODE="source"
            ;;
    esac
    
    if [ "$INSTALL_MODE" = "binary" ]; then
        # Download CLI binary
        CLI_URL="${REPO_URL}/releases/download/${VERSION}/${CLI_BINARY}"
        echo_info "Downloading CLI from: $CLI_URL"
        
        if command -v curl &> /dev/null; then
            curl -fsSL -o "$INSTALL_DIR/paprwall" "$CLI_URL" || {
                echo_warning "CLI binary download failed, falling back to source install"
                INSTALL_MODE="source"
            }
        elif command -v wget &> /dev/null; then
            wget -q -O "$INSTALL_DIR/paprwall" "$CLI_URL" || {
                echo_warning "CLI binary download failed, falling back to source install"
                INSTALL_MODE="source"
            }
        else
            echo_error "Neither curl nor wget found. Please install one of them."
            exit 1
        fi
        
        if [ "$INSTALL_MODE" = "binary" ]; then
            chmod +x "$INSTALL_DIR/paprwall"
            ln -sf "$INSTALL_DIR/paprwall" "$BIN_DIR/paprwall"
            echo_success "CLI binary installed successfully!"
            
            # Download GUI binary
            GUI_URL="${REPO_URL}/releases/download/${VERSION}/${GUI_BINARY}"
            echo_info "Downloading GUI from: $GUI_URL"
            
            if command -v curl &> /dev/null; then
                curl -fsSL -o "$INSTALL_DIR/paprwall-gui" "$GUI_URL" 2>/dev/null || {
                    echo_warning "GUI binary not available, skipping"
                    echo_info "You can install from source with: $0 --source"
                }
            elif command -v wget &> /dev/null; then
                wget -q -O "$INSTALL_DIR/paprwall-gui" "$GUI_URL" 2>/dev/null || {
                    echo_warning "GUI binary not available, skipping"
                    echo_info "You can install from source with: $0 --source"
                }
            fi
            
            # If GUI was downloaded successfully, set it up
            if [ -f "$INSTALL_DIR/paprwall-gui" ]; then
                chmod +x "$INSTALL_DIR/paprwall-gui"
                ln -sf "$INSTALL_DIR/paprwall-gui" "$BIN_DIR/paprwall-gui"
                echo_success "GUI binary installed successfully!"
            fi
        fi
    fi
fi

if [ "$INSTALL_MODE" = "source" ]; then
    # ==========================================
    # SOURCE INSTALLATION (Fallback)
    # ==========================================
    
    echo_info "Installing from source..."
    
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
                ;;
        esac
    }
    
    # Only install if not already present
    if ! python3 -c "import venv" 2>/dev/null; then
        install_system_deps
    else
        echo_success "System dependencies OK"
    fi
    
    VENV_DIR="$INSTALL_DIR/.venv"
    
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
    echo_info "Installing paprwall from GitHub..."
    pip install "git+${REPO_URL}.git@${VERSION}" -q || pip install "git+${REPO_URL}.git" -q
    
    echo_success "Paprwall installed successfully!"
    
    # Create wrapper script
    echo_info "Creating command wrappers..."
    
    cat > "$BIN_DIR/paprwall" << 'WRAPPER_EOF'
#!/bin/bash
source "$HOME/.paprwall/.venv/bin/activate"
exec python -m paprwall.cli "$@"
WRAPPER_EOF
    
    chmod +x "$BIN_DIR/paprwall"
    
    # GUI wrapper
    cat > "$BIN_DIR/paprwall-gui" << 'WRAPPER_EOF'
#!/bin/bash
source "$HOME/.paprwall/.venv/bin/activate"
exec python -m paprwall.gui.wallpaper_manager_gui "$@"
WRAPPER_EOF

    chmod +x "$BIN_DIR/paprwall-gui"
    
    echo_success "Command wrappers created"
fi

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo_warning "~/.local/bin is not in your PATH"
    echo ""
    echo "Add this to your shell configuration (~/.bashrc or ~/.zshrc):"
    echo ""
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

# Setup systemd service for auto-start (try both methods)
echo_info "Setting up auto-start service..."
if [ -f "$BIN_DIR/paprwall" ]; then
    "$BIN_DIR/paprwall" --start 2>/dev/null || {
        echo_warning "Could not enable auto-start service automatically"
        echo "You can enable it later with: systemctl --user enable paprwall"
    }
fi

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║    Installation Complete! 🎉              ║"
echo "╚═══════════════════════════════════════════╝"
echo ""
echo_success "Paprwall has been installed to: $INSTALL_DIR"
echo ""
echo "📝 Quick Start:"
echo ""
echo "  🌐 Paprwall uses Picsum Photos - no API keys needed!"
echo ""
echo "  Try these commands:"
echo "     paprwall --fetch              # Download & set new wallpaper from Picsum"
echo "     paprwall --current            # Show current wallpaper info"
if [ -f "$BIN_DIR/paprwall-gui" ] || [ -f "$HOME/.local/bin/paprwall-gui" ]; then
  echo "     paprwall-gui                  # Launch the GUI app"
else
  echo "     (GUI not installed - use: $0 --source)"
fi
echo ""
echo "  Auto-rotation:"
echo "     systemctl --user start paprwall   # Start service (fetch every 90 min)"
echo "     systemctl --user enable paprwall  # Enable on boot"
echo ""
echo "  Configuration:"
echo "     Edit ~/.config/paprwall/preferences.json to change interval"
echo "     Default: 90 minutes between wallpaper changes"
echo ""
echo "  For more help:"
echo "     paprwall --help"
echo ""
echo "🔗 Documentation: https://github.com/riturajprofile/paprwall"
echo ""
