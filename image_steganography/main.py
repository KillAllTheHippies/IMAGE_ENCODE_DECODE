import sys
from PyQt5.QtWidgets import QApplication
from image_steganography.steganography.core import SteganographyApp, encode, decode

def main():
    """Application entry point"""
    # Example usage of encode/decode functions
    encoded_image = encode("input.png", "secret message", "output.png")
    decoded_message = decode(encoded_image)
    
    print(f"Decoded message: {decoded_message}")
    
    app = SteganographyApp(sys.argv)
    app.initialize()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
