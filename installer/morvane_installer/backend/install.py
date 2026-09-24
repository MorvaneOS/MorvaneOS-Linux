"""The install itself: turns an InstallConfig into a working system under TARGET.

Each step is a function taking (config, run). install_base and generate_fstab
are done as examples; the rest are stubs with notes on what they need to do.
Test with `python -m morvane_installer --dry-run`: every command gets logged
instead of run, so you can check the sequence without touching a disk.
"""

import os
from collections.abc import Callable

from ..config import InstallConfig
from .run import Runner

TARGET = "/mnt"

# Installed on every system, before the user's app choices.
BASE_PACKAGES = [
    "base",
    "base-devel",
    "runit",
    "elogind-runit",
    "linux",
    "linux-firmware",
    "grub",
    "efibootmgr",
    "dhcpcd",
    "dhcpcd-runit",
    "iwd",
    "iwd-runit",
    "sudo",
    "nano",
]


def is_uefi() -> bool:
    return os.path.isdir("/sys/firmware/efi")


def partition(config: InstallConfig, run: Runner) -> None:
    """Auto mode: wipe config.disk and create the partitions. Manual mode: nothing to do.

    - UEFI: a GPT disk with a ~1 GiB EFI partition (type EF00) and the rest for /.
      BIOS: GPT with a 1 MiB BIOS boot partition (type EF02) for GRUB, then /.
      sgdisk does this non-interactively, e.g. `sgdisk --zap-all DISK` then
      `sgdisk -n 1:0:+1G -t 1:ef00 -n 2:0:0 -t 2:8300 DISK`.
    - Partition names differ: /dev/sda1 but /dev/nvme0n1p1 and /dev/vda1. Look
      them up afterwards (`lsblk -lnpo PATH DISK`) rather than building strings.
    - Remember which partition is which (e.g. in config.mounts) for the next step.
    """
    raise NotImplementedError("partition")


def format_and_mount(config: InstallConfig, run: Runner) -> None:
    """Create filesystems (plus LUKS/LVM if chosen) and mount everything under TARGET.

    - EFI partition: `mkfs.fat -F 32`. Root: `mkfs.ext4` (or btrfs if you add a choice).
    - LUKS: `cryptsetup luksFormat --batch-mode --key-file=- PART` with the passphrase
      as run(..., input=config.passphrase), then `cryptsetup open --key-file=- PART cryptroot`
      and format /dev/mapper/cryptroot instead of the partition.
    - LVM (on the partition or on cryptroot): pvcreate, vgcreate, lvcreate.
    - Mount / at TARGET first, then /boot/efi at TARGET/boot/efi (mkdir -p it).
    """
    raise NotImplementedError("format_and_mount")


def install_base(config: InstallConfig, run: Runner) -> None:
    packages = BASE_PACKAGES + [pkg for app in config.apps for pkg in app.packages]
    if config.encrypt:
        packages += ["cryptsetup", "cryptsetup-runit"]
    if config.lvm:
        packages += ["lvm2", "lvm2-runit"]
    run("basestrap", TARGET, *dict.fromkeys(packages))


def generate_fstab(config: InstallConfig, run: Runner) -> None:
    fstab = run("fstabgen", "-U", TARGET)
    run.write_file(f"{TARGET}/etc/fstab", fstab + "\n", append=True)


def configure_system(config: InstallConfig, run: Runner) -> None:
    """Timezone, locale, keymap and hostname on the new system.

    - Timezone: symlink /usr/share/zoneinfo/<zone> to TARGET/etc/localtime, then
      `hwclock --systohc` in the chroot.
    - Locale: uncomment the locale in TARGET/etc/locale.gen, run locale-gen in the
      chroot, write LANG=<locale> to TARGET/etc/locale.conf.
    - Keymap: KEYMAP=<keymap> in TARGET/etc/vconsole.conf.
    - Hostname: TARGET/etc/hostname, plus a matching 127.0.1.1 line in TARGET/etc/hosts.
    - Add the [morvane] repo to TARGET/etc/pacman.conf, above [system], so the
      new system gets MorvaneOS updates.
    - Encryption/LVM: add the `encrypt` and/or `lvm2` hooks to HOOKS in
      TARGET/etc/mkinitcpio.conf (before `filesystems`) and rerun `mkinitcpio -P`.
    """
    raise NotImplementedError("configure_system")


def create_user(config: InstallConfig, run: Runner) -> None:
    """Create the user with sudo rights.

    - `useradd -m -G wheel -s /bin/bash <user>` in the chroot.
    - Password: `chpasswd` in the chroot with input=f"{user}:{password}\\n" (never
      put a password on the command line; it shows up in the log and in ps).
    - Allow wheel to use sudo: write "%wheel ALL=(ALL:ALL) ALL" to
      TARGET/etc/sudoers.d/wheel with mode 0440.
    """
    raise NotImplementedError("create_user")


def install_bootloader(config: InstallConfig, run: Runner) -> None:
    """Install GRUB and generate its config.

    - UEFI: `grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=MorvaneOS`.
      BIOS: `grub-install --target=i386-pc <disk>`. Both run in the chroot.
    - Encryption: add cryptdevice=UUID=<luks partition uuid>:cryptroot to
      GRUB_CMDLINE_LINUX in TARGET/etc/default/grub first (`blkid -s UUID -o value PART`).
    - Then `grub-mkconfig -o /boot/grub/grub.cfg` in the chroot.
    """
    raise NotImplementedError("install_bootloader")


def enable_services(config: InstallConfig, run: Runner) -> None:
    """Enable runit services on the new system.

    On Artix-style runit, a service is enabled by symlinking /etc/runit/sv/<name>
    into /etc/runit/runsvdir/default/ (inside the new system, so prefix TARGET or
    use the chroot). Enable the base ones (dhcpcd, iwd) plus every
    service in config.apps.
    """
    raise NotImplementedError("enable_services")


def unmount(config: InstallConfig, run: Runner) -> None:
    """`umount -R TARGET`, then close LUKS (`cryptsetup close cryptroot`) if it was used."""
    raise NotImplementedError("unmount")


STEPS: list[tuple[str, Callable[[InstallConfig, Runner], None]]] = [
    ("Partitioning", partition),
    ("Formatting and mounting", format_and_mount),
    ("Installing packages", install_base),
    ("Generating fstab", generate_fstab),
    ("Configuring the system", configure_system),
    ("Creating your account", create_user),
    ("Installing the bootloader", install_bootloader),
    ("Enabling services", enable_services),
    ("Unmounting", unmount),
]


def install(config: InstallConfig, log: Callable[[str], None], dry_run: bool = False) -> None:
    run = Runner(log, dry_run)
    for number, (title, step) in enumerate(STEPS, start=1):
        log(f"==> [{number}/{len(STEPS)}] {title}")
        try:
            step(config, run)
        except NotImplementedError as missing:
            raise RuntimeError(f"step not written yet: backend/install.py {missing}()") from None
