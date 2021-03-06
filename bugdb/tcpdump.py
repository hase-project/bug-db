from pathlib import Path
from typing import Dict, List, Any

from .bug import Bug
from .build import Build
from .utils import ROOT

TCPDUMP_PATH = ROOT.joinpath("tcpdump")


class Tcpdump(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = "https://github.com/the-tcpdump-group/tcpdump/archive/{}.tar.gz".format(
            version
        )
        super().__init__(url, TCPDUMP_PATH, simulate, enable_address_sanitizer=True)

    def make_flags(self) -> List[str]:
        cflags = " ".join(super().cflags())
        ldflags = " ".join(super().ldflags())
        return ["CC=gcc {}".format(cflags), "LDFLAGS={}".format(ldflags)]


class TcpdumpBug(Bug):
    def __init__(self, *args: Any, bug_id: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return TCPDUMP_PATH.joinpath("ID-{}".format(self.bug_id))

    def executable(self) -> str:
        exe = self._command[0]
        tcpdump = Tcpdump(self.version, simulate=self.simulate)
        tcpdump.build()
        return "{}/{}".format(tcpdump.build_path, exe)


def tcpdump_bugs(bug_ids: Dict[int, str]) -> List[Bug]:
    bugs = []  # type: List[Bug]
    for bug_id in [72, 142, 144, 145, 146, 152, 154, 155, 158, 180]:
        bugs.append(
            TcpdumpBug(
                "tcpdump-{}".format(bug_id),
                bug_id=bug_id,
                version=bug_ids[bug_id],
                command=["tcpdump", "-vvv", "-r", "crash.pcap"],
            )
        )
    return bugs


## 145
#
# $ ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/crash.pcap'

## 146
#
# $ valgrind ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/crash.pcap'

## 152
#
# $ ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/ID-152/crash.pcap'

## 154
#
# $ ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/ID-40/crash.pcap'

## 155
#
# $ valgrind ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/ID-155/crash.pcap'

## 157

## 158
#
# $ ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/ID-158/crash.pcap'

## 160

## 180
#
# $ ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/ID-180/crash.pcap'
## 61

## 72
#
# $ valgrind ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/crash.pcap'

## 122

## 123

## 127

## 129

## 132

## 137

## 138

## 142
#
# $ ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/crash.pcap'

## 144
#
# $ valgrind ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/crash.pcap'

## 145
#
# $ ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/crash.pcap'

## 146
#
# $ valgrind ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/crash.pcap'

## 152
#
# $ ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/ID-152/crash.pcap'

## 154
#
# $ ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/ID-40/crash.pcap'

## 155
#
# $ valgrind ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/ID-155/crash.pcap'

## 157

## 158
#
# $ ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/ID-158/crash.pcap'

## 160

## 180
#
# $ ./installer/sbin/tcpdump -vvv -r 'PATH_TO_FILE/ID-180/crash.pcap'
