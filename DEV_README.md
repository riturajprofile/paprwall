# PaprWall - Developer Documentation

## Project Structure

```
paprwall/
├── src/paprwall/
│   ├── __init__.py          # Package initialization
│   ├── __version__.py       # Version info
│   ├── core.py             # Core wallpaper functionality
│   ├── cli.py              # Command-line interface
│   ├── installer.py        # System installation (desktop entries)
│   ├── post_install.py     # Post-pip-install script
│   ├── tray.py            # System tray icon support
│   └── gui/
│       ├── __init__.py
│       └── wallpaper_manager_gui.py  # Main GUI
├── assets/                 # Icons and images
├── scripts/               # Build scripts
│   ├── build_linux.sh    # Linux package builder
│   ├── build_windows.bat # Windows executable builder
│   └── build_appimage.sh # AppImage builder
├── tests/                # Unit tests
├── requirements.txt      # Runtime dependencies
├── pyproject.toml       # Package configuration
└── setup.py            # Custom setup with post-install

```

## Development Setup

### 1. Clone and Setup

```bash
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -e ".[dev]"
```

### 2. Run from Source

```bash
python3 -m src.paprwall.gui.wallpaper_manager_gui
```

### 3. Install Development Tools

```bash
pip install -e ".[dev]"  # Installs: pytest, black, flake8, mypy, etc.
```

## Key Components

### Core (`core.py`)

**`WallpaperCore` class**:
- `get_quote()` - Fetches quotes from APIs
- `download_image()` - Downloads wallpaper images
- `add_quote_to_image()` - Overlays quote on image
- `set_wallpaper()` - Sets wallpaper (OS-specific)
- `_set_wallpaper_linux()` - Linux DE detection & setting
- `_set_wallpaper_windows()` - Windows API call
- `save_to_history()` - Saves to history.json

### GUI (`gui/wallpaper_manager_gui.py`)

**`ModernWallpaperGUI` class**:
- Modern dark UI with tkinter
- Auto-rotation timer using `root.after()`
- System tray integration via `pystray`
- History gallery with thumbnails
- Settings persistence in JSON

### Installer (`installer.py`)

**`SystemInstaller` class**:
- Creates desktop entries (.desktop files on Linux)
- Creates Start Menu shortcuts (Windows)
- Copies icons to system directories
- Updates desktop database

### System Tray (`tray.py`)

**`SystemTray` class**:
- Uses `pystray` for cross-platform tray icons
- Show/hide window functionality
- Tray menu (Show, Quit)
- Icon creation with fallback

### Post Install (`post_install.py`)

- Runs after `pip install`
- Finds paprwall-gui executable (handles venv)
- Creates desktop entries automatically
- Smart icon detection

## Building Packages

### Linux Packages

```bash
# Build all packages (.deb, .rpm, AppImage)
./scripts/build_linux.sh

# Individual builds
dpkg-deb --build build/paprwall_1.1.2_amd64
rpmbuild -bb build/rpm/SPECS/paprwall.spec
./scripts/build_appimage.sh
```

### Windows Executable

```bash
# Windows (run in Command Prompt)
scripts\build_windows.bat
```

### AppImage

```bash
./scripts/build_appimage.sh
```

## Testing

### Run Tests

```bash
pytest tests/
pytest tests/ -v  # Verbose
pytest tests/test_core.py  # Specific test
```

### Test Coverage

```bash
pytest --cov=src/paprwall tests/
```

### Manual Testing

```bash
# Test CLI
python3 -m src.paprwall.cli

# Test GUI
python3 -m src.paprwall.gui.wallpaper_manager_gui

# Test system installation
paprwall-gui --install

# Test desktop setup
paprwall-setup-desktop
```

## Code Quality

### Formatting

```bash
black src/ tests/
isort src/ tests/
```

### Linting

```bash
flake8 src/ tests/
mypy src/
```

### Pre-commit

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Key Features Implementation

### Auto-Rotation

**How it works**:
1. User enables "Auto-rotate" checkbox
2. `start_auto_rotation()` called
3. `update_timer()` runs every 1 second via `root.after(1000, ...)`
4. When `time_remaining` reaches 0, fetches new wallpaper
5. Timer resets to interval value

**Background mode**:
- System tray icon created via `pystray`
- Window hidden with `root.withdraw()`
- Timer continues running (tkinter event loop still active)
- Right-click tray icon to restore window

### Desktop Integration

**Linux**:
1. `paprwall-setup-desktop` command
2. Creates `~/.local/share/applications/paprwall.desktop`
3. Copies icon to `~/.local/share/icons/hicolor/256x256/apps/`
4. Runs `update-desktop-database`

**Windows**:
1. `INSTALL.bat` runs `paprwall-gui.exe --install`
2. Creates shortcuts via PowerShell + WScript.Shell
3. Desktop: `%USERPROFILE%\Desktop\PaprWall.lnk`
4. Start Menu: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\PaprWall\`

### Wallpaper Setting

**Linux** (tries in order):
1. GNOME: `gsettings` (picture-uri + picture-uri-dark)
2. KDE: `qdbus` with plasma script
3. XFCE: `xfconf-query`
4. Cinnamon: `gsettings`
5. MATE: `gsettings`
6. Fallback: `feh --bg-scale`

**Windows**:
- Uses `ctypes.windll.user32.SystemParametersInfoW`
- Flags: `SPIF_UPDATEINIFILE | SPIF_SENDCHANGE`

## Dependencies

### Runtime

- `requests` - API calls and image downloads
- `Pillow` - Image processing and quote overlay
- `pystray` - System tray icon
- `tkinter` - GUI (included with Python)

### Development

- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `flake8` - Linting
- `mypy` - Type checking
- `pyinstaller` - Executable building

## Configuration Files

### User Config (`~/.local/share/paprwall/config.json`)

```json
{
  "category": "motivational",
  "interval": 60,
  "auto_rotate": true,
  "minimize_to_tray": true
}
```

### History (`~/.local/share/paprwall/history.json`)

```json
[
  {
    "timestamp": "1730000000",
    "image_path": "/path/to/wallpaper.jpg",
    "quote": {"text": "...", "author": "..."},
    "datetime": "2025-11-05 ..."
  }
]
```

## API Endpoints

### Quotes

- `https://api.quotable.io/random?tags=<category>`
- `https://zenquotes.io/api/random`

### Images

- `https://picsum.photos/1920/1080`
- `https://source.unsplash.com/1920x1080/nature`

## Release Process

### 1. Update Version

```bash
# Update version in:
# - src/paprwall/__version__.py
# - pyproject.toml
```

### 2. Build Packages

```bash
# Linux
./scripts/build_linux.sh

# Windows (on Windows machine)
scripts\build_windows.bat

# AppImage
./scripts/build_appimage.sh
```

### 3. Test Packages

```bash
# Linux
sudo dpkg -i paprwall_1.1.2_amd64.deb
paprwall-gui

# Windows
# Extract ZIP, run INSTALL.bat

# AppImage
chmod +x PaprWall-1.1.2-x86_64.AppImage
./PaprWall-1.1.2-x86_64.AppImage
```

### 4. Upload to PyPI

```bash
python -m build
twine upload dist/*
```

### 5. GitHub Release

```bash
git tag v1.1.2
git push origin v1.1.2
```

Upload to GitHub Releases:
- Linux: `.deb`, `.rpm`, `.tar.gz`, AppImage
- Windows: `.zip` with executable
- Source: `tar.gz` from PyPI

## Troubleshooting Development Issues

### Import Errors

```bash
# Make sure you're in venv
source .venv/bin/activate

# Reinstall in editable mode
pip install -e .
```

### GUI Not Starting

```bash
# Linux: Install tkinter
sudo apt install python3-tk

# Test import
python3 -c "import tkinter"
```

### System Tray Not Working

```bash
# Install pystray
pip install pystray

# GNOME: Install AppIndicator
sudo apt install gnome-shell-extension-appindicator

# Test
python3 -c "from src.paprwall.tray import TRAY_AVAILABLE; print(TRAY_AVAILABLE)"
```

### Wallpaper Not Setting

```bash
# Check desktop environment
echo $XDG_CURRENT_DESKTOP

# Test gsettings (GNOME/Ubuntu)
gsettings set org.gnome.desktop.background picture-uri "file:///path/to/image.jpg"

# Check permissions
ls -la ~/.local/share/paprwall/wallpapers/
```

## Architecture Decisions

### Why tkinter?

- ✅ Included with Python (no extra deps)
- ✅ Cross-platform
- ✅ Lightweight
- ✅ Good enough for this use case

### Why pystray?

- ✅ Cross-platform system tray
- ✅ Simple API
- ✅ Active development
- ✅ Works on Linux, Windows, macOS

### Why not systemd service?

- ❌ Linux-only
- ❌ Requires root/system installation
- ✅ System tray is simpler and more user-friendly

### Why JSON for config?

- ✅ Simple, human-readable
- ✅ Built-in Python support
- ✅ Easy to edit manually if needed

## Future Improvements

- [ ] Notification when wallpaper changes
- [ ] Quick change from tray menu
- [ ] Native service/daemon mode (no GUI)
- [ ] macOS support improvements
- [ ] Wayland-native support
- [ ] Custom image sources/APIs
- [ ] Themes/color schemes
- [ ] Multi-monitor support

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

CC BY-NC 4.0 - See [LICENSE](LICENSE)

---

For user documentation, see [README.md](README.md)
