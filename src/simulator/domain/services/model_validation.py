"""SRS schema validators (TKT-C02-01). ID regex, name length, ranges."""

from __future__ import annotations

from simulator.domain.models.simulation_entities import ID_REGEX


def validate_id(value: str) -> list[str]:
    """Validate ID field per SRS 3.1. Returns list of error messages."""
    errors: list[str] = []
    if not value or not isinstance(value, str):
        errors.append("id_required")
        return errors
    if not ID_REGEX.match(value):
        errors.append("id_format")
    return errors


def validate_name(value: str, min_len: int = 1, max_len: int = 128) -> list[str]:
    """Validate name field: trimmed, non-empty, length 1..max. Returns list of errors."""
    errors: list[str] = []
    if not isinstance(value, str):
        errors.append("name_type")
        return errors
    trimmed = value.strip()
    if len(trimmed) < min_len:
        errors.append("name_empty")
    if len(trimmed) > max_len:
        errors.append("name_too_long")
    return errors


def validate_timeout_ms(value: int, low: int = 100, high: int = 120_000) -> list[str]:
    """Validate timeout in ms range."""
    errors: list[str] = []
    if not isinstance(value, int) or value < low or value > high:
        errors.append("timeout_out_of_range")
    return errors


def validate_endpoint(value: str) -> list[str]:
    """Validate endpoint format host:port, port 1..65535."""
    errors: list[str] = []
    if not value or ":" not in value:
        errors.append("endpoint_format")
        return errors
    try:
        host, port_s = value.rsplit(":", 1)
        port = int(port_s)
        if port < 1 or port > 65535:
            errors.append("endpoint_port_range")
    except ValueError:
        errors.append("endpoint_format")
    return errors
