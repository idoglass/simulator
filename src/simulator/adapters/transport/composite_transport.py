"""Composite transport: dispatches to TCP or UDP adapter by protocol."""

from __future__ import annotations

from simulator.adapters.transport.tcp.adapter import TcpTransportAdapter
from simulator.adapters.transport.udp.adapter import UdpTransportAdapter
from simulator.domain.models.run_models import ObservedInteractions
from simulator.domain.models.target_and_task import MessageEnvelope, TargetRef


class CompositeTransportAdapter:
    """Implements TransportPort by delegating to TCP or UDP per protocol."""

    def __init__(self) -> None:
        self._tcp = TcpTransportAdapter()
        self._udp = UdpTransportAdapter()

    def execute(
        self,
        *,
        target: TargetRef,
        protocol: str,
        messages: list[MessageEnvelope],
        timeout_ms: int,
    ) -> ObservedInteractions:
        if protocol.lower() == "tcp":
            return self._tcp.execute(target=target, protocol=protocol, messages=messages, timeout_ms=timeout_ms)
        if protocol.lower() == "udp":
            return self._udp.execute(target=target, protocol=protocol, messages=messages, timeout_ms=timeout_ms)
        return ObservedInteractions(
            interactions=(),
            transport_errors=(f"Unsupported protocol {protocol!r}",),
        )
