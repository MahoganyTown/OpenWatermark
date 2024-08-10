from PIL import Image

from common import get_temp_file_path


def get_dims(filepath: str) -> tuple[int, int]:
    '''Return width and height of image.'''

    with Image.open(filepath) as img:
        return img.size
    

def save_image_as_png(image: Image, path: str) -> None:
    '''Save image as PNG file with transparency.'''

    # Save in staging area
    path = get_temp_file_path(path)

    image.save(path, format='png')


def stamp(file: str, template: str) -> None:
    '''
    Watermark image using a watermark image template.

        file: image to watermark.
        template: image containing watermark template.
        dims: size of image.
    '''

    image = Image.open(file)
    watermark = Image.open(get_temp_file_path(template))

    image.paste(watermark, (0, 0), watermark)

    # Save new image
    outpath = '{}_{}'.format(file[:-4], 'watermarked.png')
    image.save(outpath)
    print('%s done!' % outpath)
