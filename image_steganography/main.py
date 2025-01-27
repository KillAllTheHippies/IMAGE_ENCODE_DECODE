import sys
from PyQt5.QtWidgets import QApplication, QAction, QMenu
from PyQt5.QtCore import QSettings
from steganography.gui.main_window import MainWindow

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

def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow()
    
    # Initialize settings
    settings = QSettings("YourCompany", "Steganography")
    if settings.value("dark_mode", "false") == "true":
        window.apply_dark_style(DARK_STYLE)
    
    window.show()
    
    # Start application event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
