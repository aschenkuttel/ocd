from os.path import isdir, isfile
from os import listdir
import sys
import re


def main():
    if len(sys.argv) == 1:
        print("missing required argument: path")
        return

    path = sys.argv[1]
    if isfile(path):
        if not path.endswith(".py"):
            print("only .py files supported")
            return

        else:
            try:
                clean_up(path)
            except Exception as error:
                print(f"something unexpected happened\n{error}")
            else:
                print("file succesfully cleaned")

    elif isdir(path):
        succeeded = 0
        tmp = listdir(path)
        files = [f for f in tmp if f.endswith('.py')]

        for file in files:
            tmp_path = f"{path}\\{file}"
            try:
                clean_up(tmp_path)
                succeeded += 1
            except Exception as error:
                print(f"something unexpected happened\n{error}")
                continue

        print(f"script cleaned {succeeded}/{len(files)} files")

    else:
        print("invalid path mate")
        return


def clean_up(path):
    with open(path, 'r') as file:
        data = file.readlines()

    begin = 0
    till = None
    skipper = False
    for index, line in enumerate(data):
        if line.startswith("import ") or line.startswith("from "):
            if line.endswith("\\\n"):
                skipper = True
            continue
        elif line != "\n":
            if skipper:
                if line.endswith("\\\n"):
                    skipper = True
                else:
                    skipper = False

            else:
                begin = index
                break

        else:
            if till is None:
                till = index

    if till == 0:
        print("no imports at all, lol")
        return

    elif till is None:
        till = len(data) + 1

    last_line = ""
    import_output = []
    relevant_data = data[:till]
    for line in relevant_data:

        if line.endswith("\\\n"):
            last_line += line

        else:
            if last_line:
                line = f"{last_line}{line}"
                last_line = ""

            chopped = line.replace("\\\n", "")
            trimmed = re.sub(' +', ' ', chopped)
            import_output.append(trimmed.strip())

    sort = sorted(import_output, key=lambda l: len(l), reverse=True)
    raw_str, sort_str = "".join(relevant_data), "\n".join(sort)
    rest = "".join(data[begin:])
    result = f"{sort_str}\n\n\n{rest}"

    with open(path, 'w') as file:
        file.write(result)


if __name__ == "__main__":
    main()
