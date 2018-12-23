import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Dict, List, Optional

from .bug import Bug
from .build import Build
from .utils import REPORT_PATH, ROOT, blue_text, cd, green_text, red_text, sh

COREUTILS_PATH = ROOT.joinpath("coreutils")
COREUTILS_PATH.mkdir(exist_ok=True)


class Coreutils(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        version_list = list(map(int, version.split(".")))

        if version_list >= [6, 12]:
            ext = "tar.xz"
        else:
            ext = "tar.gz"

        archive_name = "coreutils-{}.{}".format(version, ext)

        url = "http://ftp.gnu.org/gnu/coreutils/{}".format(archive_name)
        super().__init__(url, COREUTILS_PATH, simulate, skip_auto_reconf=True)


class CoreutilsBug(Bug):
    def id(self) -> str:
        return "coreutils-{}-{}".format(self.version, self.name)

    def executable(self) -> str:
        exe = self._command[0]
        coreutils = Coreutils(self.version, simulate=self.simulate)
        coreutils.build()
        return "{}/src/{}".format(coreutils.build_path, exe)


def coreutils_bugs() -> List[Bug]:
    bugs = []  # type: List[Bug]

    bugs.append(
        CoreutilsBug(
            "tac",
            version="6.10",
            commit_ids=["d701f6abb73e36721de5df083df4769786a14528"],
            command=["tac", "-r", "@tempfile@", "@tempfile@"],
            tempfile_content="\n",
        )
    )

    bugs.append(
        CoreutilsBug(
            "mkdir",
            version="6.10",
            commit_ids=[
                "72d052896a9092b811961a8f3e6ca5d151a59be5",
                "eb8fa94f2cf030d625c12ad68bb8883de204c196",
            ],
            command=["mkdir", "-Z", "invalid-selinux-context", "@tempdir@/path"],
        )
    )

    # bugs.append(
    #    CoreutilsBug(
    #        "sha512sum",
    #        version="6.10",
    #        commit_ids=[
    #            "72d052896a9092b811961a8f3e6ca5d151a59be5",
    #            "eb8fa94f2cf030d625c12ad68bb8883de204c196",
    #        ],
    #        command=["sha512sum", "-c", "@tempfile@"],
    #        tempfile_content="SHA512 (\n",
    #    )
    # )

    bugs.append(
        CoreutilsBug(
            "ptx",
            version="6.10",
            commit_ids=["a0851554bd52038ed47e46ee521ce74a5a09f747"],
            command=["ptx", "-F\\", "@tempfile@"],
            tempfile_content="\n",
            tempfile_name="A01234567890123456789012345678901234567890123456789",
        )
    )

    bugs.append(
        CoreutilsBug(
            "paste",
            version="6.10",
            commit_ids=[],
            command=[
                "paste",
                "-d\\",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            ],
        )
    )
    bugs.append(
        CoreutilsBug(
            "stty",
            version="6.10",
            commit_ids=[],
            command=["stty", "eol", "-F", "/dev/tty"],
        )
    )

    bugs.append(
        CoreutilsBug(
            "sort",
            version="7.2",
            commit_ids=["25eb4c69097ca4f5665b050cfa4247a19ffd8c55"],
            command=["sort", "-m", "-o", "@tempfile@", "@tempfile@"],
            tempfile_content="\n",
        )
    )

    bugs.append(
        CoreutilsBug(
            "shuf",
            version="8.22",
            commit_ids=["fb13cdc727541adef0010279f770f2afa358002e"],
            command=["shuf", "-i", "0-0", "1"],
        )
    )

    bugs.append(
        CoreutilsBug(
            "ln",
            version="8.22",
            commit_ids=["0093ac8d57a0f1a16fd09d98f6a524dddb6053e7"],
            command=["ln", "-sr", "", "F"],
        )
    )

    bugs.append(
        CoreutilsBug(
            "date",
            version="8.22",
            commit_ids=["a4faa6a0a3ae93c01d036d830ae7a21b74913baf"],
            command=["date", '--date=TZ="""'],
        )
    )
    bugs.append(
        CoreutilsBug(
            "date",
            version="8.27",
            commit_ids=["9287ef2b1707e2a222f8ae776ce3785abcb16fba"],
            command=["date", "-d", "TZ=\"{}0\" 2017".format('a' * 2001)],
        )
    )

    bugs.append(
        CoreutilsBug(
            "b2sum",
            version="8.27",
            commit_ids=["9287ef2b1707e2a222f8ae776ce3785abcb16fba"],
            command=["b2sum", "-c", "@tempfile@"],
            tempfile_content="BLAKE2\n",
        )
    )

    return bugs


# 6.10

## commit-id: https://github.com/coreutils/coreutils/commit/d701f6abb73e36721de5df083df4769786a14528
# 	echo > $(BINPATH)/foobar; \
# 	sudo $(HASEBIN) record -- $(BINPATH)/tac -r $(BINPATH)/foobar $(BINPATH)/foobar; \
# 	rm -f $(BINPATH)/foorbar
#
## commit-id: https://github.com/coreutils/coreutils/commit/72d052896a9092b811961a8f3e6ca5d151a59be5
## commit-id: https://github.com/coreutils/coreutils/commit/eb8fa94f2cf030d625c12ad68bb8883de204c196
# record-mkdir:
# 	sudo $(HASEBIN) record -- $(BINPATH)/mkdir -Z invalid-selinux-context foobar
#
## commit-id: https://github.com/coreutils/coreutils/commit/7cb24684cc4ef96bb25dfc1c819acfc3b98d9442
# record-sha512sum:
# 	echo 'SHA512 (' > $(BINPATH)/foobar; \
# 	sudo $(HASEBIN) record -- $(BINPATH)/sha512sum -c < $(BINPATH)/foobar; \
# 	rm -f $(BINPATH)/foobar
#
## commit-id: https://github.com/coreutils/coreutils/commit/a0851554bd52038ed47e46ee521ce74a5a09f747
# record-ptx:
# 	echo > $(BINPATH)/A01234567890123456789012345678901234567890123456789; \
# 	sudo $(HASEBIN) record -- $(BINPATH)/ptx -F'\' $(BINPATH)/A01234567890123456789012345678901234567890123456789; \
# 	rm -f $(BINPATH)/A01234567890123456789012345678901234567890123456789
#
## commit-id: https://github.com/coreutils/coreutils/commit/b58a8b4ef588ec8a365b920d12e27fdd71aa48d1
# 	sudo $(HASEBIN) record -- $(BINPATH)/paste -d'\' 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
#
## commid-id: https://github.com/coreutils/coreutils/commit/f926f7ce0e0a224ef3a37a82e60fd3d7aaca906e
# record-stty:
# 	sudo $(HASEBIN) record -- $(BINPATH)/stty eol -F /dev/tty

# 7.2

# commit-id: https://github.com/coreutils/coreutils/commit/25eb4c69097ca4f5665b050cfa4247a19ffd8c55
# 	touch $(BINPATH)/foobar; \
# 	sudo $(HASEBIN) record -- $(BINPATH)/sort -m -o $(BINPATH)/foobar $(BINPATH)/foobar; \
# 	rm -f $(BINPATH)/foobar

# 8.22

# commit-id: https://github.com/coreutils/coreutils/commit/fb13cdc727541adef0010279f770f2afa358002e
# record-shuf:
# 	sudo $(HASEBIN) record -- $(BINPATH)/shuf -i 0-0 1
#
## commit-id: https://github.com/coreutils/coreutils/commit/0093ac8d57a0f1a16fd09d98f6a524dddb6053e7
# record-ln:
# 	sudo $(HASEBIN) record -- $(BINPATH)/ln -sr '' F
#
## commit-id: https://github.com/coreutils/coreutils/commit/a4faa6a0a3ae93c01d036d830ae7a21b74913baf
# record-date:
# 	sudo $(HASEBIN) record -- $(BINPATH)/date --date='TZ="""'

# 8.27
## commit-id: https://github.com/coreutils/coreutils/commit/9287ef2b1707e2a222f8ae776ce3785abcb16fba
# record-date:
# 	tz_long=$(printf '%2000s' | tr ' ' a); \
# 	sudo $(HASEBIN) record -- $(BINPATH)/date -d "TZ=\"${tz_long}0\" 2017"
#
## commit-id: https://github.com/coreutils/coreutils/commit/cc19f63be3ad0f27c9ea7f223883b75917fda7fb
# record-b2sum:
# 	echo "BLAKE2" > $(BINPATH)/foobar; \
# 	sudo $(HASEBIN) record -- $(BINPATH)/b2sum -c < $(BINPATH)/foobar; \
# 	rm -f $(BINPATH)/foobar
