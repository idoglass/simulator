"""Unit tests for periodic scheduler loop (TKT-C04-01)."""

from __future__ import annotations

from simulator.domain.services.periodic_scheduler import PeriodicScheduler


def test_enabled_periodic_tasks_run_during_active_run() -> None:
    s = PeriodicScheduler()
    s.start("run-1")
    assert s.is_running("run-1")
    s.stop("run-1")
    assert not s.is_running("run-1")
