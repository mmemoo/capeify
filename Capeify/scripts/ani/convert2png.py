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

    pngs = [png.getvalue() for png in pngs]

    return pngs
