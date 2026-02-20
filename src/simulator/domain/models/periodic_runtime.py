"""Periodic task runtime model (TKT-C04-01)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PeriodicTaskRuntime:
    """Per-run periodic task state: enabled, interval, overlap_policy."""

    task_id: str
    run_id: str
    enabled: bool
    interval_ms: int
    overlap_policy: str  # skip | queue | parallel
