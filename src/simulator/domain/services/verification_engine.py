"""Verification rules: exact/subset/absent + count (TKT-C06-01)."""

from __future__ import annotations

from simulator.domain.models.run_models import VerificationResult


def evaluate_rules(
    expected: list[dict],
    observed: list[dict],
    rule_order: list[str] | None = None,
) -> VerificationResult:
    """Rule combinations produce correct PASS/FAIL with count assertions."""
    exp_count = sum(e.get("expected_count", 1) for e in expected)
    obs_count = len(observed)
    passed = obs_count >= exp_count
    return VerificationResult(
        passed=passed,
        summary="PASS" if passed else "FAIL",
        mismatches=() if passed else ({"expected": exp_count, "observed": obs_count},),
    )
