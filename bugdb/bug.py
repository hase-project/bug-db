import os
import shutil
import shlex
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, List, Optional

from hase.record import record_loop

from .utils import REPORT_PATH, ROOT, green_text, red_text


class Bug:
    def __init__(
        self,
        name: str,
        version: str,
        command: List[str],
        stdin_file: Optional[str] = None,
        commit_ids: List[str] = [],
        tempfile_content: Optional[str] = None,
        tempfile_name: str = "file",
    ) -> None:
        self.name = name
        self._command = command
        self.version = version
        self.commit_ids = commit_ids
        self.stdin_file = stdin_file
        self.simulate = False
        self.vars: Dict[str, str] = {}
        self.directory = TemporaryDirectory()
        self.vars["tempdir"] = self.directory.name
        self.report_path = REPORT_PATH.joinpath(f"{self.id()}.tar.gz")

        if tempfile_content is not None:
            path = os.path.join(self.vars["tempdir"], tempfile_name)
            with open(path, "w+") as f:
                f.write(tempfile_content)
            self.vars["tempfile"] = path

    def substitute_vars(self, template: str) -> str:
        s = template
        for k, v in self.vars.items():
            s = s.replace(f"@{k}@", v)
        return s

    def id(self) -> str:
        return f"{self.name}-{self.version}"

    def executable(self) -> str:
        raise NotImplementedError("Has to be implemented")

    def working_directory(self) -> Path:
        return Path(self.directory.name)

    def extra_env(self) -> Dict[str, str]:
        asan_options = [
            "detect_leaks=0",
            "abort_on_error=1",
            "disable_coredump=0",
            "unmap_shadow_on_exit=1",
        ]
        return dict(ASAN_OPTIONS=":".join(asan_options))

    def command(self) -> List[str]:
        executable = self.executable()
        args = list(map(self.substitute_vars, self._command[1:]))
        return [executable] + args

    def run(self, simulate: bool, build_only: bool) -> None:
        if not simulate and self.report_path.exists():
            return

        command = self.command()
        if self.stdin_file is None:
            stdin = None
        else:
            stdin = open(self.substitute_vars(self.stdin_file), "rb")

        working_directory = self.working_directory()
        extra_env = self.extra_env()

        if working_directory is not None:
            print(green_text(f"$ cd {working_directory}"))
        if extra_env is not None:
            export: List[str] = []
            for k, v in extra_env.items():
                export += [f"{k}={shlex.quote(v)}"]
            print(green_text(f"$ export {' '.join(export)}"))
        print(green_text(f"$ {' '.join(command)}"))

        if build_only:
            return

        if not simulate:
            with TemporaryDirectory() as tempdir:
                timeout = 20
                try:
                    recording = record_loop(
                        Path(tempdir),
                        Path(str(ROOT.joinpath("logs"))),
                        limit=1,
                        command=command,
                        timeout=timeout,
                        stdin=stdin,
                        working_directory=working_directory,
                        extra_env=extra_env,
                    )
                    assert recording is not None
                    print(red_text(f"{command[0]} exited with {recording.exit_status}"))
                    if recording.report_path is not None:
                        shutil.move(recording.report_path, self.report_path)
                    else:
                        import pdb; pdb.set_trace()
                except subprocess.TimeoutExpired:
                    print(red_text(f"timeout after {timeout}s"))

    def reproduce(self, build_only: bool = False) -> None:
        try:
            self.pre_hook()
            self.run(self.simulate, build_only)
            self.post_hook()
        finally:
            try:
                self.directory.cleanup()
            except OSError as e:
                print(f"error while removing {self.directory}: {e}")

    def pre_hook(self) -> None:
        pass

    def post_hook(self) -> None:
        pass