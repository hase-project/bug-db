from pathlib import Path
from typing import Any, Dict, List

from .bug import Bug
from .build import Build
from .utils import ROOT, sh

LIBTASN_PATH = ROOT.joinpath("libtasn")


class Libtasn(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = "https://gitlab.com/gnutls/libtasn1/-/archive/{}/libtasn1-{}.tar.gz".format(
            version, version
        )
        self.version = version
        super().__init__(url, LIBTASN_PATH, simulate, enable_address_sanitizer=True)

    def pre_build(self) -> None:
        self.source_path().joinpath("ChangeLog").touch()
        sh(
            [
                "sed",
                "-ie",
                "s/SUBDIRS = gl lib src examples tests doc/SUBDIRS = gl lib src examples tests/",
                "Makefile.am",
            ],
            dir=(self.source_path()),
        )


class LibtasnBug(Bug):
    def __init__(self, *args: Any, bug_id: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return LIBTASN_PATH.joinpath("ID-{}".format(self.bug_id))

    def executable(self) -> str:
        exe = self._command[0]
        libtasn = Libtasn(self.version, simulate=self.simulate)
        libtasn.build()
        return str(libtasn.source_path().joinpath("src", exe))


def libtasn_bugs(bug_ids: Dict[int, str]) -> List[Bug]:
    bugs = []  # type: List[Bug]
    commands = {}  # type: Dict[int, List[str]]
    # [14, 15]
    # does not crash for me.
    # commands[14] = ["asn1Decoding", "./pkix.asn", "overflow.crt", "PKIX1Implicit88.asn1"]
    commands[15] = ["asn1Decoding", "./crash.asn", "x", "x"]
    for bug_id, command in commands.items():
        bugs.append(
            LibtasnBug(
                "libtasn-{}".format(bug_id),
                bug_id=bug_id,
                version=bug_ids[bug_id],
                command=command,
            )
        )
    return bugs


# 13

# ./asn1Decoding /PATH_TO_REPOSITORY/ID-15/crash.asn x x
#
# ./asn1Decoding /PATH_TO_REPOSITORY/ID-14/pkix.asn /PATH_TO_REPOSITORY/ID-14/overflow.crt

## 14
#
# ./asn1Decoding /PATH_TO_REPOSITORY/ID-15/crash.asn x x
#
# ./asn1Decoding /PATH_TO_REPOSITORY/ID-14/pkix.asn /PATH_TO_REPOSITORY/ID-14/overflow.crt

## 15
#
# ./asn1Decoding /PATH_TO_REPOSITORY/ID-15/crash.asn x x
#

## 22
