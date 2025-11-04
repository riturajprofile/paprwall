# Paprwall Installation Guide

This guide covers all installation methods for Paprwall wallpaper manager.

## Table of Contents

1. [Quick Install (Recommended)](#quick-install-recommended)
2. [Manual Installation](#manual-installation)
3. [Development Installation](#development-installation)
4. [PyPI Installation](#pypi-installation)
5. [System Requirements](#system-requirements)
6. [Post-Installation](#post-installation)
7. [Troubleshooting](#troubleshooting)

---

## Quick Install (Recommended)

### One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | bash
```

Or download and inspect first:

```bash
curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh -o install.sh
chmod +x install.sh
./install.sh
```

This script will:
- ✅ Detect your package manager (apt/dnf/pacman/zypper)
- ✅ Install system dependencies (python3-venv, python3-tk)
- ✅ Create virtual environment at `~/.paprwall/.venv`
- ✅ Install paprwall and dependencies
- ✅ Create command wrappers in `~/.local/bin`
- ✅ Enable auto-start service

---

## Manual Installation

### Step 1: Install System Dependencies

**Debian/Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-tk git curl
```

**Fedora/RHEL:**
```bash
sudo dnf install -y python3 python3-venv python3-tkinter git curl
```

**Arch Linux:**
```bash
sudo pacman -Sy python tk git curl
```

**openSUSE:**
```bash
sudo zypper install -y python3 python3-venv python3-tk git curl
```

### Step 2: Clone Repository

```bash
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall
```

### Step 3: Create Virtual Environment

```bash
python3 -m venv ~/.paprwall/.venv
source ~/.paprwall/.venv/bin/activate
```

### Step 4: Install Package

```bash
pip install --upgrade pip
pip install -e .
```

### Step 5: Create Command Wrappers

```bash
mkdir -p ~/.local/bin

cat > ~/.local/bin/paprwall << 'EOF'
#!/bin/bash
source "$HOME/.paprwall/.venv/bin/activate"
exec python -m paprwall.cli "$@"
EOF

cat > ~/.local/bin/wallpaper-manager << 'EOF'
#!/bin/bash
source "$HOME/.paprwall/.venv/bin/activate"
exec python -m paprwall.wallpaper_cli "$@"
EOF

cat > ~/.local/bin/wallpaper-gui << 'EOF'
#!/bin/bash
source "$HOME/.paprwall/.venv/bin/activate"
exec python -m paprwall.gui.wallpaper_manager_gui "$@"
EOF

chmod +x ~/.local/bin/{paprwall,wallpaper-manager,wallpaper-gui}
```

### Step 6: Add to PATH (if needed)

Add this to your `~/.bashrc` or `~/.zshrc`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

---

## Development Installation

For contributing or testing:

```bash
# Clone repository
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall

# Run the dev setup script
./setup_venv.sh

# Activate virtual environment
source .venv/bin/activate

# Now you can run directly:
paprwall --help
wallpaper-gui
```

The dev setup creates a `.venv` folder in the project directory with an editable install.

---

## PyPI Installation

*Coming soon - once published to PyPI:*

```bash
# System-wide (not recommended due to tkinter)
pip install paprwall

# With pipx (for CLI only, GUI may not work)
pipx install paprwall
```

**Note:** When installing via pip/pipx, tkinter might not be available. Use the virtual environment method for GUI support.

---

## System Requirements

### Minimum Requirements

- **OS:** Linux (any distribution)
- **Python:** 3.8 or higher
- **RAM:** 256 MB
- **Disk:** 100 MB for app + storage for downloaded wallpapers

### Desktop Environment

One of the following:
- GNOME / Ubuntu (with `gsettings`)
- KDE Plasma (with `qdbus`)
- XFCE (with `xfconf-query`)
- MATE / Cinnamon / LXDE / LXQt
- Fallback: `feh` or `nitrogen`

### Python Packages (auto-installed)

- `requests>=2.28.0` - API communication
- `Pillow>=10.0.0` - Image processing
- `APScheduler>=3.10.0` - Background scheduling
- `tkinter` - GUI (system package)

---

## Post-Installation

### 1. Verify Installation

```bash
paprwall --help
wallpaper-manager --help
wallpaper-gui  # Should launch GUI
```

### 2. Set Up API Keys (Optional)

Create `~/.config/paprwall/api_keys.json`:

```json
{
  "pixabay": {
    "api_key": "your_pixabay_key"
  },
  "unsplash": {
    "access_key": "your_unsplash_key"
  },
  "pexels": {
    "api_key": "your_pexels_key"
  }
}
```

Get free keys:
- **Pixabay:** https://pixabay.com/api/docs/
- **Unsplash:** https://unsplash.com/developers
- **Pexels:** https://www.pexels.com/api/

### 3. Test API Connections

```bash
paprwall --test pixabay
paprwall --test unsplash
paprwall --test pexels
```

### 4. Fetch First Wallpaper

```bash
paprwall --fetch
```

### 5. Enable Auto-Start (Optional)

```bash
paprwall --enable-service
```

This makes paprwall start automatically on boot.

---

## Troubleshooting

### "No module named 'tkinter'"

**Solution 1: Install tkinter system package**

```bash
# Debian/Ubuntu
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk

# openSUSE
sudo zypper install python3-tk
```

**Solution 2: Use venv instead of pipx**

If you installed with pipx and GUI doesn't work, uninstall and use the install script:

```bash
pipx uninstall paprwall
curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | bash
```

### "Command not found: paprwall"

Ensure `~/.local/bin` is in your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### "API key not found"

Use default keys temporarily, or set up your own:

```bash
mkdir -p ~/.config/paprwall
nano ~/.config/paprwall/api_keys.json
```

### "Permission denied" on install.sh

Make it executable:

```bash
chmod +x install.sh
./install.sh
```

### Wallpaper not changing

Check desktop environment detection:

```bash
echo $XDG_CURRENT_DESKTOP
echo $DESKTOP_SESSION
```

Install the appropriate tool:
- GNOME: Already has `gsettings`
- KDE: `sudo apt install qdbus-qt5` (or `qt5-qttools` on Arch)
- XFCE: Already has `xfconf-query`
- Other: `sudo apt install feh` or `nitrogen`

### Virtual environment activation issues

If activation fails:

```bash
# Remove and recreate
rm -rf ~/.paprwall/.venv
python3 -m venv ~/.paprwall/.venv
source ~/.paprwall/.venv/bin/activate
pip install paprwall
```

---

## Uninstallation

To completely remove paprwall:

```bash
# Stop service
systemctl --user stop paprwall
systemctl --user disable paprwall

# Remove files
rm -rf ~/.paprwall
rm -rf ~/.config/paprwall
rm -rf ~/.local/share/paprwall
rm ~/.local/bin/{paprwall,wallpaper-manager,wallpaper-gui}
rm ~/.config/systemd/user/paprwall.service

# Reload systemd
systemctl --user daemon-reload
```

Or use the uninstall script:

```bash
./uninstall.sh
```

---

## Updates

### Update Installed Version

```bash
source ~/.paprwall/.venv/bin/activate
pip install --upgrade "git+https://github.com/riturajprofile/paprwall.git"
```

### Update Development Version

```bash
cd paprwall
git pull
source .venv/bin/activate
pip install -e . --upgrade
```

---

## Support

- **Issues:** https://github.com/riturajprofile/paprwall/issues
- **Discussions:** https://github.com/riturajprofile/paprwall/discussions
- **Documentation:** https://github.com/riturajprofile/paprwall

---

**Happy Wallpapering! 🖼️**
