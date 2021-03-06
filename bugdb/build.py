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
        skip_cmake: bool = False,
        enable_address_sanitizer: bool = False,
        enable_ubsan_sanitizer: Optional[bool] = None,
    ) -> None:
        self.url = url
        self.directory = directory
        self.simulate = simulate
        self.skip_auto_reconf = skip_auto_reconf
        self.skip_cmake = skip_cmake
        self.enable_address_sanitizer = enable_address_sanitizer
        if enable_ubsan_sanitizer is not None:
            # backwards compatible
            self.enable_ubsan_sanitizer = enable_address_sanitizer
        else:
            self.enable_ubsan_sanitizer = False

        parsed_url = urlparse(url)
        self.archive_name = os.path.basename(parsed_url.path)
        self.archive_path = self.directory.joinpath(self.archive_name)
        match = re.match(r"(.+)\.(tar.gz|tar.xz|zip)$", self.archive_name)
        assert match is not None
        name = match.group(1)
        self.build_directory = Path(name)
        self.build_path = self.directory.joinpath(self.build_directory)
        self.build_finished_file = self.build_path.joinpath("build-finished")

    def source_directory(self) -> Path:
        return Path(".")

    def source_path(self) -> Path:
        return self.build_path.joinpath(self.source_directory())

    def download(self) -> None:
        if not self.simulate and self.archive_path.exists():
            return
        self.archive_path.parent.mkdir(exist_ok=True)
        tempfile = NamedTemporaryFile(dir=str(ROOT), delete=False)
        try:
            sh(["wget", self.url, "-O", tempfile.name], self.simulate)
            if not self.simulate:
                shutil.move(tempfile.name, str(self.archive_path))
        except Exception as e:
            os.unlink(tempfile.name)
            raise e

    def cflags(self) -> List[str]:
        flags = ["-g"]
        if self.enable_address_sanitizer:
            flags.append("-fsanitize=address")
        if self.enable_ubsan_sanitizer:
            flags.append("-fsanitize=undefined")
        return flags

    def ldflags(self) -> List[str]:
        flags = []
        if self.enable_address_sanitizer:
            flags.append("-lasan")
        if self.enable_ubsan_sanitizer:
            flags.append("-lubsan")
        return flags

    def configure_flags(self) -> List[str]:
        return []

    def cmake_flags(self) -> List[str]:
        return []

    def strip_components(self) -> int:
        return 1

    def unpack(self) -> None:
        self.download()

        if not self.simulate and self.build_path.exists():
            return

        tempdir = mkdtemp(prefix=str(ROOT))  # type: Optional[str]
        try:
            assert tempdir is not None
            cmd = [
                "tar",
                "--strip-components={}".format(self.strip_components()),
                "-xf",
                str(self.archive_path),
                "-C",
                str(tempdir),
            ]
            sh(cmd, self.simulate)
            print(blue_text("$ mv '{}' '{}'".format(tempdir, self.build_path)))
            if not self.simulate:
                shutil.move(tempdir, str(self.build_path))
                tempdir = None
        finally:
            if tempdir is not None:
                shutil.rmtree(tempdir)

    def make_flags(self) -> List[str]:
        return [
            "CFLAGS={}".format(" ".join(self.cflags())),
            "LDFLAGS={}".format(" ".join(self.ldflags())),
        ]

    def pre_build(self) -> None:
        pass

    def post_build(self) -> None:
        pass

    def configure(self) -> None:
        if (
            not self.skip_auto_reconf
            and self.source_path().joinpath("configure.ac").exists()
        ):
            sh(
                ["autoreconf", "--install", "--force", "--verbose"],
                self.simulate,
                dir=self.source_path(),
            )

        if (
            not self.skip_cmake
            and self.source_path().joinpath("CMakeLists.txt").exists()
        ):
            sh(
                ["cmake", "-DALLOW_IN_SOURCE_BUILD=1", "."] + self.cmake_flags(),
                self.simulate,
                dir=self.source_path(),
            )

        if self.source_path().joinpath("configure").exists():
            sh(
                ["sh", "configure"] + self.configure_flags(),
                self.simulate,
                dir=self.source_path(),
            )

    def build(self) -> None:
        self.unpack()

        if not self.simulate and self.build_finished_file.exists():
            return

        with self.build_path:
            self.pre_build()

            self.configure()

            sh(
                ["make", "-j", str(CPUS)] + self.make_flags(),
                self.simulate,
                dir=self.source_path(),
            )
            if not self.simulate:
                with open(str(self.build_finished_file), "w+"):
                    pass

            self.post_build()
