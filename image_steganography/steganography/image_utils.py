from PIL import Image
import numpy as np

def validate_image_format(image_path):
    """Validate that image is in a supported format"""
    supported_formats = ['PNG', 'BMP', 'TIFF']
    try:
        with Image.open(image_path) as img:
            # Some PNGs might report as WEBP due to metadata
            if img.format == 'WEBP' and img.mode in ['RGB', 'RGBA']:
                return True, None
            if img.format not in supported_formats:
                return False, f"Unsupported format: {img.format}. Supported formats: {', '.join(supported_formats)}"
            return True, None
    except Exception as e:
        return False, str(e)

def calculate_max_capacity(image_path, method='lsb'):
    """Calculate maximum message capacity for given encoding method"""
    img = Image.open(image_path)
    width, height = img.size
    
    if method == 'lsb':
        # 3 bits per pixel (RGB channels)
        return (width * height * 3) // 8
    elif method == 'alpha':
        if img.mode != 'RGBA':
            return 0
        # 1 bit per pixel (alpha channel)
        return (width * height) // 8
    else:
        return 0

def convert_to_rgba(image_path):
    """Convert image to RGBA format if not already"""
    img = Image.open(image_path)
    if img.mode != 'RGBA':
        return img.convert('RGBA')
    return img

def get_image_preview(image_path, max_size=(300, 300)):
    """Get resized image preview for GUI display"""
    img = Image.open(image_path)
    img.thumbnail(max_size)
    return img