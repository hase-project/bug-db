from pathlib import Path
from typing import Dict, List

from .bug import Bug
from .utils import ROOT
from .build import Build

JASPER_PATH = ROOT.joinpath("jasper")


class Jasper(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = f"https://github.com/mdadams/jasper/archive/{version}.tar.gz"
        super().__init__(url, JASPER_PATH, simulate, enable_address_sanitizer=True)


class JasperBug(Bug):
    def __init__(self, *args, bug_id: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return JASPER_PATH.joinpath(f"ID-{self.bug_id}")

    def executable(self) -> str:
        exe = self._command[0]
        file = Jasper(self.version, simulate=self.simulate)
        file.build()
        return f"{file.build_path}/src/appl/{exe}"


def jasper_bugs(bug_ids: Dict[int, str]) -> List[Bug]:
    bugs: List[Bug] = []
    commands: Dict[int, List[str]] = {}
    commands[2] = ["imginfo", "-f", "bad.jp2"]
    commands[9] = ["imginfo", "-f", "poc.jp2"]
    commands[13] = [
        "jasper",
        "--input",
        "jasper-assert-jpc_dec_tiledecode.jp2",
        "--output-format",
        "jpg",
    ]
    commands[15] = ["imginfo", "-f", "jasper-nullptr-jpc_pi_destroy.jp2"]
    commands[17] = ["imginfo", "-f", "crash"]
    commands[18] = ["imginfo", "-f", "1.crash"]
    commands[19] = ["imginfo", "-f", "bug"]
    commands[20] = ["imginfo", "-f", "assert"]
    commands[22] = ["imginfo", "-f", "00003-jasper-assert-jas_matrix_t"]
    commands[23] = ["imginfo", "-f", "642.crashes"]
    commands[24] = ["imginfo", "-f", "00005-jasper-assert-ras_getcmap"]
    commands[25] = ["imginfo", "-f", "bug"]
    commands[26] = ["imginfo", "-f", "jasper-heapoverflow-jpc_dec_cp_setfromcox.jp2"]
    commands[27] = ["imginfo", "-f", "jasper-heapoverflow-jpc_getuint16.jp2"]
    commands[28] = ["imginfo", "-f", "bug"]
    commands[29] = ["jasper", "--input", "PoC1.jpc", "--output-format", "jpc"]
    commands[30] = ["imginfo", "--input", "PoC2.jpc"]
    commands[31] = ["imginfo", "-f", "bug"]
    commands[32] = ["imginfo", "-f", "assert-pnm_getsint.mif"]
    commands[33] = ["imginfo", "-f", "681.crashes"]
    commands[34] = ["imginfo", "-f", "11.crash"]
    commands[35] = ["imginfo", "-f", "12.crash"]

    for bug_id, command in commands.items():
        bugs.append(
            JasperBug(
                f"jasper-{bug_id}",
                bug_id=bug_id,
                version=bug_ids[bug_id],
                command=command,
            )
        )

    return bugs


## 2
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/bad.jp2'

## 4
#
# $ ./install/src/appl/jasper --input 'PATH_TO_FILE/input' --input-format mif --output /dev/null --output-format jpg

## 9
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/poc.jp2'

## 13
#
# $ ./install/src/appl/jasper --input 'PATH_TO_FILE/jasper-assert-jpc_dec_tiledecode.jp2' --output-format jpg

## 15
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/jasper-nullptr-jpc_pi_destroy.jp2'

## 17
#
# $ ./installer/bin/imginfo -f 'PATH_TO_FILE/crash'

## 18

## 19
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/bug'

## 20
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/assert'

## 22
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/00003-jasper-assert-jas_matrix_t'

## 23
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/642.crashes'

## 24
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/00005-jasper-assert-ras_getcmap'

## 25
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/bug'

## 26
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/jasper-heapoverflow-jpc_dec_cp_setfromcox.jp2'

## 27
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/jasper-heapoverflow-jpc_getuint16.jp2'

## 28
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/bug'

## 29
#
# $ ./install/src/appl/jasper --input '/media/sf_Bugs/Jasper/ID-29/PoC1.jpc' --output-format jpc

## 30
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/PoC2.jpc'

## 31
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/bug'

## 32
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/assert-pnm_getsint.mif'

## 33
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/681.crashes'

## 34
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/11.crash'

## 35
#
# $ ./install/src/appl/imginfo -f 'PATH_TO_FILE/12.crash'
