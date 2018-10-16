from typing import Dict, List, Optional
from pathlib import Path

from .bug import Bug
from .utils import ROOT
from .build import Build

FILE_PATH = ROOT.joinpath("file")


class File(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = f"https://github.com/file/file/archive/{version}.tar.gz"
        super().__init__(url, FILE_PATH, simulate, enable_address_sanitizer=True)


class FileBug(Bug):
    def __init__(self, *args, bug_id: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return FILE_PATH.joinpath(f"ID-{self.bug_id}")

    def extra_env(self) -> Optional[Dict[str, str]]:
        return dict(LD_LIBRARY_PATH=str(self.libmagic_path))

    def executable(self) -> str:
        exe = self._command[0]
        file = File(self.version, simulate=self.simulate)
        file.build()
        self.libmagic_path = file.build_path.joinpath("src", ".libs")
        return str(self.libmagic_path.joinpath(exe))


def file_bugs(bug_ids: Dict[int, str]) -> List[Bug]:
    bugs: List[Bug] = []
    bugs.append(
        FileBug(
            f"file-1", bug_id=1, version=bug_ids[1], command=["file", "file_error.xls"]
        )
    )
    commands: Dict[int, List[str]] = {}
    for id in [2, 3, 4]:
        commands[id] = ["file", "crash"]

    commands[5] = ["file", "-m", "broken_magic7", "/etc/services"]
    commands[6] = ["file", "-m", "broken_magic11", "/etc/services"]
    commands[7] = ["file", "-m", "broken_magic2", "/etc/services"]
    commands[9] = ["file", "-m", "test1", "/etc/services"]
    commands[10] = ["file", "-f", "test4"]
    commands[11] = ["file", "-m", "test2", "/etc/services"]
    commands[12] = ["file", "-m", "broken_magic", "/etc/services"]
    commands[18] = ["file", "-m", "broken_magic5", "/etc/services"]

    for (id, command) in commands.items():
        bugs.append(
            FileBug(f"file-{id}", bug_id=id, version=bug_ids[id], command=command)
        )

    return bugs


## 1
#
# $ ./install/bin/file 'PATH_TO_FILE/file_error.xls'

## 2
#
# $ ./install/bin/file '/media/sf_Bugs/file/ID-2/crash'

## 3
#
# $ ./install/bin/file '/media/sf_Bugs/file/ID-3/crash'

## 4
#
# $ ./install/bin/file '/media/sf_Bugs/file/ID-4/crash'

## 5
#
# $ ./install/bin/file -m '/media/sf_Bugs/file/ID-5/broken_magic7' /etc/services

## 6
#
# $ ./install/bin/file -m 'PATH_TO_FOLDER/broken_magic11' /etc/services

## 7
#
# $ ./install/bin/file -m 'PATH_TO_FOLDER/broken_magic4' /etc/services
#

## 8
#
# $ ./install/bin/file -m 'PATH_TO_FOLDER/broken_magic2' /etc/services
#

## 9
#
# $ ./install/bin/file -m 'PATH_TO_FOLDER/test1' /etc/services

## 10
#
# $ ./install/bin/file -f 'PATH_TO_FOLDER/test4'

## 11
#
# $ ./install/bin/file -m '/media/sf_Bugs/file/ID-11/test2' /etc/services

## 12
#
# $ ./install/bin/file -m 'PATH_TO_FOLDER/broken_magic' /etc/services
#

## 13

## 17
#
# $ ./install/bin/file -m 'PATH_TO_FOLDER/broken_magic3' /etc/services
#

## 18
#
# $ ./install/bin/file -m 'PATH_TO_FOLDER/broken_magic5' /etc/services
#
