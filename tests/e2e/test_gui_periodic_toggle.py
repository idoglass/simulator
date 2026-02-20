"""E2E GUI periodic toggle (TKT-S01-02)."""

from simulator.adapters.ui.gui.controllers.run_monitor_controller import RunMonitorController


def test_gui_periodic_toggle() -> None:
    c = RunMonitorController()
    c.toggle_periodic("t1", True)
    assert isinstance(c.get_timeline_events(), list)
