"""Unit tests for error envelope contract (TKT-S02-02)."""

from __future__ import annotations

from simulator.domain.models.error_envelope import ErrorEnvelope
from simulator.domain.services.error_factory import make_error


def test_all_errors_conform_to_envelope_fields() -> None:
    e = make_error("SRS-E-VAL-001", "Invalid", run_id="r1")
    assert e.code == "SRS-E-VAL-001"
    assert e.message == "Invalid"
    assert e.run_id == "r1"
