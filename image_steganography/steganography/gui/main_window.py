import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QMessageBox, QColorDialog
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import Qt
from steganography.core import encode, decode

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Image Steganography')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.image_label = QLabel('No image selected')
        layout.addWidget(self.image_label)

        self.select_button = QPushButton('Select Image')
        self.select_button.clicked.connect(self.select_image)
        layout.addWidget(self.select_button)

        self.encode_button = QPushButton('Encode Message')
        self.encode_button.clicked.connect(self.encode_message)
        layout.addWidget(self.encode_button)

        self.decode_button = QPushButton('Decode Message')
        self.decode_button.clicked.connect(self.decode_message)
        layout.addWidget(self.decode_button)

        self.font_color = QPushButton('Choose Font Color')
        self.font_color.clicked.connect(self.choose_font_color)
        layout.addWidget(self.font_color)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "Images (*.png *.xpm *.jpg);;All Files (*)", options=options)
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))
            self.image_label.setAlignment(Qt.AlignCenter)

    def encode_message(self):
        if not hasattr(self, 'image_path'):
            QMessageBox.warning(self, 'No Image', 'Please select an image first.')
            return

        message, ok = QInputDialog.getText(self, 'Encode Message', 'Enter the message to encode:')
        if ok and message:
            encode(self.image_path, message)
            QMessageBox.information(self, 'Success', 'Message encoded successfully.')

    def decode_message(self):
        if not hasattr(self, 'image_path'):
            QMessageBox.warning(self, 'No Image', 'Please select an image first.')
            return

        message = decode(self.image_path)
        QMessageBox.information(self, 'Decoded Message', message)

    def choose_font_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.image_label.setStyleSheet(f"color: {color.name()}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())