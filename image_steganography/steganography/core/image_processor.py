from typing import Tuple, Optional
from PIL import Image
import numpy as np
import math
from ..logger import get_logger
from ..image_utils import validate_image_format, convert_to_rgba
def encode(image_path: str, message: str, output_path: str) -> None:
    """Encode a message into an image using LSB steganography.

    Args:
        image_path: Path to input image
        message: Message to encode
        output_path: Path to save encoded image
    """
    processor = ImageProcessor()
    processor.load_image(image_path)
    processor.encode_lsb(message)
    processor.save_image(output_path)

def decode(image_path: str) -> str:
    """Decode a message from an image using LSB steganography.

    Args:
        image_path: Path to encoded image

    Returns:
        Decoded message string
    """
    processor = ImageProcessor()
    processor.load_image(image_path)
    return processor.decode_lsb()

logger = get_logger(__name__)

class ImageProcessor:
    """Handles image processing operations for steganography.

    Provides methods for encoding and decoding messages in images using various techniques:
    - LSB (Least Significant Bit) encoding
    - Alpha channel encoding
    - Direct alpha encoding
    - Combined encoding methods

    Attributes:
        image: The current image being processed
        mode: The current processing mode (encode/decode)

    Example:
        >>> processor = ImageProcessor()
        >>> processor.load_image('input.png')
        >>> processor.encode_lsb('secret message')
        >>> processor.save_image('output.png')
    """
    
    def __init__(self):
        self.image: Optional[Image.Image] = None
        self.mode: Optional[str] = None
        
    def load_image(self, image_path: str) -> None:
        

        """Load an image from the specified path.
        
        Args:
            image_path: Path to the image file
            
        Raises:
            FileNotFoundError: If image file does not exist
            ValueError: If image format is invalid
        """
        try:
            self.image = Image.open(image_path)
            validate_image_format(self.image)
            self.image = convert_to_rgba(self.image)
            logger.info(f"Successfully loaded image from {image_path}")
        except Exception as e:
            logger.error(f"Failed to load image: {str(e)}")
            raise
            
    def encode_lsb(self, message: str) -> None:
        """Encode a message using LSB steganography.

        Args:
            message: The message to encode
            
        Raises:
            ValueError: If message is too large for the image
        """
        if not self.image:
            raise ValueError("No image loaded")
            
        # Convert image to numpy array for efficient processing
        if not message:
            raise ValueError("Message cannot be empty")

        max_message_size = self._calculate_max_message_size()
        if len(message) > max_message_size:
            raise ValueError(f"Message too large. Maximum size: {max_message_size} characters")

        img_array = np.array(self.image)
        
        # Convert message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        
        # Implement LSB encoding
        self._apply_lsb_encoding(img_array, binary_message)

        self.image = Image.fromarray(img_array)
        logger.info("Message encoded using LSB method")
    def decode_lsb(self) -> str:
        """Decode a message using LSB steganography.
        
        Returns:
            The decoded message
            
        Raises:
            ValueError: If no image is loaded
        """
        if not self.image:
            raise ValueError("No image loaded")
            
        # Implementation of LSB decoding logic
        img_array = np.array(self.image)
        decoded_message = self._extract_lsb_message(img_array)
        
        return decoded_message
    def encode_alpha(self, message: str, alpha_bits: int = 2) -> None:
        """Encode a message using alpha channel steganography.
        
        Args:
            message: The message to encode
            
        Raises:
            ValueError: If message is too large for the image
        """
        if not self.image:
            raise ValueError("No image loaded")
            
        # Implementation of alpha channel encoding
        img_array = np.array(self.image)
        self._apply_alpha_encoding(img_array, message, alpha_bits)
        logger.info("Message encoded using alpha channel method")
        
    def decode_alpha(self) -> str:
        """Decode a message using alpha channel steganography.
        
        Returns:
            The decoded message
            
        Raises:
            ValueError: If no image is loaded
        """
        if not self.image:
            raise ValueError("No image loaded")
            
        # Implementation of alpha channel decoding
        img_array = np.array(self.image)
        decoded_message = self._extract_alpha_message(img_array)
        return decoded_message
        
    def save_image(self, output_path: str) -> None:
        """Save the processed image to the specified path.
        
        Args:
            output_path: Path to save the image
            
        Raises:
            ValueError: If no image is loaded
            IOError: If image cannot be saved
        """
        if not self.image:
            raise ValueError("No image loaded")
            
        try:
            self.image.save(output_path)
            logger.info(f"Image successfully saved to {output_path}")
        except Exception as e:
            logger.error(f"Failed to save image: {str(e)}")
            raise

    def _calculate_max_message_size(self) -> int:
        """Calculate maximum message size that can be encoded in the image.

        Returns:
            Maximum number of characters that can be encoded
        """
        if not self.image:
            return 0
            
        width, height = self.image.size
        return (width * height * 3) // 8  # 3 channels, 8 bits per character

    def _apply_lsb_encoding(self, img_array: np.ndarray, binary_message: str) -> None:
        """Apply LSB encoding to the image array.

        Args:
            img_array: Numpy array of the image
            binary_message: Binary representation of the message
        Note: img_array must be of type uint8
        """
        message_index = 0
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                for k in range(3):  # RGB channels
                    if message_index < len(binary_message):
                        new_value = (img_array[i, j, k] & ~1) | int(binary_message[message_index])
                        # Ensure value is uint8 and within valid range by clipping first
                        clipped_value = np.clip(new_value, 0, 255)
                        img_array[i, j, k] = np.uint8(clipped_value)
                        message_index += 1

    def _extract_lsb_message(self, img_array: np.ndarray) -> str:
        """Extract LSB encoded message from the image array.

        Args:
            img_array: Numpy array of the image

        Returns:
            Decoded message string
        """
        binary_message = ''
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                for k in range(3):  # RGB channels
                    binary_message += str(img_array[i, j, k] & 1)
                    if len(binary_message) % 8 == 0 and binary_message[-8:] == '00000000':
                        # Null terminator found
                        return ''.join(chr(int(binary_message[i:i+8], 2)) 
                                    for i in range(0, len(binary_message)-8, 8))
        return ''.join(chr(int(binary_message[i:i+8], 2)) 
                      for i in range(0, len(binary_message), 8))


