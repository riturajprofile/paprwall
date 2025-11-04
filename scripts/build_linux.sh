#!/bin/bash
# PaprWall Linux Build Script
# Builds standalone executable and packages (.deb, .rpm, .AppImage)

set -e  # Exit on any error

echo "========================================"
echo "PaprWall Linux Build Script"
echo "========================================"
echo

# Check if we're in the correct directory
if [ ! -d "src/paprwall" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "Expected to find: src/paprwall/"
    exit 1
fi

# Check required tools
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "❌ Error: $1 is not installed"
        if [ "$2" != "" ]; then
            echo "Install with: $2"
        fi
        return 1
    fi
}

echo "Checking required tools..."
check_command python3 "sudo apt install python3"
check_command pip3 "sudo apt install python3-pip"

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✓ Python version: $python_version"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "❌ Error: Python 3.8+ is required"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip and install build dependencies
echo "Installing/upgrading build dependencies..."
pip install --upgrade pip setuptools wheel
pip install pyinstaller>=5.0

# Install project dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt

# Install project in development mode
echo "Installing project in development mode..."
pip install -e .

# Get version information
VERSION=$(python3 -c "from paprwall import __version__; print(__version__)")
echo "Building version: $VERSION"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist build
mkdir -p build

# Build executable using PyInstaller
echo "Building Linux executable..."
pyinstaller --onefile \
    --name paprwall-gui \
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

# Check if build was successful
if [ ! -f "dist/paprwall-gui" ]; then
    echo "❌ Build failed: Executable not found"
    echo "Check the output above for errors"
    exit 1
fi

echo "✓ Executable built successfully"

# Make executable
chmod +x dist/paprwall-gui

# Create release directory
RELEASE_DIR="release-v$VERSION"
echo "Creating release package: $RELEASE_DIR"
rm -rf "$RELEASE_DIR"
mkdir -p "$RELEASE_DIR"

# Copy executable and required files
cp "dist/paprwall-gui" "$RELEASE_DIR/"
[ -f "README.md" ] && cp "README.md" "$RELEASE_DIR/"
[ -f "LICENSE" ] && cp "LICENSE" "$RELEASE_DIR/"

# Create installation scripts
echo "Creating installation scripts..."

# Create installer script
cat > "$RELEASE_DIR/install.sh" << 'EOF'
#!/bin/bash
# PaprWall Linux Installer

set -e

echo "PaprWall Linux Installer"
echo "======================="
echo

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Warning: Running as root. Installing system-wide."
    INSTALL_SYSTEM=true
else
    echo "Installing for current user..."
    INSTALL_SYSTEM=false
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXECUTABLE="$SCRIPT_DIR/paprwall-gui"

if [ ! -f "$EXECUTABLE" ]; then
    echo "❌ Error: paprwall-gui executable not found in $SCRIPT_DIR"
    exit 1
fi

# Run the installer
"$EXECUTABLE" --install

if [ $? -eq 0 ]; then
    echo
    echo "✓ PaprWall installed successfully!"
    echo "You can now find PaprWall in your application menu."
    echo
    echo "To run PaprWall:"
    echo "  - Search for 'PaprWall' in your application menu, or"
    echo "  - Run: paprwall-gui"
    echo
else
    echo "❌ Installation failed"
    exit 1
fi
EOF

# Create uninstaller script
cat > "$RELEASE_DIR/uninstall.sh" << 'EOF'
#!/bin/bash
# PaprWall Linux Uninstaller

set -e

echo "PaprWall Linux Uninstaller"
echo "========================="
echo

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXECUTABLE="$SCRIPT_DIR/paprwall-gui"

if [ ! -f "$EXECUTABLE" ]; then
    echo "❌ Error: paprwall-gui executable not found in $SCRIPT_DIR"
    exit 1
fi

# Run the uninstaller
"$EXECUTABLE" --uninstall

echo "✓ PaprWall uninstalled successfully!"
EOF

# Create simple run script
cat > "$RELEASE_DIR/run.sh" << 'EOF'
#!/bin/bash
# Run PaprWall

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/paprwall-gui"
EOF

# Make scripts executable
chmod +x "$RELEASE_DIR"/*.sh

# Create README for release
cat > "$RELEASE_DIR/README.md" << EOF
# PaprWall v$VERSION - Linux Release

## Quick Start

1. **Run PaprWall**: \`./paprwall-gui\`
2. **Install to System**: \`./install.sh\`
3. **Uninstall**: \`./uninstall.sh\`

## Files Included

- \`paprwall-gui\` - Main application (standalone executable)
- \`install.sh\` - System installer (creates desktop entry, shortcuts)
- \`uninstall.sh\` - System uninstaller
- \`run.sh\` - Simple launcher
- \`README.md\` - This file
- \`LICENSE\` - License information

## System Requirements

- Linux (Ubuntu 20.04+, Fedora 35+, Arch, Debian, etc.)
- X11 or Wayland display server
- Display: 720p or higher recommended
- Internet connection for downloading wallpapers

## Dependencies

The executable is self-contained and includes all required dependencies. However, you may need to install:

\`\`\`bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
\`\`\`

## Desktop Environment Support

- ✅ GNOME (Ubuntu, Fedora)
- ✅ KDE Plasma (Kubuntu, KDE Neon)
- ✅ XFCE (Xubuntu)
- ✅ MATE (Ubuntu MATE)
- ✅ Cinnamon (Linux Mint)
- ✅ LXQt / LXDE

## First Run

When you run PaprWall for the first time, it will ask if you want to install it to your system. This creates:

- Desktop entry (appears in application menu)
- Application icon
- Uninstall script

## Manual Installation

If the automatic installer doesn't work, you can manually:

1. Copy \`paprwall-gui\` to \`~/.local/bin/\`
2. Make it executable: \`chmod +x ~/.local/bin/paprwall-gui\`
3. Add \`~/.local/bin\` to your PATH if not already there

## Support

- Issues: https://github.com/riturajprofile/paprwall/issues
- Documentation: https://github.com/riturajprofile/paprwall

---
Built on $(date)
Architecture: $(uname -m)
Kernel: $(uname -r)
EOF

# Calculate file sizes and create manifest
echo "Creating build manifest..."
find "$RELEASE_DIR" -type f -exec ls -lh {} \; | awk '{print $9 " - " $5}' > "$RELEASE_DIR/FILES.txt"

# Create TAR.GZ archive
echo "Creating TAR.GZ archive..."
ARCHIVE_NAME="paprwall-v$VERSION-linux-$(uname -m).tar.gz"
rm -f "$ARCHIVE_NAME"

tar -czf "$ARCHIVE_NAME" -C . "$RELEASE_DIR"

if [ -f "$ARCHIVE_NAME" ]; then
    echo "✓ Created: $ARCHIVE_NAME"
else
    echo "❌ Failed to create TAR.GZ archive"
fi

# Calculate checksums
echo "Calculating checksums..."
sha256sum "$ARCHIVE_NAME" > "$ARCHIVE_NAME.sha256"
sha256sum "dist/paprwall-gui" > "paprwall-gui.sha256"

# Try to build packages if tools are available
echo "Checking for package building tools..."

# Build .deb package if possible
if command -v dpkg-deb &> /dev/null; then
    echo "Building .deb package..."

    DEB_DIR="build/paprwall_${VERSION}_amd64"
    mkdir -p "$DEB_DIR/DEBIAN"
    mkdir -p "$DEB_DIR/usr/local/bin"
    mkdir -p "$DEB_DIR/usr/share/applications"
    mkdir -p "$DEB_DIR/usr/share/pixmaps"

    # Copy executable
    cp "dist/paprwall-gui" "$DEB_DIR/usr/local/bin/"

    # Create control file
    cat > "$DEB_DIR/DEBIAN/control" << EOF
Package: paprwall
Version: $VERSION
Section: graphics
Priority: optional
Architecture: amd64
Depends: python3-tk
Maintainer: riturajprofile <riturajprofile@gmail.com>
Description: Modern Desktop Wallpaper Manager with Motivational Quotes
 PaprWall brings a fresh, modern approach to wallpaper management with
 automatic rotation and quote personalization. Features include:
 - Modern GUI with large preview panel
 - 6 different quote categories
 - Auto-rotation with customizable intervals
 - History gallery with thumbnails
 - Multi-desktop environment support
EOF

    # Create desktop entry
    cat > "$DEB_DIR/usr/share/applications/paprwall.desktop" << EOF
[Desktop Entry]
Version=1.0
Name=PaprWall
Comment=Modern Desktop Wallpaper Manager with Motivational Quotes
GenericName=Wallpaper Manager
Exec=paprwall-gui
Icon=paprwall
Terminal=false
Type=Application
Categories=Graphics;Photography;Viewer;
Keywords=wallpaper;background;desktop;quotes;
StartupNotify=true
StartupWMClass=PaprWall
EOF

    # Create simple icon (text-based)
    echo "PW" > "$DEB_DIR/usr/share/pixmaps/paprwall.xpm"

    # Build package
    dpkg-deb --build "$DEB_DIR"
    if [ -f "$DEB_DIR.deb" ]; then
        mv "$DEB_DIR.deb" "paprwall_${VERSION}_amd64.deb"
        echo "✓ Created: paprwall_${VERSION}_amd64.deb"
    fi
fi

# Build .rpm package if possible
if command -v rpmbuild &> /dev/null; then
    echo "Building .rpm package..."

    RPM_ROOT="build/rpm"
    mkdir -p "$RPM_ROOT"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

    # Create spec file
    cat > "$RPM_ROOT/SPECS/paprwall.spec" << EOF
Name:           paprwall
Version:        $VERSION
Release:        1%{?dist}
Summary:        Modern Desktop Wallpaper Manager with Motivational Quotes
License:        MIT
URL:            https://github.com/riturajprofile/paprwall
Source0:        paprwall-$VERSION.tar.gz

BuildArch:      x86_64
Requires:       python3-tkinter

%description
PaprWall brings a fresh, modern approach to wallpaper management with
automatic rotation and quote personalization.

%install
mkdir -p %{buildroot}/usr/local/bin
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/pixmaps

cp %{_builddir}/paprwall-gui %{buildroot}/usr/local/bin/
cp %{_builddir}/paprwall.desktop %{buildroot}/usr/share/applications/
echo "PW" > %{buildroot}/usr/share/pixmaps/paprwall.xpm

%files
/usr/local/bin/paprwall-gui
/usr/share/applications/paprwall.desktop
/usr/share/pixmaps/paprwall.xpm

%changelog
* $(date +"%a %b %d %Y") riturajprofile <riturajprofile@gmail.com> - $VERSION-1
- Version $VERSION release
EOF

    # Copy files to build directory
    cp "dist/paprwall-gui" "$RPM_ROOT/BUILD/"

    # Create desktop entry in build directory
    cat > "$RPM_ROOT/BUILD/paprwall.desktop" << EOF
[Desktop Entry]
Version=1.0
Name=PaprWall
Comment=Modern Desktop Wallpaper Manager with Motivational Quotes
GenericName=Wallpaper Manager
Exec=paprwall-gui
Icon=paprwall
Terminal=false
Type=Application
Categories=Graphics;Photography;Viewer;
Keywords=wallpaper;background;desktop;quotes;
StartupNotify=true
StartupWMClass=PaprWall
EOF

    # Build RPM
    rpmbuild --define "_topdir $(pwd)/$RPM_ROOT" -bb "$RPM_ROOT/SPECS/paprwall.spec"

    # Find and copy the built RPM
    if find "$RPM_ROOT/RPMS" -name "*.rpm" -type f | head -1 | xargs -I {} cp {} "paprwall-${VERSION}-1.x86_64.rpm" 2>/dev/null; then
        echo "✓ Created: paprwall-${VERSION}-1.x86_64.rpm"
    fi
fi

# Display build summary
echo
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo
echo "Version: $VERSION"
echo "Architecture: $(uname -m)"
echo
echo "Files created:"
echo "  📁 $RELEASE_DIR/               - Release directory"
echo "  📦 $ARCHIVE_NAME               - Distribution package"
echo "  🔒 $ARCHIVE_NAME.sha256        - Package checksum"
echo "  ⚡ dist/paprwall-gui           - Standalone executable"
echo "  🔒 paprwall-gui.sha256         - Executable checksum"

# Show package files if they exist
[ -f "paprwall_${VERSION}_amd64.deb" ] && echo "  📦 paprwall_${VERSION}_amd64.deb       - Debian package"
[ -f "paprwall-${VERSION}-1.x86_64.rpm" ] && echo "  📦 paprwall-${VERSION}-1.x86_64.rpm    - RPM package"

echo

# Get file sizes
echo "File sizes:"
ls -lh "dist/paprwall-gui" | awk '{print "  Executable: " $5}'
ls -lh "$ARCHIVE_NAME" | awk '{print "  Package: " $5}'

echo
echo "🎉 Ready for distribution!"
echo
echo "To test the build:"
echo "  1. cd $RELEASE_DIR/"
echo "  2. ./paprwall-gui"
echo
echo "To install system-wide:"
echo "  1. cd $RELEASE_DIR/"
echo "  2. ./install.sh"
echo
echo "Package installation:"
if [ -f "paprwall_${VERSION}_amd64.deb" ]; then
    echo "  Debian/Ubuntu: sudo dpkg -i paprwall_${VERSION}_amd64.deb"
fi
if [ -f "paprwall-${VERSION}-1.x86_64.rpm" ]; then
    echo "  Fedora/RHEL: sudo dnf install paprwall-${VERSION}-1.x86_64.rpm"
fi
