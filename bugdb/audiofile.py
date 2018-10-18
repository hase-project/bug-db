from pathlib import Path
from typing import Dict, List, Optional

from .bug import Bug
from .build import Build
from .utils import ROOT

AUDIOFILE_PATH = ROOT.joinpath("audiofile")


class Audiofile(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = f"https://github.com/mpruett/audiofile/archive/{version}.tar.gz"
        super().__init__(url, AUDIOFILE_PATH, simulate)

    def configure_flags(self) -> List[str]:
        return super().configure_flags() + ["--disable-docs"]


class AudiofileBug(Bug):
    def __init__(self, *args, bug_id: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return AUDIOFILE_PATH.joinpath(f"ID-{self.bug_id}")

    def extra_env(self) -> Dict[str, str]:
        env = super().extra_env()
        env.update(LD_LIBRARY_PATH=str(self.libaudiofile))
        return env

    def executable(self) -> str:
        exe = self._command[0]
        audiofile = Audiofile(self.version, simulate=self.simulate)
        audiofile.build()
        self.libaudiofile = audiofile.build_path.joinpath("libaudiofile", ".libs")
        return str(audiofile.build_path.joinpath("sfcommands", ".libs", exe))


def audiofile_bugs(bug_ids: Dict[int, str]) -> List[Bug]:
    bugs: List[Bug] = []
    for id in [4, 13, 14]:
        bugs.append(
            AudiofileBug(
                f"audiofile-{id}",
                bug_id=id,
                version=bug_ids[id],
                command=["sfconvert", "crash", "@tempdir@/out"],
            )
        )
    for id in [16, 19, 20, 21, 22]:
        bugs.append(
            AudiofileBug(
                f"audiofile-{id}",
                bug_id=id,
                version=bug_ids[id],
                command=["sfconvert", "crash", "out.mp3", "format", "aiff"],
            )
        )

    return bugs


## 4
#
# ./sfconvert /PATH_TO_REPOSITORY/ID-4/crash.wav out

## 13
#
# ./sfinfo /PATH_TO_REPOSITORY/ID-13/crash

## 14
#
# ./sfinfo /PATH_TO_REPOSITORY/ID-14/crash

## 15

## 16
#
# ./sfconvert /PATH_TO_REPOSITORY/ID-16/crashh out.mp3 format aiff

## 17

## 18

## 19
#
# ./sfconvert /PATH_TO_REPOSITORY/ID-19/crashh out.mp3 format aiff

## 20
#
# ./sfconvert /PATH_TO_REPOSITORY/ID-20/crashh out.mp3 format aiff

## 21
#
# ./sfconvert /PATH_TO_REPOSITORY/ID-21/crashh out.mp3 format aiff

## 22
#
# ./sfconvert /PATH_TO_REPOSITORY/ID-22/crashh out.mp3 format aiff
