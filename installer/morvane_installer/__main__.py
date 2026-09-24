import argparse

from . import __version__
from .app import InstallerApp


def main() -> None:
    parser = argparse.ArgumentParser(prog="morvane-install", description="Install MorvaneOS.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the commands the install would run instead of running them",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args()

    InstallerApp(dry_run=args.dry_run).run()


if __name__ == "__main__":
    main()
