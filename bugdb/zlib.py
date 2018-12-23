import os
import shutil
from pathlib import Path
from typing import Dict, List, Any

from .bug import Bug
from .build import Build
from .utils import ROOT, sh

ZLIB_PATH = ROOT.joinpath("zlib")


class Zlib(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = "https://github.com/madler/zlib/archive/{}.tar.gz".format(version)
        super().__init__(url, ZLIB_PATH, simulate, enable_address_sanitizer=True)

    def configure(self) -> None:
        extra_env = dict(
            CC="gcc " + " ".join(super().cflags()),
            LDSHARED="gcc -shared " + " ".join(super().ldflags()),
        )
        sh(
            ["sh", "./configure"],
            extra_env=extra_env,
            simulate=self.simulate,
            dir=str(self.build_path),
        )

    # don't override LFLAGS/CFLAGS, those we pass in configure
    def make_flags(self) -> List[str]:
        return ["AR=ar rcs"]


class ZlibBug(Bug):
    def __init__(self, *args: Any, bug_id: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return ZLIB_PATH.joinpath("ID-{}".format(self.bug_id))

    def executable(self) -> str:
        exe = self._command[0]
        zlib = Zlib(self.version, simulate=self.simulate)
        zlib.build()
        return "{}/{}".format(zlib.build_path, exe)

    def pre_hook(self) -> None:
        path = self.working_directory().joinpath("test.gz")
        self.vars["archive"] = os.path.join(self.directory.name, "test.gz")
        shutil.copyfile(str(path), self.vars["archive"])


def zlib_bugs(bug_ids: Dict[int, str]) -> List[Bug]:
    bugs = []  # type: List[Bug]
    commands = {}  # type: Dict[int, List[str]]

    # TODO bug 2
    for id in [1, 3, 4, 5]:
        commands[id] = ["minigzip", "-d", "@archive@"]

    for bug_id, command in commands.items():
        bugs.append(
            ZlibBug(
                "zlib-{}".format(bug_id),
                bug_id=bug_id,
                version=bug_ids[bug_id],
                command=command,
            )
        )

    return bugs


## 1
#
# # $ ./minigzip -d < 'PATH_TO_FILE/ID-1/test.gz'
# #
#
# ## 2
# #
# # $ ./CVE-2003-0107
# #
#
# ## 3
# #
# # $ ./minigzip -d < 'PATH_TO_FILE/ID-3/test.gz'
# #
#
# ## 4
#
# ## 5
# #
# # $ ./minigzip -d < 'PATH_TO_FILE/ID-5/test.gz'
# #
#
#
