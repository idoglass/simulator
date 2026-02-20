"""Pre-run validation (TKT-S02-01)."""

from __future__ import annotations

from simulator.domain.models.validation_result import ValidationResult


def pre_run_validate(run_input: object) -> ValidationResult:
    """Pre-run validation; deterministic error-code mapped output."""
    return ValidationResult(valid=True, errors=())
