# 📥 PaprWall Installation Guide

Complete guide for installing PaprWall on Linux and Windows using various methods.

---

## 🚀 Quick Installation

### 🐧 Linux

**Recommended: AppImage (Universal - Works on ALL Distributions)**

```bash
# Download the latest AppImage
wget https://github.com/riturajprofile/paprwall/releases/latest/download/PaprWall-x86_64.AppImage

# Make executable
chmod +x PaprWall-x86_64.AppImage

# Run!
./PaprWall-x86_64.AppImage
```

**That's it!** No installation, no dependencies, works everywhere! 🎉

### 🪟 Windows

**Recommended: Portable Executable**

1. Download `paprwall-windows-x64.zip` from [Releases](https://github.com/riturajprofile/paprwall/releases/latest)
2. Extract the ZIP file
3. Run `paprwall-gui.exe`

**Done!** First-run will offer to install to Start Menu.

---

## 📦 Installation Methods

### Method 1: AppImage (Linux - Universal) ⭐

**Best for:** All Linux users, works on any distribution

```bash
# Download
wget https://github.com/riturajprofile/paprwall/releases/latest/download/PaprWall-x86_64.AppImage

# Make executable
chmod +x PaprWall-x86_64.AppImage

# Optional: Move to permanent location
mkdir -p ~/Applications
mv PaprWall-x86_64.AppImage ~/Applications/

# Run
~/Applications/PaprWall-x86_64.AppImage
```

**Features:**
- ✅ Works on Ubuntu, Fedora, Arch, Debian, Mint, openSUSE, etc.
- ✅ No installation required
- ✅ No root/sudo needed
- ✅ Self-contained with all dependencies
- ✅ Truly portable (USB drive ready)
- ✅ First-run offers system integration

**System Integration (Optional):**

First-run will ask: "Would you like to install PaprWall to your system?"

- **Yes** → Adds to application menu, creates desktop entry
- **No** → Ask again next time
- **Cancel** → Never ask again (portable mode)

Or install manually:
```bash
./PaprWall-x86_64.AppImage --install
```

**Uninstall:**
```bash
# Remove system integration
./PaprWall-x86_64.AppImage --uninstall

# Remove AppImage file
rm ~/Applications/PaprWall-x86_64.AppImage

# Remove data (optional)
rm -rf ~/.local/share/paprwall
```

---

### Method 2: Package Managers (Linux)

**Best for:** Users who prefer system package managers

#### Debian/Ubuntu (.deb)

```bash
# Download package
wget https://github.com/riturajprofile/paprwall/releases/latest/download/paprwall_amd64.deb

# Install
sudo dpkg -i paprwall_amd64.deb
sudo apt-get install -f  # Fix dependencies if needed

# Launch
paprwall-gui
```

**Uninstall:**
```bash
sudo apt remove paprwall
```

#### Fedora/RHEL/CentOS (.rpm)

```bash
# Download package
wget https://github.com/riturajprofile/paprwall/releases/latest/download/paprwall-x86_64.rpm

# Install
sudo dnf install paprwall-x86_64.rpm  # Fedora
# or
sudo yum install paprwall-x86_64.rpm  # RHEL/CentOS

# Launch
paprwall-gui
```

**Uninstall:**
```bash
sudo dnf remove paprwall  # Fedora
sudo yum remove paprwall  # RHEL/CentOS
```

---

### Method 3: Portable Binary (Linux)

**Best for:** Users who want portable without AppImage

```bash
# Download
wget https://github.com/riturajprofile/paprwall/releases/latest/download/paprwall-linux-x64.tar.gz

# Extract
tar -xzf paprwall-linux-x64.tar.gz
cd paprwall-linux-x64

# Run
./paprwall-gui

# Optional: Install to system
./paprwall-gui --install
```

---

### Method 4: Windows Portable

**Best for:** Windows users who want quick setup

```bash
# Download from: https://github.com/riturajprofile/paprwall/releases/latest
# File: paprwall-windows-x64.zip

# Extract to permanent location:
C:\Users\YourName\Programs\PaprWall\

# Run
paprwall-gui.exe
```

**First-run prompt:**
```
Would you like to install PaprWall to your system?

• Desktop shortcut
• Start Menu entry
• Easy uninstall option

[Yes] [No] [Cancel]
```

- **Yes** → Full system integration
- **No** → Ask again next time
- **Cancel** → Stay portable forever

**Manual installation:**
```cmd
paprwall-gui.exe --install
```

**Uninstall:**
```cmd
# Via command line
paprwall-gui.exe --uninstall

# Via Start Menu
Start Menu → PaprWall → Uninstall PaprWall

# Via GUI
Settings → Uninstall PaprWall button
```

---

### Method 5: PyPI (Python Package)

**Best for:** Python developers, pip users

```bash
# Install
pip install paprwall

# Launch GUI
paprwall-gui

# Or use CLI
paprwall --help
```

**Requirements:**
- Python 3.8+
- Tkinter (install separately on Linux)

**Linux Tkinter:**
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

**Uninstall:**
```bash
pip uninstall paprwall
```

---

### Method 6: From Source

**Best for:** Developers, contributors

```bash
# Clone repository
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install in development mode
pip install -e .

# Launch
paprwall-gui
```

**For development:**
```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

---

## 🎯 First-Run Installation Behavior

### What Happens on First Launch

When you run a portable binary (AppImage, .exe, or tar.gz) for the first time:

1. **Application launches normally** - GUI opens, fully functional
2. **After 100ms** - Installation prompt appears (non-blocking)
3. **You choose** - Install now, later, or never

### Installation Prompt

```
┌─────────────────────────────────────────┐
│ Welcome to PaprWall! 🎨                 │
│                                         │
│ Would you like to install PaprWall?    │
│                                         │
│ This creates:                           │
│   • Desktop shortcut                    │
│   • Application menu entry              │
│   • Easy uninstall option               │
│                                         │
│ [Yes] [No] [Cancel]                     │
└─────────────────────────────────────────┘
```

### Your Options

| Button | What Happens | When to Choose |
|--------|--------------|----------------|
| **Yes** | Installs immediately to your system | Want quick access from menu/desktop |
| **No** | Skip for now, ask again next time | Not sure yet, testing the app |
| **Cancel** | Never ask again (portable mode) | Want to keep it portable |

### What Gets Installed

**Linux:**
```
~/.local/bin/paprwall-gui              # Executable
~/.local/share/applications/paprwall.desktop  # Menu entry
~/.local/share/icons/hicolor/256x256/apps/paprwall.png  # Icon
```

**Windows:**
```
%LOCALAPPDATA%\Programs\PaprWall\      # Installed location
Desktop\PaprWall.lnk                   # Desktop shortcut
Start Menu\PaprWall\                   # Start Menu folder
```

### Installing Later

You can always install later from the GUI:

1. Launch PaprWall
2. Look for **Settings** section
3. Click **"💾 Install to System"** button
4. Done!

Or via command line:
```bash
./PaprWall-x86_64.AppImage --install     # Linux AppImage
./paprwall-gui --install                 # Linux binary
paprwall-gui.exe --install               # Windows
```

---

## 🗑️ Uninstallation

### Complete Removal

**Linux (AppImage):**
```bash
# Remove system integration
./PaprWall-x86_64.AppImage --uninstall

# Remove AppImage
rm ~/Applications/PaprWall-x86_64.AppImage

# Remove data (optional)
rm -rf ~/.local/share/paprwall
```

**Linux (Package):**
```bash
# Debian/Ubuntu
sudo apt remove paprwall

# Fedora
sudo dnf remove paprwall

# Remove data (optional)
rm -rf ~/.local/share/paprwall
```

**Windows:**
```cmd
# Via executable
paprwall-gui.exe --uninstall

# Via Start Menu
Start Menu → PaprWall → Uninstall PaprWall

# Manual removal
rmdir /s "%LOCALAPPDATA%\Programs\PaprWall"
rmdir /s "%APPDATA%\PaprWall"  # Data directory
```

### GUI Uninstall Button

All versions include an **Uninstall** button in the GUI:

1. Launch PaprWall
2. Scroll to bottom of left panel
3. Click **"🗑️ Uninstall PaprWall"** button
4. Confirm removal
5. Choose whether to keep data

---

## 🔧 Troubleshooting

### Linux Issues

**Problem: AppImage won't run**

```bash
# Solution: Install FUSE
sudo apt install fuse libfuse2        # Ubuntu/Debian
sudo dnf install fuse fuse-libs       # Fedora
sudo pacman -S fuse2                  # Arch

# Or extract and run
./PaprWall-x86_64.AppImage --appimage-extract
./squashfs-root/AppRun
```

**Problem: GUI doesn't launch (missing tkinter)**

```bash
# Install Tkinter
sudo apt install python3-tk           # Ubuntu/Debian
sudo dnf install python3-tkinter      # Fedora
sudo pacman -S tk                     # Arch
```

**Problem: Wallpaper doesn't change**

```bash
# Check your desktop environment
echo $XDG_CURRENT_DESKTOP

# Supported: GNOME, KDE, XFCE, MATE, Cinnamon, etc.
```

**Problem: No menu entry after install**

```bash
# Update desktop database
update-desktop-database ~/.local/share/applications
gtk-update-icon-cache ~/.local/share/icons/hicolor

# Or logout and login again
```

### Windows Issues

**Problem: Windows SmartScreen warning**

1. Click "More info"
2. Click "Run anyway"
3. Normal for unsigned executables

**Problem: Python not found (PyPI install)**

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Check "Add Python to PATH" during installation
3. Restart Command Prompt

**Problem: Desktop icon not created**

1. Wait 10 seconds (system needs to refresh)
2. Restart File Explorer
3. Try installing again from Settings
4. Check Desktop manually

---

## 🆚 Installation Comparison

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **AppImage** | All Linux users | Universal, portable, no install | Larger file size |
| **.deb/.rpm** | Package manager users | System integrated | Distro-specific |
| **Windows .exe** | Windows users | Native, easy | Windows only |
| **PyPI** | Python developers | Easy updates via pip | Needs Python |
| **Source** | Contributors | Latest code, editable | Requires dev setup |

---

## 📋 System Requirements

### Linux
- **OS**: Any distribution (AppImage), or specific distro for packages
- **Desktop**: GNOME, KDE, XFCE, MATE, Cinnamon, LXQt, etc.
- **Python**: 3.8+ (for PyPI/source install)
- **Display**: 720p or higher recommended

### Windows
- **OS**: Windows 10 (1809+) or Windows 11
- **Python**: 3.8+ (for PyPI/source install only)
- **Display**: 720p or higher recommended

---

## 📞 Getting Help

- **Documentation**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/riturajprofile/paprwall/issues)
- **Discussions**: [GitHub Discussions](https://github.com/riturajprofile/paprwall/discussions)

---

**Ready to install? Choose your method above and get started! 🚀**

*Last Updated: December 2024 | PaprWall v1.0.3*