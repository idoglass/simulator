"""Endpoint parser: host:port validation (TKT-C05-01)."""

from __future__ import annotations


def parse_endpoint(value: str) -> tuple[str, int] | None:
    """Parse host:port; port 1..65535. Returns (host, port) or None if invalid."""
    if not value or ":" not in value:
        return None
    try:
        host, port_s = value.rsplit(":", 1)
        port = int(port_s)
        if 1 <= port <= 65535:
            return (host.strip(), port)
    except ValueError:
        pass
    return None
