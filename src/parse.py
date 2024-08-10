import os
import argparse


def parse() -> dict:
    '''Parse arguments.'''

    def parse_color(raw: str) -> tuple[int]:
        '''Parse color.'''

        channels = raw.split(',')
        names = ['R', 'G', 'B', 'A']
        color = []

        if len(channels) != 4:
            raise Exception('Error: color must be in format R,G,B,A (0-255)')

        for name, channel in zip(names, channels):
            if channel.isdigit():
                amount = int(channel)

                if amount >= 0 and amount <= 255:
                    color.append(amount)
                else:
                    raise Exception('Error: color channel %s out of range.' % name)
            else:
                raise Exception('Error: color channel %s must be a number.' % name)

        return tuple(color)


    def parse_pages(raw: str) -> tuple[int]:
        '''Parse page numbers.'''

        numbers = raw.split(',')
        pages = []

        # Return empty if no pages given (all pages to watermark)
        if len(numbers) == 1 and len(numbers[0]) == 0:
            return ()
        
        for number in numbers:
            if number.isdigit():
                n = abs(int(number)) - 1

                if n >= 0:
                    pages.append(n)
                else:
                    raise Exception('Error: page numbers start at 1.')
            else:
                raise Exception('Error: %s must be a number.' % number)

        return tuple(pages)


    parser = argparse.ArgumentParser(
                    prog='OpenWatermark',
                    description='Apply watermarks on images and PDF documents.',
                    epilog='Developed by Boduru.')
    
    parser.add_argument('files', nargs='+', type=str,  
                        help='Files to watermark.')
    
    parser.add_argument('-t', '--text', type=str, 
                        help='Text of watermark.',
                        default='OpenWatermark')
    
    parser.add_argument('-f', '--font', type=str,
                        help='Font of watermark. ',
                        default='')
    
    parser.add_argument('-p', '--pages', type=str,
                        help='Pages to watermak: x,y,z.', 
                        default='')
    
    parser.add_argument('-c', '--color', type=str,
                        help='Color of watermark (format: R,G,B,A) O-255.', 
                        default='128,128,128,196')
    
    args = parser.parse_args()

    # Unpack arguments
    files = args.files
    text = args.text
    font = args.font

    # Check files
    for file in files:
        if not os.path.isfile(file):
            raise Exception('Error: %s not found.' % file)

    # Parse color
    color = parse_color(args.color)

    # Parse pages
    pages = parse_pages(args.pages)

    # Bundle arguments in dict
    out_args = {
        'files': files,
        'text': text,
        'font': font,
        'color': color,
        'pages': pages,
    }

    return out_args
