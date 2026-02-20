"""Unit tests for verification rules (TKT-C06-01)."""

from __future__ import annotations

from simulator.domain.services.verification_engine import evaluate_rules


def test_rule_combinations_produce_pass_fail() -> None:
    r = evaluate_rules([{"expected_count": 1}], [{"x": 1}])
    assert r.passed is True
    r2 = evaluate_rules([{"expected_count": 2}], [{"x": 1}])
    assert r2.passed is False
