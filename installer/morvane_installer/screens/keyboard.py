from textual.app import ComposeResult
from textual.widgets import Static

from .base import StepScreen


class KeyboardScreen(StepScreen):
    STEP_TITLE = "Keyboard layout"

    # TODO: let the user pick a console keymap and store it in self.config.keymap.
    #  - The available keymaps are the files under /usr/share/kbd/keymaps/**/*.map.gz;
    #    the keymap name is the file name without .map.gz (e.g. "uk", "de-latin1").
    #  - Textual's Select or OptionList widgets fit well; with hundreds of entries,
    #    an Input to filter the list helps.
    #  - Nice touch: apply the choice live with `loadkeys <name>` so the user can
    #    type with it on the next screens (skip that when self.installer.dry_run).
    #  - Copy the structure of screens/user.py: compose_body() + save().

    def compose_body(self) -> ComposeResult:
        yield Static("Not implemented yet: using the US layout.", classes="hint")
