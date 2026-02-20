"""Deterministic sequence step runner by order_index (TKT-C03-01)."""

from __future__ import annotations

from simulator.domain.models.step_result import StepResult
from simulator.workflows.step_executor import execute_step


def run_sequence(steps: list[dict[str, object]]) -> list[StepResult]:
    """Execute steps strictly by order_index; return lifecycle state per step."""
    ordered = sorted(steps, key=lambda s: s.get("order_index", 0))
    results: list[StepResult] = []
    for i, step in enumerate(ordered):
        idx = step.get("order_index", i)
        task_ref = step.get("task_ref", "")
        results.append(execute_step(idx, task_ref))
    return results
