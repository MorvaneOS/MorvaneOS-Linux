from textual.app import ComposeResult
from textual.widgets import Static

from .base import StepScreen


class LocaleScreen(StepScreen):
    STEP_TITLE = "Timezone and language"

    # TODO: pick self.config.timezone and self.config.locale.
    #  - Timezones: zoneinfo.available_timezones() from the standard library gives
    #    names like "Europe/London". A Select with a filter Input works; or two
    #    Selects, region then city.
    #  - Locales: the UTF-8 entries in /usr/share/i18n/SUPPORTED (first column,
    #    e.g. "en_GB.UTF-8"). The backend writes the choice to /etc/locale.gen and
    #    /etc/locale.conf on the new system.

    def compose_body(self) -> ComposeResult:
        yield Static("Not implemented yet: using UTC and en_US.UTF-8.", classes="hint")
