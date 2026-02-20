"""Unit tests for run event bus (TKT-C01-02)."""

from __future__ import annotations

from simulator.domain.models.run_events import (
    RUN_COMPLETED,
    RUN_STARTED,
    STEP_COMPLETED,
    STEP_STARTED,
)
from simulator.domain.services.run_event_bus import RunEventBus


def test_run_event_bus_publishes_run_and_step_events() -> None:
    """Run/step events are publishable and observable by UI + logging adapters."""
    received: list[dict] = []

    class CapturePort:
        def publish(self, event: dict) -> None:
            received.append(event)

    bus = RunEventBus(CapturePort())
    bus.publish_run_started("run-1", correlation_id="c1")
    bus.publish_step_started("run-1", step_index=0, task_id="task-a")
    bus.publish_step_completed("run-1", step_index=0, task_id="task-a")
    bus.publish_run_completed("run-1", correlation_id="c1")

    assert len(received) == 4
    assert received[0]["event_type"] == RUN_STARTED and received[0]["run_id"] == "run-1"
    assert received[1]["event_type"] == STEP_STARTED and received[1]["step_index"] == 0
    assert received[2]["event_type"] == STEP_COMPLETED
    assert received[3]["event_type"] == RUN_COMPLETED
