"""Run lifecycle and step event payload types (TKT-C01-02)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


# Event type constants for run/step/scheduler
RUN_STARTED = "run_started"
RUN_COMPLETED = "run_completed"
STEP_STARTED = "step_started"
STEP_COMPLETED = "step_completed"
SCHEDULER_STARTED = "scheduler_started"
SCHEDULER_STOPPED = "scheduler_stopped"


@dataclass(frozen=True)
class RunEventPayload:
    """Base run event with correlation and run identifiers."""

    run_id: str
    correlation_id: str | None = None
    payload: dict[str, Any] | None = None


@dataclass(frozen=True)
class StepEventPayload:
    """Step-level event for UI and logging observers."""

    run_id: str
    step_index: int
    task_id: str
    correlation_id: str | None = None
    payload: dict[str, Any] | None = None
