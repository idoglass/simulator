"""Run event bus: publish run/step/scheduler events via EventBusPort (TKT-C01-02)."""

from __future__ import annotations

from typing import Any

from simulator.domain.models.run_events import (
    RUN_COMPLETED,
    RUN_STARTED,
    SCHEDULER_STARTED,
    SCHEDULER_STOPPED,
    STEP_COMPLETED,
    STEP_STARTED,
)
from simulator.domain.ports.event_bus_port import EventBusPort


class RunEventBus:
    """Publishes run lifecycle and step events for UI and logging adapters."""

    def __init__(self, port: EventBusPort) -> None:
        self._port = port

    def publish_run_started(self, run_id: str, correlation_id: str | None = None, payload: dict[str, Any] | None = None) -> None:
        self._port.publish({
            "event_type": RUN_STARTED,
            "run_id": run_id,
            "correlation_id": correlation_id,
            **(payload or {}),
        })

    def publish_run_completed(self, run_id: str, correlation_id: str | None = None, payload: dict[str, Any] | None = None) -> None:
        self._port.publish({
            "event_type": RUN_COMPLETED,
            "run_id": run_id,
            "correlation_id": correlation_id,
            **(payload or {}),
        })

    def publish_step_started(self, run_id: str, step_index: int, task_id: str, correlation_id: str | None = None, payload: dict[str, Any] | None = None) -> None:
        self._port.publish({
            "event_type": STEP_STARTED,
            "run_id": run_id,
            "step_index": step_index,
            "task_id": task_id,
            "correlation_id": correlation_id,
            **(payload or {}),
        })

    def publish_step_completed(self, run_id: str, step_index: int, task_id: str, correlation_id: str | None = None, payload: dict[str, Any] | None = None) -> None:
        self._port.publish({
            "event_type": STEP_COMPLETED,
            "run_id": run_id,
            "step_index": step_index,
            "task_id": task_id,
            "correlation_id": correlation_id,
            **(payload or {}),
        })

    def publish_scheduler_started(self, run_id: str, correlation_id: str | None = None, payload: dict[str, Any] | None = None) -> None:
        self._port.publish({
            "event_type": SCHEDULER_STARTED,
            "run_id": run_id,
            "correlation_id": correlation_id,
            **(payload or {}),
        })

    def publish_scheduler_stopped(self, run_id: str, correlation_id: str | None = None, payload: dict[str, Any] | None = None) -> None:
        self._port.publish({
            "event_type": SCHEDULER_STOPPED,
            "run_id": run_id,
            "correlation_id": correlation_id,
            **(payload or {}),
        })
