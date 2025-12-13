from Capeify.ani_file import ani_file


def get_frame_duration(file):
    ani = ani_file.open(file, "rb")

    duration = ani.getrate()

    if type(duration) is tuple:
        duration = sum(duration) / len(duration)

    duration = duration / 60

    return duration
