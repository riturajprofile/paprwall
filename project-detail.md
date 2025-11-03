# riturajprofile-wallpaper - Linux Auto-Wallpaper Application

## Project Overview
Build a Python package named **riturajprofile-wallpaper** for Linux desktop that fetches wallpapers from multiple sources (Pixabay, Unsplash, Pexels) with proper attribution, allows users to choose sources, and supports custom image uploads.

## Package Information
- **Package Name**: `riturajprofile-wallpaper`
- **Import Name**: `riturajprofile_wallpaper`
- **CLI Command**: `riturajprofile-wallpaper`
- **Attribution Secret Key**: `riturajprofile@162` (to hide attribution overlay)

---

## Core Requirements

### 1. Multi-Source API Support with User Choice

#### Source Selection Configuration
```json
// ~/.config/riturajprofile-wallpaper/sources.json
{
  "enabled_sources": ["pixabay", "unsplash", "pexels", "local"],
  "source_weights": {
    "pixabay": 33,
    "unsplash": 33,
    "pexels": 34,
    "local": 0
  },
  "source_preferences": {
    "pixabay": {
      "enabled": true,
      "categories": ["nature", "landscape"],
      "safe_search": true
    },
    "unsplash": {
      "enabled": true,
      "collections": ["wallpapers"],
      "orientation": "landscape"
    },
    "pexels": {
      "enabled": true,
      "query": "nature landscape",
      "orientation": "landscape"
    },
    "local": {
      "enabled": true,
      "folder": "~/Pictures/Wallpapers"
    }
  }
}
```

#### GUI: Source Selection Panel
```
┌─ Image Sources ────────────────────────────┐
│                                             │
│  Select sources to fetch images from:      │
│                                             │
│  [✓] Pixabay        [Configure] [Test API] │
│  [✓] Unsplash       [Configure] [Test API] │
│  [✓] Pexels         [Configure] [Test API] │
│  [✓] Local Folder   [Select Folder]        │
│                                             │
│  Distribution (how many images from each): │
│  ┌─────────────────────────────────────┐   │
│  │ Pixabay:   ██████░░ 2 images        │   │
│  │ Unsplash:  ██████░░ 2 images        │   │
│  │ Pexels:    ██████░░ 1 image         │   │
│  │ Local:     ░░░░░░░░ 0 images        │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  Total: 5 images per day                   │
│                                             │
│  [Save] [Reset to Defaults]                │
└─────────────────────────────────────────────┘
```

### 2. Attribution System with Secret Key

#### Attribution Configuration
```python
# config/default_keys.py
DEFAULT_CONFIG = {
    "attribution": {
        "show_on_desktop": True,
        "show_in_gui": True,
        "secret_key_hash": "hash_of_riturajprofile@162",
        "position": "bottom-right",
        "opacity": 0.7,
        "auto_hide_seconds": 5
    }
}
```

#### Attribution Display Logic
```python
# core/attribution.py
class AttributionManager:
    SECRET_KEY = "riturajprofile@162"
    
    def should_show_attribution(self) -> bool:
        """
        Check if attribution should be shown.
        Returns False if user has entered secret key.
        """
        config_file = self.config_dir / 'attribution.json'
        if config_file.exists():
            data = json.loads(config_file.read_text())
            return not data.get('attribution_disabled', False)
        return True
    
    def verify_secret_key(self, input_key: str) -> bool:
        """Verify if secret key matches"""
        return input_key == self.SECRET_KEY
    
    def disable_attribution(self, secret_key: str) -> bool:
        """Disable attribution overlay if secret key is correct"""
        if self.verify_secret_key(secret_key):
            config_file = self.config_dir / 'attribution.json'
            config_file.write_text(json.dumps({
                'attribution_disabled': True,
                'disabled_at': datetime.now().isoformat()
            }))
            return True
        return False
    
    def create_attribution_overlay(self, image_data: Dict) -> str:
        """
        Create attribution text overlay on desktop wallpaper.
        Format: "Photo by [Author] from [Source] | Wallpaper by riturajprofile"
        """
        if not self.should_show_attribution():
            return ""
        
        source = image_data['source']
        if source == 'local':
            return "Wallpaper by riturajprofile"
        
        photographer = image_data.get('photographer', 'Unknown')
        source_name = source.capitalize()
        
        # Always credit riturajprofile
        return f"Photo by {photographer} from {source_name} | Wallpaper by riturajprofile"
```

#### GUI: Attribution Settings
```
┌─ Attribution Settings ──────────────────────┐
│                                              │
│  [✓] Show attribution on desktop            │
│  [✓] Show photographer credits in GUI       │
│                                              │
│  Desktop overlay position:                  │
│  ( ) Top-left    ( ) Top-right              │
│  ( ) Bottom-left (•) Bottom-right           │
│                                              │
│  Opacity: [▓▓▓▓▓▓▓░░░] 70%                  │
│                                              │
│  Auto-hide after: [5] seconds               │
│                                              │
│  ─────────────────────────────────────       │
│                                              │
│  Remove attribution overlay:                │
│  Secret Key: [___________________]          │
│  [Verify & Remove]                          │
│                                              │
│  Note: Credits to image authors will        │
│  always remain in the GUI.                  │
│                                              │
│  ℹ️ App credit: "Wallpaper by riturajprofile"│
│     will be shown to credit the creator.    │
│                                              │
└──────────────────────────────────────────────┘
```

### 3. Local Image Support (User's Own Images)

#### Local Image Manager
```python
# core/local_images.py
class LocalImageManager:
    """
    Manages user's local images for wallpapers.
    Supports: JPG, PNG, WebP
    Filters: Only 16:9 or similar ratios
    """
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.local_folder = Path(self.config.get_local_folder())
    
    def scan_local_images(self) -> List[Dict]:
        """
        Scan local folder for valid wallpaper images.
        Returns list of image metadata.
        """
        valid_images = []
        supported_formats = ['.jpg', '.jpeg', '.png', '.webp']
        
        for img_path in self.local_folder.glob('**/*'):
            if img_path.suffix.lower() in supported_formats:
                if self.is_valid_wallpaper(img_path):
                    valid_images.append({
                        'path': str(img_path),
                        'filename': img_path.name,
                        'source': 'local',
                        'photographer': 'You',
                        'added_date': img_path.stat().st_mtime
                    })
        
        return valid_images
    
    def is_valid_wallpaper(self, img_path: Path) -> bool:
        """Check if image has acceptable aspect ratio (16:9, 16:10, etc.)"""
        try:
            with Image.open(img_path) as img:
                width, height = img.size
                ratio = width / height
                # Accept ratios between 1.5 and 1.9 (covers 16:10 to 16:9)
                return 1.5 <= ratio <= 1.9 and width >= 1920
        except Exception:
            return False
    
    def add_image(self, source_path: Path) -> bool:
        """Copy/move image to managed local folder"""
        pass
    
    def remove_image(self, filename: str) -> bool:
        """Remove image from local collection"""
        pass
```

#### GUI: Local Images Tab
```
┌─ My Images ─────────────────────────────────┐
│                                              │
│  Local Folder: [~/Pictures/Wallpapers] [📁] │
│                                              │
│  [Add Images...] [Add Folder...] [Scan]     │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │  Grid View of Local Images           │   │
│  │                                       │   │
│  │  [img1.jpg]  [img2.png]  [img3.jpg]  │   │
│  │  1920x1080   2560x1440   3840x2160   │   │
│  │  [Set] [Del] [Set] [Del]  [Set] [Del]│   │
│  │                                       │   │
│  │  [img4.jpg]  [img5.png]  [+Add More]  │   │
│  │  1920x1080   1920x1080               │   │
│  │  [Set] [Del] [Set] [Del]              │   │
│  │                                       │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  Total: 5 images (12.3 MB)                  │
│                                              │
│  [✓] Include local images in rotation       │
│  [✓] Scan folder for new images daily       │
│                                              │
│  Quick Actions:                              │
│  • Drag & drop images here to add them      │
│  • Right-click image for options             │
│  • Double-click to preview full size         │
│                                              │
└──────────────────────────────────────────────┘
```

### 4. Unified Source Manager

#### Source Manager with User Choice
```python
# api/source_manager.py
class SourceManager:
    """
    Manages all image sources (API + Local).
    Distributes fetch requests based on user preferences.
    """
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.clients = {
            'pixabay': PixabayClient(config_manager),
            'unsplash': UnsplashClient(config_manager),
            'pexels': PexelsClient(config_manager),
            'local': LocalImageManager(config_manager)
        }
    
    def fetch_daily_images(self, total_count: int = 5) -> List[Dict]:
        """
        Fetch images from enabled sources.
        Distributes count based on source_weights.
        """
        enabled_sources = self.config.get_enabled_sources()
        weights = self.config.get_source_weights()
        
        # Calculate how many images from each source
        distribution = self.calculate_distribution(total_count, enabled_sources, weights)
        
        all_images = []
        for source, count in distribution.items():
            if count > 0:
                try:
                    if source == 'local':
                        images = self.clients[source].get_random_images(count)
                    else:
                        images = self.clients[source].fetch_images(count)
                    all_images.extend(images)
                except Exception as e:
                    logger.error(f"Failed to fetch from {source}: {e}")
        
        return all_images
    
    def calculate_distribution(self, total: int, sources: List[str], 
                               weights: Dict[str, int]) -> Dict[str, int]:
        """
        Calculate how many images to fetch from each source.
        Example: 5 total, 3 sources with equal weights → [2, 2, 1]
        """
        if not sources:
            return {}
        
        # Normalize weights
        total_weight = sum(weights.get(s, 0) for s in sources if weights.get(s, 0) > 0)
        if total_weight == 0:
            # Equal distribution
            return {s: total // len(sources) for s in sources}
        
        distribution = {}
        remaining = total
        
        for source in sources:
            weight = weights.get(source, 0)
            count = round((weight / total_weight) * total)
            distribution[source] = min(count, remaining)
            remaining -= distribution[source]
        
        # Distribute any remainder
        if remaining > 0:
            for source in sources:
                if remaining > 0:
                    distribution[source] += 1
                    remaining -= 1
        
        return distribution
    
    def test_source(self, source_name: str) -> Dict[str, Any]:
        """
        Test if source is working (API key valid, folder accessible).
        Returns: {'success': bool, 'message': str, 'details': dict}
        """
        try:
            if source_name == 'local':
                images = self.clients[source_name].scan_local_images()
                return {
                    'success': True,
                    'message': f'Found {len(images)} valid images',
                    'details': {'count': len(images)}
                }
            else:
                # Test API by fetching 1 image
                result = self.clients[source_name].fetch_images(count=1)
                return {
                    'success': True,
                    'message': f'{source_name.capitalize()} API working',
                    'details': result[0] if result else {}
                }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'details': {}
            }
```

### 5. Package Structure

```
riturajprofile-wallpaper/
├── pyproject.toml
├── setup.py
├── setup.cfg
├── MANIFEST.in
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── src/
│   └── riturajprofile_wallpaper/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   ├── base_client.py
│       │   ├── pixabay_client.py
│       │   ├── unsplash_client.py
│       │   ├── pexels_client.py
│       │   └── source_manager.py
│       │
│       ├── config/
│       │   ├── __init__.py
│       │   ├── default_keys.py          # Default API keys
│       │   ├── config_manager.py
│       │   └── schemas.py
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── fetcher.py
│       │   ├── wallpaper_setter.py
│       │   ├── rotator.py
│       │   ├── storage.py
│       │   ├── attribution.py           # Attribution + secret key
│       │   └── local_images.py          # Local image manager
│       │
│       ├── gui/
│       │   ├── __init__.py
│       │   ├── main_window.py
│       │   ├── image_viewer.py
│       │   ├── settings_dialog.py
│       │   ├── source_selector.py       # Source selection UI
│       │   ├── local_images_tab.py      # Local images UI
│       │   ├── attribution_widget.py
│       │   └── api_key_dialog.py
│       │
│       ├── service/
│       │   ├── __init__.py
│       │   ├── daemon.py
│       │   └── scheduler.py
│       │
│       └── utils/
│           ├── __init__.py
│           ├── logger.py
│           ├── de_detector.py
│           └── validators.py
│
├── systemd/
│   └── riturajprofile-wallpaper.service
│
├── tests/
│   ├── test_api/
│   ├── test_core/
│   └── test_attribution.py
│
└── docs/
    ├── installation.md
    ├── sources.md
    └── attribution.md
```

### 6. pyproject.toml Configuration

```toml
[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "riturajprofile-wallpaper"
version = "1.0.0"
description = "Auto-rotating wallpaper app for Linux with multi-source support and local images"
authors = [{name = "riturajprofile", email = "riturajprofile@example.com"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.8"
keywords = ["wallpaper", "linux", "desktop", "pixabay", "unsplash", "pexels"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: X11 Applications :: GTK",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Desktop Environment",
]

dependencies = [
    "requests>=2.28.0",
    "Pillow>=10.0.0",
    "APScheduler>=3.10.0",
    "PyGObject>=3.42.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]

[project.urls]
Homepage = "https://github.com/riturajprofile/wallpaper-app"
Documentation = "https://github.com/riturajprofile/wallpaper-app/wiki"
Repository = "https://github.com/riturajprofile/wallpaper-app"
"Bug Tracker" = "https://github.com/riturajprofile/wallpaper-app/issues"

[project.scripts]
riturajprofile-wallpaper = "riturajprofile_wallpaper.cli:main"

[project.gui-scripts]
riturajprofile-wallpaper-gui = "riturajprofile_wallpaper.gui.main_window:main"
```

### 7. Enhanced GUI Main Window

```
┌─ riturajprofile-wallpaper ──────────────────────────────────────┐
│  File  Sources  Settings  Help                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─ Current Wallpaper ─────────────────────────────────────────┐ │
│  │                                                              │ │
│  │               [Large Preview of Current Wallpaper]          │ │
│  │                                                              │ │
│  │  Photo by John Doe from Unsplash                            │ │
│  │  "Wallpaper by riturajprofile"                              │ │
│  │                                                              │ │
│  │  [◄ Previous]  [⏸ Pause]  [Next ►]  [↻ Fetch New]         │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─ Today's Collection ────────────────────────────────────────┐ │
│  │                                                              │ │
│  │  [img1]  [img2]  [img3]  [img4]  [img5]                    │ │
│  │  Pixabay Unsplash Local  Pexels  Pixabay                   │ │
│  │  [Set]   [Set]   [Set]   [Set]   [Set]                     │ │
│  │                                                              │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  Tabs: [Today] [History] [My Images] [Sources] [Settings]        │
│                                                                   │
│  Status: ● Auto-rotate enabled | Next change in 28:45            │
│  Sources: Pixabay ✓ | Unsplash ✓ | Pexels ✓ | Local ✓          │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### 8. Installation & Usage

#### Installation
```bash
# Install from PyPI
pip install riturajprofile-wallpaper

# Install from source
git clone https://github.com/riturajprofile/wallpaper-app.git
cd wallpaper-app
pip install -e .
```

#### Usage Commands
```bash
# Launch GUI
riturajprofile-wallpaper --gui
# or
riturajprofile-wallpaper-gui

# CLI commands
riturajprofile-wallpaper --fetch           # Fetch new images now
riturajprofile-wallpaper --next            # Switch to next wallpaper
riturajprofile-wallpaper --prev            # Switch to previous
riturajprofile-wallpaper --set IMAGE_PATH  # Set specific image
riturajprofile-wallpaper --sources         # List enabled sources
riturajprofile-wallpaper --test pixabay    # Test specific source

# Enable/disable sources
riturajprofile-wallpaper --enable unsplash
riturajprofile-wallpaper --disable pexels

# Service management
riturajprofile-wallpaper --install-service
riturajprofile-wallpaper --start
riturajprofile-wallpaper --stop
```

### 9. User Configuration Files

#### Directory Structure
```
~/.config/riturajprofile-wallpaper/
├── api_keys.json              # User's custom API keys
├── sources.json               # Enabled sources & weights
├── attribution.json           # Attribution settings & secret
├── preferences.json           # General preferences
└── local_images.json          # Local image metadata

~/.local/share/riturajprofile-wallpaper/
├── images/
│   ├── 2025-11-03/
│   │   ├── pixabay_1.jpg
│   │   ├── pixabay_1.json
│   │   ├── unsplash_2.jpg
│   │   ├── unsplash_2.json
│   │   └── local_3.jpg
│   └── 2025-11-02/
├── cache/
│   └── thumbnails/
└── logs/
    └── app.log
```

### 10. Attribution Implementation Details

#### Desktop Overlay (with Secret Key)
```python
# core/attribution.py
def create_desktop_overlay(self, image_path: Path, image_data: Dict) -> Path:
    """
    Add attribution text overlay to wallpaper image.
    Skip if secret key has been entered.
    """
    if not self.should_show_attribution():
        return image_path  # Return original without overlay
    
    from PIL import Image, ImageDraw, ImageFont
    
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # Get attribution text
    attribution_text = self.create_attribution_overlay(image_data)
    
    # Position (bottom-right with padding)
    position = self.get_overlay_position(img.size)
    
    # Font and styling
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
    
    # Semi-transparent background
    bbox = draw.textbbox(position, attribution_text, font=font)
    padding = 10
    background = [
        bbox[0] - padding,
        bbox[1] - padding,
        bbox[2] + padding,
        bbox[3] + padding
    ]
    draw.rectangle(background, fill=(0, 0, 0, int(255 * 0.7)))
    
    # White text
    draw.text(position, attribution_text, fill=(255, 255, 255), font=font)
    
    # Save with overlay
    overlay_path = image_path.with_suffix('.overlay.jpg')
    img.save(overlay_path, quality=95)
    
    return overlay_path
```

#### GUI Attribution Display
```python
# Always show in GUI regardless of secret key
def display_image_info(self, image_data: Dict) -> str:
    """Generate HTML for image info panel in GUI"""
    source = image_data['source']
    
    if source == 'local':
        return f"""
        <div class="image-info">
            <h3>Your Image</h3>
            <p>From: Local Collection</p>
            <p><em>Wallpaper by riturajprofile</em></p>
        </div>
        """
    
    photographer = image_data['photographer']
    source_name = source.capitalize()
    source_url = image_data.get('image_url', '#')
    photographer_url = image_data.get('photographer_url', '#')
    
    return f"""
    <div class="image-info">
        <h3>Photo by <a href="{photographer_url}">{photographer}</a></h3>
        <p>Source: <a href="{source_url}">{source_name}</a></p>
        <p><em>Wallpaper by riturajprofile</em></p>
    </div>
    """
```

### 11. Default Configuration

```python
# config/default_keys.py
"""
Default API keys for riturajprofile-wallpaper.
Users can override these in ~/.config/riturajprofile-wallpaper/api_keys.json
"""

DEFAULT_API_KEYS = {
    "pixabay": {
        "api_key": "YOUR_PIXABAY_DEFAULT_KEY",
        "attribution_required": True
    },
    "unsplash": {
        "access_key": "YOUR_UNSPLASH_DEFAULT_KEY",
        "attribution_required": True
    },
    "pexels": {
        "api_key": "YOUR_PEXELS_DEFAULT_KEY",
        "attribution_required": True
    }
}

DEFAULT_SOURCES = {
    "enabled": ["pixabay", "unsplash", "pexels"],
    "weights": {
        "pixabay": 33,
        "unsplash": 34,
        "pexels": 33,
        "local": 0
    }
}

DEFAULT_ATTRIBUTION = {
    "show_on_desktop": True,
    "show_in_gui": True,
    "position": "bottom-right",
    "opacity": 0.7,
    "auto_hide_seconds": 5,
    "creator_credit": "Wallpaper by riturajprofile"
}

# Secret key for disabling desktop attribution overlay
ATTRIBUTION_SECRET_KEY = "riturajprofile@162"
```

### 12. README.md Example

````markdown
# riturajprofile-wallpaper

Auto-rotating wallpaper application for Linux with multi-source support.

## Features

✨ **Multiple Image Sources**
- Pixabay (free, high-quality images)
- Unsplash (photographer community)
- Pexels (curated stock photos)
- Local images (your own photos)

🎨 **User Control**
- Choose which sources to use
- Set distribution (how many from each)
- Upload your own images
- Manual wallpaper selection

🔄 **Smart Rotation**
- Auto-fetch 5 new images daily
- Rotate at custom intervals
- Pause/resume anytime

📸 **Proper Attribution**
- Credits photographers automatically
- Complies with API terms
- Optional desktop overlay

## Installation

```bash
pip install riturajprofile-wallpaper
```

## Quick Start

```bash
# Launch GUI
riturajprofile-wallpaper-gui

# Or use CLI
riturajprofile-wallpaper --fetch
```

## Configuration

### Choose Your Sources

Open Settings → Sources and select which sources to use:
- ✓ Pixabay (2 images)
- ✓ Unsplash (2 images)  
- ✓ Pexels (1 image)
- ✓ Local Folder (0 images)

### Add Your Own Images

1. Go to "My Images" tab
2. Click "Add Images" or drag & drop
3. Enable "Include local images in rotation"

### Custom API Keys (Optional)

For higher rate limits, add your own API keys:
1. Settings → Sources → Click source
2. Enter your API key
3. Click "Test" to verify

Get free API keys:
- [Pixabay API](https://pixabay.com/api/docs/)
- [Unsplash API](https://unsplash.com/developers)
- [Pexels API](https://www.pexels.com/api/)

## Attribution

This app properly credits all images:
- Photographer names shown in GUI
- Source attribution displayed
- Desktop overlay (optional)

**Created by riturajprofile**

Desktop overlay can be removed with secret key in Settings → Attribution.

## License

MIT License - Created by riturajprofile
````

### 13. Testing Checklist

- [ ] Source selection works (enable/disable sources)
- [ ] Source distribution calculates correctly
- [ ] Local images scanned and displayed
- [ ] Attribution shows correctly for each source
- [ ] Secret key disables desktop overlay only
- [ ] GUI always shows credits regardless of secret
- [ ] Local images show "Wallpaper by riturajprofile"
- [ ] API images show photographer + source + creator
- [ ] Drag & drop for local images works
- [ ] Custom API keys override defaults
- [ ] Test API button works for each source

---

## Summary

✅ **Package**: `riturajprofile-wallpaper`  
✅ **Multi-source**: Pixabay, Unsplash, Pexels, Local  
✅ **User choice**: Enable/disable sources, set distribution  
✅ **Attribution**: Always credits photographers + riturajprofile  
✅ **Secret key**: `riturajprofile@162` removes desktop overlay  
✅ **Local images**: Upload and use your own photos  
✅ **No code changes**: All via GUI and config files