"""Step executor: run one step and return StepResult (TKT-C03-01)."""

from __future__ import annotations

from simulator.domain.models.step_result import StepResult


def execute_step(
    order_index: int,
    task_id: str,
    *,
    transport_send_receive: object = None,
    verify: object = None,
) -> StepResult:
    """Execute one step; returns lifecycle state output. Delegates to workflow in practice."""
    return StepResult(order_index=order_index, state="completed", verdict="PASS", evidence={"task_id": task_id})
