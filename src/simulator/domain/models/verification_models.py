"""Verification rule models (TKT-C06-01)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VerificationRule:
    """Single rule: exact | subset | absent + count assertion."""

    rule_type: str  # exact | subset | absent
    expected_count: int = 1
    comparison: str = ">="  # >= | == | <=
