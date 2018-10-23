from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import PIPE
from typing import Optional

from .utils import sh


def get_library_path(simulate: bool = False) -> Optional[Path]:
    with TemporaryDirectory() as d:
        c_source = Path(d).joinpath("main.c")
        c_prog = Path(d).joinpath("main")
        with open(c_source, "w+") as f:
            f.write("void main() { }")
        sh(["cc", "-lasan", str(c_source), "-o", str(c_prog)], dir=d, simulate=simulate)
        result = sh(["ldd", str(c_prog)], simulate=simulate, stdin=PIPE)
        if result is None:
            return None
        import pdb

        pdb.set_trace()
        print("foo")

    return None
