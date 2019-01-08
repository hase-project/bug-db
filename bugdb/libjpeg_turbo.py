from pathlib import Path
from typing import Dict, List, Any

from .bug import Bug
from .build import Build
from .utils import ROOT

LIBJPEG_TURBO_PATH = ROOT.joinpath("libjpeg-turbo")


class LibjpegTurbo(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = "https://github.com/libjpeg-turbo/libjpeg-turbo/archive/{}.tar.gz".format(
            version
        )
        super().__init__(
            url,
            LIBJPEG_TURBO_PATH,
            simulate,
            enable_address_sanitizer=True,
            skip_cmake=True,
        )


class LibjpegTurboBug(Bug):
    def __init__(self, *args: Any, bug_id: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return LIBJPEG_TURBO_PATH.joinpath("ID-{}".format(self.bug_id))

    def executable(self) -> str:
        exe = self._command[0]
        libjpeg_turbo = LibjpegTurbo(self.version, simulate=self.simulate)
        libjpeg_turbo.build()
        return str(libjpeg_turbo.build_path.joinpath(exe))


def libjpeg_turbo_bugs(bug_ids: Dict[int, str]) -> List[Bug]:
    bugs = []  # type: List[Bug]
    commands = {}  # type: Dict[int, List[str]]
    commands[17] = ["cjpeg", "crasherfile"]
    commands[23] = ["djpeg", "turbo-dht.jpg"]

    for bug_id, command in commands.items():
        bugs.append(
            LibjpegTurboBug(
                "libjpeg-turbo-{}".format(bug_id),
                bug_id=bug_id,
                version=bug_ids[bug_id],
                command=command,
            )
        )
    return bugs


## 5
# $ ./installer/bin/djpeg '/media/sf_Bugs/libjpeg-turbo/ID-5/firefox-heap-buffer-overflow-4b0.jpeg'
#

## 10

## 16

## 17
#
# $ ./installer/bin/cjpeg '/media/sf_Bugs/libjpeg-turbo/ID-17/crasherfile'
#

## 20

## 23
#
# $ ./installer/bin/djpeg '/media/sf_Bugrbo/ID-23/turbo-dht.jpg'
#

## 28
#
# $ ./installer/bin/cjpeg 'PATH_TO_REPOSITORY/ID-28/crash'
#
