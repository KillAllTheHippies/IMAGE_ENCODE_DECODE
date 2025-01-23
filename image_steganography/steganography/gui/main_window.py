from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QFileDialog, QComboBox, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ..encoder import ImageEncoder
from ..image_utils import validate_image_format, calculate_max_capacity, get_image_preview

class ImagePreviewWidget(QLabel):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:
                file_path = urls[0].toLocalFile()
                if any(file_path.lower().endswith(ext) for ext in ['.png', '.bmp', '.tiff']):
                    event.acceptProposedAction()
                    self.setProperty("dragging", "true")
                    self.style().polish(self)

    def dragLeaveEvent(self, event):
        self.setProperty("dragging", "false")
        self.style().polish(self)

    def dropEvent(self, event):
        self.setProperty("dragging", "false")
        self.style().polish(self)
        
        try:
            if event.mimeData().hasUrls():
                file_path = event.mimeData().urls()[0].toLocalFile()
                if not file_path:
                    return
                    
                # Verify file exists and is readable
                import os
                if not os.path.exists(file_path) or not os.access(file_path, os.R_OK):
                    QMessageBox.warning(self.main_window, "Error", "Cannot read the selected file")
                    return
                    
                self.main_window.select_image(file_path)
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to load image: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Steganography")
        self.setMinimumSize(800, 600)
        
        # Initialize encoder
        self.encoder = ImageEncoder()
        
        # Create main widgets
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Image selection
        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.image_preview = ImagePreviewWidget(self)
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                min-height: 200px;
            }
            QLabel[dragging="true"] {
                border: 2px dashed #666;
                background-color: #f0f0f0;
            }
        """)
        
        select_image_btn = QPushButton("Select Image")
        select_image_btn.clicked.connect(self.select_image)
        
        # Encoding options
        options_layout = QHBoxLayout()
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "LSB Encoding",
            "Alpha Channel Encoding",
            "Direct Alpha Encoding",
            "Combined Encoding"
        ])
        
        # Text input
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter message to encode...")
        self.text_input.setAcceptDrops(False)
        
        # Buttons
        encode_btn = QPushButton("Encode")
        encode_btn.clicked.connect(self.encode_message)
        
        decode_btn = QPushButton("Decode")
        decode_btn.clicked.connect(self.decode_message)
        
        # Status bar
        self.status_bar = self.statusBar()
        
        # Add widgets to layout
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.image_preview)
        main_layout.addWidget(select_image_btn)
        main_layout.addLayout(options_layout)
        options_layout.addWidget(QLabel("Encoding Method:"))
        options_layout.addWidget(self.method_combo)
        main_layout.addWidget(self.text_input)
        main_layout.addWidget(encode_btn)
        main_layout.addWidget(decode_btn)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
    def select_image(self, file_path=None):
        """Handle image selection"""
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Image", "", "Images (*.png *.bmp *.tiff)"
            )
        
        if file_path:
            valid, error = validate_image_format(file_path)
            if not valid:
                QMessageBox.warning(self, "Invalid Image", error)
                return
                
            self.encoder.load_image(file_path)
            self.image_label.setText(file_path)
            
            # Update preview
            preview = get_image_preview(file_path)
            from PIL.ImageQt import ImageQt
            from PyQt5.QtGui import QImage
            qimage = QImage(preview.tobytes(), preview.size[0], preview.size[1], QImage.Format_RGBA8888)
            self.image_preview.setPixmap(QPixmap.fromImage(qimage))
            
            # Update status
            method = self.method_combo.currentText().lower().split()[0]
            capacity = calculate_max_capacity(file_path, method)
            self.status_bar.showMessage(f"Max message capacity: {capacity} characters")
            
    def encode_message(self):
        """Handle message encoding"""
        if not self.encoder.image:
            QMessageBox.warning(self, "Error", "No image selected")
            return
            
        message = self.text_input.toPlainText()
        if not message:
            QMessageBox.warning(self, "Error", "No message to encode")
            return
            
        try:
            method = self.method_combo.currentText().lower().split()[0]
            if method == 'lsb':
                self.encoder.encode_lsb(message)
            elif method == 'alpha':
                self.encoder.encode_alpha(message)
            elif method == 'direct':
                self.encoder.encode_direct_alpha(message)
            else:  # combined
                self.encoder.encode_combined(message)
                
            # Save encoded image
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Encoded Image", "", "PNG Image (*.png)"
            )
            if file_path:
                self.encoder.save_image(file_path)
                QMessageBox.information(self, "Success", "Message encoded successfully")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
    def decode_message(self):
        """Handle message decoding"""
        if not self.encoder.image:
            QMessageBox.warning(self, "Error", "No image selected")
            return
            
        try:
            method = self.method_combo.currentText().lower().split()[0]
            if method == 'lsb':
                message = self.encoder.decode_lsb()
            elif method == 'alpha':
                message = self.encoder.decode_alpha()
            else:  # direct
                message = self.encoder.decode_direct_alpha()
                
            self.text_input.setPlainText(message)
            QMessageBox.information(self, "Decoded Message", message)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))