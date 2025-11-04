#!/bin/bash
# PaprWall v1.0.0 Installation Script

echo "=========================================="
echo "  Installing PaprWall v1.0.0"
echo "=========================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo "Please don't run as root. Run as normal user."
   exit 1
fi

# Create local bin directory
mkdir -p ~/.local/bin

# Copy GUI binary
echo "Installing GUI binary..."
if [ -f paprwall-gui ]; then
    cp paprwall-gui ~/.local/bin/ && chmod +x ~/.local/bin/paprwall-gui
    echo "✓ Installed paprwall-gui to ~/.local/bin/"
else
    echo "❌ Error: paprwall-gui binary not found!"
    exit 1
fi

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc 2>/dev/null || true
    echo "✓ Added ~/.local/bin to PATH"
fi

# Create icon directory
mkdir -p ~/.local/share/icons/hicolor/256x256/apps
mkdir -p ~/.local/share/icons/hicolor/scalable/apps

# Copy SVG icon if it exists in the package
if [ -f "paprwall.svg" ]; then
    cp paprwall.svg ~/.local/share/icons/hicolor/scalable/apps/paprwall.svg
    echo "✓ Installed icon"
else
    echo "⚠ Icon file not found in package"
fi

# Create PNG icon from SVG (if available)
if command -v convert &> /dev/null; then
    convert ~/.local/share/icons/hicolor/scalable/apps/paprwall.svg \
            -resize 256x256 \
            ~/.local/share/icons/hicolor/256x256/apps/paprwall.png 2>/dev/null || true
fi

# Create desktop entry
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/paprwall.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=PaprWall
Comment=Modern Desktop Wallpaper Manager with Motivational Quotes
Exec=paprwall-gui
Icon=paprwall
Terminal=false
Categories=Utility;Settings;DesktopSettings;Graphics;
Keywords=wallpaper;background;desktop;quotes;motivation;
EOF

# Update icon cache
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor 2>/dev/null || true
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database ~/.local/share/applications 2>/dev/null || true
fi

# Copy uninstall script to install location
if [ -f "uninstall.sh" ]; then
    mkdir -p ~/.local/share/paprwall
    cp uninstall.sh ~/.local/share/paprwall/
    chmod +x ~/.local/share/paprwall/uninstall.sh
    echo "✓ Uninstall script installed to ~/.local/share/paprwall/"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "Launch GUI:"
echo "  paprwall-gui"
echo ""
echo "Or search 'PaprWall' in your application menu"
echo ""
echo "To uninstall later:"
echo "  ~/.local/share/paprwall/uninstall.sh"
echo ""
echo "Note: You may need to restart your terminal or run:"
echo "  source ~/.bashrc"
