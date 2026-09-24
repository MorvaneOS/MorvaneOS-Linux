"""Clicks through the installer headlessly in dry-run mode.

Run from the installer/ folder: python -m pytest tests
"""

import asyncio

from textual.widgets import Input, Label

from morvane_installer.app import STEPS, InstallerApp
from morvane_installer.screens.progress import ProgressScreen
from morvane_installer.screens.user import UserScreen


async def walk_through() -> None:
    app = InstallerApp(dry_run=True)
    async with app.run_test(size=(100, 40)) as pilot:
        for step in STEPS:
            await pilot.pause()
            assert isinstance(app.screen, step), f"expected {step.__name__}, got {type(app.screen).__name__}"

            if step is UserScreen:
                # Invalid first: the screen must refuse to continue
                await pilot.click("#next")
                await pilot.pause()
                assert isinstance(app.screen, UserScreen)
                assert "Username" in str(app.screen.query_one("#error", Label).render())

                await pilot.pause(0.5)  # Button ignores presses during its click animation
                app.screen.query_one("#username", Input).value = "alex"
                app.screen.query_one("#password", Input).value = "secret"
                app.screen.query_one("#confirm", Input).value = "secret"

            await pilot.click("#next")

        await pilot.pause()
        assert isinstance(app.screen, ProgressScreen)
        await app.workers.wait_for_complete()
        await pilot.pause()

        status = str(app.screen.query_one("#status", Label).render())
        assert "step not written yet" in status, status
        assert app.config.username == "alex"


def test_walk_through() -> None:
    asyncio.run(walk_through())
