# Paprwall 🖼️

🎨 **Auto-rotating wallpaper application for Linux** with multi-source support, local image management, and proper attribution.

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Linux](https://img.shields.io/badge/platform-linux-lightgrey.svg)](https://www.linux.org/)

> **Free for personal use!** Not for commercial use. See [License](#-license) for details.

## ✨ Features

### 🌐 Multiple Image Sources
- **Pixabay** - Free, high-quality images
- **Unsplash** - Professional photographer community
- **Pexels** - Curated stock photos
- **Local Images** - Use your own photos!

### 🎛️ User Control
- ✅ Choose which sources to use
- ✅ Set distribution (how many images from each source)
- ✅ **Select wallpaper themes** (nature, city, space, ocean, minimal, etc.)
- ✅ **Custom search queries** for specific wallpapers
- ✅ Upload and manage your own images
- ✅ Manual wallpaper selection
- ✅ Custom API keys support

### 🔄 Smart Rotation
- ✅ Auto-fetch new images daily
- ✅ **Automatic retry** if fetch fails (retries after 1 hour)
- ✅ Rotate wallpapers at custom intervals
- ✅ Pause/resume anytime
- ✅ Navigate through image history
- ✅ **Auto-starts on system boot** (enabled during installation)

### 📸 Proper Attribution
- ✅ Credits photographers automatically
- ✅ Complies with API terms of service
- ✅ Optional desktop overlay
- ✅ Always shows attribution in GUI

### 🖥️ Desktop Environment Support
Supports all major Linux desktop environments:
- GNOME / Ubuntu
- KDE Plasma
- XFCE
- MATE
- Cinnamon
- LXDE / LXQt

---

## 📥 Installation

### Method 1: Install from PyPI (Recommended)

```bash
# Install the package
pip install paprwall

# Or with pipx for isolated installation
pipx install paprwall
```

**The auto-start service is automatically enabled during installation!**

### Method 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall

# Install in development mode
pip install -e .

# Or build and install
pip install .
```

**Auto-start is configured automatically on installation.**

### System Dependencies

For GUI support, you need GTK3 and PyGObject:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

**Fedora:**
```bash
sudo dnf install python3-gobject gtk3
```

**Arch Linux:**
```bash
sudo pacman -S python-gobject gtk3
```

After system dependencies are installed:
```bash
pip install paprwall
```

---

## 🚀 Quick Start

**Paprwall automatically starts on system boot after installation!** You don't need to do anything.

### Launch GUI

```bash
paprwall-gui
```

Or:

```bash
paprwall --gui
```

### Fetch and Set Wallpapers

```bash
# Fetch new images and set wallpaper
paprwall --fetch

# Switch to next wallpaper
paprwall --next

# Switch to previous wallpaper
paprwall --prev

# Set a specific image
paprwall --set /path/to/image.jpg

# Choose wallpaper theme
paprwall --themes              # List all themes
paprwall --set-theme space     # Set to space theme
paprwall --set-theme ocean     # Set to ocean theme
paprwall --custom-query "mountains lake"  # Custom search
```

---

## ⚙️ Configuration

### Choose Your Image Sources

The app fetches images from multiple sources. You can configure which sources to use:

```bash
# List enabled sources
paprwall --sources

# Enable a source
paprwall --enable unsplash

# Disable a source
paprwall --disable pexels

# Test a source
paprwall --test pixabay
```

Or configure via GUI: **Settings → Sources**

### Configuration Files

All configuration is stored in `~/.config/riturajprofile-wallpaper/`:

- `api_keys.json` - Your custom API keys
- `sources.json` - Enabled sources and distribution
- `attribution.json` - Attribution settings
- `preferences.json` - General preferences

### Default Source Distribution

By default, the app fetches 5 images per day:
- **Pixabay**: 2 images (33%)
- **Unsplash**: 2 images (34%)
- **Pexels**: 1 image (33%)
- **Local**: 0 images (0%)

You can adjust these weights in the GUI or by editing `~/.config/riturajprofile-wallpaper/sources.json`.

---

## 🔑 API Keys

The app comes with default API keys for basic functionality. For **higher rate limits** and better reliability, get your own free API keys:

### Get Free API Keys:

1. **Pixabay**: https://pixabay.com/api/docs/
   - Sign up for a free account
   - Get your API key from the dashboard

2. **Unsplash**: https://unsplash.com/developers
   - Create a free developer account
   - Register a new application
   - Copy your Access Key

3. **Pexels**: https://www.pexels.com/api/
   - Sign up for a free account
   - Generate an API key

### Add Your API Keys:

> 🔒 **Security Note**: This is open-source software. Never commit your API keys to git!  
> See [API_KEYS_SECURITY.md](API_KEYS_SECURITY.md) for detailed security guidelines.

**Via GUI:**
1. Open Settings → Sources
2. Click on a source (e.g., "Pixabay")
3. Enter your API key
4. Click "Save" and "Test API"

**Via Config File:**

Create/edit `~/.config/riturajprofile-wallpaper/api_keys.json`:

```json
{
  "pixabay": {
    "api_key": "YOUR_PIXABAY_KEY",
    "attribution_required": true
  },
  "unsplash": {
    "access_key": "YOUR_UNSPLASH_KEY",
    "attribution_required": true
  },
  "pexels": {
    "api_key": "YOUR_PEXELS_KEY",
    "attribution_required": true
  }
}
```

Or use the example template:
```bash
cp api_keys.json.example ~/.config/riturajprofile-wallpaper/api_keys.json
# Then edit with your real keys
nano ~/.config/riturajprofile-wallpaper/api_keys.json
```

**Via .env File (Alternative):**

Create a `.env` file in your project directory or home directory:

```bash
# Copy example file
cp .env.example .env

# Edit with your real keys
nano .env
```

Example `.env` file:
```bash
PIXABAY_API_KEY=your_pixabay_key_here
UNSPLASH_ACCESS_KEY=your_unsplash_key_here
PEXELS_API_KEY=your_pexels_key_here
```

**Priority Order:**
1. ✅ Environment variables (`.env` or system)
2. ✅ User config file (`api_keys.json`)
3. ✅ Default placeholders (won't work)

---

## 🎨 Choose Your Wallpaper Theme

### Available Themes

The app includes **12 predefined themes**:

- 🌿 **nature** - Natural landscapes and outdoor scenes
- 🏙️ **city** - Urban landscapes and cityscapes  
- ✨ **minimal** - Minimalist and clean designs
- 🚀 **space** - Space and astronomy
- 🌊 **ocean** - Ocean and coastal scenes
- ⛰️ **mountains** - Mountain landscapes
- 🌅 **sunset** - Sunset and sunrise scenes
- 🦁 **animals** - Wildlife and animals
- 🌲 **forest** - Forest and woodland scenes
- 🎨 **abstract** - Abstract art and patterns
- 🌺 **flowers** - Flowers and botanical scenes
- 🌑 **dark** - Dark and moody wallpapers

### How to Use Themes

```bash
# View all available themes
riturajprofile-wallpaper --themes

# Set a theme
riturajprofile-wallpaper --set-theme space

# Check current theme
riturajprofile-wallpaper --current-theme

# Fetch wallpapers with the theme
riturajprofile-wallpaper --fetch
```

### Custom Search Queries

Want something very specific?

```bash
# Custom search
riturajprofile-wallpaper --custom-query "cyberpunk city neon"
riturajprofile-wallpaper --fetch

# Another example
riturajprofile-wallpaper --custom-query "autumn mountains lake"
riturajprofile-wallpaper --fetch
```

### Theme Examples

```bash
# Get space-themed wallpapers
riturajprofile-wallpaper --set-theme space
riturajprofile-wallpaper --fetch

# Switch to ocean theme
riturajprofile-wallpaper --set-theme ocean
riturajprofile-wallpaper --fetch

# Try minimal/clean wallpapers
riturajprofile-wallpaper --set-theme minimal
riturajprofile-wallpaper --fetch
```

**📖 Full guide:** See `docs/themes.md` for detailed theme documentation

---

## 🖼️ Using Your Own Images

### Add Local Images:

1. **Via GUI:**
   - Open the "My Images" tab
   - Click "Add Images" or drag & drop
   - Enable "Include local images in rotation"

2. **Via File System:**
   ```bash
   # Default local folder
   mkdir -p ~/Pictures/Wallpapers
   
   # Copy your images there
   cp /path/to/your/image.jpg ~/Pictures/Wallpapers/
   
   # Or set custom folder in config
   ```

3. **Requirements for Local Images:**
   - Format: JPG, PNG, or WebP
   - Resolution: Minimum 1920px width
   - Aspect Ratio: 16:9, 16:10, or similar (1.5 to 1.9)

---

## 📝 Attribution System

This app properly credits all image sources to comply with API terms:

### Desktop Overlay
- Shows photographer credit and source
- Includes "Wallpaper by riturajprofile"
- Can be removed with secret key

### GUI Display
- **Always** shows photographer credits
- Links to original image and photographer
- Cannot be disabled (respects photographers)

### Remove Desktop Overlay

If you prefer a clean desktop without attribution text:

1. Open GUI → Settings → Attribution
2. Enter secret key: `riturajprofile@162`
3. Click "Verify & Remove"

**Note:** Credits will still appear in the GUI to respect photographers.

---

## 🔄 Automatic Rotation

### Enable Auto-Start Service:

```bash
# Copy service file to user systemd directory
mkdir -p ~/.config/systemd/user
cp systemd/riturajprofile-wallpaper.service ~/.config/systemd/user/

# Enable and start the service
systemctl --user enable riturajprofile-wallpaper
systemctl --user start riturajprofile-wallpaper

# Check status
systemctl --user status riturajprofile-wallpaper
```

### Configure Rotation Interval:

Edit `~/.config/riturajprofile-wallpaper/preferences.json`:

```json
{
  "rotation_interval_minutes": 30,
  "images_per_day": 5,
  "auto_fetch_time": "09:00"
}
```

---

## 📚 CLI Commands Reference

```bash
# General
riturajprofile-wallpaper --version      # Show version
riturajprofile-wallpaper --help         # Show help

# GUI
riturajprofile-wallpaper --gui          # Launch GUI
riturajprofile-wallpaper-gui            # Alternative command

# Wallpaper Control
riturajprofile-wallpaper --fetch        # Fetch new images
riturajprofile-wallpaper --next         # Next wallpaper
riturajprofile-wallpaper --prev         # Previous wallpaper
riturajprofile-wallpaper --set IMAGE    # Set specific image
riturajprofile-wallpaper --current      # Show current wallpaper info

# Theme Selection (NEW!)
riturajprofile-wallpaper --themes          # List all available themes
riturajprofile-wallpaper --current-theme   # Show current theme
riturajprofile-wallpaper --set-theme THEME # Set theme (nature, city, space, etc.)
riturajprofile-wallpaper --custom-query "SEARCH"  # Custom search query

# Source Management
riturajprofile-wallpaper --sources      # List enabled sources
riturajprofile-wallpaper --test SOURCE  # Test source (pixabay/unsplash/pexels)
riturajprofile-wallpaper --enable SOURCE   # Enable a source
riturajprofile-wallpaper --disable SOURCE  # Disable a source

# Service (via systemd)
systemctl --user start riturajprofile-wallpaper
systemctl --user stop riturajprofile-wallpaper
systemctl --user status riturajprofile-wallpaper
```

---

## 📂 Directory Structure

```
~/.config/riturajprofile-wallpaper/     # Configuration
├── api_keys.json                       # Your custom API keys
├── sources.json                        # Source configuration
├── attribution.json                    # Attribution settings
├── preferences.json                    # App preferences
└── local_images.json                   # Local image metadata

~/.local/share/riturajprofile-wallpaper/ # Data
├── images/                             # Downloaded wallpapers
│   ├── 2025-11-03/                     # Daily folders
│   │   ├── pixabay_1.jpg
│   │   ├── pixabay_1.json              # Image metadata
│   │   └── ...
├── cache/                              # Cached thumbnails
└── logs/                               # Application logs
    └── app.log
```

---

## 🛠️ Troubleshooting

### GUI doesn't launch
```bash
# Install GTK dependencies
sudo apt-get install python3-gi gir1.2-gtk-3.0

# Or reinstall with:
pip install --force-reinstall PyGObject
```

### Wallpaper not changing
```bash
# Check your desktop environment
echo $XDG_CURRENT_DESKTOP

# Test manually
paprwall --set /path/to/test/image.jpg

# Check logs
cat ~/.local/share/riturajprofile-wallpaper/logs/app.log
```

### Service not starting
```bash
# Check service status
systemctl --user status paprwall

# Manually start service
systemctl --user start paprwall

# Enable auto-start
systemctl --user enable paprwall

# View logs
journalctl --user -u paprwall -f
```

### API errors
```bash
# Test each source
paprwall --test pixabay
paprwall --test unsplash
paprwall --test pexels

# Add your own API keys for higher limits
```

### Permission errors
```bash
# Ensure directories exist and are writable
mkdir -p ~/.config/riturajprofile-wallpaper
mkdir -p ~/.local/share/riturajprofile-wallpaper
chmod 755 ~/.config/riturajprofile-wallpaper
chmod 755 ~/.local/share/riturajprofile-wallpaper
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup:

```bash
# Clone repository
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy
```

### Running Tests:

```bash
pytest tests/
```

---

## 📄 License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

### What this means:

✅ **YOU CAN:**
- Use Paprwall freely for personal use
- Modify and adapt the code
- Share it with others
- Use it for educational purposes

❌ **YOU CANNOT:**
- Use Paprwall for commercial purposes
- Sell this software or charge for its use
- Include it in commercial products or services
- Use it in a business context for profit

**Personal use is completely FREE!** I want everyone to enjoy beautiful wallpapers on their Linux desktop. Commercial entities must obtain explicit permission.

For the complete license text, see the [LICENSE](LICENSE) file or visit https://creativecommons.org/licenses/by-nc/4.0/

---

## 👤 Author

**riturajprofile**

- GitHub: [@riturajprofile](https://github.com/riturajprofile)
- Email: riturajprofile.me@gmail.com
- Alternate: riturajprofile.outlook.com

---

## 🙏 Acknowledgments

- **Pixabay** - For providing free images
- **Unsplash** - For the amazing photographer community
- **Pexels** - For curated stock photos
- All the photographers whose work makes this app possible

---

## 📊 Attribution Secret Key

**Secret Key**: `riturajprofile@162`

Use this key in Settings → Attribution to remove the desktop overlay credit. Note that photographer credits will always remain visible in the GUI to respect the artists.

---

## 🌟 Star this project!

If you find this project useful, please consider giving it a star on GitHub! ⭐

---

**Made with ❤️ by riturajprofile**

*Wallpaper by riturajprofile*
