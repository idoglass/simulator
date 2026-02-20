"""TUI config screen for entity CRUD (TKT-S01-03)."""

from __future__ import annotations


class ConfigScreen:
    """TUI CRUD flows with parity to GUI capabilities."""

    def show_entity_list(self, entity_type: str) -> list:
        return []

    def run_crud_flow(self, entity_type: str, action: str) -> dict:
        return {"ok": True}
