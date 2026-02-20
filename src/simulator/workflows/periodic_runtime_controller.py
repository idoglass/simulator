"""Periodic runtime controller: start/stop scheduler for run (TKT-C04-01)."""

from __future__ import annotations

from simulator.domain.services.periodic_scheduler import PeriodicScheduler


def start_periodic_for_run(run_id: str, scheduler: PeriodicScheduler) -> None:
    scheduler.start(run_id)


def stop_periodic_for_run(run_id: str, scheduler: PeriodicScheduler) -> None:
    scheduler.stop(run_id)
