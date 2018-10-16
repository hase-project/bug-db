import shutil
from pathlib import Path
from typing import Dict, List

from .bug import Bug
from .build import Build
from .utils import ROOT

FLAC_PATH = ROOT.joinpath("flac")


class Flac(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = f"https://github.com/xiph/flac/archive/{version}.tar.gz"
        super().__init__(url, FLAC_PATH, simulate, enable_address_sanitizer=True)

    def pre_build(self):
        with open(self.build_path.joinpath("config.rpath"), "w+"):
            pass


class FlacBug(Bug):
    def __init__(self, *args, bug_id: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return FLAC_PATH.joinpath(f"ID-{self.bug_id}")

    def executable(self) -> str:
        exe = self._command[0]
        flac = Flac(self.version, simulate=self.simulate)
        flac.build()
        return f"{flac.build_path}/src/{exe}"


def flac_bugs(bug_ids: Dict[int, str]) -> List[Bug]:
    bugs: List[Bug] = []
    commands: Dict[int, List[str]] = {}
    for id in [59, 61, 63]:
        commands[id] = ["flac", "-df", "@tempdir@/out.ogg", "crash.flac"]
    for id in [65, 66, 67]:
        commands[id] = ["flac", "-e", "-f", "-o", "@tempdir@/out.ogg", "crash.flac"]

    for bug_id, command in commands.items():
        bugs.append(
            FlacBug(
                f"flac-{bug_id}",
                bug_id=bug_id,
                version=bug_ids[bug_id],
                command=command,
            )
        )

    return bugs


## 35

## 40

## 44

## 59
#
# $ ./install/bin/flac -df ~/out.ogg PATH_TO_DIR/crash.flac
## 60

## 61
#
# $ ./install/bin/flac -df ~/out.ogg PATH_TO_DIR/crash.flac
## 63
#
# $ ./install/bin/flac -df ~/out.ogg PATH_TO_DIR/crash.flac
## 65
#
# $ ./install/bin/flac -e -f -o ~/test.flac PATH_TO_DIR/crash.flac
## 66
#
# $ ./install/bin/flac -e -f -o ~/test.flac PATH_TO_DIR/crash.flac
## 67
#
# $ ./install/bin/flac -e -f -o ~/test.flac PATH_TO_DIR/crash.flac
## 75
