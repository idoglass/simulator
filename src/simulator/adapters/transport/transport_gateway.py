"""Transport gateway: protocol/mode abstraction for TCP/UDP (TKT-C05-02)."""

from __future__ import annotations

from simulator.adapters.transport.composite_transport import CompositeTransportAdapter
from simulator.domain.models.run_models import ObservedInteractions
from simulator.domain.models.target_and_task import MessageEnvelope, TargetRef


class TransportGateway:
    """Gateway delegates to CompositeTransportAdapter for send/receive; mapped errors."""

    def __init__(self) -> None:
        self._adapter = CompositeTransportAdapter()

    def execute(
        self,
        *,
        target: TargetRef,
        protocol: str,
        messages: list[MessageEnvelope],
        timeout_ms: int,
    ) -> ObservedInteractions:
        return self._adapter.execute(
            target=target, protocol=protocol, messages=messages, timeout_ms=timeout_ms
        )
