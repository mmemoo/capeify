from PIL import Image
import io


def convert_cur2png(cur_file):
    with open(cur_file, "rb") as f:
        cur_bytes = f.read()
        cur_bytes = io.BytesIO(cur_bytes)

    cur = Image.open(cur_bytes)

    png = io.BytesIO()
    cur.save(png, "PNG")

    return png.getvalue()
