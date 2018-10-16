import os
import shutil
from pathlib import Path
from typing import Dict, List

from .bug import Bug
from .build import Build
from .utils import ROOT, sh

W3M_PATH = ROOT.joinpath("w3m")


class W3m(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = f"https://github.com/tats/w3m/archive/{version}.tar.gz"
        super().__init__(
            url,
            W3M_PATH,
            simulate,
            enable_address_sanitizer=True,
            skip_auto_reconf=True
        )

    def pre_build(self):
        sh(["aclocal", "--force"], simulate=self.simulate, dir=str(self.build_path))
        sh(["autoconf", "--force"], simulate=self.simulate, dir=str(self.build_path))

        path = shutil.which("gettext")
        # currently requires on my system to symlink an updated version of po/Makefile.in.in from gettext
        makefile_path = Path(path).parent.parent.joinpath("share/gettext/po/Makefile.in.in")

        if makefile_path.exists():
            old_makefile = self.build_path.joinpath("po/Makefile.in.in")
            if old_makefile.exists():
                os.unlink(old_makefile)
            old_makefile.symlink_to(makefile_path)


    def configure_flags(self) -> List[str]:
        return super().configure_flags() + ["--enable-messagel10n=no"]


    def make_flags(self) -> List[str]:
        cflags = " ".join(super().cflags())
        ldflags = " ".join(super().ldflags())
        return [f"CC=gcc -lncurses {cflags}", f"LDFLAGS={ldflags}"]

class W3mBug(Bug):
    def __init__(self, *args, bug_id: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return W3M_PATH.joinpath(f"ID-{self.bug_id}")

    def executable(self) -> str:
        exe = self._command[0]
        w3m = W3m(self.version, simulate=self.simulate)
        w3m.build()
        return f"{w3m.build_path}/src/{exe}"


def w3m_bugs(bug_ids: Dict[int, str]) -> List[Bug]:
    bugs: List[Bug] = []
    commands: Dict[int, List[str]] = {}

    commands[11] = ["w3m", "-dump", "-T", "text/plain", "crash.min.html"]
    commands[12] = ["w3m", "-dump", "-T", "text/plain", "bugreport.cgi.html"]
    commands[13] = ["w3m", "-dump", "crash.html"]
    commands[15] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[16] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[17] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[18] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[19] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[20] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[21] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[22] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[24] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[26] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[27] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[28] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[30] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[31] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[33] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[36] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[38] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[39] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[40] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[41] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[43] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[44] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[45] = ["w3m", "-dump", "-T", "text/html", "crash.html"]
    commands[46] = ["w3m", "-dump", "-T", "text/html", "crash.html"]

    for bug_id, command in commands.items():
        bugs.append(
            W3mBug(
                f"w3m-{bug_id}",
                bug_id=bug_id,
                version=bug_ids[bug_id],
                command=command,
            )
        )

    # TODO to the rest

    return bugs

## 11
# 
# $ ./installer/bin/w3m -dump -T text/plain 'PATH_TO_FILE/crash.min.html' 

## 12
# 
# $ ./installer/bin/w3m -dump -T text/plain 'PATH_TO_FILE/bugreport.cgi.html' 

## 13
# 
# $ ./installer/bin/w3m -dump 'PATH_TO_FILE/crash.html' 

## 14

## 15
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 16
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 17
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 18
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 19
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 20
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 21
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 22
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 23
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 24
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 25
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 26
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 27
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 28
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 30
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 31
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 33
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 35
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 36
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 38
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 39
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 40
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 41
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 43
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 44
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 45
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 46
# 
# $ ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 48
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 49
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 50
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 51
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 52
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 53
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 54
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 55
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 56
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 57
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 58
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 59
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 60
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 61
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 62
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 63
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 64
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 65
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 66
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 67
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 68
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 69
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 70
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 71
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 72
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 73
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 76
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 77
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 78
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 

## 79
# 
# $ LD_LIBRARY_PATH=../notgc  ./installer/bin/w3m -T text/html -dump 'PATH_TO_FILE/crash.html' 
