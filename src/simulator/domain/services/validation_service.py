"""Centralized validation pipeline: CRUD-time, pre-run, runtime (TKT-S02-01)."""

from __future__ import annotations

from simulator.domain.services.model_validation import validate_id, validate_name


def validate_entity(entity_type: str, data: dict) -> list[str]:
    """Validation phase outputs deterministic error codes."""
    errors: list[str] = []
    if entity_type == "application":
        errors.extend(validate_id(data.get("app_id", "")))
        errors.extend(validate_name(data.get("app_name", "")))
    return errors
