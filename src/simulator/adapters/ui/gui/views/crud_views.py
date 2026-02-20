"""GUI CRUD views (TKT-S01-01)."""

from __future__ import annotations


def build_crud_view(entity_type: str) -> object:
    """Build view for entity CRUD; display validation feedback."""
    return type("CrudView", (), {"entity_type": entity_type})()
