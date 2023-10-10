import numpy as np
from PIL import Image, ImageOps

INKPLATE_WIDTH = 1200
INKPLATE_HEIGHT = 825


def resize_to_inkplate10_size(im: Image) -> Image:
    return ImageOps.pad(im, (INKPLATE_WIDTH, INKPLATE_HEIGHT), color="white")


def convert_to_raw_1bpp(im: Image) -> bytes:
    image = im.convert("1", dither=Image.Dither.FLOYDSTEINBERG)
    data = np.array(image.getdata(), dtype=np.uint8)
    return np.invert(np.packbits(data, bitorder="little")).tobytes()


def convert_to_raw_4bpp(im: Image) -> bytes:
    image = im.convert("L")
    image = ImageOps.invert(image)
    image = image.quantize(8, dither=Image.Dither.FLOYDSTEINBERG)

    data = np.array(image.getdata(), dtype=np.uint8)
    data = np.reshape(data, newshape=(-1, 2))

    return np.bitwise_or(np.left_shift(data[:, 0], 4), data[:, 1]).tobytes()
