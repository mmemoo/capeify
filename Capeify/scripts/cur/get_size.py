import struct


def get_size(png_data):
    width, height = struct.unpack(">II", png_data[16:24])

    return width, height
