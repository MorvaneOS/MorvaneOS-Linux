"""Disk discovery helpers."""

import json
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class Disk:
    path: str
    size: int  # bytes
    model: str


def list_disks() -> list[Disk]:
    """Whole disks that could be installed onto (no partitions, CD drives or read-only devices)."""
    try:
        out = subprocess.run(
            ["lsblk", "--json", "--bytes", "--nodeps", "--output", "PATH,SIZE,MODEL,TYPE,RO"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return []
    return [
        Disk(path=dev["path"], size=int(dev["size"]), model=(dev.get("model") or "").strip())
        for dev in json.loads(out)["blockdevices"]
        if dev["type"] == "disk" and not dev["ro"]
    ]


def human_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024 or unit == "TiB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{size} B"
        value /= 1024
    raise AssertionError("unreachable")
