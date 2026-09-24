from textual.app import ComposeResult
from textual.widgets import Static

from ..backend.disk import human_size, list_disks
from .base import StepScreen


class DiskScreen(StepScreen):
    STEP_TITLE = "Disk"

    # TODO: the partitioning screen. It fills in the disk fields of self.config.
    #
    # Auto mode ("Erase disk"):
    #  - list_disks() already returns the candidate disks; show them in a
    #    RadioSet or OptionList and store the path in self.config.disk.
    #  - Two Checkboxes: "Encrypt the disk" (self.config.encrypt) and
    #    "Use LVM" (self.config.lvm). When encrypting, ask for a passphrase twice
    #    (two Inputs with password=True, like screens/user.py).
    #  - Leave out the disk the live ISO booted from: it's the one holding the
    #    partition labelled ARTIX_<yyyymm> (see `lsblk -o PATH,LABEL`).
    #
    # Manual mode:
    #  - A button that suspends the TUI and runs cfdisk on the chosen disk:
    #        with self.app.suspend():
    #            subprocess.run(["cfdisk", disk])
    #  - Then ask which partition is / (required), /boot/efi (required on UEFI:
    #    check os.path.isdir("/sys/firmware/efi")) and optionally swap, and store
    #    them in self.config.mounts, e.g. {"/": "/dev/vda2", "/boot/efi": "/dev/vda1"}.
    #
    # save() must refuse to continue until a disk (auto) or at least "/" (manual) is set.

    def compose_body(self) -> ComposeResult:
        disks = list_disks()
        lines = [f"  {d.path}  {human_size(d.size)}  {d.model}" for d in disks] or ["  (no disks found)"]
        yield Static("Not implemented yet. Disks found:\n" + "\n".join(lines), classes="hint")
