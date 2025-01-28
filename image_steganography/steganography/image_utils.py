import base64
from io import BytesIO
from PIL import Image
import numpy as np

def is_base64_image(data):
    """Check if input is a base64 encoded image"""
    try:
        if isinstance(data, str) and data.startswith('data:image'):
            return True
        return False
    except:
        return False

def decode_base64_image(data):
    """Decode base64 image string to PIL Image"""
    try:
        # Remove data:image/...;base64, prefix
        img_data = data.split('base64,')[-1]
        img_bytes = base64.b64decode(img_data)
        return Image.open(BytesIO(img_bytes))
    except Exception as e:
        raise ValueError(f"Invalid base64 image: {str(e)}")

def encode_image_to_base64(image, format='PNG'):
    """Convert PIL Image to base64 string"""
    buffered = BytesIO()
    image.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue())
    return f"data:image/{format.lower()};base64,{img_str.decode()}"

def validate_image_format(image_input):
    """Validate that image is in a supported format"""
    supported_formats = ['PNG', 'BMP', 'TIFF']
    try:
        if is_base64_image(image_input):
            img = decode_base64_image(image_input)
        else:
            img = Image.open(image_input)
            
        # Some PNGs might report as WEBP due to metadata
        if img.format == 'WEBP' and img.mode in ['RGB', 'RGBA']:
            return True, None
        if img.format not in supported_formats:
            return False, f"Unsupported format: {img.format}. Supported formats: {', '.join(supported_formats)}"
        return True, None
    except Exception as e:
        return False, str(e)

def calculate_max_capacity(image_input, method='lsb'):
    """Calculate maximum message capacity for given encoding method"""
    if is_base64_image(image_input):
        img = decode_base64_image(image_input)
    else:
        img = Image.open(image_input)
        
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

def convert_to_rgba(image_input):
    """Convert image to RGBA format if not already"""
    # If input is already an Image object, use it directly
    if isinstance(image_input, Image.Image):
        img = image_input
    else:
        if is_base64_image(image_input):
            img = decode_base64_image(image_input)
        else:
            img = Image.open(image_input)

    if img.mode != 'RGBA':
        return img.convert('RGBA')
    return img

def get_image_preview(image_input, max_size=(300, 300)):
    """Get resized image preview for GUI display"""
    if is_base64_image(image_input):
        img = decode_base64_image(image_input)
    else:
        img = Image.open(image_input)
        
    img.thumbnail(max_size)
    return img

def add_text_overlay(image, text, position=(0, 0), font_name='Arial', font_size=20,
                    font_color=(255, 255, 255), font_emphasis='normal',
                    justification='left', transparency=1.0):
    """
    Add text overlay to an image with customizable settings.
    
    Args:
        image: PIL Image object
        text: Text to overlay
        position: (x, y) tuple for text position
        font_name: Font name (default: Arial)
        font_size: Font size in points (default: 20)
        font_color: RGB tuple for text color (default: white)
        font_emphasis: Font style ('normal', 'bold', 'italic')
        justification: Text alignment ('left', 'center', 'right')
        transparency: Text transparency (0.0 to 1.0)
        
    Returns:
        PIL Image with text overlay
    """
    from PIL import ImageDraw, ImageFont
    
    # Convert image to RGBA if needed
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Create transparent layer for text
    txt_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    # Load font with specified style
    try:
        font = ImageFont.truetype(font_name, font_size)
    except IOError:
        font = ImageFont.load_default()
    
    # Apply font emphasis
    if font_emphasis == 'bold':
        font = font.font_variant(style='Bold')
    elif font_emphasis == 'italic':
        font = font.font_variant(style='Italic')
    
    # Calculate text position based on justification
    text_width, text_height = draw.textsize(text, font=font)
    if justification == 'center':
        position = (position[0] - text_width//2, position[1])
    elif justification == 'right':
        position = (position[0] - text_width, position[1])
    
    # Draw text with transparency
    r, g, b = font_color
    draw.text(position, text, font=font, fill=(r, g, b, int(255 * transparency)))
    
    # Combine layers
    return Image.alpha_composite(image, txt_layer)
