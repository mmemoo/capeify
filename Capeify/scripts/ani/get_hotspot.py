import struct


def get_cur_hotspot(data):
    _, _, cur_count = struct.unpack("<HHH", data[:6])

    cur_sizes = []
    cur_hotspots = []

    for i in range(cur_count):
        _, hotspot_x, hotspot_y, cur_size, _ = struct.unpack(
            "<4sHHII", data[i * 16 + 6 : (i + 1) * 16 + 6]
        )

        cur_sizes.append(cur_size)
        cur_hotspots.append((hotspot_x, hotspot_y))

    size_n_hotspot = [
        (size, hotspot_x, hotspot_y)
        for size, (hotspot_x, hotspot_y) in zip(cur_sizes, cur_hotspots)
    ]
    max_sizes_hotspot = max(size_n_hotspot, key=lambda x: x[0])

    hotspot_x, hotspot_y = max_sizes_hotspot[1], max_sizes_hotspot[2]

    return hotspot_x, hotspot_y
