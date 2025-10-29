from typing import final
from ani_file import ani_file
from PIL import Image
from io import BytesIO


def convert2pngs(file):
    ani = ani_file.open(file, "r")

    curs = ani.getframesdata()
    curs = [Image.open(BytesIO(cur)) for cur in curs]

    pngs = []
    for cur in curs:
        png = BytesIO()
        cur.save(png, "PNG")

        pngs.append(png)

    return pngs


def convert2png(file, pngs):
    ani = ani_file.open(file)
    seq = ani.getseq()

    pngs = [pngs[i] for i in seq]
    pngs = [Image.open(png) for png in pngs]

    png_height_sum = sum([png.height for png in pngs])
    png_max_width = max([png.width for png in pngs])

    final_png = Image.new("RGB", (png_max_width, png_height_sum))

    y = 0
    for png in pngs:
        final_png.paste(png, (0, y))

        y += png.height

    png = BytesIO()
    final_png.save(png, "PNG")
    png = png.getvalue()

    return png
