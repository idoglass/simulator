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

    @staticmethod
    def _redact(fields: dict[str, Any]) -> dict[str, Any]:
        """Placeholder: redact sensitive keys. Extended per logging spec."""
        return dict(fields)
