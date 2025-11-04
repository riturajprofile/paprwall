#!/bin/bash
# PaprWall Uninstall Script for Linux

echo "=========================================="
echo "  PaprWall Uninstaller"
echo "=========================================="
echo ""

# Check if paprwall is installed
if [ ! -f "$HOME/.local/bin/paprwall-gui" ]; then
    echo "⚠️  PaprWall doesn't appear to be installed."
    echo ""
    read -p "Remove data files anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi
else
    echo "Found PaprWall installation"
    echo ""
    echo "This will remove:"
    echo "  • Application binary (~/.local/bin/paprwall-gui)"
    echo "  • Desktop entry"
    echo "  • Application icon"
    echo "  • Configuration and data files"
    echo ""
    read -p "Continue with uninstall? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi
fi

echo ""
echo "Uninstalling PaprWall..."
echo ""

# Remove binary
if [ -f "$HOME/.local/bin/paprwall-gui" ]; then
    rm "$HOME/.local/bin/paprwall-gui"
    echo "✓ Removed binary"
fi

# Remove desktop entry
if [ -f "$HOME/.local/share/applications/paprwall.desktop" ]; then
    rm "$HOME/.local/share/applications/paprwall.desktop"
    echo "✓ Removed desktop entry"
fi

# Remove icons
if [ -d "$HOME/.local/share/icons/hicolor/scalable/apps" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/scalable/apps/paprwall.svg"
    echo "✓ Removed SVG icon"
fi

if [ -d "$HOME/.local/share/icons/hicolor/256x256/apps" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/paprwall.png"
    echo "✓ Removed PNG icon"
fi

# Update icon cache
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
fi

# Ask about data files
echo ""
read -p "Remove configuration and wallpaper data? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Remove data directory (Linux)
    if [ -d "$HOME/.local/share/paprwall" ]; then
        echo ""
        echo "Data to be removed:"
        du -sh "$HOME/.local/share/paprwall" 2>/dev/null || echo "  ~/.local/share/paprwall/"
        echo ""
        read -p "Confirm deletion? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$HOME/.local/share/paprwall"
            echo "✓ Removed data directory"
        else
            echo "⊘ Kept data directory"
        fi
    fi
    
    # Remove old data directory if exists
    if [ -d "$HOME/.paprwall" ]; then
        rm -rf "$HOME/.paprwall"
        echo "✓ Removed old data directory"
    fi
else
    echo "⊘ Kept data files (wallpapers and history)"
    echo "   Location: ~/.local/share/paprwall/"
fi

echo ""
echo "=========================================="
echo "  ✓ Uninstall Complete"
echo "=========================================="
echo ""
echo "PaprWall has been removed from your system."
echo ""
echo "If you installed via pip, also run:"
echo "  pip uninstall paprwall"
echo ""
