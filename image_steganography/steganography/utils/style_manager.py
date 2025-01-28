from PyQt5.QtCore import QSettings

DARK_STYLE = """
    QWidget {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    QMenuBar {
        background-color: #2d2d2d;
    }
    QMenuBar::item:selected {
        background: #3d3d3d;
    }
    QMenu {
        background-color: #2d2d2d;
    }
    QMenu::item:selected {
        background-color: #3d3d3d;
    }
"""

class StyleManager:
    """Manage application visual styles and themes"""
    
    def __init__(self):
        self.settings = QSettings("YourCompany", "Steganography")
    
    def apply_current_style(self, window):
        """Apply saved style preference to window"""
        if self.settings.value("dark_mode", "false") == "true":
            window.setStyleSheet(DARK_STYLE)
