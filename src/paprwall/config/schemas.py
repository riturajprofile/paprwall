"""
Configuration schemas and validation.
"""
from typing import Dict, Any


def validate_api_keys(config: Dict[str, Any]) -> bool:
    """Validate API keys configuration"""
    required_sources = ['pixabay', 'unsplash', 'pexels']
    
    for source in required_sources:
        if source not in config:
            return False
        
        if source == 'unsplash':
            if 'access_key' not in config[source]:
                return False
        else:
            if 'api_key' not in config[source]:
                return False
    
    return True


def validate_sources(config: Dict[str, Any]) -> bool:
    """Validate sources configuration"""
    if 'enabled' not in config or not isinstance(config['enabled'], list):
        return False
    
    if 'weights' not in config or not isinstance(config['weights'], dict):
        return False
    
    return True


def validate_preferences(config: Dict[str, Any]) -> bool:
    """Validate preferences configuration"""
    required_keys = [
        'rotation_interval_minutes',
        'images_per_day',
        'auto_fetch_time'
    ]
    
    for key in required_keys:
        if key not in config:
            return False
    
    return True
