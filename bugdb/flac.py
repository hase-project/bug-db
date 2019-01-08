from pathlib import Path
from typing import Dict, List, Any

from .bug import Bug
from .build import Build
from .utils import ROOT

FLAC_PATH = ROOT.joinpath("flac")


class Flac(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = "https://github.com/xiph/flac/archive/{}.tar.gz".format(version)
        super().__init__(url, FLAC_PATH, simulate, enable_address_sanitizer=True)

    def pre_build(self) -> None:
        with open(str(self.build_path.joinpath("config.rpath")), "w+"):
            pass

    def configure_flags(self) -> List[str]:
        return ["--enable-ogg", "--disable-oggtest"]


class FlacBug(Bug):
    def __init__(self, *args: Any, bug_id: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return FLAC_PATH.joinpath("ID-{}".format(self.bug_id))

    def executable(self) -> str:
        exe = self._command[0]
        flac = Flac(self.version, simulate=self.simulate)
        flac.build()
        return "{}/src/flac/{}".format(flac.build_path, exe)


def flac_bugs(bug_ids: Dict[int, str]) -> List[Bug]:
    bugs = []  # type: List[Bug]
    commands = {}  # type: Dict[int, List[str]]
    for id in [59, 61, 63]:
        commands[id] = ["flac", "-df", "@tempdir@/out.ogg", "crash.flac"]
    for id in [65, 66, 67]:
        commands[id] = ["flac", "-e", "-f", "-o", "@tempdir@/out.ogg", "crash.wav"]

    for bug_id, command in commands.items():
        bugs.append(
            FlacBug(
                "flac-{}".format(bug_id),
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
