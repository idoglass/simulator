"""Integration test: failure policy continue on fail (TKT-C03-02)."""

from __future__ import annotations

from simulator.domain.models.step_result import StepResult
from simulator.domain.services.run_summary_builder import COMPLETE_WITH_FAILURES, build_run_status


def test_continue_on_fail_returns_complete_with_failures() -> None:
    results = [StepResult(0, "completed", "FAIL"), StepResult(1, "completed", "PASS")]
    assert build_run_status(results, failure_policy="continue") == COMPLETE_WITH_FAILURES
