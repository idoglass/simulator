"""Log event schema: required fields for lifecycle events (TKT-S03-01)."""

from __future__ import annotations

from typing import Any

REQUIRED_CORRELATION = ("run_id",)


def validate_log_event(event: str, fields: dict[str, Any]) -> list[str]:
    """Ensure lifecycle events include correlation metadata where required."""
    errors: list[str] = []
    for key in REQUIRED_CORRELATION:
        if key not in fields and "run" in event.lower():
            errors.append(f"missing_{key}")
    return errors
