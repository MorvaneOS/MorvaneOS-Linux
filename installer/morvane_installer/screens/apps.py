from textual.app import ComposeResult
from textual.widgets import Static

from ..catalog import load_catalog
from .base import StepScreen


class AppsScreen(StepScreen):
    STEP_TITLE = "Extra apps"

    # TODO: let the user tick apps from the catalog (apps.toml) into self.config.apps.
    #  - load_catalog() returns categories, each with AppChoice entries.
    #  - Textual's SelectionList fits: one per category under a Label, or one
    #    list with the category name in each option's text. Keep the AppChoice as
    #    the option's value, so save() can just read `.selected`.
    #  - Pre-select whatever is already in self.config.apps, so Back keeps choices.

    def compose_body(self) -> ComposeResult:
        names = [f"  {cat.name}: {', '.join(app.name for app in cat.apps)}" for cat in load_catalog()]
        yield Static("Not implemented yet. The catalog has:\n" + "\n".join(names), classes="hint")
