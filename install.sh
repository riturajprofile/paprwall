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

# Check and install GTK dependencies (non-fatal, ask user, continue on failure)
if ! python3 -c "import gi" 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC} PyGObject (GTK) not found - GUI will not work without it"
    echo ""

    # Detect package manager
    INSTALL_CMD=""
    PACKAGES=""
    if command -v apt-get &> /dev/null; then
        INSTALL_CMD="apt-get"
        PACKAGES="python3-gi python3-gi-cairo gir1.2-gtk-3.0"
    elif command -v dnf &> /dev/null; then
        INSTALL_CMD="dnf"
        PACKAGES="python3-gobject gtk3"
    elif command -v pacman &> /dev/null; then
        INSTALL_CMD="pacman"
        PACKAGES="python-gobject gtk3"
    fi

    # Respect env overrides for automation
    AUTO_INSTALL="${PAPRWALL_AUTO_INSTALL:-}"

    if [ -n "$INSTALL_CMD" ]; then
        echo "To enable GUI, these packages need to be installed:"
        echo "  $PACKAGES"
        echo ""

        DO_INSTALL="n"
        if [ -n "$AUTO_INSTALL" ]; then
            DO_INSTALL="y"
            echo -e "${BLUE}ℹ${NC} PAPRWALL_AUTO_INSTALL=1 detected — installing GTK dependencies automatically"
        elif [ -t 0 ] && [ -z "$SUDO_USER" ]; then
            # Interactive and not running via sudo: ask user
            read -p "Do you want to install GTK dependencies now? (Y/n): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Nn]$ ]]; then DO_INSTALL="y"; fi
        else
            echo -e "${BLUE}ℹ${NC} Non-interactive or sudo session — skipping automatic install"
            echo "    Tip: export PAPRWALL_AUTO_INSTALL=1 to auto-install system packages"
        fi

        if [[ "$DO_INSTALL" == "y" ]]; then
            echo -e "${BLUE}ℹ${NC} Installing GTK packages..."

            # Build the actual command based on package manager
            CMD=""
            if [ "$INSTALL_CMD" = "apt-get" ]; then
                if command -v sudo &>/dev/null; then
                    CMD="sudo apt-get update -qq && sudo apt-get install -y $PACKAGES"
                else
                    CMD="apt-get update -qq && apt-get install -y $PACKAGES"
                fi
            elif [ "$INSTALL_CMD" = "dnf" ]; then
                if command -v sudo &>/dev/null; then
                    CMD="sudo dnf install -y $PACKAGES -q"
                else
                    CMD="dnf install -y $PACKAGES -q"
                fi
            elif [ "$INSTALL_CMD" = "pacman" ]; then
                if command -v sudo &>/dev/null; then
                    CMD="sudo pacman -S --noconfirm $PACKAGES"
                else
                    CMD="pacman -S --noconfirm $PACKAGES"
                fi
            fi

            # Run install safely (do not abort installer if it fails)
            set +e
            bash -c "$CMD"
            RC=$?
            set -e

            if [ $RC -eq 0 ]; then
                echo -e "${GREEN}✓${NC} GTK packages installed successfully"
            else
                echo -e "${YELLOW}⚠${NC} Failed to install GTK packages (exit $RC). Continuing without GUI."
            fi
        else
            echo -e "${BLUE}ℹ${NC} Skipping GTK installation — continuing with CLI-only mode"
        fi
    else
        echo -e "${RED}✗${NC} Could not detect package manager"
        echo "Please manually install: python3-gi python3-gi-cairo gir1.2-gtk-3.0 (or equivalents)"
        echo -e "${BLUE}ℹ${NC} Continuing with CLI-only installation..."
        sleep 2
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
    echo -e "${BLUE}ℹ${NC} Removing old installation and updating..."
    rm -rf "$INSTALL_DIR"
    echo -e "${GREEN}✓${NC} Removed old installation"
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

# Install package (robust pip handling)
cd "$INSTALL_DIR"
echo -e "${BLUE}ℹ${NC} Installing Python package..."

# Ensure pip exists and is up to date for this interpreter
set +e
python3 -m ensurepip --upgrade >/dev/null 2>&1
python3 -m pip install --upgrade pip >/tmp/paprwall-install.log 2>&1
set -e

PIP_CMD="python3 -m pip"

# Decide whether to use --user
USER_FLAG="--user"
if [ -n "$VIRTUAL_ENV" ] || [ "$(id -u)" -eq 0 ]; then
    USER_FLAG=""
fi

# Try preferred install first
set +e
$PIP_CMD install -e . $USER_FLAG >> /tmp/paprwall-install.log 2>&1
RC=$?
set -e

if [ $RC -ne 0 ]; then
    echo -e "${YELLOW}⚠${NC} Initial pip install failed (code $RC). Trying alternative mode..."
    # Flip the user flag and try again
    ALT_FLAG="--user"
    if [ -z "$USER_FLAG" ]; then ALT_FLAG=""; else ALT_FLAG=""; fi
    set +e
    $PIP_CMD install -e . $ALT_FLAG >> /tmp/paprwall-install.log 2>&1
    RC2=$?
    set -e
    if [ $RC2 -ne 0 ]; then
        echo -e "${RED}✗${NC} Failed to install package"
        echo "----- pip output (last 200 lines) -----"
        tail -n 200 /tmp/paprwall-install.log || true
        echo "---------------------------------------"
        echo "Tips:"
        echo "  - If running with sudo, avoid --user or use a virtual environment"
        echo "  - Ensure ~/.local/bin is on PATH for user installs"
        exit 1
    else
        echo -e "${GREEN}✓${NC} Package installed (alternative mode)"
    fi
else
    echo -e "${GREEN}✓${NC} Package installed"
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

# Optionally fetch .env from a PRIVATE GitHub repo
# Supports:
#  - Env vars: GITHUB_ENV_URL or PAPRWALL_ENV_URL
#  - Token from: GITHUB_TOKEN or PAPRWALL_GITHUB_TOKEN (or prompt)
#  - GitHub links: raw.githubusercontent.com or github.com/.../blob/... (auto-converted)
maybe_fetch_private_env() {
    # Default PRIVATE .env location (hardcoded as requested)
    local DEFAULT_ENV_URL="https://github.com/riturajprofile/env-setup/blob/main/.env"
    # Allow overrides via env if needed
    local INPUT_URL="${GITHUB_ENV_URL:-${PAPRWALL_ENV_URL:-$DEFAULT_ENV_URL}}"

    # Check if running in non-interactive mode (piped execution or sudo)
    if [ ! -t 0 ] || [ -n "$SUDO_USER" ]; then
        # Non-interactive or sudo: skip unless env var is set
        if [ "$INPUT_URL" = "$DEFAULT_ENV_URL" ]; then
            echo ""
            echo -e "${BLUE}ℹ${NC} Skipping private .env download (non-interactive mode)"
            echo "    To enable: export PAPRWALL_GITHUB_TOKEN='your_token'"
            echo "    Then re-run: curl -fsSL ...install.sh | bash"
            return 0
        fi
    else
        # Interactive: ask user
        echo ""
        read -p "Are you the developer of this app? Then you totally have a GitHub token handy, right? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 0
        fi
    fi

    # Convert regular GitHub 'blob' link to a raw link if needed
    normalize_github_url() {
        local url="$1"
        if echo "$url" | grep -qE '^https://github.com/.+/.+/blob/.+'; then
            # github.com/<owner>/<repo>/blob/<branch>/<path> -> raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>
            echo "$url" | sed -E 's#https://github.com/([^/]+)/([^/]+)/blob/([^/]+)/(.*)#https://raw.githubusercontent.com/\1/\2/\3/\4#'
        elif echo "$url" | grep -qE '^https://github.com/.+/.+/raw/.+'; then
            # github.com/<owner>/<repo>/raw/<branch>/<path> -> raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>
            echo "$url" | sed -E 's#https://github.com/([^/]+)/([^/]+)/raw/([^/]+)/(.*)#https://raw.githubusercontent.com/\1/\2/\3/\4#'
        else
            echo "$url"
        fi
    }

    RAW_URL="$(normalize_github_url "$INPUT_URL")"
    echo -e "${BLUE}ℹ${NC} Using .env source: $RAW_URL"

    # Determine if URL is GitHub API contents endpoint
    local IS_API_URL=0
    if echo "$RAW_URL" | grep -q 'api.github.com/repos'; then
        IS_API_URL=1
    fi

    # Resolve token from env or prompt
    local GH_TOKEN="${GITHUB_TOKEN:-${PAPRWALL_GITHUB_TOKEN:-}}"
    if [ -z "$GH_TOKEN" ]; then
        echo ""
        echo "To access a PRIVATE repo, a GitHub token with 'repo' scope is required."
        echo "The token is used only for this download and will not be stored."
        read -s -r -p "Enter GitHub token (input hidden): " GH_TOKEN
        echo
    else
        echo -e "${BLUE}ℹ${NC} Using GitHub token from environment"
    fi

    # Build curl command
    local CURL_HEADERS=("-H" "Authorization: token ${GH_TOKEN}")
    if [ $IS_API_URL -eq 1 ]; then
        CURL_HEADERS+=("-H" "Accept: application/vnd.github.v3.raw")
    fi

    echo -e "${BLUE}ℹ${NC} Downloading private .env from GitHub (private repo)..."
    if curl -fsSL "${CURL_HEADERS[@]}" "$RAW_URL" -o .env.tmp 2>/dev/null && [ -s .env.tmp ]; then
        mv .env.tmp .env
        echo -e "${GREEN}✓${NC} Downloaded and set .env from GitHub"
    else
        rm -f .env.tmp 2>/dev/null || true
        echo -e "${YELLOW}⚠${NC} Failed to download .env from provided URL. Keeping existing .env"
        echo -e "${YELLOW}   URL tried:${NC} $RAW_URL"
    fi

    # Do not keep token in memory
    unset GH_TOKEN
}

# Attempt to fetch private .env if requested or configured
maybe_fetch_private_env

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
