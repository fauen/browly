# Browly - Python GUI Browser Picker

## What's Being Committed

This commit transforms Browly from a Go CLI tool to a **Python GUI application** with comprehensive packaging support.

### 📁 New Files Added

1. **`browly/`** - Main Python package
   - `browsers.py` - Browser detection and configuration
   - `main.py` - Qt GUI application with PySide6

2. **`package.py`** - Comprehensive packaging script
   - Platform detection (macOS, Linux, Windows)
   - PyInstaller spec file generation
   - Clean/build management
   - Archive creation

3. **`PACKAGING.md`** - Complete packaging guide
   - Quick start instructions
   - Platform-specific guides
   - Code signing instructions
   - CI/CD examples

4. **`pyproject.toml`** - Python project configuration
   - PySide6 dependency
   - Package metadata

5. **`.gitignore`** - Proper ignore rules
   - Python cache files
   - Virtual environments
   - Build artifacts
   - Config files

### 📝 Modified Files

1. **`README.md`** - Updated for GUI version
   - New features and screenshots
   - Installation instructions
   - Usage examples
   - Configuration guide
   - Platform-specific setup

### 🚀 Key Features

- **Graphical Interface**: Qt-based GUI with PySide6
- **Cross-platform**: macOS, Linux (Fedora), Windows support
- **Browser Detection**: Automatic discovery of installed browsers
- **Custom Browsers**: Add your own browsers via GUI
- **Configuration**: JSON config file support
- **URL Handling**: Open URLs from command line or GUI
- **Packaging Ready**: PyInstaller spec files and scripts

### 🎯 Usage

```bash
# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install PySide6 pyinstaller

# Run directly
python -m browly.main https://example.com

# Create example config
python -m browly.main --init

# Package for distribution
python package.py
```

### 📦 Packaging

The project includes comprehensive packaging support:

```bash
# Clean and package
python package.py --clean
python package.py

# Platform-specific
python package.py --mac      # macOS
python package.py --linux    # Linux
python package.py --windows  # Windows
```

### 🔧 Technical Details

- **Language**: Python 3.8+
- **GUI Framework**: PySide6 (Qt for Python)
- **Packaging**: PyInstaller
- **Config Format**: JSON
- **Platform Support**: macOS, Linux, Windows

### 🎨 Next Steps

1. **Add icons** for better branding
2. **Code sign** for official distribution
3. **Create installers** for each platform
4. **Set up CI/CD** for automated builds
5. **Publish** to package managers (Homebrew, PyPI, etc.)

The application is fully functional and ready for testing and distribution!