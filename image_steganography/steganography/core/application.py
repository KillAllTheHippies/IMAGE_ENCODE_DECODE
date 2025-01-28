from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

from ..gui.main_window import MainWindow

class SteganographyApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.main_window = None
    
    def initialize(self):
        try:
            # Initialize the main window
            self.main_window = MainWindow()
            self.main_window.show()
            return True
        except Exception as e:
            print(f"Error initializing application: {str(e)}")
            return False

def main():
    import sys
    app = SteganographyApp(sys.argv)
    if app.initialize():
        sys.exit(app.exec_())
    else:
        sys.exit(1)
