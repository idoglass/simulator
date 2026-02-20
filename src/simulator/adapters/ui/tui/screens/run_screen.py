"""TUI run monitor screen (TKT-S01-04)."""

from __future__ import annotations


class RunScreen:
    """Run monitor and periodic ON/OFF command."""

    def show_runtime_status(self) -> dict:
        return {}

    def toggle_periodic(self, task_id: str, enabled: bool) -> dict:
        return {"ok": True}
