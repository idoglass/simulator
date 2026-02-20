"""E2E TUI periodic toggle (TKT-S01-04)."""

from __future__ import annotations

from simulator.adapters.ui.tui.screens.run_screen import RunScreen


def test_tui_can_toggle_periodic_and_show_status() -> None:
    screen = RunScreen()
    r = screen.toggle_periodic("task1", True)
    assert r.get("ok") is True
    assert screen.show_runtime_status() is not None
