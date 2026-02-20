"""Adapter scaffolding template."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AdapterContext:
    run_id: str
    target_id: str
    task_id: str


class ExampleAdapter:
    """Template adapter implementation.

    Keep translation logic here; avoid embedding core business rules.
    """

    def __init__(self, logger: Any) -> None:
        self._logger = logger

    def execute(self, *, context: AdapterContext, payload: dict[str, object]) -> dict[str, object]:
        try:
            # TODO: translate external API/protocol interaction here.
            result = {"ok": True, "code": "OK", "data": payload}
            self._logger.info("ADAPTER_EXECUTED", run_id=context.run_id, target_id=context.target_id)
            return result
        except Exception as exc:  # pragma: no cover - template behavior
            self._logger.error("ADAPTER_FAILED", run_id=context.run_id, error=str(exc))
            return {
                "ok": False,
                "code": "ADAPTER_EXECUTION_FAILED",
                "message": "Adapter operation failed.",
            }

