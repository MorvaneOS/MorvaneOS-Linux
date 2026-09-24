"""The optional apps offered on the Apps screen, loaded from apps.toml."""

import tomllib
from dataclasses import dataclass, field
from importlib.resources import files


@dataclass(frozen=True)
class AppChoice:
    name: str
    packages: tuple[str, ...]
    services: tuple[str, ...] = ()  # runit services to enable on the installed system


@dataclass(frozen=True)
class Category:
    name: str
    apps: tuple[AppChoice, ...] = field(default_factory=tuple)


def load_catalog() -> list[Category]:
    data = tomllib.loads(files(__package__).joinpath("apps.toml").read_text())
    return [
        Category(
            name=category["name"],
            apps=tuple(
                AppChoice(
                    name=app["name"],
                    packages=tuple(app["packages"]),
                    services=tuple(app.get("services", ())),
                )
                for app in category.get("apps", [])
            ),
        )
        for category in data.get("category", [])
    ]
