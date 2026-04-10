import csv
from os import read


def read_strings(path):
    with open(path, "r") as f:
        strings = {}
        in_strings = False
        for line in f.readlines():
            line = line.strip()

            if in_strings and line.strip() != "":
                key, val = line.split("=")
                key, val = key.strip(), val.strip()

                strings[key] = val[1:-1]

            if line != "" and len(line) >= 2:
                if line[0] == "[" and line[-1] == "]" and in_strings:
                    break

            if line == "[Strings]":
                in_strings = True

    return strings


def read_defaultInstall(path):
    dict_ = {}
    in_defaultInstall = False
    with open(path, "r") as f:
        for line in f.readlines():
            if line != "" and len(line) >= 2:
                if (
                    line.strip()[0] == "["
                    and line.strip()[-1] == "]"
                    and in_defaultInstall
                ):
                    break

            if in_defaultInstall and line.strip() != "":
                key, val = line.strip().split("=")
                key, val = key.strip(), val.strip().split(",")
                dict_[key] = val

            if "[DefaultInstall" in line.strip():
                in_defaultInstall = True

    return dict_


def read_reg(path: str, reg_header: str) -> str:
    """
    get raw string from given reg header
    """
    in_reg = False
    reg_raw = ""
    with open(path, "r") as f:
        for line in f.readlines():
            if line.strip() == "":
                continue
            elif line.strip() == f"[{reg_header}]":
                in_reg = True
            elif line.strip()[0] == "[" and in_reg:
                return reg_raw
            elif in_reg:
                reg_raw += line


idx_2_win_cur_identifier = {
    0: "Arrow",
    1: "Help",
    2: "AppStarting",
    3: "Wait",
    4: "Crosshair",
    5: "IBeam",
    6: "NWPen",
    7: "No",
    8: "SizeNS",
    9: "SizeWE",
    10: "SizeNWSE",
    11: "SizeNESW",
    12: "SizeAll",
    13: "UpArrow",
    14: "Hand",
    15: "Pin",
    16: "Person",
}


def parse_reg(reg_raw: str, sep: str) -> dict[str, str]:
    """
    parse a raw reg string to get the cursors

    returns a dict with the structure win_cursor_identifier : cursor file name/variable reference
    """
    if sep == ",":
        """
        case where reg_raw is something like:
        HKCU,"Control Panel\\Cursors\\Schemes","%SCHEME_NAME%",,"%10%\\%CUR_DIR%\\%Arrow%,%10%\\%CUR_DIR%\\%Help%,%10%\\%CUR_DIR%\\%AppStarting%...
        """
        reg_parsed = reg_raw.split(sep)
        reg_parsed = [elem for elem in reg_parsed if elem]
        cursors = []

        for elem in reg_parsed[3:]:
            elem = elem.split("\\")[-1].strip()
            elem = elem[:-1] if elem.endswith('"') else elem

            # Not removing the %'s so i can check if the string is a variable reference or not in main.py
            cursors.append(elem)

        cursors = {idx_2_win_cur_identifier[i]: cur for i, cur in enumerate(cursors)}

        return cursors
    elif sep == "\n":
        """
        case where reg_raw is something like:
        HKCU,"Control Panel\\Cursors",,0x00020000,"%SCHEME_NAME%"
        HKCU,"Control Panel\\Cursors",AppStarting,0x00020000,"%10%\\%CUR_DIR%\\%working%"
        HKCU,"Control Panel\\Cursors",Arrow,0x00020000,"%10%\\%CUR_DIR%\\%pointer%"
        HKCU,"Control Panel\\Cursors",crosshair,0x00020000,"%10%\\%CUR_DIR%\\%precision%"
        ...
        """
        reg_parsed = reg_raw.split(sep)
        reg_parsed = [elem for elem in reg_parsed if elem]
        cursors = {}

        for elem in reg_parsed[1:-1]:
            elem = elem.split(",")

            win_cur_identifier = elem[2]
            cur = elem[4].split("\\")[2]
            cur = cur[:-1] if cur.endswith('"') else cur

            cursors[win_cur_identifier] = cur

        return cursors


def determine_sep(reg: str) -> str:
    """
    determine the seperator in the reg

    returns the seperator with the type "str"
    """

    return "\n" if "\n" in reg.strip() else ","
