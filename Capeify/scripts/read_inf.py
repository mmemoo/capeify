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
                key, val = key.strip().replace(",", ""), val.strip().replace(",", "")

                dict_[key] = val

            if "[DefaultInstall" in line.strip():
                in_defaultInstall = True

    return dict_


def read_reg_fallback(path):
    result = read_reg_wreg_settings(path)
    if result:
        return result

    result = read_reg(path, "Scheme.Reg")
    if result:
        strings = read_strings(path)
        resolved = []
        for cur in result:
            cur_lower = cur.lower().replace("%", "")
            if cur_lower in strings:
                resolved.append(strings[cur_lower])
        if resolved:
            return resolved

    return None


def read_reg_wreg_settings(path):
    for section in ["Wreg", "Settings"]:
        cursors = {}
        in_section = False
        with open(path, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line == f"[{section}]":
                    in_section = True
                    continue
                if in_section:
                    if line.startswith("[") and line.endswith("]"):
                        break
                    if line and not line.startswith("HK"):
                        continue
                    if "," in line:
                        parts = line.split(",")
                        if len(parts) >= 3:
                            cursor_key = parts[2].strip().replace('"', "")
                            cursor_path = parts[-1].strip().replace('"', "")
                            if "%" in cursor_path:
                                cursor_name = cursor_path.split("\\")[-1].replace(
                                    "%", ""
                                )
                                if cursor_name:
                                    cursors[cursor_key.lower()] = cursor_name
        if cursors:
            return cursors
    return None


def read_reg(path, reg_sect):
    in_reg = False
    with open(path, "r") as f:
        for line in f.readlines():
            if in_reg and line.strip() != "":
                read_csv = csv.reader([line.strip()])
                read_csv = next(read_csv)
                reg_str = read_csv[-1]

                curs = reg_str.split(",")
                curs = [cur.split("\\")[-1][1:-1] for cur in curs]

                return curs

            if line.strip() == f"[{reg_sect}]":
                in_reg = True


def read_reg_wreg(path):
    cursors = {}
    in_wreg = False
    with open(path, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "[Wreg]":
                in_wreg = True
                continue
            if in_wreg:
                if line.startswith("[") and line.endswith("]"):
                    break
                if line and not line.startswith("HK"):
                    continue
                if "," in line:
                    parts = line.split(",")
                    if len(parts) >= 3:
                        cursor_key = parts[2].strip().replace('"', "")
                        cursor_path = parts[-1].strip().replace('"', "")
                        if "%" in cursor_path:
                            cursor_name = cursor_path.split("\\")[-1].replace("%", "")
                            if cursor_name:
                                cursors[cursor_key.lower()] = cursor_name
    return cursors if cursors else None
