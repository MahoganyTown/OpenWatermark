from common import get_temp_file_path
from io import BytesIO

import img2pdf
from PyPDF2 import PdfReader
from pikepdf import Pdf, Page, Rectangle
from PIL import Image


def get_dims(filepath: str) -> tuple[int, int]:
    '''Return width and height of first PDF page.'''

    reader = PdfReader(filepath)
    w = reader.pages[0].mediabox.width
    h = reader.pages[0].mediabox.height

    return (round(w), round(h))


def save_image_as_pdf(image: Image, path: str) -> None:
    '''
    Save image as PDF file.
    
        image: image to convert and save as PDF.
        path: PDF file path.
    '''

    temp = BytesIO()
    image.save(temp, format='png')

    # Save in staging area
    path = get_temp_file_path(path)

    with open(path, 'wb') as f:
        f.write(img2pdf.convert(temp.getvalue()))


def stamp(file: str, template: str, dims: tuple[int], pages: tuple[int]) -> None:
    '''
    Watermark PDF document using a watermark PDF template.

        file: PDF document to watermark.
        template: PDF document containing watermark template.
        dims: resolution of PDF pages.
        pages: pages to watermake.
    '''

    # Open file and template
    pdf = Pdf.open(file)
    water = Pdf.open(get_temp_file_path(template))

    # Get watermark
    water_page = Page(water.pages[0])

    # If pages is Null, apply on all pages
    if not len(pages):
        pages = range(len(pdf.pages))
        
    # Apply on selected pages
    for i in pages:
        pdf_page = Page(pdf.pages[i])
        pdf_page.add_overlay(water_page, Rectangle(0, 0, *dims))

    # Save new PDF document
    outpath = '{}_{}'.format(file[:-4], 'watermarked.pdf')
    pdf.save(outpath)
    print('%s done!' % outpath)