from wand.image import Image


def convert_cur2png(cur_file):
    with Image(filename=cur_file) as cur:
        largest = max(cur.sequence, key=lambda im: im.width * im.height)

        with Image(image=largest) as img:
            img.format = "png"
            png_data = img.make_blob()

    return png_data
