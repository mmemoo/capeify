from os import pread
from Capeify.ani_file import ani_file
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

    if len(pngs) > 24:
        n_frame_to_convert_to_1 = len(pngs) // 24

        if n_frame_to_convert_to_1 > 1:
            for i in range(
                n_frame_to_convert_to_1 - 1, len(pngs), n_frame_to_convert_to_1
            ):
                pngs[i - (n_frame_to_convert_to_1 - 2) : i + 1] = [0] * (
                    n_frame_to_convert_to_1 - 1
                )

            pngs = [png for png in pngs if png != 0]

        extra_frames = len(pngs) % 24

        if extra_frames:
            for i in range(1, extra_frames * 2, 2):
                pngs[i] = 0

            pngs = [png for png in pngs if png != 0]

    png_height_list = [png.height for png in pngs]

    png_height_sum = sum(png_height_list)

    png_max_height = max(png_height_list)
    png_max_width = max([png.width for png in pngs])

    final_png = Image.new("RGBA", (png_max_width, png_height_sum))

    y = 0
    for png in pngs:
        final_png.paste(png, (0, y))

        y += png_max_height

    png = BytesIO()
    final_png.save(png, "PNG")
    png = png.getvalue()

    return png, len(seq)
