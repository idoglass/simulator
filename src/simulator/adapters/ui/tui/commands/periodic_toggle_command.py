"""TUI periodic toggle command (TKT-S01-04)."""

from __future__ import annotations


def run_periodic_toggle(task_id: str, enabled: bool) -> dict:
    return {"ok": True, "task_id": task_id, "enabled": enabled}
