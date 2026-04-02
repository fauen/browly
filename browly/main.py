#!/usr/bin/env python3

import sys
import webbrowser
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, 
    QListWidgetItem, QPushButton, QHBoxLayout, QLabel, QMessageBox,
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices

from .browsers import BrowserDetector, Browser


class AddBrowserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Custom Browser")
        self.setMinimumWidth(400)
        
        layout = QFormLayout(self)
        
        self.name_input = QLineEdit()
        self.path_input = QLineEdit()
        self.args_input = QLineEdit()
        self.args_input.setPlaceholderText("e.g., --new-window --incognito")
        
        layout.addRow("Browser Name:", self.name_input)
        layout.addRow("Path/Command:", self.path_input)
        layout.addRow("Arguments:", self.args_input)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)
    
    def get_browser_data(self):
        args = self.args_input.text().strip()
        return {
            "name": self.name_input.text().strip(),
            "path": self.path_input.text().strip(),
            "args": [arg.strip() for arg in args.split()] if args else []
        }


class BrowlyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browly - Browser Picker")
        self.setMinimumSize(500, 400)
        
        self.detector = BrowserDetector()
        self.browsers = []
        self.url_to_open = None
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Browser list
        self.browser_list = QListWidget()
        self.browser_list.setSelectionMode(QListWidget.SingleSelection)
        self.browser_list.doubleClicked.connect(self.open_with_selected_browser)
        main_layout.addWidget(QLabel("Available Browsers:"))
        main_layout.addWidget(self.browser_list, stretch=1)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_browser_list)
        button_layout.addWidget(self.refresh_button)
        
        self.add_button = QPushButton("Add Browser")
        self.add_button.clicked.connect(self.add_custom_browser)
        button_layout.addWidget(self.add_button)
        
        self.open_button = QPushButton("Open with Selected")
        self.open_button.clicked.connect(self.open_with_selected_browser)
        button_layout.addWidget(self.open_button)
        
        main_layout.addLayout(button_layout)
        
        self.setCentralWidget(main_widget)
        
        # Parse command line arguments
        self.parse_arguments()
        
        # Refresh browser list
        self.refresh_browser_list()
    
    def parse_arguments(self):
        """Parse command line arguments for URL."""
        if len(sys.argv) > 1:
            # Check if it's a URL (starts with http:// or https://)
            arg = sys.argv[1]
            if arg.startswith(('http://', 'https://')):
                self.url_to_open = arg
                # Open the URL selection dialog immediately
                self.show_url_dialog()
    
    def show_url_dialog(self):
        """Show dialog to enter URL if not provided."""
        if self.url_to_open:
            return  # URL already provided
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Enter URL")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        url_input = QLineEdit()
        url_input.setPlaceholderText("https://example.com")
        layout.addWidget(QLabel("Enter URL to open:"))
        layout.addWidget(url_input)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        if dialog.exec() == QDialog.Accepted:
            self.url_to_open = url_input.text().strip()
            if self.url_to_open:
                # Auto-select first browser and open
                if self.browser_list.count() > 0:
                    self.browser_list.setCurrentRow(0)
                    self.open_with_selected_browser()
    
    def refresh_browser_list(self):
        """Refresh the list of available browsers."""
        self.browser_list.clear()
        self.browsers = self.detector.detect_browsers()
        
        for browser in self.browsers:
            item = QListWidgetItem(browser.name)
            item.setData(Qt.UserRole, browser)
            self.browser_list.addItem(item)
        
        if self.browsers:
            self.browser_list.setCurrentRow(0)
    
    def add_custom_browser(self):
        """Add a custom browser to the configuration."""
        dialog = AddBrowserDialog(self)
        if dialog.exec() == QDialog.Accepted:
            browser_data = dialog.get_browser_data()
            if not browser_data["name"] or not browser_data["path"]:
                QMessageBox.warning(self, "Error", "Browser name and path are required.")
                return
            
            # Create browser and test if it's available
            browser = Browser(
                name=browser_data["name"],
                path=browser_data["path"],
                args=browser_data["args"]
            )
            
            if not browser.is_available():
                reply = QMessageBox.question(
                    self, "Browser Not Found",
                    f"The browser at '{browser.path}' was not found. Add anyway?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return
            
            # Add to config
            all_browsers = self.detector._load_config() or []
            all_browsers.append(browser)
            
            if self.detector._save_config(all_browsers):
                self.refresh_browser_list()
                QMessageBox.information(self, "Success", "Browser added successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to save browser configuration.")
    
    def open_with_selected_browser(self):
        """Open the URL with the selected browser."""
        if not self.url_to_open:
            self.show_url_dialog()
            return
        
        selected_items = self.browser_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "Please select a browser first.")
            return
        
        browser = selected_items[0].data(Qt.UserRole)
        if browser.open(self.url_to_open):
            self.close()
        else:
            QMessageBox.warning(self, "Error", f"Failed to open URL with {browser.name}")


def main():
    """Main entry point."""
    # Handle --init flag before creating GUI
    if "--init" in sys.argv or "-i" in sys.argv:
        detector = BrowserDetector()
        if detector.create_example_config():
            print(f"Example config created at: {detector._get_config_path()}")
        else:
            print("Failed to create example config")
        return
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")  # Use Fusion style for better cross-platform look
    
    window = BrowlyMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()