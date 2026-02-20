"""Console logging adapter. Implements LoggingPort with structured event + fields."""

from __future__ import annotations

import json
import logging
from typing import Any


class ConsoleLoggingAdapter:
    """Structured logging to console. Redaction of sensitive fields can be extended later."""

    def __init__(self, name: str = "simulator") -> None:
        self._logger = logging.getLogger(name)

    def info(self, event: str, **fields: Any) -> None:
        self._logger.info("%s %s", event, json.dumps(self._redact(fields)))

    def warn(self, event: str, **fields: Any) -> None:
        self._logger.warning("%s %s", event, json.dumps(self._redact(fields)))

    def error(self, event: str, **fields: Any) -> None:
        self._logger.error("%s %s", event, json.dumps(self._redact(fields)))

    _REDACT_KEYS = frozenset(
        {"password", "secret", "token", "api_key", "apikey", "authorization", "cookie"}
    )

    @classmethod
    def _redact(cls, fields: dict[str, Any]) -> dict[str, Any]:
        """Redact sensitive keys per logging spec; leave correlation IDs (run_id, task_id, target_id)."""
        out: dict[str, Any] = {}
        for k, v in fields.items():
            key_lower = k.lower()
            if any(r in key_lower for r in cls._REDACT_KEYS):
                out[k] = "[REDACTED]"
            else:
                out[k] = v
        return out
