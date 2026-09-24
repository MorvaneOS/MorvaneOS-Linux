import subprocess
from typing import TYPE_CHECKING, cast

from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Log

from ..backend.install import install

if TYPE_CHECKING:
    from ..app import InstallerApp


class ProgressScreen(Screen[None]):
    """Runs the install in a background thread and streams its output."""

    @property
    def installer(self) -> "InstallerApp":
        return cast("InstallerApp", self.app)

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="body"):
            yield Label("Installing MorvaneOS…", id="status", classes="step-title")
            yield Log(id="log", auto_scroll=True)
        with Horizontal(id="nav"):
            yield Button("Quit", id="quit", disabled=True)
            yield Button("Reboot", id="reboot", variant="primary", disabled=True)
        yield Footer()

    def on_mount(self) -> None:
        self.run_install()

    @work(thread=True, exclusive=True)
    def run_install(self) -> None:
        def write(line: str) -> None:
            self.app.call_from_thread(self.query_one(Log).write_line, line)

        try:
            install(self.installer.config, write, dry_run=self.installer.dry_run)
        except Exception as error:
            self.app.call_from_thread(self.finish, f"Install failed: {error}", ok=False)
        else:
            self.app.call_from_thread(self.finish, "MorvaneOS is installed!", ok=True)

    def finish(self, message: str, ok: bool) -> None:
        status = self.query_one("#status", Label)
        status.update(message)
        status.styles.color = "green" if ok else "red"
        quit_button = self.query_one("#quit", Button)
        reboot_button = self.query_one("#reboot", Button)
        quit_button.disabled = False
        reboot_button.disabled = not ok or self.installer.dry_run
        (quit_button if reboot_button.disabled else reboot_button).focus()

    @on(Button.Pressed, "#quit")
    def _quit(self) -> None:
        self.app.exit()

    @on(Button.Pressed, "#reboot")
    def _reboot(self) -> None:
        subprocess.run(["loginctl", "reboot"])
