from textual.app import ComposeResult
from textual.widgets import Static

from .base import StepScreen


class SummaryScreen(StepScreen):
    STEP_TITLE = "Ready to install"
    NEXT_LABEL = "Install"

    def compose_body(self) -> ComposeResult:
        rows = "\n".join(f"  [b]{key}:[/b] {value}" for key, value in self.config.summary())
        yield Static(rows)
        if self.config.mode == "auto" and self.config.disk:
            yield Static(f"\n[b red]Everything on {self.config.disk} will be erased.[/]")
        yield Static("\nPress Install to start, or Back to change something.", classes="hint")

    def on_mount(self) -> None:
        self.query_one("#next").variant = "error"
