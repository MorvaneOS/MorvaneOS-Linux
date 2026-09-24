"""Everything the user chooses, collected screen by screen and handed to the backend."""

from dataclasses import dataclass, field
from typing import Literal

from .catalog import AppChoice


@dataclass
class InstallConfig:
    keymap: str = "us"

    # Disk
    mode: Literal["auto", "manual"] = "auto"
    disk: str | None = None  # auto mode: whole disk to erase, e.g. /dev/vda
    mounts: dict[str, str] = field(default_factory=dict)  # manual mode: mountpoint -> partition
    encrypt: bool = False
    passphrase: str = ""
    lvm: bool = False

    # Locale
    timezone: str = "UTC"
    locale: str = "en_US.UTF-8"

    # Accounts
    hostname: str = "morvane"
    username: str = ""
    password: str = ""

    apps: list[AppChoice] = field(default_factory=list)

    def summary(self) -> list[tuple[str, str]]:
        """Human-readable settings for the summary screen. Never includes secrets."""
        if self.mode == "auto":
            extras = [name for name, on in (("encrypted", self.encrypt), ("LVM", self.lvm)) if on]
            disk = f"Erase {self.disk or '(none selected)'}" + (f" ({', '.join(extras)})" if extras else "")
        else:
            disk = ", ".join(f"{mnt} → {part}" for mnt, part in self.mounts.items()) or "(nothing assigned)"
        return [
            ("Keyboard", self.keymap),
            ("Disk", disk),
            ("Timezone", self.timezone),
            ("Locale", self.locale),
            ("Hostname", self.hostname),
            ("User", self.username or "(not set)"),
            ("Apps", ", ".join(app.name for app in self.apps) or "(none)"),
        ]
