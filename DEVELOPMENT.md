# Browly Development Guide

This guide helps developers understand the codebase structure and contribute to Browly.

## 🗺️ Codebase Structure

```
browly/
├── browly/                  # Main Python package
│   ├── __init__.py         # Package initialization
│   ├── browsers.py         # Browser detection and management
│   └── main.py            # Qt GUI application
├── package.py              # Packaging script
├── pyproject.toml           # Python project configuration
├── README.md               # User documentation
├── PACKAGING.md             # Packaging instructions
├── DEVELOPMENT.md           # This file
└── .gitignore              # Git ignore rules
```

## 🚀 Getting Started with Development

### Prerequisites

- Python 3.8+
- PySide6 (Qt for Python)
- PyInstaller (for packaging)
- Virtual environment (recommended)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/dbackman/browly.git
cd browly

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Install dependencies
pip install PySide6 pyinstaller

# Install in development mode
pip install -e .
```

## 🔧 Architecture Overview

### Browser Detection (`browly/browsers.py`)

```python
class Browser:
    # Represents a browser with name, path, and arguments
    
class BrowserDetector:
    # Detects available browsers on the system
    # Handles configuration file I/O
    # Provides platform-specific browser lists
```

**Key Methods:**
- `detect_browsers()` - Find available browsers
- `create_example_config()` - Generate config file
- `_load_config()` / `_save_config()` - Config management

### GUI Application (`browly/main.py`)

```python
class BrowlyMainWindow(QMainWindow):
    # Main application window
    
class AddBrowserDialog(QDialog):
    # Dialog for adding custom browsers
```

**Key Components:**
- `QListWidget` - Browser list display
- `QPushButton` - Action buttons
- `QDialog` - Custom browser addition
- `QMessageBox` - User notifications

### Packaging (`package.py`)

**Key Features:**
- Platform detection
- Spec file generation
- Build management
- Archive creation

## 🛠️ Development Workflow

### 1. Implementing New Features

```bash
# 1. Create a new branch
git checkout -b feature/your-feature

# 2. Make your changes
# Edit the appropriate files

# 3. Test your changes
python -m browly.main

# 4. Run packaging tests
python package.py --clean
python package.py

# 5. Commit your changes
git add .
git commit -m "Add your feature"

# 6. Push and create PR
git push origin feature/your-feature
```

### 2. Debugging

```bash
# Run with console output
python -m browly.main --debug

# Check PyInstaller warnings
cat build/browly/warn-browly.txt

# Analyze dependencies
pyi-makespec --onefile browly/main.py
```

### 3. Testing

**Manual Testing:**
- Test on all supported platforms
- Test browser detection
- Test custom browser addition
- Test URL opening
- Test command line arguments

**Automated Testing (Future):**
```bash
# Run tests (to be implemented)
python -m pytest tests/
```

## 🎨 Common Development Tasks

### Adding a New Browser

1. **Update default browsers** in `browsers.py`:

```python
def _get_default_browsers(self) -> List[Browser]:
    if sys.platform == "darwin":
        return [
            # ... existing browsers
            Browser("Brave", "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"),
        ]
```

2. **Add browser icon** (future enhancement)

### Adding a New Feature

1. **Add GUI elements** in `main.py`
2. **Add logic** in appropriate class
3. **Update documentation** in README.md
4. **Test thoroughly**

### Adding Platform Support

1. **Add platform detection** in `browsers.py`:

```python
elif sys.platform == "your_platform":
    return [
        Browser("Platform Browser", "platform-browser"),
    ]
```

2. **Test on target platform**

## 📦 Packaging for Development

```bash
# Test packaging during development
python package.py --clean
python package.py

# Test the packaged app
open dist/Browly.app  # macOS
./dist/browly/browly  # Linux (onedir mode)
dist\browly.exe      # Windows
```

## 🔧 Technical Details

### Qt GUI Framework

- **PySide6** is used instead of PyQt for more permissive licensing
- **Qt Designer** can be used to create `.ui` files (future enhancement)
- **Signal/Slot** pattern for event handling

### Configuration Management

- **JSON format** for config files
- **Platform-specific paths** for config storage
- **Automatic fallback** to defaults if config missing

### Browser Detection

- **Absolute paths** for macOS `.app` bundles
- **Command lookup** for Linux/Windows browsers
- **Availability checking** before listing browsers

## 🎯 Future Development Ideas

### High Priority
- [ ] Add browser icons
- [ ] Implement browser favorites/priority
- [ ] Add recent URLs history
- [ ] System tray integration
- [ ] Better error handling

### Medium Priority
- [ ] Dark mode support
- [ ] Browser profile management
- [ ] Multiple URL opening
- [ ] Drag and drop URL support
- [ ] Browser health checks

### Low Priority
- [ ] Themes and customization
- [ ] Plugin system
- [ ] Cloud sync for config
- [ ] Statistics and analytics
- [ ] Advanced search/filter

## 📚 Resources

### Qt/PySide6 Resources
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [Qt for Python Tutorials](https://www.qt.io/qt-for-python)
- [PySide6 Examples](https://github.com/qt/qtbase/tree/dev/examples/python)

### PyInstaller Resources
- [PyInstaller Documentation](https://pyinstaller.org/en/stable/)
- [PyInstaller Hooks](https://pyinstaller.org/en/stable/hooks.html)
- [PyInstaller Recipes](https://github.com/pyinstaller/pyinstaller/wiki/Recipe)

### Packaging Resources
- [Python Packaging Guide](https://packaging.python.org/)
- [macOS Code Signing](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)
- [Windows Code Signing](https://docs.microsoft.com/en-us/windows/win32/seccrypto/signtool)

## 🤝 Contributing Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use type hints where appropriate
- Write docstrings for public methods
- Keep functions small and focused

### Commit Messages
- Use imperative mood ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Add detailed explanation in body if needed
- Reference issues when applicable

### Pull Requests
- Create PR from feature branch
- Include tests if applicable
- Update documentation
- Keep PRs focused on single feature/bugfix
- Be responsive to feedback

## 🚨 Troubleshooting

### Common Issues

**Qt not found:**
```bash
pip install PySide6
```

**PyInstaller not finding modules:**
```bash
# Add hidden imports to spec file
hiddenimports=['missing_module']
```

**Black window on Linux:**
```bash
sudo apt-get install libxcb-xinerama0
```

**macOS Gatekeeper issues:**
```bash
# Right-click → Open (first time only)
# Or: xattr -d com.apple.quarantine Browly.app
```

## 📈 Project Roadmap

### Short Term (1-3 months)
- Complete current feature set
- Stabilize packaging
- Add basic tests
- Improve documentation

### Medium Term (3-6 months)
- Add system tray support
- Implement browser profiles
- Add dark mode
- Create installers

### Long Term (6-12 months)
- Plugin system
- Cloud sync
- Advanced analytics
- Cross-device sync

## 🎓 Learning Resources

### Python GUI Development
- [Real Python: PySide6 Tutorial](https://realpython.com/pyside6-python/)
- [ZetCode: PySide6 Tutorial](http://zetcode.com/pyside6/)

### Packaging
- [PyInstaller Tutorial](https://realpython.com/pyinstaller-python/)
- [Python Packaging Guide](https://packaging.python.org/tutorials/packaging-projects/)

### Qt Design
- [Qt Designer Manual](https://doc.qt.io/qt-6/qtdesigner-manual.html)
- [Qt Stylesheets](https://doc.qt.io/qt-6/stylesheet-reference.html)

This development guide should help you and future contributors understand the codebase structure, development workflow, and best practices for extending Browly!