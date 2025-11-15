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
