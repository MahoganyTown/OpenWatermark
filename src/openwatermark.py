import parse
import clean
import imgstamp
import pdfstamp
from file import File
from common import *
from forge import *


def mark_img(file: File, text: str, font: str, color: tuple[int]) -> None:
    '''
    Apply watermark on image.

        text: watermark text.
        font: name of font.
        color: text color.
    '''

    size = imgstamp.get_dims(file.path)
    watermark = new_watermark(text, font, size, color)
    imgstamp.save_image_as_png(watermark, TEMP_IMG_FILEPATH)
    imgstamp.stamp(file.path, TEMP_IMG_FILEPATH)
    clean.cleanimg()


def mark_pdf(file: File, text: str, 
             font: str, color: tuple[int], 
             pages: tuple[int]) -> None:
    '''
    Apply watermark on PDF document.

        text: watermark text.
        font: name of font.
        color: text color.
    '''

    size = pdfstamp.get_dims(file.path)
    watermark = new_watermark(text, font, size, color)
    pdfstamp.save_image_as_pdf(watermark, TEMP_PDF_FILEPATH)
    pdfstamp.stamp(file.path, TEMP_PDF_FILEPATH, size, pages)
    clean.cleanpdf()


def run() -> None:
    # Parse arguments
    args = parse.parse()
    
    # Generate watermark for each file
    for filepath in args['files']:
        file = File(filepath)

        if file.is_image():
            mark_img(file, args['text'], args['font'], args['color'])
        else:
            mark_pdf(file, args['text'], args['font'], args['color'], args['pages'])


if __name__ == '__main__':
    run()
