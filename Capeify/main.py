from Capeify.scripts.cur import convert2png as c_convert2png
from Capeify.scripts.cur import get_hotspot as c_get_hotspot
from Capeify.scripts.cur import get_size as c_get_size

from Capeify.scripts.ani import convert2png as a_convert2png
from Capeify.scripts.ani import get_hotspot as a_get_hotspot
from Capeify.scripts.ani import get_frame_duration as a_get_frame_duration
from Capeify.scripts.ani import get_size as a_get_size

from Capeify.scripts import create_xml
from Capeify.scripts import read_inf

from base64 import b64encode

import argparse

from time import time

win2mac_cur = {
    0: ["com.apple.coregraphics.Arrow"],
    1: ["com.apple.cursor.40"],
    2: ["com.apple.cursor.4"],
    3: ["com.apple.coregraphics.Wait"],
    4: ["com.apple.cursor.7", "com.apple.cursor.8", "com.apple.cursor.41"],
    5: ["com.apple.coregraphics.IBeam"],
    6: None,
    7: ["com.apple.cursor.3"],
    8: [
        "com.apple.cursor.32",
        "com.apple.cursor.21",
        "com.apple.cursor.22",
        "com.apple.cursor.23",
        "com.apple.cursor.31",
        "com.apple.cursor.36",
    ],
    9: [
        "com.apple.cursor.28",
        "com.apple.cursor.17",
        "com.apple.cursor.18",
        "com.apple.cursor.19",
        "com.apple.cursor.27",
        "com.apple.cursor.38",
    ],
    10: ["com.apple.cursor.34", "com.apple.cursor.33", "com.apple.cursor.35"],
    11: ["com.apple.cursor.30", "com.apple.cursor.29", "com.apple.cursor.37"],
    12: ["com.apple.cursor.39"],
    13: ["com.apple.cursor.2"],
    14: ["com.apple.cursor.13"],
    15: None,
    16: None,
}


def convert(args):
    start = time()

    inf_file_path = f"{args.path}/{args.inf_file}"

    strings = read_inf.read_strings(inf_file_path)
    strings = {key.lower(): val for key, val in strings.items()}

    reg_sect = read_inf.read_defaultInstall(inf_file_path)["AddReg"]
    reg = read_inf.read_reg(inf_file_path, reg_sect)

    cursors = []
    for idx, win_cur in enumerate(reg):
        if win2mac_cur[idx]:
            path = f"{args.path}/{strings[win_cur.lower()]}"
            ext = strings[win_cur.lower()][-3:]
            if ext == "cur":
                data = c_convert2png.convert_cur2png(path)

                data_enc = b64encode(data)
                data_enc = data_enc.decode()

                hs_x, hs_y = c_get_hotspot.get_hotspot(path)
                w, h = c_get_size.get_size(data)

                for cur_name in win2mac_cur[idx]:
                    cursors.append(
                        create_xml.create_cursor(
                            cur_name,
                            1,
                            1,
                            hs_x,
                            hs_y,
                            h,
                            w,
                            data_enc,
                        )
                    )

            if ext == "ani":
                pngs = a_convert2png.convert2pngs(path)

                data, real_frame_count = a_convert2png.convert2png(path, pngs)
                lowered_frame_count = min(real_frame_count, 24)

                data_enc = b64encode(data)
                data_enc = data_enc.decode()

                hs_x, hs_y = a_get_hotspot.get_hotspot(path)
                w, h = a_get_size.get_size(path)

                frame_dur = a_get_frame_duration.get_frame_duration(path)
                frame_dur = (frame_dur * real_frame_count) / lowered_frame_count

                for cur_name in win2mac_cur[idx]:
                    cursors.append(
                        create_xml.create_cursor(
                            cur_name,
                            lowered_frame_count,
                            frame_dur,
                            hs_x,
                            hs_y,
                            h,
                            w,
                            data_enc,
                        )
                    )

        print(f'CAPEIFY $$ Cursor "{win_cur}" done.')

    cur_pack_name = args.path.split("/")[-1]

    cape = create_xml.create_cape(
        cur_pack_name + "_author", cur_pack_name, cursors, cur_pack_name + "_identifier"
    )
    cape.write(args.out, pretty_print=True)

    print(f"CAPEIFY $$ Conversion done! Time elapsed : {time() - start} seconds.")


def main():
    parser = argparse.ArgumentParser(prog="capeify", description="Capeify")

    subparsers = parser.add_subparsers(title="commands")

    convert_parser = subparsers.add_parser(
        "convert", help="Convert a windows cursor package to a cape file."
    )

    convert_parser.add_argument(
        "--path",
        required=True,
        help="Path to the windows cursor package. Should be absolute.",
    )

    convert_parser.add_argument(
        "--inf-file",
        required=True,
        help="The name of the inf file in the specified path.",
    )

    convert_parser.add_argument(
        "--out", required=True, help="The path of the out file."
    )

    convert_parser.set_defaults(func=convert)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
