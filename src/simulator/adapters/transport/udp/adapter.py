"""UDP transport adapter (client and server). Implements TransportPort."""

from __future__ import annotations

import socket
from typing import TYPE_CHECKING

from simulator.domain.models.run_models import ObservedInteractions
from simulator.domain.models.target_and_task import MessageEnvelope, TargetRef

if TYPE_CHECKING:
    pass


def _serialize_message(msg: MessageEnvelope) -> bytes:
    """MVP: simple payload for smoke tests."""
    body = str(msg.payload)
    return (body + "\n").encode("utf-8")


class UdpTransportAdapter:
    """UDP client and server. Client: sendto, recvfrom. Server: bind, recvfrom, sendto."""

    def execute(
        self,
        *,
        target: TargetRef,
        protocol: str,
        messages: list[MessageEnvelope],
        timeout_ms: int,
    ) -> ObservedInteractions:
        if protocol.lower() != "udp":
            return ObservedInteractions(
                interactions=(),
                transport_errors=(f"UDP adapter does not support protocol {protocol!r}",),
            )
        timeout_sec = max(0.001, timeout_ms / 1000.0)
        if target.mode == "server":
            return self._run_server(target, messages, timeout_sec)
        return self._run_client(target, messages, timeout_sec)

    def _run_client(
        self, target: TargetRef, messages: list[MessageEnvelope], timeout_sec: float
    ) -> ObservedInteractions:
        interactions: list[dict[str, object]] = []
        errors: list[str] = []
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout_sec)
            addr = (target.host, target.port)
            for msg in messages:
                if msg.direction == "send":
                    sock.sendto(_serialize_message(msg), addr)
                    interactions.append({"direction": "send", "message_type": msg.message_type})
                elif msg.direction == "receive":
                    try:
                        buf, _ = sock.recvfrom(4096)
                        if buf:
                            interactions.append({"direction": "receive", "raw_len": len(buf)})
                    except socket.timeout:
                        errors.append("TRANSPORT_READ_TIMEOUT")
            sock.close()
        except OSError as e:
            errors.append(f"TRANSPORT_ERROR:{e!s}")
        return ObservedInteractions(
            interactions=tuple(interactions),
            transport_errors=tuple(errors),
        )

    def _run_server(
        self, target: TargetRef, messages: list[MessageEnvelope], timeout_sec: float
    ) -> ObservedInteractions:
        interactions: list[dict[str, object]] = []
        errors: list[str] = []
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout_sec)
            sock.bind((target.host, target.port))
            for msg in messages:
                if msg.direction == "receive":
                    try:
                        buf, peer = sock.recvfrom(4096)
                        if buf:
                            interactions.append({"direction": "receive", "raw_len": len(buf)})
                            if messages and messages[0].direction == "send":
                                sock.sendto(_serialize_message(messages[0]), peer)
                    except socket.timeout:
                        errors.append("TRANSPORT_READ_TIMEOUT")
                elif msg.direction == "send":
                    pass  # response sent in receive branch for request/response
            sock.close()
        except OSError as e:
            errors.append(f"TRANSPORT_ERROR:{e!s}")
        return ObservedInteractions(
            interactions=tuple(interactions),
            transport_errors=tuple(errors),
        )
