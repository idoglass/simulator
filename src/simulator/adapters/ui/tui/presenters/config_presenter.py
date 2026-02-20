"""TUI config presenter (TKT-S01-03)."""

from __future__ import annotations


class ConfigPresenter:
    """Equivalent CRUD outcomes to GUI."""

    def __init__(self, screen: object) -> None:
        self._screen = screen
