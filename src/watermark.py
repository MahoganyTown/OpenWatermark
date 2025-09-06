import os
import io
import math

import fitz
import numpy as np
from PIL import Image

from .common import *
from .rand import *
from .spoof import *
from .utils import *


def flatten_pdf(doc: fitz.Document, 
    do_noise: bool = True, do_bands: bool = True, 
    dpi: int = 150) -> fitz.Document:
    '''
    Flatten the PDF document by rendering each page to an image and then
    converting it back to a PDF page. This can help in removing any
    interactive elements and ensure the watermark is embedded.
    :param doc: Input PDF document
    :param do_noise: Whether to add noise to the PDF pages
    :param do_bands: Whether to add banding noise to the PDF pages
    :param dpi: DPI for rendering the pages
    :return: Flattened PDF document
    '''

    out = fitz.open()

    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        img = pix.pil_image()
        img_arr = np.array(img)

        if do_noise:
            img_arr = add_shot_noise(img_arr)
            img_arr = add_periodic_noise(img_arr)
            img_arr = add_film_grain(img_arr)

        if do_bands:
            img_arr = add_banding_noise(img_arr)

        # Convert PIL image back to Pixmap for PyMuPDF
        img = Image.fromarray(img_arr)

        # Imge to bytes and compress
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=80)
        buf.seek(0)
        noisy_pix = fitz.Pixmap(buf)

        # New page with noisy image
        rect = page.rect
        outpage = out.new_page(width=rect.width, height=rect.height)
        outpage.insert_image(rect, pixmap=noisy_pix)

    return out


def add_watermark(
    doc: fitz.Document,
    watermark_text: str,
    fontname: str = 'helv',
    font_size: int = 40,
    spacing: float = 0.65,
) -> fitz.Document:
    '''
    Add a repeating watermark to each page of the PDF document.
    :param doc: Input PDF document
    :param watermark_text: Text for the watermark
    :param fontname: Font name for the watermark
    :param font_size: Font size for the watermark
    :param spacing: Spacing between watermarks
    :return: fitz.Document with watermarks
    '''

    # Precompute a grid covering the page
    for page in doc:
        width, height = page.rect.width, page.rect.height
        font = fitz.Font(fontname=fontname)
        text_width = font.text_length(watermark_text, font_size)
        text_height = font_size

        # Calculate rotated bounding box dimensions
        rad = math.radians(45)
        rotated_width = abs(text_width * math.cos(rad)) + \
            abs(text_height * math.sin(rad))
        rotated_height = abs(text_width * math.sin(rad)) + \
            abs(text_height * math.cos(rad))

        # Use rotated dimensions as spacing
        x_spacing = rotated_width * spacing  # slight overlap to ensure coverage
        y_spacing = rotated_height * spacing  # slight overlap to ensure coverage

        # Generate grid positions
        x_positions = []
        x = 0
        while x < width:
            x_positions.append(x)
            x += x_spacing
        y_positions = []
        y = 0
        while y < height:
            y_positions.append(y)
            y += y_spacing

        for y in y_positions:
            for x in x_positions:
                rect = fitz.Rect(x, y, x + rotated_width, y + rotated_height)

                # Morph: rotate about the top-left corner of the rect
                matrix = fitz.Matrix(1, 1)

                # Randomize the font size, opacity, and color
                opacity = random_range(OPACITY_RANGE)
                color = random_greyish_color()

                # Randomize shear and scale
                shear = random_range(SHEAR_RANGE)
                scale_x = random_range(SCALE_RANGE)
                scale_y = random_range(SCALE_RANGE)

                # Apply shear and scale
                if shear != 0:
                    matrix.preshear(shear, 0)
                if scale_x != 1 or scale_y != 1:
                    matrix.prescale(scale_x, scale_y)

                # Apply rotation
                matrix.prerotate(45)

                # Insert the watermark text
                page.insert_textbox(
                    rect,
                    watermark_text,
                    fontname=fontname,
                    fontsize=font_size,
                    color=color,
                    morph=(fitz.Point(x, y), matrix),
                    overlay=True,
                    render_mode=0,
                    fill_opacity=opacity,
                )
    return doc


def watermark(input_filenames: list, watermark_text: str, spacing: float = 0.60,
    do_date: bool = True, do_noise: bool = True, do_bands: bool = True, 
    do_lock: bool = True, do_save_pwd: bool = True) -> tuple:
    '''
    Add a watermark to a PDF document and save it with encryption.
    :param input_filenames: List of input PDF filenames
    :param watermark_text: Text for the watermark
    :param spacing: Spacing between watermarks
    :param do_date: Whether to add the current date and time to the watermark
    :param do_noise: Whether to add noise to the PDF pages
    :param do_bands: Whether to add banding noise to the PDF pages
    :param do_lock: Whether to lock the PDF with a password
    :param do_save_pwd: Whether to save the password to a txt file
    :return: Tuple containing the output filename and owner password
    '''

    # Add date and time to the watermark text
    if do_date:
        watermark_text = date_text(watermark_text)

    # Save the watermarked PDF with encryption
    length = random_range(PASSWORD_RANGE)
    owner_pw = generate_password(round(length))

    # Set permissions
    perm = get_pdf_permissions(do_lock)

    # Generate random font size and font name
    font_size = random_font_size(FONT_SIZE_RANGE)
    fontname = random_font(AVAILABLE_FONTS)

    output_pdf_filenames = []

    for filename in input_filenames:
        # Generate a new filename for the output PDF
        output_pdf_filename = get_new_pdf_filename(filename)
        output_pdf_filenames.append(output_pdf_filename)

        # Get the PDF document
        doc = open_document(filename)

        # Watermark the PDF
        doc = add_watermark(doc, watermark_text, fontname, font_size, spacing)

        # Flatten PDF and add noise to pages
        doc = flatten_pdf(doc, do_noise, do_bands)

        # Save the document with encryption
        doc.save(output_pdf_filename, garbage=3,
                deflate=True, preserve_metadata=False,
                clean=True, linear=True,
                encryption=fitz.PDF_ENCRYPT_AES_256,
                user_pw='',
                owner_pw=owner_pw,
                permissions=perm,
                compression_effort=4)
        
        # Close the document
        doc.close()

        # Set file as read-only
        os.chmod(output_pdf_filename, 0o444)

    # Save the password to a text file if required
    if do_save_pwd:
        save_pwd_to_file(owner_pw, input_filenames[0])

    # Return the output filenames and owner password
    info = {
        'output_filenames': output_pdf_filenames,
        'owner_password': owner_pw
    }

    return info


if __name__ == '__main__':
    # Example usage
    files = [
        'res/example/ducky.png'
    ]
    info = watermark(files, 'Only for the bank')
    print(f'Watermarked files saved as: {info["output_filenames"]}')
    print(f'Owner password: {info["owner_password"]}')