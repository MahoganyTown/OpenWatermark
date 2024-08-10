# Temporary file paths
TEMP_IMG_FILEPATH = 'watermark001_temporary_file.png'
TEMP_PDF_FILEPATH = 'watermark001_temporary_file.pdf'

import os
import tempfile

def get_temp_file_path(filename: str) -> str:
    '''
    Return complete file path to temporary file.

        filename: name of file with extension.
    '''

    return os.path.join(tempfile.gettempdir(), filename)