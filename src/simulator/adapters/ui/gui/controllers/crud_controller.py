"""GUI CRUD controller for core entities (TKT-S01-01)."""

from __future__ import annotations


class CrudController:
    """Create/edit/delete applications, targets, contracts, tasks, transports, messages, expectations, sequences."""

    def create_entity(self, entity_type: str, data: dict) -> dict:
        return {"ok": True, "id": data.get("id", "new")}

    def get_validation_feedback(self, entity_type: str, data: dict) -> list[str]:
        return []
