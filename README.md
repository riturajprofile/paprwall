# PaprWall v2.1.0 - Service Control Improvements 🎨

## 🎯 What's New

### Simplified Service Controls
- **Single Toggle Button**: Replaced 3-button UI (Enable/Disable/Status) with one smart toggle
- **Color-Coded Status Icons**: 
  - 🟢 Running
  - 🔴 Disabled  
  - 🟡 Enabled but Stopped
  - ⚪ Not Installed
- **Smart Button**: Automatically shows "Enable Service" or "Disable Service" based on current state
- **Better UX**: At-a-glance status understanding with icons + text

### Improvements
- ✅ Proper timeout handling to prevent UI freezes
- ✅ Improved error messages for service operations
- ✅ More intuitive service management experience

## ✨ Features

- 🎨 **Modern GUI** - Clean, intuitive interface with large wallpaper preview
- 📝 **6 Quote Categories** - Motivational, Mathematics, Science, Famous, Technology, Philosophy
- 🔄 **Auto-Rotation** - Set custom intervals (5min to 24hrs) for automatic wallpaper changes
- 📜 **History Gallery** - Browse and reuse previously applied wallpapers
- 🖥️ **Multi-Desktop Support** - Works with GNOME, KDE, XFCE, MATE, Cinnamon, LXQt
- 🤖 **Background Service** - Systemd (Linux) / Startup (Windows) for persistent operation
- 🎯 **Service Toggle** - Single-button control with visual status indicators
- 💾 **Offline Support** - Access wallpaper history without internet
- 🌐 **Cross-Platform** - Linux, Windows support

## 📥 Installation

### Option 1: PyPI (Recommended)
```bash
pip install paprwall
paprwall-setup-desktop  # Creates desktop/start menu entry
paprwall-gui           # Launch
```

### Option 2: Linux Packages
- `.deb`: `sudo dpkg -i paprwall_*.deb`
- `.rpm`: `sudo dnf install paprwall_*.rpm`  
- AppImage: `chmod +x PaprWall-*.AppImage && ./PaprWall-*.AppImage`

### Option 3: Windows
1. Download `.zip` from [Releases](https://github.com/riturajprofile/paprwall/releases/latest)
2. Run `INSTALL.bat` (creates Desktop + Start Menu shortcuts)
3. Launch from Desktop or Start Menu

### Requirements
- Python 3.9+ | Linux: `sudo apt install python3-tk`

## 🧪 Quick start

1. Select a quote category
2. Click “Random” or “Refresh” to fetch
3. Preview updates with shrink‑to‑fit quote overlay (top‑right)
4. Click “Set Wallpaper” to apply
5. Toggle “Auto‑rotate” and choose an interval
6. Use “History” to re‑apply previous wallpapers

## 📖 Usage

1. **Select Quote Category** - Choose from 6 types (Motivational, Math, Science, etc.)
2. **Fetch Wallpaper** - Click "Random" or "Refresh" button
3. **Preview** - View wallpaper with embedded quote
4. **Set Wallpaper** - Apply to desktop
5. **Auto-Rotate** - Enable timer for automatic changes (continues in background!)
6. **History** - Browse and reuse previous wallpapers

### Background Service Management

**GUI Controls:**
- Open PaprWall settings
- Find "Background Service" section with status icon (🟢/🔴/🟡/⚪)
- Click the toggle button to enable/disable
- Service status updates automatically

**Command Line (Linux - systemd):**
```bash
paprwall-service install   # Install and start service
paprwall-service status    # Check status
paprwall-service uninstall # Remove service
```
Service runs in background, auto-rotation continues even after logout!

**Command Line (Windows - Startup):**
```bash
paprwall-service install   # Add to Windows Startup
paprwall-service uninstall # Remove from Startup
```
PaprWall starts automatically when you log in.

**Manual daemon mode:**
```bash
paprwall-gui --daemon      # Run in background (no window)
```

### Data locations
- **Linux**: `~/.local/share/paprwall/wallpapers/`
- **Windows**: `%APPDATA%\PaprWall\wallpapers\`



## 🔧 Troubleshooting

**GUI won't start?** Install Tkinter: `sudo apt install python3-tk` (Linux)  
**Wallpaper not changing?** Check supported desktop: GNOME, KDE, XFCE, MATE, Cinnamon, LXQt  
**Windows SmartScreen?** Click "More info" → "Run anyway"

See the docs for more:
- Installation: [paprwall/docs/installation.md](paprwall/docs/installation.md)
- Usage: [paprwall/docs/usage.md](paprwall/docs/usage.md)

## 🤝 Contributing

```bash
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall
pip install -e ".[dev]"
```

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/riturajprofile/paprwall/issues)
- **Releases**: [Latest Version](https://github.com/riturajprofile/paprwall/releases/latest)
- **PyPI**: [pypi.org/project/paprwall](https://pypi.org/project/paprwall/)

---

⭐ Star this repo if you like it! • Made with ❤️ by [riturajprofile](https://github.com/riturajprofile)
