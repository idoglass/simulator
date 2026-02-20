"""Redaction utility for sensitive fields in logs (TKT-S03-01)."""

from __future__ import annotations

from typing import Any

REDACT_KEYS = frozenset(
    {"password", "secret", "token", "api_key", "apikey", "authorization", "cookie"}
)


def redact(fields: dict[str, Any]) -> dict[str, Any]:
    """Redact sensitive keys; leave correlation IDs (run_id, task_id, target_id)."""
    out: dict[str, Any] = {}
    for k, v in fields.items():
        if any(r in k.lower() for r in REDACT_KEYS):
            out[k] = "[REDACTED]"
        else:
            out[k] = v
    return out
