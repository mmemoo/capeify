from ani_file import ani_file
from wand.image import Image as WImage
from io import BytesIO
from PIL import Image


def convert2pngs(file):
    ani = ani_file.open(file, "r")

    curs = ani.getframesdata()

    pngs = []
    for cur in curs:
        with WImage(blob=cur, format="cur") as img:
            img.format = "png"
            png_data = img.make_blob()

        png_data = BytesIO(png_data)
        pngs.append(png_data)

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
