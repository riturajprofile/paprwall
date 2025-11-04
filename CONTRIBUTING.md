# Contributing to PaprWall 🎨

Thank you for your interest in contributing to PaprWall! This guide will help you get started with development and explain our contribution process.

## 🚀 Quick Start

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/paprwall.git
   cd paprwall
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows

   # Install development dependencies
   pip install --upgrade pip setuptools wheel
   pip install -e ".[dev]"
   ```

3. **Install System Dependencies**
   ```bash
   # Linux (Ubuntu/Debian)
   sudo apt install python3-tk python3-dev

   # Linux (Fedora)
   sudo dnf install python3-tkinter python3-devel

   # Linux (Arch)
   sudo pacman -S tk

   # Windows - Tkinter included with Python
   # macOS - Tkinter included with Python
   ```

4. **Verify Installation**
   ```bash
   python -m pytest tests/
   python -m paprwall.cli --version
   paprwall-gui  # Should launch the GUI
   ```

## 🏗️ Project Structure

```
paprwall/
├── src/
│   └── paprwall/
│       ├── __init__.py          # Package initialization
│       ├── __version__.py       # Version information
│       ├── cli.py               # Command-line interface
│       ├── core.py              # Core functionality
│       ├── installer.py         # System integration
│       └── gui/
│           ├── __init__.py      # GUI module
│           └── wallpaper_manager_gui.py  # Main GUI application
├── tests/
│   ├── __init__.py              # Test configuration
│   ├── test_core.py             # Core functionality tests
│   └── test_cli.py              # CLI tests
├── scripts/
│   ├── build_linux.sh           # Linux build script
│   ├── build_windows.bat        # Windows build script
│   └── paprwall.spec            # PyInstaller spec
├── .github/
│   └── workflows/               # CI/CD workflows
├── pyproject.toml               # Modern Python packaging
├── requirements.txt             # Runtime dependencies
└── README.md                    # Project documentation
```

## 🧪 Development Workflow

### 1. Code Style

We use several tools to maintain code quality:

```bash
# Format code
black src/ tests/

# Check imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/paprwall --ignore-missing-imports
```

### 2. Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_core.py -v

# Run with coverage
python -m pytest tests/ --cov=paprwall --cov-report=html

# GUI testing (Linux - requires X server)
xvfb-run -a python -m pytest tests/ -v
```

### 3. Building

```bash
# Build wheel package
python -m build

# Build executable (Linux)
chmod +x scripts/build_linux.sh
./scripts/build_linux.sh

# Build executable (Windows)
scripts\build_windows.bat
```

## 📋 Contribution Guidelines

### Issue Reporting

1. **Search First**: Check existing issues before creating new ones
2. **Use Templates**: Use our bug report or feature request templates
3. **Be Specific**: Provide detailed reproduction steps and environment info
4. **Add Labels**: Help us categorize with appropriate labels

### Pull Requests

1. **Branch from main**: Create feature branches from the latest main
2. **Descriptive Names**: Use clear branch names like `feature/quote-categories` or `fix/wallpaper-scaling`
3. **Small Changes**: Keep PRs focused on a single feature or bug fix
4. **Tests Required**: Add tests for new functionality
5. **Documentation**: Update README or docs if needed

### Commit Messages

Follow conventional commits format:

```
type(scope): description

Examples:
feat(gui): add dark theme toggle
fix(core): resolve quote fetching timeout
docs(readme): update installation instructions
test(cli): add version command tests
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `style`, `chore`

## 🎯 Development Focus Areas

### High Priority
- 🐧 **Linux Desktop Environments**: GNOME, KDE, XFCE support
- 🖼️ **Wallpaper Sources**: Additional image APIs and sources
- 💭 **Quote System**: More categories and custom quotes
- 🔄 **Auto-rotation**: Smart scheduling and conditions

### Medium Priority
- 🪟 **Windows Integration**: Better Windows desktop integration
- 📱 **Multi-monitor**: Support for multiple displays
- 🎨 **Theming**: Custom color schemes and fonts
- ⚙️ **Settings**: Configuration UI and persistence

### Future Ideas
- 🍎 **macOS Support**: Native macOS wallpaper setting
- 🌐 **Cloud Sync**: Sync favorites across devices
- 📊 **Analytics**: Usage statistics and preferences
- 🔌 **Plugins**: Extensible architecture

## 🔧 Technical Guidelines

### Code Standards

- **Python 3.8+**