from textual.app import ComposeResult
from textual.widgets import Static

from .base import StepScreen


class WelcomeScreen(StepScreen):
    STEP_TITLE = "Welcome to MorvaneOS"

    def compose_body(self) -> ComposeResult:
        yield Static(
            "This installer sets up MorvaneOS on this computer.\n\n"
            "You'll choose a keyboard layout, a disk, your timezone and locale, "
            "create your user account, and pick any extra apps. Nothing is changed "
            "until you confirm on the summary screen.\n\n"
            "An internet connection is needed: packages are downloaded during the install."
        )
