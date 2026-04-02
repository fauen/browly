# Browly - Cross-Platform Browser Picker with GUI

A graphical browser picker that lets you choose which browser to use for opening links on macOS, Linux, and Windows.

## Features

- ✅ **Graphical Interface** - Easy browser selection with GUI
- ✅ **Cross-platform** - Works on macOS, Linux (Fedora), and Windows
- ✅ **Custom Browsers** - Add your own browsers with custom arguments
- ✅ **Configuration** - Save your browser preferences
- ✅ **URL Handling** - Open URLs from command line or GUI
- ✅ **Browser Detection** - Automatically finds installed browsers

## Screenshots

![Browly Main Window](https://via.placeholder.com/400x300?text=Browly+Browser+Picker)

## Installation

### Prerequisites

- Python 3.8+
- PySide6 (Qt for Python)

### Install with pip

```bash
pip install browly
```

### Install from source

```bash
git clone https://github.com/dbackman/browly.git
cd browly
pip install .
```

### Run directly

```bash
python -m browly.main
```

## Usage

### Command Line

```bash
# Open URL with browser picker
browly https://example.com

# Just launch the browser picker
browly
```

### GUI Features

- **Refresh**: Scan for available browsers again
- **Add Browser**: Add custom browsers with paths and arguments
- **Double-click**: Open URL with selected browser
- **Open Button**: Open URL with selected browser

## Configuration

Browly saves your custom browsers in a configuration file:

- **Linux/macOS**: `~/.config/browly/config.json`
- **Windows**: `%APPDATA%\browly\config.json`

### Example Config

```json
{
  "browsers": [
    {
      "name": "Google Chrome",
      "path": "google-chrome",
      "args": ["--new-window"]
    },
    {
      "name": "Firefox",
      "path": "firefox",
      "args": ["--new-window"]
    },
    {
      "name": "Custom Browser",
      "path": "/path/to/your/browser",
      "args": ["--custom-flag"]
    }
  ]
}
```

### Create Example Config

```bash
# Create an example config file
browly --init
```

## Setting as Default Browser

### macOS

To set Browly as your default browser on macOS:

1. **Create an AppleScript app**:
   ```applescript
   -- Save as Browly.app
   on open location this_URL
       do shell script "browly '" & this_URL & "'"
   end open location
   ```

2. **Set as default browser**:
   ```bash
   # Install duti
   brew install duti
   
   # Set Browly as default for http/https
   duti -s com.your.browly http
   duti -s com.your.browly https
   ```

### Linux (Fedora)

1. **Create a .desktop file** (`~/.local/share/applications/browly.desktop`):
   ```ini
   [Desktop Entry]
   Name=Browly Browser Picker
   Exec=browly %u
   Terminal=false
   Type=Application
   MimeType=x-scheme-handler/http;x-scheme-handler/https;
   ```

2. **Set as default**:
   ```bash
   xdg-mime default browly.desktop x-scheme-handler/http
   xdg-mime default browly.desktop x-scheme-handler/https
   ```

### Windows

1. **Create a registry entry** to associate Browly with HTTP/HTTPS protocols
2. **Use the GUI approach** with a custom URL handler

## Supported Browsers

### macOS
- Safari
- Google Chrome
- Firefox
- Microsoft Edge

### Linux
- Google Chrome / Chromium
- Firefox
- Microsoft Edge

### Windows
- Google Chrome
- Microsoft Edge
- Firefox
- Internet Explorer

## Development

```bash
# Install dependencies
pip install poetry
poetry install

# Run in development mode
poetry run python -m browly.main

# Build package
poetry build
```

## Roadmap

- [x] GUI browser picker
- [x] Custom browser configuration
- [x] Cross-platform support
- [x] URL handling from command line
- [ ] Browser icons
- [ ] Browser priority/favorites
- [ ] Recent URLs history
- [ ] System tray integration
- [ ] Better default browser integration

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open issues and pull requests on GitHub.

## Alternative Approach: CLI with GUI Launcher

If you want a simpler approach that doesn't require setting Browly as the default browser:

1. **Install Browly** as shown above
2. **Use it manually** when you want to pick a browser: `browly https://example.com`
3. **Create keyboard shortcuts** to launch Browly quickly

This gives you browser selection without the complexity of default browser integration.