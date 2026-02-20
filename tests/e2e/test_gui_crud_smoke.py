"""E2E GUI CRUD smoke (TKT-S01-01)."""

from simulator.adapters.ui.gui.controllers.crud_controller import CrudController


def test_gui_crud_smoke() -> None:
    c = CrudController()
    assert c.create_entity("app", {"id": "a1"}).get("ok") is True
