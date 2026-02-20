"""TUI run presenter (TKT-S01-04)."""

from __future__ import annotations


class RunPresenter:
    """Toggle periodic tasks and show runtime status fields."""

    def __init__(self, screen: object) -> None:
        self._screen = screen
