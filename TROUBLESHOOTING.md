# PaprWall Troubleshooting Guide

This guide helps you resolve common issues with PaprWall, especially wallpaper setting problems on Ubuntu/Linux.

## Table of Contents
- [Wallpaper Not Setting on Ubuntu/Linux](#wallpaper-not-setting-on-ubuntulinux)
- [Network/API Connection Issues](#networkapi-connection-issues)
- [Font Issues](#font-issues)
- [GUI Won't Start](#gui-wont-start)
- [Permission Issues](#permission-issues)
- [General Debugging](#general-debugging)

---

## Wallpaper Not Setting on Ubuntu/Linux

### Problem
The app says "Wallpaper set successfully!" but your desktop wallpaper doesn't change.

### Solution Steps

#### 1. Check Your Desktop Environment

First, identify which desktop environment you're using:

```bash
echo $XDG_CURRENT_DESKTOP
```

**Supported Desktop Environments:**
- GNOME (Ubuntu default)
- KDE Plasma
- XFCE
- Cinnamon
- MATE
- LXQt

#### 2. Install Required Tools

Based on your desktop environment, install the necessary tools:

**For GNOME/Ubuntu (most common):**
```bash
# Usually pre-installed, but verify:
which gsettings
```

**For XFCE:**
```bash
sudo apt install xfce4-settings
```

**For KDE:**
```bash
sudo apt install kde-runtime
```

**For Any Desktop (Universal Fallback):**
```bash
# Install feh (lightweight wallpaper setter)
sudo apt install feh

# OR install nitrogen (GUI-based alternative)
sudo apt install nitrogen
```

#### 3. Test Wallpaper Setting Manually

**For GNOME/Ubuntu:**
```bash
# Get an absolute path to an image
IMAGE_PATH="/home/yourusername/.local/share/paprwall/wallpapers/wallpaper_123456.jpg"

# Set wallpaper (replace with your actual path)
gsettings set org.gnome.desktop.background picture-uri "file://$IMAGE_PATH"
gsettings set org.gnome.desktop.background picture-uri-dark "file://$IMAGE_PATH"

# Verify it's set
gsettings get org.gnome.desktop.background picture-uri
```

**For XFCE:**
```bash
xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s "/path/to/image.jpg"
```

**Using feh (Universal):**
```bash
feh --bg-scale "/path/to/image.jpg"
```

#### 4. Check Debug Output

When running `paprwall-gui`, watch for debug messages:

```bash
paprwall-gui
```

Look for lines like:
- `[DEBUG] Desktop environment: gnome` - Shows detected environment
- `[DEBUG] Trying GNOME gsettings...` - Shows which method is being tried
- `[DEBUG] GNOME wallpaper set successfully` - Indicates success
- `[ERROR] All wallpaper setting methods failed` - All methods failed

#### 5. Common GNOME Issues

**Issue: Wallpaper reverts on theme change**

Solution: Set both light and dark mode wallpapers:
```bash
IMAGE_PATH="/full/path/to/wallpaper.jpg"
gsettings set org.gnome.desktop.background picture-uri "file://$IMAGE_PATH"
gsettings set org.gnome.desktop.background picture-uri-dark "file://$IMAGE_PATH"
```

**Issue: Permissions denied**

Solution: Check file permissions:
```bash
chmod 644 ~/.local/share/paprwall/wallpapers/*.jpg
```

**Issue: Wallpaper path not absolute**

The app now automatically converts to absolute paths, but verify:
```bash
realpath ~/.local/share/paprwall/wallpapers/wallpaper_*.jpg
```

#### 6. Flatpak/Snap Specific Issues

If you installed PaprWall via Flatpak or Snap, it may have limited access:

**For Snap:**
```bash
# Grant additional permissions
snap connect paprwall:gsettings
snap connect paprwall:home
```

**For Flatpak:**
```bash
# Grant filesystem access
flatpak override --user --filesystem=home com.github.rituraj.paprwall
```

---

## Network/API Connection Issues

### Problem
You see errors like:
```
Quote fetch attempt failed: Failed to resolve 'api.quotable.io'
```

### Solutions

#### 1. Check Internet Connection
```bash
ping -c 3 google.com
```

#### 2. Check DNS Resolution
```bash
nslookup api.quotable.io
```

If DNS fails:
```bash
# Try using Google DNS
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf.d/base
sudo systemctl restart systemd-resolved
```

#### 3. Use Fallback Quotes
The app automatically uses fallback quotes when the API is unreachable. This is normal behavior and doesn't affect functionality.

---

## Font Issues

### Problem
You see messages like:
```
Font load failed: arial.ttf (cannot open resource)
Loaded font: /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
```

### Solution

This is **not an error** - the app tries Arial first, then falls back to DejaVu fonts which are standard on Ubuntu.

If you want to install more fonts:
```bash
# Install Microsoft fonts (includes Arial)
sudo apt install ttf-mscorefonts-installer

# Update font cache
sudo fc-cache -f -v
```

---

## GUI Won't Start

### Problem
Running `paprwall-gui` shows an error or does nothing.

### Solutions

#### 1. Install Tkinter
```bash
# For Ubuntu/Debian
sudo apt install python3-tk

# For Fedora
sudo dnf install python3-tkinter

# For Arch
sudo pacman -S tk
```

#### 2. Check Python Version
```bash
python3 --version
```

PaprWall requires Python 3.8 or higher.

#### 3. Reinstall PaprWall
```bash
pip uninstall paprwall
pip install --upgrade paprwall
```

#### 4. Check Display Environment
```bash
echo $DISPLAY
```

If empty, you're not in a graphical session.

---

## Permission Issues

### Problem
Cannot save wallpapers or history.

### Solution

```bash
# Fix directory permissions
mkdir -p ~/.local/share/paprwall/wallpapers
chmod 755 ~/.local/share/paprwall
chmod 755 ~/.local/share/paprwall/wallpapers

# Fix file permissions
chmod 644 ~/.local/share/paprwall/wallpapers/*.jpg 2>/dev/null
chmod 644 ~/.local/share/paprwall/*.json 2>/dev/null
```

---

## General Debugging

### Enable Verbose Debug Mode

The latest version includes debug output by default. When running the app, you'll see detailed logs:

```bash
paprwall-gui 2>&1 | tee paprwall-debug.log
```

This saves all output to `paprwall-debug.log` for analysis.

### Check Wallpaper Files

List saved wallpapers:
```bash
ls -lh ~/.local/share/paprwall/wallpapers/
```

View the most recent wallpaper:
```bash
eog ~/.local/share/paprwall/wallpapers/wallpaper_*.jpg
# or
feh ~/.local/share/paprwall/wallpapers/wallpaper_*.jpg
```

### Manual Wallpaper Setting Test

Use this Python script to test wallpaper setting:

```python
#!/usr/bin/env python3
import subprocess
import os

image_path = os.path.expanduser("~/.local/share/paprwall/wallpapers/wallpaper_latest.jpg")

# Test GNOME method
try:
    result = subprocess.run([
        'gsettings', 'set', 'org.gnome.desktop.background',
        'picture-uri', f'file://{image_path}'
    ], capture_output=True, text=True)
    print(f"GNOME Result: {result.returncode}")
    print(f"Output: {result.stdout}")
    print(f"Error: {result.stderr}")
except Exception as e:
    print(f"Failed: {e}")
```

Save as `test_wallpaper.py` and run:
```bash
python3 test_wallpaper.py
```

---

## Still Having Issues?

### 1. Collect System Information

```bash
# System info
uname -a
lsb_release -a
echo $XDG_CURRENT_DESKTOP
echo $DESKTOP_SESSION

# Python info
python3 --version
pip show paprwall

# Check installed tools
which gsettings
which feh
which nitrogen
```

### 2. Report an Issue

Create an issue on GitHub with:
- Output from the commands above
- Debug log from running `paprwall-gui`
- Your desktop environment
- Screenshots if relevant

**GitHub Issues:** https://github.com/riturajprofile/paprwall/issues

### 3. Quick Workaround

If wallpaper setting fails, you can manually set wallpapers:

1. Find your wallpaper files:
   ```bash
   cd ~/.local/share/paprwall/wallpapers
   ```

2. View them:
   ```bash
   eog wallpaper_*.jpg
   ```

3. Right-click on the image you like → "Set as Wallpaper"

---

## Advanced Configuration

### Custom Wallpaper Directory

If you want to use a different directory:

```bash
# Set environment variable
export PAPRWALL_DATA_DIR="$HOME/Pictures/PaprWall"
paprwall-gui
```

### Run as Background Service

To automatically rotate wallpapers:

```bash
# Create systemd service
mkdir -p ~/.config/systemd/user/

cat > ~/.config/systemd/user/paprwall-rotate.service << 'EOF'
[Unit]
Description=PaprWall Auto Rotate

[Service]
ExecStart=/usr/bin/python3 -m paprwall.cli --category motivational
Restart=always
RestartSec=3600

[Install]
WantedBy=default.target
EOF

# Enable and start
systemctl --user enable paprwall-rotate.service
systemctl --user start paprwall-rotate.service
```

---

## Version Information

This troubleshooting guide is for PaprWall v1.0.3+

Check your version:
```bash
pip show paprwall | grep Version
```

Update to latest:
```bash
pip install --upgrade paprwall
```

---

**Need more help?** Visit our [GitHub Discussions](https://github.com/riturajprofile/paprwall/discussions) or [open an issue](https://github.com/riturajprofile/paprwall/issues).