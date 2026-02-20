"""Integration test: failure policy stop on fail (TKT-C03-02)."""

from __future__ import annotations

from simulator.domain.models.step_result import StepResult
from simulator.domain.services.run_summary_builder import FAIL, build_run_status


def test_stop_on_fail_returns_fail() -> None:
    results = [StepResult(0, "completed", "PASS"), StepResult(1, "completed", "FAIL")]
    assert build_run_status(results, failure_policy="stop") == FAIL
