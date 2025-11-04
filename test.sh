#!/usr/bin/env bash
#
# Quick test script for Paprwall
# Tests basic functionality after installation
#
set -e

echo "╔═══════════════════════════════════════════╗"
echo "║     Paprwall Test Suite                   ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

PASS=0
FAIL=0

test_command() {
    local name="$1"
    local cmd="$2"
    
    printf "Testing: %-40s" "$name"
    
    if eval "$cmd" >/dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAIL++))
        return 1
    fi
}

echo "🔍 Basic Checks"
echo "─────────────────────────────────────────────"

test_command "Python 3 installed" "command -v python3"
test_command "Python version >= 3.8" "python3 -c 'import sys; exit(0 if sys.version_info >= (3,8) else 1)'"
test_command "pip installed" "command -v pip || command -v pip3"
test_command "venv module available" "python3 -c 'import venv'"

echo ""
echo "📦 Installation Checks"
echo "─────────────────────────────────────────────"

test_command "paprwall command exists" "command -v paprwall"
test_command "wallpaper-manager exists" "command -v wallpaper-manager"
test_command "wallpaper-gui exists" "command -v wallpaper-gui"
test_command "Virtual env at ~/.paprwall" "test -d ~/.paprwall/.venv"

echo ""
echo "🐍 Python Imports"
echo "─────────────────────────────────────────────"

# Activate venv if it exists
if [ -f ~/.paprwall/.venv/bin/activate ]; then
    source ~/.paprwall/.venv/bin/activate
fi

test_command "Import paprwall" "python3 -c 'import paprwall'"
test_command "Import paprwall.api" "python3 -c 'import paprwall.api'"
test_command "Import paprwall.core" "python3 -c 'import paprwall.core'"
test_command "Import paprwall.config" "python3 -c 'import paprwall.config'"
test_command "Import paprwall.service" "python3 -c 'import paprwall.service'"
test_command "Import paprwall.utils" "python3 -c 'import paprwall.utils'"
test_command "Import tkinter (for GUI)" "python3 -c 'import tkinter'" || true

echo ""
echo "🖥️  CLI Commands"
echo "─────────────────────────────────────────────"

test_command "paprwall --help" "paprwall --help"
test_command "paprwall --sources" "paprwall --sources"
test_command "paprwall --themes" "paprwall --themes"
test_command "wallpaper-manager --help" "wallpaper-manager --help"

echo ""
echo "📁 Directory Structure"
echo "─────────────────────────────────────────────"

test_command "Config dir exists" "test -d ~/.config/paprwall || mkdir -p ~/.config/paprwall"
test_command "Data dir exists" "test -d ~/.local/share/paprwall || mkdir -p ~/.local/share/paprwall"
test_command "Can write to config" "touch ~/.config/paprwall/.test && rm ~/.config/paprwall/.test"
test_command "Can write to data" "touch ~/.local/share/paprwall/.test && rm ~/.local/share/paprwall/.test"

echo ""
echo "🔧 Desktop Environment"
echo "─────────────────────────────────────────────"

if [ -n "${XDG_CURRENT_DESKTOP:-}" ]; then
    echo "Desktop: $XDG_CURRENT_DESKTOP"
else
    echo "Desktop: Not detected"
fi

test_command "gsettings (GNOME)" "command -v gsettings" || true
test_command "qdbus (KDE)" "command -v qdbus" || true  
test_command "xfconf-query (XFCE)" "command -v xfconf-query" || true
test_command "feh (fallback)" "command -v feh" || true

echo ""
echo "═══════════════════════════════════════════════"
echo "Results: ${GREEN}${PASS} passed${NC}, ${RED}${FAIL} failed${NC}"
echo "═══════════════════════════════════════════════"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ All critical tests passed!${NC}"
    echo ""
    echo "Try these commands:"
    echo "  paprwall --fetch              # Download wallpapers"
    echo "  paprwall --set-theme nature   # Set theme"
    echo "  wallpaper-gui                 # Launch GUI"
    exit 0
else
    echo -e "${RED}✗ Some tests failed.${NC}"
    echo ""
    echo "Check installation with: ./install.sh"
    exit 1
fi
