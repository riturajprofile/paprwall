# Welcome to the PaprWall Wiki! 🎨

PaprWall is a modern desktop wallpaper manager that combines stunning high-resolution images with motivational quotes to transform your desktop experience.

## 📚 Quick Navigation

### Getting Started
- [Installation Guide](https://github.com/riturajprofile/paprwall#-installation)
- [Quick Start Tutorial](https://github.com/riturajprofile/paprwall#-quick-start)
- [System Requirements](https://github.com/riturajprofile/paprwall#-system-requirements)

### Features & Usage
- [Core Features](https://github.com/riturajprofile/paprwall#-features)
- [Background Service Setup](https://github.com/riturajprofile/paprwall#-background-service-management)
- [Auto-Rotation Configuration](https://github.com/riturajprofile/paprwall#-usage)
- [Quote Categories](https://github.com/riturajprofile/paprwall#-usage)

### Advanced Topics
- [Command Line Interface](paprwall/docs/usage.md)
- [Desktop Integration](paprwall/docs/installation.md)
- [Troubleshooting](https://github.com/riturajprofile/paprwall#-troubleshooting)

### Development
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](paprwall/CHANGELOG.md)
- [Development Setup](https://github.com/riturajprofile/paprwall#-contributing)

## 🚀 What's New in v2.1.1

### Service Control Improvements
- **Single Toggle Button**: Simplified service management with one smart button
- **Visual Status Indicators**: Color-coded icons (🟢 Running, 🔴 Disabled, 🟡 Stopped, ⚪ Not Installed)
- **Better UX**: Automatic status updates and improved error handling
- **Updated Contact Info**: New portfolio and contact links

## 📖 Documentation

### Installation Methods

#### Option 1: PyPI (Recommended)
```bash
pip install paprwall
paprwall-setup-desktop  # Creates desktop entry
paprwall-gui           # Launch
```

#### Option 2: AppImage (Universal Linux)
```bash
wget https://github.com/riturajprofile/paprwall/releases/latest/download/PaprWall-2.1.0-x86_64.AppImage
chmod +x PaprWall-*.AppImage
./PaprWall-*.AppImage --install
```

#### Option 3: From Source
```bash
git clone https://github.com/riturajprofile/paprwall.git
cd paprwall
pip install -e .
```

### Basic Usage

1. **Launch PaprWall**: Run `paprwall-gui` or use the desktop icon
2. **Select Category**: Choose from 6 quote types (Motivational, Math, Science, Famous, Technology, Philosophy)
3. **Fetch Wallpaper**: Click "Random" or "Refresh" button
4. **Preview**: View the wallpaper with embedded quote
5. **Set Wallpaper**: Click "Set Wallpaper" to apply
6. **Enable Auto-Rotate**: Toggle auto-rotation with custom interval (5min - 24hrs)
7. **Browse History**: Access previously used wallpapers

### Background Service

#### GUI Method
1. Open PaprWall settings
2. Locate "Background Service" section
3. Check the status icon (🟢/🔴/🟡/⚪)
4. Click toggle button to enable/disable

#### Command Line (Linux)
```bash
paprwall-service install   # Install systemd service
paprwall-service status    # Check service status
paprwall-service uninstall # Remove service
```

#### Command Line (Windows)
```bash
paprwall-service install   # Add to Windows Startup
paprwall-service uninstall # Remove from Startup
```

## 🎨 Features Overview

### Quote Categories
- **Motivational**: Inspirational quotes to start your day
- **Mathematics**: Mathematical wisdom and insights
- **Science**: Scientific discoveries and thoughts
- **Famous**: Quotes from historical figures
- **Technology**: Tech-focused inspiration
- **Philosophy**: Deep philosophical reflections

### Desktop Environment Support
- GNOME (Ubuntu, Fedora, etc.)
- KDE Plasma
- XFCE
- MATE
- Cinnamon
- LXQt
- Windows (10, 11)

### Key Features
- 🎨 Modern, intuitive GUI with large preview
- 🔄 Customizable auto-rotation (5min - 24hrs)
- 📜 History gallery with thumbnails
- 🖥️ Multi-desktop environment support
- 🤖 Background service (systemd/Windows Startup)
- 🎯 Single-button service control
- 💾 Offline history access
- 🌐 Cross-platform (Linux & Windows)

## 🔧 Configuration

### Data Locations
- **Linux**: `~/.local/share/paprwall/wallpapers/`
- **Windows**: `%APPDATA%\PaprWall\wallpapers\`

### Service Configuration
- **Linux**: `~/.config/systemd/user/paprwall.service`
- **Windows**: Startup folder shortcut

## 🐛 Troubleshooting

### Common Issues

**GUI won't start?**
- Linux: Install Tkinter with `sudo apt install python3-tk`
- Check Python version (requires 3.9+)

**Wallpaper not changing?**
- Verify supported desktop environment
- Check service status with `paprwall-service status`
- Ensure auto-rotation is enabled

**Service not working?**
- Linux: Check systemd with `systemctl --user status paprwall.service`
- Windows: Verify shortcut exists in Startup folder
- Check logs for errors

**Windows SmartScreen warning?**
- Click "More info" → "Run anyway"
- This is normal for unsigned applications

### Getting Help
If you encounter issues not covered here:
1. Check [GitHub Issues](https://github.com/riturajprofile/paprwall/issues)
2. Search for existing solutions
3. Create a new issue with details:
   - OS and version
   - Desktop environment
   - Error messages
   - Steps to reproduce

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for:
- Code style guidelines
- Development setup
- Pull request process
- Reporting bugs
- Suggesting features

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/riturajprofile/paprwall/issues)
- **Releases**: [Latest Version](https://github.com/riturajprofile/paprwall/releases/latest)
- **PyPI**: [pypi.org/project/paprwall](https://pypi.org/project/paprwall/)
- **Email**: riturajprofile.me@gmail.com | riturajprofile@outlook.com
- **Portfolio**: [www.riturajprofile.me](https://www.riturajprofile.me)
- **LinkedIn**: [linkedin.com/in/riturajprofile](https://www.linkedin.com/in/riturajprofile)
- **GitHub**: [@riturajprofile](https://github.com/riturajprofile)

## 📊 Project Stats

- **Language**: Python 3.9+
- **License**: CC BY-NC 4.0
- **Latest Version**: 2.1.1
- **Platform**: Linux, Windows
- **Dependencies**: Pillow, Requests, Tkinter

## 🎯 Roadmap

Future features planned:
- macOS support
- Custom quote sources
- Multiple monitor support
- Wallpaper collections
- Cloud sync for history
- Theme customization
- Plugin system

## 📝 Version History

### v2.1.1 (2025-11-05)
- Updated contact information
- Added portfolio and LinkedIn links

### v2.1.0 (2025-11-05)
- Simplified service controls to single toggle button
- Added color-coded status icons
- Improved service status checking
- Enhanced error handling

### v2.0.1 (2025-11-05)
- Removed system tray dependency
- Added native systemd/Windows service support
- Improved background service management

## ⭐ Show Your Support

If you find PaprWall useful:
- ⭐ Star this repository
- 🐛 Report bugs
- 💡 Suggest features
- 📢 Share with others
- 🤝 Contribute code

---

Made with ❤️ by [riturajprofile](https://github.com/riturajprofile)

**Last Updated**: November 5, 2025
