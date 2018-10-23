import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional

from .bug import Bug
from .build import Build
from .utils import ROOT, sh

LIBTASN_PATH = ROOT.joinpath("libtasn")


class Libtasn(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = f"https://gitlab.com/gnutls/libtasn1/-/archive/{version}/libtasn1-{version}.tar.gz"
        self.version = version
        super().__init__(url, LIBTASN_PATH, simulate, enable_address_sanitizer=True)

    def pre_build(self):
        self.source_path().joinpath("ChangeLog").touch()
        sh(
            [
                "sed",
                "-ie",
                "s/SUBDIRS = gl lib src examples tests doc/SUBDIRS = gl lib src examples tests/",
                "Makefile.am",
            ],
            dir=(self.source_path())
        )


class LibtasnBug(Bug):
    def __init__(self, *args, bug_id: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return LIBTASN_PATH.joinpath(f"ID-{self.bug_id}")

    def executable(self) -> str:
        exe = self._command[0]
        libtasn = Libtasn(self.version, simulate=self.simulate)
        libtasn.build()
        return str(libtasn.source_path().joinpath("src", exe))


def libtasn_bugs(bug_ids: Dict[int, str]) -> List[Bug]:
    bugs: List[Bug] = []
    commands: Dict[int, List[str]] = {}
    # [14, 15]
    # does not crash for me.
    #commands[14] = ["asn1Decoding", "./pkix.asn", "overflow.crt", "PKIX1Implicit88.asn1"]
    commands[15] = ["asn1Decoding", "./crash.asn", "x", "x"]
    for bug_id, command in commands.items():
        bugs.append(
            LibtasnBug(
                f"libtasn-{bug_id}",
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
