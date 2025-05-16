import io
import string
import secrets
import datetime
from pathlib import Path

import fitz
from PIL import Image

from common import *


def generate_password(length: int = 40) -> str:
    '''
    Generate a secure password using a mix of letters, digits, and punctuation.
    :param length: Length of the password
    :return: Secure password string
    '''

    allowed_punctuation = ['@', '#', '$', '%', '&', '*', '!', '?', '+', '-', '=', '|', ':', ';']
    alphabet = string.ascii_letters + string.digits + ''.join(allowed_punctuation)
    password = ''.join(secrets.choice(alphabet) for _ in range(length))

    return password


def date_text(text: str) -> str:
    '''
    Generate a watermark text with the current date and time.
    :param text: Base text for the watermark
    :return: Watermark text with date and time
    '''

    now = datetime.datetime.now()
    date_str = now.strftime('%Y-%m-%d %H:%M:%S')
    text = text + f' - {date_str}'

    return text


def get_pdf_permissions(do_lock: bool) -> int:
    '''
    Get the permissions for the PDF document.
    :return: Permissions integer
    '''

    ALL = int(fitz.PDF_PERM_PRINT | fitz.PDF_PERM_MODIFY |
         fitz.PDF_PERM_COPY | fitz.PDF_PERM_ANNOTATE)
    
    return int(fitz.PDF_PERM_PRINT) if do_lock else ALL


def is_img(filename: str) -> bool:
    '''
    Check if the file is an image.
    :param filename: Path to the file
    :return: True if the file is an image, False otherwise
    '''

    return any(filename.lower().endswith(ext) for ext in SUPPORTED_IMAGE_FORMATS)


def img2pdf(input_filename: str) -> fitz.Document:
    '''
    Convert an image file to fitz PDF.
    :param input_filename: Path to the input image file
    :return: fitz.Document object
    '''

    if not is_img(input_filename):
        raise ValueError('Input file is not a valid image format.')
    
    # Open the image file
    img = Image.open(input_filename)
    img = img.convert('RGB')  # Convert to RGB if not already

    # Save the image to a BytesIO buffer in PNG format
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Create a new PDF document
    pdf = fitz.open()
    rect = fitz.Rect(0, 0, img.width, img.height)
    page = pdf.new_page(width=rect.width, height=rect.height)
    page.insert_image(rect, stream=img_bytes)

    return pdf


def get_new_pdf_filename(input_file_path: str) -> str:
    '''
    Generate a new filename for the output PDF, replacing any extension with .pdf.
    :param input_file_path: Path to the input file (image or PDF)
    :return: New filename for the output PDF
    '''

    p = Path(input_file_path)
    new_name = f'{p.stem}_marked.pdf'

    return str(p.with_name(new_name))


def open_document(input_filename: str) -> fitz.Document:
    '''
    Get the PDF document from the input file.
    :param input_filename: Path to the input file
    :return: fitz.Document object
    '''

    # Check if the input file is a PDF or an image
    if input_filename.lower().endswith('.pdf'):
        doc = fitz.open(input_filename)
    elif is_img(input_filename):
        doc = img2pdf(input_filename)
    else:
        raise ValueError('Input file is not a valid PDF or image format.')
    
    return doc


def save_pwd_to_file(owner_pw: str, input_filename: str) -> None:
    '''
    Save the password to a text file.
    :param owner_pw: Password for the PDF
    :param input_filename: Path to the input file
    '''

    p = Path(input_filename)
    pwd_file = p.with_suffix('.txt')

    with open(pwd_file, 'w') as f:
        f.write(owner_pw)
    