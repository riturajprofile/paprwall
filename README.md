# PaprWall 🎨

**Modern Desktop Wallpaper Manager with Motivational Quotes**

[![Version](https://img.shields.io/badge/version-1.0.3-blue.svg)](https://github.com/riturajprofile/paprwall/releases)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC--BY--NC%204.0-blue.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey.svg)](https://github.com/riturajprofile/paprwall)

Transform your desktop with stunning wallpapers embedded with inspirational quotes. PaprWall brings a fresh, modern approach to wallpaper management with automatic rotation and quote personalization.

![PaprWall Screenshot](https://via.placeholder.com/800x450/0f1419/3b82f6?text=PaprWall+GUI)

## ✨ Features

### 🎨 Modern GUI Interface
- **Full-screen responsive design** - Maximized by default for optimal viewing
- **480px large preview panel** - See wallpapers in stunning detail
- **Dark theme** - Professional, eye-friendly interface
- **Web-inspired layout** - Clean, intuitive controls

### 💭 Quote System
- **6 Quote Categories**:
  - 🚀 Motivational
  - 🔢 Mathematics
  - 🔬 Science
  - 👤 Famous People
  - 💻 Technology
  - 🧠 Philosophy
- **Embedded quotes** - Permanently placed on wallpaper images
- **Top-right positioning** - Non-intrusive, beautiful overlay
- **Custom quotes** - Add your own inspirational text
- **API-powered** - Fresh quotes from quotable.io & zenquotes.io

### 🔄 Auto-Rotation
- **Smart rotation** - 60-minute default interval (customizable)
- **Real-time countdown** - MM:SS timer display
- **Auto-fetch on startup** - 2 images loaded automatically
- **Background threading** - Non-blocking, smooth operation

### 📜 History Gallery
- **Large thumbnails** - 120x75px preview cards
- **Preview button** - View without setting
- **Set button** - Apply directly from history
- **Easy browsing** - Horizontal scrollable gallery

## 🚀 Quick Start

### Installation

#### 🐧 Linux (Recommended: AppImage)

```bash
# Download universal AppImage (works on ALL distros)
wget https://github.com/riturajprofile/paprwall/releases/latest/download/PaprWall-x86_64.AppImage

# Make executable and run
chmod +x PaprWall-x86_64.AppImage
./PaprWall-x86_64.AppImage
```

**Or use package manager:**
```bash
# Debian/Ubuntu
wget https://github.com/riturajprofile/paprwall/releases/latest/download/paprwall_amd64.deb
sudo dpkg -i paprwall_amd64.deb

# Fedora/RHEL
wget https://github.com/riturajprofile/paprwall/releases/latest/download/paprwall-x86_64.rpm
sudo dnf install paprwall-x86_64.rpm
```

#### 🪟 Windows

1. Download `paprwall-windows-x64.zip` from [Releases](https://github.com/riturajprofile/paprwall/releases/latest)
2. Extract and run `paprwall-gui.exe`
3. First-run will offer system integration (optional)

#### 🐍 PyPI (Any Platform)

```bash
pip install paprwall
paprwall-gui
```

**📖 Full Installation Guide:** See [INSTALLATION.md](INSTALLATION.md) for detailed instructions, troubleshooting, and all installation methods.

### 🎯 First-Run Behavior

When you run PaprWall for the first time, it will ask if you want to install it to your system:

- **Yes** → Creates desktop shortcut and menu entry
- **No** → Ask again next time
- **Cancel** → Stay portable (never ask again)

You can also install/uninstall anytime via:
```bash
paprwall-gui --install    # Install to system
paprwall-gui --uninstall  # Remove from system
```

Or use the GUI buttons in Settings.

## 📋 Requirements

### System Requirements
- **OS**: Linux (Ubuntu 20.04+, Fedora 35+, Arch, Debian, etc.) or Windows 10/11
- **Display**: 720p or higher recommended
- **Python**: 3.8+ (only for source installation)

### Platform Support

#### 🐧 Linux Desktop Environments
- ✅ **GNOME** (Ubuntu, Fedora)
- ✅ **KDE Plasma** (Kubuntu, KDE Neon)
- ✅ **XFCE** (Xubuntu)
- ✅ **MATE** (Ubuntu MATE)
- ✅ **Cinnamon** (Linux Mint)
- ✅ **LXQt** / **LXDE**

#### 🪟 Windows
- ✅ **Windows 10** (1809+)
- ✅ **Windows 11**

### Dependencies
- **Tkinter** - GUI framework (included with Python on Windows, pre-installed on most Linux)
- **Pillow** - Image processing
- **Requests** - HTTP client

#### Linux
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

#### Windows
Tkinter is included with the official Python installer - no additional setup needed!

## 🎯 Usage

### GUI Features

#### 1. Select Quote Category
Choose from 6 different quote types using the dropdown menu:
- Motivational quotes for daily inspiration
- Math quotes for analytical minds
- Science quotes for curious learners
- Famous people's wisdom
- Technology insights
- Philosophical thoughts

#### 2. Fetch Wallpapers
- Click **"Fetch Wallpaper"** for a new random image
- Or use **"🎲 Random"** quick action button
- Auto-rotation fetches new images automatically

#### 3. Preview & Set
- Large preview shows wallpaper with embedded quote
- Click **"✓ Set Wallpaper"** to apply
- Quote is permanently embedded on the image

#### 4. Auto-Rotation
- Toggle auto-rotation on/off
- Customize interval (minutes)
- Watch countdown timer
- Manual fetch resets the timer

#### 5. Browse History
- View recent wallpapers in gallery
- **Preview** button to view without setting
- **Set** button to apply immediately
- Scrollable horizontal layout

#### 6. Local Files
- Click **"📁 Browse Local File"** to use your own images
- Quote will be embedded on local images too
- Supports JPG, PNG formats

### Keyboard Shortcuts
- `Ctrl+Q` - Quit application
- `Ctrl+R` - Fetch random wallpaper
- `Ctrl+O` - Open local file

## 🛠️ Configuration

### Data Locations

#### Linux
```bash
# Wallpapers
~/.local/share/paprwall/wallpapers/

# History
~/.local/share/paprwall/history.json

# Logs
~/.local/share/paprwall/paprwall.log
```

#### Windows
```cmd
# Wallpapers
%APPDATA%\PaprWall\wallpapers\

# History
%APPDATA%\PaprWall\history.json

# Logs
%APPDATA%\PaprWall\paprwall.log
```

## 🔧 Troubleshooting

### Linux Issues

#### Issue: GUI doesn't launch
**Solution**: Ensure Tkinter is installed
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

#### Issue: Wallpaper doesn't change
**Solution**: Check your desktop environment
```bash
# Check current desktop
echo $XDG_CURRENT_DESKTOP

# Supported: GNOME, KDE, XFCE, MATE, Cinnamon, etc.
```

#### Issue: Binary doesn't run
**Solution**: Make sure it's executable
```bash
chmod +x paprwall-gui
./paprwall-gui
```

### Windows Issues

#### Issue: Windows SmartScreen warning
**Solution**:
1. Click "More info"
2. Click "Run anyway"
3. This is normal for unsigned executables

#### Issue: Wallpaper doesn't change
**Solution**:
- Make sure you have write permissions to wallpaper directory
- Try running as normal user (not administrator)
- Check Windows Settings → Personalization → Background

#### Issue: Python not found (source install)
**Solution**:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Check "Add Python to PATH" during installation
3. Restart Command Prompt

### General Issues

#### Issue: Quote not visible
**Solution**:
- Quote is embedded top-right corner
- Try a different wallpaper with more space
- Use custom quote with shorter text

#### Issue: Images not downloading
**Solution**:
- Check internet connection
- Try different image URL
- Check firewall settings

## 🗑️ Uninstallation

**Via Command Line:**
```bash
paprwall-gui --uninstall  # Linux/Windows
pip uninstall paprwall    # If installed via pip
```

**Via GUI:**
- Click the **"🗑️ Uninstall PaprWall"** button in Settings

**Via System:**
- **Linux**: `sudo apt remove paprwall` or `sudo dnf remove paprwall`
- **Windows**: Start Menu → PaprWall → Uninstall

**📖 Full details:** See [INSTALLATION.md](INSTALLATION.md) for complete uninstallation instructions.

## �📦 Building from Source

### Build Requirements
```bash
pip install build pyinstaller
```

### Build Process

#### Linux
```bash
# Clone repository
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall

# Run build script
./build_release.sh
```

This creates:
- `release-v1.0.0/` directory with binaries
- `paprwall-v1.0.0-linux-x64.tar.gz` release package
- SHA-256 checksum file

#### Windows
```cmd
# Clone repository
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall

# Run build script
build_release_windows.bat
```

This creates:
- `release-v1.0.0\` directory with binaries
- `paprwall-v1.0.0-windows-x64.zip` release package
- SHA-256 checksum file

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall
python -m venv .venv
source .venv/bin/activate
pip install -e ".[build]"
```

### Run Tests
```bash
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Quote APIs**: [Quotable.io](https://quotable.io) and [ZenQuotes.io](https://zenquotes.io)
- **Images**: [Picsum Photos](https://picsum.photos)
- **Fonts**: DejaVu and Liberation Serif
- **Icons**: Emoji from Unicode Standard

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/riturajprofile/paprwall/issues)
- **Discussions**: [GitHub Discussions](https://github.com/riturajprofile/paprwall/discussions)
- **Email**: riturajprofile@example.com

## 🗺️ Roadmap

### v1.1.0 (Planned)
- [ ] Multi-monitor support
- [ ] Custom font selection for quotes
- [ ] Color theme customization
- [ ] Image filters (blur, brightness, contrast)
- [ ] Slideshow mode

### v1.2.0 (Planned)
- [ ] Cloud sync for favorites
- [ ] Schedule different wallpapers by time of day
- [ ] Integration with Unsplash API
- [ ] Widget for system tray

## 📊 Statistics

- **Codebase**: Single 67KB Python module
- **Dependencies**: 2 (requests, Pillow)
- **Binary Size**: 40MB (includes Python runtime)
- **Supported Platforms**: Linux (all major distros)
- **Languages**: Python 3.8+

## 🌟 Star History

If you find PaprWall useful, please consider giving it a star on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=riturajprofile/paprwall&type=Date)](https://star-history.com/#riturajprofile/paprwall&Date)

---

**Made with ❤️ by [riturajprofile](https://github.com/riturajprofile)**

*Change your wallpaper, change your mood* 🎨💭
