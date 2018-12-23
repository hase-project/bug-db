import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

from ipdb import launch_ipdb_on_exception

from .audiofile import audiofile_bugs
from .bug import Bug
from .coreutils import coreutils_bugs
from .file import file_bugs
from .flac import flac_bugs
from .hemiptera import read_bug_ids_per_project
from .jasper import jasper_bugs
from .libgd import libgd_bugs
from .libjpeg_turbo import libjpeg_turbo_bugs
from .libtasn import libtasn_bugs
from .libtiff import libtiff_bugs
from .tcpdump import tcpdump_bugs
from .utils import REPORT_PATH
from .w3m import w3m_bugs
from .zlib import zlib_bugs


def all_bugs() -> List[Bug]:
    REPORT_PATH.mkdir(parents=True, exist_ok=True)

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
        # + libgd_bugs(bug_ids["libgd"])
    )
    return bugs


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=args[0])
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument("--by-angr", action="store_true")
    parser.add_argument("--name", nargs="+")
    return parser.parse_args(args[1:])


def parse_args_benchmark(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=args[0])
    parser.add_argument("--name", nargs="+")
    parser.add_argument("--run", type=int, default=3, help="The number of runs")
    parser.add_argument(
        "--result", type=str, default="result", help="The name of the result file"
    )
    parser.add_argument(
        "--record-path",
        "-p",
        type=str,
        required=True,
        help="The name of the record folder",
    )
    return parser.parse_args(args[1:])


def main() -> None:
    args = parse_args(sys.argv)
    bugs = all_bugs()

    for bug in bugs:
        if args.name is None or bug.name in args.name:
            bug.simulate = args.simulate
            bug.by_angr = args.by_angr

            with launch_ipdb_on_exception():
                bug.reproduce(build_only=args.build_only)


def benchmark() -> None:
    args = parse_args_benchmark(sys.argv)

    logging.basicConfig(
        format="%(asctime)s: %(levelname)s: %(message)s", level=logging.INFO
    )

    results = {}  # type: Dict[str, Any]
    result_file = Path(args.record_path).joinpath(args.result + ".json")
    if result_file.exists():
        with open(str(result_file), "r") as f:
            results = json.load(f)

    bugs = all_bugs()
    for bug in bugs:
        if args.name is None or bug.name in args.name:
            with launch_ipdb_on_exception():
                results[bug.name + str(bug.version)] = dict(original=[], hase=[])

    for run in range(args.run):

        for bug in bugs:
            if args.name is None or bug.name in args.name:
                with launch_ipdb_on_exception():
                    result = results[bug.name + str(bug.version)]
                    result["hase"].append(
                        dict(run=run, result=[], exit_status=0, valid=True)
                    )
                    exit_status, rusage = bug.benchmark()
                    result["hase"][run]["result"].append(list(rusage))
                    result["hase"][run]["exit_status"] = exit_status
                    result["hase"][run]["valid"] = exit_status
                    results[bug.name + str(bug.version)] = result

        bugs = all_bugs()
        for bug in bugs:
            if args.name is None or bug.name in args.name:
                with launch_ipdb_on_exception():
                    result = results[bug.name + str(bug.version)]
                    result["original"].append(
                        dict(run=run, result=[], exit_status=0, valid=True)
                    )
                    exit_status, rusage = bug.run_without_hase()
                    result["original"][run]["result"].append(list(rusage))
                    result["original"][run]["exit_status"] = exit_status
                    result["original"][run]["valid"] = exit_status
                    results[bug.name + str(bug.version)] = result

        result_file.parent.mkdir(parents=True, exist_ok=True)
        with open(str(result_file), "w") as file:
            json.dump(results, file, sort_keys=True, indent=4, separators=(",", ": "))
            file.write("\n")


if __name__ == "__main__":
    main()
