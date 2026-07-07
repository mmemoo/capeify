from PIL import Image, BmpImagePlugin
from io import BytesIO

BmpImagePlugin.USE_RAW_ALPHA = True


def convert_cur2png(cur_file):
    png_data = BytesIO()

    img = Image.open(cur_file)
    img.save(png_data, "png")

    png_data = png_data.getvalue()

    return png_data
