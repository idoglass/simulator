"""Toggle periodic task ON/OFF at runtime (TKT-C04-02)."""

from __future__ import annotations


class PeriodicToggleService:
    """Toggle state applies immediately; overlap behavior matches policy."""

    def __init__(self) -> None:
        self._enabled: dict[str, bool] = {}

    def set_enabled(self, task_id: str, enabled: bool) -> None:
        self._enabled[task_id] = enabled

    def is_enabled(self, task_id: str) -> bool:
        return self._enabled.get(task_id, False)
