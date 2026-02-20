"""Unit tests for sequence runner order (TKT-C03-01)."""

from __future__ import annotations

from simulator.workflows.sequence_runner import run_sequence


def test_steps_execute_strictly_by_order_index() -> None:
    steps = [{"order_index": 2, "task_ref": "b"}, {"order_index": 1, "task_ref": "a"}]
    results = run_sequence(steps)
    assert len(results) == 2
    assert results[0].order_index == 1
    assert results[1].order_index == 2
