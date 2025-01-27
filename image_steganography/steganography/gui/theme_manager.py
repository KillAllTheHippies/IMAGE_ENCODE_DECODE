from PyQt5.QtWidgets import QApplication
from ..config import ConfigHandler

class ThemeManager:
    LIGHT_STYLE = """
        QWidget {
            background: #f8f9fa;
            color: #212529;
            font-family: 'Segoe UI', sans-serif;
        }
        
        QLabel {
            border: 2px dashed #dee2e6;
            border-radius: 8px;
            padding: 12px;
        }
        
        QLabel[dragging="true"] {
            border: 2px dashed #adb5bd;
            background-color: #e9ecef;
        }
        
        QPushButton {
            background-color: #0d6efd;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 14px;
        }
        
        QPushButton:hover {
            background-color: #0b5ed7;
        }
        
        QPushButton:pressed {
            background-color: #0a58ca;
        }
        
        QTextEdit {
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 8px;
            background: white;
            color: #212529;
            selection-background-color: #0d6efd;
            selection-color: white;
        }
        
        QComboBox {
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 6px;
            background: white;
            color: #212529;
        }
    """
    
    DARK_STYLE = """
        QWidget {
            background: #212529;
            color: #f8f9fa;
            font-family: 'Segoe UI', sans-serif;
        }
        
        QLabel {
            border: 2px dashed #495057;
            border-radius: 8px;
            padding: 12px;
        }
        
        QLabel[dragging="true"] {
            border: 2px dashed #6c757d;
            background-color: #343a40;
        }
        
        QPushButton {
            background-color: #0d6efd;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 14px;
        }
        
        QPushButton:hover {
            background-color: #0b5ed7;
        }
        
        QPushButton:pressed {
            background-color: #0a58ca;
        }
        
        QTextEdit {
            border: 1px solid #495057;
            border-radius: 6px;
            padding: 8px;
            background: #343a40;
            color: #f8f9fa;
            selection-background-color: #0d6efd;
            selection-color: white;
        }
        
        QComboBox {
            border: 1px solid #495057;
            border-radius: 6px;
            padding: 6px;
            background: #343a40;
            color: #f8f9fa;
        }
    """

    def __init__(self, app):
        self.app = app
        self.config = ConfigHandler()
        
    def apply_theme(self):
        if self.config.dark_mode:
            self.app.setStyleSheet(self.DARK_STYLE)
        else:
            self.app.setStyleSheet(self.LIGHT_STYLE)