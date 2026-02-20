"""GUI CRUD presenter (TKT-S01-01)."""

from __future__ import annotations


class CrudPresenter:
    """Bridge view and controller; display validation feedback."""

    def __init__(self, controller: object, view: object) -> None:
        self._controller = controller
        self._view = view
