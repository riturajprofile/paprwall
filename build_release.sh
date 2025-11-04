#!/bin/bash
# PaprWall v1.0.0 Release Build Script

set -e  # Exit on error

echo "=========================================="
echo "  PaprWall v1.0.0 Release Builder"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv-build" ]; then
    echo -e "${YELLOW}Creating build virtual environment...${NC}"
    python3 -m venv .venv-build
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source .venv-build/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip wheel setuptools

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt
pip install pyinstaller

# Clean previous builds
echo -e "${YELLOW}Cleaning previous builds...${NC}"
rm -rf build/ dist/ *.spec
rm -rf src/paprwall.egg-info

# Create version file
echo -e "${BLUE}Creating version info...${NC}"
cat > src/paprwall/__version__.py << 'EOF'
"""Version information for PaprWall."""
__version__ = "1.0.0"
__author__ = "riturajprofile"
__description__ = "Modern Desktop Wallpaper Manager"
EOF

# Build GUI application with PyInstaller
echo -e "${GREEN}Building GUI application...${NC}"
pyinstaller --name=paprwall-gui \
    --onefile \
    --windowed \
    --icon=assets/icon.png 2>/dev/null || true \
    --add-data="src/paprwall:paprwall" \
    --hidden-import=PIL._tkinter_finder \
    src/paprwall/gui/wallpaper_manager_gui.py

# Build CLI application
echo -e "${GREEN}Building CLI application...${NC}"
pyinstaller --name=paprwall \
    --onefile \
    --console \
    --add-data="src/paprwall:paprwall" \
    src/paprwall/cli.py

# Create distribution package
echo -e "${GREEN}Creating distribution package...${NC}"
python -m build

# Create release directory
RELEASE_DIR="release-v1.0.0"
mkdir -p "$RELEASE_DIR"

# Copy binaries
echo -e "${BLUE}Copying binaries to release directory...${NC}"
cp dist/paprwall-gui "$RELEASE_DIR/" 2>/dev/null || echo "GUI binary not found"
cp dist/paprwall "$RELEASE_DIR/" 2>/dev/null || echo "CLI binary not found"

# Copy documentation
echo -e "${BLUE}Copying documentation...${NC}"
cp README.md "$RELEASE_DIR/" 2>/dev/null || echo "README not found"
cp LICENSE "$RELEASE_DIR/" 2>/dev/null || echo "LICENSE not found"
cp CHANGELOG.md "$RELEASE_DIR/" 2>/dev/null || echo "CHANGELOG not found"

# Create installation script
echo -e "${BLUE}Creating installation script...${NC}"
cat > "$RELEASE_DIR/INSTALL.sh" << 'INSTALLEOF'
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

# Copy binaries
echo "Installing binaries..."
cp paprwall-gui ~/.local/bin/ 2>/dev/null && chmod +x ~/.local/bin/paprwall-gui
cp paprwall ~/.local/bin/ 2>/dev/null && chmod +x ~/.local/bin/paprwall

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc 2>/dev/null || true
    echo "Added ~/.local/bin to PATH"
fi

# Create desktop entry
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/paprwall.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=PaprWall
Comment=Modern Desktop Wallpaper Manager
Exec=$HOME/.local/bin/paprwall-gui
Terminal=false
Categories=Utility;Settings;DesktopSettings;
Keywords=wallpaper;background;desktop;
EOF

echo ""
echo "✅ Installation complete!"
echo ""
echo "Run 'paprwall-gui' to launch the GUI"
echo "Run 'paprwall --help' for CLI commands"
echo ""
echo "Note: You may need to restart your terminal or run:"
echo "  source ~/.bashrc"
INSTALLEOF

chmod +x "$RELEASE_DIR/INSTALL.sh"

# Create a tarball
echo -e "${GREEN}Creating release archive...${NC}"
tar -czf "paprwall-v1.0.0-linux-x64.tar.gz" "$RELEASE_DIR"

# Generate checksums
echo -e "${BLUE}Generating checksums...${NC}"
sha256sum "paprwall-v1.0.0-linux-x64.tar.gz" > "paprwall-v1.0.0-linux-x64.tar.gz.sha256"

# Summary
echo ""
echo -e "${GREEN}=========================================="
echo "  Build Complete! ✅"
echo -e "==========================================${NC}"
echo ""
echo "📦 Release package: paprwall-v1.0.0-linux-x64.tar.gz"
echo "📁 Release directory: $RELEASE_DIR/"
echo ""
echo "Contents:"
ls -lh "$RELEASE_DIR/"
echo ""
echo "Archive size:"
ls -lh paprwall-v1.0.0-linux-x64.tar.gz
echo ""
echo "SHA-256 checksum:"
cat paprwall-v1.0.0-linux-x64.tar.gz.sha256
echo ""
echo -e "${YELLOW}To test the build:${NC}"
echo "  cd $RELEASE_DIR"
echo "  ./INSTALL.sh"
echo ""
echo -e "${YELLOW}To create a GitHub release:${NC}"
echo "  1. Create a new tag: git tag -a v1.0.0 -m 'Release v1.0.0'"
echo "  2. Push the tag: git push origin v1.0.0"
echo "  3. Upload paprwall-v1.0.0-linux-x64.tar.gz to GitHub releases"
echo ""
