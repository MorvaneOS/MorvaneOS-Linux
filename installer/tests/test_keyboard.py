"""The live ISO has no mouse: the whole installer must work from the keyboard alone."""

import asyncio

from morvane_installer.app import STEPS, InstallerApp
from morvane_installer.screens.progress import ProgressScreen
from morvane_installer.screens.user import UserScreen


async def keyboard_only() -> None:
    app = InstallerApp(dry_run=True)
    async with app.run_test(size=(100, 40)) as pilot:
        for step in STEPS:
            await pilot.pause()
            assert isinstance(app.screen, step), f"expected {step.__name__}, got {type(app.screen).__name__}"

            if step is UserScreen:
                # Focus starts in the first field (hostname, pre-filled); Tab through the rest
                await pilot.press("tab", *"alex", "tab", *"secret", "tab", *"secret")
                await pilot.press("ctrl+n")
            else:
                await pilot.press("enter")  # focus starts on Next

        await pilot.pause()
        assert isinstance(app.screen, ProgressScreen)
        assert app.config.username == "alex"

        await app.workers.wait_for_complete()
        await pilot.pause()
        assert app.focused is not None and app.focused.id == "quit"

    # Ctrl+B goes back
    app = InstallerApp(dry_run=True)
    async with app.run_test(size=(100, 40)) as pilot:
        await pilot.press("enter")
        await pilot.pause()
        assert isinstance(app.screen, STEPS[1])
        await pilot.press("ctrl+b")
        await pilot.pause()
        assert isinstance(app.screen, STEPS[0])


def test_keyboard_only() -> None:
    asyncio.run(keyboard_only())
