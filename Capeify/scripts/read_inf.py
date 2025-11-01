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
