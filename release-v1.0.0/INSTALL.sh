#!/bin/bash

# PaprWall v1.0.0 Installation Script
# Modern Desktop Wallpaper Manager

set -e

VERSION="1.0.0"
INSTALL_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

echo "=========================================="
echo "  PaprWall v${VERSION} Installation"
echo "=========================================="
echo ""

# Create directories
echo "Creating directories..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

# Install binaries
echo "Installing binaries..."
if [ -f "paprwall" ]; then
    cp paprwall "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/paprwall"
    echo "✓ CLI installed to $INSTALL_DIR/paprwall"
else
    echo "⚠ Warning: paprwall binary not found"
fi

if [ -f "paprwall-gui" ]; then
    cp paprwall-gui "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/paprwall-gui"
    echo "✓ GUI installed to $INSTALL_DIR/paprwall-gui"
else
    echo "⚠ Warning: paprwall-gui binary not found"
fi

# Create desktop entry
echo "Creating desktop entry..."
cat > "$DESKTOP_DIR/paprwall.desktop" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=PaprWall
GenericName=Wallpaper Manager
Comment=Modern Desktop Wallpaper Manager with Quote Embedding
Exec=paprwall-gui
Icon=paprwall
Terminal=false
Categories=Utility;Graphics;
Keywords=wallpaper;background;desktop;quotes;motivation;
EOF

echo "✓ Desktop entry created"

# Create simple icon (text-based)
echo "Creating application icon..."
cat > "$ICON_DIR/paprwall.svg" << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <rect width="256" height="256" fill="#2C3E50"/>
  <circle cx="128" cy="128" r="80" fill="#3498DB" opacity="0.3"/>
  <text x="128" y="150" font-family="Arial" font-size="100" font-weight="bold" fill="#ECF0F1" text-anchor="middle">PW</text>
</svg>
EOF

echo "✓ Icon created"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

# Check PATH
echo ""
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "⚠ Warning: $INSTALL_DIR is not in your PATH"
    echo ""
    echo "Add this to your ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

echo "=========================================="
echo "  Installation Complete!"
echo "=========================================="
echo ""
echo "Usage:"
echo "  CLI: paprwall --help"
echo "  GUI: paprwall-gui"
echo "  Or search 'PaprWall' in your application menu"
echo ""
echo "Documentation: See README.md"
echo "Changelog: See CHANGELOG.md"
echo ""

# Ask to launch
read -p "Launch PaprWall GUI now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    "$INSTALL_DIR/paprwall-gui" &
    echo "✓ PaprWall launched!"
fi
