from typing import TYPE_CHECKING, ClassVar, cast

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label

from ..config import InstallConfig

if TYPE_CHECKING:
    from ..app import InstallerApp


class StepScreen(Screen[None]):
    """One step of the installer, with Back/Next buttons.

    Subclasses set STEP_TITLE, yield their widgets from compose_body(), and
    implement save() to validate the input and copy it into self.config.
    """

    STEP_TITLE: ClassVar[str] = ""
    NEXT_LABEL: ClassVar[str] = "Next"

    # Start on the first text field, or on Next when there is none. The default
    # focuses the scrollable body, where Enter does nothing.
    AUTO_FOCUS = "Input, #next"

    # The live console has no mouse, so everything must work from the keyboard
    BINDINGS = [
        Binding("ctrl+n", "next", "Next"),
        Binding("ctrl+b", "back", "Back"),
    ]

    @property
    def installer(self) -> "InstallerApp":
        return cast("InstallerApp", self.app)

    @property
    def config(self) -> InstallConfig:
        return self.installer.config

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="body"):
            yield Label(self.STEP_TITLE, classes="step-title")
            yield from self.compose_body()
        with Horizontal(id="nav"):
            # Errors show here, not as a toast: toasts appear over the Next button
            yield Label(id="error")
            yield Button("Back", id="back", disabled=self.installer.step == 0)
            yield Button(self.NEXT_LABEL, id="next", variant="primary")
        yield Footer()

    def compose_body(self) -> ComposeResult:
        """The widgets for this step."""
        yield from ()

    def save(self) -> str | None:
        """Validate the input and store it in self.config.

        Return an error message to stay on this screen, or None to move on.
        """
        return None

    @on(Button.Pressed, "#next")
    def action_next(self) -> None:
        error = self.save()
        self.query_one("#error", Label).update(error or "")
        if not error:
            self.installer.next_step()

    @on(Button.Pressed, "#back")
    def action_back(self) -> None:
        self.installer.previous_step()
