# Paprwall 🖼️

🎨 **Minimal wallpaper manager for Linux & Windows** – Beautiful random images from **Picsum** with GUI & CLI!

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows-lightgrey.svg)](https://www.linux.org/)

> **Ultra-simple. No API keys. No headaches. Just beautiful random wallpapers!**
>
> ✨ **Download ready-to-use binaries** for Linux & Windows - no Python required!

---

## ✨ Features

- 🌐 **Picsum Integration** – High-quality random images (1920×1080)
- 🔄 **Auto-Rotation** – Fetch and set new wallpaper every 90 minutes
- 🖼️ **GUI & CLI** – Both graphical and command-line interfaces
- 📦 **Standalone Binaries** – Download and run, no Python needed
- 🖥️ **Cross-Platform** – Linux, Windows (macOS builds available)
- 🪶 **Lightweight** – Minimal dependencies, fast startup
- 🔄 **History Navigation** – Browse and reuse previous wallpapers
- 🖥️ **Desktop Support** – GNOME, KDE Plasma, XFCE, MATE, Cinnamon, LXDE/LXQt

---

## 📦 Installation

### Option 1: Download Binaries (Recommended)

**No Python required!** Just download and run.

#### Linux:
```bash
# Download latest release
curl -L -o paprwall https://github.com/riturajprofile/paprwall/releases/latest/download/paprwall-linux-amd64
curl -L -o paprwall-gui https://github.com/riturajprofile/paprwall/releases/latest/download/paprwall-gui-linux-amd64

# Make executable
chmod +x paprwall paprwall-gui

# Move to PATH
sudo mv paprwall paprwall-gui /usr/local/bin/

# Run
paprwall-gui
```

Or install DEB package:
```bash
curl -L -O https://github.com/riturajprofile/paprwall/releases/latest/download/paprwall_1.1.1_amd64.deb
sudo dpkg -i paprwall_1.1.1_amd64.deb
```

#### Windows:
1. Download from [Releases](https://github.com/riturajprofile/paprwall/releases/latest):
   - `paprwall-windows-amd64.exe` (CLI)
   - `paprwall-gui-windows-amd64.exe` (GUI)
2. Double-click `paprwall-gui-windows-amd64.exe` to run
3. Or add to PATH for command-line use

### Option 2: One-Line Installer (Linux)

Automatically downloads and installs both CLI and GUI:
```bash
curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install-single.sh | sh
```

### Option 3: Install from Source

```bash
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall
./install.sh
```

---

## 💻 Usage

### GUI (Graphical Interface)

```bash
paprwall-gui
```

Or launch from CLI:
```bash
paprwall --gui
```

**The GUI lets you:**
- 🖼️ **Preview wallpapers** before setting them
- 🌐 **Fetch from URL** (defaults to Picsum random images)
- 📁 **Browse local files** and set your own images
- 📜 **View history** with clickable thumbnails
- ⚡ **One-click wallpaper changes**

![GUI Screenshot](docs/screenshot-gui.png)

### CLI (Command Line)

```bash
# Fetch and set new wallpaper
paprwall --fetch

# Navigate through wallpapers
paprwall --next
paprwall --prev

# Show current wallpaper info
paprwall --current

# Set specific image
paprwall --set /path/to/image.jpg

# Service management
paprwall --start
paprwall --stop
paprwall --status
```

### Auto-Rotation Service (Linux)

Automatically change wallpapers every 90 minutes:

```bash
# Enable and start service
systemctl --user enable paprwall
systemctl --user start paprwall

# Check status
systemctl --user status paprwall

# Stop service
systemctl --user stop paprwall
```

---

## ⚙️ Configuration

Configuration files are stored in `~/.config/paprwall/`

### Change Rotation Interval

Edit `~/.config/paprwall/preferences.json`:
```json
{
  "rotation_interval_minutes": 90,
  "images_per_day": 1,
  "auto_delete_old": true,
  "keep_days": 7
}
```

Change `90` to any number of minutes you want between wallpaper changes.

### Attribution Overlay (Optional)

Edit `~/.config/paprwall/attribution.json`:
```json
{
  "overlay_enabled": true,
  "position": "bottom-right",
  "opacity": 0.7
}
```

Set `overlay_enabled` to `false` to disable the photographer credit overlay.

---

## 🗂️ File Structure

```
~/.config/paprwall/          # Configuration
├── preferences.json         # Rotation interval, cleanup settings
└── attribution.json         # Overlay settings

~/.local/share/paprwall/     # Data
├── images/                  # Downloaded wallpapers (organized by date)
│   └── 2025-11-04/
│       └── picsum_*.jpg
└── logs/                    # Application logs
    └── app.log
```

---

## 🛠️ Desktop Environment Support

Paprwall automatically detects your DE and uses the appropriate command:

- **GNOME / Ubuntu** – `gsettings` (usually pre-installed)
- **KDE Plasma** – `qdbus`
- **XFCE** – `xfconf-query`
- **MATE / Cinnamon** – `gsettings`
- **Fallback** – `feh` or `nitrogen`

**If wallpapers don't change:**
```bash
# Install the tool for your desktop environment
sudo apt install gsettings      # GNOME/Ubuntu/MATE
sudo apt install qdbus-qt5      # KDE
sudo apt install xfconf          # XFCE
sudo apt install feh            # Universal fallback
```

---

## 🔨 Building from Source

### Build Binaries Locally

```bash
# Install dependencies
pip install pyinstaller

# Build both CLI and GUI
./build_gui.sh

# Binaries will be in dist/
./dist/paprwall --help
./dist/paprwall-gui
```

### Build Python Package

```bash
python -m pip install --upgrade pip build
python -m build
pip install dist/paprwall-*.whl
```

---

## 🐛 Troubleshooting

### Wallpaper not changing

Check desktop environment:
```bash
echo $XDG_CURRENT_DESKTOP
echo $DESKTOP_SESSION
```

Install the appropriate tool (see Desktop Environment Support section above).

### Check logs

```bash
tail -f ~/.local/share/paprwall/logs/app.log
```

### GUI not launching

**On Linux:**
```bash
# Make sure Tkinter is installed
sudo apt install python3-tk      # Ubuntu/Debian
sudo dnf install python3-tkinter # Fedora
sudo pacman -S tk                # Arch

# Or use the standalone binary (no Tkinter needed)
./paprwall-gui-linux-amd64
```

**On Windows:**
- Download the `.exe` binary (Tkinter is bundled)
- Or install Python 3.8+ with Tkinter enabled

---

## 📄 License

**CC BY-NC 4.0** (Creative Commons Attribution-NonCommercial 4.0 International)

✅ **Allowed:**
- ✅ Personal use
- ✅ Modification
- ✅ Distribution (non-commercial)

❌ **Not Allowed:**
- ❌ Commercial use
- ❌ Selling this software

**Attribution Required:** Must credit riturajprofile

See [LICENSE](LICENSE) for full details.

---

## 🤝 Contributing

Contributions welcome! This is a non-commercial open-source project.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 🙏 Credits

- **Image Source**: [Picsum Photos](https://picsum.photos) - Free random image service
- **Creator**: riturajprofile

---

## 📞 Support

- **Issues**: https://github.com/riturajprofile/paprwall/issues
- **Discussions**: https://github.com/riturajprofile/paprwall/discussions

---

**Made with ❤️ by riturajprofile**
