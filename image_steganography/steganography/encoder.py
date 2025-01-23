from PIL import Image
import numpy as np

class ImageEncoder:
    def __init__(self):
        self.image = None
        self.encoded_image = None
        
    def load_image(self, image_path):
        """Load image from file"""
        self.image = Image.open(image_path)
        if self.image.mode not in ['RGB', 'RGBA']:
            self.image = self.image.convert('RGBA')
            
    def save_image(self, output_path):
        """Save encoded image to file"""
        if self.encoded_image:
            self.encoded_image.save(output_path)
            
    def encode_lsb(self, message):
        """Encode message using LSB steganography"""
        if not self.image:
            raise ValueError("No image loaded")
            
        # Convert message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        message_length = len(binary_message)
        
        # Convert image to numpy array
        img_array = np.array(self.image)
        height, width, channels = img_array.shape
        
        # Check if message fits in image
        if message_length > height * width * 3:
            raise ValueError("Message too large for image")
            
        # Encode message in LSBs
        index = 0
        for i in range(height):
            for j in range(width):
                for k in range(3):  # Only modify RGB channels
                    if index < message_length:
                        # Modify LSB
                        img_array[i, j, k] = (img_array[i, j, k] & ~1) | int(binary_message[index])
                        index += 1
                        
        self.encoded_image = Image.fromarray(img_array)
        
    def encode_alpha(self, message):
        """Encode message using alpha channel"""
        if not self.image:
            raise ValueError("No image loaded")
            
        if self.image.mode != 'RGBA':
            raise ValueError("Image must have alpha channel")
            
        # Convert message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        message_length = len(binary_message)
        
        # Convert image to numpy array
        img_array = np.array(self.image)
        height, width, _ = img_array.shape
        
        # Check if message fits in image
        if message_length > height * width:
            raise ValueError("Message too large for image")
            
        # Encode message in alpha channel
        index = 0
        for i in range(height):
            for j in range(width):
                if index < message_length:
                    # Modify alpha channel
                    img_array[i, j, 3] = (img_array[i, j, 3] & ~1) | int(binary_message[index])
                    index += 1
                    
        self.encoded_image = Image.fromarray(img_array)
        
    def decode_lsb(self):
        """Decode message from LSB steganography"""
        if not self.image:
            raise ValueError("No image loaded")
            
        try:
            img_array = np.array(self.image)
            height, width, channels = img_array.shape
            
            # Initialize variables
            binary_message = ''
            max_bits = height * width * 3
            stop_char = chr(0)  # Null character as message terminator
            
            # Extract LSBs from RGB channels
            for i in range(height):
                for j in range(width):
                    for k in range(3):  # Only check RGB channels
                        if len(binary_message) >= max_bits:
                            break
                        binary_message += str(img_array[i, j, k] & 1)
                        
            # Convert binary to string with termination check
            message = ''
            for i in range(0, len(binary_message), 8):
                if i + 8 > len(binary_message):
                    break
                byte = binary_message[i:i+8]
                char = chr(int(byte, 2))
                if char == stop_char:
                    break
                message += char
                
            return message
            
        except Exception as e:
            raise ValueError(f"LSB decoding failed: {str(e)}")
    
    def decode_alpha(self):
        """Decode message from alpha channel"""
        if not self.image:
            raise ValueError("No image loaded")
            
        if self.image.mode != 'RGBA':
            raise ValueError("Image must have alpha channel")
            
        img_array = np.array(self.image)
        height, width, _ = img_array.shape
        
        binary_message = ''
        for i in range(height):
            for j in range(width):
                binary_message += str(img_array[i, j, 3] & 1)
                
        # Convert binary to string
        message = ''
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            message += chr(int(byte, 2))
            
        return message
        
    def encode_direct_alpha(self, message):
        """Encode message directly into alpha channel"""
        if not self.image:
            raise ValueError("No image loaded")
            
        # Ensure image is in RGBA format
        if self.image.mode != 'RGBA':
            self.image = self.image.convert('RGBA')
            
        try:
            # Convert image to numpy array
            img_array = np.array(self.image)
            height, width, channels = img_array.shape
            
            # Verify array shape
            if channels != 4:
                raise ValueError("Invalid image format - must have 4 channels (RGBA)")
                
            # Check if message fits in image
            if len(message) > height * width:
                raise ValueError(f"Message too large for image. Max: {height * width} chars")
                
            # Encode message directly in alpha channel
            index = 0
            for i in range(height):
                for j in range(width):
                    if index < len(message):
                        char = message[index]
                        # Validate character is within valid ASCII range
                        if ord(char) > 255:
                            raise ValueError(f"Invalid character: {char} (must be ASCII)")
                        # Set alpha channel to character's ASCII value
                        img_array[i, j, 3] = ord(char)
                        index += 1
                    else:
                        # Fill remaining pixels with 255 (fully opaque)
                        img_array[i, j, 3] = 255
                        
            self.encoded_image = Image.fromarray(img_array)
            
        except Exception as e:
            # Clean up and re-raise error
            self.encoded_image = None
            raise ValueError(f"Encoding failed: {str(e)}")
        
    def decode_direct_alpha(self):
        """Decode message from direct alpha channel encoding"""
        if not self.image:
            raise ValueError("No image loaded")
            
        try:
            # Ensure image is in RGBA format
            if self.image.mode != 'RGBA':
                self.image = self.image.convert('RGBA')
                
            img_array = np.array(self.image)
            height, width, channels = img_array.shape
            
            # Verify array shape
            if channels != 4:
                raise ValueError("Invalid image format - must have 4 channels (RGBA)")
                
            message = ''
            for i in range(height):
                for j in range(width):
                    alpha = img_array[i, j, 3]
                    # Stop at first fully opaque pixel
                    if alpha == 255:
                        break
                    # Validate ASCII value
                    if alpha < 0 or alpha > 255:
                        raise ValueError(f"Invalid alpha value: {alpha}")
                    message += chr(alpha)
                else:
                    continue
                break
                
            return message
            
        except Exception as e:
            raise ValueError(f"Decoding failed: {str(e)}")
            
    def encode_combined(self, message):
        """Encode message using both LSB and direct alpha methods"""
        if not self.image:
            raise ValueError("No image loaded")
            
        try:
            # First encode using LSB
            self.encode_lsb(message)
            
            # Then encode using direct alpha
            if self.image.mode != 'RGBA':
                self.image = self.image.convert('RGBA')
                
            img_array = np.array(self.image)
            self.encode_direct_alpha(message)
            
        except Exception as e:
            self.encoded_image = None
            raise ValueError(f"Combined encoding failed: {str(e)}")