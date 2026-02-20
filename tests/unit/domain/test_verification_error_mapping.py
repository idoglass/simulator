"""Unit tests for verification error mapping (TKT-C06-02)."""

from __future__ import annotations

from simulator.domain.models.verification_result import VerificationEvidence


def test_failed_verification_includes_code_mapping() -> None:
    e = VerificationEvidence(passed=False, summary="count mismatch", code="SRS-E-VER-001")
    assert e.code == "SRS-E-VER-001"
    assert e.summary == "count mismatch"
