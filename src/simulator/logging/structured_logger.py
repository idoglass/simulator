"""Structured logger interface for lifecycle events and correlation metadata (TKT-S03-01)."""

from __future__ import annotations

from typing import Any


def log_event(event: str, level: str = "info", **metadata: Any) -> None:
    """Structured log with correlation metadata; use redaction for sensitive fields."""
    import json
    import logging
    from simulator.logging.redaction import redact
    payload = redact(metadata)
    getattr(logging.getLogger("simulator"), level)("%s %s", event, json.dumps(payload))
