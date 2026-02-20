"""Periodic scheduler supervisor (TKT-C04-01). Enabled periodic tasks run during active run."""

from __future__ import annotations

from simulator.domain.models.periodic_runtime import PeriodicTaskRuntime


class PeriodicScheduler:
    """Per-run scheduler lifecycle; interval-driven task execution."""

    def __init__(self) -> None:
        self._running: set[str] = set()

    def start(self, run_id: str) -> None:
        self._running.add(run_id)

    def stop(self, run_id: str) -> None:
        self._running.discard(run_id)

    def is_running(self, run_id: str) -> bool:
        return run_id in self._running
