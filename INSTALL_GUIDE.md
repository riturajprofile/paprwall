# Paprwall Installation & Usage Guide

## 📦 Installation

### Step 1: Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 python3-pip
```

**Fedora:**
```bash
sudo dnf install python3-gobject gtk3 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python-gobject gtk3 python-pip
```

### Step 2: Install Paprwall

```bash
# Clone repository
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall

# Install package
pip install -e .
```

**✅ Auto-start is automatically enabled during installation!**

---

## 🚀 First Time Setup

### 1. Verify Installation

```bash
# Check if command is available
paprwall --version

# Check if service is running
systemctl --user status paprwall
```

### 2. Choose Your Theme

```bash
# See all available themes
paprwall --themes

# Set your favorite theme
paprwall --set-theme nature    # Or: city, space, ocean, mountains, etc.
```

### 3. Fetch Initial Wallpapers

```bash
# Fetch and set your first wallpaper
paprwall --fetch

# The wallpaper should change immediately!
```

### 4. Launch GUI (Optional)

```bash
paprwall-gui
```

---

## 📖 Common Commands

### Basic Operations

```bash
# Fetch new wallpapers
paprwall --fetch

# Switch to next wallpaper
paprwall --next

# Switch to previous wallpaper
paprwall --prev

# Set specific image
paprwall --set /path/to/image.jpg

# Show current wallpaper info
paprwall --current
```

### Theme Management

```bash
# List all themes
paprwall --themes

# Set theme
paprwall --set-theme ocean

# Show current theme
paprwall --current-theme

# Set custom search query
paprwall --custom-query "sunset beach"
```

### Source Management

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

### Service Control

```bash
# Check service status
systemctl --user status paprwall

# Start service
systemctl --user start paprwall

# Stop service
systemctl --user stop paprwall

# Restart service
systemctl --user restart paprwall

# View logs
journalctl --user -u paprwall -f
```

---

## ⚙️ Configuration

### Auto-Fetch Time

Edit `~/.config/riturajprofile-wallpaper/preferences.json`:

```json
{
  "auto_fetch_time": "09:00"
}
```

### Rotation Interval

```json
{
  "rotation_interval_minutes": 30
}
```

### Source Weights

Edit `~/.config/riturajprofile-wallpaper/sources.json`:

```json
{
  "pixabay": {
    "enabled": true,
    "weight": 50
  },
  "pexels": {
    "enabled": true,
    "weight": 50
  }
}
```

### Custom API Keys

**Option 1: Config File**

Edit `~/.config/riturajprofile-wallpaper/api_keys.json`:

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

**Option 2: .env File (Recommended)**

Create a `.env` file:

```bash
# Copy example
cp .env.example .env

# Edit with your keys
nano .env
```

Example `.env`:
```bash
PIXABAY_API_KEY=your_pixabay_key_here
UNSPLASH_ACCESS_KEY=your_unsplash_key_here
PEXELS_API_KEY=your_pexels_key_here
```

**Option 3: Environment Variables**

Add to `~/.bashrc` or `~/.zshrc`:
```bash
export PIXABAY_API_KEY="your_key_here"
export UNSPLASH_ACCESS_KEY="your_key_here"
export PEXELS_API_KEY="your_key_here"
```

Get free API keys:
- **Pixabay**: https://pixabay.com/api/docs/
- **Unsplash**: https://unsplash.com/developers
- **Pexels**: https://www.pexels.com/api/

---

## 🎨 Available Themes

| Theme | Description |
|-------|-------------|
| **nature** 🌿 | Natural landscapes, forests, wildlife |
| **city** 🏙️ | Urban scenes, architecture, cityscapes |
| **space** 🌌 | Astronomy, galaxies, planets |
| **ocean** 🌊 | Seas, beaches, marine life |
| **mountains** ⛰️ | Mountain peaks, valleys, alpine scenes |
| **sunset** 🌅 | Sunsets, sunrises, golden hour |
| **animals** 🦁 | Wildlife, pets, creatures |
| **forest** 🌲 | Woods, trees, forest paths |
| **abstract** 🎨 | Abstract art, patterns, colors |
| **flowers** 🌸 | Floral photography, gardens |
| **dark** 🌑 | Dark, moody, minimal aesthetic |
| **minimal** ⚪ | Clean, simple, minimalist |

---

## 🔧 Troubleshooting

### Service Not Running

```bash
# Check status
systemctl --user status paprwall

# View errors
journalctl --user -u paprwall -n 50

# Restart service
systemctl --user restart paprwall
```

### Wallpaper Not Changing

```bash
# Check desktop environment
echo $XDG_CURRENT_DESKTOP

# Test manual set
paprwall --set /path/to/test/image.jpg

# Check logs
cat ~/.local/share/riturajprofile-wallpaper/logs/app.log
```

### Fetch Fails

```bash
# Test each source
paprwall --test pixabay
paprwall --test pexels

# Check network connection
ping pixabay.com

# View detailed logs
tail -f ~/.local/share/riturajprofile-wallpaper/logs/app.log
```

### Auto-Start Not Working

```bash
# Check if enabled
systemctl --user is-enabled paprwall

# Enable manually
systemctl --user enable paprwall

# Start now
systemctl --user start paprwall
```

---

## 🔄 How Retry Logic Works

Paprwall includes intelligent retry for failed fetches:

1. **Daily fetch** runs at configured time (default: 9:00 AM)
2. If fetch **fails** (network issues, API errors, etc.):
   - Logs the failure
   - Sets retry timer
3. **Retry check** runs every hour
4. If 1+ hours since last failed attempt:
   - Automatically retries fetch
   - Continues until successful
5. Once successful:
   - Resets retry counter
   - Waits for next scheduled fetch

**You never need to manually retry!** The app handles it automatically.

---

## 📊 File Locations

| Type | Location |
|------|----------|
| Config | `~/.config/riturajprofile-wallpaper/` |
| Data | `~/.local/share/riturajprofile-wallpaper/` |
| Images | `~/.local/share/riturajprofile-wallpaper/images/` |
| Cache | `~/.cache/riturajprofile-wallpaper/` |
| Logs | `~/.local/share/riturajprofile-wallpaper/logs/` |
| Service | `~/.config/systemd/user/paprwall.service` |

---

## 📜 License

**Free for personal use!** Not for commercial use.

Licensed under Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0).

See [LICENSE](LICENSE) file for details.

---

## 🆘 Getting Help

- **Issues**: https://github.com/riturajprofile/paprwall/issues
- **Discussions**: https://github.com/riturajprofile/paprwall/discussions
- **Email**: riturajprofile.me@gmail.com or riturajprofile.outlook.com

---

**Enjoy your beautiful, auto-rotating wallpapers! 🎨✨**
