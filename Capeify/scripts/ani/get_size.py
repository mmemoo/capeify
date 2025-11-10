import struct
from ani_file import ani_file


def get_size(file):
    ani = ani_file.open(file, "r")

    curs = ani.getframesdata()
    png_data = curs[0]

    width, height = struct.unpack(">II", png_data[16:24])

    return width, height
