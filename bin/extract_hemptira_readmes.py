#!/usr/bin/env python
import os
import re
import sys
from pathlib import Path
from typing import List


def natural_sort(l: List[str]) -> List[str]:
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(l, key=alphanum_key)


def main() -> None:
    if len(sys.argv) < 2:
        print("USAGE: {} directory".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    directory = Path(sys.argv[1])

    for entry in natural_sort(os.listdir(str(directory))):
        bug_dir = directory.joinpath(entry)
        if not bug_dir.is_dir():
            continue
        match = re.match(r"ID-(\d+)", str(entry))
        if not match:
            print("ignore {}".format(bug_dir), file=sys.stderr)
            continue
        bug_id = match.group(1)
        readme_path = bug_dir.joinpath("README")
        print("## {}".format(bug_id))
        trigger = re.compile(".*trigger:.*", re.IGNORECASE)

        if readme_path.exists():
            with open(str(readme_path)) as f:
                found_trigger = False
                for line in f:
                    if trigger.match(line):
                        found_trigger = True
                        continue
                    elif not found_trigger:
                        continue
                    print("# {}".format(line), end="")
        print("")


if __name__ == "__main__":
    main()
