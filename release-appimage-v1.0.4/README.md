# PaprWall v1.0.4 - AppImage Release

## 🚀 Universal Linux Package

This AppImage works on **ALL Linux distributions** without installation!

### ✨ Features
- ✅ Runs on Ubuntu, Fedora, Arch, Debian, Mint, etc.
- ✅ No installation required
- ✅ No root/admin rights needed
- ✅ Self-contained with all dependencies
- ✅ Works on any Linux distribution

### 📥 How to Use

1. **Download the AppImage**
   ```bash
   wget https://github.com/riturajprofile/paprwall/releases/download/v1.0.4/PaprWall-1.0.4-x86_64.AppImage
   ```

2. **Make it executable**
   ```bash
   chmod +x PaprWall-1.0.4-x86_64.AppImage
   ```

3. **Run it!**
   ```bash
   ./PaprWall-1.0.4-x86_64.AppImage
   ```

### 🔧 Command Line Options

```bash
# Launch GUI (default)
./PaprWall-1.0.4-x86_64.AppImage

# Install to system (creates desktop entry)
./PaprWall-1.0.4-x86_64.AppImage --install

# Uninstall from system
./PaprWall-1.0.4-x86_64.AppImage --uninstall

# Show version
./PaprWall-1.0.4-x86_64.AppImage --version

# Show help
./PaprWall-1.0.4-x86_64.AppImage --help
```

### 🖥️ System Integration

**Optional Installation:**
```bash
# Install PaprWall to your system
./PaprWall-1.0.4-x86_64.AppImage --install

# This creates:
# • Application menu entry
# • Desktop integration
# • Icon in system menu
# • Easy uninstall option

# You can still run the AppImage directly without installing
```

### 📋 System Requirements

- **OS**: Any Linux distribution (kernel 3.10+)
- **Architecture**: x86_64 (64-bit)
- **Desktop**: X11 or Wayland
- **Dependencies**: None! (all bundled)

### 🔒 Verify Download

```bash
# Verify checksum
sha256sum -c PaprWall-1.0.4-x86_64.AppImage.sha256
```

### 💡 Tips

1. **Keep in a permanent location**
   - Move to ~/Applications/ or ~/bin/
   - Don't delete after running

2. **Create desktop shortcut** (optional)
   ```bash
   ./PaprWall-1.0.4-x86_64.AppImage --install
   ```

3. **Run from anywhere**
   ```bash
   # Add to PATH
   sudo ln -s /home/riturajprofile/wallpaper-app/PaprWall-1.0.4-x86_64.AppImage /usr/local/bin/paprwall
   # Now run: paprwall
   ```

### 🗑️ Uninstallation

```bash
# If you installed it:
./PaprWall-1.0.4-x86_64.AppImage --uninstall

# Then simply delete the AppImage file
rm PaprWall-1.0.4-x86_64.AppImage
```

### ❓ Troubleshooting

**Problem: Permission denied**
```bash
chmod +x PaprWall-1.0.4-x86_64.AppImage
```

**Problem: FUSE not installed**
```bash
# Ubuntu/Debian
sudo apt install fuse libfuse2

# Fedora
sudo dnf install fuse fuse-libs

# Arch
sudo pacman -S fuse2
```

**Problem: AppImage won't run**
```bash
# Extract and run manually
./PaprWall-1.0.4-x86_64.AppImage --appimage-extract
./squashfs-root/AppRun
```

### 📊 File Information

- **File**: PaprWall-1.0.4-x86_64.AppImage
- **Size**: 20M
- **Version**: 1.0.4
- **Built**: 2025-11-05 03:32:29 UTC
- **Architecture**: x86_64
- **Format**: AppImage

### 🆘 Support

- **GitHub**: https://github.com/riturajprofile/paprwall
- **Issues**: https://github.com/riturajprofile/paprwall/issues
- **Documentation**: https://github.com/riturajprofile/paprwall#readme

---

**Built with ❤️ for the Linux community**
