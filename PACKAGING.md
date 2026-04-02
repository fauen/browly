# Browly Packaging Guide

This guide explains how to package Browly for distribution on macOS, Linux, and Windows.

## Quick Start

```bash
# Install PyInstaller
pip install pyinstaller

# Package for current platform
python package.py

# Or use the spec file directly
pyinstaller browly.spec
```

## Packaging Options

### 1. Using the Package Script (Recommended)

```bash
# Package for current platform
python package.py

# Clean previous builds
python package.py --clean

# Package for specific platform
python package.py --mac      # macOS only
python package.py --linux    # Linux only  
python package.py --windows  # Windows only

# Show help
python package.py --help
```

### 2. Using PyInstaller Directly

```bash
# Basic packaging
pyinstaller --onefile --windowed --name browly browly/main.py

# With UPX compression (install UPX first)
pyinstaller --onefile --windowed --upx-dir /usr/local/bin browly/main.py

# macOS .app bundle
pyinstaller --windowed --name Browly --icon=icon.icns browly.spec

# Linux
pyinstaller --onefile --windowed --name browly --icon=icon.png browly.spec

# Windows
pyinstaller --onefile --windowed --name browly --icon=icon.ico browly.spec
```

## Platform-Specific Instructions

### macOS Packaging

```bash
# 1. Install requirements
brew install pyinstaller upx

# 2. Package as .app bundle
pyinstaller --windowed --name Browly --icon=browly/assets/mac_icon.icns browly.spec

# 3. Code signing (optional but recommended)
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/Browly.app

# 4. Notarization (required for macOS Catalina+)
xcrun altool --notarize-app --primary-bundle-id "com.browly.browserpicker" --username "apple@id.com" --password "app-password" --file Browly.app.zip

# 5. Create DMG for distribution
hdiutil create -volname Browly -srcfolder dist/Browly.app -ov -format UDZO browly-macos.dmg
```

### Linux Packaging

```bash
# 1. Install requirements
sudo apt-get install pyinstaller upx

# 2. Package as single binary
pyinstaller --onefile --windowed --name browly --icon=browly/assets/linux_icon.png browly.spec

# 3. Create AppImage (optional)
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
./appimagetool-x86_64.AppImage dist/browly

# 4. Create DEB package (optional)
pip install dh-virtualenv
python setup.py --command-packages=dh_virtualenv debian
```

### Windows Packaging

```bash
# 1. Install requirements
pip install pyinstaller upx

# 2. Package as single EXE
pyinstaller --onefile --windowed --name browly --icon=browly/assets/windows_icon.ico browly.spec

# 3. Code signing (recommended)
"C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64\signtool.exe" sign /fd SHA256 /a dist\browly.exe

# 4. Create installer (optional)
# Use Inno Setup or NSIS to create an installer
```

## Distribution Formats

### 1. Standalone Executables
- **macOS**: `.app` bundle
- **Linux**: Single binary or AppImage
- **Windows**: `.exe` file

### 2. Archives
```bash
# Create zip archive
zip -r browly-macos.zip dist/Browly.app

# Create tar.gz archive
tar -czf browly-linux.tar.gz dist/browly
```

### 3. Package Managers

#### Homebrew (macOS/Linux)
```ruby
# Create a tap
brew tap yourusername/homebrew-tap

# Install formula
brew install yourusername/tap/browly
```

#### Snap (Linux)
Create a `snapcraft.yaml` file and build with `snapcraft`.

#### Flatpak (Linux)
Create a flatpak manifest and build with `flatpak-builder`.

## Code Signing (Important for Distribution)

### macOS Code Signing
```bash
# 1. Get Apple Developer certificate ($99/year)
# 2. Sign the app
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/Browly.app

# 3. Verify signing
codesign --verify --deep --strict dist/Browly.app

# 4. Notarize (required for macOS Catalina+)
xcrun altool --notarize-app --primary-bundle-id "com.browly.browserpicker" --username "apple@id.com" --password "app-password" --file Browly.app.zip
```

### Windows Code Signing
```bash
# 1. Get code signing certificate (~$200/year from DigiCert, Sectigo, etc.)
# 2. Sign the executable
signtool sign /fd SHA256 /a /tr http://timestamp.digicert.com /td SHA256 dist\browly.exe

# 3. Verify signing
signtool verify /pa dist\browly.exe
```

## Advanced Optimization

### Reducing Binary Size

```bash
# Use UPX compression
pyinstaller --upx-dir /usr/local/bin browly.spec

# Exclude unnecessary modules
pyinstaller --exclude-module tkinter --exclude-module test browly.spec

# Strip binaries (Linux/macOS)
strip dist/browly
```

### Hidden Imports

If you get module not found errors, add them to the spec file:

```python
a = Analysis(
    ['browly/main.py'],
    pathex=['.'],
    hiddenimports=['pkg_resources.py2_warn'],  # Add missing imports here
    ...
)
```

### Runtime Hooks

Create runtime hooks for special initialization:

```python
# Create hook.py
def hook():
    # Your initialization code here
    pass

# Add to spec file
runtime_hooks=['hook.py']
```

## Troubleshooting

### Common Issues

**1. "No module named PySide6"**
- Solution: `pip install PySide6` in your virtual environment

**2. Large binary size**
- Solution: Use UPX compression and exclude unnecessary modules

**3. App not opening on macOS**
- Solution: Check Gatekeeper settings or right-click → Open

**4. Black window on Linux**
- Solution: Install Qt dependencies: `sudo apt-get install libxcb-xinerama0`

**5. Antivirus blocking on Windows**
- Solution: Code sign the executable

### Debugging

```bash
# Run with console to see errors
pyinstaller --console browly.spec

# Check imported modules
pyi-makespec --onefile browly/main.py

# Analyze the binary
pyinstaller --debug all browly.spec
```

## Continuous Integration

Example GitHub Actions workflow for automatic packaging:

```yaml
name: Build and Package

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [macos-latest, ubuntu-latest, windows-latest]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pyinstaller PySide6
    
    - name: Build with PyInstaller
      run: |
        pyinstaller --onefile --windowed --name browly browly.spec
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v2
      with:
        name: browly-${{ matrix.os }}
        path: dist/
```

## Distribution Checklist

- [ ] Test on all target platforms
- [ ] Code sign executables
- [ ] Create archives (zip/tar.gz)
- [ ] Update version in pyproject.toml
- [ ] Update README with installation instructions
- [ ] Create GitHub release with binaries
- [ ] Update homepage/download links
- [ ] Announce new version

## Alternative Packaging Methods

### 1. cx_Freeze
```bash
pip install cx_Freeze
cxfreeze browly/main.py --target-dir dist
```

### 2. Nuitka (Compiles to native code)
```bash
pip install nuitka
nuitka --onefile --windowed browly/main.py
```

### 3. Briefcase (for GUI apps)
```bash
pip install briefcase
briefcase create
briefcase build
briefcase package
```

## Final Notes

- **Always test your packaged app** on a clean system
- **Code signing is highly recommended** for distribution
- **Consider using UPX** for smaller binaries
- **Document installation instructions** for users
- **Provide multiple download options** (direct, package managers, etc.)

The packaging script provided (`package.py`) handles most of these steps automatically and creates optimized, platform-specific builds ready for distribution.