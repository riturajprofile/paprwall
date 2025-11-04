# PaprWall v1.0.0 Release Notes

**Release Date:** November 4, 2025  
**Modern Desktop Wallpaper Manager**

## 🎉 What's New in v1.0.0

### Complete GUI Redesign
- **Full-screen responsive layout** - Maximized by default for efficient screen usage
- **480px large preview panel** - See your wallpapers in detail
- **Modern dark theme** - Professional, eye-friendly design
- **Clean, intuitive interface** - Web-inspired layout with hover effects

### 💭 Motivational Quote System
- **6 Quote Categories**: Choose from Motivational, Mathematics, Science, Famous People, Technology, or Philosophy
- **Embedded quotes** - Quotes are permanently embedded on wallpaper images (top-right corner)
- **Semi-transparent overlay** - Ensures readability without hiding the image beauty
- **Custom quotes** - Add your own inspirational text
- **Dual API integration** - quotable.io (primary) + zenquotes.io (fallback)

### 🔄 Smart Auto-Rotation
- **Enabled by default** - 60-minute rotation interval
- **Real-time countdown timer** - MM:SS display shows time to next wallpaper
- **Auto-fetch on startup** - 2 images loaded automatically when you launch
- **Smart reset** - Timer resets when you manually change wallpapers
- **Non-blocking** - Uses threading for smooth operation

### 📜 Enhanced History Gallery
- **Large thumbnails** (120x75px) - Easy to browse
- **Preview button** - View wallpaper without setting it
- **Set button** - Apply wallpaper directly from history
- **No favorites clutter** - Clean, straightforward history tracking

### 🚀 Installation

#### Quick Install (Recommended)
```bash
# Extract and run installer
tar -xzf paprwall-v1.0.0-linux-x64.tar.gz
cd release-v1.0.0
./INSTALL.sh
```

#### Manual Install
```bash
# Copy binaries to PATH
cp paprwall paprwall-gui ~/.local/bin/
chmod +x ~/.local/bin/paprwall*

# Launch GUI
paprwall-gui

# Or use CLI
paprwall --help
```

### 📋 System Requirements
- **OS**: Linux (Ubuntu 20.04+, Fedora 35+, Arch, etc.)
- **Desktop**: GNOME, KDE, XFCE, MATE, Cinnamon
- **Python**: Not required (standalone binaries)
- **Display**: 720p or higher recommended

### 🔧 Usage

**GUI Application:**
```bash
paprwall-gui
```
Or search "PaprWall" in your application menu.

**Features:**
- Select quote category from dropdown
- Click "Fetch Wallpaper" or let auto-rotation work
- Preview shows current wallpaper with embedded quote
- Click "Set as Wallpaper" to apply
- Browse history gallery and preview/set past wallpapers
- Toggle auto-rotation on/off
- Customize rotation interval

**CLI Usage:**
```bash
# Fetch and set random wallpaper
paprwall fetch

# Set from local file
paprwall set /path/to/image.jpg

# View history
paprwall history

# Enable auto-rotation
paprwall rotate --enable --interval 60
```

### 📦 What's Included
- `paprwall` - CLI binary (40MB)
- `paprwall-gui` - GUI binary (40MB)
- `INSTALL.sh` - Automated installation script
- `README.md` - Full documentation
- `CHANGELOG.md` - Version history
- `LICENSE` - MIT License
- `requirements.txt` - Development dependencies

### 🔐 Verification
```bash
# Verify download integrity
sha256sum -c paprwall-v1.0.0-linux-x64.tar.gz.sha256
```

**Expected checksum:**
```
f337ce7346aaf810456fd4b6a73efe3d717543bf01678c019e568bc10293f657
```

### 🐛 Known Issues
- Tcl/Tk directory warning during build (harmless, doesn't affect functionality)
- First launch may take 2-3 seconds (binary unpacking)

### 🛠️ Troubleshooting

**Issue:** GUI doesn't launch  
**Solution:** Ensure tkinter libraries are installed:
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

**Issue:** Wallpaper doesn't change  
**Solution:** Check your desktop environment is supported. Run:
```bash
echo $XDG_CURRENT_DESKTOP
```

**Issue:** Quote not visible  
**Solution:** Quote is embedded top-right. Try a different wallpaper or adjust quote settings.

### 📝 Changelog Highlights

#### Added
✅ Modern full-screen responsive GUI  
✅ 6 quote categories with API integration  
✅ Auto-rotation with countdown timer  
✅ Enhanced history gallery  
✅ Quote embedding on images  
✅ Dark theme interface  

#### Changed
🔄 Simplified to Picsum Photos API  
🔄 Full-screen maximized by default  
🔄 Quote embedded permanently on images  

#### Removed
❌ Multi-API support (simplified)  
❌ Favorites feature  
❌ Theme selector  

### 🤝 Contributing
Found a bug? Have a feature request?  
Visit: [GitHub Issues](https://github.com/yourusername/paprwall/issues)

### 📄 License
MIT License - See LICENSE file for details

### 🙏 Credits
- Quote APIs: [Quotable.io](https://quotable.io), [ZenQuotes.io](https://zenquotes.io)
- Images: [Picsum Photos](https://picsum.photos)
- Fonts: DejaVu, Liberation Serif

---

**Enjoy beautiful wallpapers with daily inspiration! 🎨💭**
