"""Unit tests for redaction (TKT-S03-01)."""

from __future__ import annotations

from simulator.logging.redaction import redact


def test_redact_sensitive_keys() -> None:
    out = redact({"password": "x", "user": "u"})
    assert out["password"] == "[REDACTED]"
    assert out["user"] == "u"


def test_redact_leaves_correlation_ids() -> None:
    out = redact({"run_id": "r1", "task_id": "t1"})
    assert out["run_id"] == "r1"
