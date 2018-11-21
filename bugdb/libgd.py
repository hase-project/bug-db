import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional

from .bug import Bug
from .build import Build
from .utils import ROOT, sh

LIBGD_PATH = ROOT.joinpath("libgd")


class Libgd(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = f"https://github.com/libgd/libgd/archive/{version}.tar.gz"
        self.version = version
        super().__init__(
            url, LIBGD_PATH, simulate, enable_address_sanitizer=True, skip_cmake=True
        )

    def pre_build(self):
        config = self.build_path.joinpath("config")
        config_symlink = self.source_path().joinpath("config")
        if not config_symlink.exists() and config.exists():
            config_symlink.symlink_to(config)

        test = self.build_path.joinpath("tests")
        test_symlink = self.source_path().joinpath("test")
        if not test_symlink.exists() and test.exists():
            test_symlink.symlink_to(test)

        bootstrap_sh = self.source_path().joinpath("bootstrap.sh")
        if bootstrap_sh.exists():
            sh(["sh", str(bootstrap_sh)], self.simulate, dir=self.source_path())

    def source_directory(self) -> Path:
        return Path("src")


class LibgdBug(Bug):
    def __init__(self, *args, bug_id: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return LIBGD_PATH.joinpath(f"ID-{self.bug_id}")

    def extra_env(self) -> Dict[str, str]:
        env = super().extra_env()
        env["LD_LIBRARY_PATH"] = str(self.libgd_path)
        return env

    def executable(self) -> str:
        exe = self._command[0]
        libgd = Libgd(self.version, simulate=self.simulate)
        libgd.build()
        include_path = libgd.source_path()
        self.libgd_path = include_path.joinpath(".libs")
        cwd = self.working_directory()
        bug_exe = cwd.joinpath("bug")
        if not bug_exe.exists():
            sources = list(map(str, cwd.glob("*.c")))
            lib = str(self.libgd_path.joinpath("libgd.so"))
            cflags = [
                "-g",
                "-I",
                str(include_path),
                "-o",
                str(bug_exe),
                lib,
                "-lm",
            ] + sources
            sh(["cc"] + cflags + libgd.cflags() + libgd.ldflags())

        return str(bug_exe)


def libgd_bugs(bug_ids: Dict[int, str]) -> List[Bug]:
    bugs: List[Bug] = []
    commands: Dict[int, List[str]] = {}
    # TODO compile the examples
    # for bug_id in [1, 12, 13, 14, 25]:
    for bug_id in [1, 12, 13, 14]:
        bugs.append(
            LibgdBug(
                f"libgd-{bug_id}",
                bug_id=bug_id,
                version=bug_ids[bug_id],
                command=["./bug"],
            )
        )
    return bugs


## 1
# $ ./bug

## 2
# $ ./bug
#
#
#

## 12
# $ ./bug
# $ echo $? # 1 upon failure!
#
#
#

## 13
# $ ./bug
#
#
#
#

## 14
# $ ./bug
#
#
#
#

## 23
# $ ./bug
#
#
#
#

## 25
# $ ./bug
#
#
#
#

## 27

## 33

## 34

## 36

## 49

## 50

## 55

## 58

## 61

## 66

## 67

## 69

## 70

## 71

## 72

## 73

## 74

## 76

## 79

## 80

## 84

## 85
