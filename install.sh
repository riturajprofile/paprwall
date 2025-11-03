#!/bin/sh
# Paprwall Installation Script
# Simple, system-independent, POSIX-compliant installer
# Usage: curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | sh

set -e

# ============================================================================
# Configuration
# ============================================================================
REPO_URL="https://github.com/riturajprofile/paprwall.git"
INSTALL_DIR="$HOME/.paprwall"
BIN_DIR="$HOME/.local/bin"
LOG_FILE="/tmp/paprwall-install-$$.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ============================================================================
# Helper Functions
# ============================================================================

print_header() {
    printf "\n${BLUE}========================================${NC}\n"
    printf "${BLUE}  Paprwall Installation Script${NC}\n"
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

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect package manager
detect_package_manager() {
    if command_exists apt-get; then
        echo "apt"
    elif command_exists dnf; then
        echo "dnf"
    elif command_exists yum; then
        echo "yum"
    elif command_exists pacman; then
        echo "pacman"
    elif command_exists zypper; then
        echo "zypper"
    else
        echo "unknown"
    fi
}

# Install system package
install_package() {
    pkg_manager=$(detect_package_manager)
    packages="$1"
    
    case "$pkg_manager" in
        apt)
            if command_exists sudo; then
                sudo apt-get update -qq && sudo apt-get install -y $packages
            else
                apt-get update -qq && apt-get install -y $packages
            fi
            ;;
        dnf|yum)
            if command_exists sudo; then
                sudo $pkg_manager install -y $packages
            else
                $pkg_manager install -y $packages
            fi
            ;;
        pacman)
            if command_exists sudo; then
                sudo pacman -S --noconfirm $packages
            else
                pacman -S --noconfirm $packages
            fi
            ;;
        zypper)
            if command_exists sudo; then
                sudo zypper install -y $packages
            else
                zypper install -y $packages
            fi
            ;;
        *)
            print_error "Unknown package manager. Please install manually: $packages"
            return 1
            ;;
    esac
}

# Get package name for python3-venv
get_venv_package() {
    pkg_manager=$(detect_package_manager)
    python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "3")
    
    case "$pkg_manager" in
        apt)
            echo "python${python_version}-venv"
            ;;
        dnf|yum)
            echo "python${python_version}-venv"
            ;;
        pacman)
            echo "python"  # venv included
            ;;
        zypper)
            echo "python3-venv"
            ;;
        *)
            echo "python3-venv"
            ;;
    esac
}

# Get package names for GTK dependencies
get_gtk_packages() {
    pkg_manager=$(detect_package_manager)
    
    case "$pkg_manager" in
        apt)
            echo "python3-gi python3-gi-cairo gir1.2-gtk-3.0"
            ;;
        dnf|yum)
            echo "python3-gobject gtk3"
            ;;
        pacman)
            echo "python-gobject gtk3"
            ;;
        zypper)
            echo "python3-gobject gtk3"
            ;;
        *)
            echo "python3-gi gtk3"
            ;;
    esac
}

# ============================================================================
# Pre-installation Checks
# ============================================================================

print_header

# Check OS
case "$(uname -s)" in
    Linux*)
        print_success "Running on Linux"
        ;;
    *)
        print_error "This installer only supports Linux"
        exit 1
        ;;
esac

# Check Python 3
if ! command_exists python3; then
    print_error "Python 3 is required but not installed"
    printf "\nInstall Python 3 using your package manager:\n"
    printf "  Ubuntu/Debian: sudo apt install python3\n"
    printf "  Fedora:        sudo dnf install python3\n"
    printf "  Arch:          sudo pacman -S python\n"
    exit 1
fi

python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
print_success "Found Python $python_version"

# Check Git
if ! command_exists git; then
    print_error "Git is required but not installed"
    printf "\nInstall Git using your package manager:\n"
    printf "  Ubuntu/Debian: sudo apt install git\n"
    printf "  Fedora:        sudo dnf install git\n"
    printf "  Arch:          sudo pacman -S git\n"
    exit 1
fi
print_success "Found Git"

# ============================================================================
# Check Dependencies
# ============================================================================

# Check GTK dependencies (optional, for GUI)
if ! python3 -c "import gi" 2>/dev/null; then
    print_warning "GTK dependencies not found (GUI will not work)"
    gtk_packages=$(get_gtk_packages)
    
    print_info "Installing GTK dependencies: $gtk_packages"
    if install_package "$gtk_packages"; then
        print_success "GTK dependencies installed"
    else
        print_warning "Failed to install GTK. GUI may not work (CLI will still work)."
    fi
else
    print_success "GTK dependencies found"
fi

# ============================================================================
# Installation
# ============================================================================

printf "\n"
print_info "Installing Paprwall to: $INSTALL_DIR"
printf "\n"

# Clear log file
: > "$LOG_FILE"

# Remove old installation
if [ -d "$INSTALL_DIR" ]; then
    print_warning "Found existing installation - updating..."
    rm -rf "$INSTALL_DIR"
    print_success "Removed old installation"
fi

# Clone repository
print_info "Cloning repository..."
if git clone --depth 1 "$REPO_URL" "$INSTALL_DIR" >>"$LOG_FILE" 2>&1; then
    print_success "Repository cloned"
else
    print_error "Failed to clone repository"
    printf "\n${YELLOW}Error details:${NC}\n"
    tail -n 20 "$LOG_FILE" 2>/dev/null || cat "$LOG_FILE"
    exit 1
fi

cd "$INSTALL_DIR" || exit 1

# ============================================================================
# Virtual Environment Setup
# ============================================================================

print_info "Creating virtual environment..."

# Try to create virtual environment
if python3 -m venv .venv >>"$LOG_FILE" 2>&1; then
    print_success "Virtual environment created"
else
    # Check if it's the ensurepip/python3-venv issue
    if grep -q "ensurepip" "$LOG_FILE" 2>/dev/null; then
        print_warning "python3-venv package is missing"
        venv_package=$(get_venv_package)
        
        print_info "Installing $venv_package automatically..."
        if install_package "$venv_package"; then
            print_success "$venv_package installed"
            
            # Try creating venv again
            print_info "Retrying virtual environment creation..."
            if python3 -m venv .venv >>"$LOG_FILE" 2>&1; then
                print_success "Virtual environment created"
            else
                print_error "Still failed to create virtual environment"
                printf "\n${YELLOW}Error details:${NC}\n"
                tail -n 20 "$LOG_FILE" 2>/dev/null || cat "$LOG_FILE"
                exit 1
            fi
        else
            print_error "Failed to install $venv_package"
            printf "\nPlease install manually:\n"
            printf "  Ubuntu/Debian: ${BLUE}sudo apt install %s${NC}\n" "$venv_package"
            printf "  Fedora:        ${BLUE}sudo dnf install python3-venv${NC}\n"
            printf "  Arch:          ${BLUE}sudo pacman -S python${NC} (venv included)\n"
            printf "\nThen run the installer again.\n"
            exit 1
        fi
    else
        # Different error
        print_error "Failed to create virtual environment"
        printf "\n${YELLOW}Error details:${NC}\n"
        tail -n 20 "$LOG_FILE" 2>/dev/null || cat "$LOG_FILE"
        printf "\n"
        exit 1
    fi
fi

# Upgrade pip
print_info "Upgrading pip..."
.venv/bin/python -m pip install --upgrade pip >>"$LOG_FILE" 2>&1 || true

# Install package
print_info "Installing Paprwall..."
if .venv/bin/pip install . >>"$LOG_FILE" 2>&1; then
    print_success "Paprwall installed"
else
    print_error "Installation failed"
    printf "\n${YELLOW}Last 50 lines of log:${NC}\n"
    tail -n 50 "$LOG_FILE" 2>/dev/null || cat "$LOG_FILE"
    printf "\n"
    exit 1
fi

# ============================================================================
# Create Wrapper Scripts
# ============================================================================

print_info "Creating wrapper scripts..."
mkdir -p "$BIN_DIR"

# Create paprwall wrapper
cat > "$BIN_DIR/paprwall" << 'EOF'
#!/bin/sh
exec "$HOME/.paprwall/.venv/bin/paprwall" "$@"
EOF
chmod +x "$BIN_DIR/paprwall"

# Create paprwall-gui wrapper
cat > "$BIN_DIR/paprwall-gui" << 'EOF'
#!/bin/sh
exec "$HOME/.paprwall/.venv/bin/paprwall-gui" "$@"
EOF
chmod +x "$BIN_DIR/paprwall-gui"

print_success "Wrapper scripts created in $BIN_DIR"

# ============================================================================
# Setup Configuration
# ============================================================================

# Copy .env.example to .env
if [ -f ".env.example" ] && [ ! -f ".env" ]; then
    cp .env.example .env
    print_success "Configuration file created: $INSTALL_DIR/.env"
fi

# ============================================================================
# Completion
# ============================================================================

printf "\n"
printf "${GREEN}========================================${NC}\n"
printf "${GREEN}  Installation Complete! 🎉${NC}\n"
printf "${GREEN}========================================${NC}\n"
printf "\n"

printf "📁 Installed to: ${BLUE}%s${NC}\n" "$INSTALL_DIR"
printf "📝 Config file:  ${BLUE}%s/.env${NC}\n" "$INSTALL_DIR"
printf "\n"

# Check if ~/.local/bin is in PATH
case ":$PATH:" in
    *:"$BIN_DIR":*)
        print_success "Commands ready to use"
        ;;
    *)
        print_warning "$BIN_DIR is not in your PATH"
        printf "\nAdd this line to your ~/.bashrc or ~/.zshrc:\n"
        printf "  ${BLUE}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}\n"
        printf "\nThen reload your shell:\n"
        printf "  ${BLUE}source ~/.bashrc${NC}  # or source ~/.zshrc\n"
        printf "\n"
        ;;
esac

printf "📖 Next Steps:\n\n"
printf "1. Get FREE API keys:\n"
printf "   • Pixabay: https://pixabay.com/api/docs/\n"
printf "   • Pexels:  https://www.pexels.com/api/\n\n"
printf "2. Edit config file:\n"
printf "   ${BLUE}nano %s/.env${NC}\n\n" "$INSTALL_DIR"
printf "3. Try these commands:\n"
printf "   ${BLUE}paprwall --themes${NC}         # List themes\n"
printf "   ${BLUE}paprwall --set-theme ocean${NC} # Set theme\n"
printf "   ${BLUE}paprwall --fetch${NC}           # Download wallpapers\n"
printf "   ${BLUE}paprwall-gui${NC}               # Launch GUI\n"
printf "\n"

printf "🆘 Help: https://github.com/riturajprofile/paprwall\n"
printf "📋 Log:  %s\n" "$LOG_FILE"
printf "\n"
