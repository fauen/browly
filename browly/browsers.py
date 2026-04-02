import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class Browser:
    def __init__(self, name: str, path: str, args: List[str] = None):
        self.name = name
        self.path = path
        self.args = args or []

    def is_available(self) -> bool:
        """Check if browser is available on the system."""
        try:
            # For absolute paths, check if file exists
            if os.path.isabs(self.path):
                return os.path.exists(self.path) and os.access(self.path, os.X_OK)
            # For command-line browsers, check if in PATH
            return subprocess.run(
                ["which", self.path], 
                capture_output=True, 
                text=True
            ).returncode == 0
        except Exception:
            return False

    def open(self, url: str) -> bool:
        """Open URL in this browser."""
        try:
            cmd = [self.path] + self.args + [url]
            subprocess.Popen(cmd)
            return True
        except Exception as e:
            print(f"Error opening {self.name}: {e}")
            return False


class BrowserDetector:
    def __init__(self):
        self.config_path = self._get_config_path()

    def _get_config_path(self) -> str:
        """Get path to config file."""
        if sys.platform == "win32":
            config_dir = os.environ.get("APPDATA", os.path.expanduser("~"))
        else:
            config_dir = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        return os.path.join(config_dir, "browly", "config.json")

    def _get_default_browsers(self) -> List[Browser]:
        """Get platform-specific default browsers."""
        if sys.platform == "darwin":  # macOS
            return [
                Browser("Safari", "/Applications/Safari.app/Contents/MacOS/Safari"),
                Browser("Google Chrome", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", ["--new-window"]),
                Browser("Firefox", "/Applications/Firefox.app/Contents/MacOS/firefox", ["--new-window"]),
                Browser("Microsoft Edge", "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge", ["--new-window"]),
            ]
        elif sys.platform.startswith("linux"):  # Linux
            return [
                Browser("Google Chrome", "google-chrome", ["--new-window"]),
                Browser("Chromium", "chromium", ["--new-window"]),
                Browser("Firefox", "firefox", ["--new-window"]),
                Browser("Microsoft Edge", "microsoft-edge", ["--new-window"]),
            ]
        elif sys.platform == "win32":  # Windows
            return [
                Browser("Google Chrome", "chrome", ["--new-window"]),
                Browser("Microsoft Edge", "msedge", ["--new-window"]),
                Browser("Firefox", "firefox", ["--new-window"]),
                Browser("Internet Explorer", "iexplore", ["--new-window"]),
            ]
        else:
            return []

    def _load_config(self) -> Optional[List[Browser]]:
        """Load browsers from config file."""
        try:
            if not os.path.exists(self.config_path):
                return None
                
            with open(self.config_path, "r") as f:
                config_data = json.load(f)
                
            browsers = []
            for browser_data in config_data.get("browsers", []):
                browsers.append(Browser(
                    name=browser_data["name"],
                    path=browser_data["path"],
                    args=browser_data.get("args", [])
                ))
                
            return browsers
        except Exception as e:
            print(f"Error loading config: {e}")
            return None

    def _save_config(self, browsers: List[Browser]) -> bool:
        """Save browsers to config file."""
        try:
            # Ensure config directory exists
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            config_data = {
                "browsers": [
                    {
                        "name": browser.name,
                        "path": browser.path,
                        "args": browser.args
                    }
                    for browser in browsers
                ]
            }
            
            with open(self.config_path, "w") as f:
                json.dump(config_data, f, indent=2)
                
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def detect_browsers(self) -> List[Browser]:
        """Detect available browsers."""
        # Try to load from config first
        config_browsers = self._load_config()
        if config_browsers:
            return [browser for browser in config_browsers if browser.is_available()]
        
        # Fall back to defaults
        default_browsers = self._get_default_browsers()
        return [browser for browser in default_browsers if browser.is_available()]

    def create_example_config(self) -> bool:
        """Create example config file."""
        example_browsers = [
            Browser("Google Chrome", "google-chrome", ["--new-window"]),
            Browser("Firefox", "firefox", ["--new-window"]),
            Browser("Custom Browser", "/path/to/your/browser", ["--custom-flag"]),
        ]
        return self._save_config(example_browsers)