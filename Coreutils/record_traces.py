#!/usr/bin/env python

import multiprocessing
import os
import shlex
import shutil
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Dict, List, Optional

from hase import path
from hase.record import record_loop

ROOT = Path(__file__).resolve().parent
REPORT_PATH = ROOT.joinpath("reports")
COREUTILS_VERSION_PATH = ROOT.joinpath("versions")
CPUS = multiprocessing.cpu_count()


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
):
    if verbose:
        args = " ".join(map(lambda s: shlex.quote(s), cmd[1:]))
        if dir is not None:
            print(blue_text("$ cd %s" % (dir)), file=sys.stderr)
        print(blue_text("$ %s %s" % (cmd[0], args)), file=sys.stderr)
    if not simulate:
        if dir is not None:
            with cd(dir):
                return subprocess.check_call(cmd)
        else:
            return subprocess.check_call(cmd)


# 6.10

## commit-id: https://github.com/coreutils/coreutils/commit/d701f6abb73e36721de5df083df4769786a14528
# 	echo > $(BINPATH)/foobar; \
# 	sudo $(HASEBIN) record -- $(BINPATH)/tac -r $(BINPATH)/foobar $(BINPATH)/foobar; \
# 	rm -f $(BINPATH)/foorbar
#
## commit-id: https://github.com/coreutils/coreutils/commit/72d052896a9092b811961a8f3e6ca5d151a59be5
## commit-id: https://github.com/coreutils/coreutils/commit/eb8fa94f2cf030d625c12ad68bb8883de204c196
# record-mkdir:
# 	sudo $(HASEBIN) record -- $(BINPATH)/mkdir -Z invalid-selinux-context foobar
#
## commit-id: https://github.com/coreutils/coreutils/commit/7cb24684cc4ef96bb25dfc1c819acfc3b98d9442
# record-sha512sum:
# 	echo 'SHA512 (' > $(BINPATH)/foobar; \
# 	sudo $(HASEBIN) record -- $(BINPATH)/sha512sum -c < $(BINPATH)/foobar; \
# 	rm -f $(BINPATH)/foobar
#
## commit-id: https://github.com/coreutils/coreutils/commit/a0851554bd52038ed47e46ee521ce74a5a09f747
# record-ptx:
# 	echo > $(BINPATH)/A01234567890123456789012345678901234567890123456789; \
# 	sudo $(HASEBIN) record -- $(BINPATH)/ptx -F'\' $(BINPATH)/A01234567890123456789012345678901234567890123456789; \
# 	rm -f $(BINPATH)/A01234567890123456789012345678901234567890123456789
#
## commit-id: https://github.com/coreutils/coreutils/commit/b58a8b4ef588ec8a365b920d12e27fdd71aa48d1
# 	sudo $(HASEBIN) record -- $(BINPATH)/paste -d'\' 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
#
## commid-id: https://github.com/coreutils/coreutils/commit/f926f7ce0e0a224ef3a37a82e60fd3d7aaca906e
# record-stty:
# 	sudo $(HASEBIN) record -- $(BINPATH)/stty eol -F /dev/tty

# 7.2

# commit-id: https://github.com/coreutils/coreutils/commit/25eb4c69097ca4f5665b050cfa4247a19ffd8c55
# 	touch $(BINPATH)/foobar; \
# 	sudo $(HASEBIN) record -- $(BINPATH)/sort -m -o $(BINPATH)/foobar $(BINPATH)/foobar; \
# 	rm -f $(BINPATH)/foobar

# 8.22

# commit-id: https://github.com/coreutils/coreutils/commit/fb13cdc727541adef0010279f770f2afa358002e
# record-shuf:
# 	sudo $(HASEBIN) record -- $(BINPATH)/shuf -i 0-0 1
#
## commit-id: https://github.com/coreutils/coreutils/commit/0093ac8d57a0f1a16fd09d98f6a524dddb6053e7
# record-ln:
# 	sudo $(HASEBIN) record -- $(BINPATH)/ln -sr '' F
#
## commit-id: https://github.com/coreutils/coreutils/commit/a4faa6a0a3ae93c01d036d830ae7a21b74913baf
# record-date:
# 	sudo $(HASEBIN) record -- $(BINPATH)/date --date='TZ="""'

# 8.27
## commit-id: https://github.com/coreutils/coreutils/commit/9287ef2b1707e2a222f8ae776ce3785abcb16fba
# record-date:
# 	tz_long=$(printf '%2000s' | tr ' ' a); \
# 	sudo $(HASEBIN) record -- $(BINPATH)/date -d "TZ=\"${tz_long}0\" 2017"
#
## commit-id: https://github.com/coreutils/coreutils/commit/cc19f63be3ad0f27c9ea7f223883b75917fda7fb
# record-b2sum:
# 	echo "BLAKE2" > $(BINPATH)/foobar; \
# 	sudo $(HASEBIN) record -- $(BINPATH)/b2sum -c < $(BINPATH)/foobar; \
# 	rm -f $(BINPATH)/foobar


class Coreutils:
    def __init__(self, version: str, simulate: bool = False) -> None:
        self.version = version
        self.simulate = simulate
        self.build_directory = f"coreutils-{self.version}"
        self.build_path = COREUTILS_VERSION_PATH.joinpath(self.build_directory)
        self.build_finished_file = self.build_path.joinpath("build-finished")

        version_list = list(map(int, version.split(".")))

        if version_list >= [6, 12]:
            ext = "tar.xz"
        else:
            ext = "tar.gz"

        self.archive_name = f"{self.build_directory}.{ext}"
        self.archive_path = COREUTILS_VERSION_PATH.joinpath(self.archive_name)

    def download(self) -> None:
        url = f"http://ftp.gnu.org/gnu/coreutils/{self.archive_name}"

        if not self.simulate and os.path.exists(self.archive_path):
            return

        tempfile = NamedTemporaryFile(dir=str(ROOT), delete=False)
        try:
            sh(["wget", url, "-O", tempfile.name], self.simulate)
            if not self.simulate:
                shutil.move(tempfile.name, self.archive_path)
        except Exception as e:
            os.unlink(tempfile.name)
            raise e

    def extract(self) -> None:
        self.download()

        if not self.simulate and os.path.exists(self.build_path):
            return

        with TemporaryDirectory(dir=str(ROOT)) as tempdir:
            sh(["tar", "-xf", str(self.archive_path), "-C", tempdir], self.simulate)
            if not self.simulate:
                shutil.move(
                    os.path.join(tempdir, self.build_directory), self.build_path
                )

    def build(self) -> None:
        self.extract()

        if not self.simulate and os.path.exists(self.build_finished_file):
            return

        with self.build_path:
            build = str(self.build_path)
            sh(["./configure"], self.simulate, dir=build)
            sh(["make", "-j", str(CPUS), "CFLAGS=-g"], self.simulate, dir=build)
            if not self.simulate:
                with open(self.build_finished_file, "w+"):
                    pass


class Bug:
    def __init__(
        self,
        name: str,
        version: str,
        command: List[str],
        stdin_file: Optional[str] = None,
        commit_ids: List[str] = [],
        simulate: bool = False,
    ) -> None:
        self.name = name
        self._command = command
        self.version = version
        self.commit_ids = commit_ids
        self.stdin_file = stdin_file
        self.vars: Dict[str, str] = {}
        self.directory = TemporaryDirectory()
        self.vars["tempdir"] = self.directory.name
        self.report_path = REPORT_PATH.joinpath(f"{self.id()}.tar.gz")

    def substitute_vars(self, template: str) -> str:
        s = template
        for k, v in self.vars.items():
            s = s.replace(f"@{k}@", v)
        return s

    def id(self) -> str:
        return f"coreutils-{self.version}-{self.name}"

    def command(self):
        exe = self._command[0]
        coreutils = Coreutils(self.version)
        command = f"{coreutils.build_path}/src/{exe}"
        args = list(map(self.substitute_vars, self._command[1:]))
        return [command] + args

    def run(self, simulate: bool) -> None:
        if not simulate and self.report_path.exists():
            return

        command = self.command()
        if self.stdin_file is None:
            stdin = None
        else:
            stdin = open(self.substitute_vars(self.stdin_file), "rb")

        print(green_text("$ " + " ".join(command)))

        if not simulate:
            with TemporaryDirectory() as tempdir:
                timeout = 3
                try:
                    recording = record_loop(
                        path.Path(tempdir),
                        path.Path(str(ROOT.joinpath("logs"))),
                        limit=1,
                        command=command,
                        timeout=timeout,
                        stdin=stdin,
                    )
                    assert recording is not None
                    print(red_text(f"{command[0]} exited with {recording.exit_status}"))
                    if recording.report_path is not None:
                        shutil.move(recording.report_path, self.report_path)
                except subprocess.TimeoutExpired:
                    print(red_text(f"timeout after {timeout}s"))

    def reproduce(self, simulate: bool = False) -> None:
        self.pre_hook()
        self.run(simulate)
        self.post_hook()

        try:
            self.directory.cleanup()
        except OSError as e:
            print(f"error while removing {self.directory}: {e}")

    def pre_hook(self) -> None:
        pass

    def post_hook(self) -> None:
        pass


def create_setups() -> List[Bug]:
    bugs: List[Bug] = []

    class TacBug(Bug):
        def pre_hook(self):
            self.vars["tempfile"] = os.path.join(self.vars["tempdir"], "foobar")
            with open(self.vars["tempfile"], "w+") as f:
                f.write("\n")

    bugs.append(
        TacBug(
            "tac",
            version="6.10",
            commit_ids=["d701f6abb73e36721de5df083df4769786a14528"],
            command=["tac", "-r", "@tempfile@", "@tempfile@"],
        )
    )

    bugs.append(
        Bug(
            "mkdir",
            version="6.10",
            commit_ids=[
                "72d052896a9092b811961a8f3e6ca5d151a59be5",
                "eb8fa94f2cf030d625c12ad68bb8883de204c196",
            ],
            command=["mkdir", "-Z", "invalid-selinux-context", "@tempdir@/path"],
        )
    )

    class SHA512Bug(Bug):
        def pre_hook(self):
            self.vars["tempfile"] = os.path.join(self.vars["tempdir"], "foobar")
            with open(self.vars["tempfile"], "w+") as f:
                f.write("SHA512 (\n")

    bugs.append(
       SHA512Bug(
           "sha512sum",
           version="6.10",
           commit_ids=[
               "72d052896a9092b811961a8f3e6ca5d151a59be5",
               "eb8fa94f2cf030d625c12ad68bb8883de204c196",
           ],
           command=["sha512sum", "-c", "@tempfile@"],
       )
    )

    class PTXBug(Bug):
        def pre_hook(self):
            self.vars["tempfile"] = os.path.join(
                self.vars["tempdir"],
                "A01234567890123456789012345678901234567890123456789",
            )
            with open(self.vars["tempfile"], "w+") as f:
                f.write("\n")

    bugs.append(
        PTXBug(
            "ptx",
            version="6.10",
            commit_ids=["a0851554bd52038ed47e46ee521ce74a5a09f747"],
            command=["ptx", "-F\\", "@tempfile@"],
        )
    )

    bugs.append(
        Bug(
            "paste",
            version="6.10",
            commit_ids=[],
            command=[
                "paste",
                "-d\\",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            ],
        )
    )
    bugs.append(
        Bug(
            "stty",
            version="6.10",
            commit_ids=[],
            command=["stty", "eol", "-F", "/dev/tty"],
        )
    )

    class SortBug(Bug):
        def pre_hook(self):
            self.vars["tempfile"] = os.path.join(self.vars["tempdir"], "foobar")
            with open(self.vars["tempfile"], "w+") as f:
                f.write("\n")

    bugs.append(
        SortBug(
            "sort",
            version="7.2",
            commit_ids=["25eb4c69097ca4f5665b050cfa4247a19ffd8c55"],
            command=["sort", "-m", "-o", "@tempfile@", "@tempfile@"],
        )
    )

    bugs.append(
        Bug(
            "shuf",
            version="8.22",
            commit_ids=["fb13cdc727541adef0010279f770f2afa358002e"],
            command=["shuf", "-i", "0-0", "1"],
        )
    )

    bugs.append(
        Bug(
            "ln",
            version="8.22",
            commit_ids=["0093ac8d57a0f1a16fd09d98f6a524dddb6053e7"],
            command=["ln", "-sr", "", "F"],
        )
    )

    bugs.append(
        Bug(
            "date",
            version="8.22",
            commit_ids=["a4faa6a0a3ae93c01d036d830ae7a21b74913baf"],
            command=["date", '--date=TZ="""'],
        )
    )
    bugs.append(
        Bug(
            "date",
            version="8.27",
            commit_ids=["9287ef2b1707e2a222f8ae776ce3785abcb16fba"],
            command=["date", "-d", f"TZ=\"{'a' * 2001}0\" 2017"],
        )
    )

    class B2SumBug(Bug):
        def pre_hook(self):
            self.vars["tempfile"] = os.path.join(
                self.vars["tempdir"],
                "foobar",
            )
            with open(self.vars["tempfile"], "w+") as f:
                f.write("BLAKE2\n")

    bugs.append(
        B2SumBug(
            "b2sum",
            version="8.27",
            commit_ids=["9287ef2b1707e2a222f8ae776ce3785abcb16fba"],
            command=["b2sum", "-c", "@tempfile@"],
        )
    )

    return bugs


def main():
    os.makedirs(COREUTILS_VERSION_PATH, exist_ok=True)
    os.makedirs(REPORT_PATH, exist_ok=True)
    os.environ["FORCE_UNSAFE_CONFIGURE"] = "1"
    # nixos shenanigans
    os.environ["hardeningDisable"] = "all"
    bugs = create_setups()

    simulate = False
    for bug in bugs:
        coreutils = Coreutils(bug.version, simulate)
        coreutils.build()
        bug.reproduce(simulate)


if __name__ == "__main__":
    main()
