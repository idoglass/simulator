"""Transport config validation: protocol, mode, timeout range (TKT-C05-01)."""

from __future__ import annotations

from simulator.adapters.transport.common.endpoint_parser import parse_endpoint

VALID_PROTOCOLS = ("tcp", "udp")
VALID_MODES = ("client", "server")
TIMEOUT_MS_MIN, TIMEOUT_MS_MAX = 100, 120_000


def validate_transport_config(
    protocol: str,
    mode: str,
    local_endpoint: str = "",
    remote_endpoint: str = "",
    timeout_ms: int = 5000,
) -> list[str]:
    """Return deterministic error codes for invalid config."""
    errors: list[str] = []
    if protocol not in VALID_PROTOCOLS:
        errors.append("SRS-E-TRN-001")
    if mode not in VALID_MODES:
        errors.append("SRS-E-TRN-001")
    if mode == "server" and not local_endpoint:
        errors.append("SRS-E-VAL-005")
    if mode == "client" and not remote_endpoint:
        errors.append("SRS-E-VAL-005")
    if remote_endpoint and parse_endpoint(remote_endpoint) is None:
        errors.append("SRS-E-TRN-001")
    if local_endpoint and parse_endpoint(local_endpoint) is None:
        errors.append("SRS-E-TRN-001")
    if not (TIMEOUT_MS_MIN <= timeout_ms <= TIMEOUT_MS_MAX):
        errors.append("SRS-E-TRN-001")
    return errors
