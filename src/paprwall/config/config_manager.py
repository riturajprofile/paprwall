"""
Configuration manager for paprwall (Picsum-only, simplified).

This version removes API key and multi-source management. It keeps only:
- preferences.json: general app preferences
- attribution.json: overlay configuration
"""
import json
import os
from pathlib import Path
from typing import Any, Dict
from paprwall import CONFIG_DIR

# Built-in defaults (no external imports required)
DEFAULT_PREFERENCES: Dict[str, Any] = {
    # Rotation frequency (minutes)
    "rotation_interval_minutes": 60,
    # How many images to fetch per fetch run
    "images_per_day": 1,
    # Time of the day to auto-fetch (HH:MM), optional feature
    "auto_fetch_time": "08:00",
    # Whether to delete old images automatically
    "auto_delete_old": True,
    # Keep images for N days
    "keep_days": 7,
    # Optional: local images folder (used by local mode if ever enabled)
    "local_folder": str(Path('~/Pictures/Wallpapers').expanduser()),
}

DEFAULT_ATTRIBUTION: Dict[str, Any] = {
    # Show overlay text on wallpapers
    "overlay_enabled": True,
    # Overlay position: bottom-right, bottom-left, top-right, top-left
    "position": "bottom-right",
    # Background box opacity (0..1)
    "opacity": 0.7,
}


class ConfigManager:
    """Manages simplified configuration files (preferences + attribution)."""

    def __init__(self):
        self.config_dir = CONFIG_DIR
        self.attribution_file = self.config_dir / "attribution.json"
        self.preferences_file = self.config_dir / "preferences.json"

        # Load .env file if present (kept for future extensibility)
        self._load_env_file()

        # Initialize config files if they don't exist
        self._initialize_configs()
    
    def _load_env_file(self):
        """Load environment variables from .env file"""
        env_paths = [
            Path.cwd() / '.env',  # Current directory
            Path.home() / '.env',  # Home directory
            self.config_dir / '.env',  # Config directory
        ]
        
        for env_path in env_paths:
            if env_path.exists():
                self._parse_env_file(env_path)
                break
    
    def _parse_env_file(self, env_path: Path):
        """Parse .env file and set environment variables"""
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse KEY=VALUE
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        
                        # Set environment variable if not already set
                        if key and value and not os.getenv(key):
                            os.environ[key] = value
        except Exception as e:
            # Silently fail if .env parsing fails
            pass
    
    def _initialize_configs(self):
        """Create default config files if they don't exist"""
        if not self.attribution_file.exists():
            self._save_json(self.attribution_file, DEFAULT_ATTRIBUTION)

        if not self.preferences_file.exists():
            self._save_json(self.preferences_file, DEFAULT_PREFERENCES)
    
    def _load_json(self, file_path: Path) -> Dict:
        """Load JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _save_json(self, file_path: Path, data: Dict):
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    # Simplified API (no keys/sources management in Picsum-only mode)
    # Attribution methods
    def get_attribution_config(self) -> Dict[str, Any]:
        """Get attribution configuration"""
        return self._load_json(self.attribution_file)
    
    def set_attribution_config(self, config: Dict[str, Any]):
        """Set attribution configuration"""
        self._save_json(self.attribution_file, config)
    
    # Preferences methods
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a preference value"""
        prefs = self._load_json(self.preferences_file)
        return prefs.get(key, default if default is not None else DEFAULT_PREFERENCES.get(key))
    
    def set_preference(self, key: str, value: Any):
        """Set a preference value"""
        prefs = self._load_json(self.preferences_file)
        prefs[key] = value
        self._save_json(self.preferences_file, prefs)
    
    def get_all_preferences(self) -> Dict[str, Any]:
        """Get all preferences"""
        return self._load_json(self.preferences_file)
    
    def get_local_folder(self) -> str:
        """Get local images folder path"""
        folder = self.get_preference('local_folder', str(Path('~/Pictures/Wallpapers').expanduser()))
        return str(Path(folder).expanduser())
