import os
import shlex
import shutil
import subprocess
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict, List, Optional, Tuple

import angr
from hase.record import record

from .utils import REPORT_PATH, ROOT, Timeout, green_text, red_text


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
        self.by_angr = False
        self.vars = {}  # type: Dict[str, str]
        self.directory = TemporaryDirectory()
        self.vars["tempdir"] = self.directory.name
        self.report_path = REPORT_PATH.joinpath("{}.tar.gz".format(self.id()))

        if tempfile_content is not None:
            path = os.path.join(self.vars["tempdir"], tempfile_name)
            with open(path, "w+") as f:
                f.write(tempfile_content)
            self.vars["tempfile"] = path

    def substitute_vars(self, template: str) -> str:
        s = template
        for k, v in self.vars.items():
            s = s.replace("@{}@".format(k), v)
        return s

    def id(self) -> str:
        return "{}-{}".format(self.name, self.version)

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
        return dict(
            ASAN_OPTIONS=":".join(asan_options),
            UBSAN_OPTIONS="abort_on_error=1:halt_on_error=1:print_stacktrace=1",
        )

    def command(self) -> List[str]:
        executable = self.executable()
        args = list(map(self.substitute_vars, self._command[1:]))
        return [executable] + args

    def run_by_angr(self) -> None:
        self.directory.cleanup()
        proj = angr.Project(self.executable())
        state = proj.factory.full_init_state(args=self.command())
        simgr = proj.factory.simulation_manager(state)
        timeout = 60 * 60
        with Timeout(timeout) as _:
            try:
                current_time = time.time()
                simgr.run()
            except TimeoutError:
                print(red_text("{}: Angr simulation timeout".format(self.name)))
                with open(
                    str(REPORT_PATH.joinpath("{}.txt".format(self.name))), "w+"
                ) as f:
                    f.write("time: >{}s".format(timeout))
            except Exception as e:
                print(red_text("{}: Angr simulation error {}".format(self.name, e)))
                with open(
                    str(REPORT_PATH.joinpath("{}.txt".format(self.name))), "w+"
                ) as f:
                    f.write("time: error {}".format(e))
            else:
                time_diff = time.time() - current_time
                print(green_text("{}: Execution time {}s".format(self.name, time_diff)))
                with open(
                    str(REPORT_PATH.joinpath("{}.txt".format(self.name))), "w+"
                ) as f:
                    f.write("time: {}s".format(time_diff))
                import pdb

                pdb.set_trace()

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
            print(green_text("$ cd {}".format(working_directory)))
        if extra_env is not None:
            export = []  # type: List[str]
            for k, v in extra_env.items():
                export += ["{}={}".format(k, shlex.quote(v))]
            print(green_text("$ export {}".format(" ".join(export))))
        print(green_text("$ {}".format(" ".join(command))))

        if build_only:
            return

        if not simulate:
            with TemporaryDirectory() as tempdir:
                timeout = 20
                try:
                    recording = record(
                        record_path=Path(tempdir),
                        log_path=Path(str(ROOT.joinpath("logs"))),
                        limit=1,
                        target=command,
                        timeout=timeout,
                        stdin=stdin,
                        working_directory=working_directory,
                        extra_env=extra_env,
                    )
                    assert recording is not None
                    print(
                        red_text(
                            "{} exited with {}".format(
                                command[0], recording.exit_status
                            )
                        )
                    )
                    if recording.report_path is not None:
                        shutil.move(recording.report_path, str(self.report_path))
                    else:
                        import pdb

                        pdb.set_trace()
                except subprocess.TimeoutExpired:
                    print(red_text("timeout after {}s".format(timeout)))
        else:
            if self.by_angr:
                self.run_by_angr()

    def measure(self) -> Tuple[int, Any]:
        command = self.command()
        if self.stdin_file is None:
            stdin = None
        else:
            stdin = open(self.substitute_vars(self.stdin_file), "rb")

        working_directory = self.working_directory()
        extra_env = self.extra_env()

        with TemporaryDirectory() as tempdir:
            timeout = 20
            try:
                recording = record(
                    record_path=Path(tempdir),
                    log_path=Path(str(ROOT.joinpath("logs"))),
                    limit=1,
                    target=command,
                    timeout=timeout,
                    stdin=stdin,
                    working_directory=working_directory,
                    extra_env=extra_env,
                )
                assert recording is not None
                print(
                    red_text(
                        "{} exited with {}".format(command[0], recording.exit_status)
                    )
                )
                if recording.report_path is not None:
                    shutil.move(recording.report_path, str(self.report_path))

                return (recording.exit_status, recording.rusage)
            except subprocess.TimeoutExpired:
                print(red_text("timeout after {}s".format(timeout)))
                return (-1, None)

    def run_without_hase(self) -> Tuple[int, Any]:
        command = self.command()
        if self.stdin_file is None:
            stdin = None
        else:
            stdin = open(self.substitute_vars(self.stdin_file), "rb")

        working_directory = self.working_directory()
        extra_env = self.extra_env()

        with TemporaryDirectory() as tempdir:
            timeout = 20
            try:
                process = subprocess.Popen(
                    command, stdin=stdin, cwd=str(working_directory), env=extra_env
                )
                _, exit_status, rusage = os.wait4(process.pid, 0)
                print(red_text("{} exited with {}".format(command[0], exit_status)))

                return (exit_status, rusage)
            except subprocess.TimeoutExpired:
                print(red_text("timeout after {}s".format(timeout)))
                return (-1, None)

    def reproduce(self, build_only: bool = False) -> None:
        try:
            self.pre_hook()
            self.run(self.simulate, build_only)
            self.post_hook()
        finally:
            try:
                self.directory.cleanup()
            except OSError as e:
                print("error while removing {}: {}".format(self.directory, e))

    def benchmark(self) -> Tuple[int, Any]:
        try:
            self.pre_hook()
            data = self.measure()
            self.post_hook()
        finally:
            try:
                self.directory.cleanup()
            except OSError as e:
                print("error while removing {}: {}".format(self.directory, e))

        return data

    def pre_hook(self) -> None:
        pass

    def post_hook(self) -> None:
        pass
