"""TCP transport adapter (client and server). Implements TransportPort."""

from __future__ import annotations

import socket
from typing import TYPE_CHECKING

from simulator.domain.models.run_models import ObservedInteractions
from simulator.domain.models.target_and_task import MessageEnvelope, TargetRef

if TYPE_CHECKING:
    pass


def _serialize_message(msg: MessageEnvelope) -> bytes:
    """MVP: simple newline-terminated JSON-like payload for smoke tests."""
    body = str(msg.payload)
    return (body + "\n").encode("utf-8")


class TcpTransportAdapter:
    """TCP client and server. Client: connect, send, receive. Server: bind, accept, recv, send."""

    def execute(
        self,
        *,
        target: TargetRef,
        protocol: str,
        messages: list[MessageEnvelope],
        timeout_ms: int,
    ) -> ObservedInteractions:
        if protocol.lower() != "tcp":
            return ObservedInteractions(
                interactions=(),
                transport_errors=(f"TCP adapter does not support protocol {protocol!r}",),
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
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout_sec)
            sock.connect((target.host, target.port))
            for msg in messages:
                if msg.direction == "send":
                    data = _serialize_message(msg)
                    sock.sendall(data)
                    interactions.append({"direction": "send", "message_type": msg.message_type})
                elif msg.direction == "receive":
                    try:
                        buf = sock.recv(4096)
                        if buf:
                            interactions.append({"direction": "receive", "raw_len": len(buf)})
                    except socket.timeout:
                        errors.append("TRANSPORT_READ_TIMEOUT")
            sock.close()
        except socket.timeout:
            errors.append("TRANSPORT_CONNECT_TIMEOUT")
        except ConnectionRefusedError:
            errors.append("TRANSPORT_CONNECTION_REFUSED")
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
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.settimeout(timeout_sec)
            server.bind((target.host, target.port))
            server.listen(1)
            conn, _ = server.accept()
            conn.settimeout(timeout_sec)
            for msg in messages:
                if msg.direction == "send":
                    conn.sendall(_serialize_message(msg))
                    interactions.append({"direction": "send", "message_type": msg.message_type})
                elif msg.direction == "receive":
                    try:
                        buf = conn.recv(4096)
                        if buf:
                            interactions.append({"direction": "receive", "raw_len": len(buf)})
                    except socket.timeout:
                        errors.append("TRANSPORT_READ_TIMEOUT")
            conn.close()
            server.close()
        except (socket.timeout, OSError) as e:
            errors.append(f"TRANSPORT_ERROR:{e!s}")
        return ObservedInteractions(
            interactions=tuple(interactions),
            transport_errors=tuple(errors),
        )
