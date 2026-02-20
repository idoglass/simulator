"""Validation result (TKT-S02-01)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...]
