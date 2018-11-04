import argparse
import os
import sys
from typing import List

import pry

from .audiofile import audiofile_bugs
from .bug import Bug
from .coreutils import coreutils_bugs
from .file import file_bugs
from .flac import flac_bugs
from .hemiptera import read_bug_ids_per_project
from .jasper import jasper_bugs
from .libgd import libgd_bugs
from .libjpeg_turbo import libjpeg_turbo_bugs
from .libtiff import libtiff_bugs
from .tcpdump import tcpdump_bugs
from .utils import REPORT_PATH
from .w3m import w3m_bugs
from .zlib import zlib_bugs
from .libtasn import libtasn_bugs


def all_bugs() -> List[Bug]:
    os.makedirs(REPORT_PATH, exist_ok=True)

    bug_ids = read_bug_ids_per_project()

    os.environ["FORCE_UNSAFE_CONFIGURE"] = "1"
    # nixos shenanigans
    os.environ["hardeningDisable"] = "all"
    # breaks file build
    os.environ["ASAN_OPTIONS"] = "detect_leaks=0"

    # bugs = coreutils_bugs() + audiofile_bugs()
    bugs = (
        coreutils_bugs()
        + w3m_bugs(bug_ids["w3m"])
        + file_bugs(bug_ids["file"])
        + audiofile_bugs(bug_ids["audiofile"])
        + libtiff_bugs(bug_ids["libtiff"])
        + jasper_bugs(bug_ids["jasper"])
        + flac_bugs(bug_ids["libflac"])
        + zlib_bugs(bug_ids["zlib"])
        + tcpdump_bugs(bug_ids["tcpdump"])
        + libjpeg_turbo_bugs(bug_ids["libjpeg-turbo"])
        + libtasn_bugs(bug_ids["libtasn"])
        # this is marked as "ongoing" in hemiptera
        #+ libgd_bugs(bug_ids["libgd"])
    )
    return bugs


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=args[0])
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument("--by_angr", action="store_true")
    parser.add_argument("--name")
    return parser.parse_args(args[1:])


def main():
    args = parse_args(sys.argv)
    bugs = all_bugs()
    for bug in bugs:
        if args.name is None or args.name == bug.name:
            bug.simulate = args.simulate
            bug.by_angr = args.by_angr

            with pry:
                bug.reproduce(build_only=args.build_only)


if __name__ == "__main__":
    main()
