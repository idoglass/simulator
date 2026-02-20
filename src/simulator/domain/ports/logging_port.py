"""Logging port contract. Adapters implement structured logging with redaction."""

from __future__ import annotations

from typing import Any, Protocol


class LoggingPort(Protocol):
    """Structured logging; correlation fields (run_id, task_id, target_id) and redaction."""

    def info(self, event: str, **fields: Any) -> None: ...
    def warn(self, event: str, **fields: Any) -> None: ...
    def error(self, event: str, **fields: Any) -> None: ...
