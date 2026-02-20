"""Unit tests for validation service (TKT-S02-01)."""

from __future__ import annotations

from simulator.domain.services.validation_service import validate_entity


def test_validation_phase_outputs_deterministic_error_codes() -> None:
    assert validate_entity("application", {"app_id": "a1", "app_name": "App"}) == []
    assert "id_format" in validate_entity("application", {"app_id": "bad id", "app_name": "App"})
