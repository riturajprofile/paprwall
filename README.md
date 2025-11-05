# PaprWall 🎨

Modern desktop wallpaper manager with inspirational quotes and one-click apply.

[![Version](https://img.shields.io/badge/version-1.1.1-blue.svg)](https://github.com/riturajprofile/paprwall/releases)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC--BY--NC%204.0-blue.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey.svg)](https://github.com/riturajprofile/paprwall)

Beautiful wallpapers with inspirational quotes. Auto-rotation, 6 quote categories, and a clean dark UI. Robust cross-desktop wallpaper setting with detailed debug logs.

## ✨ Features

- 🎨 Modern dark UI with large preview
- 💭 6 quote categories: Motivational, Math, Science, Famous, Tech, Philosophy
- 🔄 Auto-rotation with live countdown; interval changes take effect immediately
- ✅ “Applied” indicator shows when the preview matches the current wallpaper
- ♻️ Fallback to previously applied wallpaper if a fetch fails
- 📜 History gallery with quick “Set” from any past wallpaper
- 🖥️ Multi-desktop support: GNOME, KDE, XFCE, Cinnamon, MATE, LXQt; feh fallback
- 🧰 Detailed debug logs for wallpaper setting (per-desktop methods and fallbacks)
- 🌐 Random images from multiple APIs + 📁 use your own images with quotes

## 🚀 Installation

### PyPI (easiest)
```bash
pip install paprwall
paprwall-gui
```

### Linux / Windows binaries
Download from [Releases](https://github.com/riturajprofile/paprwall/releases/latest):
- Linux: `.tar.gz`, `.deb`, `.rpm`, or AppImage
- Windows: `.zip` with executable

### Requirements
- Python 3.9+ (PyPI install only)
- Linux: `sudo apt install python3-tk` (Ubuntu/Debian)
- Windows: Included with Python

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
5. **Auto-Rotate** - Enable timer for automatic changes
6. **History** - Browse and reuse previous wallpapers

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


---

⭐ Star this repo if you like it! • Made with ❤️ by [riturajprofile](https://github.com/riturajprofile)
