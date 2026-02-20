"""Transport port contract. Adapters implement TCP/UDP client and server."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from simulator.domain.models.run_models import ObservedInteractions
    from simulator.domain.models.target_and_task import MessageEnvelope, TargetRef


class TransportPort(Protocol):
    """Execute message send/receive for a target over a given protocol."""

    def execute(
        self,
        *,
        target: "TargetRef",
        protocol: str,
        messages: list["MessageEnvelope"],
        timeout_ms: int,
    ) -> "ObservedInteractions": ...
