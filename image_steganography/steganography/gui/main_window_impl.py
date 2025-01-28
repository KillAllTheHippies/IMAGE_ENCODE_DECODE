from PyQt6.QtWidgets import QMainWindow
from image_steganography.steganography.utils.style_manager import StyleManager

class MainWindowImpl(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize theme management
        self.style_manager = StyleManager()
        self.style_manager.apply_default_theme(self)
        
        self.setWindowTitle("Image Steganography")
        self.setGeometry(100, 100, 800, 600)