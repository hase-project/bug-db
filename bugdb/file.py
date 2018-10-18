from pathlib import Path
from typing import Dict, List, Optional

from .bug import Bug
from .build import Build
from .utils import ROOT

FILE_PATH = ROOT.joinpath("file")


class File(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = f"https://github.com/file/file/archive/{version}.tar.gz"
        super().__init__(url, FILE_PATH, simulate, enable_address_sanitizer=True)

    def post_build(self) -> None:
        magic_symlink = self.source_path().joinpath("magic", ".magic.mgc")
        magic_symlink2 = self.source_path().joinpath("magic", ".magic")
        magic_file = self.source_path().joinpath("magic", "magic.mgc")
        magic_symlink.symlink_to(magic_file)
        magic_symlink2.symlink_to(magic_file)


class FileBug(Bug):
    def __init__(self, *args, bug_id: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return FILE_PATH.joinpath(f"ID-{self.bug_id}")

    def extra_env(self) -> Dict[str, str]:
        env = super().extra_env()
        env["LD_LIBRARY_PATH"] = str(self.libmagic_path)
        env["HOME"] = str(self.magic_home)
        return env

    def executable(self) -> str:
        exe = self._command[0]
        file = File(self.version, simulate=self.simulate)
        file.build()
        self.libmagic_path = file.build_path.joinpath("src", ".libs")
        self.magic_home = file.build_path.joinpath("magic")
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

    commands[5] = ["file", "-m", "broken_magic7", "@tempfile@"]
    commands[6] = ["file", "-m", "broken_magic11", "@tempfile@"]
    commands[7] = ["file", "-m", "broken_magic4", "@tempfile@"]
    commands[9] = ["file", "-m", "test1", "@tempfile@"]
    commands[10] = ["file", "-f", "test4"]
    commands[11] = ["file", "-m", "test2", "@tempfile@"]
    commands[12] = ["file", "-m", "broken_magic", "@tempfile@"]
    commands[18] = ["file", "-m", "broken_magic5", "@tempfile@"]

    for (id, command) in commands.items():
        bugs.append(
            FileBug(
                f"file-{id}",
                bug_id=id,
                version=bug_ids[id],
                command=command,
                tempfile_content="a\n" * 4096,
            )
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
