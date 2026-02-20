"""Build final run status: PASS / FAIL / COMPLETE_WITH_FAILURES (TKT-C03-02)."""

from __future__ import annotations

from simulator.domain.models.step_result import StepResult

PASS = "PASS"
FAIL = "FAIL"
COMPLETE_WITH_FAILURES = "COMPLETE_WITH_FAILURES"


def build_run_status(results: list[StepResult], failure_policy: str = "stop") -> str:
    """Compute final run status from step results and policy."""
    failed = [r for r in results if r.verdict == "FAIL"]
    if not failed:
        return PASS
    if failure_policy == "continue":
        return COMPLETE_WITH_FAILURES
    return FAIL
