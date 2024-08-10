import os

from common import *


def cleanimg():
    '''Remove temporary image.'''

    path = get_temp_file_path(TEMP_IMG_FILEPATH)

    if os.path.exists(path):
        os.remove(path)


def cleanpdf():
    '''Remove temporary PDF.'''

    path = get_temp_file_path(TEMP_IMG_FILEPATH)

    if os.path.exists(path):
        os.remove(path)
