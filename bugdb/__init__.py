import os

from .audiofile import audiofile_bugs
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


def main():
    os.makedirs(REPORT_PATH, exist_ok=True)

    bug_ids = read_bug_ids_per_project()

    os.environ["FORCE_UNSAFE_CONFIGURE"] = "1"
    # nixos shenanigans
    os.environ["hardeningDisable"] = "all"
    # make address sanitzer coredump on violation
    asan_options = [
        "detect_leaks=0",
        "abort_on_error=1",
        "disable_coredump=0",
        "unmap_shadow_on_exit=1",
    ]
    os.environ["ASAN_OPTIONS"] = ":".join(asan_options)

    # bugs = coreutils_bugs() + audiofile_bugs()
    bugs = (
        coreutils_bugs()
        + audiofile_bugs(bug_ids["audiofile"])
        + file_bugs(bug_ids["file"])
        + libtiff_bugs(bug_ids["libtiff"])
        + jasper_bugs(bug_ids["jasper"])
        + flac_bugs(bug_ids["libflac"])
        + zlib_bugs(bug_ids["zlib"])
        + tcpdump_bugs(bug_ids["tcpdump"])
        + w3m_bugs(bug_ids["w3m"])
        + libjpeg_turbo_bugs(bug_ids["libjpeg-turbo"])
        + libgd_bugs(bug_ids["libgd"])
    )

    simulate = False
    for bug in bugs:
        bug.simulate = simulate
        import pry

        with pry:
            bug.reproduce(build_only=True)


if __name__ == "__main__":
    main()
