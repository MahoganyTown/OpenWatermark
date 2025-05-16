import random


def random_font(available_fonts: list) -> str:
    '''
    Generate a random font name from the available fonts.
    :return: Random font name
    '''

    return random.choice(available_fonts)


def random_font_size(font_size_range: tuple) -> int:
    '''
    Generate a random font size for the watermark.
    :return: Random font size
    '''

    return random.randint(font_size_range[0], font_size_range[1])


def random_greyish_color():
    '''
    Generate a random greyish color.
    :return: Tuple of RGB values
    '''

    base = random.uniform(0, 0.4)  # Controls darkness (black to dark grey)
    tint = random.uniform(-0.05, 0.05)  # Small color deviation

    r = min(max(base + random.uniform(-tint, tint), 0), 1)
    g = min(max(base + random.uniform(-tint, tint), 0), 1)
    b = min(max(base + random.uniform(-tint, tint), 0), 1)

    return (r, g, b)


def random_range(range_tuple: tuple) -> float:
    '''
    Generate a random value within a specified range.
    :param range_tuple: Tuple containing the min and max values
    :return: Random value within the range
    '''

    return random.uniform(range_tuple[0], range_tuple[1])
