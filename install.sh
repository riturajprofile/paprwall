#!/bin/sh
# One-line installation script for Paprwall (POSIX-compliant)
# Usage: curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | sh

set -e

# Colors (using printf for POSIX compliance)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
REPO_URL="https://github.com/riturajprofile/paprwall.git"
INSTALL_DIR="$HOME/.paprwall"
TEMP_DIR="/tmp/paprwall-install-$$"
LOG_FILE="/tmp/paprwall-install.log"

printf "${BLUE}╔════════════════════════════════════════╗${NC}\n"
printf "${BLUE}║   Paprwall Installation Script v1.0   ║${NC}\n"
printf "${BLUE}╚════════════════════════════════════════╝${NC}\n"
printf "\n"

# Check if running on Linux
case "$(uname -s)" in
    Linux*) printf "${GREEN}✓${NC} Running on Linux\n" ;;
    *)
        printf "${RED}✗${NC} This script only works on Linux systems\n"
        exit 1
        ;;
esac

# Check if Python 3 is installed
if ! command -v python3 >/dev/null 2>&1; then
    printf "${RED}✗${NC} Python 3 is not installed\n"
    printf "\n"
    printf "Install Python:\n"
    printf "  Ubuntu/Debian: sudo apt install python3 python3-pip\n"
    printf "  Fedora: sudo dnf install python3 python3-pip\n"
    printf "  Arch: sudo pacman -S python python-pip\n"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
printf "${GREEN}✓${NC} Found Python %s\n" "$PYTHON_VERSION"

# Check if git is installed
if ! command -v git >/dev/null 2>&1; then
    printf "${RED}✗${NC} Git is not installed\n"
    printf "\n"
    printf "Install Git:\n"
    printf "  Ubuntu/Debian: sudo apt install git\n"
    printf "  Fedora: sudo dnf install git\n"
    printf "  Arch: sudo pacman -S git\n"
    exit 1
fi
printf "${GREEN}✓${NC} Found Git\n"

# Check and install GTK dependencies (non-fatal)
if ! python3 -c "import gi" 2>/dev/null; then
    printf "${YELLOW}⚠${NC} PyGObject (GTK) not found - GUI will not work without it\n"
    printf "\n"

    # Detect package manager
    INSTALL_CMD=""
    PACKAGES=""
    if command -v apt-get >/dev/null 2>&1; then
        INSTALL_CMD="apt-get"
        PACKAGES="python3-gi python3-gi-cairo gir1.2-gtk-3.0"
    elif command -v dnf >/dev/null 2>&1; then
        INSTALL_CMD="dnf"
        PACKAGES="python3-gobject gtk3"
    elif command -v pacman >/dev/null 2>&1; then
        INSTALL_CMD="pacman"
        PACKAGES="python-gobject gtk3"
    fi

    AUTO_INSTALL="${PAPRWALL_AUTO_INSTALL:-}"

    if [ -n "$INSTALL_CMD" ]; then
        printf "To enable GUI, these packages need to be installed:\n"
        printf "  %s\n" "$PACKAGES"
        printf "\n"

        DO_INSTALL="n"
        if [ -n "$AUTO_INSTALL" ]; then
            DO_INSTALL="y"
            printf "${BLUE}ℹ${NC} PAPRWALL_AUTO_INSTALL=1 detected — installing GTK dependencies automatically\n"
        elif [ -t 0 ] && [ -z "$SUDO_USER" ]; then
            printf "Do you want to install GTK dependencies now? (Y/n): "
            read -r REPLY
            case "$REPLY" in
                [Nn]*) DO_INSTALL="n" ;;
                *) DO_INSTALL="y" ;;
            esac
        else
            printf "${BLUE}ℹ${NC} Non-interactive or sudo session — skipping automatic install\n"
            printf "    Tip: export PAPRWALL_AUTO_INSTALL=1 to auto-install system packages\n"
        fi

        if [ "$DO_INSTALL" = "y" ]; then
            printf "${BLUE}ℹ${NC} Installing GTK packages...\n"

            CMD=""
            if [ "$INSTALL_CMD" = "apt-get" ]; then
                if command -v sudo >/dev/null 2>&1; then
                    CMD="sudo apt-get update -qq && sudo apt-get install -y $PACKAGES"
                else
                    CMD="apt-get update -qq && apt-get install -y $PACKAGES"
                fi
            elif [ "$INSTALL_CMD" = "dnf" ]; then
                if command -v sudo >/dev/null 2>&1; then
                    CMD="sudo dnf install -y $PACKAGES -q"
                else
                    CMD="dnf install -y $PACKAGES -q"
                fi
            elif [ "$INSTALL_CMD" = "pacman" ]; then
                if command -v sudo >/dev/null 2>&1; then
                    CMD="sudo pacman -S --noconfirm $PACKAGES"
                else
                    CMD="pacman -S --noconfirm $PACKAGES"
                fi
            fi

            set +e
            sh -c "$CMD"
            RC=$?
            set -e

            if [ $RC -eq 0 ]; then
                printf "${GREEN}✓${NC} GTK packages installed successfully\n"
            else
                printf "${YELLOW}⚠${NC} Failed to install GTK packages (exit %d). Continuing without GUI.\n" "$RC"
            fi
        else
            printf "${BLUE}ℹ${NC} Skipping GTK installation — continuing with CLI-only mode\n"
        fi
    else
        printf "${RED}✗${NC} Could not detect package manager\n"
        printf "Please manually install: python3-gi python3-gi-cairo gir1.2-gtk-3.0 (or equivalents)\n"
        printf "${BLUE}ℹ${NC} Continuing with CLI-only installation...\n"
        sleep 2
    fi
else
    printf "${GREEN}✓${NC} GTK dependencies found\n"
fi

printf "\n"
printf "${BLUE}ℹ${NC} Installing Paprwall...\n"
printf "\n"

: > "$LOG_FILE"

# Remove old installation if exists
if [ -d "$INSTALL_DIR" ]; then
    printf "${YELLOW}⚠${NC} Found existing installation\n"
    printf "${BLUE}ℹ${NC} Removing old installation and updating...\n"
    rm -rf "$INSTALL_DIR"
    printf "${GREEN}✓${NC} Removed old installation\n"
fi

# Create temporary directory
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# Clone repository
printf "${BLUE}ℹ${NC} Cloning repository...\n"
git clone --depth 1 "$REPO_URL" "$TEMP_DIR" >/dev/null 2>&1
printf "${GREEN}✓${NC} Repository cloned\n"

# Move to install directory
mkdir -p "$INSTALL_DIR"
cp -r "$TEMP_DIR"/* "$INSTALL_DIR/" 2>/dev/null || true
cp -r "$TEMP_DIR"/.env.example "$INSTALL_DIR/" 2>/dev/null || true
cp -r "$TEMP_DIR"/.gitignore "$INSTALL_DIR/" 2>/dev/null || true
printf "${GREEN}✓${NC} Files copied to %s\n" "$INSTALL_DIR"

# Clean up
rm -rf "$TEMP_DIR"

# Begin installation
cd "$INSTALL_DIR" || exit 1

# Helper: install into dedicated virtualenv and create wrappers
install_in_venv() {
    cd "$INSTALL_DIR" || return 1
    printf "${BLUE}ℹ${NC} Creating virtual environment at %s/.venv\n" "$INSTALL_DIR"
    
    # Check if venv module is available
    if ! python3 -m venv --help >/dev/null 2>&1; then
        printf "${YELLOW}⚠${NC} python3-venv not available\n"
        
        # Detect Python version and package name
        PYTHON_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        VENV_PKG=""
        VENV_INSTALL_CMD=""
        
        if command -v apt-get >/dev/null 2>&1; then
            VENV_PKG="python${PYTHON_VER}-venv"
            VENV_INSTALL_CMD="apt-get install -y $VENV_PKG"
        elif command -v dnf >/dev/null 2>&1; then
            VENV_PKG="python${PYTHON_VER}-venv"
            VENV_INSTALL_CMD="dnf install -y $VENV_PKG"
        elif command -v pacman >/dev/null 2>&1; then
            VENV_PKG="python"
            printf "${BLUE}ℹ${NC} On Arch, venv is included with python package\n"
            return 1
        fi
        
        if [ -n "$VENV_INSTALL_CMD" ]; then
            printf "\n"
            printf "To create virtual environments, %s needs to be installed.\n" "$VENV_PKG"
            
            DO_VENV_INSTALL="n"
            if [ -n "$PAPRWALL_AUTO_INSTALL" ]; then
                DO_VENV_INSTALL="y"
                printf "${BLUE}ℹ${NC} PAPRWALL_AUTO_INSTALL=1 detected — installing %s automatically\n" "$VENV_PKG"
            elif [ -t 0 ] && [ -z "$SUDO_USER" ]; then
                printf "Install %s now? (Y/n): " "$VENV_PKG"
                read -r REPLY
                case "$REPLY" in
                    [Nn]*) DO_VENV_INSTALL="n" ;;
                    *) DO_VENV_INSTALL="y" ;;
                esac
            else
                printf "${BLUE}ℹ${NC} Non-interactive or sudo session — not installing automatically\n"
                printf "    Tip: export PAPRWALL_AUTO_INSTALL=1 to auto-install system packages\n"
            fi
            
            if [ "$DO_VENV_INSTALL" = "y" ]; then
                printf "${BLUE}ℹ${NC} Installing %s...\n" "$VENV_PKG"
                if command -v sudo >/dev/null 2>&1; then
                    if sudo sh -c "$VENV_INSTALL_CMD"; then
                        printf "${GREEN}✓${NC} %s installed successfully\n" "$VENV_PKG"
                    else
                        printf "${RED}✗${NC} Failed to install %s\n" "$VENV_PKG"
                        return 1
                    fi
                else
                    if sh -c "$VENV_INSTALL_CMD"; then
                        printf "${GREEN}✓${NC} %s installed successfully\n" "$VENV_PKG"
                    else
                        printf "${RED}✗${NC} Failed to install %s\n" "$VENV_PKG"
                        return 1
                    fi
                fi
            else
                printf "${YELLOW}⚠${NC} Skipping %s installation\n" "$VENV_PKG"
                return 1
            fi
        else
            printf "${RED}✗${NC} Could not detect package manager\n"
            return 1
        fi
    fi
    
    python3 -m venv .venv || return 1
    .venv/bin/python -m ensurepip --upgrade >>"$LOG_FILE" 2>&1 || true
    .venv/bin/python -m pip install --upgrade pip >>"$LOG_FILE" 2>&1 || return 1
    printf "${BLUE}ℹ${NC} Installing Paprwall into virtualenv...\n"
    .venv/bin/pip install . >>"$LOG_FILE" 2>&1 || return 1
    
    # Create wrapper scripts
    mkdir -p "$HOME/.local/bin"
    
    cat > "$HOME/.local/bin/paprwall" << 'WRAP'
#!/bin/sh
VENV_DIR="$HOME/.paprwall/.venv"
exec "$VENV_DIR/bin/paprwall" "$@"
WRAP
    chmod +x "$HOME/.local/bin/paprwall"
    
    cat > "$HOME/.local/bin/paprwall-gui" << 'WRAP2'
#!/bin/sh
VENV_DIR="$HOME/.paprwall/.venv"
exec "$VENV_DIR/bin/paprwall-gui" "$@"
WRAP2
    chmod +x "$HOME/.local/bin/paprwall-gui"
    
    printf "${GREEN}✓${NC} Installed into virtualenv and created wrappers in ~/.local/bin\n"
    return 0
}

# Helper: install via pip --user
install_via_pip_user() {
    if ! python3 -m pip --version >/dev/null 2>&1; then
        printf "${YELLOW}⚠${NC} python3-pip is not installed\n"
        PIP_INSTALL_CMD=""
        
        if command -v apt-get >/dev/null 2>&1; then
            PIP_INSTALL_CMD="apt-get install -y python3-pip"
        elif command -v dnf >/dev/null 2>&1; then
            PIP_INSTALL_CMD="dnf install -y python3-pip"
        elif command -v pacman >/dev/null 2>&1; then
            PIP_INSTALL_CMD="pacman -S --noconfirm python-pip"
        fi
        
        if [ -n "$PIP_INSTALL_CMD" ]; then
            DO_PIP_INSTALL="n"
            if [ -n "$PAPRWALL_AUTO_INSTALL" ]; then
                DO_PIP_INSTALL="y"
                printf "${BLUE}ℹ${NC} PAPRWALL_AUTO_INSTALL=1 detected — installing python3-pip automatically\n"
            elif [ -t 0 ] && [ -z "$SUDO_USER" ]; then
                printf "Install python3-pip now? (Y/n): "
                read -r REPLY
                case "$REPLY" in
                    [Nn]*) DO_PIP_INSTALL="n" ;;
                    *) DO_PIP_INSTALL="y" ;;
                esac
            else
                printf "${BLUE}ℹ${NC} Non-interactive or sudo session — not installing python3-pip automatically\n"
                printf "    Tip: export PAPRWALL_AUTO_INSTALL=1 to auto-install system packages\n"
            fi
            
            if [ "$DO_PIP_INSTALL" = "y" ]; then
                if command -v sudo >/dev/null 2>&1; then
                    sudo sh -c "$PIP_INSTALL_CMD"
                else
                    sh -c "$PIP_INSTALL_CMD"
                fi
            fi
        fi
    fi
    
    python3 -m ensurepip --upgrade >/dev/null 2>&1 || true
    python3 -m pip install --upgrade pip >>"$LOG_FILE" 2>&1 || true
    printf "${BLUE}ℹ${NC} Installing Paprwall into user site-packages (pip --user)\n"
    
    set +e
    python3 -m pip install -e . --user >>"$LOG_FILE" 2>&1
    RC=$?
    set -e
    return $RC
}

# Determine install mode
MODE="${PAPRWALL_INSTALL_MODE:-venv}"

if [ "$MODE" = "venv" ]; then
    if ! install_in_venv; then
        printf "${RED}✗${NC} Virtualenv installation failed. Install python3-venv or try PAPRWALL_INSTALL_MODE=auto.\n"
        printf -- "----- install log (last 150 lines) -----\n"
        tail -n 150 "$LOG_FILE" 2>/dev/null || true
        printf -- "----------------------------------------\n"
        exit 1
    fi
elif [ "$MODE" = "auto" ]; then
    if ! install_in_venv; then
        printf "${YELLOW}⚠${NC} Virtualenv failed, trying pip --user fallback...\n"
        if ! install_via_pip_user; then
            printf "${RED}✗${NC} pip --user installation failed\n"
            printf -- "----- pip output (last 200 lines) -----\n"
            tail -n 200 "$LOG_FILE" 2>/dev/null || true
            printf -- "---------------------------------------\n"
            exit 1
        fi
    fi
elif [ "$MODE" = "pip-user" ]; then
    if ! install_via_pip_user; then
        printf "${RED}✗${NC} pip --user installation failed\n"
        printf -- "----- pip output (last 200 lines) -----\n"
        tail -n 200 "$LOG_FILE" 2>/dev/null || true
        printf -- "---------------------------------------\n"
        exit 1
    fi
elif [ "$MODE" = "pip-system" ]; then
    printf "${YELLOW}⚠${NC} Installing into system site-packages (not recommended)\n"
    set +e
    python3 -m pip install -e . >>"$LOG_FILE" 2>&1
    RC_SYS=$?
    set -e
    if [ $RC_SYS -ne 0 ]; then
        printf "${RED}✗${NC} System pip install failed\n"
        printf -- "----- pip output (last 200 lines) -----\n"
        tail -n 200 "$LOG_FILE" 2>/dev/null || true
        printf -- "---------------------------------------\n"
        exit 1
    fi
else
    printf "${YELLOW}⚠${NC} Unknown PAPRWALL_INSTALL_MODE='%s', defaulting to venv\n" "$MODE"
    if ! install_in_venv; then
        printf "${RED}✗${NC} Virtualenv installation failed.\n"
        printf -- "----- install log (last 150 lines) -----\n"
        tail -n 150 "$LOG_FILE" 2>/dev/null || true
        printf -- "----------------------------------------\n"
        exit 1
    fi
fi

# Setup .env file
if [ -f ".env.example" ]; then
    cp .env.example .env
    printf "${GREEN}✓${NC} Created .env configuration file\n"
fi

# Function to fetch private .env
maybe_fetch_private_env() {
    DEFAULT_ENV_URL="https://github.com/riturajprofile/env-setup/blob/main/.env"
    INPUT_URL="${GITHUB_ENV_URL:-${PAPRWALL_ENV_URL:-$DEFAULT_ENV_URL}}"

    # Skip in non-interactive mode unless env var is set
    if [ ! -t 0 ] || [ -n "$SUDO_USER" ]; then
        if [ "$INPUT_URL" = "$DEFAULT_ENV_URL" ]; then
            printf "\n"
            printf "${BLUE}ℹ${NC} Skipping private .env download (non-interactive mode)\n"
            printf "    To enable: export PAPRWALL_GITHUB_TOKEN='your_token'\n"
            printf "    Then re-run: curl -fsSL ...install.sh | sh\n"
            return 0
        fi
    else
        printf "\n"
        printf "Are you the developer of this app? Then you totally have a GitHub token handy, right? (y/N): "
        read -r REPLY
        case "$REPLY" in
            [Yy]*) ;;
            *) return 0 ;;
        esac
    fi

    # Normalize GitHub URL (blob -> raw)
    RAW_URL="$INPUT_URL"
    case "$RAW_URL" in
        *github.com/*/blob/*)
            RAW_URL=$(printf "%s" "$RAW_URL" | sed 's|github.com/\([^/]*/[^/]*/\)blob/|raw.githubusercontent.com/\1|')
            ;;
        *github.com/*/raw/*)
            RAW_URL=$(printf "%s" "$RAW_URL" | sed 's|github.com/\([^/]*/[^/]*/\)raw/|raw.githubusercontent.com/\1|')
            ;;
    esac

    printf "${BLUE}ℹ${NC} Using .env source: %s\n" "$RAW_URL"

    # Get token
    GH_TOKEN="${GITHUB_TOKEN:-${PAPRWALL_GITHUB_TOKEN:-}}"
    if [ -z "$GH_TOKEN" ]; then
        printf "\n"
        printf "To access a PRIVATE repo, a GitHub token with 'repo' scope is required.\n"
        printf "The token is used only for this download and will not be stored.\n"
        printf "Enter GitHub token (input hidden): "
        stty -echo 2>/dev/null
        read -r GH_TOKEN
        stty echo 2>/dev/null
        printf "\n"
    else
        printf "${BLUE}ℹ${NC} Using GitHub token from environment\n"
    fi

    printf "${BLUE}ℹ${NC} Downloading private .env from GitHub (private repo)...\n"
    if curl -fsSL -H "Authorization: token $GH_TOKEN" "$RAW_URL" -o .env.tmp 2>/dev/null && [ -s .env.tmp ]; then
        mv .env.tmp .env
        printf "${GREEN}✓${NC} Downloaded and set .env from GitHub\n"
    else
        rm -f .env.tmp 2>/dev/null || true
        printf "${YELLOW}⚠${NC} Failed to download .env from provided URL. Keeping existing .env\n"
        printf "${YELLOW}   URL tried:${NC} %s\n" "$RAW_URL"
    fi

    unset GH_TOKEN
}

# Attempt to fetch private .env
maybe_fetch_private_env

printf "\n"
printf "${GREEN}╔════════════════════════════════════════╗${NC}\n"
printf "${GREEN}║   Installation Complete! 🎉           ║${NC}\n"
printf "${GREEN}╚════════════════════════════════════════╝${NC}\n"
printf "\n"
printf "📁 Installation: %s\n" "$INSTALL_DIR"
printf "\n"
printf "📝 Next steps:\n"
printf "\n"
printf "1. Get FREE API keys:\n"
printf "   • Pixabay: https://pixabay.com/api/docs/\n"
printf "   • Pexels: https://www.pexels.com/api/\n"
printf "\n"
printf "2. Add API keys:\n"
printf "   nano %s/.env\n" "$INSTALL_DIR"
printf "\n"
printf "3. Use Paprwall:\n"
printf "   paprwall --themes          # List themes\n"
printf "   paprwall --set-theme ocean # Set theme\n"
printf "   paprwall --fetch           # Get wallpapers\n"
printf "   paprwall-gui               # Launch GUI\n"
printf "\n"
printf "🔑 Attribution Secret: riturajprofile@162\n"
printf "   (Enter in GUI to remove desktop overlay)\n"
printf "\n"
printf "📖 Docs: %s/README.md\n" "$INSTALL_DIR"
printf "🆘 Help: https://github.com/riturajprofile/paprwall/issues\n"
printf "\n"

# Check service
if systemctl --user is-enabled paprwall >/dev/null 2>&1; then
    printf "${GREEN}✓${NC} Auto-start service enabled\n"
    printf "   Start: systemctl --user start paprwall\n"
fi

printf "\n"
printf "${BLUE}ℹ${NC} To uninstall: curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/uninstall.sh | sh\n"
printf "\n"
