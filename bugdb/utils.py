import os
import shlex
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = ROOT.joinpath("reports")


def blue_text(s: str) -> str:
    return "\x1b[34m%s\x1b[0m" % s


def red_text(s: str) -> str:
    return "\x1b[31m%s\x1b[0m" % s


def green_text(s: str) -> str:
    return "\x1b[32m%s\x1b[0m" % s


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def sh(
    cmd: List[str],
    simulate: bool = False,
    verbose: bool = True,
    dir: Optional[str] = None,
    extra_env: Dict[str, str] = None,
):
    if verbose:
        args = " ".join(map(lambda s: shlex.quote(s), cmd[1:]))
        if dir is not None:
            print(blue_text("$ cd %s" % (dir)), file=sys.stderr)
        print(blue_text("$ %s %s" % (cmd[0], args)), file=sys.stderr)

    env = None
    if extra_env is not None:
        env = os.environ.copy()
        env.update(extra_env)

    if not simulate:
        return subprocess.run(cmd, cwd=dir, check=True, env=env)
