import struct
from Capeify.ani_file import ani_file
from PIL import Image
from io import BytesIO


def get_size(file):
    ani = ani_file.open(file, "r")

    curs = ani.getframesdata()
    cur = Image.open(BytesIO(curs[0]))

    w, h = cur.size

    return w, h
