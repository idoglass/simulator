"""GUI run timeline and periodic ON/OFF controller (TKT-S01-02)."""

from __future__ import annotations


class RunMonitorController:
    """Live timeline and periodic toggle controls."""

    def toggle_periodic(self, task_id: str, enabled: bool) -> None:
        pass

    def get_timeline_events(self) -> list:
        return []
