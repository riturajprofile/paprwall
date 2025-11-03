"""
Default API keys and configuration for paprwall.
Users can override these in ~/.config/paprwall/api_keys.json

SECURITY NOTE: This file contains placeholder keys for demonstration.
Users MUST add their own API keys in the config file to use the app.
Get free API keys from:
- Pixabay: https://pixabay.com/api/docs/
- Unsplash: https://unsplash.com/developers
- Pexels: https://www.pexels.com/api/
"""
import hashlib

# Default API keys - PLACEHOLDERS ONLY!
# Users must provide their own keys in ~/.config/paprwall/api_keys.json
DEFAULT_API_KEYS = {
    "pixabay": {
        "api_key": "YOUR_PIXABAY_API_KEY_HERE",  # Get from: https://pixabay.com/api/docs/
        "attribution_required": True
    },
    "unsplash": {
        "access_key": "YOUR_UNSPLASH_ACCESS_KEY_HERE",  # Get from: https://unsplash.com/developers
        "attribution_required": True
    },
    "pexels": {
        "api_key": "YOUR_PEXELS_API_KEY_HERE",  # Get from: https://www.pexels.com/api/
        "attribution_required": True
    }
}

# Default source configuration
DEFAULT_SOURCES = {
    "enabled": ["pixabay", "pexels"],
    "weights": {
        "pixabay": 50,
        "unsplash": 0,
        "pexels": 50,
        "local": 0
    },
    "preferences": {
        "pixabay": {
            "enabled": True,
            "categories": ["nature", "landscape"],
            "safe_search": True,
            "theme": "nature"  # Options: nature, landscape, city, abstract, minimal, animals, space, ocean, mountains, sunset
        },
        "unsplash": {
            "enabled": True,
            "collections": [],
            "orientation": "landscape",
            "theme": "nature"  # Custom search query
        },
        "pexels": {
            "enabled": True,
            "query": "nature landscape",
            "orientation": "landscape",
            "theme": "nature"  # Custom search query
        },
        "local": {
            "enabled": False,
            "folder": "~/Pictures/Wallpapers"
        }
    }
}

# Default attribution settings
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
ATTRIBUTION_SECRET_HASH = hashlib.sha256(ATTRIBUTION_SECRET_KEY.encode()).hexdigest()

# Default general preferences
DEFAULT_PREFERENCES = {
    "rotation_interval_minutes": 30,
    "images_per_day": 5,
    "auto_fetch_time": "09:00",
    "image_quality": "high",
    "cache_size_mb": 500,
    "auto_delete_old": True,
    "keep_days": 7,
    "theme": "nature",  # Global theme preference
    "custom_query": ""  # Custom search query for all sources
}

# Available themes/categories
AVAILABLE_THEMES = {
    "nature": {
        "pixabay_categories": ["nature", "landscape"],
        "search_queries": ["nature", "landscape", "scenery"],
        "description": "Natural landscapes and outdoor scenes"
    },
    "city": {
        "pixabay_categories": ["places", "buildings"],
        "search_queries": ["city", "urban", "architecture", "skyline"],
        "description": "Urban landscapes and cityscapes"
    },
    "minimal": {
        "pixabay_categories": ["backgrounds"],
        "search_queries": ["minimal", "abstract", "simple", "clean"],
        "description": "Minimalist and clean designs"
    },
    "space": {
        "pixabay_categories": ["science", "nature"],
        "search_queries": ["space", "galaxy", "nebula", "stars", "cosmos"],
        "description": "Space and astronomy"
    },
    "ocean": {
        "pixabay_categories": ["nature"],
        "search_queries": ["ocean", "sea", "beach", "waves", "water"],
        "description": "Ocean and coastal scenes"
    },
    "mountains": {
        "pixabay_categories": ["nature", "landscape"],
        "search_queries": ["mountains", "peaks", "alpine", "summit"],
        "description": "Mountain landscapes"
    },
    "sunset": {
        "pixabay_categories": ["nature"],
        "search_queries": ["sunset", "sunrise", "dusk", "dawn", "golden hour"],
        "description": "Sunset and sunrise scenes"
    },
    "animals": {
        "pixabay_categories": ["animals"],
        "search_queries": ["animals", "wildlife", "nature", "fauna"],
        "description": "Wildlife and animals"
    },
    "forest": {
        "pixabay_categories": ["nature"],
        "search_queries": ["forest", "trees", "woods", "jungle"],
        "description": "Forest and woodland scenes"
    },
    "abstract": {
        "pixabay_categories": ["backgrounds"],
        "search_queries": ["abstract", "pattern", "texture", "art"],
        "description": "Abstract art and patterns"
    },
    "flowers": {
        "pixabay_categories": ["nature"],
        "search_queries": ["flowers", "floral", "botanical", "garden"],
        "description": "Flowers and botanical scenes"
    },
    "dark": {
        "pixabay_categories": ["backgrounds"],
        "search_queries": ["dark", "night", "black", "moody"],
        "description": "Dark and moody wallpapers"
    }
}
