from typing import NamedTuple
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
from lxml import etree

win2mac_cur = {
    "Arrow": ["com.apple.coregraphics.Arrow"],
    "Help": ["com.apple.cursor.40"],
    "AppStarting": ["com.apple.cursor.4"],
    "Wait": ["com.apple.coregraphics.Wait"],
    "Crosshair": ["com.apple.cursor.7", "com.apple.cursor.8", "com.apple.cursor.41"],
    "IBeam": ["com.apple.coregraphics.IBeam"],
    "NWPen": None,
    "No": ["com.apple.cursor.3"],
    "SizeNS": [
        "com.apple.cursor.32",
        "com.apple.cursor.21",
        "com.apple.cursor.22",
        "com.apple.cursor.23",
        "com.apple.cursor.31",
        "com.apple.cursor.36",
    ],
    "SizeWE": [
        "com.apple.cursor.28",
        "com.apple.cursor.17",
        "com.apple.cursor.18",
        "com.apple.cursor.19",
        "com.apple.cursor.27",
        "com.apple.cursor.38",
    ],
    "SizeNWSE": ["com.apple.cursor.34", "com.apple.cursor.33", "com.apple.cursor.35"],
    "SizeNESW": ["com.apple.cursor.30", "com.apple.cursor.29", "com.apple.cursor.37"],
    "SizeAll": ["com.apple.cursor.39"],
    "UpArrow": ["com.apple.cursor.2"],
    "Hand": ["com.apple.cursor.13"],
    "Pin": None,
    "Person": None,
}


def convert_(path: str, inf_file: str, log: bool) -> etree:
    """
    converts given windows cursor pack to a cape file according to given args

    path : str -> path of the windows cursor pack
    inf_file : str -> name of the .INF file to be used

    log : bool -> bool to specify if the fn should log the progress

    returns -> xml data of the cape file as a string
    """
    inf_file_path = f"{path}/{inf_file}"

    strings = read_inf.read_strings(inf_file_path)
    strings = {key.lower(): val for key, val in strings.items()}

    reg_header = read_inf.read_defaultInstall(inf_file_path)["AddReg"][0]
    reg_header = reg_header.split(",")[0]
    raw_reg = read_inf.read_reg(inf_file_path, reg_header)
    reg_sep = read_inf.determine_sep(raw_reg)
    parsed_reg = read_inf.parse_reg(raw_reg, reg_sep)

    cursors = []
    for win_cur_identifier, win_cur in parsed_reg.items():
        if win_cur.split() == "":
            continue
        if win2mac_cur[win_cur_identifier]:
            win_cur_file = (
                strings[win_cur.lower()[1:-1]]
                if win_cur[0] == "%" and win_cur[-1] == "%"
                else win_cur
            )
            file_path = f"{path}/{win_cur_file}"
            ext = win_cur_file[-3:]
            if ext == "cur":
                data = c_convert2png.convert_cur2png(file_path)

                data_enc = b64encode(data)
                data_enc = data_enc.decode()

                hs_x, hs_y = c_get_hotspot.get_hotspot(file_path)
                w, h = c_get_size.get_size(data)

                for cur_name in win2mac_cur[win_cur_identifier]:
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
                pngs = a_convert2png.convert2pngs(file_path)

                data, real_frame_count = a_convert2png.convert2png(file_path, pngs)
                lowered_frame_count = min(real_frame_count, 24)

                data_enc = b64encode(data)
                data_enc = data_enc.decode()

                hs_x, hs_y = a_get_hotspot.get_hotspot(file_path)
                w, h = a_get_size.get_size(file_path)

                frame_dur = a_get_frame_duration.get_frame_duration(file_path)
                frame_dur = (frame_dur * real_frame_count) / lowered_frame_count

                for cur_name in win2mac_cur[win_cur_identifier]:
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

            print(f"CAPEIFY $$ Cursor {win_cur_file} done.") if log else None

    cur_pack_name = path.split("/")[-1]

    cape = create_xml.create_cape(
        cur_pack_name + "_author", cur_pack_name, cursors, cur_pack_name + "_identifier"
    )

    return cape


def convert(args: NamedTuple) -> None:
    """
    the main fn to be passed to the parser

    args : NamedTuple -> args input by the user
    """

    start = time()

    xml = convert_(args.path, args.inf_file, True)
    xml.write(args.out, pretty_print=True)

    print(f"CAPEIFY $$ Conversion done! Time elapsed : {(time() - start):.4f} seconds.")


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
