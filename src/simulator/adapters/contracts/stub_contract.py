"""Stub contract adapter: accepts all messages; full .h/ctypes validation can be added later."""

from __future__ import annotations

from typing import Any

from simulator.domain.models.target_and_task import MessageEnvelope


class StubContractAdapter:
    """Implements ContractPort. MVP: no-op load; validate passes. Extend for .h/ctypes validation."""

    def load_sources(self, sources: list[dict[str, Any]]) -> dict[str, Any]:
        """Load contract sources. Stub returns empty bundle."""
        return {"sources": sources, "types": {}}

    def validate_message(self, message: MessageEnvelope, bundle: dict[str, Any]) -> dict[str, Any]:
        """Validate message against bundle. Stub: pass. Full impl rejects invalid type/field refs."""
        return {"valid": True, "errors": []}
