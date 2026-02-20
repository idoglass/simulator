"""Integration test: verification failures (TKT-C06-02)."""

from __future__ import annotations

from simulator.domain.services.verification_engine import evaluate_rules


def test_failed_verification_includes_summary_and_codes() -> None:
    r = evaluate_rules([{"expected_count": 2}], [{}])
    assert r.passed is False
    assert r.summary == "FAIL"
    assert len(r.mismatches) > 0
