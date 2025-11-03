# Installation Guide

## Prerequisites

### System Requirements
- Linux-based operating system
- Python 3.8 or higher
- GTK 3.0 (for GUI)
- One of the supported desktop environments:
  - GNOME / Ubuntu
  - KDE Plasma
  - XFCE
  - MATE
  - Cinnamon
  - LXDE / LXQt

## Installation Methods

### 1. Install from PyPI (Easiest)

```bash
pip install riturajprofile-wallpaper
```

### 2. Install from Source

```bash
# Clone the repository
git clone https://github.com/riturajprofile/wallpaper-app.git
cd wallpaper-app

# Install
pip install .
```

### 3. Install in Development Mode

```bash
# Clone the repository
git clone https://github.com/riturajprofile/wallpaper-app.git
cd wallpaper-app

# Install in editable mode
pip install -e .
```

## System Dependencies

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-3.0 \
    python3-dev \
    libcairo2-dev \
    pkg-config
```

### Fedora
```bash
sudo dnf install -y \
    python3-gobject \
    gtk3 \
    cairo-devel \
    pkg-config \
    python3-devel
```

### Arch Linux
```bash
sudo pacman -S \
    python-gobject \
    gtk3 \
    cairo \
    pkgconf
```

## Verify Installation

```bash
# Check version
riturajprofile-wallpaper --version

# Test CLI
riturajprofile-wallpaper --help

# Launch GUI
riturajprofile-wallpaper-gui
```

## First Run

1. **Launch the application:**
   ```bash
   riturajprofile-wallpaper-gui
   ```

2. **Fetch your first wallpapers:**
   ```bash
   riturajprofile-wallpaper --fetch
   ```

3. **Check enabled sources:**
   ```bash
   riturajprofile-wallpaper --sources
   ```

## Optional: Add Custom API Keys

For better rate limits and reliability, add your own API keys:

1. Get free API keys from:
   - Pixabay: https://pixabay.com/api/docs/
   - Unsplash: https://unsplash.com/developers
   - Pexels: https://www.pexels.com/api/

2. Add them via GUI:
   - Settings → Sources → Click source → Enter key

## Optional: Enable Auto-Start

```bash
# Copy service file
mkdir -p ~/.config/systemd/user
cp systemd/riturajprofile-wallpaper.service ~/.config/systemd/user/

# Enable service
systemctl --user enable riturajprofile-wallpaper
systemctl --user start riturajprofile-wallpaper
```

## Troubleshooting

### "No module named 'gi'"
```bash
# Install PyGObject
pip install PyGObject

# Or install system package
sudo apt-get install python3-gi  # Ubuntu/Debian
```

### "Failed to set wallpaper"
```bash
# Check your desktop environment
echo $XDG_CURRENT_DESKTOP

# Check logs
cat ~/.local/share/riturajprofile-wallpaper/logs/app.log
```

### Permission Issues
```bash
# Fix permissions
chmod 755 ~/.config/riturajprofile-wallpaper
chmod 755 ~/.local/share/riturajprofile-wallpaper
```
