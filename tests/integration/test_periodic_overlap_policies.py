"""Integration test: periodic overlap policies (TKT-C04-02)."""

from __future__ import annotations

from simulator.domain.services.periodic_toggle_service import PeriodicToggleService


def test_toggle_state_applies_immediately() -> None:
    svc = PeriodicToggleService()
    svc.set_enabled("task1", True)
    assert svc.is_enabled("task1") is True
    svc.set_enabled("task1", False)
    assert svc.is_enabled("task1") is False
