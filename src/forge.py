import os
import math

from PIL import Image, ImageFont, ImageDraw


def load_font(font_name: str, size: int) -> ImageFont.FreeTypeFont:
    '''
    Load font from the fonts directory. If not found use a default font.

        font_name: name of the font (without extension).
        size: text size.
    '''

    supported_formats = ('.otf', '.ttf', '.ttc')

    dirname, _ = os.path.split(os.path.abspath(__file__))
    fontdir = os.path.join(dirname, '..', 'res', 'fonts')

    # Complete path to font name (if applicable)
    fontpath = ''

    # Search for font in fonts folder
    for file in os.listdir(fontdir):
        filename = file[:-4]
        ext = file[-4:]

        if ext in supported_formats and font_name.lower() == filename.lower():
            fontpath = os.path.join(fontdir, file)

    # Load font, use default if font not found
    if fontpath:
        font = ImageFont.truetype(fontpath, size, encoding='unic')
    else:
        print('Warning: font %s not found, using default...' % font_name)
        font = ImageFont.load_default(size)

    return font


def get_font_size(text: str, size: tuple[int]) -> int:
    '''Compute size of font.
    
        text: text of watermark.
        size: canvas dimensions.
    '''

    FONT_RATIO = 1.0
    DIAGONAL_PERCENTAGE = 1.61

    width, height = size
    message_length = len(text)
    diagonal_length = int(math.sqrt((width**2) + (height**2)))
    diagonal_to_use = diagonal_length * DIAGONAL_PERCENTAGE
    font_size = int(diagonal_to_use / (message_length / FONT_RATIO))

    return font_size


def create_watermark(text: str, size: tuple[int], 
                  font: ImageFont.FreeTypeFont, 
                  color: tuple[int]) -> Image:
    '''
    Create new watermark and return it as an image.
    
        text: text of watermark.
        size: dimensions of base image.
        font: text font.
        color: text color (RGBA 0-255).
    '''

    # Target
    width, height = size
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    # Watermark
    x1, y1, x2, y2 = font.getbbox(text)
    mark_width, mark_height = x2, y2

    watermark = Image.new('RGBA', (mark_width, mark_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)
    draw.text((0, 0), text=text, font=font, fill=color)

    angle = math.degrees(math.atan(height / width))
    watermark = watermark.rotate(angle, expand=1)

    # Merge
    wx, wy = watermark.size
    px = int((width - wx) / 2)
    py = int((height - wy) / 2)
    image.paste(watermark, (px, py, px + wx, py + wy), watermark)

    return image


def new_watermark(text: str, font: str, size: tuple[int], color: tuple[int]) -> Image:
    '''
    Create watermark.
    
        text: text of watermark.
        size: canvas dimenstions.
        font: text font name.
        color: text color (RGBA 0-255).
    '''

    font_size = get_font_size(text, size)
    font = load_font(font, font_size)
    watermark = create_watermark(text, size, font, color)

    return watermark
