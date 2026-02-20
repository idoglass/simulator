"""Integration: periodic toggle (TKT-C04-02)."""
from simulator.domain.services.periodic_toggle_service import PeriodicToggleService

def test_toggle() -> None:
    s = PeriodicToggleService()
    s.set_enabled("t1", True)
    assert s.is_enabled("t1")
