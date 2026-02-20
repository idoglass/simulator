"""Unit tests for endpoint parser (TKT-C05-01)."""

from __future__ import annotations

from simulator.adapters.transport.common.endpoint_parser import parse_endpoint


def test_parse_valid_endpoint() -> None:
    assert parse_endpoint("127.0.0.1:8080") == ("127.0.0.1", 8080)


def test_parse_invalid_fails_deterministically() -> None:
    assert parse_endpoint("") is None
    assert parse_endpoint("nocolon") is None
    assert parse_endpoint("host:0") is None
    assert parse_endpoint("host:99999") is None
