"""Contract port: load and validate .h/ctypes message structures."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from simulator.domain.models.target_and_task import MessageEnvelope


class ContractPort(Protocol):
    """Load contract sources and validate messages against them. Invalid type/field refs rejected."""

    def load_sources(self, sources: list[dict[str, Any]]) -> dict[str, Any]: ...
    def validate_message(self, message: "MessageEnvelope", bundle: dict[str, Any]) -> dict[str, Any]: ...
