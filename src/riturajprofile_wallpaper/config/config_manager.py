"""
Configuration manager for riturajprofile-wallpaper.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from riturajprofile_wallpaper import CONFIG_DIR
from riturajprofile_wallpaper.config.default_keys import (
    DEFAULT_API_KEYS,
    DEFAULT_SOURCES,
    DEFAULT_ATTRIBUTION,
    DEFAULT_PREFERENCES
)


class ConfigManager:
    """Manages all configuration files"""
    
    def __init__(self):
        self.config_dir = CONFIG_DIR
        self.api_keys_file = self.config_dir / "api_keys.json"
        self.sources_file = self.config_dir / "sources.json"
        self.attribution_file = self.config_dir / "attribution.json"
        self.preferences_file = self.config_dir / "preferences.json"
        
        # Load .env file if present
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
        if not self.api_keys_file.exists():
            self._save_json(self.api_keys_file, DEFAULT_API_KEYS)
        
        if not self.sources_file.exists():
            self._save_json(self.sources_file, DEFAULT_SOURCES)
        
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
    
    # API Keys methods
    def get_api_key(self, source: str) -> str:
        """Get API key for a source
        
        Priority order:
        1. Environment variables (.env or system)
        2. User config file (api_keys.json)
        3. Default keys (placeholders)
        """
        # Check environment variables first
        env_key = None
        if source == 'pixabay':
            env_key = os.getenv('PIXABAY_API_KEY')
        elif source == 'unsplash':
            env_key = os.getenv('UNSPLASH_ACCESS_KEY')
        elif source == 'pexels':
            env_key = os.getenv('PEXELS_API_KEY')
        
        if env_key and env_key != 'YOUR_' + source.upper() + '_API_KEY_HERE':
            return env_key
        
        # Check user config file
        keys = self._load_json(self.api_keys_file)
        source_config = keys.get(source, {})
        
        # Return custom key or default key
        if source == 'pixabay':
            return source_config.get('api_key', DEFAULT_API_KEYS['pixabay']['api_key'])
        elif source == 'unsplash':
            return source_config.get('access_key', DEFAULT_API_KEYS['unsplash']['access_key'])
        elif source == 'pexels':
            return source_config.get('api_key', DEFAULT_API_KEYS['pexels']['api_key'])
        
        return ""
    
    def set_api_key(self, source: str, key: str):
        """Set custom API key for a source"""
        keys = self._load_json(self.api_keys_file)
        
        if source not in keys:
            keys[source] = {}
        
        if source == 'unsplash':
            keys[source]['access_key'] = key
        else:
            keys[source]['api_key'] = key
        
        self._save_json(self.api_keys_file, keys)
    
    # Sources methods
    def get_enabled_sources(self) -> List[str]:
        """Get list of enabled sources"""
        sources = self._load_json(self.sources_file)
        return sources.get('enabled', DEFAULT_SOURCES['enabled'])
    
    def set_enabled_sources(self, sources: List[str]):
        """Set enabled sources"""
        config = self._load_json(self.sources_file)
        config['enabled'] = sources
        self._save_json(self.sources_file, config)
    
    def get_source_weights(self) -> Dict[str, int]:
        """Get source weights for distribution"""
        sources = self._load_json(self.sources_file)
        return sources.get('weights', DEFAULT_SOURCES['weights'])
    
    def set_source_weights(self, weights: Dict[str, int]):
        """Set source weights"""
        config = self._load_json(self.sources_file)
        config['weights'] = weights
        self._save_json(self.sources_file, config)
    
    def get_source_preferences(self, source: str) -> Dict[str, Any]:
        """Get preferences for a specific source"""
        sources = self._load_json(self.sources_file)
        prefs = sources.get('preferences', DEFAULT_SOURCES['preferences'])
        return prefs.get(source, {})
    
    def set_source_preferences(self, source: str, preferences: Dict[str, Any]):
        """Set preferences for a specific source"""
        config = self._load_json(self.sources_file)
        if 'preferences' not in config:
            config['preferences'] = {}
        config['preferences'][source] = preferences
        self._save_json(self.sources_file, config)
    
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
        prefs = self.get_source_preferences('local')
        folder = prefs.get('folder', '~/Pictures/Wallpapers')
        return str(Path(folder).expanduser())
