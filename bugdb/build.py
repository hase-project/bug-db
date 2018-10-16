import multiprocessing
import os
import re
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile, mkdtemp
from typing import List, Optional
from urllib.parse import urlparse

from .utils import ROOT, blue_text, sh

CPUS = multiprocessing.cpu_count()


class Build:
    def __init__(
        self,
        url: str,
        directory: Path,
        simulate: bool = False,
        skip_auto_reconf: bool = False,
        enable_address_sanitizer: bool = False,
    ) -> None:
        self.url = url
        self.directory = directory
        self.simulate = simulate
        self.skip_auto_reconf = skip_auto_reconf
        self.enable_address_sanitizer = enable_address_sanitizer

        parsed_url = urlparse(url)
        self.archive_name = os.path.basename(parsed_url.path)
        self.archive_path = self.directory.joinpath(self.archive_name)
        match = re.match(r"(.+)\.(tar.gz|tar.xz|zip)$", self.archive_name)
        assert match is not None
        name = match.group(1)
        self.build_directory = name
        self.build_path = self.directory.joinpath(self.build_directory)
        self.build_finished_file = self.build_path.joinpath("build-finished")

    def download(self) -> None:
        if not self.simulate and os.path.exists(self.archive_path):
            return

        tempfile = NamedTemporaryFile(dir=str(ROOT), delete=False)
        try:
            sh(["wget", self.url, "-O", tempfile.name], self.simulate)
            if not self.simulate:
                shutil.move(tempfile.name, self.archive_path)
        except Exception as e:
            os.unlink(tempfile.name)
            raise e


    def cflags(self) -> List[str]:
        flags = ["-g"]
        if self.enable_address_sanitizer:
            flags += ["-fsanitize=address", "-fsanitize=undefined"]
        return flags

    def ldflags(self) -> List[str]:
        if self.enable_address_sanitizer:
            return ["-lasan"]
        else:
            return []

    def configure_flags(self) -> List[str]:
        return []

    def cmake_flags(self) -> List[str]:
        return []

    def unpack(self) -> None:
        self.download()

        if not self.simulate and os.path.exists(self.build_path):
            return

        tempdir: Optional[str] = mkdtemp(prefix=str(ROOT))
        try:
            assert tempdir is not None
            cmd = [
                "tar",
                "--strip-components=1",
                "-xf",
                str(self.archive_path),
                "-C",
                str(tempdir),
            ]
            sh(cmd, self.simulate)
            print(blue_text(f"$ mv '{tempdir}' '{self.build_path}'"))
            if not self.simulate:
                shutil.move(tempdir, self.build_path)
                tempdir = None
        finally:
            if tempdir is not None:
                shutil.rmtree(tempdir)

    def make_flags(self) -> List[str]:
        return [
            f"CFLAGS={' '.join(self.cflags())}",
            f"LDFLAGS={' '.join(self.ldflags())}",
        ]

    def pre_build(self) -> None:
        pass

    def configure(self) -> None:
        build = str(self.build_path)
        if (
            self.build_path.joinpath("configure.ac").exists()
            and not self.skip_auto_reconf
        ):
            sh(
                ["autoreconf", "--install", "--force", "--verbose"],
                self.simulate,
                dir=build,
            )

        if self.build_path.joinpath("CMakeLists.txt").exists():
            sh(
                ["cmake", "-DALLOW_IN_SOURCE_BUILD=1", "."] + self.cmake_flags(),
                self.simulate,
                dir=build,
            )

        if self.build_path.joinpath("configure").exists():
            sh(["sh", "configure"] + self.configure_flags(), self.simulate, dir=build)

    def build(self) -> None:
        self.unpack()

        if not self.simulate and os.path.exists(self.build_finished_file):
            return

        with self.build_path:
            build = str(self.build_path)
            self.pre_build()

            self.configure()

            sh(["make", "-j", str(CPUS)] + self.make_flags(), self.simulate, dir=build)
            if not self.simulate:
                with open(self.build_finished_file, "w+"):
                    pass
