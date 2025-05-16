import numpy as np
from PIL import Image


def add_film_grain(image: Image, intensity: float = 0.1) -> np.ndarray:
    '''
    Adds film grain noise to an RGB image.
    :param image: Input image (numpy array, uint8, shape HxWx3)
    :param intensity: Grain intensity (0-1)
    :return: Noisy image
    '''

    noise = np.random.normal(0, intensity * 255, image.shape).astype(np.float32)
    noisy = image.astype(np.float32) + noise

    return np.clip(noisy, 0, 255).astype(np.uint8)


def add_banding_noise(image: Image, band_width: int = 5, amplitude: int = 15, 
    orientation: str = 'horizontal') -> np.ndarray:
    '''
    Adds banding noise to an RGB image.
    :param image: Input image (numpy array, uint8, shape HxWx3)
    :param band_width: Width of each band in pixels
    :param amplitude: Intensity of the bands
    :param orientation: 'horizontal' or 'vertical'
    :return: Noisy image
    '''

    noisy = image.astype(np.float32)

    if orientation == 'horizontal':
        for i in range(0, image.shape[0], band_width * 2):
            noisy[i:i+band_width, :, :] += amplitude
    else:
        for i in range(0, image.shape[1], band_width * 2):
            noisy[:, i:i+band_width, :] += amplitude

    return np.clip(noisy, 0, 255).astype(np.uint8)


def add_shot_noise(image: Image) -> np.ndarray:
    '''
    Adds shot (Poisson) noise to an RGB image.
    :param image: Input image (numpy array, uint8, shape HxWx3)
    :return: Noisy image
    '''

    image_float = image.astype(np.float32) / 255.0
    noisy = np.random.poisson(image_float * 255) / 255.0

    return np.clip(noisy * 255, 0, 255).astype(np.uint8)


def add_periodic_noise(image: Image, frequency: float = 10, amplitude: float = 20, 
    orientation='horizontal') -> np.ndarray:
    '''
    Adds periodic (sinusoidal) noise to an RGB image.
    :param image: Input image (numpy array, uint8, shape HxWx3)
    :param frequency: Frequency of the sine wave
    :param amplitude: Amplitude of the noise
    :param orientation: 'horizontal' or 'vertical'
    :return: Noisy image
    '''

    noisy = image.astype(np.float32)

    if orientation == 'horizontal':
        rows = image.shape[0]
        sine_wave = amplitude * np.sin(2 * np.pi * np.arange(rows) / frequency)
        sine_wave = sine_wave[:, None, None]  # shape (rows, 1, 1)
        noisy += sine_wave
    else:
        cols = image.shape[1]
        sine_wave = amplitude * np.sin(2 * np.pi * np.arange(cols) / frequency)
        sine_wave = sine_wave[None, :, None]  # shape (1, cols, 1)
        noisy += sine_wave

    return np.clip(noisy, 0, 255).astype(np.uint8)
