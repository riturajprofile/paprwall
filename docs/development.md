# Development Guide

## Setting Up Development Environment

### Clone and Install

```bash
# Clone repository
git clone https://github.com/riturajprofile/wallpaper-app.git
cd wallpaper-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### Development Dependencies

Create `requirements-dev.txt`:

```txt
pytest>=7.0.0
pytest-cov>=4.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
isort>=5.12.0
```

## Project Structure

```
riturajprofile-wallpaper/
├── src/riturajprofile_wallpaper/
│   ├── api/              # API clients
│   ├── config/           # Configuration management
│   ├── core/             # Core functionality
│   ├── gui/              # GTK GUI
│   ├── service/          # Background service
│   └── utils/            # Utilities
├── tests/                # Test suite
├── docs/                 # Documentation
└── systemd/              # System service files
```

## Code Style

### Format Code

```bash
# Format with black
black src/

# Sort imports
isort src/

# Lint with flake8
flake8 src/
```

### Type Checking

```bash
mypy src/riturajprofile_wallpaper/
```

## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=riturajprofile_wallpaper

# Run specific test
pytest tests/test_api/test_pixabay.py
```

### Writing Tests

Create tests in `tests/` directory:

```python
# tests/test_core/test_rotator.py
import pytest
from riturajprofile_wallpaper.core.rotator import WallpaperRotator

def test_rotator_initialization():
    rotator = WallpaperRotator(config_manager)
    assert rotator is not None
```

## Building Package

### Build Distribution

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check distribution
twine check dist/*
```

### Test Installation

```bash
# Install from local build
pip install dist/riturajprofile_wallpaper-1.0.0-py3-none-any.whl

# Test commands
riturajprofile-wallpaper --version
```

## Making Changes

### Workflow

1. Create a new branch
2. Make your changes
3. Write/update tests
4. Format code
5. Run tests
6. Commit and push
7. Create pull request

### Commit Messages

Follow conventional commits:

```
feat: Add support for new image source
fix: Fix wallpaper setting on KDE
docs: Update installation guide
test: Add tests for attribution manager
```

## API Key Testing

For development, you can use test API keys or add your own in:

```
~/.config/riturajprofile-wallpaper/api_keys.json
```

## Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Logs

```bash
tail -f ~/.local/share/riturajprofile-wallpaper/logs/app.log
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create git tag
4. Build distribution
5. Upload to PyPI

```bash
# Tag release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Build and upload
python -m build
twine upload dist/*
```
