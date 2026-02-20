"""E2E TUI CRUD smoke (TKT-S01-03)."""

from simulator.adapters.ui.tui.screens.config_screen import ConfigScreen


def test_tui_crud_smoke() -> None:
    s = ConfigScreen()
    assert s.run_crud_flow("app", "create").get("ok") is True
