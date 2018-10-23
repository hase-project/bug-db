import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional

from .bug import Bug
from .build import Build
from .utils import ROOT, sh

LIBJPEG_TURBO_PATH = ROOT.joinpath("libjpeg-turbo")


class LibjpegTurbo(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = f"https://github.com/libjpeg-turbo/libjpeg-turbo/archive/{version}.tar.gz"
        super().__init__(
            url, LIBJPEG_TURBO_PATH, simulate, enable_address_sanitizer=True, skip_cmake=True
        )


class LibjpegTurboBug(Bug):
    def __init__(self, *args, bug_id: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return LIBJPEG_TURBO_PATH.joinpath(f"ID-{self.bug_id}")

    def executable(self) -> str:
        exe = self._command[0]
        libjpeg_turbo = LibjpegTurbo(self.version, simulate=self.simulate)
        libjpeg_turbo.build()
        return str(libjpeg_turbo.build_path.joinpath(exe))


def libjpeg_turbo_bugs(bug_ids: Dict[int, str]) -> List[Bug]:
    bugs: List[Bug] = []
    commands: Dict[int, List[str]] = {}
    commands[17] = ["cjpeg", "crasherfile"]
    commands[23] = ["djpeg", "turbo-dht.jpg"]

    for bug_id, command in commands.items():
        bugs.append(
            LibjpegTurboBug(
                f"libjpeg-turbo-{bug_id}",
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


