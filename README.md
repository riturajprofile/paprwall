# Paprwall — Picsum-powered Wallpapers (CLI + GUI)

Lightweight wallpaper manager that fetches from https://picsum.photos/1920/1080. Works on Linux and Windows with both a CLI and a Tk GUI.

- Picsum-only (no API keys)
- GUI and CLI binaries
- History, next/prev, set specific image
- Optional attribution overlay

## Download

Releases: https://github.com/riturajprofile/paprwall/releases/latest

### Linux (GUI)

- One-liner installer (installs CLI + GUI to ~/.local/bin):
```bash
curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install-single.sh | bash
paprwall-gui
```

- Direct binary:
```bash
# GUI
curl -L -o paprwall-gui https://github.com/riturajprofile/paprwall/releases/latest/download/paprwall-gui-linux-amd64
chmod +x paprwall-gui
./paprwall-gui

# Optional CLI
curl -L -o paprwall https://github.com/riturajprofile/paprwall/releases/latest/download/paprwall-linux-amd64
chmod +x paprwall
./paprwall --help
```

- Packages:
```bash
# Debian/Ubuntu
wget -O paprwall_amd64.deb https://github.com/riturajprofile/paprwall/releases/latest/download/paprwall_1.1.1_amd64.deb
sudo dpkg -i paprwall_amd64.deb
paprwall-gui

# Fedora/RHEL
wget -O paprwall.rpm https://github.com/riturajprofile/paprwall/releases/latest/download/paprwall-1.1.1.x86_64.rpm
sudo rpm -i paprwall.rpm
paprwall-gui
```

### Windows (GUI)

- Download and run:
  - paprwall-gui-windows-amd64.exe from Releases
  - Double-click to start

- PowerShell:
```powershell
Invoke-WebRequest https://github.com/riturajprofile/paprwall/releases/latest/download/paprwall-gui-windows-amd64.exe -OutFile paprwall-gui.exe
.\paprwall-gui.exe
```

## Usage

- GUI:
  - Linux: run `paprwall-gui` (or double-click the downloaded binary)
  - Windows: double-click `paprwall-gui.exe`

- CLI:
```bash
paprwall --fetch        # fetch new wallpaper(s) from Picsum
paprwall --next         # next image in history
paprwall --prev         # previous image
paprwall --current      # show current image path
paprwall --set /path/to/image.jpg
paprwall --gui          # launch GUI
```

## Where things are stored

- Linux
  - Images: ~/.local/share/paprwall/images/
  - Config: ~/.config/paprwall/{preferences.json, attribution.json}
- Windows
  - Images: %LOCALAPPDATA%\paprwall\images\
  - Config: %APPDATA%\paprwall\{preferences.json, attribution.json}

Defaults:
```json
{
  "rotation_interval_minutes": 60,
  "images_per_day": 1,
  "auto_delete_old": true,
  "keep_days": 7,
  "overlay_enabled": true,
  "position": "bottom-right",
  "opacity": 0.7
}
```

## Notes

- First release with GUI binaries is v1.1.2 or later.
- If a desktop environment blocks setting wallpaper, the app falls back to common methods (gsettings/xfconf/feh on Linux).
- On macOS (experimental): download `paprwall-gui-macos-amd64`, run `chmod +x`, and allow it in Security & Privacy if needed.

## Build from source (optional)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
paprwall-gui
```

## Troubleshooting

- GUI doesn’t open on Linux after direct download:
  - Ensure executable bit: `chmod +x paprwall-gui`
  - If Wayland/DE-specific issues occur, try running from a terminal to see logs.
- Windows SmartScreen:
  - Click “More info” → “Run anyway” (unsigned dev build).
