"""Example step: a complete screen to copy the pattern from.

1. compose_body() yields the widgets, pre-filled from self.config so Back keeps input.
2. save() validates, returns an error message or stores the values and returns None.
"""

import re

from textual.app import ComposeResult
from textual.widgets import Input, Label

from .base import StepScreen

USERNAME = re.compile(r"^[a-z_][a-z0-9_-]{0,31}$")
HOSTNAME = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$")


class UserScreen(StepScreen):
    STEP_TITLE = "Your account"

    def compose_body(self) -> ComposeResult:
        yield Label("Computer name", classes="field-label")
        yield Input(self.config.hostname, id="hostname")
        yield Label("Username", classes="field-label")
        yield Input(self.config.username, placeholder="lowercase, e.g. alex", id="username")
        yield Label("Password", classes="field-label")
        yield Input(self.config.password, password=True, id="password")
        yield Label("Confirm password", classes="field-label")
        yield Input(self.config.password, password=True, id="confirm")

    def save(self) -> str | None:
        hostname = self.query_one("#hostname", Input).value.strip()
        username = self.query_one("#username", Input).value.strip()
        password = self.query_one("#password", Input).value
        confirm = self.query_one("#confirm", Input).value

        if not HOSTNAME.match(hostname):
            return "Computer name can only use letters, numbers and dashes (max 63)."
        if not USERNAME.match(username):
            return "Username must start with a lowercase letter and use only a-z, 0-9, _ and -."
        if username == "root":
            return "Pick a username other than root."
        if not password:
            return "Enter a password."
        if password != confirm:
            return "The passwords don't match."

        self.config.hostname = hostname
        self.config.username = username
        self.config.password = password
        return None
