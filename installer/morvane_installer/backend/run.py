"""Running commands for the install, with live output and a dry-run mode."""

import shlex
import subprocess
from collections.abc import Callable
from pathlib import Path


class CommandError(Exception):
    def __init__(self, cmd: tuple[str, ...], code: int) -> None:
        super().__init__(f"`{shlex.join(cmd)}` exited with status {code}")


class Runner:
    """Runs commands and sends every line of output to `log`.

    In dry-run mode nothing is executed or written: commands and file writes
    are only logged, so the whole install can be walked through safely.
    """

    def __init__(self, log: Callable[[str], None], dry_run: bool) -> None:
        self.log = log
        self.dry_run = dry_run

    def __call__(self, *cmd: str, input: str | None = None, check: bool = True) -> str:
        """Run a command and return its output.

        `input` is fed to stdin and never logged, so use it for passwords
        (chpasswd, cryptsetup --key-file=-).
        """
        self.log("$ " + shlex.join(cmd))
        if self.dry_run:
            return ""

        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE if input is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if input is not None:
            assert proc.stdin
            proc.stdin.write(input)
            proc.stdin.close()

        output = []
        assert proc.stdout
        for line in proc.stdout:
            line = line.rstrip("\n")
            output.append(line)
            self.log(line)

        code = proc.wait()
        if check and code != 0:
            raise CommandError(cmd, code)
        return "\n".join(output)

    def chroot(self, target: str, *cmd: str, input: str | None = None) -> str:
        """Run a command inside the new system."""
        return self("artix-chroot", target, *cmd, input=input)

    def write_file(self, path: str | Path, content: str, append: bool = False) -> None:
        self.log(f"{'>>' if append else '>'} {path}")
        if self.dry_run:
            for line in content.splitlines():
                self.log(f"    {line}")
            return
        with open(path, "a" if append else "w") as f:
            f.write(content)
