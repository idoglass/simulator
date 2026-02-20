"""TUI CRUD commands (TKT-S01-03)."""

from __future__ import annotations


def create_command(entity_type: str, data: dict) -> dict:
    return {"ok": True}


def list_command(entity_type: str) -> list:
    return []
