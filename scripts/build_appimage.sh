#!/usr/bin/env bash
# PaprWall AppImage Build Script
# Creates a universal Linux executable that runs on all distributions

set -euo pipefail  # Exit on error and treat unset vars as errors

echo "========================================"
echo "PaprWall AppImage Builder"
echo "Universal Linux Package"
echo "========================================"
echo

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the correct directory
if [ ! -d "src/paprwall" ]; then
    echo -e "${RED}❌ Error: Please run this script from the project root directory${NC}"
    echo "Expected to find: src/paprwall/"
    exit 1
fi

# Check required tools
echo -e "${BLUE}Checking required tools...${NC}"

check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}❌ Error: $1 is not installed${NC}"
        if [ "${2:-}" != "" ]; then
            echo "Install with: $2"
        fi
        return 1
    else
        echo -e "${GREEN}✓ $1 found${NC}"
    fi
}

check_command python3 "sudo apt install python3"
check_command pip3 "sudo apt install python3-pip"
check_command wget "sudo apt install wget"

# Get version (ensure src is on PYTHONPATH)
VERSION=$(python3 - <<'PY'
import sys
sys.path.insert(0, 'src')
try:
    from paprwall.__version__ import __version__
except Exception:
    __version__ = '0.0.0'
print(__version__)
PY
)
echo -e "${GREEN}Building version: $VERSION${NC}"
echo

# Set variables
APPDIR="build/PaprWall.AppDir"
APPIMAGE_NAME="PaprWall-${VERSION}-x86_64.AppImage"
BUILD_DIR="build/appimage-build"

# Clean previous builds
echo -e "${BLUE}Cleaning previous AppImage builds...${NC}"
rm -rf "$APPDIR" "$BUILD_DIR" "$APPIMAGE_NAME"
mkdir -p "$APPDIR" "$BUILD_DIR"

# Create virtual environment for bundling
echo -e "${BLUE}Creating Python environment...${NC}"
cd "$BUILD_DIR"
python3 -m venv python-env
source python-env/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip setuptools wheel
pip install pyinstaller

# Install project dependencies
cd ../..
pip install -r requirements.txt
pip install -e .

echo -e "${GREEN}✓ Dependencies installed${NC}"

# Build with PyInstaller
echo -e "${BLUE}Building standalone executable with PyInstaller...${NC}"

pyinstaller --onefile \
    --name paprwall \
    --add-data "README.md:." \
    --add-data "LICENSE:." \
    --hidden-import PIL \
    --hidden-import PIL.Image \
    --hidden-import PIL.ImageDraw \
    --hidden-import PIL.ImageFont \
    --hidden-import PIL.ImageTk \
    --hidden-import requests \
    --hidden-import tkinter \
    --hidden-import tkinter.ttk \
    --hidden-import tkinter.filedialog \
    --hidden-import tkinter.messagebox \
    --hidden-import paprwall \
    --hidden-import paprwall.core \
    --hidden-import paprwall.gui \
    --hidden-import paprwall.gui.wallpaper_manager_gui \
    --hidden-import paprwall.cli \
    --hidden-import paprwall.installer \
    --exclude-module matplotlib \
    --exclude-module numpy \
    --exclude-module scipy \
    --exclude-module pandas \
    --exclude-module jupyter \
    --exclude-module IPython \
    --exclude-module pytest \
    --exclude-module unittest \
    --exclude-module setuptools \
    --exclude-module distutils \
    --windowed \
    --strip \
    --clean \
    src/paprwall/gui/wallpaper_manager_gui.py

if [ ! -f "dist/paprwall" ]; then
    echo -e "${RED}❌ Build failed: Executable not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Executable built successfully${NC}"

# Create AppDir structure
echo -e "${BLUE}Creating AppImage directory structure...${NC}"

# Create required directories
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/lib"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$APPDIR/usr/share/metainfo"

# Copy executable
cp dist/paprwall "$APPDIR/usr/bin/paprwall"
chmod +x "$APPDIR/usr/bin/paprwall"

# Create AppRun script (entry point)
cat > "$APPDIR/AppRun" << 'APPRUN_EOF'
#!/bin/bash
# AppImage entry point for PaprWall

HERE="$(dirname "$(readlink -f "${0}")")"

# Set up environment
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
export PYTHONHOME="${HERE}/usr"
export PYTHONPATH="${HERE}/usr/lib/python3:${PYTHONPATH}"

# Handle command line arguments
case "$1" in
    --install)
        exec "${HERE}/usr/bin/paprwall" --install
        ;;
    --uninstall)
        exec "${HERE}/usr/bin/paprwall" --uninstall
        ;;
    --version)
        exec "${HERE}/usr/bin/paprwall" --version
        ;;
    --help|-h)
        echo "PaprWall - Modern Desktop Wallpaper Manager"
        echo ""
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --install      Install PaprWall to system"
        echo "  --uninstall    Uninstall PaprWall from system"
        echo "  --version      Show version information"
        echo "  --help, -h     Show this help message"
        echo ""
        echo "Run without arguments to launch the GUI"
        exit 0
        ;;
    *)
        # Launch GUI
        exec "${HERE}/usr/bin/paprwall"
        ;;
esac
APPRUN_EOF

chmod +x "$APPDIR/AppRun"

# Create desktop entry
cat > "$APPDIR/paprwall.desktop" << DESKTOP_EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=PaprWall
Comment=Modern Desktop Wallpaper Manager with Motivational Quotes
GenericName=Wallpaper Manager
Exec=paprwall
Icon=paprwall
Terminal=false
Categories=Graphics;Photography;Utility;
Keywords=wallpaper;background;desktop;quotes;image;
StartupNotify=true
StartupWMClass=PaprWall
MimeType=image/jpeg;image/png;image/bmp;
DESKTOP_EOF

# Copy desktop file to standard location
cp "$APPDIR/paprwall.desktop" "$APPDIR/usr/share/applications/"

# Create AppStream metadata
cat > "$APPDIR/usr/share/metainfo/paprwall.appdata.xml" << METADATA_EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>com.github.riturajprofile.paprwall</id>
  <metadata_license>MIT</metadata_license>
  <project_license>MIT</project_license>
  <name>PaprWall</name>
  <summary>Modern Desktop Wallpaper Manager with Motivational Quotes</summary>

  <description>
    <p>
      Transform your desktop with stunning wallpapers embedded with inspirational quotes.
      PaprWall brings a fresh, modern approach to wallpaper management with automatic
      rotation and quote personalization.
    </p>
    <p>Features:</p>
    <ul>
      <li>Modern GUI with large preview panel</li>
      <li>6 quote categories (Motivational, Mathematics, Science, Famous, Technology, Philosophy)</li>
      <li>Auto-rotation with customizable intervals</li>
      <li>History gallery with thumbnails</li>
      <li>Multi-desktop environment support</li>
    </ul>
  </description>

  <launchable type="desktop-id">paprwall.desktop</launchable>

  <screenshots>
    <screenshot type="default">
      <caption>Main window with wallpaper preview</caption>
    </screenshot>
  </screenshots>

  <url type="homepage">https://github.com/riturajprofile/paprwall</url>
  <url type="bugtracker">https://github.com/riturajprofile/paprwall/issues</url>

  <provides>
    <binary>paprwall</binary>
  </provides>

  <releases>
    <release version="$VERSION" date="$(date +%Y-%m-%d)">
      <description>
        <p>Latest release with improvements and bug fixes.</p>
      </description>
    </release>
  </releases>
</component>
METADATA_EOF

# Create or download icon
echo -e "${BLUE}Creating application icon...${NC}"

# Check if icon already exists
if [ -f "assets/icon.png" ]; then
    cp "assets/icon.png" "$APPDIR/paprwall.png"
    cp "assets/icon.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/paprwall.png"
else
    # Create a simple text-based icon using ImageMagick if available
    if command -v convert &> /dev/null; then
        convert -size 256x256 xc:blue \
                -font DejaVu-Sans-Bold -pointsize 72 \
                -fill white -gravity center \
                -annotate +0+0 "PW" \
                "$APPDIR/paprwall.png"
        cp "$APPDIR/paprwall.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/paprwall.png"
    else
        # Create a minimal icon file
        echo "Creating placeholder icon..."
        touch "$APPDIR/paprwall.png"
        touch "$APPDIR/usr/share/icons/hicolor/256x256/apps/paprwall.png"
    fi
fi

# Copy icon to all required locations
cp "$APPDIR/paprwall.png" "$APPDIR/.DirIcon"

# Copy additional resources if they exist
if [ -f "README.md" ]; then
    cp "README.md" "$APPDIR/"
fi
if [ -f "LICENSE" ]; then
    cp "LICENSE" "$APPDIR/"
fi

echo -e "${GREEN}✓ AppDir structure created${NC}"

# Download appimagetool if not present
echo -e "${BLUE}Checking for appimagetool...${NC}"

APPIMAGETOOL="build/appimagetool-x86_64.AppImage"

if [ ! -f "$APPIMAGETOOL" ]; then
    echo "Downloading appimagetool..."
    wget -O "$APPIMAGETOOL" \
        "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x "$APPIMAGETOOL"
    echo -e "${GREEN}✓ appimagetool downloaded${NC}"
else
    echo -e "${GREEN}✓ appimagetool already present${NC}"
fi

# Build AppImage
echo -e "${BLUE}Building AppImage...${NC}"
echo

# Set ARCH for appimagetool
export ARCH=x86_64

# Build the AppImage
"$APPIMAGETOOL" "$APPDIR" "$APPIMAGE_NAME"

if [ ! -f "$APPIMAGE_NAME" ]; then
    echo -e "${RED}❌ AppImage creation failed${NC}"
    exit 1
fi

# Make AppImage executable
chmod +x "$APPIMAGE_NAME"

# Calculate checksum
echo -e "${BLUE}Calculating checksum...${NC}"
sha256sum "$APPIMAGE_NAME" > "${APPIMAGE_NAME}.sha256"

# Get file size
FILE_SIZE=$(du -h "$APPIMAGE_NAME" | cut -f1)

# Create release directory
RELEASE_DIR="release-appimage-v${VERSION}"
mkdir -p "$RELEASE_DIR"

# Copy AppImage to release directory
cp "$APPIMAGE_NAME" "$RELEASE_DIR/"
cp "${APPIMAGE_NAME}.sha256" "$RELEASE_DIR/"

# Create README for AppImage
cat > "$RELEASE_DIR/README.md" << README_EOF
# PaprWall v${VERSION} - AppImage Release

## 🚀 Universal Linux Package

This AppImage works on **ALL Linux distributions** without installation!

### ✨ Features
- ✅ Runs on Ubuntu, Fedora, Arch, Debian, Mint, etc.
- ✅ No installation required
- ✅ No root/admin rights needed
- ✅ Self-contained with all dependencies
- ✅ Works on any Linux distribution

### 📥 How to Use

1. **Download the AppImage**
   \`\`\`bash
   wget https://github.com/riturajprofile/paprwall/releases/download/v${VERSION}/${APPIMAGE_NAME}
   \`\`\`

2. **Make it executable**
   \`\`\`bash
   chmod +x ${APPIMAGE_NAME}
   \`\`\`

3. **Run it!**
   \`\`\`bash
   ./${APPIMAGE_NAME}
   \`\`\`

### 🔧 Command Line Options

\`\`\`bash
# Launch GUI (default)
./${APPIMAGE_NAME}

# Install to system (creates desktop entry)
./${APPIMAGE_NAME} --install

# Uninstall from system
./${APPIMAGE_NAME} --uninstall

# Show version
./${APPIMAGE_NAME} --version

# Show help
./${APPIMAGE_NAME} --help
\`\`\`

### 🖥️ System Integration

**Optional Installation:**
\`\`\`bash
# Install PaprWall to your system
./${APPIMAGE_NAME} --install

# This creates:
# • Application menu entry
# • Desktop integration
# • Icon in system menu
# • Easy uninstall option

# You can still run the AppImage directly without installing
\`\`\`

### 📋 System Requirements

- **OS**: Any Linux distribution (kernel 3.10+)
- **Architecture**: x86_64 (64-bit)
- **Desktop**: X11 or Wayland
- **Dependencies**: None! (all bundled)

### 🔒 Verify Download

\`\`\`bash
# Verify checksum
sha256sum -c ${APPIMAGE_NAME}.sha256
\`\`\`

### 💡 Tips

1. **Keep in a permanent location**
   - Move to ~/Applications/ or ~/bin/
   - Don't delete after running

2. **Create desktop shortcut** (optional)
   \`\`\`bash
   ./${APPIMAGE_NAME} --install
   \`\`\`

3. **Run from anywhere**
   \`\`\`bash
   # Add to PATH
   sudo ln -s $(pwd)/${APPIMAGE_NAME} /usr/local/bin/paprwall
   # Now run: paprwall
   \`\`\`

### 🗑️ Uninstallation

\`\`\`bash
# If you installed it:
./${APPIMAGE_NAME} --uninstall

# Then simply delete the AppImage file
rm ${APPIMAGE_NAME}
\`\`\`

### ❓ Troubleshooting

**Problem: Permission denied**
\`\`\`bash
chmod +x ${APPIMAGE_NAME}
\`\`\`

**Problem: FUSE not installed**
\`\`\`bash
# Ubuntu/Debian
sudo apt install fuse libfuse2

# Fedora
sudo dnf install fuse fuse-libs

# Arch
sudo pacman -S fuse2
\`\`\`

**Problem: AppImage won't run**
\`\`\`bash
# Extract and run manually
./${APPIMAGE_NAME} --appimage-extract
./squashfs-root/AppRun
\`\`\`

### 📊 File Information

- **File**: ${APPIMAGE_NAME}
- **Size**: ${FILE_SIZE}
- **Version**: ${VERSION}
- **Built**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
- **Architecture**: x86_64
- **Format**: AppImage

### 🆘 Support

- **GitHub**: https://github.com/riturajprofile/paprwall
- **Issues**: https://github.com/riturajprofile/paprwall/issues
- **Documentation**: https://github.com/riturajprofile/paprwall#readme

---

**Built with ❤️ for the Linux community**
README_EOF

# Display summary
echo
echo -e "${GREEN}========================================"
echo "AppImage Build Complete!"
echo "========================================${NC}"
echo
echo -e "${GREEN}Version:${NC} $VERSION"
echo -e "${GREEN}File:${NC} $APPIMAGE_NAME"
echo -e "${GREEN}Size:${NC} $FILE_SIZE"
echo -e "${GREEN}Location:${NC} $(pwd)/$APPIMAGE_NAME"
echo -e "${GREEN}Release:${NC} $RELEASE_DIR/"
echo
echo -e "${BLUE}Files created:${NC}"
echo "  📦 $APPIMAGE_NAME"
echo "  🔒 ${APPIMAGE_NAME}.sha256"
echo "  📁 $RELEASE_DIR/"
echo
echo -e "${YELLOW}To test the AppImage:${NC}"
echo "  chmod +x $APPIMAGE_NAME"
echo "  ./$APPIMAGE_NAME"
echo
echo -e "${YELLOW}To install to system:${NC}"
echo "  ./$APPIMAGE_NAME --install"
echo
echo -e "${GREEN}🎉 Ready for distribution!${NC}"
echo
