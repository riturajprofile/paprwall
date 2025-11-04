#!/usr/bin/env bash
#
# Build standalone binaries with PyInstaller
# Creates self-contained executables for distribution
#
set -euo pipefail

echo "╔═══════════════════════════════════════════╗"
echo "║     Paprwall Binary Builder               ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo_info() { echo -e "${BLUE}ℹ${NC} $1"; }
echo_success() { echo -e "${GREEN}✓${NC} $1"; }
echo_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
echo_error() { echo -e "${RED}✗${NC} $1"; }

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo_info "Installing PyInstaller..."
    pip install pyinstaller
    echo_success "PyInstaller installed"
    echo ""
fi

# Clean previous builds
echo_info "Cleaning previous builds..."
rm -rf build/ dist/wallpaper-* dist/*.spec
echo_success "Cleaned build artifacts"
echo ""

# Get version
VERSION=$(grep -E "version=\"[0-9.]+\"" setup.py | sed -E 's/.*version="([0-9.]+)".*/\1/')
echo_info "Building binaries for Paprwall v$VERSION"
echo ""

# Build CLI binary
echo_info "Building wallpaper-manager (CLI)..."
pyinstaller \
    --onefile \
    --name wallpaper-manager \
    --hidden-import=paprwall.api \
    --hidden-import=paprwall.core \
    --hidden-import=paprwall.config \
    --hidden-import=paprwall.service \
    --hidden-import=paprwall.utils \
    src/paprwall/wallpaper_cli.py

if [ $? -eq 0 ]; then
    echo_success "CLI binary built successfully"
    echo ""
else
    echo_error "CLI build failed"
    exit 1
fi

# Build GUI binary
echo_info "Building wallpaper-gui (GUI)..."
pyinstaller \
    --onefile \
    --name wallpaper-gui \
    --hidden-import=paprwall.api \
    --hidden-import=paprwall.core \
    --hidden-import=paprwall.config \
    --hidden-import=paprwall.service \
    --hidden-import=paprwall.utils \
    --hidden-import=tkinter \
    src/paprwall/gui/wallpaper_manager_gui.py

if [ $? -eq 0 ]; then
    echo_success "GUI binary built successfully"
    echo ""
else
    echo_error "GUI build failed"
    exit 1
fi

# Test binaries
echo_info "Testing binaries..."
echo ""

echo "Testing wallpaper-manager:"
./dist/wallpaper-manager --version 2>/dev/null || ./dist/wallpaper-manager --help | head -3
echo ""

echo "Testing wallpaper-gui:"
echo "(GUI will not launch in headless mode, checking if it starts)"
timeout 2 ./dist/wallpaper-gui 2>&1 || true
echo ""

# Show binary info
echo_info "Binary information:"
ls -lh dist/wallpaper-* | awk '{print "  " $9 " - " $5}'
echo ""

# Create archive
echo_info "Creating distribution archive..."
ARCHIVE_NAME="paprwall-v$VERSION-linux-x64"
mkdir -p "$ARCHIVE_NAME"
cp dist/wallpaper-manager "$ARCHIVE_NAME/"
cp dist/wallpaper-gui "$ARCHIVE_NAME/"
cp README.md "$ARCHIVE_NAME/"
cp LICENSE "$ARCHIVE_NAME/"

# Create install script for binary distribution
cat > "$ARCHIVE_NAME/install.sh" << 'EOF'
#!/bin/bash
# Install prebuilt Paprwall binaries

set -e

BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

echo "Installing Paprwall binaries..."
cp wallpaper-manager "$BIN_DIR/"
cp wallpaper-gui "$BIN_DIR/"
chmod +x "$BIN_DIR/wallpaper-manager"
chmod +x "$BIN_DIR/wallpaper-gui"

echo "✓ Installed to $BIN_DIR"
echo ""
echo "Make sure $BIN_DIR is in your PATH:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
echo "Try: wallpaper-manager --help"
EOF

chmod +x "$ARCHIVE_NAME/install.sh"

# Create tarball
tar czf "${ARCHIVE_NAME}.tar.gz" "$ARCHIVE_NAME"
echo_success "Created ${ARCHIVE_NAME}.tar.gz"
echo ""

# Cleanup temp directory
rm -rf "$ARCHIVE_NAME"

# Summary
echo "╔═══════════════════════════════════════════╗"
echo "║     Binary Build Complete! 🎉             ║"
echo "╚═══════════════════════════════════════════╝"
echo ""
echo_success "Standalone binaries created:"
echo "  • dist/wallpaper-manager"
echo "  • dist/wallpaper-gui"
echo "  • ${ARCHIVE_NAME}.tar.gz (distribution archive)"
echo ""
echo "📝 Distribution:"
echo ""
echo "  Users can extract and install with:"
echo "    tar xzf ${ARCHIVE_NAME}.tar.gz"
echo "    cd $ARCHIVE_NAME"
echo "    ./install.sh"
echo ""
echo "  Or upload to GitHub Releases:"
echo "    https://github.com/riturajprofile/paprwall/releases"
echo ""
