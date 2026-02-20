"""Integration test: periodic parallel flow (TKT-S04-02)."""

from __future__ import annotations

from simulator.domain.services.periodic_scheduler import PeriodicScheduler


def test_scheduler_lifecycle() -> None:
    s = PeriodicScheduler()
    s.start("run-1")
    assert s.is_running("run-1")
    s.stop("run-1")
    assert not s.is_running("run-1")
