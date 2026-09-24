from textual.app import App

from .config import InstallConfig
from .screens.apps import AppsScreen
from .screens.base import StepScreen
from .screens.disk import DiskScreen
from .screens.keyboard import KeyboardScreen
from .screens.locale import LocaleScreen
from .screens.progress import ProgressScreen
from .screens.summary import SummaryScreen
from .screens.user import UserScreen
from .screens.welcome import WelcomeScreen

# The installer's steps, in order. Add, remove or reorder screens here.
STEPS: list[type[StepScreen]] = [
    WelcomeScreen,
    KeyboardScreen,
    DiskScreen,
    LocaleScreen,
    UserScreen,
    AppsScreen,
    SummaryScreen,
]


class InstallerApp(App[None]):
    TITLE = "MorvaneOS Installer"
    CSS_PATH = "installer.tcss"

    def __init__(self, dry_run: bool = False) -> None:
        super().__init__()
        self.config = InstallConfig()
        self.dry_run = dry_run
        self.step = 0
        if dry_run:
            self.sub_title = "dry run: nothing will be changed"

    def on_mount(self) -> None:
        self.push_screen(STEPS[0]())

    def next_step(self) -> None:
        if self.step == len(STEPS) - 1:
            self.switch_screen(ProgressScreen())
            return
        self.step += 1
        self.switch_screen(STEPS[self.step]())

    def previous_step(self) -> None:
        if self.step > 0:
            self.step -= 1
            self.switch_screen(STEPS[self.step]())
